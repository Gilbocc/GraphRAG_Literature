"""Every Cypher statement in the project, in one place.

Queries used to live next to the code that ran them, which meant the graph
contract was spread across eight modules and label/relationship changes had to
be chased through all of them. Nothing here executes — see `store.GraphStore`.
"""

from __future__ import annotations

# --------------------------------------------------------------------- schema

CONSTRAINTS = [
    "CREATE CONSTRAINT paper_id IF NOT EXISTS FOR (n:Paper) REQUIRE n.paper_id IS UNIQUE",
    "CREATE CONSTRAINT section_id IF NOT EXISTS FOR (n:Section) REQUIRE n.section_id IS UNIQUE",
    "CREATE CONSTRAINT chunk_id IF NOT EXISTS FOR (n:Chunk) REQUIRE n.chunk_id IS UNIQUE",
    "CREATE CONSTRAINT claim_id IF NOT EXISTS FOR (n:Claim) REQUIRE n.claim_id IS UNIQUE",
    "CREATE CONSTRAINT evidence_id IF NOT EXISTS FOR (n:Evidence) REQUIRE n.evidence_id IS UNIQUE",
    "CREATE CONSTRAINT dataset_key IF NOT EXISTS FOR (n:Dataset) REQUIRE n.dataset_key IS UNIQUE",
    "CREATE CONSTRAINT community_id IF NOT EXISTS FOR (n:Community) REQUIRE n.community_id IS UNIQUE",
    "CREATE CONSTRAINT author_key IF NOT EXISTS FOR (n:Author) REQUIRE n.author_key IS UNIQUE",
    "CREATE CONSTRAINT venue_name IF NOT EXISTS FOR (n:Venue) REQUIRE n.name IS UNIQUE",
]

INDEXES = [
    "CREATE INDEX chunk_paper IF NOT EXISTS FOR (n:Chunk) ON (n.paper_id)",
    "CREATE INDEX paper_year IF NOT EXISTS FOR (n:Paper) ON (n.year)",
    "CREATE INDEX paper_doi IF NOT EXISTS FOR (n:Paper) ON (n.doi)",
    "CREATE INDEX paper_arxiv IF NOT EXISTS FOR (n:Paper) ON (n.arxiv_id)",
    "CREATE FULLTEXT INDEX chunk_fulltext IF NOT EXISTS FOR (n:Chunk) ON EACH [n.text]",
    "CREATE FULLTEXT INDEX claim_fulltext IF NOT EXISTS FOR (n:Claim) ON EACH [n.text]",
]

VECTOR_INDEXES = {
    "chunk_embeddings": ("Chunk", "embedding"),
    "claim_embeddings": ("Claim", "embedding"),
    "community_embeddings": ("Community", "embedding"),
    "evidence_embeddings": ("Evidence", "embedding"),
}

SHOW_VECTOR_INDEXES = (
    "SHOW VECTOR INDEXES YIELD name, options WHERE name IN $names RETURN name, options"
)
DROP_INDEX = "DROP INDEX {name} IF EXISTS"
CLEAR_EMBEDDINGS = "MATCH (n) WHERE n.embedding IS NOT NULL REMOVE n.embedding"
WIPE = "MATCH (n) CALL (n) { DETACH DELETE n } IN TRANSACTIONS OF 10000 ROWS"

# Everything one paper contributed, so it can be ingested again from clean.
#
# Needed because an interrupted ingest leaves a half-extracted paper, and
# re-running does not repair it: claim ids hash the claim's own text, so an
# identical claim re-merges but a re-worded one lands as a second node beside
# the first. Re-ingesting on top silently doubles part of a paper.
#
# The Paper node itself stays. Ingest MERGEs it by id regardless, and keeping
# it preserves the CITES edges other papers' reference lists point at it.
# Datasets are shared, so only those left with no other paper go.
DELETE_PAPER_CONTENT = """
MATCH (p:Paper {paper_id: $paper_id})
OPTIONAL MATCH (p)-[:MAKES_CLAIM]->(cl:Claim)
OPTIONAL MATCH (cl)-[:SUPPORTED_BY]->(ev:Evidence)
OPTIONAL MATCH (p)-[:HAS_SECTION]->(sec:Section)-[:HAS_CHUNK]->(ch:Chunk)
WITH p, collect(DISTINCT cl) + collect(DISTINCT ev)
      + collect(DISTINCT sec) + collect(DISTINCT ch) AS doomed
FOREACH (n IN doomed | DETACH DELETE n)
WITH p
OPTIONAL MATCH (p)-[:USES_DATASET]->(d:Dataset)
WHERE NOT EXISTS { MATCH (other:Paper)-[:USES_DATASET]->(d) WHERE other <> p }
DETACH DELETE d
"""

# ------------------------------------------------------------------ documents

WRITE_DOCUMENT = """
MERGE (p:Paper {paper_id: $paper.paper_id})
SET p.title = $paper.title,
    p.doi = $paper.doi,
    p.arxiv_id = $paper.arxiv_id,
    p.is_stub = false,
    p.source_path = $paper.source_path,
    p.n_pages = $paper.n_pages
WITH p
UNWIND $sections AS s
  MERGE (sec:Section {section_id: s.section_id})
  SET sec.title = s.title,
      sec.order = s.order,
      sec.page_start = s.page_start,
      sec.page_end = s.page_end,
      sec.paper_id = s.paper_id
  MERGE (p)-[:HAS_SECTION]->(sec)
WITH p
UNWIND $chunks AS c
  MERGE (ch:Chunk {chunk_id: c.chunk_id})
  SET ch.text = c.text,
      ch.index = c.index,
      ch.paper_id = c.paper_id,
      ch.section_id = c.section_id,
      ch.section_title = c.section_title,
      ch.page_start = c.page_start,
      ch.page_end = c.page_end
  WITH p, ch, c
  MATCH (sec:Section {section_id: c.section_id})
  MERGE (sec)-[:HAS_CHUNK]->(ch)
"""

# Cited works become stub Papers keyed like real ones, so they merge if that
# paper is later ingested.
WRITE_REFERENCES = """
MATCH (src:Paper {paper_id: $source_id})
UNWIND $refs AS r
  MERGE (tgt:Paper {paper_id: r.paper_id})
  ON CREATE SET tgt.is_stub = true,
                tgt.title = r.title,
                tgt.doi = r.doi,
                tgt.arxiv_id = r.arxiv_id,
                tgt.year = r.year
  SET tgt.title = coalesce(tgt.title, r.title),
      tgt.doi = coalesce(tgt.doi, r.doi),
      tgt.arxiv_id = coalesce(tgt.arxiv_id, r.arxiv_id),
      tgt.year = coalesce(tgt.year, r.year)
  MERGE (src)-[c:CITES]->(tgt)
  SET c.raw = r.raw, c.resolved_by = r.resolved_by
"""

# ------------------------------------------------------- claims and evidence

# Evidence is a range of the paper's own text, identified by character offsets
# into the chunk it came from. Nothing here was written by a model: the span is
# sliced out of the chunk, so a stored quotation is the paper's words by
# construction rather than by later verification.
WRITE_EVIDENCE = """
UNWIND $rows AS r
  MATCH (cl:Claim {claim_id: r.claim_id})
  MATCH (ch:Chunk {chunk_id: r.chunk_id})
  MERGE (ev:Evidence {evidence_id: r.evidence_id})
  SET ev.text = r.text,
      ev.char_start = r.char_start,
      ev.char_end = r.char_end,
      ev.confidence = r.confidence,
      ev.paper_id = r.paper_id,
      ev.section = r.section,
      ev.page_start = r.page_start,
      ev.page_end = r.page_end,
      ev.chunk_id = r.chunk_id
  MERGE (cl)-[:SUPPORTED_BY]->(ev)
  MERGE (ev)-[:EXTRACTED_FROM]->(ch)
"""

# A claim discovered while reading the body hangs off the thesis-level claim it
# elaborates, so the paper's argument keeps its shape instead of flattening
# into a list.
LINK_SUBCLAIM = """
MATCH (child:Claim {claim_id: $child_id})
MATCH (parent:Claim {claim_id: $parent_id})
MERGE (child)-[:ELABORATES]->(parent)
"""


# A sub-claim nothing supports is not a claim the paper made. Top-level claims
# are exempt: they come from the abstract, which is the paper asserting them
# directly, so absence of a body span is not absence of the claim.
DROP_UNSUPPORTED_SUBCLAIMS = """
MATCH (p:Paper)-[:MAKES_CLAIM]->(c:Claim)
WHERE c.is_main = false
  AND NOT (c)-[:SUPPORTED_BY]->(:Evidence)
  AND NOT (:Claim)-[:ELABORATES]->(c)   // keeps a claim its children establish
DETACH DELETE c
RETURN count(*) AS dropped
"""

MARK_VERDICT = """
MATCH (c:Claim {claim_id: $claim_id})
SET c.status = $status,
    c.verified = $status <> 'unsupported',
    c.contradicted = $contradicts,
    c.verdict_reason = $reason
"""

# Every claim is returned, including those with nothing behind them: a claim
# that was never judged and a claim judged unsupported are indistinguishable in
# the graph otherwise, and the second is a finding while the first is a gap.
#
# A claim is backed by its own spans and by what its sub-claims establish. An
# abstract states a finding in aggregate — "domain-specific models outperform
# generic ones" — while the body demonstrates it model by model, so the general
# claim is supported through its children rather than by any span restating it.
CLAIMS_WITH_EVIDENCE = """
MATCH (p:Paper {paper_id: $paper_id})-[:MAKES_CLAIM]->(c:Claim)
OPTIONAL MATCH (c)-[:SUPPORTED_BY]->(own:Evidence)
OPTIONAL MATCH (child:Claim)-[:ELABORATES]->(c)
OPTIONAL MATCH (child)-[:SUPPORTED_BY]->(sub:Evidence)
WITH c,
     collect(DISTINCT own.text)[..8] AS own_evidence,
     collect(DISTINCT (child.text + '  ||  ' + sub.text))[..8] AS via_subclaims
RETURN c.claim_id AS claim_id, c.text AS text, c.is_main AS is_main,
       own_evidence, via_subclaims
"""


# Claims are what this graph is about, so they are what communities run over.
# Two claims are related when the measurements behind them share an artifact —
# the same model, or the same benchmark. That link comes from the measurement's
# own slots rather than from any name a model invented, so "BM25" in one paper
# meets "BM25" in another without an entity-resolution step in between.
# Claims are linked ACROSS papers only, to their nearest neighbours by
# embedding. Two claims in the same paper are already related by the paper —
# that structure is the ELABORATES tree and the shared paper node — so a
# community built from within-paper edges only restates what the paper already
# says. What a corpus-level community should answer is: which papers argue
# near-identical things, and where do they diverge?
#
# An earlier version linked claims whenever their two papers shared a dataset,
# which joined every claim in one paper to every claim in the other and, on a
# corpus that shares no dataset, produced no cross-paper edge at all.
BUILD_CLAIM_GRAPH = """
MATCH (a:Claim) WHERE a.embedding IS NOT NULL
CALL (a) {
  MATCH (b:Claim)
  WHERE b.embedding IS NOT NULL AND b.paper_id <> a.paper_id
  WITH b, vector.similarity.cosine(a.embedding, b.embedding) AS score
  WHERE score >= $min_similarity
  RETURN b, score ORDER BY score DESC LIMIT $k
}
WITH a, b, score WHERE elementId(a) < elementId(b)
MERGE (a)-[r:RELATED_CLAIM]->(b)
// The weight is the similarity rescaled onto the range that actually survived
// the threshold, not the raw cosine. Every edge here scored at least
// $min_similarity, so raw scores span 0.80-1.00 — to modularity that is a
// nearly uniform graph, and a uniform graph has no structure to find, which is
// how Leiden ended up cutting one topic into equal-sized halves while nominally
// running weighted. Rescaled, a 0.98 pair outweighs a 0.81 pair roughly 9 to 1.
SET r.weight = (score - $min_similarity) / (1.0 - $min_similarity),
    r.similarity = score,
    r.source = 'cross_paper_knn'
RETURN count(*) AS created
"""



# --------------------------------------------------------------------- claims

# A claim carries no evidence of its own. It used to mint an Evidence node from
# its own text, which meant every claim arrived pre-supported by a restatement
# of itself — 45 such nodes on one paper, indistinguishable in the graph from
# the 66 real spans. Evidence comes only from the pass that locates spans.
WRITE_CLAIMS = """
UNWIND $claims AS c
  MATCH (p:Paper {paper_id: c.paper_id})
  MERGE (cl:Claim {claim_id: c.claim_id})
  SET cl.text = c.text,
      cl.claim_type = c.claim_type,
      cl.paper_id = c.paper_id,
      cl.section = c.section,
      cl.page_start = c.page_start,
      cl.page_end = c.page_end,
      cl.chunk_id = c.chunk_id,
      cl.confidence = c.confidence,
      cl.is_main = coalesce(c.is_main, false),
      cl.rank = c.rank
  MERGE (p)-[:MAKES_CLAIM]->(cl)
"""


# __REL__ comes from a fixed allowlist, never from model output.
# Two claims are worth comparing when their papers measured the same thing. The
# artifact comes from a measurement's own `method` / `dataset` slot — a name the
# paper printed rather than one a model chose — so it matches across papers with
# no resolution step in between. Pairing on shared nodes found nothing, because
# no two papers ever landed on the same node.
# Two claims are worth comparing when they say near enough the same thing and
# NOTE: the LLM pass that judged claim pairs (CONTRADICTS / SUPPORTS / REFINES)
# was removed. Across three corpus sizes it judged every candidate UNRELATED,
# and the one real disagreement this corpus contains — CUAD's "a 20-fold
# parameter increase yields ~3% AUPR" against LawBench's "scaling up the model
# size improves performance" — sat at cosine 0.799, below the pairing floor,
# and was surfaced by retrieval instead. RELATED_CLAIM survives: it is the kNN
# graph community detection runs on, and has nothing to do with judging.

# Passages matched against the question directly, with no community or claim in
# between. The first attempt at this folded the spans into `hybrid` and made it
# worse: ranked on similarity alone, all five slots went to whichever paper
# wrote most densely on the topic — LEGALBENCH took every one on "which model
# families recur" — and those hits pushed the themes' cross-paper claims out of
# the context. Two spans per paper is the fix; the route itself was never the
# problem.
EVIDENCE_QUERY = """
MATCH (ev:Evidence) WHERE ev = node
MATCH (cl:Claim)-[:SUPPORTED_BY]->(ev)
MATCH (p:Paper)-[:MAKES_CLAIM]->(cl)
WITH p, ev, cl, score ORDER BY score DESC
WITH p, collect({{ev: ev, cl: cl, score: score}})[..2] AS best
UNWIND best AS hit
WITH p, hit.ev AS ev, hit.cl AS cl, hit.score AS score
ORDER BY score DESC LIMIT {limit}
RETURN '--- PASSAGE (similarity ' + toString(round(score, 3)) + ') ---\\n' +
       '"' + left(ev.text, 900) + '"' +
       '  \u2014\u2014 CITE AS: [' + coalesce(p.title, '?') + ', ' +
       coalesce(ev.section, cl.section, '?') +
       ', p.' + toString(coalesce(ev.page_start, cl.page_start)) + ']\\n' +
       '    (what it supports, our paraphrase \u2014 do not quote: ' + cl.text +
       ')  [' + coalesce(cl.status, 'unverified') + ']'
       AS info
ORDER BY score DESC
"""

# ---------------------------------------------------------------- communities

# Detection is a full recomputation, so the previous generation must go first.
# Leaving it behind accumulated three overlapping generations of the same
# clusters — 21 community nodes over 11 distinct claim sets — and global-mode
# answers cited the same cluster three times as if it were three sources.
CLEAR_COMMUNITIES = """
MATCH (c:Community) DETACH DELETE c
RETURN count(*) AS removed
"""

# Detection is deterministic, so re-running it usually reproduces the same
# communities exactly. Deleting them all first threw away every summary anyway,
# which made each run cost 23 LLM calls and meant an interrupted run left the
# graph worse than it found it. This drops only what no longer exists.
PRUNE_COMMUNITIES = """
MATCH (c:Community) WHERE NOT c.community_id IN $ids
DETACH DELETE c
RETURN count(*) AS removed
"""

# A summary is only valid for the exact set of claims it was written from, so
# membership is fingerprinted and the summary survives precisely when that
# fingerprint does. Same claims -> keep the summary and its embedding; one claim
# different -> the summary now describes something else, so it goes and is
# regenerated.
WRITE_COMMUNITIES = """
UNWIND $rows AS row
  MERGE (c:Community {community_id: row.community_id})
  FOREACH (_ IN CASE
             WHEN c.members_hash IS NULL OR c.members_hash <> row.members_hash
             THEN [1] ELSE [] END |
    SET c.summary = NULL, c.title = NULL, c.key_themes = NULL
    REMOVE c.embedding
  )
  SET c.algorithm = $algorithm, c.size = row.size, c.level = row.level,
      c.members_hash = row.members_hash
  WITH c, row
  CALL (c) { MATCH (c)<-[old:IN_COMMUNITY]-() DELETE old }
  WITH c, row
  UNWIND row.members AS member_key
    MATCH (n:Claim {claim_id: member_key})
    MERGE (n)-[:IN_COMMUNITY]->(c)
"""

# A community is a set of claims, so its context is those claims, the artifacts
# their measurements share, and the papers making them.
COMMUNITY_CONTEXT = """
MATCH (c:Community {community_id: $community_id})<-[:IN_COMMUNITY]-(cl:Claim)
OPTIONAL MATCH (p:Paper)-[:MAKES_CLAIM]->(cl)
OPTIONAL MATCH (p)-[:USES_DATASET]->(d:Dataset)
RETURN collect(DISTINCT cl.text)[..30] AS claims,
       [x IN collect(DISTINCT d.name) WHERE x IS NOT NULL AND x <> ''][..20] AS concepts,
       collect(DISTINCT p.title)[..15] AS papers
"""

SAVE_COMMUNITY_SUMMARY = """
MATCH (c:Community {community_id: $community_id})
SET c.title = $title, c.summary = $summary, c.key_themes = $key_themes
"""

UNSUMMARIZED_COMMUNITIES = (
    "MATCH (c:Community) WHERE c.summary IS NULL RETURN c.community_id AS community_id"
)

# ------------------------------------------------------------------ citations

# Which works the corpus keeps citing but does not contain. A paper cited
# independently by several of your papers is one the field treats as load-
# bearing, so this is the corpus telling you what to read next — and it needs
# no extraction, only the reference lists already parsed.
SUGGEST_PAPERS = """
MATCH (src:Paper {is_stub: false})-[:CITES]->(t:Paper {is_stub: true})
WHERE t.title IS NOT NULL AND t.title <> ''
WITH t, count(DISTINCT src) AS citers, collect(DISTINCT src.title)[..5] AS cited_by
WHERE citers >= $min_citers
RETURN t.title AS title, t.year AS year, t.doi AS doi, t.arxiv_id AS arxiv_id,
       citers, cited_by
ORDER BY citers DESC, t.year DESC
LIMIT $limit
"""

# ------------------------------------------------------------------- datasets


# A Dataset carries what the paper says about the data, which is what a
# retriever needs when the question is about the data rather than the number.
# It is created only from a name some measurement was actually recorded against,
# so it cannot drift into a list of things the paper merely mentions.
WRITE_DATASETS = """
UNWIND $rows AS r
  MERGE (d:Dataset {dataset_key: r.key})
  ON CREATE SET d.name = r.name
  SET d.description = coalesce(r.description, d.description),
      d.size = coalesce(r.size, d.size),
      d.language = coalesce(r.language, d.language),
      d.domain = coalesce(r.domain, d.domain),
      d.source = coalesce(r.source, d.source),
      d.supporting_text = coalesce(r.supporting_text, d.supporting_text)
  WITH d, r
  MATCH (p:Paper {paper_id: r.paper_id})
  MERGE (p)-[u:USES_DATASET]->(d)
  SET u.introduced_here = r.introduced_here
"""

# ------------------------------------------------------------------ artifacts


# ----------------------------------------------------------------- embeddings

# label -> (query selecting unembedded nodes, id property)
# What text stands for each node when a question is matched against it.
#
# A claim is embedded bare, and it was worth trying the alternative to find out
# why. Prefixing the paper title and section — on the theory that "performance
# degrades sharply on longer inputs" names neither task nor model — made the
# cross-paper kNN worse, because the prefix is near-constant within a paper and
# long relative to one sentence. Four unrelated LEGALBENCH claims came back
# paired to the same LawBench claim at an identical 0.905: the score was
# measuring the prefix. Bare text recovers pairs that are actually about one
# thing, e.g. both benchmarks excluding long-document tasks over context limits.
# Context that discriminates *between* claims in a paper would help; metadata
# shared by all of them does not.
EMBED_TARGETS = {
    "Chunk": (
        "MATCH (n:Chunk) WHERE n.embedding IS NULL AND n.text IS NOT NULL "
        "RETURN n.chunk_id AS id, n.text AS text LIMIT $limit",
        "chunk_id",
    ),
    "Claim": (
        "MATCH (n:Claim) WHERE n.embedding IS NULL "
        "RETURN n.claim_id AS id, n.text AS text LIMIT $limit",
        "claim_id",
    ),
    "Community": (
        "MATCH (n:Community) WHERE n.embedding IS NULL AND n.summary IS NOT NULL "
        "RETURN n.community_id AS id, "
        "  coalesce(n.title,'') + '. ' + n.summary AS text LIMIT $limit",
        "community_id",
    ),
    "Evidence": (
        "MATCH (n:Evidence) WHERE n.embedding IS NULL AND n.text IS NOT NULL "
        "RETURN n.evidence_id AS id, n.text AS text LIMIT $limit",
        "evidence_id",
    ),
}

# Changing what a label embeds makes the stored vectors stale, and the
# incremental `embedding IS NULL` filter will never notice.
CLEAR_LABEL_EMBEDDINGS = "MATCH (n:{label}) REMOVE n.embedding"

WRITE_EMBEDDING = """
UNWIND $rows AS row
  MATCH (n:{label} {{{id_prop}: row.id}})
  CALL db.create.setNodeVectorProperty(n, 'embedding', row.embedding)
"""

# --------------------------------------------------------------------- biblio

PAPERS_TO_ENRICH = """
MATCH (p:Paper)
WHERE p.openalex_id IS NULL AND (p.is_stub = false OR $include_stubs)
RETURN p.paper_id AS paper_id, p.title AS title, p.doi AS doi, p.arxiv_id AS arxiv_id
LIMIT $limit
"""

WRITE_ENRICHMENT = """
UNWIND $rows AS row
  MATCH (p:Paper {paper_id: row.paper_id})
  SET p.openalex_id = row.openalex_id,
      p.year = coalesce(row.year, p.year),
      p.published_date = coalesce(row.published_date, p.published_date),
      p.cited_by_count = row.cited_by_count,
      p.publication_type = row.publication_type,
      p.title = coalesce(p.title, row.title)
  WITH p, row
  FOREACH (_ IN CASE WHEN row.venue IS NULL THEN [] ELSE [1] END |
    MERGE (v:Venue {name: row.venue})
    MERGE (p)-[:PUBLISHED_IN]->(v))
  WITH p, row
  UNWIND (CASE WHEN row.authors = [] THEN [null] ELSE row.authors END) AS a
    WITH p, a WHERE a IS NOT NULL
    MERGE (au:Author {author_key: a.key})
    ON CREATE SET au.name = a.name, au.orcid = a.orcid
    SET au.orcid = coalesce(au.orcid, a.orcid)
    MERGE (p)-[r:AUTHORED_BY]->(au)
    SET r.position = a.position
"""

# ---------------------------------------------------------------------- stats

NODE_COUNTS = """
MATCH (n) UNWIND labels(n) AS label
RETURN label, count(*) AS n ORDER BY n DESC, label
"""

REL_COUNTS = "MATCH ()-[r]->() RETURN type(r) AS label, count(*) AS n ORDER BY n DESC, label"

COVERAGE = """
MATCH (n) WHERE n.embedding IS NOT NULL
WITH count(n) AS embedded
OPTIONAL MATCH (c:Community) WHERE c.summary IS NOT NULL
RETURN embedded, count(c) AS summarized
"""


# ------------------------------------------------------------------ retrieval


def _join(var: str, sep: str = "; ") -> str:
    """Cypher has no join(); fold the list with reduce()."""
    return (
        f"reduce(s = '', x IN {var} | "
        f"CASE WHEN s = '' THEN x ELSE s + '{sep}' + x END)"
    )


LOCAL_QUERY = f"""
MATCH (chunk:Chunk)<-[:HAS_CHUNK]-(section:Section)<-[:HAS_SECTION]-(paper:Paper)
WHERE chunk = node
OPTIONAL MATCH (paper)-[:MAKES_CLAIM]->(claim:Claim)-[:SUPPORTED_BY]->(:Evidence)
               -[:EXTRACTED_FROM]->(chunk)
OPTIONAL MATCH (paper)-[:USES_DATASET]->(d:Dataset)
WITH paper, section, chunk, score,
     collect(DISTINCT claim.text)[..8] AS claims,
     [x IN collect(DISTINCT
        d.name + ' — ' + coalesce(d.description, '') +
        CASE WHEN coalesce(d.size, '') = '' THEN '' ELSE ' (' + d.size + ')' END)
      WHERE x IS NOT NULL][..6] AS datasets
RETURN
  '--- PASSAGE (similarity ' + toString(round(score, 3)) + ') ---\\n' +
  'Paper: ' + paper.title + '\\n' +
  'DOI: ' + coalesce(paper.doi, 'n/a') + '\\n' +
  'Section: ' + section.title + '\\n' +
  'Pages: ' + toString(chunk.page_start) + '-' + toString(chunk.page_end) + '\\n' +
  'Chunk ID: ' + chunk.chunk_id + '\\n' +
  CASE WHEN size(datasets) > 0
       THEN 'Datasets involved: ' + {_join('datasets')} + '\\n' ELSE '' END +
  CASE WHEN size(claims) > 0
       THEN 'Claims grounded here: ' + {_join('claims')} + '\\n' ELSE '' END +
  'Passage text:\\n' + chunk.text
  AS info
ORDER BY score DESC
"""

# --- global: community summaries, with their concepts and papers --------------
# Community summaries carry no page numbers of their own, so a few grounded
# claims are attached. Without them the model is asked for page-level citations
# it has no data for, and fabricates them.
# Broad themes only, and citable. This used to match `(e)<-[:ABOUT]-(cl:Claim)`
# with `e` unbound, against a relationship that no longer exists since entities
# were dropped: every "concept" came back empty and the citations came from a
# cartesian product. Global answered from titles alone, which is why it either
# invented sources or refused outright.
#
# {level} is filled in at build time. The vector index is shared by both
# hierarchy levels, and the library applies its LIMIT before this query runs,
# so callers over-fetch and this filters down.
GLOBAL_QUERY = f"""
MATCH (community:Community) WHERE community = node AND community.level = {{level}}
OPTIONAL MATCH (community)<-[:IN_COMMUNITY]-(cl:Claim)<-[:MAKES_CLAIM]-(p:Paper)
OPTIONAL MATCH (cl)-[:SUPPORTED_BY]->(ev:Evidence)
WITH community, score,
     collect(DISTINCT p.title)[..15] AS papers,
     collect(DISTINCT
       '  * "' + left(coalesce(ev.text, cl.text), 400) + '"' +
       '  \u2014\u2014 CITE AS: [' + coalesce(p.title, '?') + ', ' +
       coalesce(ev.section, cl.section, '?') +
       ', p.' + toString(coalesce(ev.page_start, cl.page_start)) + ']'
     )[..12] AS citations
RETURN
  '--- THEME (similarity ' + toString(round(score, 3)) + ') ---\\n' +
  'Community: ' + coalesce(community.title, community.community_id) + '\\n' +
  'Size: ' + toString(community.size) + ' claims\\n' +
  'Papers: ' + {_join('papers')} + '\\n' +
  'Passages behind this theme:\\n' +
  {_join('citations', sep=chr(92) + 'n')}
  AS info
ORDER BY score DESC
LIMIT {{limit}}
"""

HYBRID_QUERY = f"""
MATCH (community:Community) WHERE community = node AND community.level = {{level}}
OPTIONAL MATCH (community)<-[:IN_COMMUNITY]-(cl:Claim)
OPTIONAL MATCH (p:Paper)-[:MAKES_CLAIM]->(cl)
OPTIONAL MATCH (cl)-[:SUPPORTED_BY]->(ev:Evidence)
// The data the papers in this theme worked on. A score is uninterpretable
// without knowing what it was measured on, and the descriptions carry the
// task, the size and the provenance that a claim mentions only in passing.
OPTIONAL MATCH (p)-[:USES_DATASET]->(d:Dataset)
WITH community, score,
     // Each dataset carries the paper that describes it. Without that the
     // model cited the block itself — "(Legal Reasoning Benchmarks, Datasets,
     // p.---)" — inventing a source out of a community title, which is the
     // same uncheckable citation the CLAIM/PASSAGE split exists to prevent.
     [x IN collect(DISTINCT
        d.name + ' — ' + coalesce(d.description, '') +
        CASE WHEN coalesce(d.size, '') = '' THEN '' ELSE ' (' + d.size + ')' END +
        CASE WHEN coalesce(d.language, '') = '' THEN '' ELSE ' [' + d.language + ']' END +
        '  — described in: ' + coalesce(p.title, '?'))
      WHERE x IS NOT NULL][..8] AS datasets,
     // The quotation and its citation share one line, in that order. They
     // used to sit on separate lines with the source above the quote, and
     // synthesis across a dozen claims lost the binding: an answer quoted
     // LegalBench and cited a different paper. Whatever the model copies, it
     // now copies the attribution with it.
     //
     // The claim follows as a clearly-marked paraphrase, because only the
     // passage is the paper's own words.
     collect(DISTINCT
       '  * "' + left(coalesce(ev.text, '(none)'), 500) + '"' +
       '  —— CITE AS: [' + coalesce(p.title, '?') + ', ' +
       coalesce(ev.section, cl.section) +
       ', p.' + toString(coalesce(ev.page_start, cl.page_start)) + ']\\n' +
       '    (what it supports, our paraphrase — do not quote: ' + cl.text +
       ')  [' + coalesce(cl.status, 'unverified') + ']'
     )[..14] AS evidence
RETURN
  '--- THEME (similarity ' + toString(round(score, 3)) + ') ---\\n' +
  'Community: ' + coalesce(community.title, community.community_id) + '\\n' +
  'Summary: ' + coalesce(community.summary, '(not yet summarized)') + '\\n' +
  CASE WHEN size(datasets) > 0
       THEN 'Datasets the papers in this theme use (background, not quotable; ' +
            'cite the paper named after each):\\n  ' +
            {_join('datasets', sep=chr(92) + 'n  ')} + '\\n' ELSE '' END +
  'Claims in this theme, each with the passage behind it:\\n' +
  {_join('evidence', sep=chr(92) + 'n')}
  AS info
ORDER BY score DESC
LIMIT {{limit}}
"""




# ----------------------------------------------------------- concept linking


# ------------------------------------------------------------- paper profile


