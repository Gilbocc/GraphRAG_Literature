"""Claim-to-claim linking: CONTRADICTS / SUPPORTS / REFINES.

Storing claims as nodes only pays off if the relationships between them are
materialized. Otherwise a question like "do these papers disagree?" depends on
the answering model happening to notice the conflict in retrieved context.

Candidate pairs come from claim-embedding similarity across papers, ranked so
the LLM judges plausible pairs rather than the full cross product.

The threshold is high on purpose. It used to be 0.5, which worked only because
a shared measurement artifact was also required; with that gate gone, 0.5 means
"vaguely on the same topic" and three papers saturated the 200-pair cap. Two
papers that genuinely contradict each other say nearly the same sentence with
the opposite sign, so a high floor costs little and the candidate set stops
growing quadratically with the corpus.

Candidates are deliberately loose: requiring a shared dataset or model produced
zero pairs on this corpus, because five papers on the same topic evaluate
different artifacts. The precision now comes from the judge, which sees each
claim's *backing* — the experiments, datasets and measured values its paper put
behind it — and can therefore tell a real disagreement from two papers measuring
different things. That is the check a shared-artifact filter was standing in for.
"""

from __future__ import annotations

import logging
from concurrent.futures import ThreadPoolExecutor
from datetime import datetime, timezone

from ..config import Config
from ..graph.store import GraphStore
from ..llm.openrouter import StructuredLLM
from ..models import ClaimRelationJudgement

log = logging.getLogger(__name__)

# Shared-entity candidates, ranked by claim-embedding cosine similarity.


# __REL__ comes from a fixed allowlist, never from model output.


ALLOWED = {"CONTRADICTS", "SUPPORTS", "REFINES", "UNRELATED_TO"}

SYSTEM_PROMPT = """\
You compare two claims taken from two different scientific papers and decide how
they relate. Judge only what the two statements assert — do not use outside
knowledge about the field, and do not speculate about experiments you cannot see.

- CONTRADICTS: the claims cannot both be true as stated. A genuine disagreement
  about the same question, not merely different numbers on different setups.
- SUPPORTS: they assert compatible findings pointing the same way.
- REFINES: one narrows, qualifies, or scopes the other (same direction, but with
  an added condition).
- UNRELATED: they concern different questions, even if they share vocabulary.

Two claims mentioning the same method or dataset are very often UNRELATED. Prefer
UNRELATED when the claims are not really addressing the same question, and reserve
CONTRADICTS for real, direct opposition.

Before answering CONTRADICTS, check all four. If any fails, it is not a contradiction:

1. Same referent. Each paper's "our benchmark", "the dataset", "our method" refers
   to its own artifact. A limitation of paper A's benchmark says nothing about
   paper B's benchmark. Use the "about" lists to check whether the two claims
   concern the same artifact; if they name different ones, answer UNRELATED.
2. Same scope. Different tasks, jurisdictions, languages, or model sizes are
   different questions, even under one shared word like "accuracy".
3. Both are findings. A proposal, plan, or research aim ("the study proposes to
   evaluate...") is not a finding and cannot contradict one.
4. Directly opposed, not merely differently emphasised. "X has potential and
   limitations" does not contradict "X improves accuracy" — both can be true.

Sharing an abstract word such as accuracy, precision, performance, or legal
reasoning is not evidence that two claims are about the same thing.

Each claim is shown with the evidence its own paper put behind it — the
experiments, models, datasets, metrics and measured values that back it. Use
that evidence to decide whether the two papers measured the same thing: if their
backings show different benchmarks, tasks or model scales, the claims are not
comparable and the answer is UNRELATED.

Whenever the relation is not UNRELATED, write an `explanation` stating what
specifically differs or agrees: which setups are being compared, what each paper
found, and why that puts them in this relation. Name the artifacts and numbers
from the backings.
"""

USER_TEMPLATE = """\
Shared concepts: {shared}
Shared artifacts (datasets/methods/tasks/metrics): {shared_specific}

Claim A — "{a_paper}" ({a_section}, p.{a_page})
  claim: "{a_text}"
  backed by: {a_backing}

Claim B — "{b_paper}" ({b_section}, p.{b_page})
  claim: "{b_text}"
  backed by: {b_backing}
"""


def link_claims(
    store: GraphStore,
    cfg: Config,
    limit: int = 200,
    min_similarity: float = 0.78,
    min_specific: int = 1,
) -> dict[str, int]:
    """Judge candidate claim pairs and write the resulting relationships."""
    pairs = store.candidate_claim_pairs(limit, min_similarity, min_specific)

    if not pairs:
        log.info("No candidate claim pairs (need embedded claims sharing an entity)")
        return {}

    log.info("Judging %d candidate claim pairs", len(pairs))
    llm = StructuredLLM(cfg)
    counts: dict[str, int] = {}

    def judge(pair: dict) -> ClaimRelationJudgement | None:
        user = USER_TEMPLATE.format(
            shared=", ".join(pair["shared"][:10]) or "(none)",
            shared_specific=", ".join(pair["shared_specific"][:10]) or "(none)",
            a_backing="; ".join(pair["a_backing"]) or "(none)",
            b_backing="; ".join(pair["b_backing"]) or "(none)",
            **{k: pair[k] for k in
               ("a_paper", "a_section", "a_page", "a_text",
                "b_paper", "b_section", "b_page", "b_text")},
        )
        try:
            return llm.parse(SYSTEM_PROMPT, user, ClaimRelationJudgement)
        except Exception as exc:
            log.error("Judgement failed for %s/%s: %s", pair["a_id"], pair["b_id"], exc)
            return None

    with ThreadPoolExecutor(max_workers=max(1, cfg.extract_concurrency)) as pool:
        verdicts = list(pool.map(judge, pairs))

    for pair, verdict in zip(pairs, verdicts):
        if verdict is None:
            continue

        # Persist UNRELATED too, so the same pair is not re-judged on the next run.
        rel = "UNRELATED_TO" if verdict.relation == "UNRELATED" else verdict.relation
        if rel not in ALLOWED:
            continue
        store.write_claim_link(
            rel,
            a_id=pair["a_id"], b_id=pair["b_id"],
            rationale=verdict.rationale, explanation=verdict.explanation,
            confidence=verdict.confidence,
            similarity=pair["similarity"], shared=pair["shared"][:10],
            shared_specific=pair["shared_specific"][:10],
            model=cfg.llm_model,
            judged_at=datetime.now(timezone.utc).isoformat(),
        )
        counts[rel] = counts.get(rel, 0) + 1

    log.info("Wrote claim relations: %s", counts)
    return counts


def list_disagreements(store: GraphStore) -> list[dict]:
    return store.disagreements()
