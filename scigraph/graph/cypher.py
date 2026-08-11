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
}

SHOW_VECTOR_INDEXES = (
    "SHOW VECTOR INDEXES YIELD name, options WHERE name IN $names RETURN name, options"
)
DROP_INDEX = "DROP INDEX {name} IF EXISTS"
CLEAR_EMBEDDINGS = "MATCH (n) WHERE n.embedding IS NOT NULL REMOVE n.embedding"
WIPE = "MATCH (n) CALL (n) { DETACH DELETE n } IN TRANSACTIONS OF 10000 ROWS"

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
SET r.weight = score, r.source = 'cross_paper_knn'
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
# come from different papers. Pairing used to require a shared measurement
# artifact; that machinery is gone with the measurements, and it never produced
# a comparable pair anyway — the papers evaluate different models on different
# data, so the artifacts almost never met.
CLAIM_CANDIDATE_PAIRS = """
MATCH (pa:Paper)-[:MAKES_CLAIM]->(a:Claim)
MATCH (pb:Paper)-[:MAKES_CLAIM]->(b:Claim)
WHERE a.paper_id < b.paper_id
  AND coalesce(a.status, '') <> 'unsupported'
  AND coalesce(b.status, '') <> 'unsupported'
  AND a.embedding IS NOT NULL AND b.embedding IS NOT NULL
  AND NOT EXISTS { (a)-[:CONTRADICTS|SUPPORTS|REFINES|UNRELATED_TO]-(b) }
WITH a, b, pa, pb, vector.similarity.cosine(a.embedding, b.embedding) AS similarity
WHERE similarity >= $min_similarity
// Datasets both papers work on, so a judge can tell a real disagreement from
// two papers measuring different things.
OPTIONAL MATCH (pa)-[:USES_DATASET]->(d:Dataset)<-[:USES_DATASET]-(pb)
WITH a, b, pa, pb, similarity, collect(DISTINCT d.name)[..8] AS shared_specific
// The spans behind each claim: what the paper actually put in front of the
// reader, tables included.
WITH a, b, pa, pb, similarity, shared_specific,
     [(a)-[:SUPPORTED_BY]->(e:Evidence) | left(e.text, 400)][..4] AS a_backing,
     [(b)-[:SUPPORTED_BY]->(e:Evidence) | left(e.text, 400)][..4] AS b_backing
RETURN a.claim_id AS a_id, a.text AS a_text, pa.title AS a_paper,
       a.section AS a_section, a.page_start AS a_page, a_backing,
       b.claim_id AS b_id, b.text AS b_text, pb.title AS b_paper,
       b.section AS b_section, b.page_start AS b_page, b_backing,
       shared_specific AS shared, shared_specific, similarity
ORDER BY similarity DESC
LIMIT $limit
"""


WRITE_CLAIM_LINK = """
MATCH (a:Claim {claim_id: $a_id})
MATCH (b:Claim {claim_id: $b_id})
MERGE (a)-[r:`__REL__`]->(b)
SET r.rationale = $rationale,
    r.confidence = $confidence,
    r.similarity = $similarity,
    r.shared_entities = $shared,
    r.shared_artifacts = $shared_specific,
    r.explanation = $explanation,
    r.judged_by = $model,
    r.judged_at = $judged_at
"""

DISAGREEMENTS = """
MATCH (a:Claim)-[r:CONTRADICTS]->(b:Claim)
MATCH (pa:Paper)-[:MAKES_CLAIM]->(a)
MATCH (pb:Paper)-[:MAKES_CLAIM]->(b)
RETURN pa.title AS paper_a, a.text AS claim_a, a.section AS section_a, a.page_start AS page_a,
       pb.title AS paper_b, b.text AS claim_b, b.section AS section_b, b.page_start AS page_b,
       r.rationale AS rationale, r.explanation AS explanation,
       r.confidence AS confidence
ORDER BY r.confidence DESC
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

WRITE_COMMUNITIES = """
UNWIND $rows AS row
  MERGE (c:Community {community_id: row.community_id})
  SET c.algorithm = $algorithm, c.size = row.size, c.level = 0
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
}

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
GLOBAL_QUERY = f"""
MATCH (community:Community) WHERE community = node
OPTIONAL MATCH (community)<-[:IN_COMMUNITY]-(cl2:Claim)
OPTIONAL MATCH (e)<-[:ABOUT]-(cl:Claim)<-[:MAKES_CLAIM]-(p:Paper)
WITH community, score,
     collect(DISTINCT e.name)[..25] AS concepts,
     collect(DISTINCT p.title)[..15] AS papers,
     collect(DISTINCT
       '  * "' + cl.text + '" [' + p.title + ', ' + cl.section +
       ', p.' + toString(cl.page_start) + ']'
     )[..10] AS citations
RETURN
  '--- THEME (similarity ' + toString(round(score, 3)) + ') ---\\n' +
  'Community: ' + coalesce(community.title, community.community_id) + '\\n' +
  'Size: ' + toString(community.size) + ' concepts\\n' +
  'Concepts: ' + {_join('concepts')} + '\\n' +
  'Papers: ' + {_join('papers')} + '\\n' +
  'Summary: ' + coalesce(community.summary, '(not yet summarized)') + '\\n' +
  'Citable claims from this theme:\\n' + {_join('citations', sep=chr(92) + 'n')}
  AS info
ORDER BY score DESC
"""

# --- hybrid: community framing, then the cited evidence underneath it ---------
# A theme, and underneath it the claims that constitute it with the passage
# behind each. Global mode answers from summaries alone, so its citations
# resolve to a community rather than to a page and a reader cannot check them;
# this carries the evidence through, which is the whole point of grouping
# claims rather than chunks.
HYBRID_QUERY = f"""
MATCH (community:Community) WHERE community = node
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
"""



# ----------------------------------------------------------- concept linking


# ------------------------------------------------------------- paper profile


