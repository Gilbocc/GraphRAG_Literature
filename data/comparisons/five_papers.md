# Retrieval comparison — 2026-08-11 18:19

Model `openai/gpt-oss-120b`, embeddings `openai/text-embedding-3-small`, top_k=5.

- **plain** — nearest chunks only, no graph. The control.
- **local** — nearest chunks, plus the claims each one grounds.
- **global** — community summaries only.
- **hybrid** — community summaries, plus each theme's claims and the verbatim passage behind them.


---

## Q1. Do the papers agree on whether fine-tuning LLMs on legal text is worthwhile?

### plain

The papers convey a consistent view that fine‑tuning large language models on legal‑specific text can yield some performance gains, but that such gains are modest and do not solve the deeper shortcomings of current models.

* **LawBench** explicitly notes that “fine‑tuning LLMs on legal specific text brings certain improvements, we are still a long way from obtaining usable and reliable LLMs in legal tasks” (LawBench, Abstract, p.1).  
* **Legal Evaluations and Challenges of Large Language Models** stresses the need to “integrate domain‑specific legal knowledge” and improve training methodologies (Legal Evaluations and Challenges of Large Language Models, VI. DISCUSSION, p.8; D. Technical limitations, p.8). While it does not use the word “fine‑tuning,” the call for domain‑specific training aligns with the idea that adapting models to legal data is beneficial, yet still insufficient on its own.  

Thus, both papers agree that adapting LLMs to legal text (e.g., via fine‑tuning or domain‑specific training) is worthwhile insofar as it improves performance, but they also agree that this alone does not make the models fully reliable for legal tasks.

**Sources**

- LawBench: Benchmarking Legal Knowledge of Large Language Models, *Abstract*, p.1.  
- Legal Evaluations and Challenges of Large Language Models, *VI. DISCUSSION*, p.8.  
- Legal Evaluations and Challenges of Large Language Models, *D. Technical limitations*, p.8.

### local

Both papers acknowledge that fine‑tuning large language models on legal‑specific corpora can bring some gains, but they also stress that such improvements are limited and do not make the models fully reliable for legal tasks.  

* The LawBench study reports that “fine‑tuning open‑source LLMs on legal‑specific text yields modest improvements but they still lag far behind GPT‑4 and are not yet reliable for practical legal tasks” (LawBench, Abstract, p.1).  
* The Legal Evaluations paper notes that “tailoring LLMs to the legal domain (e.g., fine‑tuning on legal corpora) improves terminology understanding but does not fully resolve cross‑jurisdictional or ethical challenges” (Legal Evalutions and Challenges of Large Language Models, VI. DISCUSSION, p.8).  

Thus, the two papers agree that fine‑tuning is beneficial to a degree but is not sufficient on its own to produce dependable legal‑domain performance.

**Sources**

- *LawBench: Benchmarking Legal Knowledge of Large Language Models*, Abstract, p.1: “Fine‑tuning open‑source LLMs on legal‑specific text yields modest improvements but they still lag far behind GPT‑4 and are not yet reliable for practical legal tasks.”  
- *Legal Evalutions and Challenges of Large Language Models*, VI. DISCUSSION, p.8: “Tailoring LLMs to the legal domain (e.g., fine‑tuning on legal corpora) improves terminology understanding but does not fully resolve cross‑jurisdictional or ethical challenges.”

### global

The papers concur that fine‑tuning large language models on legal corpora is beneficial but not a complete solution.  Fine‑tuning improves the models’ grasp of legal terminology and yields modest performance gains, yet it does not fully close the gaps caused by model size, cross‑jurisdictional nuances, or factual errors, so the models still fall short of reliable, fully automated legal judgment.

**Sources**

- (Legal Reasoning with Large Language Models, summary, p.N) – “Fine‑tuning on legal corpora improves terminology understanding and modestly boosts performance, yet it does not fully eliminate gaps caused by model scale or cross‑jurisdictional nuances.”

### hybrid

The papers do not present a unanimous endorsement that fine‑tuning LLMs on legal text is a complete solution.  One paper notes that domain‑specific fine‑tuning **does improve** the model’s handling of legal terminology and provisions, but it also stresses that this improvement **does not fully close the performance gap** with larger, general‑purpose models (Legal Evalutions and Challenges of Large Language Models, I. INTRODUCTION, p.1).  Another discussion in the same work points out that, despite the potential of LLMs, their **limitations in accurately interpreting complex legal language and reasoning remain clear**, indicating that further advances in training—such as better integration of domain‑specific knowledge—are still needed (Legal Evalutions and Challenges of Large Language Models, VI. DISCUSSION, p.8).

Together, these passages suggest that the authors view fine‑tuning on legal data as **worthwhile insofar as it yields measurable gains**, but they also agree that it is **insufficient on its own** to achieve parity with the best‑performing, larger models or to fully overcome the challenges of legal reasoning.

**Sources**

- Legal Evalutions and Challenges of Large Language Models, I. INTRODUCTION, p.1  
  “This specialization aims to increase the practical value of LLMs in legal practice … Domain‑specific fine‑tuning improves LLMs’ ability to handle legal terminology and provisions, but does not fully close the performance gap with larger, general‑purpose models.”  

- Legal Evalutions and Challenges of Large Language Models, VI. DISCUSSION, p.8  
  “In conclusion, while LLMs show considerable potential … their limitations in accurately interpreting complex legal language and reasoning remain clear. These models struggle to fully grasp the subtle nuances of legal concepts … indicating a need for improvements in training methodologies—particularly in integrating domain‑specific legal knowledge and strengthening reasoning capabilities.”


---

## Q2. What makes legal retrieval harder than open-domain retrieval?

### plain

**Answer**

Legal retrieval is harder than open‑domain retrieval because the query‑document relationship in law often has **very little lexical overlap** and requires **reasoning‑intensive, multi‑hop or analogical matching** rather than simple keyword matching.  In legal tasks the relevant passage may restate a rule or principle in language that is quite different from the factual description in the query, so a retriever must understand the underlying legal issue and locate statutes or case passages that apply to that issue.  Moreover, legal corpora are **much larger** (often millions of documents) and contain many passages that are superficially similar but legally irrelevant, making it difficult to rank the truly pertinent documents.  These factors together mean that standard lexical retrievers such as BM25 struggle on legal benchmarks, whereas open‑domain retrieval datasets typically exhibit higher lexical similarity between query and answer passages.

**Sources**

- (A Reasoning-Focused Legal Retrieval Benchmark, 1 Introduction, p.1‑2) – notes that “existing benchmarks fail to represent tasks where the query and relevant document have little lexical overlap, and identifying the relevant document requires multi‑hop or analogical reasoning… In practice this setting is ubiquitous… producing the legal cases relevant to a client’s factual circumstances… even if the specific factual descriptions are quite different.”
- (A Reasoning-Focused Legal Retrieval Benchmark, 2 Related Works > 2.2 Legal Information Retrieval Datasets, p.2) – observes that “the citing contexts often summarize the high‑level rule… As a result, we find the lexical similarity of the query and the gold passage is often quite high… [but] few datasets have natural question‑style queries…"
- (A Reasoning-Focused Legal Retrieval Benchmark, 3 Datasets, p.2‑3) – points out that “our retrieval corpora… are substantially larger (~1‑2M documents)… Retrieval corpora size matters because retrieval becomes harder to perform as the corpora increases in size and the relative fraction of irrelevant documents increases.”

### local

Legal retrieval is more difficult than open‑domain retrieval for several reasons.  

First, the corpora used for legal tasks are far larger – the Housing Statute QA benchmark searches over roughly 1–2 million statute passages, whereas many open‑domain or prior legal benchmarks use only tens of thousands of documents.  The sheer size increases the fraction of irrelevant material and makes it harder for a retriever to surface the correct passage【A Reasoning-Focused Legal Retrieval Benchmark, 3 Datasets, p.2‑3】.  

Second, the lexical overlap between a user’s question and the relevant legal text is often low.  The Bar Exam QA and Housing Statute QA queries are natural‑language questions that do not share many surface words with the statutes or case passages that justify the answer, so simple lexical matchers such as BM25 perform poorly【A Reasoning-Focused Legal Retrieval Benchmark, 7 Conclusion, p.8】.  

Third, identifying the right document frequently requires multi‑hop or analogical legal reasoning – the retriever must infer the underlying legal issue from the facts and then locate statutes or cases that address that issue, even when the factual description differs substantially from the language of the law【A Reasoning-Focused Legal Retrieval Benchmark, 1 Introduction, p.1‑2】.  

Together, the combination of massive, heterogeneous legal corpora, low surface‑form similarity, and the need for reasoning‑intensive matching makes legal retrieval a harder problem than typical open‑domain retrieval.  

**Sources**  
- *A Reasoning-Focused Legal Retrieval Benchmark*, **3 Datasets**, p.2‑3: “The retrieval corpora for Housing Statute QA are substantially larger (≈1–2 M documents) … increasing retrieval difficulty as corpus size grows.”  
- *A Reasoning-Focused Legal Retrieval Benchmark*, **7 Conclusion**, p.8: “State‑of‑the‑art lexical retrievers such as BM25 perform poorly on the new benchmarks, confirming that low lexical overlap makes retrieval challenging.”  
- *A Reasoning-Focused Legal Retrieval Benchmark*, **1 Introduction**, p.1‑2: “they fail to represent tasks where the query and relevant document have little lexical overlap, and identifying the relevant document requires multi‑hop or analogical reasoning.”

### global

Legal retrieval is harder than open‑domain retrieval for several reasons that the cited literature highlights:

1. **Need for legal reasoning in the retriever** – Unlike open‑domain search, which can rely on simple keyword matching, legal retrieval must identify and reason over nuanced legal concepts, precedents, and statutory language. Effective legal RAG systems therefore require retrievers that can perform legal reasoning rather than just lexical overlap (Legal Retrieval‑Augmented Generation and Evaluation, Summary).

2. **Complex, domain‑specific knowledge** – Legal tasks demand extensive, highly specialized knowledge that is often implicit, hierarchical, and context‑dependent. Models must retrieve not only surface‑level facts but also the underlying legal principles and doctrinal relationships, which are far richer than the general‑world facts typical of open‑domain corpora (Legal Reasoning and Retrieval Benchmarks for LLMs, Summary).

3. **Evaluation challenges** – Standard lexical overlap metrics (e.g., ROUGE‑L) that work reasonably well for open‑domain generation do not correlate with human judgments of answer quality in legal contexts. This makes it difficult to measure retrieval effectiveness and to guide system improvement (Legal Retrieval‑Augmented Generation and Evaluation, Summary).

4. **Document characteristics** – Legal documents are often long, highly structured, and contain dense jargon, making it harder for retrievers to index and retrieve the relevant passages within limited context windows. Additionally, certain sensitive documents (e.g., NDAs) are excluded from benchmarks, further complicating the retrieval landscape (Legal Reasoning and Retrieval Benchmarks for LLMs, Summary).

5. **Risk of hallucination and factual error** – Because legal decisions hinge on precise facts and correct application of law, any hallucination or factual inaccuracy in retrieved material can have severe consequences, raising the stakes for retrieval fidelity compared with open‑domain tasks (Legal Large Language Model Benchmarking and Evaluation, Summary).

**Sources**

- Legal Retrieval‑Augmented Generation and Evaluation, Summary.  
- Legal Reasoning and Retrieval Benchmarks for LLMs, Summary.  
- Legal Large Language Model Benchmarking and Evaluation, Summary.

### hybrid

Legal retrieval is harder than open‑domain retrieval because it must go beyond simple keyword or lexical overlap matching and perform legal reasoning on the retrieved material.  The authors of the reasoning‑focused benchmark argue that “retrievers must themselves be reasoners too” and that “developers of retrieval‑augmented legal LLM products may need to go further than simple retrievers to improve the performance of their approaches… they may need to ensure that retrievers can also be legal reasoners” (A Reasoning‑Focused Legal Retrieval Benchmark, 1 Introduction, p.1; 7 Conclusion, p.8).  Moreover, the benchmark’s results show that “certain legal tasks may be particularly well suited to exposing limitations of current retrieval models on reasoning‑intensive retrieval tasks” (A Reasoning‑Focused Legal Retrieval Benchmark, 7 Conclusion, p.8).  Together, these points indicate that legal retrieval requires understanding and applying legal concepts, statutes, and precedents—capabilities that typical open‑domain retrievers, which rely mainly on surface lexical similarity, do not possess.  

**Sources**

- *A Reasoning‑Focused Legal Retrieval Benchmark*, 1 Introduction, p.1: “developers of retrieval‑augmented legal LLM products may need to go further than simple retrievers to improve the performance of their approaches. In particular, they may need to ensure that retrievers can also be legal reasoners.”
- *A Reasoning‑Focused Legal Retrieval Benchmark*, 7 Conclusion, p.8: “These findings suggest that retrievers must themselves be reasoners too. And that certain legal tasks may be particularly well suited to exposing limitations of current retrieval models on reasoning‑intensive retrieval tasks.”


---

## Q3. How should legal LLM outputs be evaluated, and what is wrong with current metrics?

### plain

**Answer**

The provided passages do not contain a discussion of how legal‑LLM outputs should be evaluated, nor do they identify specific problems with the metrics that are currently used for such evaluation.  

The excerpts describe the existence of various benchmarks (LawBench, LegalBench, LexEval, etc.) and the metrics that have been applied in particular tasks—such as accuracy, F‑score, and ROUGE‑L—but they do not offer guidance on the appropriate evaluation methodology for legal‑LLM outputs or critique the adequacy of those metrics.

**Sources**

- *LawBench: Benchmarking Legal Knowledge of Large Language Models*, Abstract, p. 1 – describes the benchmark and the cognitive dimensions it covers, but gives no prescription for evaluating LLM outputs or a critique of metrics.  
- *LawBench: Benchmarking Legal Knowledge of Large Language Models*, Introduction, p. 1‑3 – outlines the benchmark tasks and mentions the use of rules, regular expressions, and metrics for each task, yet does not discuss how outputs should be evaluated overall or the shortcomings of current metrics.  
- *Evaluating Test-Time Scaling LLMs for Legal Reasoning: OpenAI o1, DeepSeek‑R1, and Beyond*, Sections 2.1 and A.1, pp. 2, 12‑14 – list various legal tasks and the metrics employed (accuracy, F1, ROUGE‑L), without evaluating those metrics or proposing alternatives.  
- *Better Call GPT, Comparing Large Language Models Against Lawyers*, 5.1, pp. 9‑10 – reports performance numbers (F‑scores) for contract‑issue tasks, but does not discuss the adequacy of the metrics themselves.  

Since none of the supplied passages address the question of proper evaluation methods for legal‑LLM outputs or the deficiencies of existing metrics, the answer cannot be derived from the given material.

### local

The provided passages describe how various legal‑oriented benchmarks evaluate LLM outputs—typically by measuring task‑specific scores such as accuracy for multiple‑choice or classification tasks, F‑score for issue‑determination and location, Rouge‑L for article‑recitation, and normalized log‑distance for sentence‑length prediction. However, none of the cited papers explicitly discuss shortcomings of these metrics or propose alternative evaluation approaches. Consequently, the current documents do not contain an answer to the question about what is wrong with existing metrics.  

**Sources**  
- LawBench: Benchmarking Legal Knowledge of Large Language Models, *Abstract*, p.1‑1 – describes the suite of tasks and the metrics (accuracy, F0.5, Rouge‑L, nLog‑distance) used for evaluation.  
- LawBench: Benchmarking Legal Knowledge of Large Language Models, *1 Introduction*, p.1‑3 – details the same task‑specific metrics and the overall evaluation framework.  
- Better Call GPT, Comparing Large Language Models Against Lawyers, *5.1 Do LLMs outperform Junior Lawyers and LPOs…*, p.9‑10 – reports F‑scores for issue determination and location but does not critique the metrics themselves.

### global

The community literature agrees that legal‑focused large‑language‑model outputs should be judged with evaluation methods that reflect real legal reasoning and professional standards rather than relying on generic lexical overlap scores.  Researchers emphasize the need for **human‑centered assessments** that measure whether a model’s answer is legally accurate, interpretable, and useful for practitioners, and they call for **open‑book or retrieval‑augmented testing** that separates the quality of the retrieved legal material from the model’s reasoning process.  

By contrast, the most common automatic metrics such as **ROUGE‑L** (and similar n‑gram overlap measures) have been shown to be poor proxies for human judgments in legal settings.  These metrics reward surface‑level similarity without capturing whether the generated text correctly applies the law, respects jurisdictional nuances, or avoids factual and legal errors.  Consequently, they can rate a legally incorrect but superficially similar answer highly, while penalizing a correct answer that uses different phrasing.

**Key points drawn from the literature**

* Evaluation should be **task‑specific and legally grounded**, using benchmarks like LawBench that categorize tasks by cognitive difficulty (memorization, understanding, applying) and that include open‑book setups to isolate retrieval performance.  
* **Human expert review** is required to assess factual correctness, legal reasoning, interpretability, and bias, because automatic lexical metrics do not capture these dimensions.  
* Metrics that only measure lexical overlap (e.g., ROUGE‑L) are **inadequate for legal RAG systems**, as they do not reflect the quality of legal reasoning or the relevance of retrieved passages.  

**What is wrong with current metrics**

* They **ignore the necessity of legal reasoning**, focusing solely on surface similarity.  
* They **fail to account for the correctness of legal facts and arguments**, leading to misleading performance scores.  
* They **do not differentiate between good retrieval and good generation**, making it hard to diagnose where a system is weak.  

**Recommended evaluation approach**

1. **Use standardized, multilingual legal benchmarks** (e.g., LawBench) that cover a range of tasks and jurisdictions.  
2. **Incorporate open‑book or retrieval‑augmented evaluation** to separate the retrieval component from the reasoning component.  
3. **Rely on human expert judgments** for final quality assessment, especially for higher‑order reasoning tasks such as judicial ethics or complex statutory interpretation.  
4. **Develop new automatic metrics** that better correlate with human legal judgments, possibly by integrating legal knowledge graphs or domain‑specific entailment models.  

These recommendations reflect the consensus across the cited legal‑LLM communities.  

**Sources**

* Legal Retrieval‑Augmented Generation and Evaluation – the community summary notes that ROUGE‑L is a poor proxy for human judgments in legal contexts and that effective evaluation must involve retrievers capable of legal reasoning.  
* Legal Reasoning and Retrieval Benchmarks for LLMs – the community summary describes the need for open‑book evaluation to separate retrieval from reasoning and the importance of task‑specific benchmarks like LawBench.  
* Legal Large Language Model Benchmarking and Evaluation – the community summary highlights the overall consensus that current LLMs suffer from factual and legal inaccuracies and that systematic, transparent, and multilingual benchmarking is required.

### hybrid

Legal‑oriented large language models should be judged with evaluation methods that go beyond simple lexical‑overlap scores.  The literature notes that **ROUGE‑L (and similar n‑gram metrics) are only a convenience measure and do not capture the quality of legal answers as perceived by humans**; high ROUGE scores can coexist with low human‑judged quality, indicating that these metrics miss nuanced reasoning, factual correctness, and legal adequacy.  Consequently, researchers call for **more sophisticated, legally‑aware automatic metrics or direct human evaluation protocols** that assess factual accuracy, reasoning steps, and compliance with legal standards rather than relying on surface similarity alone.  

**What is wrong with current metrics**

* ROUGE‑L is used for generative legal tasks “for convenience, which cannot fully reflect the human judgement about the answer quality”【Legal Evalutions and Challenges of Large Language Models, Limitations, p.16】.  
* Empirical results show a disconnect: models obtain relatively high ROUGE‑1/2/L scores while their overall human evaluation scores remain modest (e.g., Gemma2‑9B: ROUGE‑L 0.39 but overall evaluation 3.27)【Legal Evalutions and Challenges of Large Language Models, TABLE III OVERALL PERFORMANCE OF LLMS, p.8】.  

Together, these findings suggest that **current lexical overlap metrics are insufficient for legal LLM evaluation** and that **evaluation frameworks should incorporate human‑centric criteria or specialized legal metrics that measure factual correctness, reasoning depth, and adherence to legal norms**.  

---  
**Sources**  

* “For generative tasks, we only use Rouge‑L to evaluate the model predictions for convenience, which cannot fully reflect the human judgement about the answer quality.” (Legal Evalutions and Challenges of Large Language Models, Limitations, p.16)  
* Table showing ROUGE scores versus overall human evaluation scores, e.g., “Gemma2‑9B … Overall ROUGE‑L 0.39 … Overall Evaluation 3.27” (Legal Evalutions and Challenges of Large Language Models, TABLE III OVERALL PERFORMANCE OF LLMS, p.8)


---

## Q4. Where do these papers disagree with each other?

### plain

The provided excerpts do not contain any statements in which the papers express differing conclusions, findings, or interpretations of the same issue. All of the passages are either examples of flawed reasoning in various legal‑reasoning tasks (CFE, IAPE, CPC) or descriptions of error types and experimental results from a single study (“Evaluating Test‑Time Scaling LLMs for Legal Reasoning”). The other excerpt (“A Reasoning‑Focused Legal Retrieval Benchmark”) discusses query‑expansion prompts and retrieval performance but does not present a claim that conflicts with any claim made in the first paper.

**Therefore, the passages do not answer the question “Where do these papers disagree with each other?”** They instead cover:

* Types of flawed reasoning observed in different legal‑reasoning tasks (CFE, IAPE, CPC) – (Evaluating Test‑Time Scaling LLMs for Legal Reasoning, Table 11, p. 16; Table 10, p. 16; Table 14, p. 18).  
* Error categories (Inconsistent Subjects, Indirect or Weak Rebuttals) observed in the IAPE task – (Evaluating Test‑Time Scaling LLMs for Legal Reasoning, 5.3.1 IAPE task, pp. 6‑7).  
* Query‑expansion prompts and retrieval‑performance results for Bar Exam QA and Housing Statute QA – (A Reasoning‑Focused Legal Retrieval Benchmark, Table 14, pp. 16‑25).  

No direct disagreement between the papers is evident in the supplied text.

### local

The provided excerpts do not contain any statements in which the two papers contradict one another.  
The first paper (“Evaluating Test‑Time Scaling LLMs for Legal Reasoning: OpenAI o1, DeepSeek‑R1, and Beyond”) reports error analyses for several legal‑reasoning tasks (CFE, IAPE, CPC) and describes the performance of different language models on those tasks.  
The second paper (“A Reasoning‑Focused Legal Retrieval Benchmark”) describes a retrieval benchmark for housing‑statute and bar‑exam questions, presenting query‑expansion methods and retrieval results.  

Because the two works address different research questions—model error typology versus retrieval‑benchmark design—and do not make overlapping claims about the same phenomena, there is no explicit disagreement to report.

**Sources**

- *Evaluating Test‑Time Scaling LLMs for Legal Reasoning: OpenAI o1, DeepSeek‑R1, and Beyond*, various sections (Table 11, 5.3.1 IAPE, Table 10, Table 14) describe error types and examples for legal‑reasoning tasks.  
- *A Reasoning‑Focused Legal Retrieval Benchmark*, Section “Table 14: Query expansion prompts for Housing Statute QA” (pages 16‑25) details the retrieval benchmark and experimental tables.

### global

The provided excerpts do not contain any specific statements in which the individual papers take opposing positions. All three theme summaries describe a general consensus that current legal‑focused large language models face significant challenges (e.g., retrieval difficulties, factual errors, limited higher‑order reasoning) and that further work on benchmarking, domain‑specific training, and retrieval‑augmented generation is needed. No concrete disagreement between particular papers is presented in the available context.

**Sources**

- The three theme summaries (Legal Reasoning and Retrieval Benchmarks for LLMs; Legal Reasoning with Large Language Models; Legal Large Language Model Benchmarking and Evaluation; Legal Retrieval‑Augmented Generation and Evaluation) all describe similar challenges and recommendations, without noting any contradictory findings.

### hybrid

The passages that have been provided do not contain any explicit contradictions between the papers.  

* Several papers agree that **GPT‑4 is the best‑performing model on the LawBench benchmark** (LawBench abstract, Introduction, and Main Results sections).  
* Other papers report that **DeepSeek‑R1 is among the strongest models on Chinese legal tasks** (Evaluating Test‑Time Scaling … Chinese Legal Task Results and Conclusion sections), but they do not claim that DeepSeek‑R1 surpasses GPT‑4, so there is no direct conflict.  
* The claim that **top‑performing legal‑specific LLMs suffer a performance drop after seeing a one‑shot example** (LawBench 4.3 Main Results) is not contradicted by any other passage.  
* The observation that **retrievers need to be legal reasoners** (A Reasoning‑Focused Legal Retrieval Benchmark) is consistent with the broader discussion of retrieval challenges and is not opposed by any other record.  
* Statements about **the difficulty of retrieving all needed legal knowledge** (LawBench Legal Knowledge Memorization Tasks) and the **need for richer domain‑specific training** (Legal Evaluations and Challenges of Large Language Models VI Discussion) are complementary rather than contradictory.  

Because none of the cited passages present opposing empirical results or mutually exclusive claims, there is no documented disagreement among the papers in the supplied context.

**Sources**

* “The results show that GPT‑4 remains the best‑performing LLM in the legal domain, surpassing the others by a significant margin.” – *LawBench: Benchmarking Legal Knowledge of Large Language Models*, Abstract, p.1.  
* “Figure 3 shows the overall zero‑shot performance of each model. As can be seen, GPT‑4 and ChatGPT clearly lead the benchmark, substantially outperform all other models.” – *LawBench: Benchmarking Legal Knowledge of Large Language Models*, 4 Experiment > 4.3 Main Results, p.12.  
* “DeepSeek‑R1 demonstrates consistently strong performance across a wide range of Chinese legal reasoning tasks… it excels in tasks that require logical inference and long‑text comprehension.” – *Evaluating Test‑Time Scaling LLMs for Legal Reasoning: OpenAI o1, DeepSeek‑R1, and Beyond*, 5.2.1 Chinese Legal Task Results, p.5.  
* “DeepSeek‑R1 remains among the strongest on both Chinese and English tasks.” – *Evaluating Test‑Time Scaling LLMs for Legal Reasoning: OpenAI o1, DeepSeek‑R1, and Beyond*, 6 Conclusion, p.9.  
* “The top‑performing legal specific LLMs, however, suffers a drop in performance after seeing the one‑shot example.” – *LawBench: Benchmarking Legal Knowledge of Large Language Models*, 4 Experiment > 4.3 Main Results, p.12.  
* “It is very difficult, if not impossible, to retrieve all needed legal knowledge for complicated reasoning tasks.” – *LawBench: Benchmarking Legal Knowledge of Large Language Models*, Legal Knowledge Memorization Tasks, p.5.  
* “In conclusion, while LLMs show considerable potential … their limitations in accurately interpreting complex legal language and reasoning remain clear. These models struggle to fully grasp the subtle nuances of legal concepts … indicating a need for improvements in training methodologies—particularly in integrating domain‑specific legal knowledge and strengthening reasoning capabilities.” – *Legal Evaluations and Challenges of Large Language Models*, VI Discussion, p.8.  
* “The top‑performing legal specific LLMs, however, suffers a drop in performance after seeing the one‑shot example.” – *LawBench: Benchmarking Legal Knowledge of Large Language Models*, 4 Experiment > 4.3 Main Results, p.12.  
* “And that certain legal tasks may be particularly well suited to exposing limitations of current retrieval models on reasoning‑intensive retrieval tasks.” – *A Reasoning‑Focused Legal Retrieval Benchmark*, 7 Conclusion, p.8.
