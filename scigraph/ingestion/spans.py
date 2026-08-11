"""Locate a span in a chunk from its first and last few words.

Evidence is a range of the paper's own text, not something a model wrote. That
distinction is the point: when the model produced evidence prose, a third of it
turned out not to appear in the chunk at all, and there was no way to tell a
faithful quotation from an invention except by checking — which is exactly what
locating an anchor does, except here a failure to locate costs one span instead
of silently storing a fabrication.

Anchors rather than whole quotations because a span may be an entire results
table. Reproducing one verbatim is unreliable; naming its first and last few
words is not.
"""

from __future__ import annotations

import re

from rapidfuzz import fuzz

# Below this, an "anchor" is too generic to identify a position — "the", "we
# find" — and would match the wrong place confidently.
MIN_ANCHOR_CHARS = 8
# Fuzzy alignment floor. Anchors are usually copied exactly; this covers the
# cases where the model normalises whitespace, a ligature, or a dash.
MIN_RATIO = 82


# Papers use typographic dashes, quotes and ligatures that a model reproduces
# inconsistently; folding them costs nothing and recovers anchors that differ
# from the chunk only by a non-breaking hyphen.
_FOLD = str.maketrans({
    "\u2010": "-", "\u2011": "-", "\u2012": "-", "\u2013": "-", "\u2014": "-",
    "\u2018": "'", "\u2019": "'", "\u201c": '"', "\u201d": '"',
    "\u00a0": " ", "\u2009": " ", "\u202f": " ",
    "\ufb01": "fi", "\ufb02": "fl",
})


def _normalize(text: str) -> str:
    return re.sub(r"\s+", " ", (text or "").translate(_FOLD)).strip().lower()


def _find(needle: str, hay_norm: str, hay_map: list[int], start: int = 0) -> int | None:
    """Index in the ORIGINAL text where `needle` begins, or None."""
    needle = _normalize(needle)
    if len(needle) < MIN_ANCHOR_CHARS:
        return None
    at = hay_norm.find(needle, start)
    if at != -1:
        return hay_map[at]

    # Fuzzy: slide a window of the needle's length and keep the best match.
    best, best_at = MIN_RATIO, None
    width = len(needle)
    for i in range(start, max(start, len(hay_norm) - width) + 1, 4):
        score = fuzz.ratio(needle, hay_norm[i:i + width])
        if score > best:
            best, best_at = score, i
    return hay_map[best_at] if best_at is not None else None


def locate(text: str, start_anchor: str, end_anchor: str) -> tuple[int, int] | None:
    """Character range of the span in `text`, or None if it cannot be found.

    The end anchor is searched for *after* the start anchor, so a phrase that
    recurs later in the chunk cannot invert the range.
    """
    if not text:
        return None
    norm, index_map = [], []
    previous_space = True
    for i, ch in enumerate(text):
        lowered = ch.lower()
        if ch.isspace():
            if previous_space:
                continue
            norm.append(" ")
            index_map.append(i)
            previous_space = True
        else:
            norm.append(lowered)
            index_map.append(i)
            previous_space = False
    hay = "".join(norm)

    start = _find(start_anchor, hay, index_map)
    if start is None:
        return None

    # Search from the start of the start anchor, not from after it. Anchors are
    # meant to be 5-10 words but often come back as most of the sentence, and
    # then the end anchor lies INSIDE the start anchor — searching past it made
    # the span unlocatable even though both anchors were present verbatim.
    head = _normalize(start_anchor)
    at = hay.find(head)
    end = _find(end_anchor, hay, index_map, start=at if at != -1 else 0)
    if end is None:
        return None
    end += len(end_anchor.strip())

    # The span covers at least the start anchor: an end anchor found within it
    # means the start anchor already spanned the evidence.
    if at != -1:
        end = max(end, index_map[min(at + len(head) - 1, len(index_map) - 1)] + 1)
    if end <= start:
        return None
    return start, min(end, len(text))


def extract(text: str, start_anchor: str, end_anchor: str) -> str | None:
    """The span itself, taken from the chunk — never from the model."""
    found = locate(text, start_anchor, end_anchor)
    if not found:
        return None
    return text[found[0]:found[1]].strip()
