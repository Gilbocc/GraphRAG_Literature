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

    # --- Querying ---
    # Extraction and answering are different jobs. Extraction fills a fixed JSON
    # schema from one chunk, where a small fast model at temperature 0 is right
    # and the bill is one call per chunk per pass. Answering synthesises a dozen
    # passages across papers into cited prose, happens a handful of times, and
    # is where a stronger model is worth paying for. These override the
    # extraction settings above; each falls back to it when unset.
    #
    # Mind OPENROUTER_PROVIDER_ORDER: it is pinned to groq, which serves
    # gpt-oss only. Naming a query model from another family without also
    # setting QUERY_PROVIDER_ORDER (blank is fine) routes to a provider that
    # cannot serve it.
    query_llm_model: str | None = field(
        default_factory=lambda: os.getenv("QUERY_LLM_MODEL")
    )
    query_reasoning_effort: str | None = field(
        default_factory=lambda: os.getenv("QUERY_REASONING_EFFORT")
    )
    query_provider_order: str | None = field(
        default_factory=lambda: os.getenv("QUERY_PROVIDER_ORDER")
    )
    # Answering stays deterministic by default: a citation that changes between
    # runs is not checkable. Raise it only to sample phrasings deliberately.
    query_temperature: float = field(
        default_factory=lambda: float(os.getenv("QUERY_TEMPERATURE", "0.0"))
    )

    @property
    def answer_model(self) -> str:
        return self.query_llm_model or self.llm_model

    @property
    def answer_reasoning_effort(self) -> str:
        effort = self.query_reasoning_effort
        return self.llm_reasoning_effort if effort is None else effort

    @property
    def answer_provider_order(self) -> str:
        order = self.query_provider_order
        return self.openrouter_provider_order if order is None else order

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
    # Leiden resolution, which now sets the granularity of the finest level
    # only. It used to matter a great deal, because detection kept just the
    # last level Leiden produced — the fully merged one — and at ten papers
    # that was one 89-claim group spanning nine of them. Raising gamma to force
    # that level apart worked but flattened the hierarchy: at 2.4 the levels
    # came out near-identical, leaving nothing to choose between.
    #
    # Keeping the intermediate levels makes low values better, not worse: at
    # 0.6 the middle levels separate cleanly into 16 fine themes and 7 broad
    # ones, which is the range worth retrieving over.
    community_resolution: float = field(
        default_factory=lambda: float(os.getenv("COMMUNITY_RESOLUTION", "0.6"))
    )
    # Leiden is randomised; without a fixed seed the same graph partitions
    # differently every run, and the difference is amplified by
    # min_community_size below, which discards whatever ends up too small.
    community_seed: int = field(
        default_factory=lambda: int(os.getenv("COMMUNITY_SEED", "42"))
    )
    min_community_size: int = field(
        default_factory=lambda: int(os.getenv("MIN_COMMUNITY_SIZE", "4"))
    )


def provider_routing(cfg: Config, order: str | None = None) -> dict | None:
    """OpenRouter `provider` routing block, or None when unpinned.

    `order` defaults to the extraction pin; pass `cfg.answer_provider_order` for
    the query path, which may name a different model on a different provider.
    """
    if order is None:
        order = cfg.openrouter_provider_order
    providers = [p.strip() for p in order.split(",") if p.strip()]
    if not providers:
        return None
    return {"order": providers, "allow_fallbacks": cfg.openrouter_allow_fallbacks}


def load_config() -> Config:
    return Config()
