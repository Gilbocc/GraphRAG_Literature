"""Embeddings for chunks, entities, claims, and community summaries.

Texts go up in batches — the embeddings endpoint accepts an array, and embedding
one node per request turned a few calls into thousands and dominated wall time.
"""

from __future__ import annotations

import logging

from openai import OpenAI

from ..config import Config
from ..graph.cypher import EMBED_TARGETS
from ..graph.store import GraphStore
from ..llm.openrouter import raw_client

log = logging.getLogger(__name__)

BATCH_SIZE = 128
MAX_CHARS = 24000  # roughly the model's per-input token ceiling


def embed_texts(client: OpenAI, model: str, texts: list[str]) -> list[list[float]]:
    response = client.embeddings.create(model=model, input=texts)
    return [d.embedding for d in sorted(response.data, key=lambda d: d.index)]


def embed_label(
    store: GraphStore, cfg: Config, client: OpenAI, label: str, batch_size: int = BATCH_SIZE
) -> int:
    total = 0
    while True:
        pending = store.pending_embeddings(label, batch_size)
        if not pending:
            break
        ids, texts = [], []
        for record in pending:
            text = (record.get("text") or "").strip()
            if text:
                ids.append(record["id"])
                texts.append(text[:MAX_CHARS])
        if not texts:
            break
        vectors = embed_texts(client, cfg.embedding_model, texts)
        store.write_embeddings(label, [{"id": i, "embedding": v} for i, v in zip(ids, vectors)])
        total += len(ids)
        log.info("Embedded %d %s nodes (%d total)", len(ids), label, total)
    return total


def embed_all(store: GraphStore, cfg: Config, client: OpenAI | None = None) -> dict[str, int]:
    client = client or raw_client(cfg)
    return {label: embed_label(store, cfg, client, label) for label in EMBED_TARGETS}
