"""Answer the same questions four ways and write the results down.

The graph is only worth its cost if retrieval that carries claims, verdicts and
themes beats retrieval that carries passages alone. That is a claim about
output quality, so it has to be read rather than measured — hence a file of
answers to compare side by side rather than a score.

Everything is held constant except retrieval: the same chunks, the same
embedding model, the same answering model. `plain` is the control.
"""

from __future__ import annotations

import datetime
import logging
from pathlib import Path

import neo4j

from .config import Config
from .retrieval import ask, plain_rag

log = logging.getLogger(__name__)

MODES = ("plain", "local", "global", "hybrid", "evidence")


def _answer(driver: neo4j.Driver, cfg: Config, mode: str, question: str, top_k: int) -> str:
    if mode == "plain":
        return plain_rag(driver, cfg, question, top_k=top_k)
    result = ask(driver, cfg, question, mode=mode, top_k=top_k)
    return getattr(result, "answer", str(result))


def compare(
    driver: neo4j.Driver,
    cfg: Config,
    questions: list[str],
    out: Path,
    top_k: int = 5,
) -> Path:
    """Write every question answered in every mode to one readable file."""
    stamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M")
    lines = [
        f"# Retrieval comparison — {stamp}",
        "",
        f"Answering model `{cfg.answer_model}` at temperature "
        f"{cfg.query_temperature}, embeddings `{cfg.embedding_model}`, "
        f"top_k={top_k}. Extraction ran on `{cfg.llm_model}`.",
        "",
        "- **plain** — nearest chunks only, no graph. The control.",
        "- **local** — nearest chunks, plus the claims each one grounds.",
        "- **global** — community summaries only.",
        "- **hybrid** — community summaries, plus each theme's claims and the "
        "verbatim passage behind them, plus the nearest chunks.",
        "- **evidence** — the verbatim spans nearest the question, at most two "
        "per paper.",
        "",
    ]

    for number, question in enumerate(questions, start=1):
        log.info("Q%d: %s", number, question)
        lines += [f"\n---\n\n## Q{number}. {question}\n"]
        for mode in MODES:
            log.info("  ... %s", mode)
            try:
                answer = _answer(driver, cfg, mode, question, top_k)
            except Exception as exc:  # a failing mode is a result too
                answer = f"_FAILED: {exc}_"
                log.error("  %s failed: %s", mode, exc)
            lines += [f"### {mode}", "", answer.strip(), ""]

    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text("\n".join(lines))
    log.info("Wrote %s", out)
    return out
