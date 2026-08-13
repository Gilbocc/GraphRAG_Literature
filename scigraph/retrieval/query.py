"""Three GraphRAG query modes, all of which cite paper, section, page, and passage.

local  — specific papers, methods, datasets, claims (chunk vectors)
global — corpus-wide themes (community summary vectors)
hybrid — community summaries for framing and cross-paper reach, plus the
           nearest chunks, so an answer does not depend on community membership
evidence — the verbatim spans nearest the question, at most two per paper
"""

from __future__ import annotations

import logging
from typing import Literal

import neo4j
from neo4j_graphrag.generation import GraphRAG, RagTemplate
from neo4j_graphrag.retrievers import VectorCypherRetriever
from neo4j_graphrag.types import RetrieverResultItem

from ..config import Config
from ..graph.cypher import EVIDENCE_QUERY, GLOBAL_QUERY, HYBRID_QUERY, LOCAL_QUERY
from .baseline import PLAIN_QUERY
from ..llm.openrouter import embedder, graphrag_llm

log = logging.getLogger(__name__)

Mode = Literal["local", "global", "hybrid", "evidence"]


class _Answer:
    """What GraphRAG.search returns, for the one mode assembled here."""

    def __init__(self, answer: str, retriever_result=None):
        self.answer = answer
        self.retriever_result = retriever_result


CITATION_RULES = """\
You answer questions about a corpus of scientific papers using only the context provided.

Citation requirements, these are mandatory:
- Every factual statement must carry an inline citation of the form
  [paper title, section, p.PAGE].
- After the answer, add a "Sources" section. For each citation, quote the
  supporting passage verbatim from the context.
- If the context does not answer the question, say so explicitly. Never fill the
  gap from your own knowledge, and never invent a citation.
- Cite only section names and page numbers that appear verbatim in the context.
  A community/theme name is not a section. If a statement comes from a theme
  summary with no citable claim attached, attribute it to the theme and the
  papers listed, and do not attach a page number to it.
- When papers disagree, present both positions and attribute each to its paper
  rather than silently picking one.
"""

RAG_TEMPLATE = """\
You answer questions about a corpus of scientific papers, using only the context
below. Each passage carries its paper, section and page.

Cite as (Paper title, Section, p.N) — the human-readable fields, nothing else.
The context arrives as database records; never reproduce a record, a chunk id,
or a similarity score in your answer. A citation a reader cannot follow is
worse than none.

Never cite a community title or a Datasets block as if it were a source: they
are groupings we made, not sections of a paper. A dataset line names the paper
that describes it — cite that paper, or say the detail is unattributed.

Every quotation in the context is followed on the same line by "CITE AS: [...]".
Use exactly that citation for that quotation and no other — the themes group
passages from several papers, so a citation borrowed from a neighbouring line
names the wrong paper. If you cannot see a quotation's own CITE AS, do not
quote it.

Quote only the text in quotation marks before a CITE AS. Anything labelled CLAIM is our own
paraphrase of what a paper argues — use it to understand and to organise, never
inside quotation marks and never attributed to a page. Putting a paraphrase in
quotes with a page number produces a citation a reader cannot verify, which is
the one failure this context is designed to prevent. Where
a passage is a table, read the whole table rather than one row: the columns are
what make a comparison possible.

If the context does not answer the question, say so plainly and say what it does
cover. Do not fill a gap with knowledge from outside the context.

Context:
{context}

{examples}

Question:
{query_text}

Answer, then a Sources section listing each paper, section and page you used:
"""

MODES: dict[str, tuple[str, str]] = {
    "local": ("chunk_embeddings", LOCAL_QUERY),
    "global": ("community_embeddings", GLOBAL_QUERY),
    "hybrid": ("community_embeddings", HYBRID_QUERY),
    "evidence": ("evidence_embeddings", EVIDENCE_QUERY),
}

# Modes whose retrieval query filters or caps its own candidates, so the caller
# over-fetches and the query trims back to top_k itself. The client library
# applies its LIMIT before the retrieval query runs, which would otherwise turn
# every filter into a shrunken result set rather than a selection.
OVERFETCH_MODES = {"global", "hybrid", "evidence"}
OVERFETCH = 4

# Five themes and five chunks. Hybrid spends roughly 70% of its context on
# themes, which looks unbalanced and is not: rebalancing was tried both ways and
# both lost the one cross-paper disagreement this corpus contains.
#
# At 3 themes the community holding CUAD's scaling claims fell out entirely.
# At 8 chunks the themes were still present but the answer stopped using them —
# more passages did not add depth, they displaced attention, and hybrid returned
# the same "bigger usually helps" as every other mode. Restoring 5/5 brought the
# CUAD result back in two consecutive runs, so this is the configuration, not a
# coincidence.
#
# The passage-depth questions hybrid loses to `local` did not improve under
# either change. That gap is real and this is not the lever for it.
HYBRID_THEMES = 5
HYBRID_EXTRA_CHUNKS = 0

# Both hierarchy levels share one vector index, so without a filter a 9-claim
# theme and a 53-claim one compete on cosine alone — and a level-2 community
# that merged nothing is a byte-for-byte duplicate of its level-1 child, so the
# same claims arrived twice under two names. Splitting them gives each mode the
# granularity it is for: global answers corpus-wide questions from the broad
# level, hybrid wants specific themes and gets its breadth from chunks anyway.
LEVEL_FOR_MODE = {"global": "broad", "hybrid": "fine"}

# The library LIMITs to top_k before the retrieval query runs, so the level
# filter would otherwise shrink the result set rather than select within it.



def _levels(driver: neo4j.Driver, cfg: Config) -> dict[str, int]:
    """The finest and broadest community levels present in the graph."""
    with driver.session(database=cfg.neo4j_database) as session:
        found = sorted(r["level"] for r in session.run(
            "MATCH (c:Community) WHERE c.level IS NOT NULL "
            "RETURN DISTINCT c.level AS level"))
    if not found:
        return {"fine": 0, "broad": 0}
    return {"fine": found[0], "broad": found[-1]}


def build_rag(driver: neo4j.Driver, cfg: Config, mode: Mode, top_k: int = 5) -> GraphRAG:
    if mode not in MODES:
        raise ValueError(f"mode must be one of {sorted(MODES)}, got {mode!r}")
    index_name, retrieval_query = MODES[mode]
    if mode in OVERFETCH_MODES:
        fmt = {"limit": HYBRID_THEMES if mode == "hybrid" else top_k}
        if mode in LEVEL_FOR_MODE:
            fmt["level"] = _levels(driver, cfg)[LEVEL_FOR_MODE[mode]]
        retrieval_query = retrieval_query.format(**fmt)

    # Without a formatter the retriever hands the LLM `str(record)` — the
    # Python repr of a neo4j Record: `<Record info='--- THEME ...\n...'>`, with
    # every newline escaped to a literal backslash-n. The theme blocks are
    # built with deliberate line structure, one quotation per line followed by
    # its CITE AS, and all of it arrived as a single escaped string inside a
    # wrapper. The prompt had a rule telling the model not to quote record
    # syntax back, which treated the symptom.
    retriever = VectorCypherRetriever(
        result_formatter=lambda record: RetrieverResultItem(
            content=record["info"]),
        driver=driver,
        index_name=index_name,
        retrieval_query=retrieval_query,
        embedder=embedder(cfg),
        neo4j_database=cfg.neo4j_database,
    )
    template = RagTemplate(
        template=RAG_TEMPLATE,
        expected_inputs=["context", "query_text", "examples"],
        system_instructions=CITATION_RULES,
    )
    return GraphRAG(retriever=retriever, llm=graphrag_llm(cfg), prompt_template=template)


def _nearest_chunks(driver: neo4j.Driver, cfg: Config, question: str, top_k: int) -> str:
    """The plain-RAG half of hybrid: passages matched against the question.

    Community membership is not universal and cannot be made so. A claim joins
    a community only if it is close enough to a claim in another paper, and in
    a single-domain corpus that threshold has to stay strict or the communities
    stop meaning anything — so a paper that argues something genuinely its own
    is exactly the paper least likely to be in one. Two of ten papers reached
    no community at all.

    Retrieving chunks alongside the themes removes that dependency: the graph
    contributes cross-paper structure where it has any, and where it has none
    the answer still finds the passage.
    """
    vector = embedder(cfg).embed_query(question)
    with driver.session(database=cfg.neo4j_database) as session:
        rows = list(session.run(PLAIN_QUERY, embedding=vector, top_k=top_k))
    if not rows:
        return ""
    passages = "\n\n".join(
        f"--- PASSAGE (similarity {r['score']:.3f}) ---\n"
        f"CITE AS: [{r['paper']}, {r['section']}, p.{r['page_start']}]\n"
        f"{r['text']}"
        for r in rows
    )
    return ("--- PASSAGES MATCHING THE QUESTION DIRECTLY (quotable) ---\n"
            + passages)


def ask(
    driver: neo4j.Driver,
    cfg: Config,
    question: str,
    mode: Mode = "local",
    top_k: int = 5,
    return_context: bool = False,
):
    rag = build_rag(driver, cfg, mode, top_k=top_k)
    fetch = top_k * OVERFETCH if mode in OVERFETCH_MODES else top_k
    if mode != "hybrid":
        return rag.search(
            query_text=question,
            retriever_config={"top_k": fetch},
            return_context=return_context,
        )

    # Two indexes, which one retriever cannot span: themes from the community
    # index, passages from the chunk index, assembled into one context.
    themes = rag.retriever.search(query_text=question, top_k=fetch)
    context = "\n\n".join(item.content for item in themes.items)
    chunks = _nearest_chunks(driver, cfg, question, top_k + HYBRID_EXTRA_CHUNKS)
    if chunks:
        context = f"{context}\n\n{chunks}"
    answer = graphrag_llm(cfg).invoke(
        RAG_TEMPLATE.format(context=context, query_text=question, examples="")
    ).content
    return _Answer(answer, context if return_context else None)
