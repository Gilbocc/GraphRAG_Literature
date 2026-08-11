"""Command line entrypoint.

    python -m scigraph pipeline data/papers     # everything, in order
    python -m scigraph ask "..." --mode local|global|hybrid
"""

from __future__ import annotations

import argparse
import logging
import sys
from pathlib import Path

from .config import load_config
from .enrichment import (
    detect_communities,
    embed_all,
    enrich,
    link_claims,
    list_disagreements,
    summarize_communities,
)
from .graph import GraphStore
from .ingestion import ingest_directory
from .llm import StructuredLLM, neo4j_driver, raw_client
from .retrieval import ask, plain_rag


def _setup_logging(verbose: bool) -> None:
    logging.basicConfig(
        level=logging.DEBUG if verbose else logging.INFO,
        format="%(levelname)s %(name)s: %(message)s",
    )
    for noisy in ("neo4j", "httpx", "neo4j.notifications"):
        logging.getLogger(noisy).setLevel(logging.WARNING)


def _build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="scigraph", description=__doc__)
    parser.add_argument("-v", "--verbose", action="store_true")
    sub = parser.add_subparsers(dest="command", required=True)

    sub.add_parser("init", help="Create constraints and vector indexes")

    p_ingest = sub.add_parser("ingest", help="Parse PDFs and extract into the graph")
    p_ingest.add_argument("directory", type=Path)

    sub.add_parser("embed", help="Embed chunks, claims and community summaries")

    p_comm = sub.add_parser("communities", help="Detect communities and summarize them")
    p_comm.add_argument("--skip-summaries", action="store_true")

    p_bib = sub.add_parser("biblio", help="Enrich papers from OpenAlex (year, venue, authors)")
    p_bib.add_argument("--include-stubs", action="store_true",
                       help="also resolve cited-but-not-ingested papers")

    p_link = sub.add_parser("link-claims", help="Judge and link claim pairs across papers")
    p_link.add_argument("--limit", type=int, default=200)
    p_link.add_argument("--min-similarity", type=float, default=0.78)

    sub.add_parser("disagreements", help="List contradicting claims across papers")

    p_ask = sub.add_parser("ask", help="Query the graph")
    p_ask.add_argument("question")
    p_ask.add_argument("--mode", choices=["local", "global", "hybrid"], default="local")
    p_ask.add_argument("--top-k", type=int, default=5)
    p_ask.add_argument("--show-context", action="store_true")
    p_ask.add_argument("--plain", action="store_true",
                       help="answer from nearest chunks only, no graph (baseline)")

    p_pipe = sub.add_parser("pipeline", help="init -> ingest -> embed -> communities -> biblio -> claim links")
    p_pipe.add_argument("directory", type=Path)

    p_ex = sub.add_parser(
        "export-parsed",
        help="Write the merged GROBID+docling parse of each PDF to JSON and text")
    p_ex.add_argument("directory", type=Path)
    p_ex.add_argument("--out", type=Path, default=Path("data/parsed"))
    p_ex.add_argument("--no-openalex", action="store_true",
                      help="skip bibliographic lookup (offline)")

    p_ds = sub.add_parser(
        "datasets", help="Re-describe the datasets each paper uses or introduces")
    p_ds.add_argument("directory", type=Path)

    p_cmp = sub.add_parser(
        "compare", help="Answer questions in every mode and write them to a file")
    p_cmp.add_argument("questions", nargs="+")
    p_cmp.add_argument("--out", type=Path, default=Path("data/comparisons/latest.md"))
    p_cmp.add_argument("--top-k", type=int, default=5)

    p_sg = sub.add_parser(
        "suggest", help="Rank works the corpus cites but does not contain")
    p_sg.add_argument("--min-citers", type=int, default=2)
    p_sg.add_argument("--limit", type=int, default=20)

    sub.add_parser("stats", help="Show node and relationship counts")
    sub.add_parser("reset-vectors",
                   help="Drop vector indexes and embeddings (after changing dimensions)")
    sub.add_parser("wipe", help="Delete all graph data")
    return parser


def _print_stats(store: GraphStore) -> None:
    print("Nodes:")
    for record in store.node_counts():
        print(f"  {record['label']:>22}: {record['n']}")
    print("Relationships:")
    for record in store.relationship_counts():
        print(f"  {record['label']:>22}: {record['n']}")
    coverage = store.coverage()
    if coverage:
        print(f"Embedded nodes: {coverage['embedded']} | "
              f"communities summarized: {coverage['summarized']}")


def _print_disagreements(rows: list[dict]) -> None:
    if not rows:
        print("No contradictions found. Run 'link-claims' first.")
        return
    for row in rows:
        print(f"\n[conf {row['confidence']:.2f}] {row['rationale']}")
        print(f"  A: {row['claim_a']}")
        print(f"     -- {row['paper_a']}, {row['section_a']}, p.{row['page_a']}")
        print(f"  B: {row['claim_b']}")
        print(f"     -- {row['paper_b']}, {row['section_b']}, p.{row['page_b']}")


def main(argv: list[str] | None = None) -> int:
    args = _build_parser().parse_args(argv)
    _setup_logging(args.verbose)

    cfg = load_config()

    # Parsing touches no database, so this runs without Neo4j.
    if args.command == "export-parsed":
        from .ingestion.export import export, openalex_block
        from .ingestion.grobid import load_directory

        papers = load_directory(
            args.directory, cfg.chunk_size, cfg.chunk_overlap, cfg.grobid_url,
            cfg.docling_cache if cfg.docling_tables else None,
        )
        for paper in papers:
            block = None if args.no_openalex else openalex_block(paper, cfg)
            json_path, text_path = export(paper, args.out, block)
            record = (block or {}).get("record") or {}
            check = (block or {}).get("reference_check") or {}
            print(f"{paper.paper.title[:44]:46s} -> {json_path.name}"
                  f"  openalex={record.get('year') or '-'}"
                  f" refs {check.get('grobid_count', 0)}/{check.get('openalex_count', 0)}"
                  f" agree {check.get('matched_count', 0)}")
        return 0

    store = GraphStore(neo4j_driver(cfg), cfg)

    try:
        if args.command == "init":
            store.apply_schema()

        elif args.command == "ingest":
            print(f"Ingested: {ingest_directory(store, cfg, args.directory)}")

        elif args.command == "datasets":
            from .ingestion.grobid import load_directory
            from .ingestion.ingest import _describe_datasets

            llm = StructuredLLM(cfg)
            total = 0
            for parsed in load_directory(
                    args.directory, cfg.chunk_size, cfg.chunk_overlap, cfg.grobid_url,
                    cfg.docling_cache if cfg.docling_tables else None):
                total += _describe_datasets(store, parsed, llm)
            print(f"Datasets described: {total}")

        elif args.command == "embed":
            print(f"Embedded: {embed_all(store, cfg, raw_client(cfg))}")

        elif args.command == "communities":
            print(f"Detection: {detect_communities(store, cfg)}")
            if not args.skip_summaries:
                print(f"Summarized {summarize_communities(store, cfg)} communities")

        elif args.command == "biblio":
            print(f"OpenAlex: {enrich(store, cfg, include_stubs=args.include_stubs)}")

        elif args.command == "link-claims":
            print(f"Claim links: "
                  f"{link_claims(store, cfg, limit=args.limit, min_similarity=args.min_similarity)}")

        elif args.command == "disagreements":
            _print_disagreements(list_disagreements(store))

        elif args.command == "ask":
            if args.plain:
                print(plain_rag(store.driver, cfg, args.question, top_k=args.top_k))
            else:
                result = ask(store.driver, cfg, args.question,
                             mode=args.mode, top_k=args.top_k)
                print(getattr(result, "answer", result))

        elif args.command == "pipeline":
            store.apply_schema()
            print(f"Ingested: {ingest_directory(store, cfg, args.directory)}")
            print(f"Embedded: {embed_all(store, cfg, raw_client(cfg))}")
            print(f"Detection: {detect_communities(store, cfg)}")
            print(f"Summarized {summarize_communities(store, cfg)} communities")
            print(f"Embedded: {embed_all(store, cfg, raw_client(cfg))}")
            print(f"OpenAlex: {enrich(store, cfg)}")
            print(f"Claim links: {link_claims(store, cfg)}")

        elif args.command == "compare":
            from .compare import compare

            print(f"Wrote {compare(store.driver, cfg, args.questions, args.out, args.top_k)}")

        elif args.command == "suggest":
            rows = store.suggest_papers(args.min_citers, args.limit)
            if not rows:
                print(f"Nothing cited by {args.min_citers}+ of the ingested papers.")
            for row in rows:
                ident = row["doi"] or row["arxiv_id"] or ""
                print(f"\n[{row['citers']} papers cite it]  "
                      f"({row['year'] or '?'})  {(row['title'] or '?')[:76]}")
                if ident:
                    print(f"    {ident}")
                print(f"    cited by: {', '.join(t[:34] for t in row['cited_by'])}")

        elif args.command == "stats":
            _print_stats(store)

        elif args.command == "reset-vectors":
            store.drop_vector_indexes()
            store.apply_schema()

        elif args.command == "wipe":
            store.wipe()

    finally:
        store.close()

    return 0


if __name__ == "__main__":
    sys.exit(main())
