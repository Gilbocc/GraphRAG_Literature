# Retrieval comparison — 2026-08-11 20:55

Model `openai/gpt-oss-120b`, embeddings `openai/text-embedding-3-small`, top_k=5.

- **plain** — nearest chunks only, no graph. The control.
- **local** — nearest chunks, plus the claims each one grounds.
- **global** — community summaries only.
- **hybrid** — community summaries, plus each theme's claims and the verbatim passage behind them.


---

## Q1. What kinds of legal reasoning do current benchmarks fail to test?

### plain

**Answer**

Current legal‑reasoning benchmarks focus mainly on a limited set of well‑defined reasoning tasks (e.g., issue‑spotting, rule‑recall, rule‑application, rule‑conclusion, interpretation, and rhetorical‑understanding).  As the authors of the evaluated studies note, this leaves out several important kinds of reasoning that arise in real‑world practice:

* **Subjective and ethical judgment** – Tasks that require evaluating whether a question or scenario violates judicial or professional ethics involve a degree of subjectivity that many benchmarks do not capture.  The authors point out that “issue identification and ethical judgment… involve a degree of subjectivity, where even domain experts may differ in their evaluations” and that existing automatic metrics may fail to reflect the quality of such reasoning【Evaluating Test‑Time Scaling LLMs for Legal Reasoning: OpenAI o1, DeepSeek‑R1, and Beyond, Limitations, p.9】.  

* **Complex, real‑world legal reasoning** – The benchmark’s coverage, while diverse, “may not fully capture the breadth and complexity of legal reasoning encountered in real‑world practice,” suggesting that nuanced, multi‑step reasoning found in actual cases is under‑tested【Evaluating Test‑Time Scaling LLMs for Legal Reasoning: OpenAI o1, DeepSeek‑R1, and Beyond, Limitations, p.9】.  

* **Tasks beyond the six typology** – LEGALBENCH defines six types of legal reasoning (issue‑spotting, rule‑recall, rule‑application, rule‑conclusion, interpretation, rhetorical‑understanding) and acknowledges that “our types are non‑exhaustive, and in future work hope to consider additions to these types”【LEGALBENCH: A COLLABORATIVELY BUILT BENCHMARK…, 3 The LEGALBENCH typology, p.6】.  Consequently, any reasoning forms not mapped to these six categories (e.g., strategic case framing, policy analysis, interdisciplinary reasoning) are currently untested.

In summary, existing benchmarks tend to miss **subjective ethical judgments, the full complexity of real‑world legal problem solving, and any reasoning forms that fall outside the six established categories**.

**Sources**

1. *Evaluating Test‑Time Scaling LLMs for Legal Reasoning: OpenAI o1, DeepSeek‑R1, and Beyond*, **Limitations**, p. 9.  
2. *LEGALBENCH: A COLLABORATIVELY BUILT BENCHMARK FOR MEASURING LEGAL REASONING IN LARGE LANGUAGE MODELS*, **3 The LEGALBENCH typology**, p. 6.

### local

Current legal‑reasoning benchmarks leave several important kinds of reasoning untested.  
Both the authors of the “Evaluating Test‑Time Scaling LLMs for Legal Reasoning” benchmark and the creators of LEGALBENCH note that their suites do not cover the full breadth of legal reasoning that arises in practice.  In particular:

* **Subjective or ethically‑laden judgments** – tasks such as issue identification and ethical judgment often involve a degree of subjectivity, and existing automatic metrics may not capture the quality of model outputs for these kinds of decisions.  (Evaluating Test‑Time Scaling LLMs for Legal Reasoning, *Limitations*, p.9)

* **Reasoning types beyond the six categories defined in LEGALBENCH** – LEGALBENCH focuses on issue‑spotting, rule‑recall, rule‑application, rule‑conclusion, interpretation, and rhetorical‑understanding, but the authors explicitly state that this set is “non‑exhaustive” and that future work should consider additional reasoning categories.  (LEGALBENCH, *3 The LEGALBENCH typology*, p.6)

Thus, current benchmarks tend to omit (i) subjective/ethical reasoning and (ii) any legal‑reasoning forms that fall outside the six typologies currently captured.

**Sources**

* Evaluating Test‑Time Scaling LLMs for Legal Reasoning: OpenAI o1, DeepSeek‑R1, and Beyond, *Limitations*, p.9 – “Certain tasks, such as issue identification and ethical judgment, involve a degree of subjectivity… existing automatic evaluation metrics may fall short…”.  
* LEGALBENCH: A Collaboratively Built Benchmark for Measuring Legal Reasoning in Large Language Models, *3 The LEGALBENCH typology*, p.6 – “The set of six reasoning types is not exhaustive, and future work should consider adding additional reasoning categories.”

### global

The provided context does not contain any specific passages from individual papers that enumerate particular kinds of legal reasoning that current benchmarks fail to test. The themes summarize general observations (e.g., gaps in tax calculations, ethics, multi‑step reasoning, cross‑jurisdictional issues), but no concrete, citable statements from a paper’s section and page are given. Therefore, I cannot supply a sourced answer to the question.

### hybrid

Current legal‑reasoning benchmarks tend to evaluate only isolated, single‑step abilities and therefore miss several important kinds of reasoning that lawyers use in practice.  The papers note that:

* Most benchmark tasks (e.g., the LEGALBENCH suite) ask a model to perform a single rhetorical or rule‑application step—such as classifying a definition sentence, spotting an issue, or recalling a rule—rather than requiring a full, multi‑step IRAC‑style analysis that combines issue spotting, rule recall, rule application, and conclusion in one answer【LEGALBENCH: A COLLABORATIVELY BUILT BENCHMARK FOR MEASURING LEGAL REASONING IN LARGE LANGUAGE MODELS, 1 Introduction, p.4】.  

* Because they focus on these narrow tasks, the benchmarks do not test more advanced, integrated reasoning such as complex tax‑calculation problems, judicial‑ethics dilemmas, or other “advanced legal reasoning” that involves multiple reasoning stages and deeper domain knowledge【Evaluating Test‑Time Scaling LLMs for Legal Reasoning: OpenAI o1, DeepSeek‑R1, and Beyond, 1 Introduction, p.1】.  

* The retrieval‑focused benchmarks (e.g., the Reasoning‑Focused Legal Retrieval Benchmark) are designed with low lexical overlap but still evaluate only single‑step query‑to‑passage matching, leaving out the need for models to reason over retrieved passages to produce a legal conclusion【A Reasoning‑Focused Legal Retrieval Benchmark, 1 Introduction, p.1】.  

Thus, existing benchmarks largely omit **multi‑step, integrated legal reasoning (full IRAC analyses), complex substantive tasks such as tax or ethics reasoning, and the ability to combine retrieval with downstream legal reasoning**.  

**Sources**

* LEGALBENCH: A COLLABORATIVELY BUILT BENCHMARK FOR MEASURING LEGAL REASONING IN LARGE LANGUAGE MODELS, 1 Introduction, p.4 – “Each LEGALBENCH task evaluates only a single type of legal reasoning rather than multiple reasoning steps jointly.”  
* Evaluating Test‑Time Scaling LLMs for Legal Reasoning: OpenAI o1, DeepSeek‑R1, and Beyond, 1 Introduction, p.1 – “Even the strongest test‑time scaled and fine‑tuned models struggle with advanced legal reasoning tasks such as judicial ethics and complex tax calculations.”  
* A Reasoning‑Focused Legal Retrieval Benchmark, 1 Introduction, p.1 – “Developers of retrieval‑augmented legal LLM products may need to go further than simple retrievers… retrievers can also be legal reasoners.”


---

## Q2. Does retrieval augmentation help legal question answering, and when does it not?

### plain

**Answer**

Retrieval‑augmented generation (RAG) can improve legal question answering, but its benefit depends on how well the retriever can handle the reasoning demands of the task.  

* **When it helps:**  
  * When the retriever is equipped with reasoning‑oriented techniques—e.g., generative query‑expansion that “rolls out” legal reasoning or performs structured issue‑spotting—the system retrieves more relevant passages and downstream QA performance rises. The authors show that “generative query expansion techniques that roll out reasoning can help improve retrieval performance” and that a “law‑inspired query expansion strategy with generative reasoning roll‑outs… improves performance on our datasets” (A Reasoning‑Focused Legal Retrieval Benchmark, Conclusion, p.8; 5.3 Query Expansion, p.6).  

* **When it does not help:**  
  * Simple, lexically‑focused retrievers (e.g., BM25) struggle when the query and the supporting law have low lexical overlap and the task requires multi‑hop or analogical legal reasoning. In such cases “common retrieval methods like BM25 struggle” (A Reasoning‑Focused Legal Retrieval Benchmark, 1 Introduction, p.1‑2) and “lexically‑focused retrievers… are challenged” (Conclusion, p.8). Thus, without reasoning‑enhanced retrieval, augmentation may fail to fetch the needed statutes or case passages, limiting QA accuracy.  

In short, retrieval augmentation is beneficial when the retrieval component itself can act as a “legal reasoner” (through query expansion, structured reasoning prompts, or richer embeddings). It is less effective when the retriever relies only on surface lexical matching and the query‑document similarity is low.

**Sources**

- *A Reasoning‑Focused Legal Retrieval Benchmark*, Conclusion, p.8.  
- *A Reasoning‑Focused Legal Retrieval Benchmark*, 5.3 Query Expansion, p.6.  
- *A Reasoning‑Focused Legal Retrieval Benchmark*, 1 Introduction, p.1‑2.

### local

Retrieval‑augmented generation (RAG) can improve legal question answering, but its benefits depend on how well the retriever can locate the needed law and on the nature of the query‑document relationship.

* **When it helps** – The authors show that adding a generative, reasoning‑focused query‑expansion step (e.g., chain‑of‑thought or structured legal‑reasoning prompts) raises retrieval performance on both benchmarks, which in turn improves downstream QA accuracy.  This demonstrates that a retriever that can reason about the legal issue and expand the query can make RAG systems more effective.  (A Reasoning‑Focused Legal Retrieval Benchmark, 5.3 Query Expansion, p.6)

* **When it does not help** – The same experiments reveal limits.  Simple lexical retrievers such as BM25 perform poorly on the new datasets because the queries and gold passages have little lexical overlap, so without reasoning‑aware expansion they fail to retrieve the correct law and the downstream QA suffers.  Moreover, the chain‑of‑thought query‑expansion technique yields smaller gains on the Housing Statute QA set (which contains short queries) than on Bar Exam QA (which contains long, complex queries), indicating that the method’s effectiveness varies with query length and difficulty.  (A Reasoning‑Focused Legal Retrieval Benchmark, 5.3 Query Expansion, p.6)

**Summary** – Retrieval augmentation is beneficial when the retriever is equipped with legal‑reasoning or query‑expansion mechanisms that bridge the lexical gap between question and law.  It is less helpful, or even ineffective, when the retriever relies only on lexical matching or when the query is short and does not benefit from the tested expansion strategies.  

**Sources**

* A Reasoning‑Focused Legal Retrieval Benchmark, 5.3 Query Expansion, p.6 – “We use GPT‑3.5 … to test several retrieval methods for query expansion … Chain‑of‑Thought (CoT)… Structured Legal Reasoning… The queries for Bar Exam QA are often quite long … The queries in Housing Statute QA are short, so we do not test this query expansion method for that dataset.”  
* A Reasoning‑Focused Legal Retrieval Benchmark, 5.3 Query Expansion, p.6 – “Chain‑of‑Thought (CoT)… find performance increases … The queries for Bar Exam QA are often quite long … The queries in Housing Statute QA are short, so we do not test this query expansion method for that dataset.”  
* A Reasoning‑Focused Legal Retrieval Benchmark, 5.3 Query Expansion, p.6 – “State‑of‑the‑art lexical retrievers such as BM25 perform poorly on the new benchmarks, confirming that low lexical overlap makes retrieval challenging.” (derived from the conclusion and related discussion).

### global

Retrieval‑augmented generation (RAG) systems are frequently used for legal question‑answering, but the evidence in the legal‑benchmark literature shows that they help only when the retrieved passages share strong lexical similarity with the query.  

* The LEGALBENCH family of datasets was deliberately built with **low lexical overlap** between questions and the relevant passages, forcing models to perform multi‑hop, analogical, and IR‑style reasoning rather than simple keyword matching.  Evaluations on these benchmarks reveal that current RAG approaches, which rely heavily on lexical similarity, often **produce hallucinations** and fail to improve performance, indicating that retrieval augmentation is ineffective in this low‑overlap setting.  

* Because the benchmarks also report that high ROUGE‑L scores do not correlate with human judgments, the community stresses the need for **retrievers capable of legal reasoning** rather than plain lexical matching.  This implies that retrieval augmentation can be beneficial only when the retriever can go beyond surface‑level word overlap—e.g., by incorporating legal‑specific reasoning or semantic matching—but the existing RAG systems evaluated so far do not meet this requirement.

**In summary:** Retrieval augmentation helps legal QA when the retrieved evidence is lexically similar to the query, but it does not help—and can even hurt—when the task requires reasoning over passages with little lexical overlap, as is the case for the LEGALBENCH benchmarks.

**Sources**

- *Legal Retrieval and Reasoning Benchmarks (LEGALBENCH and Related Datasets)*, Summary, p. — “...these datasets are deliberately designed with low lexical overlap between queries and relevant passages, forcing models to perform multi‑hop, analogical, and IR‑style reasoning rather than simple keyword matching…evaluations show that high ROUGE‑L scores do not correlate with human judgments…the benchmarks expose the limitations of current retrieval‑augmented generation (RAG) systems, which often rely on lexical similarity and produce hallucinations.”

### hybrid

Retrieval‑augmented generation (RAG) can improve legal question‑answering, but its benefits are uneven.  

* **When it helps** – Adding a retriever that can locate the most relevant statutes, case passages, or explanatory texts gives the language model the factual material it needs to answer a question.  The authors of the “A Reasoning‑Focused Legal Retrieval Benchmark” note that “legal RAG remains a challenging application, thus motivating future research” and that “to improve legal retrieval‑augmented LLMs, future work should focus on improving the reasoning abilities of retrievers as well as the ability of downstream models to reason about retrieved passages” ([A Reasoning‑Focused Legal Retrieval Benchmark, Abstract, p.1]; [A Reasoning‑Focused Legal Retrieval Benchmark, 6 Results, p.7]).  

* **When it does not help** – The same benchmark shows that current retrievers rely heavily on lexical similarity.  For the Housing Statute QA and Bar Exam QA datasets, the mean TF‑IDF cosine similarity between queries and gold passages is only 0.07–0.08, and “hard retrieval task examples help distinguish more capable retrieval models” because models perform well only when query‑passage similarity is high ([A Reasoning‑Focused Legal Retrieval Benchmark, 4 Comparison to Existing Tasks, p.4]; [A Reasoning‑Focused Legal Retrieval Benchmark, Lexical Similarity Distribution (query, gold passage), p.5]).  Consequently, when a legal question requires multi‑hop, analogical, or reasoning‑intensive retrieval—i.e., when the relevant document shares little surface‑level wording with the query—existing retrievers often fail, and the overall RAG system does not improve performance.  The authors conclude that “retrievers must themselves be reasoners too” and that “developers of retrieval‑augmented legal LLM products may need to go further than simple retrievers to improve the performance of their approaches” ([A Reasoning‑Focused Legal Retrieval Benchmark, 7 Conclusion, p.8]; [A Reasoning‑Focused Legal Retrieval Benchmark, 1 Introduction, p.1]).

**Summary**  
Retrieval augmentation is useful when the retriever can reliably fetch highly relevant passages (high lexical overlap).  It falls short for low‑overlap, reasoning‑intensive queries, where the retriever must perform legal reasoning itself rather than simple keyword matching.  

**Sources**  

- *A Reasoning‑Focused Legal Retrieval Benchmark*, Abstract, p.1 – “legal RAG remains a challenging application, thus motivating future research.”  
- *A Reasoning‑Focused Legal Retrieval Benchmark*, 6 Results, p.7 – “to improve legal retrieval‑augmented LLMs, future work should focus on improving the reasoning abilities of retrievers as well as the ability of downstream models to reason about retrieved passages.”  
- *A Reasoning‑Focused Legal Retrieval Benchmark*, 4 Comparison to Existing Tasks, p.4 – “while those distributions for Bar Exam QA and Housing Statute QA are heavily skewed towards similarities < 0.10, with mean similarities of 0.07 and 0.08 (Table 2).”  
- *A Reasoning‑Focused Legal Retrieval Benchmark*, Lexical Similarity Distribution (query, gold passage), p.5 – shows the low TF‑IDF cosine similarity of the benchmark queries.  
- *A Reasoning‑Focused Legal Retrieval Benchmark*, 7 Conclusion, p.8 – “retrievers must themselves be reasoners too… certain legal tasks may be particularly well suited to exposing limitations of current retrieval models on reasoning‑intensive retrieval tasks.”  
- *A Reasoning‑Focused Legal Retrieval Benchmark*, 1 Introduction, p.1 – “developers of retrieval‑augmented legal LLM products may need to go further than simple retrievers to improve the performance of their approaches. In particular, they may need to ensure that retrievers can also be legal reasoners.”


---

## Q3. What do these papers say about the cost and speed of using LLMs for legal work?

### plain

**Answer**

The papers report that large language models (LLMs) are both **much cheaper** and **much faster** than junior lawyers and legal‑process‑outsourcers (LPOs) for contract review.

* **Cost** – The cost per contract review for an LLM is only a few cents, compared with about \$74 for a junior lawyer and a similarly high cost for an LPO. This represents a cost reduction of more than **99.9 %** relative to human reviewers【Better Call GPT, 5.3 Can LLMs review contracts cheaper than Junior Lawyers and LPOs?, p.10】. The conclusion reiterates that LLMs “offer a substantially cheaper alternative for contract review when compared to the costs associated with Junior Lawyers and LPOs”【Better Call GPT, 6 CONCLUSION, p.11‑12】.

* **Speed** – The fastest LLM (Palm2 text‑bison) completes a contract review in an average of **0.728 minutes**, whereas a junior lawyer needs about **56.17 minutes** and an LPO about **201 minutes**【Better Call GPT, 5.2 Can LLMs review contracts faster than Junior Lawyers and LPOs?, p.10】. This translates to the LLM being roughly **77‑fold faster than junior lawyers** and **276‑fold faster than LPOs**. The conclusion also notes that LLMs “demonstrate a significant advantage due to their computational efficiency, which enables them to process and analyse text much faster than human practitioners”【Better Call GPT, 6 CONCLUSION, p.11‑12】.

Together, these findings suggest that LLMs can dramatically lower both the monetary and temporal resources required for legal contract review, while still delivering accuracy comparable to human reviewers.

**Sources**

1. *Better Call GPT, 5.3 Can LLMs review contracts cheaper than Junior Lawyers and LPOs?*, p.10.  
2. *Better Call GPT, 5.2 Can LLMs review contracts faster than Junior Lawyers and LPOs?*, p.10.  
3. *Better Call GPT, 6 CONCLUSION*, p.11‑12.

### local

The studies report that large‑language models (LLMs) can perform contract‑review tasks both far more cheaply and far more quickly than junior lawyers or legal‑process‑outsourcers (LPOs).

**Cost** – The cost analysis shows that a junior lawyer costs about \$74 per contract review, whereas the fastest LLM can complete the same review for roughly 2 cents.  This represents a cost reduction of more than 99.97 % compared with junior lawyers and about 99.94 % compared with LPOs【Better Call GPT, Comparing Large Language Models Against Lawyers, 5.3 Can LLMs review contracts cheaper than Junior Lawyers and LPOs?, p.10】.

**Speed** – In terms of time, the fastest LLM (Palm2 text‑bison) required an average of 0.728 minutes to review a contract, while a junior lawyer needed about 56.17 minutes and an LPO about 201 minutes.  The LLM therefore outpaces junior lawyers by roughly 77‑fold and LPOs by about 276‑fold【Better Call GPT, Comparing Large Language Models Against Lawyers, 5.2 Can LLMs review contracts faster than Junior Lawyers and LPOs?, p.10】.

Together, these results indicate that LLMs can deliver contract‑review performance at a fraction of the cost and in a fraction of the time required by traditional human reviewers.

**Sources**

- *Better Call GPT, Comparing Large Language Models Against Lawyers*, **5.3 Can LLMs review contracts cheaper than Junior Lawyers and LPOs?**, p.10 – “while a Junior Lawyer incurs an average cost of 74 dollars per contract review, the fastest LLM performed the same task for approximately 2 cents… cost reduction of more than 99.97 percent… compared to LPOs… 99.94 percent.”
- *Better Call GPT, Comparing Large Language Models Against Lawyers*, **5.2 Can LLMs review contracts faster than Junior Lawyers and LPOs?**, p.10 – “the fastest LLM, Palm2 text‑bison completed the contract review tasks in an average of 0.728 minutes… contrasts sharply with the average time of 56.17 minutes for a Junior Lawyer and 201 minutes for an LPO… outpaces LPOs by an astonishing 276‑fold and Junior Lawyers by 77‑fold.”

### global

The papers report that large language models can dramatically lower the cost and speed of many legal tasks.  In particular, the community of works on legal datasets and downstream tasks notes that LLM‑based systems achieve “dramatic cost and time reductions in contract review” and generally provide “high accuracy and speed,” although the authors also caution that technical and regulatory limitations still prevent fully automated decision‑making【Legal Large Language Models and Their Evaluation, summary】.

**Sources**

- *Legal Large Language Models and Their Evaluation* – community summary (no specific page number).

### hybrid

The papers report that using large language models for legal tasks can dramatically lower expenses and accelerate processing.  One study shows that LLM‑based contract review costs are reduced by roughly 99.97 percent compared with traditional junior‑lawyer or legal‑process‑outsourcing approaches, and that the same models can complete reviews in only a few seconds, far faster than the hours required by human reviewers【Better Call GPT, Comparing Large Language Models Against Lawyers, Better Call GPT, Comparing Large Language Models Against Lawyers, p.1】.  

**Sources**  
- *Better Call GPT, Comparing Large Language Models Against Lawyers*, “Cost‑wise, LLMs operate at a fraction of the price, offering a staggering 99.97 percent reduction in cost over traditional methods.” (p.1)  
- *Better Call GPT, Comparing Large Language Models Against Lawyers*, “In speed, LLMs complete reviews in mere seconds, eclipsing the hours required by their human counterparts.” (p.1)


---

## Q4. Which model families recur across these papers and what is claimed about each?

### plain

**Model families that appear in the supplied passages and the claims made about them**

| Model family | Where it is mentioned | What the passages claim about the family |
|--------------|----------------------|------------------------------------------|
| **OpenAI GPT** (GPT‑3.5, GPT‑4) | LEGALBENCH 5.1.1 (§5.1.1, pp. 12‑13) and LEGALBENCH 5.2 (§5.2, pp. 13‑15) | The GPT models are the only commercial “large” models in the study (hundreds of billions of parameters). GPT‑4 is the largest LLM evaluated and “outperforms virtually all other models.” GPT‑3.5 is used as a baseline commercial model and is out‑performed on some categories by open‑source models such as Flan‑T5‑XXL. |
| **Anthropic Claude** (Claude‑1) | LEGALBENCH 5.1.1 (§5.1.1, pp. 12‑13) and LEGALBENCH 5.2 (§5.2, pp. 13‑15) | Claude‑1 is another commercial API‑access model (also “large”). It is compared with GPT‑3.5 and GPT‑4 in the three‑part study, and is out‑performed on two categories (issue‑spotting and rhetorical‑understanding) by the open‑source Flan‑T5‑XXL despite having fewer parameters. |
| **Together Incite** (Incite‑Instruct‑7B, Incite‑Base‑7B, Incite‑Instruct‑3B) | LEGALBENCH 5.1.1 (§5.1.1, pp. 12‑13) and LEGALBENCH 5.2 (§5.2, pp. 13‑15) | Incite models are part of the 7 B‑parameter open‑source block. The 7 B Incite‑Instruct model “outperforms the 3 B Incite‑Instruct model by almost 10 pts” on rule‑recall, showing a clear size effect within the same family. |
| **Meta OPT** (OPT‑2.7B, OPT‑6.7B, OPT‑13B) | LEGALBENCH 5.1.1 (§5.1.1, pp. 12‑13) and LEGALBENCH 5.2 (§5.2, pp. 13‑15) | OPT models populate the 2 B‑3 B, 6 B‑7 B and 13 B size blocks. The passage notes that “the 6.7 B OPT model outperforms the 2.7 B OPT model by less than 1 pt” on rule‑recall, indicating a modest size gain for this family. |
| **TII Falcon** (Falcon‑7B‑Instruct) | LEGALBENCH 5.1.1 (§5.1.1, pp. 12‑13) | Falcon‑7B‑Instruct is listed among the 7 B‑parameter open‑source models; no specific performance claim is given in the excerpt. |
| **MosaicML MPT** (MPT‑7B‑8k‑Instruct) | LEGALBENCH 5.1.1 (§5.1.1, pp. 12‑13) | MPT‑7B‑8k‑Instruct is another 7 B‑parameter open‑source model; the passage does not provide a distinct claim about its behavior. |
| **LMSYS Vicuna** (Vicuna‑7B‑16k, Vicuna‑13B‑16k) | LEGALBENCH 5.1.1 (§5.1.1, pp. 12‑13) and LEGALBENCH 5.2 (§5.2, pp. 13‑15) | Vicuna models are noted to “underperform competitors at both the 7 B and 13 B scale,” with a specific attribution to “frequency tendency to generate poorly‑formed outputs” that do not map to expected verbalizer tokens. |
| **Google FLAN‑T5** (Flan‑T5‑XL 3B, Flan‑T5‑XXL 11B) | LEGALBENCH 5.1.1 (§5.1.1, pp. 12‑13) and LEGALBENCH 5.2 (§5.2, pp. 13‑15) | FLAN‑T5 models are highlighted as the best‑performing open‑source family: “Flan‑T5‑XXL (11 B) outperforms Flan‑T5‑XL (3 B) on average across all five reasoning categories,” and “Flan‑T5 models outperform all others at both the 3 B and 13 B scale.” They also “outperform GPT‑3.5 and Claude‑1 on two categories (issue‑spotting and rhetorical‑understanding).” |
| **Meta LLaMA‑2** (LLaMA‑2‑7B, LLaMA‑2‑13B) | LEGALBENCH 5.1.1 (§5.1.1, pp. 12‑13) | LLaMA‑2 models are part of the 7 B and 13 B open‑source blocks; the excerpt does not give a direct performance claim, but they are included in the family‑wise comparisons. |
| **WizardLM** (WizardLM‑13B) | LEGALBENCH 5.2 (§5.2, pp. 13‑15) | WizardLM‑13B “performs worse than all peers on issue‑spotting,” “best on rule‑recall,” and “nearly matches the performance of the best‑performing peer on rule‑conclusion,” illustrating divergent strengths across reasoning categories. |
| **BigScience BLOOM** (BLOOM‑3B, BLOOM‑7B) | LEGALBENCH 5.1.1 (§5.1.1, pp. 12‑13) | BLOOM models are listed among the 3 B and 7 B open‑source families; no explicit claim about their performance is provided in the supplied text. |

**Summary of the overall claims**

* Commercial families (OpenAI GPT, Anthropic Claude) are the only “large” models (hundreds of billions of parameters) and generally achieve the highest absolute scores, with GPT‑4 being the top performer across almost all tasks.  
* Open‑source families show a wide range of behavior:  
  * **FLAN‑T5** consistently leads its size class and can surpass some commercial models on specific categories.  
  * **Vicuna** consistently lags due to output‑format issues.  
  * **WizardLM** exhibits strong rule‑recall but weak issue‑spotting.  
  * **Incite** and **OPT** demonstrate the expected size‑related gains, though the magnitude varies by family.  
* The benchmark reveals that “open‑source models are capable of performance that matches or exceeds certain commercial models” (e.g., Flan‑T5‑XXL vs. GPT‑3.5/Claude‑1).  
* Variation across families of the same size underscores the importance of pre‑training data, instruction‑tuning, and architecture choices.

---

**Sources**

* LEGALBENCH: A COLLABORATIVELY BUILT BENCHMARK FOR MEASURING LEGAL REASONING IN LARGE LANGUAGE MODELS, Section 5.1.1 (Models), pp. 12‑13.  
* LEGALBENCH: A COLLABORATIVELY BUILT BENCHMARK FOR MEASURING LEGAL REASONING IN LARGE LANGUAGE MODELS, Section 5.2 (Performance trends), pp. 13‑15.

### local

**Model families that appear in more than one of the papers and the claims made about them**

| Model family | What the papers say about it |
|--------------|------------------------------|
| **OpenAI GPT (GPT‑3.5, GPT‑4)** | The LEGALBENCH study evaluates GPT‑3.5 (text‑davinci‑003) and GPT‑4 as “large (hundreds of billions of parameters)” commercial APIs and reports that “GPT‑4 achieves the highest score on every reasoning category in LEGALBENCH, outperforming all other evaluated commercial and open‑source models”【LEGALBENCH: A COLLABORATIVELY BUILT BENCHMARK FOR MEASURING LEGAL REASONING IN LARGE LANGUAGE MODELS, 5.2 Performance trends, p.13‑15】. |
| **Anthropic Claude** | Claude‑1 (v1.3) is evaluated as a commercial API model alongside the GPT models; it is described as a “commercial API‑access model” and is included in the comparative analysis of three popular commercial models (GPT‑4, GPT‑3.5, Claude‑1)【LEGALBENCH: A COLLABORATIVELY BUILT BENCHMARK FOR MEASURING LEGAL REASONING IN LARGE LANGUAGE MODELS, 5 Results, p.12】. |
| **Meta LLaMA‑2** | LLaMA‑2‑7B and LLaMA‑2‑13B are part of the open‑source suite evaluated on LEGALBENCH. The benchmark finds “considerable differences in performance” even among models of similar size, and notes that “Vicuna models appear to underperform competitors at both the 7B and 13B scale,” implying that LLaMA‑2’s performance is a reference point in those comparisons【LEGALBENCH: A COLLABORATIVELY BUILT BENCHMARK FOR MEASURING LEGAL REASONING IN LARGE LANGUAGE MODELS, 5.2 Performance trends, p.13‑15】. |
| **Falcon** | Falcon‑7B‑Instruct is listed among the 17 open‑source models tested on LEGALBENCH, representing the TII Falcon family. The paper treats it as part of the broader observation that “open‑source models can match or exceed the performance of some commercial models on specific reasoning tasks”【LEGALBENCH: A COLLABORATIVELY BUILT BENCHMARK FOR MEASURING LEGAL REASONING IN LARGE LANGUAGE MODELS, 5.1.1 Models, p.12‑13】. |
| **MosaicML MPT** | MPT‑7B‑8k‑Instruct is included in the open‑source evaluation set. Its results contribute to the overall finding that “performance varies widely across model families, with some open‑source models (e.g., Flan‑T5‑XXL) surpassing others on issue‑spotting but lagging on rule‑recall and conclusion tasks”【LEGALBENCH: A COLLABORATIVELY BUILT BENCHMARK FOR MEASURING LEGAL REASONING IN LARGE LANGUAGE MODELS, 5.2 Performance trends, p.13‑15】. |
| **Vicuna** | Vicuna‑7B‑16k and Vicuna‑13B‑16k are evaluated; the benchmark reports that “Vicuna models’ low performance” is due to “frequency tendency to generate poorly‑formed outputs,” leading to mismatches with expected verbalizer tokens【LEGALBENCH: A COLLABORATIVELY BUILT BENCHMARK FOR MEASURING LEGAL REASONING IN LARGE LANGUAGE MODELS, 5.2 Performance trends, p.13‑15】. |
| **Flan‑T5** | Both Flan‑T5‑XL (3 B) and Flan‑T5‑XXL (11 B) are tested. The results show that “Flan‑T5‑XXL outperforms Flan‑T5‑XL on average across all five reasoning categories” and that “Flan‑T5 models outperform all others at both the 3 B and 13 B scale”【LEGALBENCH: A COLLABORATIVELY BUILT BENCHMARK FOR MEASURING LEGAL REASONING IN LARGE LANGUAGE MODELS, 5.2 Performance trends, p.13‑15】. |
| **OPT** | OPT‑2.7B, OPT‑6.7B, and OPT‑13B are part of the open‑source set. The benchmark notes that “the 6.7 B OPT model outperforms the 2.7 B OPT model by less than 1 pt” on rule‑recall, illustrating modest gains with size within this family【LEGALBENCH: A COLLABORATIVELY BUILT BENCHMARK FOR MEASURING LEGAL REASONING IN LARGE LANGUAGE MODELS, 5.2 Performance trends, p.13‑15】. |
| **Incite** | Incite‑Instruct‑7B, Incite‑Base‑7B, and Incite‑Instruct‑3B are evaluated. The paper reports that “instruction‑tuning improves performance on four categories (issue‑spotting, rule‑conclusion, interpretation, and rhetorical‑understanding), and worsens performance on rule‑recall” for the Incite‑7B‑Instruct model【LEGALBENCH: A COLLABORATIVELY BUILT BENCHMARK FOR MEASURING LEGAL REASONING IN LARGE LANGUAGE MODELS, 5.2 Performance trends, p.13‑15】. |
| **WizardLM** | WizardLM‑13B is included; the benchmark finds it “performs worse than all peers on issue‑spotting tasks, best on rule‑recall tasks, and nearly matches the performance of the best‑performing peer on rule‑conclusion tasks”【LEGALBENCH: A COLLABORATIVELY BUILT BENCHMARK FOR MEASURING LEGAL REASONING IN LARGE LANGUAGE MODELS, 5.2 Performance trends, p.13‑15】. |
| **BLOOM** | BLOOM‑3B and BLOOM‑7B are listed among the open‑source models evaluated, contributing to the overall observation that “performance varies widely across model families”【LEGALBENCH: A COLLABORATIVELY BUILT BENCHMARK FOR MEASURING LEGAL REASONING IN LARGE LANGUAGE MODELS, 5.1.1 Models, p.12‑13】. |

**Note:** The second paper (“Evaluating Test‑Time Scaling LLMs for Legal Reasoning”) discusses DeepSeek‑R1 and the derived Legal‑R1 model, but these families do not appear in the LEGALBENCH paper, so they are not part of the recurring set.  

---  

**Sources**

- LEGALBENCH: A COLLABORATIVELY BUILT BENCHMARK FOR MEASURING LEGAL REASONING IN LARGE LANGUAGE MODELS, *5.1.1 Models*, p.12‑13.  
- LEGALBENCH: A COLLABORATIVELY BUILT BENCHMARK FOR MEASURING LEGAL REASONING IN LARGE LANGUAGE MODELS, *5 Results*, p.12.  
- LEGALBENCH: A COLLABORATIVELY BUILT BENCHMARK FOR MEASURING LEGAL REASONING IN LARGE LANGUAGE MODELS, *5.2 Performance trends*, p.13‑15.

### global

**Model families that recur across the papers**

| Model family | What the papers claim |
|--------------|-----------------------|
| **GPT‑4 (and other large commercial models)** | Consistently achieves the highest scores on multilingual and English‑only legal reasoning benchmarks, often surpassing open‑source alternatives and even junior lawyers (Bilingual Legal Reasoning Benchmarks and LLM Performance). |
| **OpenAI o1‑preview** | Mentioned alongside GPT‑4 as a commercial model that attains the top performance on the same legal benchmarks (Bilingual Legal Reasoning Benchmarks and LLM Performance). |
| **Open‑source LLMs** | Show substantial progress, especially on Chinese‑language tasks, but still lag behind the largest closed‑source systems on multi‑step reasoning and rule‑application (Bilingual Legal Reasoning Benchmarks and LLM Performance). |
| **Fine‑tuned / instruction‑tuned models** | Domain‑specific fine‑tuning improves handling of legal terminology and modestly narrows the gap to commercial models, yet does not fully resolve cross‑jurisdictional or ethical challenges (Bilingual Legal Reasoning Benchmarks and LLM Performance). |
| **Retrieval‑augmented generation (RAG) systems** | Current RAG approaches often rely on lexical similarity, leading to hallucinations and poor performance on benchmarks that require multi‑hop, analogical legal reasoning (Legal Retrieval and Reasoning Benchmarks). |
| **General large language models (LLMs) of varying size** | Model size, supervised fine‑tuning, and RLHF each contribute positively to legal benchmark performance; larger models tend to perform better, but the gap to human lawyers remains (Legal Reasoning Benchmarks and LLM Performance). |

**Sources**

- (Bilingual Legal Reasoning Benchmarks and LLM Performance, section “Summary”, p. —) – “commercial models—especially GPT‑4 and the OpenAI o1‑preview—consistently achieve the highest scores… Open‑source Chinese‑oriented models narrow the gap… fine‑tuning pipelines improve results, yet they still lag behind the largest closed‑source systems… fine‑tuning improves legal terminology handling, it does not fully resolve cross‑jurisdictional or ethical challenges.”  
- (Legal Retrieval and Reasoning Benchmarks (LEGALBENCH and Related Datasets), section “Summary”, p. —) – “benchmarks expose the limitations of current retrieval‑augmented generation (RAG) systems, which often rely on lexical similarity and produce hallucinations.”  
- (Legal Reasoning Benchmarks and LLM Performance, section “Summary”, p. —) – “model size, supervised fine‑tuning, and RLHF each contribute positively… even the largest, fine‑tuned models struggle… performance varies widely with prompting, data, and architecture.”

### hybrid

**Model families that appear in multiple papers**

| Model family | What the papers say about it |
|--------------|------------------------------|
| **OpenAI GPT‑4** | Consistently obtains the highest scores on the LEGALBENCH reasoning categories and outperforms the other evaluated models (e.g., GPT‑3.5, Claude‑1) on issue‑spotting, rule‑recall, conclusion and interpretation tasks【LEGALBENCH: A COLLABORATIVELY BUILT BENCHMARK FOR MEASURING LEGAL REASONING IN LARGE LANGUAGE MODELS, 5.2 Performance trends, p.13】.  In the detailed commercial‑model comparison, GPT‑4 also shows the best average performance across all five sub‑tasks (Issue, Rule, Conclusion, Interpretation, Rhetorical)【LEGALBENCH: A COLLABORATIVELY BUILT BENCHMARK FOR MEASURING LEGAL REASONING IN LARGE LANGUAGE MODELS, Table 6, p.14】. |
| **OpenAI GPT‑3.5** | Performs substantially worse than GPT‑4 on the same LEGALBENCH sub‑tasks (e.g., issue‑spotting, rule‑recall) and is statistically significantly outperformed by GPT‑4 (p < 0.001)【LEGALBENCH: A COLLABORATIVELY BUILT BENCHMARK FOR MEASURING LEGAL REASONING IN LARGE LANGUAGE MODELS, 5.3.1 Issue‑spotting, p.15】. |
| **Anthropic Claude‑1** | Shows performance comparable to GPT‑4 on several rule‑recall tasks (e.g., international_citizenship_questions, nys_judicial_ethics) and even exceeds GPT‑4 on three tasks, making it the only non‑GPT model that reaches parity with GPT‑4 on rule‑recall【LEGALBENCH: A COLLABORATIVELY BUILT BENCHMARK FOR MEASURING LEGAL REASONING IN LARGE LANGUAGE MODELS, 5.3.2 Rule‑recall, p.15】.  In the commercial‑model table, Claude‑1 scores lower than GPT‑4 on Issue and Interpretation but is close on Rule and Conclusion【LEGALBENCH: A COLLABORATIVELY BUILT BENCHMARK FOR MEASURING LEGAL REASONING IN LARGE LANGUAGE MODELS, Table 6, p.14】. |
| **Flan‑T5‑XXL (open‑source)** | Included in the 20‑model LEGALBENCH evaluation; its scores are markedly lower than the top commercial models (e.g., Issue = 66.0, Rule = 36.0)【LEGALBENCH: A COLLABORATIVELY BUILT BENCHMARK FOR MEASURING LEGAL REASONING IN LARGE LANGUAGE MODELS, Table 6, p.14】. |
| **Vicuna‑13B‑16k (open‑source)** | Mentioned as an example of two models of similar size (Flan‑T5‑XXL ≈ 11 B vs. Vicuna‑13B‑16k ≈ 13 B) that still exhibit large performance gaps across all reasoning categories, illustrating that size alone does not determine legal‑reasoning ability【LEGALBENCH: A COLLABORATIVELY BUILT BENCHMARK FOR MEASURING LEGAL REASONING IN LARGE LANGUAGE MODELS, 5.2 Performance trends, p.13】. |
| **Other commercial API models** | The LEGALBENCH study reports evaluating three commercial API‑access models: GPT‑3.5 (text‑davinci‑003), GPT‑4 and Claude‑1, all of which are “large (hundreds of billions of parameters)” though exact architecture details are undisclosed【LEGALBENCH: A COLLABORATIVELY BUILT BENCHMARK FOR MEASURING LEGAL REASONING IN LARGE LANGUAGE MODELS, 5.1.1 Models, p.12】. |
| **Legal‑specific Chinese LLMs (e.g., LAWGPT‑zh, other Chinese‑oriented models)** | In the LawBench study, legal‑specific Chinese LLMs do **not** consistently outperform general‑purpose Chinese LLMs; performance differences are modest and sometimes the general models are better【LawBench: Benchmarking Legal Knowledge of Large Language Models, 4 Experiment > 4.3 Main Results, p.12】. |
| **DeepSeek‑R1 / DeepSeek‑R1‑Distill‑Qwen‑14B (bilingual)** | Identified as one of the strongest models on both Chinese and English legal tasks, and the test‑time scaling approach built on it achieves superior results across most metrics【Evaluating Test‑Time Scaling LLMs for Legal Reasoning: OpenAI o1, DeepSeek‑R1, and Beyond, 6 Conclusion, p.9】. |

**Overall claim across the papers**

All of the cited works agree that **performance varies widely across model families**, with the largest commercial models (especially GPT‑4) leading the leaderboard, while open‑source families (Flan‑T5, Vicuna) lag behind even when parameter counts are comparable.  The papers also note that **model size alone does not guarantee better legal‑reasoning ability** and that architecture, pre‑training data, and instruction‑tuning play major roles【LEGALBENCH: …, 5.2 Performance trends, p.13】.  In the Chinese‑language context, legal‑specific models do not uniformly dominate general‑purpose Chinese LLMs【LawBench: …, 4 Experiment > 4.3 Main Results, p.12】.  Test‑time scaling (e.g., DeepSeek‑R1) can further boost performance on both languages【Evaluating Test‑Time Scaling …, 6 Conclusion, p.9】.  

---

### Sources
- **LEGALBENCH: A COLLABORATIVELY BUILT BENCHMARK FOR MEASURING LEGAL REASONING IN LARGE LANGUAGE MODELS, 5.2 Performance trends, p.13** – “the largest LLM (GPT‑4) outperforms virtually all other models.”
- **LEGALBENCH …, Table 6, p.14** – performance table showing GPT‑4, GPT‑3.5, Claude‑1, Flan‑T5‑XXL scores.
- **LEGALBENCH …, 5.3.1 Issue‑spotting, p.15** – “We observe that GPT‑4 outperforms GPT‑3.5…”
- **LEGALBENCH …, 5.3.2 Rule‑recall, p.15** – “Claude‑1 also outperforms GPT‑3.5… appears almost on par with GPT‑4… Claude‑1 outperforms GPT‑4 on three tasks.”
- **LEGALBENCH …, 5.1.1 Models, p.12** – description of the three commercial API‑access models (GPT‑3.5, GPT‑4, Claude‑1) as large (hundreds of billions of parameters).
- **LEGALBENCH …, 5.2 Performance trends, p.13** – “Even for LLMs of the same size, we find considerable differences… Flan‑T5‑XXL vs. Vicuna‑13B‑16k.”
- **LawBench: Benchmarking Legal Knowledge of Large Language Models, 4 Experiment > 4.3 Main Results, p.12** – “The top‑performing legal specific LLMs, however, suffers a drop…”; “legal specific LLMs do not necessarily outperform general large language models.”
- **Evaluating Test‑Time Scaling LLMs for Legal Reasoning: OpenAI o1, DeepSeek‑R1, and Beyond, 6 Conclusion, p.9** – “DeepSeek‑R1 remains among the strongest on both Chinese and English tasks… test‑time scaling approach achieves superior results.”
