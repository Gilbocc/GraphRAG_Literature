# Demo corpus — LLMs in the legal domain

Five open-access arXiv preprints on AI & Law with large language models, chosen
to overlap topically (shared models, benchmarks, tasks, and metrics) so that
entity normalization, cross-paper linking, and community detection have
something real to work on. They also disagree in useful ways — see below.

The PDFs themselves are gitignored. Re-fetch them with:

```bash
cd data/papers
curl -sL -o better_call_gpt.pdf              https://arxiv.org/pdf/2401.16212v1
curl -sL -o test_time_scaling_legal.pdf      https://arxiv.org/pdf/2503.16040v2
curl -sL -o legal_evaluations_challenges.pdf https://arxiv.org/pdf/2411.10137v1
curl -sL -o legalbench.pdf                   https://arxiv.org/pdf/2308.11462
curl -sL -o lawbench.pdf                     https://arxiv.org/pdf/2309.16289
curl -sL -o legal_retrieval_benchmark.pdf    https://arxiv.org/pdf/2505.03970v1
```

| File | arXiv | Title |
| --- | --- | --- |
| `better_call_gpt.pdf` | [2401.16212](https://arxiv.org/abs/2401.16212) | Better Call GPT: Comparing Large Language Models Against Lawyers |
| `test_time_scaling_legal.pdf` | [2503.16040](https://arxiv.org/abs/2503.16040) | Evaluating Test-Time Scaling LLMs for Legal Reasoning: OpenAI o1, DeepSeek-R1, and Beyond |
| `legal_evaluations_challenges.pdf` | [2411.10137](https://arxiv.org/abs/2411.10137) | Legal Evaluations and Challenges of Large Language Models |
| `legal_retrieval_benchmark.pdf` | [2505.03970](https://arxiv.org/abs/2505.03970) | A Reasoning-Focused Legal Retrieval Benchmark |
| `legalbench.pdf` | [2308.11462](https://arxiv.org/abs/2308.11462) | LegalBench: A Collaboratively Built Benchmark for Measuring Legal Reasoning in LLMs |
| `lawbench.pdf` | [2309.16289](https://arxiv.org/abs/2309.16289) | LawBench: Benchmarking Legal Knowledge of Large Language Models |

## Why these five

They share a dense vocabulary — GPT-4, o1, DeepSeek-R1, LegalBench, CAIL,
COLIEE, legal judgment prediction, legal retrieval, hallucination — so entities
merge across papers instead of forming five disconnected islands. In a test
ingest, 7 entities appeared in all 5 papers and 10+ in at least 4.

They also hold genuinely opposed positions, which is what the `Claim`-as-node
design exists to represent:

- **Better Call GPT** argues LLMs match or beat human lawyers on contract review
  at a fraction of the cost.
- **Legal Evaluations and Challenges** and **Test-Time Scaling** report that
  LLMs still fall short on substantive legal reasoning.
- **A Reasoning-Focused Legal Retrieval Benchmark** argues existing retrieval
  benchmarks overstate performance because they under-test reasoning.

Good questions to try against this corpus:

```bash
python -m scigraph ask "Do LLMs outperform human lawyers on legal tasks?" --mode hybrid
python -m scigraph ask "Which benchmarks are used to evaluate legal reasoning?" --mode local
python -m scigraph ask "What are the main open challenges in legal AI?" --mode global
```

## Licensing

arXiv preprints, downloaded for research use. Each retains its own licence
(check the arXiv abstract page); several are CC BY. They are not redistributed
in this repository.
