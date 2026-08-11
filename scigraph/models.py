"""Pydantic schemas: PDF structure + the LLM's structured extraction output."""

from __future__ import annotations

from typing import Literal

from pydantic import BaseModel, Field

# ---------------------------------------------------------------- document side


class Chunk(BaseModel):
    chunk_id: str
    paper_id: str
    section_id: str
    section_title: str
    page_start: int
    page_end: int
    index: int
    text: str


class Section(BaseModel):
    section_id: str
    paper_id: str
    title: str
    order: int
    page_start: int
    page_end: int
    text: str


class Paper(BaseModel):
    paper_id: str
    title: str
    doi: str | None = None
    arxiv_id: str | None = None
    source_path: str
    n_pages: int


class RawReference(BaseModel):
    """One entry parsed out of a paper's reference list."""

    raw: str
    title: str | None = None
    doi: str | None = None
    arxiv_id: str | None = None
    year: int | None = None
    authors: list[str] = Field(default_factory=list)


class ParsedPaper(BaseModel):
    paper: Paper
    sections: list[Section]
    chunks: list[Chunk]
    references: list[RawReference] = Field(default_factory=list)


# ---------------------------------------------------------------- extraction side

Attribution = Literal["own", "cited"]


class DatasetDetail(BaseModel):
    """What a paper says about a dataset it uses or introduces.

    An evidence span names a dataset in passing; these details are what a
    retriever hands an LLM when the question is about the data itself — what the
    examples are, how many, in what language, from where.
    """

    name: str = Field(description="The dataset as the paper names it.")
    introduced_here: bool = Field(
        description="True if this paper builds or releases it, False if it reuses it."
    )
    description: str = Field(
        description=(
            "What the examples are, what the model must do with them, and what "
            "counts as correct — written so someone who has never seen this "
            "dataset could interpret a score reported on it. A description that "
            "would fit any dataset in the field is worse than a short one."
        )
    )
    size: str = Field(default="", description="Examples, queries or documents, if stated.")
    language: str = Field(default="", description="Language(s), if stated.")
    domain: str = Field(default="", description="Legal area or jurisdiction, if stated.")
    source: str = Field(
        default="",
        description="Where the data came from: a prior dataset, a court, an exam board.",
    )
    supporting_text: str = Field(
        default="", description="Verbatim span from the paper describing it."
    )


class DatasetDetails(BaseModel):
    datasets: list[DatasetDetail] = Field(default_factory=list)


class Span(BaseModel):
    """A range of the chunk, given by its first and last few words.

    Anchors rather than the whole quotation: a span may be an entire results
    table, and asking a model to reproduce one verbatim fails. Anchors are
    short, and the text between them is taken from the chunk itself — so the
    stored evidence is the paper's own words by construction, and cannot be a
    paraphrase or an invention.
    """

    start_anchor: str = Field(
        description="The first 5-10 words of the span, copied exactly."
    )
    end_anchor: str = Field(
        description="The last 5-10 words of the span, copied exactly."
    )


class ClaimSupport(Span):
    """Evidence in this chunk for one claim, given by its anchors."""

    claim_index: int = Field(description="Index of the claim being supported.")
    confidence: float = Field(ge=0.0, le=1.0, default=0.8)


class ChunkEvidence(BaseModel):
    """Pass 3: what this chunk supports, judged against the complete claim set."""

    supports: list[ClaimSupport] = Field(default_factory=list)


class NewClaim(BaseModel):
    """A claim the body argues that the abstract never states."""

    text: str = Field(description="The claim as one self-contained sentence.")
    claim_type: str = Field(
        default="finding",
        description="finding, comparison, limitation, method_property, or contribution.",
    )
    parent_index: int = Field(
        description=(
            "Index of the claim from the list that this one elaborates — the "
            "claim it narrows, explains, qualifies or gives a special case of. "
            "Nearly every finding in a paper's body elaborates something the "
            "paper already argues, so choose the closest one. Use -1 only when "
            "the claim genuinely relates to none of them."
        )
    )
    confidence: float = Field(ge=0.0, le=1.0, default=0.8)


ClaimStatus = Literal["established", "asserted", "unsupported"]


class ClaimVerdict(BaseModel):
    """Whether the evidence found for a claim actually backs it.

    Three outcomes, not two. A binary established/not test suited empirical
    papers and quietly gutted argumentative ones: a paper whose contribution is
    an analysis of legal accountability states claims it argues rather than
    measures, and calling those unsupported confuses "the paper does not claim
    this" with "the paper claims this without an experiment". Both are worth
    keeping; only the first is worth discarding.
    """

    status: ClaimStatus = Field(
        description=(
            "'established' when the evidence reports a result, measurement or "
            "observation that makes the claim true. "
            "'asserted' when the paper genuinely argues the claim and the "
            "evidence is that argument — an analysis, a position, a discussion "
            "of consequences — but no result demonstrates it. "
            "'unsupported' when the evidence does not back the claim at all: it "
            "states an intention ('we study whether X helps'), describes a "
            "method without an outcome, gives background about other work, or "
            "is merely on the same topic."
        )
    )
    contradicts: bool = Field(
        default=False,
        description="True if the evidence shows the OPPOSITE of the claim.",
    )
    reason: str = Field(default="", description="One sentence.")


class ChunkSubclaims(BaseModel):
    """Pass 2: claims this chunk asserts that are not yet known."""

    new_claims: list[NewClaim] = Field(default_factory=list)


ClaimRelationType = Literal["CONTRADICTS", "SUPPORTS", "REFINES", "UNRELATED"]


class ClaimRelationJudgement(BaseModel):
    """The LLM's verdict on how two claims from different papers relate."""

    relation: ClaimRelationType = Field(
        description=(
            "CONTRADICTS if the claims cannot both be true as stated. "
            "SUPPORTS if they assert compatible findings in the same direction. "
            "REFINES if one narrows, qualifies, or scopes the other. "
            "UNRELATED if they concern different questions."
        )
    )
    rationale: str = Field(description="One sentence justifying the verdict.")
    explanation: str = Field(
        default="",
        description=(
            "For CONTRADICTS, SUPPORTS or REFINES: what specifically differs or "
            "agrees between the two claims and their evidence — the setups "
            "compared, the direction of each finding, and why that puts them in "
            "this relation. Empty for UNRELATED."
        ),
    )
    confidence: float = Field(ge=0.0, le=1.0, default=0.7)


class MainClaim(BaseModel):
    """A claim the paper is actually arguing for — its thesis-level assertions."""

    text: str = Field(description="The claim as one self-contained sentence.")
    claim_type: Literal[
        "finding", "comparison", "limitation", "hypothesis", "method_property",
        "contribution", "future_direction",
    ] = "finding"
    supporting_text: str = Field(description="Verbatim span from the paper.")

    concepts: list[str] = Field(
        default_factory=list, description="Central concepts the claim is about."
    )
    confidence: float = Field(ge=0.0, le=1.0, default=0.8)


class PaperThesis(BaseModel):
    """What the paper argues, read as a whole. The spine everything else hangs on."""

    contribution: str = Field(description="What this paper contributes, one sentence.")
    research_question: str = Field(description="The question it answers, one sentence.")
    main_claims: list[MainClaim] = Field(
        default_factory=list,
        description="5-15 claims the paper argues for, most important first.",
    )


class CommunitySummary(BaseModel):
    title: str = Field(description="Short noun-phrase name for this research theme.")
    summary: str = Field(description="A paragraph describing what unites these concepts.")
    key_themes: list[str] = Field(default_factory=list)
