"""Environment-driven configuration. Every credential comes from the environment."""

from __future__ import annotations

import os
from dataclasses import dataclass, field
from pathlib import Path

from dotenv import load_dotenv

load_dotenv()

OPENROUTER_BASE_URL = "https://openrouter.ai/api/v1"


def _require(name: str) -> str:
    value = os.environ.get(name)
    if not value:
        raise RuntimeError(
            f"{name} is not set. Copy .env.example to .env and fill it in."
        )
    return value


@dataclass(frozen=True)
class Config:
    # --- Neo4j ---
    neo4j_uri: str = field(default_factory=lambda: os.getenv("NEO4J_URI", "bolt://localhost:7687"))
    neo4j_user: str = field(default_factory=lambda: os.getenv("NEO4J_USER", "neo4j"))
    neo4j_password: str = field(default_factory=lambda: _require("NEO4J_PASSWORD"))
    neo4j_database: str = field(default_factory=lambda: os.getenv("NEO4J_DATABASE", "neo4j"))

    # --- OpenRouter (chat + embeddings share one key) ---
    openrouter_api_key: str = field(default_factory=lambda: _require("OPENROUTER_API_KEY"))
    llm_model: str = field(
        default_factory=lambda: os.getenv("OPENROUTER_LLM_MODEL", "anthropic/claude-sonnet-4.5")
    )
    embedding_model: str = field(
        default_factory=lambda: os.getenv(
            "OPENROUTER_EMBEDDING_MODEL", "openai/text-embedding-3-small"
        )
    )
    # Must match the model above. text-embedding-3-small -> 1536.
    embedding_dimensions: int = field(
        default_factory=lambda: int(os.getenv("EMBEDDING_DIMENSIONS", "1536"))
    )

    # Output cap per structured call. Reasoning models spend tokens before
    # emitting JSON, so too small a value truncates the object mid-parse.
    llm_max_tokens: int = field(
        default_factory=lambda: int(os.getenv("LLM_MAX_TOKENS", "8000"))
    )
    # "low" | "medium" | "high", or empty to leave the model's default alone.
    # Some models (e.g. openai/gpt-oss-120b) reject reasoning being disabled.
    llm_reasoning_effort: str = field(
        default_factory=lambda: os.getenv("LLM_REASONING_EFFORT", "low")
    )
    # OpenRouter fans one model out to many providers whose speed differs by
    # more than an order of magnitude (measured: 3.5s on groq vs 66s on
    # auto-routing for the same extraction call). Pin the fast ones.
    openrouter_provider_order: str = field(
        default_factory=lambda: os.getenv("OPENROUTER_PROVIDER_ORDER", "groq")
    )
    # Keep True so a provider outage degrades to slower routing instead of
    # failing the run; set False to guarantee the pinned provider or error.
    openrouter_allow_fallbacks: bool = field(
        default_factory=lambda: os.getenv("OPENROUTER_ALLOW_FALLBACKS", "true").lower()
        not in ("0", "false", "no")
    )

    # Chunks extracted concurrently. Extraction is network-bound, so this is the
    # main throughput lever; raise it if your provider tolerates the rate.
    # A request with no timeout blocks forever. One stalled call held an
    # ingest for fifteen minutes with no error and no log line, which is worse
    # than a failure: a failure would have been retried.
    llm_timeout: float = field(
        default_factory=lambda: float(os.getenv("LLM_TIMEOUT", "120"))
    )

    extract_concurrency: int = field(
        default_factory=lambda: int(os.getenv("EXTRACT_CONCURRENCY", "8"))
    )

    # --- GROBID (scholarly PDF structuring service) ---
    grobid_url: str = field(
        default_factory=lambda: os.getenv("GROBID_URL", "http://localhost:8070")
    )

    # --- docling (table extraction; GROBID loses table bodies) ---
    # Conversion runs layout and table-structure models and takes minutes per
    # paper on CPU, so results are cached here, keyed by PDF content hash.
    # Set DOCLING_TABLES=0 to fall back to GROBID's own (much worse) tables.
    docling_tables: bool = field(
        default_factory=lambda: os.getenv("DOCLING_TABLES", "1") != "0"
    )
    docling_cache: Path = field(
        default_factory=lambda: Path(os.getenv("DOCLING_CACHE", "data/docling_cache"))
    )

    # --- OpenAlex (bibliographic enrichment; no key, polite pool wants a mailto) ---
    openalex_mailto: str = field(
        default_factory=lambda: os.getenv("OPENALEX_MAILTO", "anonymous@example.com")
    )

    # --- Chunking ---
    # 4000 matches neo4j-graphrag's own FixedSizeSplitter default. At 1200,
    # 22% of chunks yielded no entities and 25% no claims: too little context
    # per extraction call, and claims split across chunk boundaries.
    chunk_size: int = field(default_factory=lambda: int(os.getenv("CHUNK_SIZE", "4000")))
    chunk_overlap: int = field(default_factory=lambda: int(os.getenv("CHUNK_OVERLAP", "400")))

    # --- Community detection ---
    community_algorithm: str = field(
        default_factory=lambda: os.getenv("COMMUNITY_ALGORITHM", "leiden")  # leiden | louvain
    )
    # Leiden resolution. Below 1.0 yields fewer, larger communities; at the
    # default 1.0 a 131-concept graph fragmented into 19 communities for 5
    # papers, half of them with <=4 members.
    community_resolution: float = field(
        default_factory=lambda: float(os.getenv("COMMUNITY_RESOLUTION", "0.6"))
    )
    min_community_size: int = field(
        default_factory=lambda: int(os.getenv("MIN_COMMUNITY_SIZE", "4"))
    )


def provider_routing(cfg: Config) -> dict | None:
    """OpenRouter `provider` routing block, or None when unpinned."""
    order = [p.strip() for p in cfg.openrouter_provider_order.split(",") if p.strip()]
    if not order:
        return None
    return {"order": order, "allow_fallbacks": cfg.openrouter_allow_fallbacks}


def load_config() -> Config:
    return Config()
