"""GraphStore — the only place that talks to Neo4j.

Callers get intention-revealing methods (`write_claims`, `claims_with_evidence`)
instead of holding Cypher and repeating session/transaction boilerplate. All
statements live in `cypher.py`; this module executes them.
"""

from __future__ import annotations

import logging
from collections.abc import Iterator
from contextlib import contextmanager
from typing import Any

import neo4j
from neo4j_graphrag.indexes import create_vector_index

from ..config import Config
from . import cypher

# Types worth reconciling across papers. Experiment and Result are per-paper
# artifacts, so merging them across papers would be wrong.
RECONCILABLE_KINDS = ["concept", "task", "metric", "benchmark", "corpus"]

log = logging.getLogger(__name__)


class GraphStore:
    def __init__(self, driver: neo4j.Driver, cfg: Config) -> None:
        self.driver = driver
        self.cfg = cfg
        self.database = cfg.neo4j_database

    # ------------------------------------------------------------- plumbing

    @contextmanager
    def session(self) -> Iterator[neo4j.Session]:
        with self.driver.session(database=self.database) as session:
            yield session

    def read(self, query: str, **params: Any) -> list[dict]:
        with self.session() as session:
            return session.run(query, **params).data()

    def read_one(self, query: str, **params: Any) -> dict | None:
        with self.session() as session:
            record = session.run(query, **params).single()
            return dict(record) if record else None

    def write(self, query: str, **params: Any) -> None:
        with self.session() as session:
            session.execute_write(lambda tx: tx.run(query, **params).consume())

    def close(self) -> None:
        self.driver.close()

    # --------------------------------------------------------------- schema

    def apply_schema(self) -> None:
        with self.session() as session:
            for statement in cypher.CONSTRAINTS + cypher.INDEXES:
                session.run(statement)
        log.info(
            "Applied %d constraints and %d indexes",
            len(cypher.CONSTRAINTS), len(cypher.INDEXES),
        )
        self._warn_on_dimension_mismatch()
        for name, (label, prop) in cypher.VECTOR_INDEXES.items():
            create_vector_index(
                self.driver,
                name=name,
                label=label,
                embedding_property=prop,
                dimensions=self.cfg.embedding_dimensions,
                similarity_fn="cosine",
                neo4j_database=self.database,
            )
        log.info(
            "Ensured %d vector indexes at %d dimensions",
            len(cypher.VECTOR_INDEXES), self.cfg.embedding_dimensions,
        )

    def _warn_on_dimension_mismatch(self) -> None:
        """create_vector_index is a no-op if the index exists at another size."""
        rows = self.read(cypher.SHOW_VECTOR_INDEXES, names=list(cypher.VECTOR_INDEXES))
        for row in rows:
            dims = ((row.get("options") or {}).get("indexConfig", {})).get("vector.dimensions")
            if dims is not None and int(dims) != self.cfg.embedding_dimensions:
                log.warning(
                    "Vector index %r exists with %d dimensions but EMBEDDING_DIMENSIONS=%d. "
                    "Run: python -m scigraph reset-vectors",
                    row["name"], int(dims), self.cfg.embedding_dimensions,
                )

    def drop_vector_indexes(self) -> None:
        with self.session() as session:
            for name in cypher.VECTOR_INDEXES:
                session.run(cypher.DROP_INDEX.format(name=name))
            session.run(cypher.CLEAR_EMBEDDINGS)
        log.info("Dropped vector indexes and cleared embeddings")

    def wipe(self) -> None:
        # CALL { ... } IN TRANSACTIONS is only valid in an implicit transaction,
        # so this cannot go through execute_write like every other write.
        with self.session() as session:
            session.run(cypher.WIPE).consume()
        log.info("Wiped graph data")

    # ------------------------------------------------------------ documents

    def write_document(self, paper: dict, sections: list[dict], chunks: list[dict]) -> None:
        self.write(cypher.WRITE_DOCUMENT, paper=paper, sections=sections, chunks=chunks)

    def write_references(self, source_id: str, refs: list[dict]) -> None:
        if refs:
            self.write(cypher.WRITE_REFERENCES, source_id=source_id, refs=refs)

    # ------------------------------------------------------------- entities

    def build_claim_graph(self, k: int = 6, min_similarity: float = 0.80) -> int:
        """Link each claim to its nearest cross-paper neighbours.

        0.80 is high on purpose, and 0.75 was tried and reverted. Every paper
        here is about LLMs and law, so at 0.75 the vector step called almost
        everything related: 662 edges instead of 281, and Leiden then returned
        two 70-plus-claim "communities" drawn from nine of the ten papers each,
        titled "Legal-LLM Evaluation" and "Legal-LLM Benchmarking" — one blob
        cut in half. Coverage rose and meaning fell.

        The lesson is that in a single-domain corpus broad connectedness is
        real, not a threshold artefact, so the vector step has to insist on
        specificity. What that leaves unconnected is a genuine cost — a third
        of MultiEURLEX's claims reach no community — and the answer to that is
        to stop making community membership the only route into an answer,
        which is why `hybrid` also retrieves chunks directly.
        """
        row = self.read_one(cypher.BUILD_CLAIM_GRAPH, k=k, min_similarity=min_similarity)
        created = row["created"] if row else 0
        log.info("Built %d cross-paper RELATED_CLAIM edges", created)
        return created


    # -------------------------------------------------------- paper profile

    def write_claims(self, claims: list[dict]) -> None:
        if claims:
            self.write(cypher.WRITE_CLAIMS, claims=claims)

    def suggest_papers(self, min_citers: int = 2, limit: int = 20) -> list[dict]:
        return self.read(cypher.SUGGEST_PAPERS, min_citers=min_citers, limit=limit)

    def write_datasets(self, rows: list[dict]) -> None:
        if rows:
            self.write(cypher.WRITE_DATASETS, rows=rows)

    def write_evidence(self, rows: list[dict]) -> None:
        if rows:
            self.write(cypher.WRITE_EVIDENCE, rows=rows)

    def link_subclaim(self, child_id: str, parent_id: str) -> None:
        self.write(cypher.LINK_SUBCLAIM, child_id=child_id, parent_id=parent_id)

    def drop_unsupported_subclaims(self) -> int:
        row = self.read_one(cypher.DROP_UNSUPPORTED_SUBCLAIMS)
        return row["dropped"] if row else 0

    def claims_with_evidence(self, paper_id: str) -> list[dict]:
        return self.read(cypher.CLAIMS_WITH_EVIDENCE, paper_id=paper_id)

    def mark_verdict(self, claim_id: str, status: str, contradicts: bool,
                     reason: str) -> None:
        self.write(cypher.MARK_VERDICT, claim_id=claim_id,
                   status=status, contradicts=contradicts, reason=reason)

    # ---------------------------------------------------------- communities

    def clear_communities(self) -> int:
        row = self.read_one(cypher.CLEAR_COMMUNITIES)
        return row["removed"] if row else 0

    def prune_communities(self, ids: list[str]) -> int:
        """Delete communities this run did not produce, keeping the rest."""
        row = self.read_one(cypher.PRUNE_COMMUNITIES, ids=ids)
        return row["removed"] if row else 0

    def write_communities(self, rows: list[dict], algorithm: str) -> None:
        if rows:
            self.write(cypher.WRITE_COMMUNITIES, rows=rows, algorithm=algorithm)

    def unsummarized_communities(self) -> list[str]:
        return [r["community_id"] for r in self.read(cypher.UNSUMMARIZED_COMMUNITIES)]

    def community_context(self, community_id: str) -> dict | None:
        return self.read_one(cypher.COMMUNITY_CONTEXT, community_id=community_id)

    def save_community_summary(
        self, community_id: str, title: str, summary: str, key_themes: list[str]
    ) -> None:
        self.write(
            cypher.SAVE_COMMUNITY_SUMMARY,
            community_id=community_id, title=title, summary=summary, key_themes=key_themes,
        )

    def delete_paper_content(self, paper_id: str) -> None:
        """Drop one paper's sections, chunks, claims, evidence and datasets."""
        self.write(cypher.DELETE_PAPER_CONTENT, paper_id=paper_id)

    # ----------------------------------------------------------- embeddings

    def pending_embeddings(self, label: str, limit: int) -> list[dict]:
        query, _ = cypher.EMBED_TARGETS[label]
        return self.read(query, limit=limit)

    def clear_label_embeddings(self, label: str) -> None:
        """Drop one label's vectors so the next `embed` regenerates them."""
        self.write(cypher.CLEAR_LABEL_EMBEDDINGS.format(label=label))

    def write_embeddings(self, label: str, rows: list[dict]) -> None:
        _, id_prop = cypher.EMBED_TARGETS[label]
        self.write(cypher.WRITE_EMBEDDING.format(label=label, id_prop=id_prop), rows=rows)

    # --------------------------------------------------------------- biblio

    def papers_to_enrich(self, include_stubs: bool, limit: int) -> list[dict]:
        return self.read(cypher.PAPERS_TO_ENRICH, include_stubs=include_stubs, limit=limit)

    def write_enrichment(self, rows: list[dict]) -> None:
        if rows:
            self.write(cypher.WRITE_ENRICHMENT, rows=rows)

    # ---------------------------------------------------------------- stats

    def node_counts(self) -> list[dict]:
        return self.read(cypher.NODE_COUNTS)

    def relationship_counts(self) -> list[dict]:
        return self.read(cypher.REL_COUNTS)

    def coverage(self) -> dict | None:
        return self.read_one(cypher.COVERAGE)
