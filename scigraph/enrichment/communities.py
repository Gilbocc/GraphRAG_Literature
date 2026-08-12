"""Community detection over Claim nodes via Neo4j GDS, plus LLM summaries.

Detection runs on the Claim projection only — chunks, evidence,
and claim nodes are excluded, so communities describe scientific themes rather
than document structure.
"""

from __future__ import annotations

import hashlib
import logging
from concurrent.futures import ThreadPoolExecutor

from graphdatascience import GraphDataScience
from neo4j.exceptions import ClientError

from ..config import Config
from ..graph.store import GraphStore
from ..llm.openrouter import StructuredLLM
from ..models import CommunitySummary

log = logging.getLogger(__name__)

GRAPH_NAME = "conceptGraph"

# A summary is a title, a paragraph and a few themes. Asking for the pipeline's
# 32000-token default made each call reserve capacity it never used, and this
# provider queues on the reservation: the same call took 8.9s at 32000 and 0.2s
# at 800. Eight of them at once turned that into 70-87s each.
SUMMARY_MAX_TOKENS = 2000


# Members plus the claims and papers that touch them: the summarizer's context.


SUMMARY_SYSTEM = """\
You summarize a community of related scientific concepts detected in a corpus of
research papers. Describe what actually unites this cluster and what the papers
collectively say about it. Ground every statement in the concepts and claims
given; do not introduce outside knowledge. If the cluster is incoherent, say so
plainly in the summary rather than inventing a theme.
"""

SUMMARY_USER = """\
Claims in this community:
{concepts}

Claims made about these concepts:
{claims}

Papers involved:
{papers}
"""


def _fingerprint(members: list[str]) -> str:
    """Identity of a community's membership, order-independent.

    A summary is written from one exact set of claims and is only true of that
    set, so this is what decides whether it survives a re-run rather than the
    community id, which is stable even when membership shifts underneath it.
    """
    return hashlib.sha256("|".join(sorted(members)).encode()).hexdigest()[:16]


def _usable_levels(depth: int) -> list[int]:
    """Which levels of the dendrogram are worth keeping.

    Neither end is. Level 0 is what Leiden starts from — mostly pairs and
    singletons, and at ten papers it left over half the linked claims in groups
    too small to keep. The final level is where merging stopped, which on a
    single-domain corpus is close to "everything": one 89-claim community drawn
    from nine of ten papers.

    The middle is where the themes are, and taking it by position rather than
    by size means this does not need retuning as the corpus grows — Leiden adds
    levels as the graph gets bigger, and the fragmentary bottom and degenerate
    top stay at the ends.
    """
    if depth <= 1:
        return [0]
    if depth == 2:
        return [0]
    return list(range(1, depth - 1))


def _drop_graph(gds: GraphDataScience) -> None:
    if gds.graph.exists(GRAPH_NAME)["exists"]:
        gds.graph.drop(GRAPH_NAME)


def detect_communities(store: GraphStore, cfg: Config) -> dict[str, int]:
    """Build the cross-paper claim graph, then run Leiden or Louvain over it.

    The kNN is rebuilt here rather than at the end of ingest because it reads
    claim embeddings, and ingest runs before `embed`. Built there it silently
    skipped every claim the ingest had just created: four new papers added 128
    claims and none of them could join a community, so detection reported "5
    communities over 361 claims" while actually partitioning the 233 older ones.
    """
    store.build_claim_graph()
    gds = GraphDataScience(store.driver, database=store.database)
    algorithm = cfg.community_algorithm.lower()
    if algorithm not in {"leiden", "louvain"}:
        raise ValueError(f"COMMUNITY_ALGORITHM must be 'leiden' or 'louvain', got {algorithm!r}")

    _drop_graph(gds)
    graph, _ = gds.graph.project(
        GRAPH_NAME,
        {"Claim": {"properties": []}},
        # Both algorithms need an undirected graph.
        {"RELATED_CLAIM": {"orientation": "UNDIRECTED", "properties": ["weight"]}},
    )

    try:
        if graph.node_count() == 0:
            log.warning("No Claim nodes projected; skipping community detection")
            return {"communities": 0, "nodes": 0}

        runner = gds.leiden if algorithm == "leiden" else gds.louvain
        # Seeded and single-threaded, because GDS only guarantees a
        # reproducible partition at concurrency 1. Unseeded, Leiden randomises
        # node order and settles in a different local optimum each run: on this
        # graph two runs over the identical 281 edges kept 126 and 247 claims,
        # because the ones that changed hands fell either side of
        # MIN_COMMUNITY_SIZE and communities under it are discarded. That made
        # every before/after comparison of a parameter change unreadable — the
        # run-to-run swing was larger than the effect being measured.
        params = {"gamma": cfg.community_resolution,
                  "randomSeed": cfg.community_seed, "concurrency": 1,
                  # Leiden merges bottom-up and we used to read only where it
                  # stopped. That final level is the whole corpus barely
                  # divided; the themes worth retrieving are the ones it passed
                  # through on the way.
                  "includeIntermediateCommunities": True}
        try:
            result = runner.stream(graph, relationshipWeightProperty="weight",
                                   **params)
        except ClientError as exc:
            # GDS 2.x throws an NPE from LeidenResult.dendrogramManager() when the
            # weighted run converges in zero levels, which happens on very small or
            # near-complete concept graphs. The unweighted run is unaffected.
            if "dendrogramManager" not in str(exc):
                raise
            log.warning(
                "Weighted %s failed on this graph (GDS degeneracy); "
                "retrying unweighted. Add more papers for weighted communities.",
                algorithm,
            )
            result = runner.stream(graph, **params)

        node_ids = result["nodeId"].tolist()
        keys = [gds.util.asNode(nid)["claim_id"] for nid in node_ids]
        levels = [list(ids) for ids in result["intermediateCommunityIds"].tolist()]
        depth = max(len(x) for x in levels)

        rows: list[dict] = []
        for level in _usable_levels(depth):
            grouped: dict[int, list[str]] = {}
            for key, ids in zip(keys, levels):
                grouped.setdefault(int(ids[min(level, len(ids) - 1)]), []).append(key)
            kept = {c: m for c, m in grouped.items()
                    if len(m) >= cfg.min_community_size}
            log.info("  level %d: %d communities over %d claims (of %d groups)",
                     level, len(kept), sum(len(m) for m in kept.values()), len(grouped))
            rows += [
                {
                    "community_id": f"{algorithm}-L{level}-{cid}",
                    "level": level,
                    "size": len(members),
                    "members": members,
                    "members_hash": _fingerprint(members),
                }
                for cid, members in kept.items()
            ]

        removed = store.prune_communities([r["community_id"] for r in rows])
        store.write_communities(rows, algorithm)
        kept_summaries = len(rows) - len(store.unsummarized_communities())
        log.info("%d communities written, %d dropped, %d summaries reused",
                 len(rows), removed, kept_summaries)

        log.info(
            "%s produced %d communities across %d levels (>= %d members) "
            "over %d claims",
            algorithm, len(rows), len(_usable_levels(depth)),
            cfg.min_community_size, graph.node_count(),
        )
        return {"communities": len(rows), "nodes": graph.node_count()}
    finally:
        _drop_graph(gds)


def summarize_communities(store: GraphStore, cfg: Config, client=None) -> int:
    """Summarize every community that lacks one, then embed the summaries.

    Parallel, because communities are independent and each prompt now carries
    up to thirty full claim sentences rather than a handful of short names.

    The embedding is done here rather than left to a later `embed` call: global
    and hybrid retrieval search the community vector index, so a freshly
    detected community that has not been embedded is invisible, and the query
    answers "the context contains no information" instead of failing. Silence
    is the worst possible way for that to surface.
    """
    llm = StructuredLLM(cfg)
    ids = store.unsummarized_communities()
    if not ids:
        return 0

    def summarize(community_id: str):
        context = store.community_context(community_id)
        if not context:
            return None
        user = SUMMARY_USER.format(
            concepts="\n".join(f"- {c}" for c in context["concepts"]) or "(none)",
            claims="\n".join(f"- {c}" for c in context["claims"] if c) or "(none)",
            papers="\n".join(f"- {p}" for p in context["papers"] if p) or "(none)",
        )
        try:
            return community_id, llm.parse(SUMMARY_SYSTEM, user, CommunitySummary,
                                           max_tokens=SUMMARY_MAX_TOKENS)
        except Exception as exc:
            log.error("Summary failed for %s: %s", community_id, exc)
            return None

    written = 0
    with ThreadPoolExecutor(max_workers=max(1, cfg.extract_concurrency)) as pool:
        for result in pool.map(summarize, ids):
            if result is None:
                continue
            community_id, summary = result
            store.save_community_summary(
                community_id, summary.title, summary.summary, summary.key_themes)
            written += 1
            log.info("Summarized %s: %s", community_id, summary.title)

    if written:
        from .embed import embed_label
        from ..llm.openrouter import raw_client

        embedded = embed_label(store, cfg, client or raw_client(cfg), "Community")
        log.info("Embedded %d community summaries", embedded)
    return written
