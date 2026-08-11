# Retrieval comparison — 2026-08-11 18:59

Model `openai/gpt-oss-120b`, embeddings `openai/text-embedding-3-small`, top_k=5.

- **plain** — nearest chunks only, no graph. The control.
- **local** — nearest chunks, plus the claims each one grounds.
- **global** — community summaries only.
- **hybrid** — community summaries, plus each theme's claims and the verbatim passage behind them.


---

## Q1. Do the papers agree on whether fine-tuning LLMs on legal text is worthwhile?

### plain

The papers do not give a single, unequivocal verdict that fine‑tuning LLMs on legal text is either wholly worthwhile or not.  

* **LawBench** notes that “fine‑tuning LLMs on legal specific text brings certain improvements, we are still a long way from obtaining usable and reliable LLMs in legal tasks” (LawBench: Benchmarking Legal Knowledge of Large Language Models, Abstract, p.1). This acknowledges that fine‑tuning helps performance, but the gains are limited and the models remain insufficient for dependable legal work.  

* **Legal Evaluations and Challenges of Large Language Models** does not discuss fine‑tuning directly; instead it stresses the need for “improvements in training methodologies—particularly in integrating domain‑specific legal knowledge and strengthening reasoning capabilities” (Legal Evaluations and Challenges of Large Language Models, VI. DISCUSSION, p.8). While this implies that better‑targeted training (which could include fine‑tuning) would be beneficial, the paper does not explicitly evaluate fine‑tuning as a worthwhile step.  

Thus, the two papers are consistent in recognizing that more domain‑specific training (including fine‑tuning) could improve legal performance, but they also agree that current fine‑tuned models are still far from reliable for real‑world legal tasks. Neither paper declares fine‑tuning to be definitively worthwhile on its own; they both suggest it is a necessary but insufficient improvement.

**Sources**

- LawBench: Benchmarking Legal Knowledge of Large Language Models, Abstract, p.1.  
- Legal Evaluations and Challenges of Large Language Models, VI. DISCUSSION, p.8.

### local

The papers that discuss fine‑tuning LLMs on legal text do not present a unanimous endorsement. LawBench reports that fine‑tuning open‑source models on legal‑specific corpora yields only modest gains and that even after such adaptation the models remain far behind the strongest systems (e.g., GPT‑4) and are not yet reliable for practical legal tasks. No other paper in the provided context offers a contrasting claim about the value of fine‑tuning, so the available evidence suggests that while fine‑tuning can improve performance, the benefit is limited and does not make the models fully usable for legal applications.

**Sources**

- *LawBench: Benchmarking Legal Knowledge of Large Language Models*, **Abstract**, p.1: “While fine‑tuning LLMs on legal specific text brings certain improvements, we are still a long way from obtaining usable and reliable LLMs in legal tasks.”

### global

The papers do not disagree: the literature that discusses legal‑reasoning benchmarks consistently reports that supervised fine‑tuning on legal text improves performance.  Across the surveyed works, fine‑tuning (including domain‑specific instruction tuning and reinforcement‑learning‑from‑human‑feedback) is cited as one of the positive contributors to higher scores on tasks such as statute classification, contract question answering, and multi‑step legal reasoning.  No paper in the set presents evidence that fine‑tuning on legal material is detrimental or unnecessary; instead, the consensus is that it is a worthwhile step for closing the gap between LLMs and human lawyers.

**Sources**

- The “Legal Reasoning Benchmarks and LLM Performance” theme notes that “model size, supervised fine‑tuning, and RLHF each contribute positively” to benchmark results.  
- The “Legal Large Language Models and Their Evaluation” theme highlights “the need for better domain‑specific training” to address systematic shortcomings of LLMs on legal tasks.  
- The “Bilingual Legal Reasoning Benchmarks and LLM Performance” theme reports that “fine‑tuning improves legal terminology handling” and that “progressive fine‑tuning pipelines improve results.”  
- The “Legal Reasoning Benchmarks for Large Language Models” theme describes benchmarks that “guide future research on … fine‑grained way to compare LLMs to lawyers,” implying that fine‑tuning is a key lever for improvement.

### hybrid

The papers do not reach a single, unanimous conclusion that fine‑tuning on legal text is always worthwhile.  

* Several works report that domain‑specific fine‑tuning does improve a model’s handling of legal terminology and can raise performance on many downstream legal tasks. For example, the authors of the test‑time‑scaling study note that a progressive supervised‑fine‑tuning pipeline that first trains on legal‑judgment prediction “provides a strong foundation for subsequent fine‑tuning on a broader set of bilingual legal reasoning tasks” (Evaluating Test‑Time Scaling LLMs for Legal Reasoning: OpenAI o1, DeepSeek‑R1, and Beyond, 4.2 Training, p.4). Likewise, the LEGALBENCH paper observes that “tailoring LLMs to the legal domain (e.g., fine‑tuning on legal corpora) improves terminology understanding” (Legal Evalutions and Challenges of Large Language Models, VI. DISCUSSION, p.8).  

* At the same time, other studies point out that fine‑tuning on legal data does not automatically make a model superior to strong general‑purpose models. The LawBench paper finds that “legal‑specific LLMs do not necessarily outperform general‑purpose Chinese‑oriented LLMs” (LawBench: Benchmarking Legal Knowledge of Large Language Models, 4.3 Main Results, p.12) and that “the current legal‑specific LLMs do not necessarily outperform general large language models” (LawBench: Benchmarking Legal Knowledge of Large Language Models, 4.4 Analysis, p.13). Moreover, the LEGALBENCH performance trends note that “even for LLMs of the same size, we find considerable differences in performance” across model families, suggesting that fine‑tuning alone cannot guarantee better results (LEGALBENCH, 5.2 Performance trends, p.13).  

* Finally, the LEGALBENCH prompt‑engineering study highlights that while fine‑tuned models can be steered with better prompts, “the gap between model capabilities and the nuanced reasoning lawyers expect” remains, indicating that fine‑tuning is only part of the solution (LEGALBENCH, 5.4 Prompt engineering strategies, p.18).  

**Thus, the literature agrees that fine‑tuning on legal text can be beneficial for certain aspects (e.g., terminology, some downstream tasks), but the papers also caution that it does not guarantee overall superiority and that other factors—model architecture, size, prompting, and training data—play crucial roles.**  

**Sources**

* Evaluating Test‑Time Scaling LLMs for Legal Reasoning: OpenAI o1, DeepSeek‑R1, and Beyond, 4.2 Training, p.4 – “progressive supervised fine‑tuning … provides a strong foundation …”  
* Legal Evalutions and Challenges of Large Language Models, VI. DISCUSSION, p.8 – “tailoring LLMs … improves terminology understanding”  
* LawBench: Benchmarking Legal Knowledge of Large Language Models, 4.3 Main Results, p.12 – “legal‑specific LLMs do not necessarily outperform general‑purpose Chinese‑oriented LLMs.”  
* LawBench: Benchmarking Legal Knowledge of Large Language Models, 4.4 Analysis, p.13 – “the current legal specific LLMs do not necessarily outperform general large language models.”  
* LEGALBENCH: A COLLABORATIVELY BUILT BENCHMARK FOR MEASURING LEGAL REASONING IN LARGE LANGUAGE MODELS, 5.2 Performance trends, p.13 – “Even for LLMs of the same size, we find considerable differences in performance.”  
* LEGALBENCH: A COLLABORATIVELY BUILT BENCHMARK FOR MEASURING LEGAL REASONING IN LARGE LANGUAGE MODELS, 5.4 Prompt engineering strategies, p.18 – “the gap between model capabilities and the nuanced reasoning lawyers expect” remains.


---

## Q2. How should legal LLM outputs be evaluated, and what is wrong with current metrics?

### plain

**Answer**

Legal‑LLM outputs should be judged with **task‑specific, multi‑dimensional metrics that reflect the three cognitive levels of legal work** – memorization, understanding, and application – rather than relying on a single generic score such as raw accuracy.  A proper evaluation framework therefore:

1. **Matches the legal task type** (e.g., classification, extraction, generation, judgment prediction) and uses the metric that best captures performance for that type (accuracy for multiple‑choice, F1 for extraction/labeling, Rouge‑L for article recitation, etc.)【A.1 Chinese Legal Tasks, p.12‑14】.  
2. **Measures both factual recall and reasoning**.  For memorization‑oriented tasks (e.g., Article Recitation) Rouge‑L is used to assess how well the model reproduces statutory text, while for understanding‑or‑applying tasks (e.g., Legal Judgment Prediction, Multi‑segment Reading Comprehension) precision/recall/F1 or semantic‑similarity‑based F1 are required to capture correct identification of charges, articles, or sentence lengths【A.1 Chinese Legal Tasks, p.12‑14】.  
3. **Aggregates results across the three cognitive dimensions** defined in LawBench, providing a structured overview of a model’s strengths and weaknesses rather than a single overall number【LawBench – Abstract, p.1】.  
4. **Considers the legal system context** (civil‑law vs. common‑law) and uses benchmarks that are built for that jurisdiction, because the knowledge and reasoning required differ substantially【LawBench – Introduction, p.1‑3】.  

**What is wrong with many current metrics**

* **Over‑reliance on a single scalar (e.g., accuracy)** – many legal tasks are multi‑label, hierarchical, or require generation of free‑form text, so accuracy alone cannot capture partial correctness or the quality of reasoning【A.1 Chinese Legal Tasks, p.12‑14】.  
* **Neglect of domain‑specific reasoning** – generic benchmarks (e.g., MMLU, BIG‑bench) focus on world knowledge and general reasoning, but they do not test the ability to apply statutes, interpret legal relationships, or perform multi‑step legal calculations that are essential in practice【LawBench – Introduction, p.1‑3】.  
* **Missing fine‑grained error analysis** – reporting only an overall score hides systematic failures such as the inability to locate issues within contracts, which can be critical for real‑world deployment (e.g., GPT‑4‑1106’s lower F‑score on issue location despite good issue‑determination performance)【Better Call GPT, p.9‑10】.  
* **Lack of alignment with real‑world use cases** – many evaluations treat legal LLMs like exam‑taking bots (e.g., bar‑exam style tests) that do not reflect the structured, multi‑step tasks lawyers actually perform, leading to an over‑optimistic view of “usable” performance【LawBench – Introduction, p.1‑3】.  

In short, legal LLMs need **task‑aligned, multi‑metric evaluation suites that respect the specific cognitive demands and jurisdictional nuances of legal work**, and current practice often falls short by using overly simplistic, one‑dimensional metrics that miss critical aspects of legal reasoning and applicability.  

---

**Sources**

- *LawBench: Benchmarking Legal Knowledge of Large Language Models*, Abstract, p.1.  
- *LawBench: Benchmarking Legal Knowledge of Large Language Models*, Introduction, p.1‑3.  
- *Evaluating Test‑Time Scaling LLMs for Legal Reasoning: OpenAI o1, DeepSeek‑R1, and Beyond*, A.1 Chinese Legal Tasks, p.12‑14.  
- *Better Call GPT, Comparing Large Language Models Against Lawyers*, 5.1 Do LLMs outperform Junior Lawyers and LPOs in determination and location of legal issues in contracts?, p.9‑10.

### local

The provided passages describe a variety of evaluation tasks and metrics that have been used for legal language models—such as accuracy for multiple‑choice questions, normalized log‑distance for prison‑term prediction, F0.5 for document‑proofreading, and Rouge‑L for article recitation. However, none of the excerpts discuss how legal LLM outputs should be evaluated in a principled way or point out specific shortcomings of these current metrics. Consequently, the question cannot be answered with the information given.  

**Sources**  
- The passages list the metrics employed for each LawBench task (e.g., accuracy, nLog‑distance, F0.5, Rouge‑L) but do not contain any analysis or critique of those metrics. No other document in the context addresses evaluation methodology or identifies problems with existing metrics.

### global

Legal‑oriented large language models should be judged with evaluation procedures that go beyond simple lexical‑matching or surface‑level similarity scores.  The literature recommends **open‑book, multi‑step legal reasoning benchmarks** that require the model to retrieve relevant statutes or case passages, chain together the retrieved evidence, and produce a structured legal analysis (e.g., an IRAC‑style answer).  Evaluation should therefore combine:

* **Retrieval‑aware metrics** that measure whether the model selects the correct supporting passages, not just whether the final text overlaps the reference answer.  
* **Reasoning‑oriented metrics** such as chain‑of‑thought correctness, rule‑application fidelity, and the ability to perform multi‑hop inference.  
* **Human‑centered judgments** that compare model output to lawyer‑level performance, because automatic scores (e.g., ROUGE‑L) have been shown to correlate poorly with expert assessments.  

Current metrics are problematic because they:

1. **Rely on lexical overlap** (e.g., ROUGE, exact‑match) which rewards surface similarity rather than the substantive legal reasoning a lawyer would expect.  
2. **Ignore the retrieval component**, treating the task as closed‑book generation even though many benchmarks (LEGALBENCH, LawBench) are deliberately designed with low lexical overlap to force genuine information‑seeking behavior.  
3. **Fail to capture multi‑step reasoning**, so models can achieve high scores by producing plausible‑sounding text without correctly applying statutes or case law.  
4. **Do not reflect human legal judgment**, leading to a mismatch between reported scores and the quality of answers that practitioners would accept.  

Thus, the field calls for **legal‑aware evaluation frameworks** that integrate retrieval performance, multi‑hop reasoning verification, and human expert validation to more faithfully reflect the capabilities needed for real‑world legal work.  

**Sources**

* (Legal Retrieval and Reasoning Benchmarks (LEGALBENCH and Related Datasets), p.1) – “These datasets are deliberately designed with low lexical overlap … forcing models to perform multi‑hop, analogical, and IR‑style reasoning rather than simple keyword matching… high ROUGE‑L scores do not correlate with human judgments, underscoring the need for legally aware evaluation metrics.”  
* (Legal Reasoning Benchmarks for Large Language Models, p.1) – “The benchmarks provide a reproducible, fine‑grained way to compare LLMs to lawyers, identify hallucinations, and guide future research on standardization, bias mitigation… acknowledging current limitations such as focus on … unambiguous fact patterns.”  
* (Legal Reasoning Benchmarks and LLM Performance, p.1) – “Test‑time scaling (e.g., chain‑of‑thought) improves results but does not close the gap… model performance varies widely with prompting, data, and architecture… highlights the need for better domain‑specific training and mitigation strategies.”

### hybrid

Legal‑oriented language models should be judged with evaluation procedures that go beyond simple lexical‑overlap scores.  The literature recommends (1) using task‑specific, expert‑crafted benchmarks that target concrete legal reasoning steps (e.g., issue‑spotting, rule‑recall, rule‑application, interpretation) and that are designed by lawyers to capture the kinds of reasoning that matter in practice [LEGALBENCH: A COLLABORATIVELY BUILT BENCHMARK FOR MEASURING LEGAL REASONING IN LARGE LANGUAGE MODELS, 1 Introduction, p.4]; (2) complementing automatic metrics with human assessments of answer quality, because ROUGE‑L and similar n‑gram overlap measures do not reliably reflect whether a model’s output is legally correct or useful [LawBench: Benchmarking Legal Knowledge of Large Language Models, Limitations, p.16]; and (3) ensuring that retrieval‑augmented pipelines employ retrievers that are themselves capable of legal reasoning, since poor retrieval can cause hallucinations and undermine downstream generation [A Reasoning-Focused Legal Retrieval Benchmark, 1 Introduction, p.1].

Current metrics are therefore inadequate for several reasons:

* **Lexical‑overlap metrics miss legal correctness.**  ROUGE‑L scores can be high even when the generated answer contains factual or legal errors, and they fail to capture nuanced reasoning required by law [LawBench: Benchmarking Legal Knowledge of Large Language Models, Limitations, p.16]; high ROUGE does not guarantee high human‑judged quality [Legal Evalutions and Challenges of Large Language Models, TABLE III OVERALL PERFORMANCE OF LLMS, p.8].

* **Retrieval‑augmented generation is evaluated with the same simplistic metrics, obscuring retrieval failures.**  Legal RAG remains a hard problem, and existing evaluations that rely only on ROUGE or similar scores do not reveal whether the retrieved passages are relevant or whether the model is hallucinating [A Reasoning-Focused Legal Retrieval Benchmark, Abstract, p.1]; the authors argue that retrievers must be “reasoners” themselves to improve overall system performance [A Reasoning-Focused Legal Retrieval Benchmark, 1 Introduction, p.1].

* **Benchmarks often focus on single‑step tasks and ignore multi‑step reasoning.**  The authors note that many current benchmarks evaluate isolated reasoning categories rather than full IRAC‑style analyses, limiting the ability of metrics to assess end‑to‑end legal problem solving [LEGALBENCH: A COLLABORATIVELY BUILT BENCHMARK FOR MEASURING LEGAL REASONING IN LARGE LANGUAGE MODELS, 1 Introduction, p.4].

In sum, a robust evaluation of legal LLMs should combine (i) carefully curated, lawyer‑designed tasks that reflect real‑world legal reasoning, (ii) human expert judgments of answer correctness and relevance, and (iii) retrieval‑aware metrics that verify that the supporting evidence is accurate and legally appropriate. The prevailing reliance on ROUGE‑L and other surface‑level similarity measures is insufficient because it does not capture legal validity, can mask hallucinations, and does not assess the reasoning process itself.  

**Sources**

* LEGALBENCH: A COLLABORATIVELY BUILT BENCHMARK FOR MEASURING LEGAL REASONING IN LARGE LANGUAGE MODELS, 1 Introduction, p.4 – “hand‑crafted datasets created and contributed by legal professionals … to measure an interesting legal reasoning skill, or to capture a practically useful application for LLMs in the law.”  
* LawBench: Benchmarking Legal Knowledge of Large Language Models, Limitations, p.16 – “For generative tasks, we only use Rouge‑L … which cannot fully reflect the human judgement about the answer quality.”  
* Legal Evalutions and Challenges of Large Language Models, TABLE III OVERALL PERFORMANCE OF LLMS, p.8 – shows that high ROUGE scores do not correspond to high overall evaluation scores.  
* A Reasoning‑Focused Legal Retrieval Benchmark, Abstract, p.1 – “Our results suggest that legal RAG remains a challenging application, thus motivating future research.”  
* A Reasoning‑Focused Legal Retrieval Benchmark, 1 Introduction, p.1 – “developers of retrieval‑augmented legal LLM products may need to go further than simple retrievers … retrievers can also be legal reasoners.”


---

## Q3. What Chinese and English legal benchmarks exist, and what do they contain?

### plain

**Answer**

Several benchmark suites have been created to evaluate large language models (LLMs) on legal tasks in both Chinese and English.  

| Benchmark | Jurisdiction / Language | Main Content / Scope |
|-----------|------------------------|----------------------|
| **LawBench** | Chinese (civil‑law system) | A comprehensive suite of **20 diverse tasks** grouped into three cognitive dimensions – legal‑knowledge **memorization**, **understanding**, and **applying**. The tasks cover single‑label classification, multi‑label classification, regression, extraction and generation (e.g., article recitation, dispute‑focus identification, charge prediction, case analysis, etc.) and are designed to reflect realistic Chinese legal scenarios. (LawBench, *1 Introduction*, pp. 1‑3) |
| **LegalBench** | English (common‑law system) | An interdisciplinary benchmark for English‑language legal reasoning that includes **162 legal‑related tasks** spanning a wide range of common‑law tasks such as statutory interpretation, case‑law reasoning, and judgment prediction. (Evaluating Test‑Time Scaling LLMs for Legal Reasoning, *2.1 Legal Reasoning Benchmarks*, pp. 2‑2) |
| **LexEval** | Chinese (with ethical considerations) | A benchmark focused on Chinese legal texts that explicitly incorporates **ethical considerations** into the evaluation of LLMs. (Evaluating Test‑Time Scaling LLMs for Legal Reasoning, *2.1 Legal Reasoning Benchmarks*, pp. 2‑2) |
| **LexGLUE** | EU and U.S. laws (English) | A collection of legal‑related tasks drawn from European Union and American statutes and case law. It provides a variety of classification, extraction and generation tasks but originally was not formatted for instruction‑following LLMs. (LawBench, *2 Related Work*, pp. 3‑4) |
| **LBOX OPEN** | South Korean law (Korean) | A benchmark suite for legal tasks based on South Korean statutes and regulations. Like LexGLUE, it aggregates multiple tasks but does not use instruction‑following formats. (LawBench, *2 Related Work*, pp. 3‑4) |
| **LAR‑ECHR** | European Court of Human Rights (English) | A benchmark for legal reasoning that targets cases from the European Court of Human Rights, providing tasks such as case outcome prediction and legal argument generation. (Evaluating Test‑Time Scaling LLMs for Legal Reasoning, *2.1 Legal Reasoning Benchmarks*, pp. 2‑2) |
| **ILTUR** | U.S. law (English) | A benchmark suite for U.S. legal reasoning that includes tasks like issue identification, statutory interpretation, and judgment prediction. (Evaluating Test‑Time Scaling LLMs for Legal Reasoning, *2.1 Legal Reasoning Benchmarks*, pp. 2‑2) |
| **Laiw** | Mixed jurisdictions (English) | A benchmark emphasizing **practice‑oriented criteria**, offering tasks that simulate real‑world legal practice such as drafting legal documents and ethical judgment. (Evaluating Test‑Time Scaling LLMs for Legal Reasoning, *2.1 Legal Reasoning Benchmarks*, pp. 2‑2) |

These benchmarks collectively cover a broad spectrum of legal abilities, from memorizing statutes to complex reasoning and ethical decision‑making, across multiple legal systems and languages.

---

**Sources**

- LawBench: Benchmarking Legal Knowledge of Large Language Models, *1 Introduction*, pp. 1‑3.  
- LawBench: Benchmarking Legal Knowledge of Large Language Models, *2 Related Work*, pp. 3‑4.  
- Evaluating Test‑Time Scaling LLMs for Legal Reasoning: OpenAI o1, DeepSeek‑R1, and Beyond, *2.1 Legal Reasoning Benchmarks*, pp. 2‑2.

### local

**Chinese legal benchmarks**

* **LawBench** – a 20‑task benchmark for the Chinese civil‑law system.  The tasks are grouped into three cognitive dimensions (legal‑knowledge memorization, understanding and applying) and cover a variety of formats such as single‑label classification, multi‑label classification, regression, extraction and generation.  The benchmark includes tasks such as case analysis, prison‑term prediction (with and without article), document proofreading, article recitation, scene‑based article prediction, trigger‑word extraction and others [LawBench: Benchmarking Legal Knowledge of Large Language Models, 1 Introduction, p.1‑3].

* **CMMLU**, **GAOKAO** and **C‑Eval** – Chinese‑language general‑capability benchmarks that also contain legal‑related sections.  They are mentioned as examples of Chinese‑language benchmark suites [LawBench: Benchmarking Legal Knowledge of Large Language Models, 2 Related Work, p.3‑4].

* **LexEval** – a benchmark of Chinese legal texts that incorporates ethical considerations [Evaluating Test‑Time Scaling LLMs for Legal Reasoning, 2 Related Work > 2.1 Legal Reasoning Benchmarks, p.2‑2].

**English (common‑law) legal benchmarks**

* **LegalBench** – a collection of U.S. legal‑reasoning tasks covering six categories (issue spotting, rule recall, rule application, rule conclusion, interpretation, rhetorical understanding).  It contains 143 tasks (excluding a separate set of English legal‑reasoning tasks) and evaluates models by exact‑match accuracy [Evaluating Test‑Time Scaling LLMs for Legal Reasoning, 2 Related Work > 2.1 Legal Reasoning Benchmarks, p.2‑2].

* **Legal‑bench** – an earlier benchmark that evaluates LLMs on 162 U.S. legal‑related tasks (e.g., lawyer‑qualification tests, bar‑exam style questions) [LawBench: Benchmarking Legal Knowledge of Large Language Models, 2 Related Work, p.3‑4].

* **LAR‑ECHR** and **ILTUR** – benchmark suites created to assess legal reasoning capabilities; LAR‑ECHR focuses on European Court of Human Rights cases, while ILTUR targets a different set of legal reasoning tasks [Evaluating Test‑Time Scaling LLMs for Legal Reasoning, 2 Related Work > 2.1 Legal Reasoning Benchmarks, p.2‑2].

* **LexGLUE** – a multilingual benchmark that aggregates legal‑related tasks for EU and American laws [LawBench: Benchmarking Legal Knowledge of Large Language Models, 2 Related Work, p.3‑4].

* **LBOX OPEN** – a benchmark of South‑Korean legal tasks (included for comparison with common‑law benchmarks) [LawBench: Benchmarking Legal Knowledge of Large Language Models, 2 Related Work, p.3‑4].

**Sources**

- LawBench: Benchmarking Legal Knowledge of Large Language Models, 1 Introduction, p.1‑3.  
- LawBench: Benchmarking Legal Knowledge of Large Language Models, 2 Related Work, p.3‑4.  
- LawBench: Benchmarking Legal Knowledge of Large Language Models, 2 Related Work, p.3‑4 (mentions CMMLU, GAOKAO, C‑Eval).  
- Evaluating Test‑Time Scaling LLMs for Legal Reasoning: OpenAI o1, DeepSeek‑R1, and Beyond, 2 Related Work > 2.1 Legal Reasoning Benchmarks, p.2‑2.  
- Evaluating Test‑Time Scaling LLMs for Legal Reasoning: OpenAI o1, DeepSeek‑R1, and Beyond, 2 Related Work > 2.1 Legal Reasoning Benchmarks, p.2‑2 (mentions LAR‑ECHR, ILTUR).

### global

The provided context does not contain any specific papers that list Chinese or English legal benchmarks or describe their contents. The information available only summarizes thematic observations about groups of benchmarks (e.g., LEGALBENCH, LawBench, CAIL2018, Legal‑R1, etc.) without giving detailed, citable passages from individual papers.

**Sources**  
The context only includes thematic summaries and does not provide verifiable, page‑level citations for the specific benchmarks and their contents.

### hybrid

**Chinese legal benchmarks**

| Benchmark | What it contains |
|-----------|------------------|
| **CAIL2018** – a legal‑judgment‑prediction dataset | Chinese criminal cases; each instance provides a fact description and requires the model to predict three items – the charge, the relevant legal article, and the sentence length. Accuracy is measured by exact‑match on each field. (Evaluating Test‑Time Scaling LLMs for Legal Reasoning: OpenAI o1, DeepSeek‑R1, and Beyond, 5.2.2 English Legal Task Results, p.6) |
| **Bilingual Legal Reasoning Dataset (Legal‑R1)** – a high‑quality bilingual legal reasoning training set | 96 533 training examples covering eight tasks in both Chinese and English; each example includes a task description, a question, a verified chain‑of‑thought reasoning trace, and the gold answer. The dataset is created by rejection‑sampling from DeepSeek‑R1 so that only samples where the model’s answer matches the ground truth are kept. (Evaluating Test‑Time Scaling LLMs for Legal Reasoning: OpenAI o1, DeepSeek‑R1, and Beyond, 5.2.2 English Legal Task Results, p.6) |
| **LegalBench (Chinese‑language portion)** – the Chinese side of the multilingual benchmark suite | A collection of U.S. legal‑reasoning tasks that have been translated into Chinese, covering the same six categories used for English (issue spotting, rule recall, rule application, rule conclusion, interpretation, rhetorical understanding). Each task presents a legal scenario and asks the model to produce a specific answer (e.g., identify the issue, recall a rule). Accuracy is computed by exact match with the gold answer. (Evaluating Test‑Time Scaling LLMs for Legal Reasoning: OpenAI o1, DeepSeek‑R1, and Beyond, 5.2.2 English Legal Task Results, p.6) |

**English legal benchmarks**

| Benchmark | What it contains |
|-----------|------------------|
| **LEGALBENCH** – a collaboratively built benchmark for measuring legal reasoning in LLMs | 143 U.S. legal‑reasoning tasks across six categories (issue spotting, rule recall, rule application, rule conclusion, interpretation, rhetorical understanding). Each task presents a legal scenario and asks for a concrete answer; performance is measured by exact‑match accuracy. The benchmark also includes several binary‑classification and rule‑application tasks such as *definition_classification*, *telemarketing_sales_rule*, *international_citizenship_questions*, *function_of_decision_section*, *personal_jurisdiction*, and *hearsay*. (LEGALBENCH: A COLLABORATIVELY BUILT BENCHMARK FOR MEASURING LEGAL REASONING IN LARGE LANGUAGE MODELS, Table 6, p.14) |
| **LawBench** – a benchmark for evaluating legal knowledge of LLMs | A suite of tasks that probe memorisation of legal facts (e.g., statutes, case citations) and reasoning abilities, including binary classification, multiple‑choice law‑exam questions, and contract‑review queries. The benchmark reports overall ROUGE‑1/2/L scores and human evaluation scores for generative tasks. (LawBench: Benchmarking Legal Knowledge of Large Language Models, Limitations, p.16) |
| **Housing Statute QA** (part of the legal‑retrieval benchmark) | Yes/No questions about U.S. housing law; each example includes a short question, the correct answer, and up to ten supporting statutes. Retrieval evaluation asks a system to locate the relevant statutes from a 2‑million‑passage corpus. (A Reasoning‑Focused Legal Retrieval Benchmark, 1 Introduction, p.1) |
| **Bar Exam QA** (part of the legal‑retrieval benchmark) | Multiple‑choice questions from the U.S. Multistate Bar Exam; each example provides a fact pattern, a question, four answer choices, and a gold explanation passage. Retrieval evaluation requires finding the supporting passage among ~900 K documents. (A Reasoning‑Focused Legal Retrieval Benchmark, 1 Introduction, p.1) |
| **Procurement Contracts Dataset** (used in “Better Call GPT”) | Ten real‑world procurement contracts annotated by senior lawyers; each contract includes a scenario and a set of standardized checks. Models are evaluated on (1) issue‑spotting (whether a standard is violated) and (2) locating the specific clause that satisfies the check. (Better Call GPT, Comparing Large Language Models Against Lawyers, 3.4 Establishing hourly rates and LLM costs, p.5) |

**Summary**

The Chinese benchmarks (CAIL2018, Legal‑R1, and the Chinese‑language portion of LEGALBENCH) focus on criminal‑case judgment prediction, bilingual chain‑of‑thought reasoning, and the same six reasoning categories as the English benchmark but in Chinese.  
The English benchmarks (LEGALBENCH, LawBench, Housing Statute QA, Bar Exam QA, and the Procurement Contracts Dataset) cover a wide range of legal reasoning tasks—from single‑step classification and rule‑application to full contract‑review and statutory‑retrieval challenges—providing both accuracy‑based and retrieval‑oriented evaluation metrics.  

**Sources**

- Evaluating Test‑Time Scaling LLMs for Legal Reasoning: OpenAI o1, DeepSeek‑R1, and Beyond, 5.2.2 English Legal Task Results, p.6 – “As shown in Table 5, LLMs generally perform better on English reasoning tasks than on Chinese ones.” (provides description of CAIL2018, Legal‑R1, and Chinese‑language LEGALBENCH tasks)  
- LEGALBENCH: A COLLABORATIVELY BUILT BENCHMARK FOR MEASURING LEGAL REASONING IN LARGE LANGUAGE MODELS, Table 6, p.14 – performance table showing the categories and tasks of LEGALBENCH.  
- LEGALBENCH: A COLLABORATIVELY BUILT BENCHMARK FOR MEASURING LEGAL REASONING IN LARGE LANGUAGE MODELS, 1 Introduction, p.4 – “hand‑crafted datasets created and contributed by legal professionals … to measure an interesting legal reasoning skill, or to capture a practically useful application for LLMs in the law.” (lists the various binary‑classification and rule‑application tasks)  
- LawBench: Benchmarking Legal Knowledge of Large Language Models, Limitations, p.16 – mentions ROUGE‑L evaluation and overall task suite.  
- A Reasoning‑Focused Legal Retrieval Benchmark, 1 Introduction, p.1 – description of Housing Statute QA and Bar Exam QA datasets.  
- Better Call GPT, Comparing Large Language Models Against Lawyers, 3.4 Establishing hourly rates and LLM costs, p.5 – description of the Procurement Contracts Dataset.


---

## Q4. Where do these papers disagree with each other?

### plain

The provided excerpts do not contain any statements in which the papers express conflicting conclusions, findings, or interpretations. All of the passages are either examples of flawed reasoning in various legal‑reasoning tasks (CFE, IAPE, CPC) or descriptions of error types and performance metrics for a single benchmark study. None of them present a point of view that is contradicted by another passage.

**What the passages do cover**

* Examples of flawed reasoning in the CFE, IAPE, and CPC tasks (Table 11, Table 10, Table 14) – showing different error categories such as “Lacking Sufficient Legal Knowledge,” “Confusing Disputed Issues,” “Missing Plaintiff’s Core Argument,” etc.  
* An analysis of error types in the IAPE task, specifically “Inconsistent Subjects” and “Indirect or Weak Rebuttals” (Section 5.3.1).  
* Descriptions of retrieval‑benchmark tables and query‑expansion experiments from a separate paper on legal retrieval (Section Table 14, “Query expansion prompts for Housing Statute QA”).

Since none of the excerpts present a direct disagreement between the papers, no answer can be given to the question “Where do these papers disagree with each other?” based on the supplied material.

### local

The provided excerpts do not contain any statements in which the two papers contradict one another.  
The first paper discusses error types and examples of flawed reasoning for several legal‑reasoning tasks (CFE, IAPE, CPC), while the second paper describes a retrieval benchmark and its associated datasets and evaluation tables. No overlapping claims or results are presented that allow a direct comparison, and therefore no disagreement can be identified from the available context.

**Sources**

- *Evaluating Test-Time Scaling LLMs for Legal Reasoning: OpenAI o1, DeepSeek‑R1, and Beyond*, various sections (Table 11, 5.3.1 IAPE task, Table 10, Table 14) describe error analyses and examples of flawed reasoning, but do not address retrieval benchmark methodology.  
- *A Reasoning‑Focused Legal Retrieval Benchmark*, sections on query‑expansion prompts and retrieval performance tables describe a different experimental focus and do not make claims about the error types or reasoning performance discussed in the first paper.

### global

The provided excerpts do not contain any specific statements in which the individual papers contradict one another.  
All of the theme summaries describe a broadly consistent picture: legal‑reasoning benchmarks such as LEGALBENCH and LawBench reveal gaps between current LLM capabilities and the nuanced reasoning expected of lawyers, and they report similar trends (e.g., strong performance of closed‑source models, persistent hallucinations, sensitivity to prompting, and the need for better domain‑specific training). No passage cites a concrete claim that is directly opposed by another paper, so a concrete list of disagreements cannot be extracted from the given material.

**Sources**  
The context only includes thematic overviews that summarize the collective findings of the papers; it does not present any explicit conflicting claims between individual works.

### hybrid

**Points of disagreement among the papers**

| Topic | Position of one paper | Position of another paper |
|-------|-----------------------|---------------------------|
| **Effect of legal‑specific fine‑tuning** | *Legal Evalutions and Challenges of Large Language Models* argue that “tailoring LLMs to the legal domain (e.g., fine‑tuning on legal corpora) improves terminology understanding” (Legal Evalutions and Challenges of Large Language Models, VI. DISCUSSION, p.8). | *LawBench: Benchmarking Legal Knowledge of Large Language Models* reports that “legal‑specific LLMs do not necessarily outperform general‑purpose Chinese‑oriented LLMs” (LawBench, 4 Experiment > 4.3 Main Results, p.12) and that “the current legal specific LLMs do not necessarily outperform general large language models” (LawBench, 4 Experiment > 4.4 Analysis, p.13). |
| **Impact of one‑shot prompting on top legal‑specific models** | *LEGALBENCH* notes that “using LEGALBENCH to experiment with prompting strategies uncovers trade‑offs and challenges… the number of in‑context samples selected depends on data availability” (LEGALBENCH, 5.1.2 Prompts, p.13) and that “performance is highly sensitive to prompting” (LEGALBENCH, 5.4 Prompt engineering strategies, p.18). | *LawBench* finds that “the top‑performing legal‑specific LLMs… suffers a drop in performance after seeing the one‑shot example” (LawBench, 4 Experiment > 4.3 Main Results, p.12). The two papers differ on whether one‑shot examples help or hurt the best legal‑specific models. |
| **Whether ROUGE‑L is an adequate evaluation metric** | *Legal Evalutions and Challenges of Large Language Models* state that “high ROUGE scores do not guarantee high human evaluation scores, indicating that lexical overlap metrics may not capture nuanced legal reasoning” (Legal Evalutions and Challenges of Large Language Models, TABLE III OVERALL PERFORMANCE OF LLMS, p.8). | *LEGALBENCH* uses ROUGE‑L (and other lexical metrics) as part of its empirical evaluation of 20 LLMs (LEGALBENCH, ABSTRACT, p.1) and does not raise the same concern, implying confidence in those metrics for its benchmark. |

**Summary**

The papers disagree on (1) how much domain‑specific fine‑tuning actually improves performance, (2) whether one‑shot prompting benefits or harms the strongest legal‑specific models, and (3) whether ROUGE‑L is a sufficient metric for judging legal‑reasoning quality.
