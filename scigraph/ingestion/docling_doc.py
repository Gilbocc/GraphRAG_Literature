"""Body text and tables from docling, because GROBID loses most of a paper.

GROBID is excellent at bibliography and at header metadata, and poor at reading
a PDF's body. Measured across the five corpus papers by numeric recall — what
fraction of the numbers printed in the PDF survive parsing, which is the content
this graph is built from:

    paper                          GROBID   docling
    llm_legal_ai_survey             10.6%     98.0%
    better_call_gpt                 27.2%     97.3%
    legal_evaluations_challenges    61.6%     98.9%
    test_time_scaling_legal         69.7%     87.8%
    legal_retrieval_benchmark       71.7%     91.1%

GROBID was dropping up to 89% of a paper's numbers: whole appendix pages never
appeared in its <div> tree, and table bodies came back empty — one paper's
headline F-score table arrived as a single cell reading "and Palm2". Parsing
raised no error in either case, which is why this went unnoticed for so long.

So docling supplies the body and the tables; GROBID keeps references and the
DOI/arXiv identifiers. Conversion runs layout and table-structure models and
costs minutes per paper on CPU, so results are cached by PDF content hash.
"""

from __future__ import annotations

import hashlib
import json
import logging
import re
from pathlib import Path

log = logging.getLogger(__name__)

MIN_TABLE_CHARS = 40

# Page furniture and the bibliography: parsed into Reference nodes by GROBID,
# so including them here would duplicate them as body prose.
SKIP_LABELS = {"page_header", "page_footer", "footnote"}
NON_SECTION = ("references", "bibliography", "acknowledgment", "acknowledgement")

# Docling numbers headings ("3.1 Legal Reasoning Tasks"); the number is noise
# for matching but useful for reading order, so it is kept in the title only.
BODY_LABELS = {"text", "list_item", "caption", "code", "formula"}


def _digest(pdf: Path) -> str:
    return hashlib.sha256(pdf.read_bytes()).hexdigest()[:16]


# A standalone "References" line ends the body. Everything after it is the
# bibliography (GROBID's job, from the full PDF) and the appendices, which no
# extraction pass reads.
END_OF_BODY = re.compile(r"^\s*(references|bibliography)\s*$", re.I | re.M)


def _body_only(pdf: Path, tmp_dir: Path) -> tuple[Path, str]:
    """A copy of the PDF truncated at the bibliography, or the original.

    docling runs layout and table-structure models over every page, so a paper
    whose appendices dwarf its body pays almost all of its conversion cost on
    pages nothing will ever read — LegalBench is 143 pages of which the body is
    19. GROBID still gets the whole file, because the references it parses live
    in exactly the part cut here.
    """
    from pypdf import PdfReader, PdfWriter

    reader = PdfReader(str(pdf))
    cut = None
    for index, page in enumerate(reader.pages):
        if END_OF_BODY.search(page.extract_text() or ""):
            cut = index
            break
    if cut is None or cut < 2 or cut >= len(reader.pages) - 1:
        return pdf, f"{len(reader.pages)} pages (no bibliography found, using all)"

    writer = PdfWriter()
    for page in reader.pages[:cut]:
        writer.add_page(page)
    tmp_dir.mkdir(parents=True, exist_ok=True)
    out = tmp_dir / f"{pdf.stem}.body.pdf"
    with out.open("wb") as handle:
        writer.write(handle)
    return out, f"{cut} of {len(reader.pages)} pages (cut at the bibliography)"


def _convert(pdf: Path, tmp_dir: Path) -> dict:
    """Run docling. Slow and model-backed; only called on a cache miss."""
    from docling.document_converter import DocumentConverter

    body, note = _body_only(pdf, tmp_dir)
    log.info("Converting %s with docling: %s (minutes, then cached)", pdf.name, note)
    doc = DocumentConverter().convert(str(body)).document
    return {
        "tables": [
            {
                "page": table.prov[0].page_no if table.prov else None,
                "markdown": table.export_to_markdown(doc),
            }
            for table in doc.tables
        ],
        "texts": [
            {
                "page": item.prov[0].page_no if item.prov else None,
                "label": str(item.label),
                "text": item.text,
            }
            for item in doc.texts
            if getattr(item, "text", "").strip()
        ],
    }


def document(pdf: Path, cache_dir: Path) -> dict:
    """docling's parse of one PDF, converting only on a cache miss."""
    cache_dir.mkdir(parents=True, exist_ok=True)
    path = cache_dir / f"{pdf.stem}.{_digest(pdf)}.json"
    if path.exists():
        return json.loads(path.read_text())

    for stale in cache_dir.glob(f"{pdf.stem}.*.json"):
        stale.unlink()  # a previous version of the same paper

    # Keyed on the ORIGINAL file, so editing the paper invalidates the cache
    # even though conversion only ever sees the body.
    parsed = _convert(pdf, cache_dir / "_body")
    path.write_text(json.dumps(parsed, ensure_ascii=False))
    return parsed


def _is_reference_heading(title: str) -> bool:
    return title.strip().lower().lstrip("0123456789. ").startswith(NON_SECTION)


def body_sections(pdf: Path, cache_dir: Path) -> list[tuple[str, str, set[int]]]:
    """(title, text, pages) per section, split at docling's section headers.

    The first header is the paper title rather than a section, so text before
    any real heading is collected under "Frontmatter" — that is where the
    abstract lives when docling does not label it separately.
    """
    doc = document(pdf, cache_dir)
    out: list[tuple[str, list[str], set[int]]] = []
    title, buffer, pages = "Frontmatter", [], set()
    skipping = False
    # A heading whose whole body is subsections ("2 Related Work") produces no
    # section of its own, so its children arrive as bare "2.1 ..." with nothing
    # saying what they are part of. Carrying the parent into the child's title
    # keeps that context, which is what lets related work be recognised later.
    bodyless: dict[str, str] = {}

    for item in doc.get("texts", []):
        label = item.get("label", "")
        if label in SKIP_LABELS:
            continue

        if "header" in label or label == "title":
            if buffer and not skipping:
                out.append((title, buffer, pages))
            elif not buffer and (number := re.match(r"\s*(\d+)\s+\S", title)):
                bodyless[number.group(1)] = title  # a heading of subsections only

            title, buffer, pages = item["text"].strip()[:200], [], set()
            if (child := re.match(r"\s*(\d+)\.\d+\s+\S", title)) and (
                    parent := bodyless.get(child.group(1))):
                title = f"{parent} > {title}"[:200]
            # Everything from "References" to the next real heading is
            # bibliography; GROBID parses that properly into Reference nodes.
            skipping = _is_reference_heading(title)
            continue

        if skipping or label not in BODY_LABELS:
            continue
        buffer.append(item["text"])
        if item.get("page"):
            pages.add(item["page"])

    if buffer and not skipping:
        out.append((title, buffer, pages))

    return [(t, " ".join(b), p) for t, b, p in out if " ".join(b).strip()]


CAPTION_RE = re.compile(r"^\s*((?:Table|TABLE)\s*\d+[.:]?)", re.MULTILINE)


def _table_title(markdown: str, index: int) -> str:
    """The caption docling puts above the grid, else a positional fallback."""
    for line in markdown.splitlines():
        line = line.strip()
        if line and not line.startswith("|"):
            return line[:200]
    match = CAPTION_RE.search(markdown)
    return (match.group(1) if match else f"Table {index + 1}")[:200]


def table_sections(pdf: Path, cache_dir: Path) -> list[tuple[str, str, set[int]]]:
    """(title, text, pages) per table, in the shape the TEI reader returned."""
    out = []
    for index, table in enumerate(document(pdf, cache_dir).get("tables", [])):
        markdown = (table.get("markdown") or "").strip()
        if len(markdown) < MIN_TABLE_CHARS:
            continue
        page = table.get("page")
        out.append((_table_title(markdown, index), markdown, {page} if page else set()))
    return out
