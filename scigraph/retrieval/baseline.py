"""A plain RAG baseline: embed the chunks, retrieve, answer. No graph.

The point of the graph is supposed to be that retrieval returns more than the
nearest passages — the claims a passage grounds, whether the paper established
them or merely argued them, the datasets it worked on. That is a claim worth
testing rather than assuming, and it can only be tested against the obvious
alternative.

So this uses the same chunks, the same embedding model and the same answering
model as the graph path, and differs in exactly one way: it retrieves passages
by similarity and passes them through, with nothing attached.
"""

from __future__ import annotations

import logging

import neo4j

from ..config import Config
from ..llm.openrouter import embedder, graphrag_llm

log = logging.getLogger(__name__)

# Same fields a reader needs to follow a citation, and nothing the graph adds.
PLAIN_QUERY = """
CALL db.index.vector.queryNodes('chunk_embeddings', $top_k, $embedding)
YIELD node AS chunk, score
MATCH (chunk)<-[:HAS_CHUNK]-(section:Section)<-[:HAS_SECTION]-(paper:Paper)
RETURN paper.title AS paper, section.title AS section,
       chunk.page_start AS page_start, chunk.page_end AS page_end,
       chunk.text AS text, score
ORDER BY score DESC
"""

PROMPT = """\
You answer questions about a corpus of scientific papers, using only the
passages below. Each carries its paper, section and page.

Cite as (Paper title, Section, p.N). Quote the paper's own words where the
wording matters. Where a passage is a table, read the whole table rather than
one row.

If the passages do not answer the question, say so plainly and say what they do
cover. Do not fill a gap with knowledge from outside them.

Passages:
{context}

Question:
{question}

Answer, then a Sources section listing each paper, section and page you used:
"""


def plain_rag(
    driver: neo4j.Driver, cfg: Config, question: str, top_k: int = 5,
    return_context: bool = False,
) -> str | tuple[str, str]:
    """Answer from the nearest chunks alone."""
    vector = embedder(cfg).embed_query(question)
    with driver.session(database=cfg.neo4j_database) as session:
        rows = list(session.run(PLAIN_QUERY, embedding=vector, top_k=top_k))

    context = "\n\n".join(
        f"--- PASSAGE (similarity {r['score']:.3f}) ---\n"
        f"Paper: {r['paper']}\n"
        f"Section: {r['section']}\n"
        f"Pages: {r['page_start']}-{r['page_end']}\n"
        f"Passage text:\n{r['text']}"
        for r in rows
    )
    answer = graphrag_llm(cfg).invoke(
        PROMPT.format(context=context, question=question)).content
    return (answer, context) if return_context else answer
