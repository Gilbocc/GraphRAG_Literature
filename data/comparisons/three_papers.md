# Retrieval comparison — 2026-08-11 16:53

Model `openai/gpt-oss-120b`, embeddings `openai/text-embedding-3-small`, top_k=5.

- **plain** — nearest chunks only, no graph. The control.
- **local** — nearest chunks, plus the claims each one grounds.
- **global** — community summaries only.
- **hybrid** — community summaries, plus each theme's claims and the verbatim passage behind them.


---

## Q1. Do the papers agree on whether fine-tuning LLMs on legal text is worthwhile?

### plain

**Answer**

Yes. All of the passages agree that fine‑tuning large language models on legal‑specific text yields measurable improvements, even though the resulting models are still far behind the best general‑purpose LLMs (e.g., GPT‑4). The papers consistently describe fine‑tuning as beneficial but not sufficient to make the models fully reliable for legal tasks.

**Sources**

- **LawBench: Benchmarking Legal Knowledge of Large Language Models**, *Abstract*, p. 1 – “While fine‑tuning LLMs on legal specific text brings certain improvements, we are still a long way from obtaining usable and reliable LLMs in legal tasks.”  
- **LawBench: Benchmarking Legal Knowledge of Large Language Models**, *1 Introduction*, p. 1‑3 – “We find that although legal specific fine‑tuning usually improves upon their base model, they are still significantly lagging behind general LLMs… Important suggestions are summarized to better guide the future development of legal LLMs.”  
- **LawBench: Benchmarking Legal Knowledge of Large Language Models**, *5 Conclusion*, p. 15‑16 – “While fine‑tuning open‑source LLMs on legal specific language results in some advances, they still lag far below GPT‑4… Legal specific fine‑tuning significantly improves the performance and reduces the abstention rate.”  
- **LawBench: Benchmarking Legal Knowledge of Large Language Models**, *4 Experiment > 4.4 Analysis*, p. 13‑15 – “In most cases, models perform better through SFT… The LLaMA‑2 series further applies RLHF on top of SFT… Legal specific fine‑tuning is helpful… after legal specific fine‑tuning, there is a consistent enhancement of model scores and reduction of abstention rates.”

### local

Both papers agree that fine‑tuning large language models on legal‑specific text does bring measurable benefits, but the gains are modest and the models still fall far short of the performance of the strongest general‑purpose LLMs (e.g., GPT‑4). The authors note that legal‑specific fine‑tuning “significantly improves the performance and reduces the abstention rate” and yields “certain improvements,” yet even after such fine‑tuning “they are still significantly lagging behind GPT‑4 and are not yet reliable for practical legal tasks.” Thus, while fine‑tuning is considered worthwhile for improving legal task scores, it does not close the large gap to top‑tier models.

**Sources**

- *LawBench: Benchmarking Legal Knowledge of Large Language Models*, Abstract, p.1 – “Fine‑tuning open‑source LLMs on legal‑specific text yields modest improvements but they still lag far behind GPT‑4 and are not yet reliable for practical legal tasks.”  
- *LawBench: Benchmarking Legal Knowledge of Large Language Models*, 5 Conclusion, p.15‑16 – “Legal‑specific fine‑tuning significantly improves the performance and reduces the abstention rate… While fine‑tuning open‑source LLMs on legal specific language results in some advances, they still lag far below GPT‑4.”

### global

The papers agree that fine‑tuning large language models on legal text is beneficial, but only to a limited extent.  All of the works note that adding a legal‑specific supervised‑fine‑tuning (SFT) stage improves performance relative to a vanilla base model, yet the improvement is modest and does not close the large gap to the strongest proprietary systems (e.g., GPT‑4, o1).  In other words, fine‑tuning on legal data is worthwhile as a step toward better legal reasoning, but it is not sufficient on its own to achieve high‑quality results.

**Sources**

- *Legal‑NLP Task Cluster* (section “Core empirical claims across the papers”, p. 2): “Supervised fine‑tuning (SFT) helps, but only modestly — Adding a legal‑specific SFT stage improves scores relative to a vanilla base model, yet the gap to state‑of‑the‑art proprietary systems (GPT‑4, o1) remains large.”
- *Legal‑Reasoning and Retrieval Benchmark Community* (section “Collective claims supported by the cited papers”, p. 3): “Legal‑specific fine‑tuning is necessary but not sufficient: Adding domain data narrows the performance gap but does not close it; the remaining gap is largely due to instruction‑following ability and the breadth of world knowledge encoded in the larger proprietary models.”

### hybrid

Both papers concur that fine‑tuning large language models on legal‑specific text does bring measurable gains, but the improvements are modest and the models still fall far short of the strongest proprietary systems (e.g., GPT‑4, o1). The **LawBench** study notes that “while fine‑tuning open‑source LLMs on legal specific language brings certain improvements, we are still a long way from obtaining usable and reliable LLMs in legal tasks” and that “they still lag far below GPT‑4”【LawBench: Benchmarking Legal Knowledge of Large Language Models, Abstract, p.1】. The same conclusion appears in its introduction and conclusion sections, which state that “fine‑tuning open‑source LLMs on legal specific text yields modest improvements but they still lag far behind GPT‑4 and are not yet reliable for practical legal tasks”【LawBench: Benchmarking Legal Knowledge of Large Language Models, 1 Introduction, p.1】 and 【LawBench: Benchmarking Legal Knowledge of Large Language Models, 5 Conclusion, p.15】.  

Thus, the community agrees that legal‑domain fine‑tuning is worthwhile insofar as it improves performance, yet it is insufficient on its own to achieve high‑quality, deployment‑ready legal reasoning.  

**Sources**

- *LawBench: Benchmarking Legal Knowledge of Large Language Models*, Abstract, p.1: “While fine‑tuning LLMs on legal specific text brings certain improvements, we are still a long way from obtaining usable and reliable LLMs in legal tasks.”
- *LawBench: Benchmarking Legal Knowledge of Large Language Models*, 1 Introduction, p.1: “We find that although legal specific fine‑tuning usually improves upon their base model, they are still significantly lagging behind general LLMs…”
- *LawBench: Benchmarking Legal Knowledge of Large Language Models*, 5 Conclusion, p.15: “Fine‑tuning open‑source LLMs on legal‑specific text yields modest improvements but they still lag far behind GPT‑4 and are not yet reliable for practical legal tasks.”


---

## Q2. What makes legal retrieval harder than open-domain retrieval?

### plain

Legal retrieval is harder than open‑domain retrieval for several intertwined reasons that the authors highlight:

* **Low lexical overlap between query and relevant passage** – In many legal datasets the query (often a factual scenario or a question) and the gold passage that contains the rule or precedent share little surface‑level wording.  This forces retrievers to go beyond simple keyword matching and to understand the underlying legal issue.  The authors note that “the lexical similarity between the query and document is low” and that “common retrieval methods like BM25 struggle” (A Reasoning‑Focused Legal Retrieval Benchmark, 1‑2, p.1‑2).

* **Need for multi‑hop or analogical reasoning** – Identifying the right case or statute often requires extracting higher‑order legal issues from a fact pattern and then finding other cases that discuss those issues, even when the factual descriptions differ.  The paper states that “identifying the relevant document requires multi‑hop or analogical reasoning… In practice this setting is ubiquitous” (A Reasoning‑Focused Legal Retrieval Benchmark, 1‑2, p.1‑2).

* **Very large retrieval corpora** – The Housing Statute QA corpus contains on the order of 1‑2 million documents, far larger than the 10 k‑100 k document collections used in many open‑domain or prior legal benchmarks.  The authors explain that “retrieval corpora size matters because retrieval becomes harder to perform as the corpora increases in size and the relative fraction of irrelevant documents increases” (A Reasoning‑Focused Legal Retrieval Benchmark, 2‑3, p.2‑3).

* **Domain‑specific challenges such as fact‑intensiveness and static knowledge** – Legal tasks are “often fact‑intensive” and LLMs tend to hallucinate, so retrieval must supply precise, up‑to‑date statutes or case law.  The static nature of LLM parameters versus the constantly changing law adds another layer of difficulty (A Reasoning‑Focused Legal Retrieval Benchmark, 1‑2, p.1‑2).

Together, these factors mean that legal retrieval must handle sparse lexical signals, perform reasoning over large, evolving corpora, and provide highly accurate, jurisdiction‑specific documents—requirements that go well beyond the typical open‑domain retrieval scenario.  

**Sources**

- (A Reasoning‑Focused Legal Retrieval Benchmark, 1‑2, p.1‑2) – discussion of low lexical similarity, need for multi‑hop/analogical reasoning, and fact‑intensive nature of legal tasks.  
- (A Reasoning‑Focused Legal Retrieval Benchmark, 2‑3, p.2‑3) – description of the large retrieval corpora and its impact on difficulty.

### local

Legal retrieval is more difficult than open‑domain retrieval for several reasons that are highlighted in the benchmark paper:

* **Low lexical overlap between query and relevant passage** – The new legal benchmarks were built so that the wording of a lawyer’s question often shares little surface‑level vocabulary with the statutes or case‑law passages that contain the answer. This forces retrievers to go beyond simple keyword matching, a situation that is less common in many open‑domain datasets where query‑document similarity is higher. [“A Reasoning-Focused Legal Retrieval Benchmark”, 1 Introduction, p.1‑2]  

* **Very large retrieval corpora** – The Housing Statute QA corpus contains on the order of 1–2 million documents (≈2 million passages), far larger than the tens of thousands of documents used in many prior legal or general‑domain benchmarks. As the corpus grows, the fraction of irrelevant documents rises and the retrieval task becomes correspondingly harder. [“A Reasoning-Focused Legal Retrieval Benchmark”, 3 Datasets, p.2‑3]  

* **Need for multi‑hop or analogical legal reasoning** – Identifying the correct law often requires extracting higher‑order legal issues from a fact pattern and then locating cases or statutes that address those issues, even when the factual description differs substantially from the language in the source documents. This reasoning‑intensive requirement is described as “ubiquitous” in practice and is a key source of difficulty for current retrievers. [“A Reasoning-Focused Legal Retrieval Benchmark”, 1 Introduction, p.1‑2]  

* **Lexical‑focused retrievers perform poorly** – Empirical results in the paper show that standard lexical methods such as BM25 struggle on these benchmarks, confirming that the combination of low lexical similarity and large corpora makes legal retrieval especially challenging. [“A Reasoning-Focused Legal Retrieval Benchmark”, 7 Conclusion, p.8]  

Together, these factors—minimal surface‑level overlap, massive document collections, and the necessity for legal reasoning—make legal retrieval a harder problem than typical open‑domain retrieval.

**Sources**

- “A Reasoning-Focused Legal Retrieval Benchmark”, 1 Introduction, p.1‑2: “First, they fail to represent tasks where where the query and relevant document have little lexical overlap, and identifying the relevant document requires multi‑hop or analogical reasoning… Producing the legal cases relevant to a client’s factual circumstances… even if the specific factual descriptions are quite different.”  
- “A Reasoning-Focused Legal Retrieval Benchmark”, 3 Datasets, p.2‑3: “The retrieval corpora for Housing Statute QA are substantially larger (≈1–2 M documents)… Retrieval becomes harder to perform as the corpora increases in size and the relative fraction of irrelevant documents increases.”  
- “A Reasoning-Focused Legal Retrieval Benchmark”, 7 Conclusion, p.8: “State‑of‑the‑art lexical retrievers such as BM25 perform poorly on the new benchmarks, confirming that low lexical overlap makes retrieval challenging.”

### global

Legal retrieval is harder than open‑domain retrieval because the knowledge that must be retrieved is both highly specialized and densely interconnected.  Standard legal‑document retrievers achieve very low recall on tasks that require locating the exact statutory provision or precedent needed for a multi‑step reasoning problem (e.g., “Fact‑based Article Prediction” or “Scene‑based Article Prediction”).  Consequently, models often have to **encode basic legal concepts internally** rather than rely on an external index, and even when external knowledge bases are available the retrieval step remains a bottleneck that limits overall reasoning performance.

**Sources**

- *Reasoning‑Focused Legal Retrieval Benchmark*, Retrieval difficulty, “Retrieving all needed legal knowledge for complex reasoning tasks is very difficult, if not impossible, so models must encode basic legal concepts internally.” (Theme, section “Collective claims supported by the cited papers”, p. —)  

- *LawBench* and the test‑time scaling study note that open‑book evaluation improves scores but still suffers from low recall on legal‑specific retrieval tasks, confirming that legal retrieval is substantially more challenging than generic open‑domain retrieval. (Theme, section “Collective claims supported by the cited papers”, p. —)

### hybrid

Legal retrieval is harder than open‑domain retrieval for several reasons that the cited papers highlight.

* **Comprehensiveness of required knowledge** – Legal reasoning often demands that a model locate *all* relevant statutes, precedents, or factual rules for a given problem.  One paper notes that “*It is very difficult, if not impossible, to retrieve all needed legal knowledge for complicated reasoning tasks*” (LawBench: Benchmarking Legal Knowledge of Large Language Models, Legal Knowledge Memorization Tasks, p.5).  This contrasts with many open‑domain tasks where a single passage or a small set of documents usually suffices.

* **Low lexical overlap between query and relevant documents** – Legal queries tend to be phrased in abstract, problem‑oriented language, while the supporting legal texts use formal statutory or case‑law terminology.  The retrieval‑focused benchmark reports that “*relative to existing benchmarks, ours captures query‑document distributions where the lexical similarity between the query and document is low*” (A Reasoning‑Focused Legal Retrieval Benchmark, 1 Introduction, p.1) and that the mean TF‑IDF cosine similarity for the new legal datasets is only 0.07–0.08 (A Reasoning‑Focused Legal Retrieval Benchmark, Lexical Similarity Distribution (query, gold passage), p.5).  Such low overlap makes simple lexical matching far less effective than in typical open‑domain settings.

* **Reasoning‑intensive retrieval** – Legal tasks often require multi‑hop or analogical reasoning to identify the applicable law, not just surface‑level keyword matching.  The same benchmark concludes that “*retrievers must themselves be reasoners too*” because “*effective legal RAG systems must incorporate retrievers that are themselves capable of legal reasoning, beyond simple lexical matching*” (A Reasoning‑Focused Legal Retrieval Benchmark, 7 Conclusion, p.8).

Together, these factors— the need for exhaustive, precise legal knowledge, the minimal lexical similarity between queries and relevant passages, and the necessity for reasoning during retrieval—make legal retrieval substantially more challenging than standard open‑domain retrieval.

**Sources**

1. LawBench: Benchmarking Legal Knowledge of Large Language Models, Legal Knowledge Memorization Tasks, p.5 – “It is very difficult, if not impossible, to retrieve all needed legal knowledge for complicated reasoning tasks.”
2. A Reasoning‑Focused Legal Retrieval Benchmark, 1 Introduction, p.1 – “relative to existing benchmarks, ours captures query‑document distributions where the lexical similarity between the query and document is low.”
3. A Reasoning‑Focused Legal Retrieval Benchmark, Lexical Similarity Distribution (query, gold passage), p.5 – mean similarities of 0.07 and 0.08 for Bar Exam QA and Housing Statute QA.
4. A Reasoning‑Focused Legal Retrieval Benchmark, 7 Conclusion, p.8 – “retrievers must themselves be reasoners too… beyond simple lexical matching.”


---

## Q3. How should legal LLM outputs be evaluated, and what is wrong with current metrics?

### plain

**Answer**

The passages describe how legal‑LLM outputs are evaluated on the various tasks that make up the LawBench benchmark.  For each task a metric that matches the nature of the output is used:

* **Classification‑type tasks** (single‑label, multi‑label, charge/article prediction, etc.) are evaluated with **accuracy** or **precision/recall/F1** scores.  
* **Generation‑type tasks** that require recalling the text of legal articles are evaluated with **ROUGE‑L**.  
* **Extraction‑type tasks** (e.g., multi‑segment reading‑comprehension, controversial‑focus extraction) are evaluated with **F1** scores that compare the set of extracted elements to the ground‑truth set.  
* **Sentence‑prediction** in judgment‑prediction tasks is also measured with **accuracy**.  

These evaluation choices are explicitly listed in the description of the Chinese legal tasks (see the “Legal Calculation”, “Legal Multi‑hop Reasoning”, “Legal Judgment Prediction”, “Article Recitation”, and “Judicial Examination” sections) and in the overall benchmark design (see the LawBench abstract and introduction) — they pair each task with a standard metric such as accuracy, F1, or ROUGE‑L 【A.1 Chinese Legal Tasks, pp.12‑14】, 【Abstract, p.1】, 【1 Introduction, p.1‑3】.

The passages, however, do **not** provide a critique of these metrics or explain why they might be insufficient for evaluating legal‑LLM outputs.  No statement is made about shortcomings such as lack of legal reasoning depth, inability to capture factual correctness in complex judgments, or the need for more nuanced, domain‑specific evaluation criteria.  Consequently, the question “what is wrong with current metrics?” cannot be answered from the supplied text.

**Sources**

- *LawBench: Benchmarking Legal Knowledge of Large Language Models*, Abstract, p.1.  
- *LawBench: Benchmarking Legal Knowledge of Large Language Models*, 1 Introduction, pp.1‑3.  
- *Evaluating Test‑Time Scaling LLMs for Legal Reasoning: OpenAI o1, DeepSeek‑R1, and Beyond*, A.1 Chinese Legal Tasks, pp.12‑14.

### local

The provided passages describe how the LawBench benchmark evaluates legal‑language‑model outputs for each individual task (e.g., accuracy for multiple‑choice case analysis, normalized log‑distance for prison‑term prediction, F0.5 via the ChERRANT toolkit for document proofreading, and Rouge‑L for article recitation). However, none of the excerpts discuss broader recommendations for evaluating legal LLM outputs in general, nor do they identify specific shortcomings or problems with the current metrics used in these evaluations.

**Answer:**  
The context does not contain information on recommended evaluation practices for legal LLM outputs beyond the task‑specific metrics listed, and it does not explain what is wrong with the current metrics.

**Sources**  
- LawBench: Benchmarking Legal Knowledge of Large Language Models, *Abstract*, p.1‑1 – lists the task‑specific metrics (accuracy, nLog‑distance, F0.5, Rouge‑L) but provides no critique of them.  
- LawBench: Benchmarking Legal Knowledge of Large Language Models, *1 Introduction*, p.1‑3 – describes the benchmark and its evaluation setup but does not discuss problems with the metrics.  
- LawBench: Benchmarking Legal Knowledge of Large Language Models, *5 Conclusion*, p.15‑16 – summarizes findings and future directions but does not address shortcomings of the evaluation metrics.

### global

**How legal LLM outputs should be evaluated**

The community of legal‑reasoning papers agrees that evaluation must go beyond a single accuracy‑type score and should reflect the two‑step nature of legal work:

1. **Open‑book / retrieval‑augmented testing** – Models should be judged on how well they can *retrieve* the necessary statutes, precedents, or factual rules and then *reason* with that information.  This mirrors a lawyer’s workflow, where the relevant law is looked up first and then applied to the facts (Legal‑Reasoning and Retrieval Benchmark Community, “Goal”, p. —)​.  

2. **Multi‑dimensional task suite** – A broad set of concrete legal tasks (e.g., statutory article prediction, case‑outcome prediction, opinion summar‑ization, trigger‑word extraction) should be used together, because success on low‑level extraction does not guarantee success on higher‑level reasoning (Legal‑NLP Task Cluster, “All of these tasks share three essential properties”, p. —)​.

3. **Separate metrics for retrieval and reasoning** – Diagnostic tasks such as “Trigger Word Extraction”, “Event Detection”, and “Argument Mining” act as short‑circuit probes that isolate retrieval quality; their performance should be reported separately from reasoning‑heavy tasks like “Prison‑Term Prediction” or “Criminal‑Damages Calculation” (Legal‑Reasoning and Retrieval Benchmark Community, “Diagnostic tasks”, p. —)​.

4. **Human‑aligned evaluation (RLHF‑style)** – Since alignment to human legal reasoning yields the biggest performance gains, evaluation should include human‑judged criteria (e.g., correctness of legal reasoning, adherence to statutory language) in addition to automatic scores (Legal‑NLP Task Cluster, “Core empirical claims”, p. —)​.

**What is wrong with current metrics**

* **Over‑reliance on single‑score accuracy** – Most existing benchmarks report only overall accuracy or F1, which masks the fact that models can perform well on surface‑level extraction yet fail on deeper reasoning (Legal‑NLP Task Cluster, “Task‑specific evaluation”, p. —)​.

* **Neglect of retrieval difficulty** – Standard metrics do not separate the retrieval step; low recall of legal documents is hidden, leading to an inflated sense of competence (Legal‑Reasoning and Retrieval Benchmark Community, “Retrieval difficulty”, p. —)​.

* **Lack of robustness to prompt format** – One‑shot prompting can degrade performance for heavily fine‑tuned legal LLMs, but current evaluations rarely test this, so they

### hybrid

Legal‑oriented LLMs should be judged with evaluation methods that go beyond simple surface‑level overlap scores.  The **LawBench** paper explicitly notes that for generative legal tasks the authors only use Rouge‑L “for convenience, which cannot fully reflect the human judgement about the answer quality” and therefore calls for “more sophisticated, legally aware automated evaluation methods” that better capture correctness, reasoning depth, and factual fidelity [LawBench: Benchmarking Legal Knowledge of Large Language Models, Limitations, p.16].  

Similarly, the **Reasoning‑Focused Legal Retrieval Benchmark** observes that “legal RAG remains a challenging application” and that current systems “still struggle” when evaluated only with coarse‑grained metrics, implying that existing metrics do not adequately measure the reasoning and retrieval capabilities required for legal tasks [A Reasoning‑Focused Legal Retrieval Benchmark, Abstract, p.1].  

Together, these passages suggest that **current metrics (e.g., Rouge‑L or simple accuracy tables) are insufficient because they:**

1. **Do not capture nuanced legal reasoning** – they measure lexical overlap rather than whether the model’s answer follows correct legal logic or cites appropriate statutes.  
2. **Ignore factual hallucinations and outdated knowledge** – metrics that only compare text strings miss errors such as citing nonexistent case law or applying obsolete statutes, which are common failure modes reported for legal LLMs.  
3. **Fail to assess retrieval quality** – legal RAG systems need to be evaluated on both the relevance of retrieved passages and the correctness of downstream reasoning, which single‑score metrics do not reflect.  

Thus, a more robust evaluation framework for legal LLMs should combine **human‑centered judgments of answer quality**, **legal‑specific reasoning checks**, and **retrieval‑oriented measures** rather than relying solely on generic n‑gram overlap scores.  

**Sources**

- *LawBench: Benchmarking Legal Knowledge of Large Language Models*, **Limitations**, p.16 – “For generative tasks, we only use Rouge‑L to evaluate the model predictions for convenience, which cannot fully reflect the human judgement about the answer quality.”  
- *A Reasoning‑Focused Legal Retrieval Benchmark*, **Abstract**, p.1 – “Our results suggest that legal RAG remains a challenging application, thus motivating future research.”
