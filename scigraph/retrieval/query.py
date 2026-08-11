"""Three GraphRAG query modes, all of which cite paper, section, page, and passage.

local  — specific papers, methods, datasets, claims (chunk vectors)
global — corpus-wide themes (community summary vectors)
hybrid — community summaries for framing, claim/evidence detail for grounding
"""

from __future__ import annotations

import logging
from typing import Literal

import neo4j
from neo4j_graphrag.generation import GraphRAG, RagTemplate
from neo4j_graphrag.retrievers import VectorCypherRetriever

from ..config import Config
from ..graph.cypher import GLOBAL_QUERY, HYBRID_QUERY, LOCAL_QUERY
from ..llm.openrouter import embedder, graphrag_llm

log = logging.getLogger(__name__)

Mode = Literal["local", "global", "hybrid"]


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

# --- local: chunks, plus the entities and claims grounded in them -------------
MODES: dict[str, tuple[str, str]] = {
    "local": ("chunk_embeddings", LOCAL_QUERY),
    "global": ("community_embeddings", GLOBAL_QUERY),
    "hybrid": ("community_embeddings", HYBRID_QUERY),
}


def build_rag(driver: neo4j.Driver, cfg: Config, mode: Mode) -> GraphRAG:
    if mode not in MODES:
        raise ValueError(f"mode must be one of {sorted(MODES)}, got {mode!r}")
    index_name, retrieval_query = MODES[mode]

    retriever = VectorCypherRetriever(
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


def ask(
    driver: neo4j.Driver,
    cfg: Config,
    question: str,
    mode: Mode = "local",
    top_k: int = 5,
    return_context: bool = False,
):
    rag = build_rag(driver, cfg, mode)
    return rag.search(
        query_text=question,
        retriever_config={"top_k": top_k},
        return_context=return_context,
    )
