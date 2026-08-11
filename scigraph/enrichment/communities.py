"""Community detection over Claim nodes via Neo4j GDS, plus LLM summaries.

Detection runs on the Claim projection only — chunks, evidence,
and claim nodes are excluded, so communities describe scientific themes rather
than document structure.
"""

from __future__ import annotations

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


def _drop_graph(gds: GraphDataScience) -> None:
    if gds.graph.exists(GRAPH_NAME)["exists"]:
        gds.graph.drop(GRAPH_NAME)


def detect_communities(store: GraphStore, cfg: Config) -> dict[str, int]:
    """Project Claim-[:RELATED_CLAIM]-Claim and run Leiden or Louvain."""
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
        try:
            result = runner.stream(graph, relationshipWeightProperty="weight",
                                   gamma=cfg.community_resolution)
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
            result = runner.stream(graph, gamma=cfg.community_resolution)

        node_ids = result["nodeId"].tolist()
        keys = [gds.util.asNode(nid)["claim_id"] for nid in node_ids]
        communities = result["communityId"].tolist()

        grouped: dict[int, list[str]] = {}
        for key, community in zip(keys, communities):
            grouped.setdefault(int(community), []).append(key)

        rows = [
            {
                "community_id": f"{algorithm}-0-{cid}",
                "size": len(members),
                "members": members,
            }
            for cid, members in grouped.items()
            if len(members) >= cfg.min_community_size
        ]

        log.info("Cleared %d communities from the previous run",
                 store.clear_communities())
        store.write_communities(rows, algorithm)

        log.info(
            "%s produced %d communities (>= %d members) over %d concepts",
            algorithm,
            len(rows),
            cfg.min_community_size,
            graph.node_count(),
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
            return community_id, llm.parse(SUMMARY_SYSTEM, user, CommunitySummary)
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
