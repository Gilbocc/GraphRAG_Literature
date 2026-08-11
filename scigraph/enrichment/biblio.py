"""Bibliographic enrichment from OpenAlex: year, venue, authors, citation counts.

This is API enrichment, not LLM extraction — it costs no tokens and is more
accurate than anything a model would infer from the PDF text.
"""

from __future__ import annotations

import difflib
import logging
import re
import time
import urllib.parse

import httpx

from ..config import Config
from ..graph.store import GraphStore

log = logging.getLogger(__name__)

OPENALEX = "https://api.openalex.org/works"


def _clean_for_filter(text: str) -> str:
    """OpenAlex filter values cannot contain , : or | — they are syntax."""
    return re.sub(r"\s+", " ", re.sub(r"[,:|]", " ", text)).strip()


def _get(client: httpx.Client, url: str) -> dict | None:
    try:
        response = client.get(url, timeout=30.0)
        if response.status_code == 200:
            return response.json()
        log.debug("OpenAlex %s -> %s", url, response.status_code)
    except httpx.HTTPError as exc:
        log.warning("OpenAlex request failed: %s", exc)
    return None


def resolve_work(client: httpx.Client, title: str, doi: str | None, arxiv_id: str | None,
                 mailto: str) -> dict | None:
    """Find the best OpenAlex record for a paper.

    Title search is tried even when an identifier exists, because arXiv preprint
    records frequently carry no `referenced_works` while the published version
    of the same paper does.
    """
    candidates: list[dict] = []

    if doi:
        work = _get(client, f"{OPENALEX}/doi:{urllib.parse.quote(doi)}?mailto={mailto}")
        if work:
            candidates.append(work)
    if arxiv_id:
        work = _get(client, f"{OPENALEX}/doi:10.48550/arXiv.{arxiv_id}?mailto={mailto}")
        if work:
            candidates.append(work)
    if title:
        query = urllib.parse.quote(_clean_for_filter(title))
        found = _get(
            client, f"{OPENALEX}?filter=title.search:{query}&per-page=5&mailto={mailto}"
        )
        for candidate in (found or {}).get("results", []):
            ratio = difflib.SequenceMatcher(
                None, title.lower(), (candidate.get("title") or "").lower()
            ).ratio()
            if ratio > 0.85:
                candidates.append(candidate)

    if not candidates:
        return None
    # Prefer the richest record: one with references beats a bare preprint stub.
    return max(
        candidates,
        key=lambda w: (len(w.get("referenced_works") or []), w.get("cited_by_count") or 0),
    )


def fetch_works(client: httpx.Client, ids: list[str], mailto: str) -> dict[str, dict]:
    """Resolve OpenAlex work ids to records, 50 per request.

    `referenced_works` comes back as bare ids, which are useless for checking a
    citation against a parsed reference list. One batched lookup per 50 turns
    them into titles, years and DOIs.
    """
    out: dict[str, dict] = {}
    for start in range(0, len(ids), 50):
        batch = [i.rsplit("/", 1)[-1] for i in ids[start:start + 50]]
        found = _get(
            client,
            f"{OPENALEX}?filter=openalex_id:{'|'.join(batch)}"
            f"&per-page=50&mailto={mailto}",
        )
        for work in (found or {}).get("results", []):
            out[work["id"]] = work
        time.sleep(0.2)  # polite pool
    return out


def _row_from_work(paper_id: str, work: dict) -> dict:
    source = (work.get("primary_location") or {}).get("source") or {}
    authors = []
    for position, authorship in enumerate(work.get("authorships") or []):
        author = authorship.get("author") or {}
        name = author.get("display_name")
        if not name:
            continue
        openalex_author = author.get("id") or ""
        authors.append({
            "key": openalex_author or f"name:{name.lower()}",
            "name": name,
            "orcid": author.get("orcid"),
            "position": position,
        })
    return {
        "paper_id": paper_id,
        "openalex_id": work.get("id"),
        "year": work.get("publication_year"),
        "published_date": work.get("publication_date"),
        "cited_by_count": work.get("cited_by_count"),
        "publication_type": work.get("type"),
        "venue": source.get("display_name"),
        "title": work.get("title"),
        "authors": authors[:60],
        "referenced_works": work.get("referenced_works") or [],
    }


ARXIV_DOI = re.compile(r"^10\.48550/arxiv\.(.+)$", re.IGNORECASE)


def citation_rows(cited: dict[str, dict]) -> list[dict]:
    """OpenAlex referenced works as CITES rows, keyed like GROBID's.

    Same paper_id scheme as the parsed reference list, so a work both sources
    know merges onto one node instead of appearing twice.
    """
    from ..ingestion.grobid import canonical_paper_id, normalize_title_key

    rows = []
    for work in cited.values():
        doi = (work.get("doi") or "").replace("https://doi.org/", "").lower() or None
        title = work.get("title") or ""
        arxiv = None
        if doi and (match := ARXIV_DOI.match(doi)):
            arxiv, doi = match.group(1), None
        if not (doi or arxiv or title):
            continue
        rows.append({
            "paper_id": canonical_paper_id(doi, arxiv, normalize_title_key(title)),
            "title": title or None,
            "doi": doi,
            "arxiv_id": arxiv,
            "year": work.get("publication_year"),
            "raw": work.get("id") or "",
            "resolved_by": "openalex",
        })
    return rows


def enrich(
    store: GraphStore,
    cfg: Config,
    include_stubs: bool = False,
    limit: int = 500,
    pause: float = 0.2,
) -> dict[str, int]:
    """Attach year, venue, authors, and citation counts from OpenAlex."""
    pending = store.papers_to_enrich(include_stubs, limit)

    if not pending:
        log.info("Nothing to enrich")
        return {"resolved": 0, "unresolved": 0}

    rows, unresolved, citations = [], 0, 0
    headers = {"User-Agent": f"scigraph/0.1 (mailto:{cfg.openalex_mailto})"}
    with httpx.Client(headers=headers, follow_redirects=True) as client:
        for record in pending:
            work = resolve_work(
                client,
                record.get("title") or "",
                record.get("doi"),
                record.get("arxiv_id"),
                cfg.openalex_mailto,
            )
            if work:
                row = _row_from_work(record["paper_id"], work)
                rows.append(row)
                # OpenAlex citations supplement GROBID's, they do not replace
                # them: arXiv preprint records carry no referenced_works at all
                # (4 of the 5 corpus papers), so the parsed list stays primary.
                if row["referenced_works"]:
                    cited = fetch_works(
                        client, row["referenced_works"], cfg.openalex_mailto)
                    links = citation_rows(cited)
                    store.write_references(record["paper_id"], links)
                    citations += len(links)
            else:
                unresolved += 1
                log.debug("Unresolved: %s", (record.get("title") or "")[:70])
            time.sleep(pause)  # stay inside the OpenAlex polite-pool rate limit

    store.write_enrichment(rows)

    log.info("Enriched %d papers (%d unresolved), %d OpenAlex citations",
             len(rows), unresolved, citations)
    return {"resolved": len(rows), "unresolved": unresolved,
            "openalex_citations": citations}
