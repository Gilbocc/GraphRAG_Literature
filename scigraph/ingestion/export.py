"""Write the merged parse of a paper to disk, for inspection.

Two parsers each contribute what they are good at — GROBID the bibliography and
the identifiers, docling the body text and the tables — and the result is
merged into one ParsedPaper. That merge only ever existed in memory on the way
into Neo4j, so there was no way to look at what the extractor would actually be
given. Everything upstream of the LLM is deterministic, so it is worth being
able to read it.

The JSON is complete and the text file is the readable rendering of the same
data, in reading order.
"""

from __future__ import annotations

import json
import logging
import re
from pathlib import Path

from ..models import ParsedPaper

log = logging.getLogger(__name__)


def _provenance(with_openalex: bool) -> dict:
    """Which source produced what, recorded next to the data it produced."""
    out = {
        "identifiers_title_and_references": "grobid",
        "sections_body_text_and_tables": "docling",
    }
    if with_openalex:
        out["year_venue_authors_and_citations"] = "openalex"
    return out


def _match_references(parsed: ParsedPaper, cited: dict[str, dict]) -> dict:
    """Cross-check GROBID's reference list against OpenAlex's referenced_works.

    Two independent sources for the same bibliography, so each covers the
    other's misses: GROBID reads the printed list and gets DOIs the API lacks,
    OpenAlex knows the works a preprint's reference list renders badly.
    """
    def key(title: str) -> str:
        return re.sub(r"[^a-z0-9]", "", (title or "").lower())[:60]

    grobid_keys = {key(r.title): r for r in parsed.references if (r.title or "").strip()}
    openalex_keys = {key(w.get("title") or ""): w for w in cited.values()}
    matched = sorted(set(grobid_keys) & set(openalex_keys))
    return {
        "grobid_only": sorted(
            grobid_keys[k].title for k in set(grobid_keys) - set(openalex_keys) if k
        )[:40],
        "openalex_only": sorted(
            openalex_keys[k].get("title") or "" for k in set(openalex_keys) - set(grobid_keys) if k
        )[:40],
        "matched_count": len(matched),
        "grobid_count": len(parsed.references),
        "openalex_count": len(cited),
    }


def as_dict(paper: ParsedPaper, openalex: dict | None = None) -> dict:
    doc = paper.paper
    return {
        "paper_id": doc.paper_id,
        "title": doc.title,
        "doi": doc.doi,
        "arxiv_id": doc.arxiv_id,
        "n_pages": doc.n_pages,
        "source_path": doc.source_path,
        "parsed_by": _provenance(openalex is not None),
        "openalex": openalex,
        "counts": {
            "sections": len(paper.sections),
            "chunks": len(paper.chunks),
            "references": len(paper.references),
        },
        "sections": [
            {
                "section_id": s.section_id,
                "order": s.order,
                "title": s.title,
                "page_start": s.page_start,
                "page_end": s.page_end,
                "text": s.text,
            }
            for s in sorted(paper.sections, key=lambda s: s.order)
        ],
        "chunks": [
            {
                "chunk_id": c.chunk_id,
                "index": c.index,
                "section_title": c.section_title,
                "page_start": c.page_start,
                "page_end": c.page_end,
                "text": c.text,
            }
            for c in sorted(paper.chunks, key=lambda c: c.index)
        ],
        "references": [r.model_dump() for r in paper.references],
    }


def as_text(paper: ParsedPaper, openalex: dict | None = None) -> str:
    """The same content, laid out to be read."""
    doc = paper.paper
    out = [
        f"{doc.title}",
        f"paper_id : {doc.paper_id}",
        f"doi      : {doc.doi or '-'}",
        f"arxiv    : {doc.arxiv_id or '-'}",
        f"pages    : {doc.n_pages}",
        "parsed   : identifiers+references by GROBID, body+tables by docling",
        f"contents : {len(paper.sections)} sections, {len(paper.chunks)} chunks, "
        f"{len(paper.references)} references",
    ]
    if openalex:
        record = openalex.get("record") or {}
        check = openalex.get("reference_check") or {}
        out += [
            "",
            "-- OpenAlex " + "-" * 66,
            f"openalex : {record.get('openalex_id') or '(unresolved)'}",
            f"year     : {record.get('year') or '-'}    "
            f"venue: {record.get('venue') or '-'}",
            f"type     : {record.get('publication_type') or '-'}    "
            f"cited by: {record.get('cited_by_count')}",
            f"authors  : {', '.join(a['name'] for a in (record.get('authors') or [])[:8])}",
            f"refs     : GROBID {check.get('grobid_count', 0)}, "
            f"OpenAlex {check.get('openalex_count', 0)}, "
            f"agreeing {check.get('matched_count', 0)}",
        ]
    out += [
        "",
        "=" * 78,
        "SECTIONS",
        "=" * 78,
    ]
    for section in sorted(paper.sections, key=lambda s: s.order):
        pages = (f"p.{section.page_start}" if section.page_start == section.page_end
                 else f"p.{section.page_start}-{section.page_end}")
        out += ["", f"## [{section.order}] {section.title}  ({pages})", "", section.text]

    out += ["", "=" * 78, "REFERENCES", "=" * 78, ""]
    for i, ref in enumerate(paper.references, start=1):
        ids = " ".join(x for x in (
            f"doi:{ref.doi}" if ref.doi else "",
            f"arxiv:{ref.arxiv_id}" if ref.arxiv_id else "",
            f"({ref.year})" if ref.year else "",
        ) if x)
        authors = ", ".join(ref.authors[:4]) + ("..." if len(ref.authors) > 4 else "")
        out.append(f"[{i:>3}] {ref.title or ref.raw[:90]}")
        if authors or ids:
            out.append(f"      {authors}  {ids}".rstrip())
    return "\n".join(out)


def openalex_block(paper: ParsedPaper, cfg) -> dict | None:
    """Resolve this paper on OpenAlex and check its bibliography against ours."""
    import httpx

    from ..enrichment.biblio import _row_from_work, fetch_works, resolve_work

    doc = paper.paper
    headers = {"User-Agent": f"scigraph/0.1 (mailto:{cfg.openalex_mailto})"}
    with httpx.Client(headers=headers, follow_redirects=True) as client:
        work = resolve_work(
            client, doc.title, doc.doi, doc.arxiv_id, cfg.openalex_mailto)
        if not work:
            log.warning("OpenAlex could not resolve %s", doc.title[:60])
            return {"record": None, "reference_check": None}
        row = _row_from_work(doc.paper_id, work)
        cited = fetch_works(client, row["referenced_works"], cfg.openalex_mailto)

    return {
        "record": row,
        "referenced_works": [
            {
                "openalex_id": w.get("id"),
                "title": w.get("title"),
                "year": w.get("publication_year"),
                "doi": w.get("doi"),
            }
            for w in cited.values()
        ],
        "reference_check": _match_references(paper, cited),
    }


def export(
    paper: ParsedPaper, directory: Path, openalex: dict | None = None
) -> tuple[Path, Path]:
    """Write <paper>.json and <paper>.txt; returns both paths."""
    directory.mkdir(parents=True, exist_ok=True)
    stem = Path(paper.paper.source_path).stem
    json_path = directory / f"{stem}.json"
    text_path = directory / f"{stem}.txt"
    json_path.write_text(
        json.dumps(as_dict(paper, openalex), ensure_ascii=False, indent=2))
    text_path.write_text(as_text(paper, openalex))
    log.info("Wrote %s and %s", json_path, text_path)
    return json_path, text_path
