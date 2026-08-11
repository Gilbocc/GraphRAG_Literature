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
(Claim)-[:IN_COMMUNITY]->(Community)
(Claim)-[:CONTRADICTS|SUPPORTS|REFINES|UNRELATED_TO {explanation}]->(Claim)

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
   5. datasets    one call → what each dataset contains
                          │
   embed → cross-paper claim graph → communities → OpenAlex → claim links
```

Pass 2 is sequential so each chunk sees the claims found before it — that is
what removes the need for a dedup step. Pass 3 is parallel because the claim
set is fixed by then, which also means every chunk is judged against every
claim rather than only those discovered so far.

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
| `global` | community summaries only |
| `hybrid` | community summaries, plus each theme's claims **and the verbatim passage behind each** |

**Use `hybrid`.** On a corpus of six papers it beat plain RAG on cross-paper
synthesis, and won outright where the answer existed but was not lexically
close to the question:

> *"How should legal LLM outputs be evaluated, and what is wrong with current
> metrics?"*
>
> plain: *"cannot be answered from the supplied text"*
> local: *"the context does not contain information"*
> hybrid: found LawBench's Limitations, p.16 — *"we only use Rouge-L … which
> cannot fully reflect the human judgement about the answer quality"*

`plain` still wins when an answer sits in one paper and is lexically obvious.
`global` cites community summaries, which have no page, so its citations cannot
be verified — prefer `hybrid`.

### What the comparisons showed

Every mode answering the same questions, same chunks, same model — only
retrieval differs. Runs are in [`data/comparisons/`](data/comparisons/),
newest last:

| run | corpus | file |
|---|---|---|
| first | 3 papers | [`three_papers.md`](data/comparisons/three_papers.md) |
| after two more | 5 papers | [`five_papers.md`](data/comparisons/five_papers.md) |
| after LegalBench | 6 papers | [`six_papers.md`](data/comparisons/six_papers.md) |
| after the citation fix | 6 papers, new questions | [`six_papers_v2.md`](data/comparisons/six_papers_v2.md) |

What they show:

- **`hybrid` wins wherever the answer is not lexically close to the question.**
  Asked how legal LLM outputs should be evaluated, `plain` answered *"cannot be
  answered from the supplied text"* and `local` *"the context does not contain
  information"*; `hybrid` found LawBench's Limitations, p.16. The sentence was
  in the corpus all along — chunk similarity could not reach it, because the
  passage argues the point without using the question's words.
- **`hybrid` synthesises across papers; `plain` rarely leaves one.** On "which
  model families recur and what is claimed about each", `hybrid` produced a
  comparison table over eight families from three papers, each row cited to a
  section and page. `plain` answered from one paper.
- **`plain` still wins when the answer is in one paper and obvious.** Asked
  whether fine-tuning is worthwhile, it quoted four LawBench passages including
  an analysis section the graph modes missed.
- **Neither found a contradiction, and that is probably right.** Six papers
  sharing no benchmarks or models do not disagree; `link-claims` independently
  judged every candidate pair `UNRELATED`. Only `hybrid` demonstrated it by
  examining the candidates rather than failing to retrieve any.
- **`global` is not usable.** It answers from summaries alone, so its citations
  have no page and cannot be checked; on one question it also reached the
  opposite conclusion to `hybrid` by silently narrowing the question.

Two bugs the comparisons caught, both since fixed: `hybrid` quoting our
paraphrased claim text as if it were the paper's words, and — after datasets
were added to the context — citing a community title as a source. Both produced
citations that look checkable and are not, which is the one failure this design
exists to prevent.

Context distinguishes what may be quoted from what may not: claims are labelled
`CLAIM (our paraphrase, do not quote)` and spans `VERBATIM PASSAGE (quotable)`.
Without that split, answers quoted our paraphrase and attributed it to a page —
a citation that looks checkable and is not.

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
python -m scigraph communities               # summaries are embedded here too
python -m scigraph link-claims

python -m scigraph compare "q1" "q2" --out data/comparisons/run.md
python -m scigraph export-parsed data/papers # inspect the parse, no Neo4j needed
python -m scigraph stats
```

## Configuration

| variable | default | note |
|---|---|---|
| `OPENROUTER_LLM_MODEL` | `openai/gpt-oss-120b` | see the model note |
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

Per paper, on the six-paper corpus:

```
legalbench (40 chunks): subclaims=216s evidence=22s verify=27s datasets=89s
                        155 LLM calls, 556s in the model
smaller papers:         ~75s end to end, ~85 LLM calls
```

Plus one-off docling conversion, minutes per paper, cached by PDF content hash.
The sequential sub-claim pass is the dominant cost and grows with chunk count.

## Status

Working: parsing, five extraction passes, verification, cross-paper communities,
OpenAlex enrichment, four query modes, citation suggestions.

Known gaps, roughly by how much they matter:

- **`link-claims` finds no contradictions**, and that is probably correct — six
  papers sharing no benchmarks or models do not contradict each other. Untested
  on a corpus that genuinely overlaps.
- **Communities need a bigger, more varied corpus.** At six homogeneous papers
  there are two or three real cross-paper themes; forcing more produces blobs.
  The similarity floor is 0.80 for that reason.
- **Run-to-run variance is large** — the same paper gave 23 and 54 claims on
  different runs. Pass 2 being sequential compounds an early divergence.
- **Support propagation is undiscriminating** — a parent inherits every child's
  evidence whether or not the child concerns the same proposition.
- **`global` mode citations are unverifiable** (no page).
- **No tests.** They were deleted during the schema rework and should return —
  docling and GROBID behaviour is load-bearing and unpinned.

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

Three node types, all with `openai/text-embedding-3-small`, 1536 dims, 128
texts per request. Embedding is incremental (`WHERE n.embedding IS NULL`), so
re-running `embed` only touches new nodes.

| node | text embedded | what it powers |
|---|---|---|
| `Chunk` | the raw passage, up to ~4000 chars — a table chunk is the whole table | `plain` and `local` retrieval |
| `Claim` | the claim sentence alone — no evidence, no paper title | the cross-paper kNN graph, and claim pairing for contradiction judging |
| `Community` | `title + ". " + summary` — the generated summary, not its member claims | `global` and `hybrid` retrieval |

**Not embedded:** `Evidence` spans, `Dataset` descriptions, `Paper` metadata.

Two of those omissions shape retrieval:

- A question never matches an evidence span directly. `hybrid` reaches a passage
  only by matching its community summary first, then walking summary → claim →
  span. Two hops of indirection, which is why `hybrid` depends so much on
  summary quality.
- Dataset descriptions are reachable only through a paper that has already been
  retrieved, so a question purely about data ("which benchmarks use Chinese
  criminal cases?") has no direct route to them.

Both are cheap to change — embed the node, add a vector index — and both are
open rather than decided.

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
corpus every claim is about the same subject: at 0.6 the graph connects
near-arbitrary pairs and Leiden splits a structureless graph into equal blobs
that look like communities and are not.

**Detecting communities** — **Leiden** (Neo4j GDS) over that graph, undirected
and weighted by similarity, `gamma=0.6`, keeping communities of `≥4` claims.
Set `COMMUNITY_ALGORITHM=louvain` to switch. Weighted Leiden falls back to
unweighted on the `dendrogramManager` NPE that GDS raises on degenerate graphs.
Detection deletes the previous generation first — without that, re-running
stacked three generations of the same clusters and answers cited one theme
three times as if it were three sources.

**Pairing claims to judge for contradiction** — cross-paper cosine `≥0.78`,
at most `200` pairs. Measured on this corpus: 0.70 gives 500+ candidates
(the cap), 0.78 gives 38, 0.85 gives 1.

**Retrieval** — Neo4j vector search, `top_k=5`, over chunks (`local`, `plain`)
or community summaries (`global`, `hybrid`).

**Concurrency** — `EXTRACT_CONCURRENCY=8` threads for the evidence, verify and
summary passes. The sub-claim pass is deliberately sequential so each chunk
sees the claims found before it; it is the slowest pass as a result
(216s of LegalBench's 354s).

### Libraries

`docling` 2.118 · `neo4j` 6.2 · `neo4j-graphrag` 1.18 · `graphdatascience` 1.22 ·
`openai` 2.53 · `pydantic` 2.13 · `rapidfuzz` 3.14 · `unidecode` 1.4 ·
`pypdf` 6.14 · `httpx` 0.28

`rapidfuzz` aligns spans, `unidecode` folds names, `pypdf` cuts the body. No
entity-resolution library — that layer was removed.

## Demo corpus

Six open-access AI-and-law papers; see `data/papers/SOURCES.md`. PDFs are not
committed. Comparison runs are saved under `data/comparisons/`.
