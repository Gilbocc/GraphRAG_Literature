"""Scholarly PDF parsing via GROBID.

GROBID returns TEI XML with a proper section hierarchy, header metadata (title,
DOI, arXiv id), per-sentence page coordinates, and — critically for the citation
layer — bibliographic references parsed into structured records rather than raw
strings. Requires a running GROBID service (see README).
"""

from __future__ import annotations

import logging
import re
import xml.etree.ElementTree as ET
from pathlib import Path

import httpx

from ..models import Chunk, Paper, ParsedPaper, RawReference, Section

log = logging.getLogger(__name__)

TEI_NS = {"t": "http://www.tei-c.org/ns/1.0"}
ARXIV_RE = re.compile(r"(\d{4}\.\d{4,5})")
# Unfilled LaTeX/ACM template DOIs must not become a paper's primary key.
PLACEHOLDER_DOI_RE = re.compile(r"(n{4,}|x{4,}|1234567|0{6,})", re.IGNORECASE)

NON_SECTION_TAIL = ("references", "bibliography", "acknowledgment", "acknowledgement")


class GrobidError(RuntimeError):
    pass


def canonical_paper_id(
    doi: str | None, arxiv_id: str | None, fallback: str | None = None
) -> str:
    """Stable, mergeable id.

    Preference order matters: a paper cited by arXiv id in someone's reference
    list must land on the same node as that paper ingested from its own PDF, so
    real identifiers beat any local fallback.
    """
    if doi:
        return f"doi:{doi.lower()}"
    if arxiv_id:
        return f"arxiv:{arxiv_id.lower()}"
    if fallback:
        return f"title:{fallback}"
    raise ValueError("need one of doi, arxiv_id, or fallback")


def normalize_title_key(title: str) -> str:
    return re.sub(r"[^a-z0-9]+", " ", (title or "").lower()).strip()


# ------------------------------------------------------------------ GROBID call


def process_pdf(path: Path, base_url: str, timeout: float = 300.0) -> str:
    """Send one PDF to GROBID and return TEI XML."""
    url = base_url.rstrip("/") + "/api/processFulltextDocument"
    with path.open("rb") as handle:
        files = {"input": (path.name, handle, "application/pdf")}
        data = {
            "segmentSentences": "1",
            # Repeated form field: httpx encodes a list value as repeated keys.
            "teiCoordinates": ["s", "head", "figure"],
            "consolidateHeader": "0",
            "consolidateCitations": "0",
        }
        try:
            response = httpx.post(url, files=files, data=data, timeout=timeout)
        except httpx.HTTPError as exc:
            raise GrobidError(
                f"Could not reach GROBID at {base_url}: {exc}. "
                "Start it with: docker run -d --name grobid -p 8070:8070 "
                "lfoppiano/grobid:0.8.0"
            ) from exc
    if response.status_code != 200:
        raise GrobidError(f"GROBID returned {response.status_code} for {path.name}")
    return response.text


def check_alive(base_url: str, timeout: float = 10.0) -> bool:
    try:
        response = httpx.get(base_url.rstrip("/") + "/api/isalive", timeout=timeout)
        return response.status_code == 200 and "true" in response.text.lower()
    except httpx.HTTPError:
        return False


# ------------------------------------------------------------------ TEI parsing


def _text(element: ET.Element | None) -> str:
    if element is None:
        return ""
    return re.sub(r"\s+", " ", "".join(element.itertext())).strip()


def _pages(element: ET.Element | None) -> set[int]:
    """Page numbers from a GROBID coords attribute ('page,x,y,w,h;...')."""
    if element is None:
        return set()
    coords = element.get("coords") or ""
    pages = set()
    for span in coords.split(";"):
        head = span.split(",")[0]
        if head.isdigit():
            pages.add(int(head))
    return pages


def _header_ids(root: ET.Element) -> tuple[str | None, str | None]:
    doi = arxiv = None
    for idno in root.findall(".//t:sourceDesc//t:idno", TEI_NS):
        kind = (idno.get("type") or "").lower()
        value = (idno.text or "").strip()
        if not value:
            continue
        if kind == "doi" and not PLACEHOLDER_DOI_RE.search(value):
            doi = value.lower()
        elif kind == "arxiv":
            match = ARXIV_RE.search(value)
            if match:
                arxiv = match.group(1)
    return doi, arxiv


def _reference_from_bibl(bibl: ET.Element) -> RawReference | None:
    title = _text(bibl.find('.//t:title[@level="a"]', TEI_NS)) or _text(
        bibl.find('.//t:title[@level="m"]', TEI_NS)
    )
    doi = arxiv = None
    for idno in bibl.findall(".//t:idno", TEI_NS):
        kind = (idno.get("type") or "").lower()
        value = (idno.text or "").strip()
        if kind == "doi" and not PLACEHOLDER_DOI_RE.search(value):
            doi = value.lower()
        elif kind == "arxiv":
            match = ARXIV_RE.search(value)
            if match:
                arxiv = match.group(1)

    year = None
    date = bibl.find(".//t:date", TEI_NS)
    if date is not None:
        match = re.search(r"(19|20)\d{2}", date.get("when") or date.text or "")
        if match:
            year = int(match.group(0))

    authors = []
    for author in bibl.findall(".//t:author/t:persName", TEI_NS):
        name = " ".join(
            part for part in (
                _text(author.find("t:forename", TEI_NS)),
                _text(author.find("t:surname", TEI_NS)),
            ) if part
        )
        if name:
            authors.append(name)

    if not (title or doi or arxiv):
        return None  # unusable: nothing to key or display on
    return RawReference(
        raw=_text(bibl)[:600],
        title=title[:250] or None,
        doi=doi,
        arxiv_id=arxiv,
        year=year,
        authors=authors[:20],
    )


def _table_text(figure: ET.Element) -> str:
    """Render a TEI table as text so its numbers reach the extractor.

    GROBID emits tables as <figure type="table"> directly under <body>, outside
    the <div> hierarchy. Reading only <div> sentences discarded every results
    table — 161 cells in one paper — which is why headline numbers were missing.
    """
    head = _text(figure.find("t:head", TEI_NS))
    desc = _text(figure.find("t:figDesc", TEI_NS))
    lines = [" ".join(x for x in (head, desc) if x)]
    for row in figure.findall(".//t:row", TEI_NS):
        cells = [_text(c) for c in row.findall("t:cell", TEI_NS)]
        if any(cells):
            lines.append(" | ".join(cells))
    return "\n".join(line for line in lines if line.strip())


def _tables(root: ET.Element) -> list[tuple[str, str, set[int]]]:
    """(title, text, pages) for every table in the document."""
    body = root.find(".//t:body", TEI_NS)
    if body is None:
        return []
    out = []
    for figure in body.iter(f"{{{TEI_NS['t']}}}figure"):
        if (figure.get("type") or "") != "table":
            continue
        text = _table_text(figure)
        if len(text) < 40:
            continue
        title = _text(figure.find("t:head", TEI_NS)) or "Table"
        out.append((title[:200], text, _pages(figure)))
    return out


def _sentences(div: ET.Element) -> list[tuple[str, set[int]]]:
    out = []
    for sentence in div.findall(".//t:s", TEI_NS):
        text = _text(sentence)
        if text:
            out.append((text, _pages(sentence)))
    if not out:  # some divs carry bare <p> without sentence segmentation
        for para in div.findall("t:p", TEI_NS):
            text = _text(para)
            if text:
                out.append((text, set()))
    return out


def _chunk_sentences(
    sentences: list[tuple[str, set[int]]],
    section: Section,
    chunk_size: int,
    chunk_overlap: int,
    start_index: int,
) -> list[Chunk]:
    """Group whole sentences into chunks, carrying exact page ranges."""
    chunks: list[Chunk] = []
    buffer: list[tuple[str, set[int]]] = []
    length = 0

    def flush() -> None:
        nonlocal buffer, length
        if not buffer:
            return
        text = " ".join(s for s, _ in buffer)
        pages = {p for _, ps in buffer for p in ps} or {section.page_start}
        offset = len(chunks)
        chunks.append(
            Chunk(
                chunk_id=f"{section.section_id}::c{offset}",
                paper_id=section.paper_id,
                section_id=section.section_id,
                section_title=section.title,
                page_start=min(pages),
                page_end=max(pages),
                index=start_index + offset,
                text=text,
            )
        )
        # Carry trailing sentences forward as overlap.
        carry: list[tuple[str, set[int]]] = []
        carried = 0
        for item in reversed(buffer):
            if carried >= chunk_overlap:
                break
            carry.insert(0, item)
            carried += len(item[0])
        buffer = carry if carried < length else []
        length = sum(len(s) for s, _ in buffer)

    for sentence, pages in sentences:
        if length + len(sentence) > chunk_size and buffer:
            flush()
        buffer.append((sentence, pages))
        length += len(sentence)
    if buffer:
        # Final flush must not re-seed overlap.
        text = " ".join(s for s, _ in buffer)
        pages = {p for _, ps in buffer for p in ps} or {section.page_start}
        offset = len(chunks)
        chunks.append(
            Chunk(
                chunk_id=f"{section.section_id}::c{offset}",
                paper_id=section.paper_id,
                section_id=section.section_id,
                section_title=section.title,
                page_start=min(pages),
                page_end=max(pages),
                index=start_index + offset,
                text=text,
            )
        )
    return chunks


def parse_tei(
    xml: str,
    source_path: Path,
    chunk_size: int,
    chunk_overlap: int,
    tables: list[tuple[str, str, set[int]]] | None = None,
    body: list[tuple[str, str, set[int]]] | None = None,
) -> ParsedPaper:
    """Parse TEI into a paper, optionally taking body and tables from docling.

    GROBID reads bibliography and header metadata well and a paper's body
    badly — on this corpus it lost up to 89% of the numbers printed in a PDF,
    without raising an error. So callers may supply `body` and `tables` from
    docling and keep GROBID for references and identifiers. Passing None for
    both keeps the TEI content, which is what the offline fixture tests use.
    """
    root = ET.fromstring(xml)

    title = _text(root.find(".//t:titleStmt/t:title", TEI_NS))
    doi, arxiv_id = _header_ids(root)
    paper_id = canonical_paper_id(
        doi, arxiv_id, fallback=normalize_title_key(title) or source_path.stem
    )

    n_pages = 0
    for surface in root.findall(".//t:facsimile/t:surface", TEI_NS):
        if (surface.get("n") or "").isdigit():
            n_pages = max(n_pages, int(surface.get("n")))

    sections: list[Section] = []
    chunks: list[Chunk] = []

    abstract = root.find(".//t:profileDesc//t:abstract", TEI_NS)
    divs: list[tuple[str, ET.Element]] = []
    if abstract is not None and _text(abstract):
        divs.append(("Abstract", abstract))
    for div in root.findall(".//t:body/t:div", TEI_NS):
        head = div.find("t:head", TEI_NS)
        name = _text(head) or "Untitled section"
        divs.append((name, div))

    if body is not None:
        divs = []  # section order below comes from docling, not the TEI tree
        blocks = [
            (name, text, pages) for name, text, pages in body
            if not name.lower().startswith(NON_SECTION_TAIL)
        ]
    else:
        blocks = []
        for name, div in divs:
            if name.lower().startswith(NON_SECTION_TAIL):
                continue
            sentences = _sentences(div)
            if not sentences:
                continue
            pages = {p for _, ps in sentences for p in ps} | _pages(
                div.find("t:head", TEI_NS))
            blocks.append((name, " ".join(s for s, _ in sentences), pages))

    # Tables are placed at the page they appear on, not appended after the
    # body. Appending them made every table sort after a paper's appendices,
    # which is wrong on its own terms and made "where does the appendix start"
    # unanswerable from section order.
    table_blocks = _tables(root) if tables is None else tables
    ordered: list[tuple[int, int, str, str, set[int]]] = [
        (min(pages) if pages else 1, index, name, text, pages)
        for index, (name, text, pages) in enumerate(blocks)
    ]
    ordered += [
        # +0.5 in effect: a table sorts after the prose of the page it is on.
        (min(pages) if pages else 1, len(blocks) + index, name, text, pages)
        for index, (name, text, pages) in enumerate(table_blocks)
    ]
    ordered.sort(key=lambda row: (row[0], row[1]))

    for order, (_, _, name, text, pages) in enumerate(ordered):
        section = Section(
            section_id=f"{paper_id}::s{order}",
            paper_id=paper_id,
            title=name[:200],
            order=order,
            page_start=min(pages) if pages else 1,
            page_end=max(pages) if pages else 1,
            text=text,
        )
        sections.append(section)
        chunks.extend(
            _chunk_sentences(
                [(text, pages)], section, chunk_size, chunk_overlap, len(chunks)
            )
        )
        n_pages = max(n_pages, section.page_end)

    references = []
    for bibl in root.findall(".//t:listBibl/t:biblStruct", TEI_NS):
        reference = _reference_from_bibl(bibl)
        if reference:
            references.append(reference)

    paper = Paper(
        paper_id=paper_id,
        title=title or source_path.stem,
        doi=doi,
        arxiv_id=arxiv_id,
        source_path=str(source_path.resolve()),
        n_pages=n_pages,
    )
    log.info(
        "%s -> %d sections, %d chunks, %d refs (doi=%s arxiv=%s)",
        source_path.name, len(sections), len(chunks), len(references), doi, arxiv_id,
    )
    return ParsedPaper(
        paper=paper, sections=sections, chunks=chunks, references=references
    )


def parse_pdf(
    path: Path,
    chunk_size: int,
    chunk_overlap: int,
    grobid_url: str,
    table_cache: Path | None = None,
) -> ParsedPaper:
    """References and identifiers from GROBID, body and tables from docling."""
    doc_tables = doc_body = None
    if table_cache is not None:
        from .docling_doc import body_sections, table_sections

        doc_tables = table_sections(path, table_cache)
        doc_body = body_sections(path, table_cache)
    return parse_tei(
        process_pdf(path, grobid_url), path, chunk_size, chunk_overlap,
        doc_tables, doc_body,
    )


def load_directory(
    directory: Path,
    chunk_size: int,
    chunk_overlap: int,
    grobid_url: str,
    table_cache: Path | None = None,
) -> list[ParsedPaper]:
    pdfs = sorted(directory.glob("*.pdf"))
    if not pdfs:
        raise FileNotFoundError(f"No PDFs found in {directory}")
    if not check_alive(grobid_url):
        raise GrobidError(
            f"GROBID is not responding at {grobid_url}. Start it with:\n"
            "  docker run -d --name grobid -p 8070:8070 lfoppiano/grobid:0.8.0"
        )
    return [
        parse_pdf(p, chunk_size, chunk_overlap, grobid_url, table_cache)
        for p in pdfs
    ]
