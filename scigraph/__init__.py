"""scigraph — a Neo4j GraphRAG knowledge graph over scientific PDFs.

Layers, top to bottom:

    cli            command line entrypoint
    retrieval/     GraphRAG query modes (local, global, hybrid)
    enrichment/    passes over an already-populated graph
                   (biblio, dedupe, embed, communities, claims)
    ingestion/     PDF -> graph (grobid, extract, ingest)
    graph/         persistence: all Cypher, the only Neo4j access
    llm/           OpenRouter access for chat and embeddings
    config, models cross-cutting settings and schemas

Dependencies point downward only: nothing in `graph/` imports from
`ingestion/` or above.
"""

__version__ = "0.2.0"
