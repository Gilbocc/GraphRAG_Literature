# Retrieval comparison — 2026-08-12 15:20

Answering model `openai/gpt-oss-120b` at temperature 0.0, embeddings `openai/text-embedding-3-small`, top_k=5. Extraction ran on `openai/gpt-oss-120b`.

- **plain** — nearest chunks only, no graph. The control.
- **local** — nearest chunks, plus the claims each one grounds.
- **global** — community summaries only.
- **hybrid** — community summaries, plus each theme's claims and the verbatim passage behind them.


---

## Q1. How do multilingual or cross-lingual legal NLP tasks differ from English-only ones?

### plain

**Answer**

Multilingual or cross‑lingual legal NLP tasks involve additional challenges that are not present in English‑only (monolingual) settings:

| Aspect | English‑only legal NLP | Multilingual / cross‑lingual legal NLP |
|--------|------------------------|----------------------------------------|
| **Training data** | Typically a single language (English) is used for both training and evaluation.  Earlier work on EU legislation was limited to English documents (“Legal topic classification has been studied for EU legislation … in a monolingual setting (English)”)【PASSAGE (similarity 0.847)】. | Documents are available in many languages (23 EU official languages in MULTI‑EURLEX).  The goal is to train on a source language and classify in target languages without any target‑language labels. |
| **Cross‑lingual transfer** | Not required; models can be fine‑tuned directly on the target language. | Requires that a model trained on one language retain multilingual knowledge so it can be applied zero‑shot to other languages.  Fine‑tuning a multilingual model on a single source language often causes **catastrophic forgetting** of that knowledge, leading to poor transfer【PASSAGE (similarity 0.813)】【PASSAGE (similarity 0.794)】. |
| **Adaptation strategies** | Standard fine‑tuning of monolingual models (e.g., BERT) is sufficient. | Special adaptation techniques (partial fine‑tuning, adapters, BITFIT, LNFIT, etc.) are needed to preserve multilingual representations and improve zero‑shot performance【PASSAGE (similarity 0.813)】【PASSAGE (similarity 0.794)】. |
| **Model choice** | Monolingual pretrained models (e.g., English BERT) are commonly used. | Multilingual pretrained Transformers (XLM‑ROBERTA, MT5) are employed, but must be handled carefully to avoid losing cross‑lingual capacity. |
| **Evaluation splits** | Random splits are often used without concern for temporal drift. | Chronological splits are important because **temporal concept drift** can inflate performance on random splits; this issue is highlighted for legal topic classification across languages【PASSAGE (similarity 0.813)】. |
| **Resource availability** | Large annotated English corpora exist; cross‑lingual resources are scarce. | Parallel multilingual corpora (e.g., MULTI‑EURLEX) are newly introduced to enable research, but many languages still lack labeled data, motivating zero‑shot approaches. |

In summary, while English‑only legal NLP can rely on monolingual models and straightforward fine‑tuning, multilingual or cross‑lingual legal NLP must contend with preserving multilingual knowledge, handling catastrophic forgetting, selecting appropriate adaptation methods, and accounting for temporal concept drift across languages.

**Sources**

- MultiEURLEX – “Related Work” (Section 2, pp. 2‑3) – discusses prior English‑only work and the lack of cross‑lingual studies【PASSAGE (similarity 0.847)】.  
- MultiEURLEX – “Introduction” (Section 1, pp. 1‑2) – describes the multilingual dataset, zero‑shot setup, and adaptation strategies【PASSAGE (similarity 0.834)】.  
- MultiEURLEX – “Abstract” (Section Abstract, pp. 1‑1) – notes catastrophic forgetting when fine‑tuning on a single language【PASSAGE (similarity 0.813)】.  
- MultiEURLEX – “Conclusions and Future Work” (Section 7, pp. 9‑9) – reiterates the need for adaptation strategies and the impact of label‑set size【PASSAGE (similarity 0.794)】.

### local

Multilingual and cross‑lingual legal NLP tasks differ from English‑only (monolingual) tasks in several ways:

* **Scope of languages** – Multilingual legal tasks must handle many languages (23 EU official languages in MULTI‑EURLEX) and often rely on a single source‑language training set to classify documents in other target languages, whereas English‑only tasks train and evaluate on a single language. [MultiEURLEX – 1 Introduction, p.1‑2]  

* **Zero‑shot cross‑lingual transfer** – In multilingual settings the model is expected to transfer knowledge to languages for which no labeled training data are available (zero‑shot transfer). This scenario has not been explored in prior English‑only legal NLP work. [MultiEURLEX – 2 Related Work, p.2‑3]  

* **Catastrophic forgetting of multilingual knowledge** – Fine‑tuning a multilingual pretrained model on only one language can cause it to lose the multilingual representations it learned during pre‑training, leading to poor performance on other languages. This issue does not arise for monolingual English models. [MultiEURLEX – Abstract, p.1]  

* **Adaptation strategies** – To retain multilingual knowledge, researchers employ partial fine‑tuning, adapters, BITFIT, LNFIT, or other adaptation methods. These techniques are specific to multilingual transfer and are not needed for English‑only tasks. [MultiEURLEX – 1 Introduction, p.1‑2]  

* **Temporal concept drift and split design** – Multilingual legal datasets often span many years and languages, making chronological splits important to reflect temporal drift; random splits can over‑estimate performance. While temporal drift can also affect English datasets, the multilingual setting amplifies the need for careful split design. [MultiEURLEX – 7 Conclusions and Future Work, p.9]  

* **Dataset size and diversity** – MULTI‑EURLEX provides a much larger and more diverse set of documents (≈65 k EU laws) across many languages compared with many English‑only legal datasets that are smaller and limited to a single language. [MultiEURLEX – 2 Related Work, p.2‑3]  

In contrast, English‑only legal NLP research (e.g., contract‑review datasets such as CUAD) focuses on tasks defined for a single language and does not need to address cross‑lingual transfer, multilingual adaptation, or the associated challenges. [CUAD – 2 Related Work > 2.1 Legal NLP, p.2‑3]  

**Sources**

* MultiEURLEX – 1 Introduction, p.1‑2  
* MultiEURLEX – 2 Related Work, p.2‑3  
* MultiEURLEX – Abstract, p.1  
* MultiEURLEX – 7 Conclusions and Future Work, p.9  
* CUAD – 2 Related Work > 2.1 Legal NLP, p.2‑3

### global

The provided context does not contain any specific passages that describe how multilingual or cross‑lingual legal NLP tasks differ from English‑only tasks. The themes summarize general findings but do not include citable statements with paper titles, sections, and page numbers that directly address this comparison. Therefore, I cannot provide an answer supported by the required citations.

### hybrid

Multilingual and cross‑lingual legal NLP tasks pose challenges that are largely absent from English‑only benchmarks.  

* **Data and language coverage** – Unlike the many English‑only corpora, multilingual resources such as MULTI‑EURLEX contain the same EU statutes translated into 23 official languages, requiring models to handle a far broader set of vocabularies, scripts and linguistic phenomena (MultiEURLEX, 1 Introduction, p.1).  

* **Zero‑shot transfer difficulty** – When a multilingual model is fine‑tuned on a single source language, it tends to forget the multilingual knowledge it acquired during pre‑training, leading to poor performance on target languages (MultiEURLEX, 1 Introduction, p.1).  

* **Adaptation strategies are essential** – Techniques such as partial fine‑tuning, adapters, BITFIT and LNFIT can preserve multilingual knowledge and substantially improve zero‑shot cross‑lingual transfer, but their effectiveness depends on the pretrained model and on the size of the label set (MultiEURLEX, Abstract, p.1; MultiEURLEX, 7 Conclusions and Future Work, p.9). Larger label sets tend to yield larger gains.  

* **Temporal concept drift** – Legal topics evolve over time, and chronological data splits expose a drift that random splits hide; this drift is especially pronounced in multilingual settings where documents in different languages may be updated at different times (MultiEURLEX, 1 Introduction, p.1).  

* **Lexical overlap is lower** – Cross‑lingual legal retrieval tasks deliberately exhibit very low lexical similarity between queries and relevant passages, making traditional lexical retrievers such as BM25 ineffective (A Reasoning‑Focused Legal Retrieval Benchmark, 1 Introduction, p.1). This low overlap is less of an issue for English‑only datasets, where many benchmarks contain higher lexical similarity.  

* **Evaluation complexity** – Multilingual benchmarks must assess both language‑specific performance and cross‑lingual transfer, often requiring many‑to‑many fine‑tuning setups and careful handling of label granularity across languages (MultiEURLEX, 6.3 Multilingual Fine‑tuning (many‑to‑many), p.9).  

Together, these factors make multilingual or cross‑lingual legal NLP tasks more demanding than English‑only ones, demanding richer data, specialized adaptation methods, and evaluation protocols that account for language diversity and temporal change.  

**Sources**  
- MultiEURLEX – “Multilingual learning is an active field of research … we introduce a new multilingual dataset … 23 languages” (MultiEURLEX, 1 Introduction, p.1)  
- MultiEURLEX – “We find that fine‑tuning a multilingually pretrained model … leads to catastrophic forgetting … poor zero‑shot transfer” (MultiEURLEX, Abstract, p.1)  
- MultiEURLEX – “Adaptation strategies … help retain multilingual knowledge … their impact also depends on the particular pretrained model used and the size of the label set” (MultiEURLEX, Abstract, p.1)  
- MultiEURLEX – “the gains increase as the label set increases” (MultiEURLEX, 7 Conclusions and Future Work, p.9)  
- MultiEURLEX – “We also compare chronological vs. random splits, highlighting the impact of temporal concept drift” (MultiEURLEX, 1 Introduction, p.1)  
- A Reasoning‑Focused Legal Retrieval Benchmark – “we benchmark existing state‑of‑the‑art retrieval pipelines … low lexical similarity … common retrieval methods like BM25 struggle” (A Reasoning‑Focused Legal Retrieval Benchmark, 1 Introduction, p.1)


---

## Q2. What methods are used to extract structured information from contracts?

### plain

**Answer**

The papers describe two complementary ways of turning the unstructured text of a contract into structured information:

1. **Human‑driven clause annotation** –  
   *Law‑student annotators* read each contract and, following a detailed annotation guide (over 100 pages of rules), mark every passage that corresponds to one of the 41 pre‑defined label categories (e.g., party names, governing law, restrictive covenants, revenue‑risk clauses). For each label the start‑ and end‑token positions of the clause are recorded, producing a structured “clause‑span” representation that can later be used as training data for machine‑learning models. (CUAD, *Section 3 CUAD: A Contract Review Dataset*, pp. 3‑4)

2. **Model‑driven clause extraction** –  
   After the annotated dataset is built, **large language models** (e.g., BERT, DeBERTa, GPT‑4) are fine‑tuned to *predict the same start‑ and end‑token spans* for any new contract. The models therefore output a structured list of clause spans for each of the 41 label categories, effectively automating the extraction of the same information that human annotators recorded. (CUAD, *Section 3 CUAD: A Contract Review Dataset*, pp. 3‑4)

3. **Prompt‑based LLM review** –  
   In the “Better Call GPT” study, a **system prompt** is given to a large language model (GPT‑4‑1106) that instructs it to act as an experienced lawyer and to “identify any legal issues… and locate the specific sections of the contract that influence their judgments.” The model then returns a JSON object that lists, for each checklist item, the contract lines (i.e., the relevant clause text) and an explanation, thereby extracting structured information directly from the contract via a zero‑shot prompting approach. (Better Call GPT, *Table 6*, pp. 14‑14)

Together, these methods provide a pipeline: **manual annotation → structured clause‑span data → supervised model training → automated clause extraction**, and an alternative **prompt‑based LLM extraction** that directly produces structured outputs without prior fine‑tuning.

---

**Sources**

- *CUAD: An Expert‑Annotated NLP Dataset for Legal Contract Review*, **Section 3 CUAD: A Contract Review Dataset**, pp. 3‑4.  
- *CUAD: An Expert‑Annotated NLP Dataset for Legal Contract Review*, **Section 3 CUAD: A Contract Review Dataset**, pp. 3‑4 (for the description of model training and span prediction).  
- *Better Call GPT, Comparing Large Language Models Against Lawyers*, **Table 6**, pp. 14‑14.

### local

**Answer**

The papers describe two complementary approaches for extracting structured information from contracts:

1. **Human‑annotated span labeling** – Law‑students and lawyers read each contract and highlight every text span that corresponds to one of 41 predefined clause categories (e.g., Governing Law, Non‑Compete). The resulting dataset records the start and end token positions of each relevant span, which serves as ground‑truth structured information for training and evaluation [CUAD: An Expert‑Annotated NLP Dataset for Legal Contract Review, “CUAD Contract Page Lengths”, p.4‑5].

2. **Machine‑learning models that predict token spans** – Trained models take a contract and a clause description as input and output the start‑ and end‑token positions of the clause(s) that match the description. This formulation turns clause extraction into a span‑prediction problem that can be solved with transformer‑based classifiers [CUAD: An Expert‑Annotated NLP Dataset for Legal Contract Review, “3 CUAD: A Contract Review Dataset”, p.3‑4].

3. **Large language model (LLM) prompting** – An LLM (e.g., GPT‑4) is given a detailed system prompt that frames it as an experienced lawyer and asks it to locate every checklist item in the contract, returning the matching contract lines and explanations in a structured JSON format. This prompt‑driven approach lets the LLM directly produce structured outputs (checklist number, contract lines, explanation, compliance flag, assumptions) for each clause [Better Call GPT, Comparing Large Language Models Against Lawyers, “Table 6”, p.14].

Together, these methods combine expert human annotation to create high‑quality training data, supervised span‑prediction models to automate clause detection, and carefully engineered prompts to harness LLMs for structured clause extraction.

**Sources**

- *CUAD: An Expert‑Annotated NLP Dataset for Legal Contract Review*, **CUAD Contract Page Lengths**, p.4‑5: “Figure 2: A histogram of the number of pages in CUAD contracts… The EDGAR contracts are more complicated… The model’s task is, given a contract and a category … to output the start and end token positions of each relevant span.”  
- *CUAD: An Expert‑Annotated NLP Dataset for Legal Contract Review*, **3 CUAD: A Contract Review Dataset**, p.3‑4: “For each label category, we identify every clause in every contract that is most relevant to that label category. We then have models extract the relevant clauses from a contract by outputting the start and end tokens that identify the span of text that relates to that label category.”  
- *Better Call GPT, Comparing Large Language Models Against Lawyers*, **Table 6**, p.14: “System Prompt … Your goal is to identify any legal issues … For each section of the provided contract, carefully analyze it and identify ALL of the checks listed in the provided checklist. Format your answer as a JSON object that includes … ‘contract_Lines’, ‘explanation’, ‘check_Met’, ‘assumptions’ …”

### global

The provided excerpts do not contain any specific descriptions of methods that are used to extract structured information from contracts. The themes summarize overall findings about dataset performance, model architectures, and benchmark results, but they do not detail particular extraction techniques (e.g., rule‑based parsing, named‑entity recognition, hierarchical models, or other algorithms).

**Sources**

- The themes on “Legal Contract and Clause Understanding Benchmarks,” “Legal Large Language Model Evaluation and Automation,” “Legal Retrieval and Question‑Answering Benchmarks,” “Legal Reasoning Benchmarks and Datasets,” and “Legal Benchmark Datasets and Model Evaluation” discuss datasets, model performance, and evaluation challenges, but none provide concrete methodological details for extracting structured information from contracts.

### hybrid

**Methods for extracting structured information from contracts**

* **Span‑based clause extraction** –  The CUAD benchmark frames contract‑information extraction as a *span‑prediction* problem: for each predefined clause category a model must output the start and end token positions of the relevant text.  Transformer‑based models (e.g., DeBERTa, BERT, RoBERTa) are trained on the expert‑annotated CUAD data to learn to “highlight” the salient portions of a contract that a lawyer would need to review.  This approach turns the unstructured contract into a set of labeled text spans that can be downstream‑processed as structured clause data.  

* **Prompt‑driven LLM extraction** –  In the “Better Call GPT” study, a large language model is given a detailed system prompt that instructs it to act as an experienced lawyer and to **identify every checklist item** in a contract, returning a JSON object that lists the checklist number, the exact contract sentences or clauses that satisfy (or fail to satisfy) the item, an explanation, and a “check‑Met” flag.  By parsing the model’s JSON output, the raw contract text is transformed into a structured representation of compliance checks.  

These two approaches—trained span‑prediction models and prompt‑engineered LLMs that output structured JSON—are the primary methods reported for turning free‑form contract language into machine‑readable, structured information.  

**Sources**

* CUAD: “The task is to highlight salient portions of a contract that are important for a human to review.” (CUAD: An Expert‑Annotated NLP Dataset for Legal Contract Review, 1 Introduction, p.1)  
* CUAD: “For each label category, we identify every clause in every contract that is most relevant to that label category… models extract the relevant clauses from a contract by outputting the start and end tokens that identify the span of text that relates to that label category.” (CUAD: An Expert‑Annotated NLP Dataset for Legal Contract Review, 3 CUAD: A Contract Review Dataset, p.3)  
* Better Call GPT: System prompt that requires the model to “identify ALL of the checks listed in the provided checklist” and to return a JSON object containing the contract lines that correspond to each check. (Better Call GPT, Comparing Large Language Models Against Lawyers, Table 6, p.14)


---

## Q3. What risks and responsibilities come with building large legal datasets?

### plain

**Answer**

Building large legal datasets carries several intertwined risks and responsibilities:

1. **Risk of Harm from Sensitive or Restricted Content** –  
   Large‑language‑model pre‑training can inadvertently expose or reproduce biased, obscene, copyrighted, or private information that appears in the source material.  When legal texts contain personal identifiers, financial details, or medical records, a model trained on them may “leak” that sensitive data during generation, creating privacy violations and potential legal liability【Legal Evalutions and Challenges of Large Language Models, A. Data privacy, p.7】.

2. **Responsibility to Filter According to Legal Norms** –  
   The authors argue that existing ad‑hoc filtering approaches “failed to take context into account” and propose grounding filtering in the law itself.  They distill governmental legal norms that constrain the inclusion of toxic or private content into “actionable lessons for researchers,” making the dataset’s construction a concrete exercise in applying those norms【Pile of Law, Abstract, p.1】.

3. **Ethical Duty to Remove or Flag Sensitive Material** –  
   Even though the underlying records are public, the dataset may still contain material that “escaped administrative scrutiny” (e.g., undisclosed personal details).  The authors discuss “mechanisms for content removal” and emphasize that the dataset’s utility for pre‑training must be balanced against the need to protect individuals from harm【Pile of Law, 2 Pile of Law, p.2‑3】.

4. **Ensuring Open‑License and Transparency** –  
   By curating only content that is “already entirely public and mostly available under permissive licenses,” the creators aim to respect copyright and licensing constraints, thereby reducing the risk of infringing on proprietary works【Pile of Law, 2 Pile of Law, p.2‑3】.

5. **Ongoing Curation and Governance** –  
   The dataset is described as “growing” and the authors plan to continue adding material while “recognize[ing] that it may contain sensitive material.”  This implies an ongoing responsibility to monitor, audit, and possibly prune the collection as new legal or ethical concerns emerge【Pile of Law, 2 Pile of Law, p.2‑3】.

In sum, building large legal corpora requires (a) vigilant privacy protection to prevent data leakage, (b) systematic, law‑grounded filtering of toxic or copyrighted material, (c) transparent licensing practices, and (d) continuous ethical oversight to address any sensitive content that may surface.

**Sources**

- *Pile of Law: Learning Responsible Data Filtering from the Law and a 256GB Open-Source Legal Dataset*, Abstract, p.1.  
- *Pile of Law: Learning Responsible Data Filtering from the Law and a 256GB Open-Source Legal Dataset*, 2 Pile of Law, pp. 2‑3.  
- *Legal Evalutions and Challenges of Large Language Models*, A. Data privacy, p.7.

### local

Building large legal datasets carries several important risks and corresponding responsibilities:

* **Risk of exposing sensitive personal information.**  
  Legal documents often contain details such as identities, financial status, or medical records. When such data is used to train language models, there is a danger that the model could unintentionally reveal this private information during generation, leading to data‑leakage incidents【Legal Evalutions and Challenges of Large Language Models, A. Data privacy, p.7】.

* **Responsibility to implement strict privacy safeguards.**  
  To mitigate the above risk, developers must prioritize data‑privacy protections throughout the design and training pipeline, ensuring that model outputs do not disclose personal data and that rigorous data‑processing and output‑review mechanisms are in place【Legal Evalutions and Challenges of Large Language Models, A. Data privacy, p.7】.

* **Risk that the underlying public‑record data still includes material that escaped administrative scrutiny.**  
  Even though the Pile of Law consists of entirely public documents, it may contain sensitive content that was not filtered by existing legal or administrative mechanisms【Pile of Law: Learning Responsible Data Filtering from the Law and a 256GB Open‑Source Legal Dataset, 2 Pile of Law, p.2‑3】.

* **Responsibility to discuss and apply ethical removal mechanisms.**  
  The authors of the Pile of Law explicitly address the ethics of their work and propose processes for content removal, emphasizing the need for responsible curation and filtering that respects legal standards of privacy and toxicity【Pile of Law: Learning Responsible Data Filtering from the Law and a 256GB Open‑Source Legal Dataset, 2 Pile of Law, p.2‑3】.

* **Responsibility to respect implicit legal filtering mechanisms.**  
  Each source in a large legal corpus carries its own implicit filtering rules derived from the relevant legal standards. Curators must recognize and discuss these implicit filters, and consider additional safeguards where they may be insufficient【Pile of Law: Learning Responsible Data Filtering from the Law and a 256GB Open‑Source Legal Dataset, 2 Pile of Law, p.2‑3】.

* **Responsibility to provide transparent documentation and open licensing.**  
  The Pile of Law is released under permissive, open licenses and is accompanied by detailed documentation of its composition and the implicit filters, supporting community scrutiny and responsible reuse【Pile of Law: Learning Responsible Data Filtering from the Law and a 256GB Open‑Source Legal Dataset, 2 Pile of Law, p.2‑3】.

**In summary**, building large legal datasets requires careful handling of privacy‑sensitive information, the implementation of robust data‑processing and output‑review procedures, ethical consideration of content removal, acknowledgment of source‑specific legal filters, and transparent, open documentation to enable responsible downstream use.

**Sources**

- Pile of Law: Learning Responsible Data Filtering from the Law and a 256GB Open‑Source Legal Dataset, “2 Pile of Law”, p.2‑3.  
- Legal Evalutions and Challenges of Large Language Models, “A. Data privacy”, p.7.

### global

The provided context does not contain any specific passages that state the risks and responsibilities associated with building large legal datasets, nor does it give page‑level citations from individual papers that could be used to support such a claim. The themes summarize general concerns (e.g., data confidentiality, privacy, bias, ethical and regulatory issues), but they do not include the required “paper title, section, p.PAGE” citations needed for a factual answer. Therefore, I cannot provide a sourced answer to this question based on the given material.

### hybrid

Building large‑scale legal corpora brings clear technical benefits, but it also creates a set of ethical and practical risks that must be managed responsibly.

* **Privacy leakage** – Legal documents often contain personally identifying information (names, financial details, medical records).  When such data are used for model training the model can unintentionally reproduce that information in its outputs, creating a risk of data‑leakage.  The authors therefore stress that “the design and training processes of the model must prioritize the protection of data” and that “rigorous data‑processing and review mechanisms … should be implemented to minimize risks and ensure compliance and security” (Legal Evalutions and Challenges of Large Language Models, A. Data privacy, p.7).

* **Bias and unfair outputs** – Because legal corpora are assembled from many heterogeneous sources, they can embed societal and procedural biases.  The papers note that “Due to the diverse sources of data, these models can introduce biases, which may result in unfair outputs” and that such bias “may have serious repercussions when applied in the legal context” (Legal Evalutions and Challenges of Large Language Models, C. Ethical and moral issues, p.8; I. INTRODUCTION, p.1).

* **Licensing and data‑use constraints** – Even when the raw material is publicly available, the underlying licenses may be restrictive.  The Pile of Law authors point out that “All of the content is already entirely public and mostly available under permissive licenses, but has not previously been compiled at scale for research purposes” and that they deliberately select only openly‑licensed material to avoid legal violations (Pile of Law, 2 Pile of Law, p.2).

* **Anonymization and loss of utility** – Removing personal identifiers is necessary for privacy, but aggressive anonymization can degrade the usefulness of the data for downstream tasks.  The study of Chinese and U.S. case datasets reports that “we strictly anonymized all personal privacy information in the cases” to ensure fairness, acknowledging that this step is essential for ethical research even though it may affect model performance (Legal Evalutions and Challenges of Large Language Models, A. Scope of the Study and Used Datasets, p.5).

* **Responsibility for content filtering** – Legal texts contain material that may be toxic, obscene, or otherwise problematic.  The Pile of Law project proposes a “filtering grounded in law” that captures the implicit legal norms used to exclude such content, and they discuss “mechanisms for content removal” to mitigate potential harms (Pile of Law, 2 Pile of Law, p.2).

* **Need for ethical oversight** – The authors argue that “the lack of transparency in model‑generated results complicates users’ ability to assess their reliability” and call for a “robust ethical review mechanism” to ensure that models remain neutral and do not perpetuate discrimination (Legal Evalutions and Challenges of Large Language Models, C. Ethical and moral issues, p.8).

Together, these points illustrate that building large legal datasets requires careful **privacy protection, bias mitigation, licensing compliance, thoughtful anonymization, systematic content filtering, and ongoing ethical governance** to avoid harmful outcomes and to uphold the responsibilities of the legal‑NLP community.

**Sources**

- (Legal Evalutions and Challenges of Large Language Models, A. Data privacy, p.7)  
- (Legal Evalutions and Challenges of Large Language Models, C. Ethical and moral issues, p.8)  
- (Legal Evalutions and Challenges of Large Language Models, I. INTRODUCTION, p.1)  
- (Pile of Law: Learning Responsible Data Filtering from the Law and a 256GB Open-Source Legal Dataset, 2 Pile of Law, p.2)  
- (Legal Evalutions and Challenges of Large Language Models, A. Scope of the Study and Used Datasets, p.5)


---

## Q4. How did legal NLP methods change with the arrival of large language models?

### plain

**Answer**

The emergence of large‑language models (LLMs) has shifted legal‑NLP from relatively narrow, task‑specific tools toward broadly capable, transformer‑based systems that can be fine‑tuned on massive legal corpora.  

* **From classic NLP pipelines to end‑to‑end LLMs** – Earlier legal‑NLP work relied on separate components such as tokenizers, rule‑based extractors, and shallow classifiers.  With LLMs, a single model can perform many of these steps jointly (e.g., entity recognition, classification, reasoning) because the transformer architecture learns rich contextual representations from huge amounts of text.  

* **Domain‑specific fine‑tuning** – Researchers now take general‑purpose LLMs and continue pre‑training or fine‑tune them on large, curated legal datasets (e.g., Chinese statutes, case law, contracts).  This produces “legal‑specific” LLMs such as **LawGPT**, **ChatLaw**, **LAWGPT‑zh**, **Lawyer‑LLama**, **LexiLaw**, and **KL3M**, which show superior understanding of legal terminology, concepts, and reasoning compared with earlier models.  

* **Expanded capabilities** – Modern legal LLMs can handle a wider range of tasks:  
  * **Legal reasoning and question answering** – they generate answers to complex legal inquiries and can apply provisions to fact patterns.  
  * **Summarization and drafting** – they produce concise case summaries, draft contract clauses, and suggest language improvements.  
  * **Research assistance** – they retrieve and synthesize case law, produce plain‑language memoranda, and power chat‑bots for Supreme Court rulings.  

* **Performance gains and new challenges** – Benchmarks show that fine‑tuned legal LLMs often outperform earlier models and even rival human junior lawyers in accuracy, speed, and cost for contract review.  However, evaluations still reveal limitations: occasional factual inaccuracies, hallucinations, and difficulty with nuanced legal language, especially in zero‑shot settings.  

Overall, the arrival of LLMs has transformed legal NLP from fragmented, narrowly scoped pipelines into integrated, high‑capacity language models that can be adapted to many legal tasks, while also introducing new research questions around reliability, bias, and ethical use.

**Sources**

1. *Legal Evalutions and Challenges of Large Language Models*, Section **C. Overview of legal‑specific LLMs**, p.5 – describes the shift to fine‑tuned legal LLMs (LexNLP, LawGPT, ChatLaw) and their superior capabilities.  
2. *Legal Evalutions and Challenges of Large Language Models*, Section **II. REVIEW OF LLMS IN THE LEGAL FIELD**, pp.2‑3 – outlines how LLMs are now used for summarization, drafting, research, and legal reasoning, and notes the performance gaps of earlier models versus newer legal‑specific LLMs.  
3. *Better Call GPT, Comparing Large Language Models Against Lawyers*, Section **Better Call GPT, Comparing Large Language Models Against Lawyers**, p.1 – reports empirical results showing LLMs matching or exceeding human accuracy and speed in contract review, highlighting the practical impact of LLMs on legal NLP tasks.

### local

Legal natural‑language‑processing (NLP) has moved from rule‑based or modest‑size neural tools toward large‑scale, transformer‑based language models that can be fine‑tuned for legal tasks. Early work focused on classic NLP pipelines (tokenisation, entity extraction, text classification) applied to legal documents, but the rapid progress of transformer LLMs has introduced “general‑purpose” models such as GPT‑4 that already possess broad legal knowledge and can perform reasoning, summarisation, drafting and question answering across jurisdictions [Legal Evalutions and Challenges of Large Language Models, I. INTRODUCTION, p.1‑2].  

Researchers have responded by creating domain‑specific legal LLMs that are pre‑trained on large corpora of statutes, case law and contracts and then fine‑tuned with legal‑question‑answer data (e.g., LawGPT, ChatLaw, LAWGPT‑zh). These models show improved understanding of legal terminology, provisions and jurisdiction‑specific nuances compared with generic LLMs [Legal Evalutions and Challenges of Large Language Models, C. Overview of legal‑specific LLMs, p.5‑5].  

The arrival of LLMs also shifted evaluation practices: benchmarks now test models on full case texts (Chinese and U.S. judgments) and measure both automatic similarity (ROUGE/BLEU) and human alignment with reference judgments, rather than only measuring token‑level classification accuracy [Legal Evalutions and Challenges of Large Language Models, I. INTRODUCTION, p.1‑2].  

At the same time, the literature notes new challenges introduced by LLMs: legal language’s high precision leads to factual and legal inaccuracies, hallucinations, and bias inherited from training data, prompting research on retrieval‑augmented pipelines (vector‑database + keyword retrieval) to reduce hallucination risk [Legal Evalutions and Challenges of Large Language Models, II. REVIEW OF LLMS IN THE LEGAL FIELD, p.2‑3].  

Overall, the field has transitioned from narrow, task‑specific NLP tools to large, adaptable language models that can be specialised for law, while also confronting new reliability and ethical issues that did not arise with earlier methods.  

**Sources**  
- Legal Evalutions and Challenges of Large Language Models, I. INTRODUCTION, p.1‑2 – “In the legal field, LLMs are seen as a transformative force … comprehensive legal knowledge base and exceptional capabilities in natural language understanding and generation …” and discussion of evaluation challenges.  
- Legal Evalutions and Challenges of Large Language Models, C. Overview of legal‑specific LLMs, p.5‑5 – Description of LexNLP, LawGPT, ChatLaw and domain‑specific fine‑tuning.  
- Legal Evalutions and Challenges of Large Language Models, II. REVIEW OF LLMS IN THE LEGAL FIELD, p.2‑3 – “ChatLaw … designed to reduce hallucination risks during legal data retrieval by combining vector database and keyword‑based retrieval …” and notes on inaccuracies and hallucinations.

### global

The provided context does not contain any specific passages that cite particular papers, sections, or page numbers describing how legal‑NLP methods changed with the arrival of large language models. The themes summarize overall trends, but without concrete, citable excerpts they cannot be used to support factual statements in the required citation format.

**Sources**  
The context only includes thematic summaries and does not provide any verifiable, page‑level citations from individual papers. Consequently, a detailed answer with the required citations cannot be generated from the available information.

### hybrid

Legal natural‑language‑processing (NLP) in the legal domain has been reshaped by the emergence of large language models (LLMs) in several ways.

* **From narrow, task‑specific pipelines to general‑purpose LLMs** – Early legal NLP relied on handcrafted features or modest‑size models trained on limited legal corpora. The rapid progress of transformer‑based LLMs (e.g., GPT‑3/4, Claude, Gemini) has introduced “general‑purpose” systems that can perform many legal tasks—summarization, drafting, research, and question answering—without task‑specific engineering.  (“Models like OpenAI's GPT series have demonstrated exceptional capabilities … in the legal field, LLMs are seen as a transformative force …” — Legal Evalutions and Challenges of Large Language Models, I. INTRODUCTION, p.1)

* **Domain‑specific pre‑training and fine‑tuning** – Researchers now pre‑train or continuously fine‑tune LLMs on large, curated legal collections such as the Pile of Law or Chinese case corpora. This yields models that “exhibit superior capabilities in understanding legal concepts, conducting legal reasoning, and generating legal text” compared with generic LLMs.  (“These models, fine‑tuned on extensive legal corpora, exhibit superior capabilities …” — Legal Evalutions and Challenges of Large Language Models, C. Overview of legal‑specific LLMs, p.5)

* **Prompt‑engineering and in‑context learning** – Because LLM performance is highly sensitive to the way tasks are phrased, systematic prompt‑engineering studies have become a core part of legal NLP research. Experiments on LEGALBENCH show that “prompt engineering strategies significantly influence LLM performance on LEGALBENCH tasks” and that description‑style prompts can boost results on many rule‑application and classification tasks.  (“Prompt engineering strategies significantly influence LLM performance on LEGALBENCH tasks.” — LEGALBENCH, 5 Results, p.12)

* **Long‑context handling** – Legal documents often exceed the 16 k‑token windows of early LLMs, forcing document splitting and hurting accuracy. New ultra‑long‑context models (Claude 2.1, Gemini 1.5) and mixture‑of‑experts architectures are being adopted to process whole contracts or case files without splitting, addressing a key technical bottleneck.  (“Gemini 1.5 further enhances its capabilities by supporting ultra‑long contexts of up to millions of tokens … improve efficiency and scalability for processing complex legal tasks.” — Legal Evalutions and Challenges of Large Language Models, A. Overview of leading non‑open source LLMs, p.3)

* **Error patterns and reliability concerns** – Despite higher capability, LLMs still make systematic mistakes—arithmetic errors, mis‑citing rule provisions, or mis‑assessing party diversity—highlighting the need for robust evaluation and mitigation.  (“L​LM errors on rule‑application tasks frequently arise from arithmetic mistakes or citing incorrect portions of legal rules.” — LEGALBENCH, 5.3.3 Rule‑application, p.15)

* **Ethical and privacy safeguards** – The broader adoption of LLMs has foregrounded data‑privacy and bias issues, prompting calls for responsible data‑filtering, privacy‑preserving training, and transparent evaluation.  (“Cases in the legal domain often involve individuals' sensitive information … there is a risk that the model may unintentionally expose … during content generation.” — Legal Evalutions and Challenges of Large Language Models, A. Data privacy, p.7)

Overall, the arrival of LLMs shifted legal NLP from narrowly engineered, small‑scale models toward large, pre‑trained architectures that are fine‑tuned, carefully prompted, and increasingly able to handle long legal texts—while also exposing new challenges in accuracy, bias, and privacy that must be addressed.

**Sources**

- Legal Evalutions and Challenges of Large Language Models, I. INTRODUCTION, p.1  
- Legal Evalutions and Challenges of Large Language Models, C. Overview of legal‑specific LLMs, p.5  
- LEGALBENCH: A COLLABORATIVELY BUILT BENCHMARK FOR MEASURING LEGAL REASONING IN LARGE LANGUAGE MODELS, 5 Results, p.12  
- LEGALBENCH: A COLLABORATIVELY BUILT BENCHMARK FOR MEASURING LEGAL REASONING IN LARGE LANGUAGE MODELS, 5.3.3 Rule‑application, p.15  
- Legal Evalutions and Challenges of Large Language Models, A. Data privacy, p.7  
- Legal Evalutions and Challenges of Large Language Models, A. Overview of leading non‑open source LLMs, p.3


---

## Q5. Does making a model bigger reliably improve legal task performance?

### plain

**Answer**

Increasing a model’s size tends to help, but it does not guarantee better performance on legal tasks.

* In the legal‑benchmark study (LawBench) the authors observe that *“scaling up the model size usually improves the performance, but the improvement is more consistent in the one‑shot than in the zero‑shot scenario.”* They also note exceptions: *“ChatLaw is an outlier, a larger size results in lower performance,”* and that *“simply increasing the model size may not automatically lead to better performance”* in zero‑shot settings. This shows that while larger models often achieve higher scores and lower abstention rates, the effect is not uniform across all tasks or prompting conditions. (LawBench, **4 Experiment > 4.4 Analysis**, pp. 13‑15)

* A complementary analysis (LEGALBENCH) reports that *“within LLM families, larger models usually outperform smaller models… the margin of the gap varies across LLM families and reasoning categories.”* The authors also point out that *“the largest LLM (GPT‑4) outperforms virtually all other models,”* but that *“significant gaps… exist even among models of the same size,”* indicating that size alone does not fully determine performance. (LEGALBENCH, **5.2 Performance trends**, pp. 13‑15)

Together, the evidence suggests that **making a model bigger generally leads to better legal‑task performance, especially in one‑shot prompting, but the improvement is not reliable across all scenarios; other factors such as model architecture, training data, fine‑tuning, and the prompting regime also play crucial roles.**

**Sources**

1. *LawBench: Benchmarking Legal Knowledge of Large Language Models*, Section 4 Experiment > 4.4 Analysis, pp. 13‑15.  
2. *LEGALBENCH: A Collaboratively Built Benchmark for Measuring Legal Reasoning in Large Language Models*, Section 5.2 Performance trends, pp. 13‑15.

### local

Increasing the size of a language model tends to raise its legal‑task performance, but the improvement is not guaranteed in every setting.

* **LawBench (LawBench: Benchmarking Legal Knowledge of Large Language Models)** reports that scaling up model size “usually improves the performance, but the improvement is more consistent in the one‑shot than in the zero‑shot scenario” and that larger models have lower abstention rates, indicating better instruction following. However, the authors also note mixed results in zero‑shot settings and an outlier (ChatLaw) where a larger model performed worse【LawBench: Benchmarking Legal Knowledge of Large Language Models, 4 Experiment > 4.4 Analysis, p.13‑15】.  

* **LEGALBENCH (LEGALBENCH: A COLLABORATIVELY BUILT BENCHMARK FOR MEASURING LEGAL REASONING IN LARGE LANGUAGE MODELS)** finds that “within LLM families, larger models usually outperform smaller models” across most reasoning categories, though the margin varies by family and task【LEGALBENCH: A COLLABORATIVELY BUILT BENCHMARK FOR MEASURING LEGAL REASONING IN LARGE LANGUAGE MODELS, 5.2 Performance trends, p.13‑15】.

Together, the evidence suggests that larger models generally achieve higher scores on legal benchmarks, especially in one‑shot or within‑family comparisons, but the benefit can be inconsistent for zero‑shot evaluations or specific model families.

**Sources**

* LawBench: Benchmarking Legal Knowledge of Large Language Models – Section 4 Experiment > 4.4 Analysis, pp. 13‑15.  
* LEGALBENCH: A COLLABORATIVELY BUILT BENCHMARK FOR MEASURING LEGAL REASONING IN LARGE LANGUAGE MODELS – Section 5.2 Performance trends, pp. 13‑15.

### global

The provided material does not contain any specific empirical results that directly compare model size with legal‑task performance across individual papers. The themes summarize general observations—e.g., that “ultra‑long‑context models (Claude, Gemini 1.5) can avoid document splitting” and that “model size and architecture matter: DeBERTa‑xlarge consistently attains the highest precision‑recall trade‑offs on contract‑review tasks”—but they do not present a systematic claim that increasing model size reliably improves performance on legal tasks. Consequently, the question cannot be answered definitively from the given context.

**Sources**  
The context only offers high‑level thematic summaries and does not provide citable passages that address the relationship between model size and legal task performance.

### hybrid

Increasing the size of a language model tends to raise its legal‑task performance, but the improvement is not uniform across all settings.  

* Within a given model family, larger variants usually score higher than their smaller siblings (e.g., Flan‑T5‑XXL beats Flan‑T5‑XL, LLaMA‑2‑13B beats LLaMA‑2‑7B) and they also tend to have lower abstention rates, especially in one‑shot prompting scenarios (LEGALBENCH, “Table 2 … Within LLM families, we observe that larger models usually outperform smaller models.” — LEGALBENCH, 5.2 Performance trends, p.13).  

* However, the benefit of scaling is less consistent in zero‑shot conditions. The LawBench analysis shows that while model size generally helps in one‑shot cases, “simply increasing the model size may not automatically lead to better performance” in zero‑shot settings, and some larger models (e.g., ChatLaw) even perform worse (LawBench, 4 Experiment > 4.4 Analysis, p.13).  

Thus, making a model bigger often improves legal task performance, particularly when the model can be prompted with a few examples, but larger size alone does not guarantee better results across all evaluation regimes.  

**Sources**  
- *LawBench: Benchmarking Legal Knowledge of Large Language Models*, 4 Experiment > 4.4 Analysis, p.13.  
- *LEGALBENCH: A collaboratively built benchmark for measuring legal reasoning in large language models*, 5.2 Performance trends, p.13.
