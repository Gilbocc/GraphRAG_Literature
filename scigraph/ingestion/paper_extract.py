"""Whole-paper extraction in focused passes.

Per-chunk extraction splits apart the things needed to interpret a fact: a table
cell holds the number, the header names the metric, the caption names the
dataset, and the surrounding prose names the split. Measured on this corpus,
63% of extracted Results could not be linked to their metric, dataset and model
because no single chunk contained all of them.

Given the whole paper, the same model links 100% of them. Two findings drove
this design:

- Context was never the constraint. A paper is ~9K tokens against a 131K window.
  The binding limit was the *output* cap: a 299-result response was truncated at
  max_tokens=8000 and discarded, yielding zero.
- A single general-purpose prompt over a whole paper *summarizes* — it returned
  17 entities where per-chunk extraction found ~300. A focused prompt over the
  same input returned 301 results. Exhaustiveness follows from narrow job scope,
  not from context length.

So: one pass per kind of thing, each with a large output budget. Chunks remain
the retrieval and citation index; extracted items are mapped back onto them for
provenance.
"""

from __future__ import annotations

import logging
import re
from typing import TYPE_CHECKING

from rapidfuzz import fuzz

from ..models import (
    ChunkEvidence,
    DatasetDetails,
    ChunkSubclaims,
    ClaimVerdict,
    PaperThesis,
    ParsedPaper,
)

if TYPE_CHECKING:  # heavy import chain
    from ..llm import StructuredLLM

log = logging.getLogger(__name__)

# The model's context is ~131K tokens; 400K chars leaves ample headroom and is
# larger than any paper in the corpus. The previous 120K silently truncated the
# retrieval-benchmark paper, which docling parses to 152K chars — the cap was
# set when GROBID was losing two thirds of every paper.
MAX_INPUT_CHARS = 400_000

# One results call must emit every number in the paper, so its output — not its
# input — is the binding limit. Past this many characters of input the paper is
# split into windows and the results are merged, because a single call that
# overruns max_tokens returns an empty completion and yields nothing at all.
RESULTS_WINDOW_CHARS = 60_000

# A table that fails is a table's worth of numbers gone, so it is worth retrying
# before giving up and saying so loudly.
RESULTS_ATTEMPTS = 3


# Sections that hold no claim of the paper's own. Related work states what
# *other* papers found, and appendices hold task definitions, prompts and
# transcripts — including both cost tokens and invites claims attributed to the
# wrong paper. Everything else is kept: limitations, ablations and error
# analysis are where several real claims live, so an abstract-only pass misses
# them.
NON_CLAIM_TITLES = re.compile(
    r"^\s*(?:[A-E]\s+|\d+(?:\.\d+)*\s*)?"
    r"(related\s+work|related\s+survey|background|prior\s+work|appendi|acknowledg|ethics|"
    r"references|bibliography|ccs\s+concepts|keywords|acm\s*reference)",
    re.IGNORECASE,
)
# Appendix headings look like "Appendix B", "A.1 Chinese Legal Tasks", or just
# "H Retrieval Results". The last form cannot be recognised by shape alone: the
# retrieval paper's own title section is "A Reasoning-Focused Legal Retrieval
# Benchmark", identical in form to its appendix "A Bar Exam QA Dataset
# Construction". A pattern loose enough to catch the appendix ate the title and
# 59 sections with it; a pattern tight enough to spare the title recognised no
# appendix in that paper at all, so every appendix table was extracted.
#
# What actually separates them is position: appendices follow the body. So the
# search starts after the last numbered section ("7 Conclusion") and takes the
# first lettered heading from there.
LETTERED_HEADING = re.compile(r"^\s*(?:appendix\b|[A-Z](?:\.\d+)*\s+\S)", re.IGNORECASE)
NUMBERED_HEADING = re.compile(r"^\s*\d+(?:\.\d+)*\s+\S")


def appendix_start(sections) -> int | None:
    """Order of the first appendix section, or None if the paper has none."""
    ordered = sorted(sections, key=lambda s: s.order)
    numbered = [s.order for s in ordered if NUMBERED_HEADING.match(s.title)]
    body_end = max(numbered) if numbered else -1

    for section in ordered:
        if re.match(r"^\s*(?:appendix\b|[A-Z]\.\d)", section.title, re.IGNORECASE):
            return section.order  # unambiguous, wherever it sits
        if section.order > body_end and LETTERED_HEADING.match(section.title):
            return section.order
    return None


THESIS_SECTIONS = re.compile(
    r"^\s*(?:[IVX]+\.?\s*|\d+(?:\.\d+)*\s*)?"
    r"(abstract|introduction|conclusion|frontmatter)", re.IGNORECASE)


def thesis_text(parsed: ParsedPaper) -> str:
    """Abstract, introduction and conclusion — where a paper states its thesis.

    The rest of the body is not read here on purpose: findings that live only
    in the results or discussion are picked up chunk by chunk as new claims,
    anchored to the thesis-level claim they elaborate.
    """
    kept = [
        f"\n\n## {title}\n{text}"
        for title, text in _body_sections(parsed)
        if THESIS_SECTIONS.match(title)
    ]
    return "".join(kept)[:MAX_INPUT_CHARS] or claim_text(parsed)


def claim_text(parsed: ParsedPaper) -> str:
    """The paper minus the parts that carry none of its own claims.

    Related-work subsections are numbered under a parent heading ("2.1 ...")
    that often has no body of its own and so never becomes a section, which is
    why the parent's number is resolved first and its children dropped with it.
    """
    return "".join(
        f"\n\n## {title}\n{text}"
        for title, text in _body_sections(parsed)
        # Numbers are the results pass's job, not the claims pass's.
        if not re.match(r"^\s*table\s*\d", title, re.IGNORECASE)
    )[:MAX_INPUT_CHARS]


def _blocks(parsed: ParsedPaper) -> list[str]:
    """Section-headed pieces in reading order."""
    parts, current = [], None
    for chunk in sorted(parsed.chunks, key=lambda c: c.index):
        if chunk.section_title != current:
            current = chunk.section_title
            parts.append(f"\n\n## {current}\n")
        parts.append(chunk.text)
    return parts


def _body_sections(parsed: ParsedPaper) -> list[tuple[str, str]]:
    """(title, text) for the paper's own body: no related work, no appendices.

    Related work reports other papers' numbers. Appendices hold secondary
    detail, and anything there that matters is picked up by the per-chunk
    backing pass, which reads every chunk including the appendix ones.
    """
    prefixes = {
        match.group(1)
        for s in parsed.sections
        if (match := re.match(r"^\s*(\d+)(?:\.\d+)*\s*(.*)$", s.title))
        and re.match(r"(related\s+work|background|prior\s+work)", match.group(2), re.IGNORECASE)
    }
    cutoff = appendix_start(parsed.sections)
    kept = []
    for section in sorted(parsed.sections, key=lambda s: s.order):
        if cutoff is not None and section.order >= cutoff:
            continue  # appendices carry no claim of the paper's own
        if NON_CLAIM_TITLES.match(section.title):
            continue
        number = re.match(r"^\s*(\d+)(?:\.\d+)*\s", section.title)
        if number and number.group(1) in prefixes:
            continue
        kept.append((section.title, section.text))
    return kept


def _header(parsed: ParsedPaper) -> str:
    return f"TITLE: {parsed.paper.title}\n\n"


def _normalize(text: str) -> str:
    return re.sub(r"\s+", " ", text or "").strip().lower()


def locate(supporting_text: str, parsed: ParsedPaper) -> tuple[str | None, bool]:
    """Find the chunk a span came from, so whole-paper output keeps page-level provenance.

    Returns (chunk_id, verbatim). Exact containment first, then fuzzy alignment
    for spans the model reworded.
    """
    needle = _normalize(supporting_text)
    if len(needle) < 12:
        return None, False
    for chunk in parsed.chunks:
        if needle in _normalize(chunk.text):
            return chunk.chunk_id, True
    best, best_score = None, 0.0
    for chunk in parsed.chunks:
        score = fuzz.partial_ratio(needle, _normalize(chunk.text))
        if score > best_score:
            best, best_score = chunk.chunk_id, score
    return (best, False) if best_score >= 75 else (None, False)


# --------------------------------------------------------------- thesis-first

THESIS_PROMPT = """\
You read a whole scientific paper and state what it ARGUES.

- contribution: what the paper adds that did not exist before. One sentence.
- research_question: the question it answers. One sentence.
- central_concepts: 5-8 concepts the paper is about, most central first, named as
  short canonical noun phrases another paper could reuse.
- main_claims: 5-15 assertions the paper actually argues for, most important
  first. A main claim is something another paper could agree or disagree with —
  a finding, a comparison, a limitation, or a property of a method.

  Claim 1 must be the paper's contribution, stated as the assertion the paper is
  making about it: "Legal-R1, fine-tuned on a bilingual chain-of-thought legal
  dataset, matches larger proprietary models on Chinese legal reasoning", not
  "we introduce Legal-R1". A paper proposing a method, dataset or benchmark is
  claiming that artifact works, and that is the claim everything else in the
  paper is built to support — name the artifact in it.

  Bare procedure without an assertion is not a claim ("we evaluate 12 models").
  Cover the abstract, results, discussion and limitations.

Every claim needs `supporting_text`: a verbatim span from the paper.
"""

SUBCLAIM_PROMPT = """\
You are reading one chunk of a paper's body, and you already know the claims
the paper makes at the top level — the ones it states in its abstract,
introduction and conclusion.

Your only job here is to find claims this chunk argues that are NOT already on
the list. Do not mark evidence, do not quote, do not repeat a claim already
listed in other words.

A claim is an assertion another paper could disagree with:
  "paraphrasing query expansion does not improve and can hurt retrieval"
  "improvements in retrieval recall do not always translate to downstream QA"
It is not a description of what was done ("we evaluate five retrievers"), and
it is not a fact quoted from a worked example or a dataset sample.

For each new claim, set parent_index to the listed claim it elaborates — the
one it narrows, qualifies, or gives a special case of. A finding in the body
nearly always elaborates something the paper already argues at the top level,
so choose the closest. Use -1 only if it truly relates to none of them.

Most chunks introduce no new claim at all. Returning an empty list is the
normal outcome for background, setup and method description.
"""

EVIDENCE_PROMPT = """\
You are given one chunk of a paper and the COMPLETE list of claims that paper
makes, top-level claims and their sub-claims together.

Your only job is to mark evidence. For each claim this chunk supports, give the
span that is the evidence, by its first 5-10 words and its last 5-10 words,
copied EXACTLY from the chunk.

The span may be a sentence, a paragraph, or an ENTIRE TABLE. If a results table
is the evidence, anchor from its caption through to its final row so that every
row is inside the span. Never shorten a table to its interesting rows, and
never write the table out — the two anchors are enough.

Do not invent claims here; the list is complete. Do not mark a span that merely
mentions the same topic — it must actually support the claim. A chunk that
supports nothing returns an empty list.
"""

VERDICT_PROMPT = """\
You are given one claim attributed to a paper, and the passages from that paper
that were marked as its evidence.

Some evidence is marked "via sub-claims": a narrower claim of the same paper,
followed by the passage backing it. A general claim is often demonstrated that
way — an abstract says models of one kind outperform another, and the body
shows it model by model — so treat what the sub-claims establish as backing the
general claim.

Choose one status:

established — a passage reports a result, measurement or observation that makes
  the claim true, or its sub-claims collectively do.

asserted — the paper genuinely argues this, and the evidence is that argument:
  an analysis, a position, a discussion of consequences or risks. No experiment
  demonstrates it, but the paper is making the claim. A paper's discussion of
  liability or interpretability belongs here, not below.

unsupported — the evidence does not back the claim at all. It states an
  intention ("we use this method to study whether simplifying the query helps"),
  describes a method or dataset without an outcome, reports what OTHER work has
  done, or is an axis label, caption fragment or header carrying no content.

Set contradicts as well if a passage reports the OPPOSITE of the claim.

Be strict about the difference between arguing something and merely mentioning
it. This graph exists to be cited from, and an assertion the paper never made
is the one thing it must not contain.
"""

VERDICT_PROMPT = """\
You are given one claim attributed to a paper, and the passages from that paper
that were marked as its evidence.

Some evidence is marked "via sub-claims": a narrower claim of the same paper,
followed by the passage backing it. A general claim is often demonstrated that
way — an abstract says models of one kind outperform another, and the body
shows it model by model — so treat what the sub-claims establish as backing the
general claim.

Choose one status:

established — a passage reports a result, measurement or observation that makes
  the claim true, or its sub-claims collectively do.

asserted — the paper genuinely argues this, and the evidence is that argument:
  an analysis, a position, a discussion of consequences or risks. No experiment
  demonstrates it, but the paper is making the claim. A paper's discussion of
  liability or interpretability belongs here, not below.

unsupported — the evidence does not back the claim at all. It states an
  intention ("we use this method to study whether simplifying the query helps"),
  describes a method or dataset without an outcome, reports what OTHER work has
  done, or is an axis label, caption fragment or header carrying no content.

Set contradicts as well if a passage reports the OPPOSITE of the claim.

Be strict about the difference between arguing something and merely mentioning
it. This graph exists to be cited from, and an assertion the paper never made
is the one thing it must not contain.
"""

MEASUREMENT_PROMPT = """\
You are given a span of text that has already been established as evidence for
a claim. Extract every number it reports.

Each measurement has one field per coordinate, and each belongs in its own:
- metric    what was measured           "Recall@10", "F1"
- method    the model or system ALONE   "BM25", "E5-large-v2"
- dataset   what it was measured ON     "CAIL2018", "Bar Exam QA"   REQUIRED
- condition the setting varied          "baseline", "open-book"  (empty if none)
- value, unit, interval

Never write "BM25 (Bar Exam QA) - structured reasoning" as a method: that is a
method, a dataset and a condition, and each has its own field.

Every measurement needs a dataset. A number with no data behind it cannot be
interpreted, so there is no such thing as a result without one:
- a named benchmark or corpus, as the paper writes it
- a corpus this paper built: use the paper's own name, or describe it as the
  paper does — "10 procurement contracts", "26 bilingual legal cases"
- a task within a benchmark, when results are reported per task: "Article
  Recitation", "Charge Prediction"

Emit ONLY results of evaluating something on data. A parameter count ("7B"), a
temperature, a context-window limit, the number of tasks in a benchmark or the
size of a split are properties, not measurements — leave them out entirely.

If the span is a table, emit one entry per cell, reading the method from its row
and the dataset or condition from its column header. Be exhaustive — a table of
fourteen result numbers yields fourteen entries. If the span reports no results,
return an empty list.
"""


def extract_thesis(llm: StructuredLLM, parsed: ParsedPaper) -> PaperThesis:
    """The paper's contribution, central concepts and main claims, read whole."""
    return llm.parse(THESIS_PROMPT, _header(parsed) + thesis_text(parsed), PaperThesis)


def _with_claims(claims: list[str], chunk_text: str, section: str, header: str) -> str:
    listing = "\n".join(f"[{i}] {c}" for i, c in enumerate(claims))
    return (
        f"{header}\n{listing}\n\n"
        f"Chunk (section: {section}):\n\"\"\"\n{chunk_text}\n\"\"\"\n"
    )


def find_subclaims(
    llm: StructuredLLM, chunk_text: str, claims: list[str], section: str
) -> ChunkSubclaims:
    """Pass 2: claims this chunk argues that are not yet known."""
    return llm.parse(
        SUBCLAIM_PROMPT,
        _with_claims(claims, chunk_text, section, "Claims known so far:"),
        ChunkSubclaims,
    )


def find_evidence(
    llm: StructuredLLM, chunk_text: str, claims: list[str], section: str
) -> ChunkEvidence:
    """Pass 3: which claims this chunk supports, against the complete set."""
    return llm.parse(
        EVIDENCE_PROMPT,
        _with_claims(claims, chunk_text, section, "All claims this paper makes:"),
        ChunkEvidence,
    )


DATASET_PROMPT = """\
You are reading ONE SECTION of a paper, and you already know the datasets found
in the sections before it, with everything recorded about each so far.

Return a dataset only when this section changes what is known:

  - A dataset not on the list at all: return it with existing_index = -1.
  - A dataset already on the list, where this section adds something the record
    is missing or gets wrong: return it with existing_index set to its position
    on the list, and fill in EVERY field — the ones already known as well as
    the ones you are adding. What you return replaces the record entirely, so
    anything you leave out is lost. Never return a shorter description than the
    one already recorded.
  - A dataset already on the list that this section adds nothing to: leave it
    out. Most sections mention datasets without adding anything.

Names change across a paper — "CUAD", "the Contract Understanding Atticus
Dataset", "our dataset", "the corpus" all name one thing. Match on what is
being described, not on the string.

`description` is the important field. Say what the examples actually are, what
the model is asked to do, and what a correct answer looks like. Write it so a
reader who has never seen the dataset understands the task:

  good — "Multiple-choice questions from the Chinese national judicial
  examination. Each item gives a fact pattern and four candidate answers, one
  or more of which are correct; a model must select the correct set. Drawn from
  JEC-QA and scored by exact match."

  useless — "A Chinese legal dataset used for evaluation."

Never write a description that would fit any dataset in the field. If the paper
does not say enough to write a real one, say what it does say and leave it
short rather than padding it with generic phrasing.

The other fields: `introduced_here` is true when THIS paper builds or releases
the dataset — check the title and abstract, not just the section in front of
you, because a paper introducing a dataset spends most of its sections simply
using it. It is false only for data that existed before this paper. Then its size, language, legal domain or jurisdiction, and where the
data came from — a prior dataset, a court, an exam board, a government
database. Take all of it from the paper; leave a field empty rather than
supplying knowledge from elsewhere.

`supporting_text` must be a verbatim span from THIS section describing it.

Include a dataset only if this paper actually evaluates on it or builds it.
Datasets mentioned only as prior work someone else used do not belong here.
"""


# Sections that describe data. Every other pass reads a bounded slice of the
# paper; this one used to send the whole paper in a single request, which made
# it both the largest call in the pipeline and the one that hung — sixteen
# minutes on a 60k-character prompt, with the socket timeout unable to bound it.
DATA_SECTION = re.compile(
    r"data|dataset|corpus|benchmark|task|experiment|setup|evaluat|abstract|"
    r"introduction|resource|annotat",
    re.I,
)
MAX_DATASET_CHARS = 8000


def dataset_sections(parsed: ParsedPaper) -> list[tuple[str, str]]:
    """Body sections likely to describe data, each bounded to one small call."""
    out = []
    for title, text in _body_sections(parsed):
        if not DATA_SECTION.search(title):
            continue
        text = text.strip()
        if text:
            out.append((title, text[:MAX_DATASET_CHARS]))
    return out


def _known_datasets(known: list[dict]) -> str:
    """The running record, as the model needs to see it to add to it."""
    if not known:
        return "Datasets found so far: (none yet — this is the first section)\n"
    lines = ["Datasets found so far:"]
    for index, d in enumerate(known):
        lines.append(
            f"[{index}] {d['name']}"
            f"\n     description: {d.get('description') or '(missing)'}"
            f"\n     size: {d.get('size') or '(missing)'}"
            f" | language: {d.get('language') or '(missing)'}"
            f" | domain: {d.get('domain') or '(missing)'}"
            f" | source: {d.get('source') or '(missing)'}"
        )
    return "\n".join(lines) + "\n"


def describe_datasets_in(
    llm: StructuredLLM, parsed: ParsedPaper, title: str, text: str,
    known: list[dict],
) -> DatasetDetails:
    """Datasets this section adds to what is already known."""
    user = (
        f"{_header(parsed)}{_known_datasets(known)}\n"
        f"SECTION — {title}\n{text}\n"
    )
    return llm.parse(DATASET_PROMPT, user, DatasetDetails)


def verify_claim(llm: StructuredLLM, claim: str, evidence: list[str]) -> ClaimVerdict:
    """Does the evidence found for this claim actually establish it?"""
    listing = "\n\n".join(f"- {e[:1200]}" for e in evidence)
    user = f"CLAIM:\n{claim}\n\nEVIDENCE MARKED FOR IT:\n{listing}\n"
    return llm.parse(VERDICT_PROMPT, user, ClaimVerdict)


