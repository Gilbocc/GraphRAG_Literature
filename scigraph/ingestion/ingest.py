"""Write papers, sections, chunks, entities, relations, claims and evidence to Neo4j.

Provenance rule: every extracted claim and relationship carries paper_id, section,
page, chunk_id, supporting text, and confidence.
"""

from __future__ import annotations

import hashlib
import logging
import time
import re
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

from unidecode import unidecode

from ..config import Config
from ..graph.store import GraphStore
from ..llm.openrouter import StructuredLLM
from ..models import (
    ClaimVerdict,
    ParsedPaper,
)
from . import paper_extract as px
from . import spans
from .grobid import canonical_paper_id, load_directory, normalize_title_key

log = logging.getLogger(__name__)

# Guards against Cypher injection when interpolating a relationship type.


def _reference_rows(parsed) -> list[dict]:
    """Turn parsed references into mergeable stub-paper rows."""
    rows, seen = [], set()
    for ref in parsed.references:
        title_key = normalize_title_key(ref.title or "")
        if not (ref.doi or ref.arxiv_id or title_key):
            continue
        paper_id = canonical_paper_id(ref.doi, ref.arxiv_id, fallback=title_key or None)
        if paper_id in seen or paper_id == parsed.paper.paper_id:
            continue  # dedupe, and never let a paper cite itself
        seen.add(paper_id)
        rows.append({
            "paper_id": paper_id,
            "title": ref.title,
            "doi": ref.doi,
            "arxiv_id": ref.arxiv_id,
            "year": ref.year,
            "raw": ref.raw[:400],
            "resolved_by": "doi" if ref.doi else ("arxiv" if ref.arxiv_id else "title"),
        })
    return rows


def _claim_id(paper_id: str, text: str) -> str:
    """Key on the claim text, not the chunk.

    Overlapping chunks repeat sentences, so hashing the chunk id would create a
    separate Claim node per copy of the same assertion.
    """
    normalized = re.sub(r"[^a-z0-9]+", " ", text.lower()).strip()
    digest = hashlib.sha256(normalized.encode()).hexdigest()[:16]
    return f"{paper_id}::claim::{digest}"


def _evidence_id(claim_id: str, chunk_id: str, supporting_text: str) -> str:
    """One claim may be supported by several passages, so evidence keys on both."""
    digest = hashlib.sha256(f"{chunk_id}|{supporting_text}".encode()).hexdigest()[:12]
    return f"{claim_id}::ev::{digest}"


def _provenance(chunk_id: str | None, parsed: ParsedPaper) -> dict:
    """Section and page for a located chunk, falling back to the paper itself."""
    chunk = next((c for c in parsed.chunks if c.chunk_id == chunk_id), None)
    if chunk is None:
        first = parsed.chunks[0] if parsed.chunks else None
        return {
            "paper_id": parsed.paper.paper_id,
            "section": first.section_title if first else "",
            "page_start": first.page_start if first else 1,
            "page_end": first.page_end if first else 1,
            "chunk_id": first.chunk_id if first else "",
        }
    return {
        "paper_id": parsed.paper.paper_id, "section": chunk.section_title,
        "page_start": chunk.page_start, "page_end": chunk.page_end,
        "chunk_id": chunk.chunk_id,
    }


def _body_chunks(parsed: ParsedPaper) -> list:
    """Chunks of the paper's own argument: no appendices, no related work."""
    body = {title for title, _ in px._body_sections(parsed)}
    return [c for c in sorted(parsed.chunks, key=lambda c: c.index)
            if c.section_title in body]


def _find_subclaims(
    parsed: ParsedPaper, llm: StructuredLLM, claim_rows: list[dict], chunks: list,
) -> tuple[list[dict], list[tuple[str, str]]]:
    """Pass 2: walk the body in order, collecting claims the abstract omits.

    Sequential on purpose. Each chunk sees every claim found before it, so a
    finding it would otherwise restate is recognised as already known, and one
    it does introduce can be attached to the claim it elaborates. Running these
    concurrently would have every chunk propose against the same starting list
    and leave the duplicates to be reconciled afterwards.
    """
    claims = list(claim_rows)
    links: list[tuple[str, str]] = []

    started = time.monotonic()
    for position, chunk in enumerate(chunks, start=1):
        step = time.monotonic()
        try:
            found = px.find_subclaims(
                llm, chunk.text, [c["text"] for c in claims], chunk.section_title)
        except Exception as exc:
            log.warning("Subclaims failed for chunk %d/%d (%s): %s",
                        position, len(chunks), chunk.chunk_id, exc)
            continue

        log.info("  subclaims %d/%d  %.1fs  (+%d claims, %.0fs elapsed)  %s",
                 position, len(chunks), time.monotonic() - step,
                 len(found.new_claims), time.monotonic() - started,
                 chunk.section_title[:34])

        for new in found.new_claims:
            text = new.text.strip()
            if not text:
                continue
            claim_id = _claim_id(parsed.paper.paper_id, text)
            if any(c["claim_id"] == claim_id for c in claims):
                continue
            parent = (claims[new.parent_index]["claim_id"]
                      if 0 <= new.parent_index < len(claims) else None)
            claims.append({
                **_provenance(chunk.chunk_id, parsed),
                "claim_id": claim_id, "text": text, "claim_type": new.claim_type,
                "supporting_text": text, "verbatim": False,
                "confidence": new.confidence, "is_main": False,
                "rank": len(claims) + 1,
                "evidence_id": _evidence_id(claim_id, chunk.chunk_id, text),
            })
            if parent:
                links.append((claim_id, parent))
    return claims, links


def _find_evidence(
    parsed: ParsedPaper, cfg: Config, llm: StructuredLLM, claims: list[dict],
    chunks: list,
) -> tuple[list[dict], int]:
    """Pass 3: mark evidence for the complete claim set, chunk by chunk.

    Parallel, because the claim list no longer changes. It also means every
    chunk is judged against every claim — under a single growing-list pass the
    first chunk could only ever support the handful of claims known at that
    point, so evidence for anything discovered later was unreachable.
    """
    texts = [c["text"] for c in claims]

    def read(chunk):
        try:
            return chunk, px.find_evidence(llm, chunk.text, texts, chunk.section_title)
        except Exception as exc:
            log.debug("Evidence failed for %s: %s", chunk.chunk_id, exc)
            return chunk, None

    rows, unlocated, seen = [], 0, 0
    started = time.monotonic()
    with ThreadPoolExecutor(max_workers=max(1, cfg.extract_concurrency)) as pool:
        for chunk, found in pool.map(read, chunks):
            seen += 1
            log.info("  evidence %d/%d  (%.0fs elapsed)  %s",
                     seen, len(chunks), time.monotonic() - started,
                     chunk.section_title[:38])
            if found is None:
                continue
            prov = _provenance(chunk.chunk_id, parsed)
            for item in found.supports:
                if not (0 <= item.claim_index < len(claims)):
                    continue
                span = spans.locate(chunk.text, item.start_anchor, item.end_anchor)
                if not span:
                    unlocated += 1
                    continue
                text = chunk.text[span[0]:span[1]].strip()
                claim_id = claims[item.claim_index]["claim_id"]
                rows.append({
                    **prov, "claim_id": claim_id,
                    "evidence_id": _evidence_id(claim_id, chunk.chunk_id, text),
                    "text": text, "char_start": span[0], "char_end": span[1],
                    "confidence": item.confidence,
                })
    return rows, unlocated


def _verify_claims(
    store: GraphStore, cfg: Config, paper_id: str, llm: StructuredLLM
) -> dict[str, int]:
    """Judge each claim against the spans marked for it, and record the verdict.

    Claims are demoted rather than deleted. An earlier round of filtering in
    this project silently removed real content, and there was no way to see
    what had gone; a `verified` flag keeps the judgement visible and reversible.
    """
    rows = store.claims_with_evidence(paper_id)
    if not rows:
        return {"established": 0, "asserted": 0, "unsupported": 0, "contradicted": 0}

    def judge(row: dict) -> tuple[dict, object] | None:
        evidence = list(row["own_evidence"]) + [
            f"(via sub-claim) {t}" for t in row["via_subclaims"]]
        if not evidence:
            # Nothing to weigh: recorded rather than left unjudged, so the
            # graph says why the claim carries no weight.
            return row, ClaimVerdict(
                status="unsupported", contradicts=False,
                reason="No span in the paper's body was marked for this claim.")
        for _ in range(2):
            try:
                return row, px.verify_claim(llm, row["text"], evidence)
            except Exception as exc:
                log.debug("Verification failed for %s: %s", row["claim_id"], exc)
        return None

    counts = {"established": 0, "asserted": 0, "unsupported": 0, "contradicted": 0}
    seen = 0
    started = time.monotonic()
    with ThreadPoolExecutor(max_workers=max(1, cfg.extract_concurrency)) as pool:
        for result in pool.map(judge, rows):
            seen += 1
            log.info("  verify %d/%d  (%.0fs elapsed)", seen, len(rows),
                     time.monotonic() - started)
            if result is None:
                continue
            row, verdict = result
            store.mark_verdict(row["claim_id"], verdict.status,
                               verdict.contradicts, verdict.reason[:300])
            counts[verdict.status] += 1
            counts["contradicted"] += bool(verdict.contradicts)
            if verdict.status != "established":
                log.info("%s%s: %s -- %s", verdict.status.upper(),
                         " (contradicted)" if verdict.contradicts else "",
                         row["text"][:70], verdict.reason[:88])
    return counts


# A span that reports numbers is worth retrying: it is already known to be
# evidence, so failing to read it loses a whole table from an argument the
# graph otherwise holds correctly.
MEASUREMENT_ATTEMPTS = 3


def _key(text: str) -> str:
    """Fold a coordinate to a comparison key, so one number is one node."""
    return re.sub(r"[^a-z0-9]", "", unidecode(text or "").lower())


def _describe_datasets(
    store: GraphStore, parsed: ParsedPaper, llm: StructuredLLM
) -> int:
    """Record what the paper says about each dataset its numbers came from."""
    log.info("  describing datasets (one call over the whole paper)")
    try:
        found = px.describe_datasets(llm, parsed)
    except Exception as exc:
        log.warning("Dataset descriptions failed for %s: %s",
                    parsed.paper.paper_id, exc)
        return 0

    rows = []
    for d in found.datasets:
        name = d.name.strip()
        if not name:
            continue
        rows.append({
            "paper_id": parsed.paper.paper_id, "name": name,
            "key": _key(name), "description": d.description[:600],
            "size": d.size, "language": d.language, "domain": d.domain,
            "source": d.source, "supporting_text": d.supporting_text[:400],
            "introduced_here": d.introduced_here,
        })
    store.write_datasets(rows)
    return len(rows)


def _main_claim_rows(thesis, parsed: ParsedPaper) -> list[dict]:
    """The paper's claims, located back onto the chunk that states them.

    The paper's contribution is among these, asserted rather than described: a
    paper proposing a method is claiming that method works, and that claim is
    what the methodology sections exist to back.
    """
    rows = []
    for rank, claim in enumerate(thesis.main_claims, start=1):
        if not claim.text.strip():
            continue
        chunk_id, verbatim = px.locate(claim.supporting_text, parsed)
        prov = _provenance(chunk_id, parsed)
        claim_id = _claim_id(parsed.paper.paper_id, claim.text)
        rows.append({
            **prov, "claim_id": claim_id,
            "evidence_id": _evidence_id(claim_id, prov["chunk_id"], claim.supporting_text),
            "text": claim.text, "claim_type": claim.claim_type,
            "supporting_text": claim.supporting_text, "verbatim": verbatim,
            "confidence": claim.confidence, "is_main": True, "rank": rank,
        })
    return rows


def ingest_paper(
    store: GraphStore, cfg: Config, parsed: ParsedPaper, llm: StructuredLLM
) -> dict[str, int]:
    """Thesis first, then chunks that back it.

    Free-form chunk extraction produced entities that floated free of anything
    the paper argued, and whole-paper extraction summarized away the detail. So
    the paper is read whole once to establish what it claims, and every chunk
    pass afterwards answers a narrower question: what in here backs one of those
    claims, and with what evidence? Everything in the graph then hangs off a
    claim the paper actually makes.
    """

    stats = {"chunks": len(parsed.chunks),
             "claims": 0, "subclaims": 0, "evidence": 0, "datasets": 0,
             "references": 0, "unlocated": 0}

    store.write_document(
        parsed.paper.model_dump(),
        [sec.model_dump() for sec in parsed.sections],
        [c.model_dump() for c in parsed.chunks],
    )
    refs = _reference_rows(parsed)
    store.write_references(parsed.paper.paper_id, refs)
    stats["references"] = len(refs)

    # 1. What does this paper argue?
    try:
        thesis = px.extract_thesis(llm, parsed)
    except Exception as exc:
        log.error("Thesis pass failed for %s: %s", parsed.paper.paper_id, exc)
        return stats

    claim_rows = _main_claim_rows(thesis, parsed)
    store.write_claims(claim_rows)
    stats["claims"] = len(claim_rows)
    if not claim_rows:
        return stats

    chunks = _body_chunks(parsed)
    log.info("%s: %d of %d chunks are body (appendices and related work excluded)",
             parsed.paper.paper_id, len(chunks), len(parsed.chunks))

    timings: dict[str, float] = {}

    # 2. What else does the body argue that the abstract never says?
    mark = time.monotonic()
    claims, links = _find_subclaims(parsed, llm, claim_rows, chunks)
    timings["subclaims"] = time.monotonic() - mark
    store.write_claims(claims[len(claim_rows):])
    for child, parent in links:
        store.link_subclaim(child, parent)
    stats["claims"] = len(claims)
    stats["subclaims"] = len(links)

    # 3. Where is each of those claims supported? Judged against them all.
    mark = time.monotonic()
    evidence, unlocated = _find_evidence(parsed, cfg, llm, claims, chunks)
    timings["evidence"] = time.monotonic() - mark
    store.write_evidence(evidence)
    stats["evidence"] = len(evidence)
    stats["unlocated"] = unlocated

    # 4. A sub-claim nothing supports is not a claim the paper made.
    stats["dropped"] = store.drop_unsupported_subclaims()

    # 5. Does the evidence actually establish each claim?
    mark = time.monotonic()
    stats.update(_verify_claims(store, cfg, parsed.paper.paper_id, llm))
    timings["verify"] = time.monotonic() - mark

    mark = time.monotonic()
    stats["datasets"] = _describe_datasets(store, parsed, llm)
    timings["datasets"] = time.monotonic() - mark

    log.info("%s timings: %s | %d LLM calls, %.0fs in the model",
             parsed.paper.paper_id,
             "  ".join(f"{k}={v:.0f}s" for k, v in timings.items()),
             llm.calls, llm.seconds)

    log.info(
        "%s: %d claims (%d sub, %d dropped), %d evidence, "
        "%d established / %d asserted / %d unsupported, %d datasets",
        parsed.paper.title[:38], stats["claims"], stats["subclaims"],
        stats["dropped"], stats["evidence"], stats["established"],
        stats["asserted"], stats["unsupported"], stats["datasets"],
    )
    return stats


def ingest_directory(store: GraphStore, cfg: Config, directory: Path) -> dict[str, int]:
    llm = StructuredLLM(cfg)
    papers = load_directory(
        directory, cfg.chunk_size, cfg.chunk_overlap, cfg.grobid_url,
        cfg.docling_cache if cfg.docling_tables else None,
    )
    totals: dict[str, int] = {"papers": 0}
    for parsed in papers:
        stats = ingest_paper(store, cfg, parsed, llm)
        totals["papers"] += 1
        for key, value in stats.items():
            totals[key] = totals.get(key, 0) + value
    store.build_claim_graph()
    return totals
