"""Query modes: local, global, hybrid — all citation-bearing — and a plain-RAG
baseline to measure them against."""

from .baseline import plain_rag
from .query import Mode, ask, build_rag

__all__ = ["Mode", "ask", "build_rag", "plain_rag"]
