# scigraph

A Neo4j knowledge graph of what scientific papers **claim**, and the passages
that back those claims — built to answer questions across a corpus with
citations a reader can actually check.

Evidence is a character range of the paper's own text, located by anchors and
sliced out of the chunk, so a stored quotation is verbatim by construction
rather than by later verification. Nothing enters the graph that is not
evidence for a claim some paper makes.

## Graph model

```text
(Paper)-[:HAS_SECTION]->(Section)-[:HAS_CHUNK]->(Chunk)
(Paper)-[:MAKES_CLAIM]->(Claim)
(Claim)-[:ELABORATES]->(Claim)                    // sub-claim to what it refines
(Claim)-[:SUPPORTED_BY]->(Evidence)-[:EXTRACTED_FROM]->(Chunk)
(Paper)-[:USES_DATASET {introduced_here}]->(Dataset)
(Claim)-[:RELATED_CLAIM {weight}]->(Claim)        // cross-paper kNN, drives communities
(Claim)-[:IN_COMMUNITY]->(Community)          // hierarchical: Community.level

(Paper)-[:CITES {resolved_by}]->(Paper)           // cited works become stub Papers
(Paper)-[:AUTHORED_BY {position}]->(Author)       // from OpenAlex
(Paper)-[:PUBLISHED_IN]->(Venue)
```

| node | what it holds |
|---|---|
| `Claim` | text, `claim_type`, `is_main`, `status`, `contradicted`, `verdict_reason` |
| `Evidence` | `text` (the span), `char_start`, `char_end`, page, section, chunk |
| `Dataset` | name, description, size, language, domain, source, supporting_text |
| `Community` | title, summary, key_themes over a set of cross-paper claims |

`Claim.status` is three-way:

- `established` — a passage reports a result that makes the claim true
- `asserted` — the paper argues it; nothing measures it
- `unsupported` — the evidence is an intention, a method description, or background

A binary test suited empirical papers and gutted argumentative ones, discarding
a paper's entire discussion of liability and accountability as "unsupported"
when the paper plainly argues it.

## Pipeline

```
PDF ─┬─ GROBID   → references, DOI/arXiv id, title      (full PDF)
     └─ docling  → body text, sections, tables          (cut at the bibliography)
                          │
   1. thesis      abstract + intro + conclusion → the paper's main claims
   2. sub-claims  body chunks IN ORDER → claims the abstract never states,
                  each attached to the claim it elaborates        [sequential]
   3. evidence    every chunk × the complete claim set → span anchors  [parallel]
   4. verify      each claim vs its own spans and its children's       [parallel]
   5. datasets    data-bearing sections IN ORDER → what each dataset
                  contains, each section enriching what is known  [sequential]
                          │
   embed → communities (claim graph → Leiden levels → summaries) → OpenAlex
```

Pass 2 is sequential so each chunk sees the claims found before it — that is
what removes the need for a dedup step. Pass 3 is parallel because the claim
set is fixed by then, which also means every chunk is judged against every
claim rather than only those discovered so far.

Pass 5 is sequential for the same reason. It used to send the whole paper in
one call, which made it both the largest request in the pipeline and the one
that hung; now each data-bearing section sees the datasets already found, and
either adds a new one or returns a fuller record for one already there. A paper
names the same dataset several ways — "CUAD", "the Contract Understanding
Atticus Dataset", "our dataset" — so the model reconciles them while it can see
both, rather than leaving one dataset as three nodes holding a third of the
account each.

The cross-paper claim graph is built during `communities`, not at the end of
ingest: it is a kNN over claim embeddings, and nothing is embedded until `embed`
runs. Built at the end of ingest it silently skipped every claim that run had
just created.

Appendices and related work are excluded everywhere. Appendices are found
positionally — the first lettered heading after the last numbered section —
because `A Bar Exam QA Dataset Construction` and a paper's own title
`A Reasoning-Focused Legal Retrieval Benchmark` are identical in shape.

The PDF is also **truncated at the bibliography before docling runs**, since
conversion is the slowest step and nothing downstream reads past it:

```
legalbench   19 of 143 pages     test_time_scaling   8 of 23 pages
lawbench     16 of  38 pages     better_call_gpt    11 of 16 pages
```

GROBID still receives the whole file — the references it parses live in exactly
the part that gets cut.

## Why two parsers

GROBID reads bibliography and header metadata well and a paper's body badly.
Measured by numeric recall — what fraction of the numbers printed in the PDF
survive parsing:

| paper | GROBID | docling |
|---|---|---|
| llm_legal_ai_survey | 10.6% | 98.0% |
| better_call_gpt | 27.2% | 97.3% |
| legal_evaluations_challenges | 61.6% | 98.9% |
| test_time_scaling_legal | 69.7% | 87.8% |
| legal_retrieval_benchmark | 71.7% | 91.1% |

GROBID dropped up to 89% of a paper's numbers: appendix pages never entered its
`<div>` tree, and table bodies came back empty — one paper's headline F-score
table arrived as a single cell reading `and Palm2`. Neither raised an error.

## Query modes

```bash
python -m scigraph ask "how does query expansion affect legal retrieval?"
python -m scigraph ask --mode hybrid "what are the open problems in legal AI?"
python -m scigraph ask --plain "..."      # baseline: nearest chunks, no graph
```

| mode | context |
|---|---|
| `plain` | nearest chunks only — the control |
| `local` | nearest chunks, plus the claims each grounds and the paper's datasets |
| `global` | **broad** community themes, with the passage behind each claim |
| `hybrid` | **fine** community themes with their passages, **plus** the nearest chunks |
| `evidence` | the verbatim spans nearest the question, at most two per paper |

Communities are hierarchical, and each mode reads the level it is for: `global`
takes the broadest level for corpus-wide questions, `hybrid` the finest, since
it gets breadth from chunks instead. Both cite the passage, not the summary.

**No mode wins everything.** Measured by reading answers on a ten-paper corpus:

| question type | best mode | why |
|---|---|---|
| cross-paper disagreement | `hybrid` | only mode that connected CUAD's scaling result to LawBench's |
| corpus-wide breadth | `global` | broadest coverage, 30 page-citations on one question |
| "what methods exist" | `local` | reads passages closely; separated annotation from prediction where hybrid merged them |
| single-paper factual | `plain` | its whole context is passages |

`evidence` is the newest and narrowest: five spans is 2-3 KB of context against
`plain`'s 20 KB, so every line it gets is a verified quotable span and there are
too few of them to answer a broad question. It was the thinnest mode on four of
five questions. `top_k` means something different for spans than for chunks and
has not been retuned.

`hybrid` is the default worth reaching for, because synthesis across papers is
what the graph is for, but it spends about 70% of its context on themes and 30%
on passages — which is the right trade for connecting claims and the wrong one
for reading two passages closely.

### What the comparisons showed

Every mode answering the same questions, same chunks, same model — only
retrieval differs. Runs are in [`data/comparisons/`](data/comparisons/),
newest last:

| run | corpus | file |
|---|---|---|
| first | 3 papers | [`three_papers.md`](data/comparisons/three_papers.md) |
| after two more | 5 papers | [`five_papers.md`](data/comparisons/five_papers.md) |
| after LegalBench | 6 papers | [`six_papers.md`](data/comparisons/six_papers.md) |
| after the citation fix | 6 papers | [`six_papers_v2.md`](data/comparisons/six_papers_v2.md) |
| four more papers, wider topics | 10 papers | [`ten_papers.md`](data/comparisons/ten_papers.md) |
| after the record-formatting fix | 10 papers | [`ten_papers_v2.md`](data/comparisons/ten_papers_v2.md) |
| after hierarchical levels | 10 papers | [`ten_papers_v3_levels.md`](data/comparisons/ten_papers_v3_levels.md) |

What they show:

- **The graph earns its cost on disagreement, and only once it could see one.**
  Asked whether bigger models reliably do better on legal tasks, `hybrid` set
  CUAD's *"a 20-fold increase in parameters for ALBERT yields only about a 3%
  improvement in AUPR"* (Table 2, p.6) against LawBench's *"scaling up the model
  size results in better performance in one-shot case"* (§4.4, p.13), and
  resolved it — architecture changes help where parameter count alone does not.
  Every other mode answered "usually helps, not always" from LawBench and
  LEGALBENCH alone. The same question failed in all four modes two runs earlier;
  what changed was retrieval, not the corpus.
- **`hybrid` reaches papers the claim graph barely connects.** CUAD and
  MultiEURLEX link weakly to the rest, so community membership alone would miss
  them; the chunk half retrieves them anyway, with page-level citations.
- **`plain` still wins when the answer is in one paper.** On how cross-lingual
  legal NLP differs from English-only — essentially a MultiEURLEX question — it
  gave the most detailed answer of any mode.
- **`local` reads passages more closely than `hybrid`.** Asked what methods
  extract structure from contracts, it distinguished human span annotation from
  model span prediction and gave the matching metric (Jaccard ≥ 0.5); `hybrid`
  merged the two.
- **Disagreement is rare and mostly absent.** Six near-identical benchmark
  papers produced none. Broadening the corpus to contract extraction, judgment
  prediction, multilingual transfer and data curation produced the scaling
  disagreement above — the graph finds what is there, and homogeneous corpora
  have little to find.

Four bugs these runs caught, all since fixed, all of which produced answers that
looked citable and were not: `hybrid` quoting our paraphrase as the paper's
words; citing a community title as a source; `GLOBAL_QUERY` matching a
relationship that no longer existed, so global answered from titles alone or
refused; and the retriever handing the model `str(record)` — a Python repr with
every newline escaped — which broke the line structure binding each quotation to
its citation.

## Choosing what to read next

```bash
python -m scigraph suggest
```

Ranks works the corpus cites but does not contain, by how many of your papers
independently cite them. No extraction, no LLM — only the reference lists
already parsed:

```
[3 papers cite it]  (2024)  LegalBench: A collaboratively built benchmark...
      cited by: A Reasoning-Focused Legal Retrieval, Evaluating Test-Time Scaling, Legal Evaluations
[2 papers cite it]  (2023)  ChatLaw: Open-source legal LLM...   2306.16092
```

LegalBench was chosen this way, and turned out to be the most densely connected
paper in the corpus — 82 claims and 109 of the 266 cross-paper edges.

## Setup

```bash
docker run -d --name neo4j -p 7474:7474 -p 7687:7687 \
  -e NEO4J_AUTH=neo4j/yourpassword \
  -e NEO4J_PLUGINS='["graph-data-science"]' neo4j:5.26
docker run -d --name grobid -p 8070:8070 lfoppiano/grobid:0.8.0

python -m venv .venv && .venv/bin/pip install -r requirements.txt
cp .env.example .env      # set OPENROUTER_API_KEY and NEO4J_PASSWORD
```

## Usage

```bash
python -m scigraph pipeline data/papers      # everything

# adding one paper to an existing graph — only it hits the LLM
python -m scigraph ingest /path/to/one-paper/
python -m scigraph embed
python -m scigraph communities               # claim graph, levels, summaries, embeddings

# an interrupted ingest leaves a half-extracted paper; re-running does not
# repair it, because claim ids hash the claim text and a re-worded claim lands
# beside the old one. Clear it first.
python -m scigraph forget arxiv:2103.06268
python -m scigraph ingest /path/to/one-paper/

python -m scigraph embed --redo Claim        # after changing what a label embeds
python -m scigraph compare "q1" "q2" --out data/comparisons/run.md
python -m scigraph export-parsed data/papers # inspect the parse, no Neo4j needed
python -m scigraph stats
```

Every command also appends to `data/logs/scigraph.log`, timestamped and flushed
per line, so a long run can be watched from another shell with `tail -f`. That
exists because piping the console output through anything that buffers hides it
completely: an ingest once ran thirty minutes emitting progress into a pipe that
held every line until the process exited, which is indistinguishable from a
hang.

## Configuration

| variable | default | note |
|---|---|---|
| `OPENROUTER_LLM_MODEL` | `openai/gpt-oss-120b` | extraction; see the model note |
| `QUERY_LLM_MODEL` | *(extraction model)* | answering only — a stronger model here does not change ingest cost |
| `QUERY_PROVIDER_ORDER` | *(extraction pin)* | **blank this if the query model is not groq-served** |
| `QUERY_REASONING_EFFORT` / `QUERY_TEMPERATURE` | *(extraction)* / `0.0` | temperature 0 keeps citations reproducible |
| `OPENROUTER_PROVIDER_ORDER` | `groq` | serves gpt-oss only — blank it for other models |
| `LLM_TIMEOUT` | `120` | seconds; **without this a stalled call blocks forever** |
| `LLM_MAX_TOKENS` | `32000` | a truncated response is discarded whole |
| `EXTRACT_CONCURRENCY` | `8` | passes 3–5 are parallel; pass 2 is not |
| `CHUNK_SIZE` / `CHUNK_OVERLAP` | `4000` / `400` | at 1200, claims split across boundaries |
| `DOCLING_TABLES` | `1` | `0` falls back to GROBID's much worse tables |
| `COMMUNITY_RESOLUTION` | `0.6` | Leiden gamma |

### Model note

Developed against `openai/gpt-oss-120b` (cheap). A run on
`deepseek/deepseek-chat-v3.1` with no code changes gave, on the same paper:

| | gpt-oss-120b | deepseek-v3.1 |
|---|---|---|
| evidence spans | 40 | 54 |
| anchors that failed to locate | 5 | 0 |
| main claims with evidence | 3 of 6 | 10 of 10 |
| spans not verbatim | 0 | 0 |

The gains land where model capability should matter — anchor fidelity and
coverage — and the structural guarantees hold either way.

## Cost

Per paper, measured on the ten-paper corpus:

```
legalbench (40 chunks): subclaims=216s evidence=22s verify=27s datasets=89s
                        155 LLM calls, 556s in the model
multieurlex (21 chunks): subclaims=24s evidence=85s verify=13s datasets=7s
                        77 LLM calls
smaller papers:         ~40-90s end to end, ~50-90 LLM calls
```

Plus one-off docling conversion — **the dominant wall-clock cost**, minutes per
paper on CPU and cached by PDF content hash. Four uncached papers took 30
minutes to convert and under 4 minutes to extract.

Re-running `communities` on an unchanged graph is free: summaries survive when
membership does.

## Status

Working: parsing, five extraction passes, verification, hierarchical
cross-paper communities, OpenAlex enrichment, four query modes, citation
suggestions. Ten papers, 361 claims, 399 evidence spans, 23 communities across
two levels.

Known gaps, roughly by how much they matter:

- **A third of claims reach no community** — 114 of 361, because they link to
  nothing above the 0.80 floor. Lowering it destroys the communities instead, so
  `hybrid` covers those papers through chunks rather than themes.
- **Nothing judges claims against each other any more.** An LLM pass used to
  label cross-paper pairs `CONTRADICTS` / `SUPPORTS` / `REFINES`; it called
  every candidate `UNRELATED` across three corpus sizes and was deleted. The one
  real disagreement here — CUAD against LawBench on whether scale helps — sits
  at cosine 0.799, under the pairing floor, and `hybrid` surfaced it from
  retrieval instead. Contradiction is currently something a reader notices in an
  answer, not something the graph records.
- **Run-to-run variance is large** — the same paper gave 23 and 54 claims on
  different runs. Pass 2 being sequential compounds an early divergence.
  Community *detection* is now seeded and reproducible; extraction is not.
- **Support propagation is undiscriminating** — a parent inherits every child's
  evidence whether or not the child concerns the same proposition.
- **Rate limits are invisible.** The OpenAI client retries 429s internally with
  backoff and logs nothing, so a throttled call looks like a hang: summaries ran
  at 5s each until the quota went, then 101s each.
- **No tests.** They were deleted during the schema rework and should return —
  docling and GROBID behaviour is load-bearing and unpinned, and four of the
  bugs found this week were schema drift that a single query-parse test would
  have caught.

## Stack and parameters

### Services

| | version | role | settings |
|---|---|---|---|
| **Neo4j** | 5.26 + GDS 2.13 | graph store, Leiden, vector search | 1536-dim cosine indexes on `Chunk`, `Claim`, `Community` |
| **GROBID** | 0.8.0 (Docker) | references, DOI/arXiv id, title | `segmentSentences=1`, `teiCoordinates=s,head,figure`, `consolidateHeader=0`, `consolidateCitations=0` — gets the **whole** PDF |
| **OpenAlex** | public API | year, venue, authors, citations | polite pool via `mailto`, 0.2s between calls, 50 ids per batch |

`teiCoordinates` must include `figure`, or every table is reported as page 1.

### Models

| | model | settings |
|---|---|---|
| extraction + answering | `openai/gpt-oss-120b` via OpenRouter | `temperature=0`, `max_tokens=32000`, `reasoning.effort=low`, provider pinned to `groq`, **`timeout=120s`, `max_retries=2`** |
| embeddings | `openai/text-embedding-3-small` | 1536 dims, 128 texts per request |
| layout + tables | docling 2.118 (RT-DETR layout, TableFormer) | CPU, 1–10 min/paper, cached by PDF content hash |

The timeout is not optional: without it a stalled request blocks forever with no
error and no log line. One paper hung fifteen minutes twice before this existed,
and every apparent "slowness" turned out to be that.

Structured output tries native `json_schema`, then falls back to `json_object`
with an embedded schema — not every OpenRouter-routed model supports the former.

### What gets embedded

All with `openai/text-embedding-3-small`, 1536 dims, 128 texts per request.
Embedding is incremental (`WHERE n.embedding IS NULL`), so re-running `embed`
only touches new nodes; `embed --redo Claim` drops a label's vectors first, for
when the embedded *text* changed and the incremental filter would skip them.

| node | text embedded | what it powers |
|---|---|---|
| `Chunk` | the raw passage, up to ~4000 chars — a table chunk is the whole table | `plain` and `local` retrieval |
| `Claim` | the claim sentence, bare | the cross-paper kNN graph, and claim pairing for contradiction judging |
| `Community` | `title + ". " + summary` — the generated summary, not its member claims | `global` and `hybrid` retrieval |
| `Evidence` | the verbatim span | nothing yet — see below |

**A claim is embedded bare, and the alternative was tried.** A claim sentence
alone is ambiguous about what it is a claim *about* — "performance degrades
sharply on longer inputs" names neither task nor model — so the paper title and
section were prefixed to it. That made the kNN worse. The prefix is
near-constant within a paper and long relative to one sentence, so it dominated
the score: four unrelated LEGALBENCH claims came back paired to the same
LawBench claim at an identical 0.905. Bare text pairs things that are actually
about one thing — both benchmarks excluding long-document tasks over context
limits, two papers independently finding fine-tuning helps but does not close
the gap to GPT-4. Context that discriminates *between* the claims in a paper
would help; metadata shared by all of them does not.

**Evidence is embedded, but no query uses it.** `hybrid` reaches a passage only
through a community summary and then a claim, and both hops are lossy — a
summary that does not happen to mention what a passage says makes that passage
unreachable however well it answers the question. Searching the evidence index
directly and unioning the two was tried, and it cut both ways: on a question the
theme route had failed entirely it found four papers' worth of answer, but on
questions the theme route already handled it *lost* papers. Similarity alone
gave every direct slot to whichever paper wrote most densely on the topic — all
five to LEGALBENCH on "which model families recur" — and those hits pushed the
themes' cross-paper claims out of the context, costing the answer LawBench on
Chinese legal-specific models and DeepSeek-R1 on test-time scaling. The union
needs per-paper diversity before it is worth having; the vectors are kept so
that work does not have to start by paying for embeddings again.

**Not embedded:** `Dataset` descriptions and `Paper` metadata. A dataset is
reachable only through a paper already retrieved, so a question purely about
data ("which benchmarks use Chinese criminal cases?") has no direct route to
one. With ~60 dataset nodes the ceiling is low, so this is left open.

### Algorithms and thresholds

**Chunking** — sentences grouped into `4000`-char chunks with `400` overlap.
At 1200 chars, 22% of chunks yielded nothing and claims were split across
boundaries. A table is never split, so table chunks can exceed the target.

**Cutting the PDF before conversion** — everything from the first standalone
`References`/`Bibliography` page onward is dropped before docling runs. docling
is the slowest step and nothing downstream reads past that point: LegalBench
converts 19 pages instead of 143. GROBID still gets the whole file.

**Cutting appendices before extraction** — the appendix starts at the first
lettered heading (`A Bar Exam QA Dataset Construction`) that appears *after the
last numbered section*. Position is needed because shape alone cannot tell that
heading apart from a paper's own title, `A Reasoning-Focused Legal Retrieval
Benchmark` — a pattern loose enough to catch one ate the other and 59 sections
with it.

**Locating an evidence span** — the model returns a first and last few words;
we find them in the chunk and slice out the range. Exact match first, then
`rapidfuzz.ratio ≥ 82` for anchors that differ by a ligature or a dash. An
anchor shorter than `8` chars is rejected as too generic to place. A span that
cannot be located is dropped rather than stored unverified.

**Linking claims into a graph** — each claim connects to its `k=6` nearest
neighbours by embedding cosine, **only across papers**, and only above `0.80`.
Two claims in the same paper are already related by the paper, so within-paper
edges would just restate its structure. The floor is high because in a topical
corpus every claim is about the same subject; 0.75 was tried and reverted, as it
doubled the edges to 662 and left Leiden returning two 70-claim "communities"
drawn from nine of the ten papers.

The edge weight is the similarity **rescaled onto the surviving range**,
`(score - 0.80) / 0.20`, not the raw cosine. Every edge is above the threshold
by construction, so raw weights span 0.80–1.00 — near-uniform to modularity,
which is the same as having no weights at all. Rescaled they span 0–1 and a 0.98
pair outweighs a 0.81 pair about nine to one.

Claims that link to nothing stay unlinked: 114 of 361 here, including a third of
MultiEURLEX's. No threshold fixes that without destroying the communities, which
is why `hybrid` retrieves chunks as well as themes.

**Detecting communities** — **Leiden** (Neo4j GDS) over that graph, undirected,
weighted, `gamma=0.6`, `randomSeed=42`, `concurrency=1`, keeping communities of
`≥4` claims. Set `COMMUNITY_ALGORITHM=louvain` to switch. Weighted Leiden falls
back to unweighted on the `dendrogramManager` NPE that GDS raises on degenerate
graphs.

*Seeded and single-threaded* because GDS only guarantees a reproducible
partition at concurrency 1. Unseeded, two runs over the identical 281 edges kept
126 and 247 claims — the ones that changed hands fell either side of the
four-member minimum. That swing was larger than any effect being measured, which
made every before/after comparison meaningless.

*Hierarchical.* Leiden merges bottom-up and only its final level used to be
read — on ten papers that was one 89-claim community spanning nine of them.
Every level is now kept except the fragmentary bottom and the degenerate top,
giving 16 fine themes and 7 broad ones here. This is why `gamma` matters much
less than it did: coarse views come from the levels above, not from tuning one
number, and Leiden adds levels by itself as the corpus grows.

*Idempotent.* Each community stores a fingerprint of its exact claim set. Same
fingerprint on a re-run, the summary and its embedding survive; different, they
are regenerated. Detection used to delete everything first, so every run cost a
full re-summarisation and an interrupted one left the graph worse than it found
it.

**Pairing claims to judge for contradiction** — cross-paper cosine `≥0.78`,
at most `200` pairs. Measured on this corpus: 0.70 gives 500+ candidates
(the cap), 0.78 gives 38, 0.85 gives 1.

**Retrieval** — Neo4j vector search, `top_k=5`, over chunks (`plain`, `local`,
and the second half of `hybrid`) or community summaries (`global`, `hybrid`).
The two hierarchy levels share one index, so the graph modes over-fetch `4x`
and filter to their level, then trim back to `top_k` — the client library
applies its own `LIMIT` before the retrieval query runs.

**Concurrency** — `EXTRACT_CONCURRENCY=8` threads for the evidence, verify and
summary passes. The sub-claim and dataset passes are deliberately sequential so
each step sees what was found before it.

**Token budgets** — `LLM_MAX_TOKENS=32000` for extraction, where a truncated
structured reply is discarded whole, but short replies ask for less: community
summaries request `2000`. The budget is *reserved*, not billed by use — the same
summary-sized call took 8.9s at 32000 and 0.2s at 800.

**Timeouts** — `LLM_TIMEOUT=120` is passed to the client, but that is a
per-socket-operation timeout: a server that trickles bytes resets it forever.
One dataset call sat blocked for sixteen minutes with no error and no retry. So
every structured call also runs under a wall-clock deadline of `3x` that,
enforced from outside the client.

### Libraries

`docling` 2.118 · `neo4j` 6.2 · `neo4j-graphrag` 1.18 · `graphdatascience` 1.22 ·
`openai` 2.53 · `pydantic` 2.13 · `rapidfuzz` 3.14 · `unidecode` 1.4 ·
`pypdf` 6.14 · `httpx` 0.28

`rapidfuzz` aligns spans, `unidecode` folds names, `pypdf` cuts the body. No
entity-resolution library — that layer was removed.

## Demo corpus

Ten open-access AI-and-law papers; see `data/papers/SOURCES.md`. PDFs are not
committed. Comparison runs are saved under `data/comparisons/`.

The first six all evaluate LLMs on legal benchmarks, and that homogeneity was
itself a finding: nothing contradicted anything, and communities had little to
separate. The next four were chosen for spread rather than closeness — contract
clause extraction (CUAD), judgment prediction on ECHR cases, multilingual
zero-shot transfer over EU law (MultiEURLEX), and dataset curation and
responsible filtering (Pile of Law). Three of them predate or sidestep the LLM
framing entirely, and that is where the first real disagreement came from.
