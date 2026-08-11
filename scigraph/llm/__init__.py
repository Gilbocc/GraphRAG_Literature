"""Model access. Everything goes through OpenRouter — chat and embeddings alike."""

from .openrouter import (
    StructuredLLM,
    embedder,
    graphrag_llm,
    neo4j_driver,
    raw_client,
)

__all__ = ["StructuredLLM", "embedder", "graphrag_llm", "neo4j_driver", "raw_client"]
