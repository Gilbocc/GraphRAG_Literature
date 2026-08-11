"""Persistence layer: all Cypher, and the only code that talks to Neo4j."""

from .store import GraphStore

__all__ = ["GraphStore"]
