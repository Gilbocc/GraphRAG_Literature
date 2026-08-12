# Retrieval comparison — 2026-08-12 15:43

Answering model `openai/gpt-oss-120b` at temperature 0.0, embeddings `openai/text-embedding-3-small`, top_k=5. Extraction ran on `openai/gpt-oss-120b`.

- **plain** — nearest chunks only, no graph. The control.
- **local** — nearest chunks, plus the claims each one grounds.
- **global** — community summaries only.
- **hybrid** — community summaries, plus each theme's claims and the verbatim passage behind them.


---

## Q1. How do multilingual or cross-lingual legal NLP tasks differ from English-only ones?

### plain

**Answer**

Multilingual or cross‑lingual legal NLP tasks differ from English‑only tasks in several ways that are highlighted by the MultiEURLEX papers:

1. **Data Availability and Scope**  
   * English‑only research has traditionally used monolingual corpora of EU legislation (e.g., Chalkidis et al., 2019) or other single‑language legal datasets.  
   * Multilingual legal NLP must work with documents that are **officially translated into many languages** (23 EU languages in MultiEURLEX) and often with **parallel or comparable** versions of the same law (MultiEURLEX contains 65 k EU laws in 23 languages) (Paper *MultiEURLEX – A multi‑lingual and multi‑label legal document classification dataset for zero‑shot cross‑lingual transfer*, Abstract, p.1).

2. **Cross‑lingual Transfer Challenges**  
   * In the legal domain, **cross‑lingual transfer had not been studied before** (Related Work, p.2‑3).  
   * When a multilingual model is fine‑tuned on a single source language, it suffers **catastrophic forgetting of multilingual knowledge**, leading to poor performance on target languages (Abstract, p.1; Conclusions, p.9).  
   * Effective cross‑lingual transfer therefore requires **adaptation strategies** (partial fine‑tuning, adapters, BITFIT, LNFIT) that preserve the multilingual representations learned during pre‑training (Introduction, p.1‑2; Conclusions, p.9).

3. **Modeling Considerations**  
   * Multilingual legal NLP must choose between **monolingual models** (e.g., BERT per language) and **multilingual transformer‑based models** (XLM‑ROBERTA, MT5). Experiments show that multilingual models can be **competitive with monolingual ones** when proper adaptation is used (Conclusions, p.9).  
   * Adaptation strategies that fine‑tune only a tiny fraction of parameters (e.g., <0.05 % in BITFIT/LNFIT) can still yield strong zero‑shot performance, a finding that is less relevant for purely English tasks (Conclusions, p.9).

4. **Temporal Concept Drift**  
   * Legal vocabularies evolve over time, and this **temporal concept drift** is especially problematic when using random splits for evaluation. The authors stress the need for **chronological splits** to obtain realistic estimates of performance (Introduction, p.1‑2; Conclusions, p.9). While drift is a concern for any legal NLP, the multilingual setting amplifies it because the drift may differ across languages.

5. **Research Landscape**  
   * Prior legal NLP work has focused on English or a few non‑English languages, but **cross‑lingual transfer has not been explored** in the legal domain until this work (Related Work, p.2‑3). This contrasts with the broader NLP field, where cross‑lingual transfer is an active research area (Related Work, p.2‑3).

In summary, multilingual/cross‑lingual legal NLP must handle a far larger linguistic diversity, contend with the loss of multilingual knowledge during fine‑tuning, employ specialized adaptation techniques, and carefully address temporal drift—issues that are largely absent or less pronounced in English‑only legal NLP research.

---

**Sources**

1. *MultiEURLEX – A multi‑lingual and multi‑label legal document classification dataset for zero‑shot cross‑lingual transfer*, **Abstract**, p.1.  
2. *MultiEURLEX – A multi‑lingual and multi‑label legal document classification dataset for zero‑shot cross‑lingual transfer*, **Section 2 Related Work**, pp.2‑3.  
3. *MultiEURLEX – A multi‑lingual and multi‑label legal document classification dataset for zero‑shot cross‑lingual transfer*, **Section 1 Introduction**, pp.1‑2.  
4. *MultiEURLEX – A multi‑lingual and multi‑label legal document classification dataset for zero‑shot cross‑lingual transfer*, **Section 7 Conclusions and Future Work**, p.9.

### local

Multilingual and cross‑lingual legal NLP tasks differ from English‑only tasks in several ways.  

* **Scope of languages** – English‑only work on legal text has traditionally focused on a single language (e.g., EU legislation in English) and uses monolingual models or datasets [MultiEURLEX, 2 Related Work, p.2‑3].  In contrast, multilingual and cross‑lingual research must handle many languages simultaneously (23 EU official languages in MULTI‑EURLEX) and often relies on large multilingual pretrained Transformers such as XLM‑ROBERTA or MT5 [MultiEURLEX, 1 Introduction, p.1‑2].  

* **Transfer setting** – Cross‑lingual legal NLP aims to train on labeled data in a resource‑rich source language and predict labels in target languages where no training data exist (zero‑shot transfer) [MultiEURLEX, Abstract, p.1‑1]; English‑only tasks do not require such transfer because the training and test data are in the same language.  

* **Model adaptation challenges** – Fine‑tuning a multilingual model on a single source language can cause catastrophic forgetting of the multilingual knowledge that is needed for other languages, leading to poor zero‑shot performance [MultiEURLEX, 1 Introduction, p.1‑2].  English‑only models do not face this issue because they are trained and evaluated on the same language.  

* **Adaptation strategies** – To mitigate forgetting, cross‑lingual legal NLP employs adaptation techniques such as partial fine‑tuning, adapters, BITFIT, and LNFIT, which retain multilingual knowledge and substantially improve zero‑shot transfer [MultiEURLEX, 1 Introduction, p.1‑2; 7 Conclusions and Future Work, p.9‑9].  Such strategies are unnecessary for English‑only tasks, which typically fine‑tune the entire model on the single language.  

* **Temporal concept drift** – Multilingual legal datasets like MULTI‑EURLEX enable the study of temporal concept drift across languages, and chronological splits are recommended because random splits over‑estimate performance [MultiEURLEX, 1 Introduction, p.1‑2; 7 Conclusions and Future Work, p.9‑9].  English‑only studies often ignore this cross‑lingual temporal aspect.  

Overall, multilingual/cross‑lingual legal NLP must address language diversity, zero‑shot transfer, preservation of multilingual knowledge, and temporal drift, whereas English‑only tasks operate within a single‑language, monolingual framework.  

**Sources**  
- MultiEURLEX – “Legal topic classification has been studied for EU legislation … in a monolingual setting (English).” (2 Related Work, p.2‑3)  
- MultiEURLEX – “We introduce MULTI‑EURLEX … 23 official EU languages … we use the dataset as a testbed for zero‑shot cross‑lingual transfer.” (1 Introduction, p.1‑2)  
- MultiEURLEX – “We find that fine‑tuning a multilingual model in a single source language leads to catastrophic forgetting … poor zero‑shot transfer to target languages.” (1 Introduction, p.1‑2)  
- MultiEURLEX – “Adaptation strategies … help retain multilingual knowledge … substantially improving zero‑shot cross‑lingual transfer.” (1 Introduction, p.1‑2)  
- MultiEURLEX – “We highlight the effect of temporal concept drift and the importance of chronological, instead of random, splits.” (7 Conclusions and Future Work, p.9‑9)

### global

Multilingual or cross‑lingual legal NLP tasks involve additional challenges that are not present in English‑only settings.  

* **Data availability** – Many legal documents are not available in all languages; in the MultiEURLEX study only a subset of the 23 languages has full coverage, so multilingual training must randomly select a language for each batch (MultiEURLEX, 6.3 Multilingual Fine‑tuning (many‑to‑many), p.9).  

* **Zero‑shot transfer** – Cross‑lingual transfer for legal text has been largely unexplored (MultiEURLEX, 1 Introduction, p.1) and requires models to generalise from English (or another source language) to target languages without any target‑language fine‑tuning.  

* **Adaptation strategies** – Simple adaptation methods such as BITFIT or LNFIT, which fine‑tune only a tiny fraction of parameters (<0.05 %), can still be competitive in multilingual settings (MultiEURLEX, 7 Conclusions and Future Work, p.9). Adapter modules consistently improve multilingual performance, yielding gains of up to +4.2 % mRP over no‑adaptation (MultiEURLEX, 6.2 Cross‑lingual Transfer (one‑to‑many), p.6).  

* **Label sparsity** – Multilingual legal datasets often contain many labels that are absent or extremely rare in the training split, making them good testbeds for few‑shot learning (Neural Legal Judgment Prediction in English, 2 ECHR Dataset, p.1).  

* **Evaluation differences** – English‑only benchmarks (e.g., ECHR judgment prediction) highlight the difficulty of few‑shot learning when labels appear in only 1.25 % of documents, whereas multilingual benchmarks must also account for language‑specific token distributions and the need to handle multiple label vocabularies simultaneously (Neural Legal Judgment Prediction in English, 5.3 Multi‑label Violation Results, p.4).  

Overall, multilingual legal NLP must cope with uneven language coverage, cross‑lingual generalisation, and often more severe label sparsity, whereas English‑only tasks focus primarily on handling rare labels within a single language.

**Sources**

- MultiEURLEX –A multi‑lingual and multi‑label legal document classification dataset for zero‑shot cross‑lingual transfer, 6.3 Multilingual Fine‑tuning (many‑to‑many), p.9.  
- MultiEURLEX –A multi‑lingual and multi‑label legal document classification dataset for zero‑shot cross‑lingual transfer, 1 Introduction, p.1.  
- MultiEURLEX –A multi‑lingual and multi‑label legal document classification dataset for zero‑shot cross‑lingual transfer, 6.2 Cross‑lingual Transfer (one‑to‑many), p.6.  
- MultiEURLEX –A multi‑lingual and multi‑label legal document classification dataset for zero‑shot cross‑lingual transfer, 7 Conclusions and Future Work, p.9.  
- Neural Legal Judgment Prediction in English, 2 ECHR Dataset, p.1.  
- Neural Legal Judgment Prediction in English, 5.3 Multi‑label Violation Results, p.4.

### hybrid

Multilingual and cross‑lingual legal NLP tasks introduce several challenges that are largely absent from English‑only settings.  First, they require **zero‑shot transfer** from a source language (often a resource‑rich language such as English) to target languages that have little or no labeled data.  This transfer is difficult because fine‑tuning a multilingual model on a single source language tends to cause **catastrophic forgetting of the multilingual knowledge** that the model acquired during pre‑training, leading to poor performance on the other languages — a problem that does not arise when the model is trained and evaluated only on English 【MultiEURLEX – A multi‑lingual and multi‑label legal document classification dataset for zero‑shot cross‑lingual transfer, 1 Introduction, p.1】.  

Second, successful cross‑lingual transfer depends heavily on **adaptation strategies** (e.g., partial fine‑tuning, adapters, BITFIT, LNFIT) that preserve multilingual representations; these strategies are unnecessary for monolingual English tasks 【MultiEURLEX – A multi‑lingual and multi‑label legal document classification dataset for zero‑shot cross‑lingual transfer, 1 Introduction, p.1】.  

Third, the **size and granularity of the label set** (EUROVOC concepts) affect how much benefit adaptation brings, with larger label sets yielding larger gains — another factor specific to multilingual legal topic classification 【MultiEURLEX – A multi‑lingual and multi‑label legal document classification dataset for zero‑shot cross‑lingual transfer, 1 Introduction, p.1】.  

Fourth, multilingual legal corpora expose **temporal concept drift** across languages and jurisdictions, requiring careful split strategies (chronological rather than random) to obtain realistic estimates of performance — a concern that is largely absent in static English‑only benchmarks 【MultiEURLEX – A multi‑lingual and multi‑label legal document classification dataset for zero‑shot cross‑lingual transfer, Abstract, p.1】.  

Finally, the literature notes that **cross‑lingual transfer has not been studied in the legal domain** before these works, highlighting a gap that English‑only research does not face 【MultiEURLEX – A multi‑lingual and multi‑label legal document classification dataset for zero‑shot cross‑lingual transfer, 2 Related Work, p.2】.  

In sum, multilingual legal NLP must address language‑specific data scarcity, preservation of multilingual knowledge during fine‑tuning, label‑set effects, and temporal drift—issues that are largely irrelevant for English‑only legal NLP tasks.  

**Sources**  
- MultiEURLEX – A multi‑lingual and multi‑label legal document classification dataset for zero‑shot cross‑lingual transfer, 1 Introduction, p.1  
- MultiEURLEX – A multi‑lingual and multi‑label legal document classification dataset for zero‑shot cross-lingual transfer, 2 Related Work, p.2  
- MultiEURLEX – A multi‑lingual and multi‑label legal document classification dataset for zero‑shot cross-lingual transfer, Abstract, p.1


---

## Q2. What methods are used to extract structured information from contracts?

### plain

**Answer**

The papers describe two complementary ways of turning the unstructured text of a contract into structured information:

1. **Manual clause‑level annotation and span extraction** –  
   In the CUAD dataset, expert annotators (law students trained for 70‑100 hours and quality‑checked by lawyers) read each contract and marked every clause that corresponded to one of 41 pre‑defined label categories.  For each label the exact start‑ and end‑token positions of the relevant clause were recorded, so that a model can later be trained to *extract the relevant clause spans* automatically.  This “needle‑in‑a‑haystack” approach turns the free‑form contract into a set of labeled text spans that represent structured information such as party names, governing law, renewal terms, restrictive covenants, etc. 【CUAD: An Expert‑Annotated NLP Dataset for Legal Contract Review, 3 CUAD: A Contract Review Dataset, pp. 3‑4】

2. **Prompt‑driven large‑language‑model (LLM) extraction** –  
   In *Better Call GPT* the authors evaluate LLMs by giving them a detailed system prompt that instructs the model to act as an experienced lawyer and to **identify, for each checklist item, the exact contract sentences or clauses that satisfy (or fail to satisfy) the requirement**.  The model must output a JSON object that includes the checklist number, the matching contract lines (or a null value), an explanation, and a “Met/Not met” flag.  This method extracts structured data (checklist results, clause references, explanations) directly from the contract text by means of a carefully engineered prompt. 【Better Call GPT, Comparing Large Language Models Against Lawyers, Table 6, pp. 14‑14】

Together, these approaches provide structured representations of contracts: the first by human‑created, token‑level annotations that can be used to train automatic clause‑extraction models, and the second by using LLMs with a structured prompt to produce machine‑generated, checklist‑based extractions.

---

**Sources**

- *CUAD: An Expert‑Annotated NLP Dataset for Legal Contract Review*, **Section 3 CUAD: A Contract Review Dataset**, pp. 3‑4.  
- *Better Call GPT, Comparing Large Language Models Against Lawyers*, **Section Table 6**, pp. 14‑14.

### local

**Answer**

The papers describe two complementary approaches for extracting structured information from contracts:

1. **Human‑annotated span labeling** – Law‑students and lawyers read each contract and manually highlight every text span that corresponds to each of the 41 predefined clause categories (e.g., Governing Law, Non‑Compete). The annotation guidelines, training (70‑100 h) and quality‑control procedures ensure that the highlighted spans serve as ground‑truth “needles in a haystack” for later modeling. [CUAD: An Expert‑Annotated NLP Dataset for Legal Contract Review, *CUAD Contract Page Lengths*, p.4‑5]  

2. **Machine‑learning models that predict span boundaries** – Given a contract and a clause description, a model is trained to output the start and end token positions of the relevant span, counting a prediction as correct when it overlaps the human‑annotated span with Jaccard ≥ 0.5. This formulation turns clause extraction into a span‑prediction task that can be solved with transformer‑based classifiers. [CUAD: An Expert‑Annotated NLP Dataset for Legal Contract Review, *3 CUAD: A Contract Review Dataset*, p.3‑4]  

3. **Prompt‑driven large language models (LLMs)** – A system prompt instructs GPT‑4‑1106 to act as an experienced lawyer and to “identify any legal issues… and locate the specific contract text” for each checklist item. The model returns JSON objects that list the checklist number, the contract lines that satisfy (or fail) the check, and an explanation, thereby extracting structured clause information directly from the raw contract text. [Better Call GPT, *Table 6*, p.14]  

Together, these methods combine expert‑curated span annotations with supervised learning and LLM prompting to turn unstructured contract prose into structured, machine‑readable clause data.  

**Sources**

- *CUAD: An Expert‑Annotated NLP Dataset for Legal Contract Review*, **CUAD Contract Page Lengths**, p.4‑5 – “Our dataset includes detailed annotations… annotators highlighted every span of text in the contract that is relevant to that category… The model’s task is… to output the start and end token positions of each relevant span.”  
- *CUAD: An Expert‑Annotated NLP Dataset for Legal Contract Review*, **3 CUAD: A Contract Review Dataset**, p.3‑4 – “For each label category, we identify every clause in every contract that is most relevant… we then have models extract the relevant clauses from a contract by outputting the start and end tokens that identify the span of text.”  
- *Better Call GPT, Comparing Large Language Models Against Lawyers*, **Table 6**, p.14 – System prompt example that directs GPT‑4‑1106 to “identify… all of the checks… and locate the specific contract text… Format your answer as a JSON object…”.

### global

The provided passages do not describe any specific methods for extracting structured information from contracts. They mention the CUAD dataset for contract‑review tasks and that models are evaluated on highlighting salient contract portions, but no concrete extraction techniques (e.g., rule‑based parsing, supervised sequence labeling, or graph‑based approaches) are detailed in the cited material.

**Sources**

- The CUAD passages describe the dataset and its purpose but contain no methodological details about structured information extraction (e.g., “We address this bottleneck within the legal domain by introducing the Contract Understanding Atticus Dataset (CUAD)… The task is to highlight salient portions of a contract…” – *CUAD: An Expert‑Annotated NLP Dataset for Legal Contract Review, Abstract, p.1*).

### hybrid

**Answer**

The papers describe two complementary ways of turning the un‑structured text of a contract into a structured representation:

1. **Span‑level clause annotation** – Contracts are manually annotated by trained law‑students and vetted by experienced lawyers, who mark the exact start‑ and end‑tokens of every clause that belongs to a predefined label (e.g., “Governing Law”, “Uncapped Liability”).  The resulting gold‑standard data consist of *spans* that identify the portions of a contract that a model must later predict.  This approach turns a contract into a set of (label, span) pairs that can be used for supervised training and evaluation. (CITE AS: CUAD: An Expert‑Annotated NLP Dataset for Legal Contract Review, 3 CUAD: A Contract Review Dataset, p.3)

2. **Checklist‑driven JSON output** – In the procurement‑contract benchmark, each contract is paired with a “contract‑review playbook” that lists the legal checks a practitioner would apply.  The model is prompted to read the contract and, for every checklist item, return a JSON object that includes the checklist number, the relevant contract sentences (or an empty field if the clause is absent), an explanation, and a “check‑Met” flag.  This format converts the contract into a structured table of (checklist item, matched text, explanation, status) entries. (CITE AS: Better Call GPT, Comparing Large Language Models Against Lawyers, Table 6, p.14)

Both methods rely on **expert‑generated ground‑truth** (law‑student annotations or senior‑lawyer‑verified checklist answers) to train and evaluate large language models that can automatically locate and label the relevant contract passages.  

**Sources**

- CUAD: An Expert‑Annotated NLP Dataset for Legal Contract Review, 3 CUAD: A Contract Review Dataset, p.3  
- Better Call GPT, Comparing Large Language Models Against Lawyers, Table 6, p.14


---

## Q3. What risks and responsibilities come with building large legal datasets?

### plain

**Answer**

Building large legal datasets carries several intertwined risks and responsibilities:

1. **Risk of Harm from Sensitive or Restricted Content** –  
   Large‑scale pre‑training data can contain biased, obscene, copyrighted, or private information that, if left unchecked, may cause “significant harm” when models generate output (e.g., leaking personal details or reproducing toxic language)【Pile of Law, Abstract, p.1】.  

2. **Privacy Risks and Data Leakage** –  
   Legal documents often include personally identifying, financial, or medical details. When such data are used for model training, there is a concrete danger that the model will unintentionally expose that information in its generations, leading to data‑leakage incidents【Legal Evalutions and Challenges of Large Language Models, A. Data privacy, p.7】.  

3. **Responsibility to Apply Legal‑Based Filtering** –  
   The authors argue that filtering should be grounded in existing legal norms that already regulate the inclusion of toxic or private material. By distilling “the legal norms that governments have developed to constrain the inclusion of toxic or private content into actionable lessons,” researchers can align dataset construction with the same standards that protect privacy and public safety【Pile of Law, Abstract, p.1】.  

4. **Ethical Duty to Remove Sensitive Material** –  
   Even though the underlying sources are public records, the dataset may still contain “sensitive material that has escaped administrative scrutiny.” The creators therefore discuss “the ethics of our work and our proposed mechanisms for content removal” as part of their responsibility to mitigate unforeseen harms【Pile of Law, 2 Pile of Law, p.2‑3】.  

5. **Ensuring Transparency and Ongoing Curation** –  
   Because the dataset is “open‑source, legal‑focused” and intended for future pre‑training, the authors commit to continuously adding material while maintaining “implicit filtering mechanisms formed under relevant legal standards of privacy and toxicity.” This ongoing curation reflects a responsibility to keep the dataset aligned with evolving legal and ethical expectations【Pile of Law, 2 Pile of Law, p.2‑3】.  

In sum, constructing large legal corpora requires careful attention to privacy, copyright, bias, and toxicity; it obliges researchers to embed legally grounded filtering, to actively remove or redact sensitive content, and to maintain transparent, continuously vetted collections.

**Sources**

- *Pile of Law: Learning Responsible Data Filtering from the Law and a 256GB Open‑Source Legal Dataset*, Abstract, p.1.  
- *Pile of Law: Learning Responsible Data Filtering from the Law and a 256GB Open‑Source Legal Dataset*, Section “2 Pile of Law”, pp.2‑3.  
- *Legal Evalutions and Challenges of Large Language Models*, Section A. Data privacy, p.7.

### local

Building large legal datasets carries several important risks and corresponding responsibilities:

* **Risk of exposing sensitive personal information** – Legal documents often contain private details such as identities, financial status, or medical records. When these texts are used to train language models, the models can unintentionally reproduce or leak that information during generation. (Legal Evalutions and Challenges of Large Language Models, A. Data privacy, p.7)

* **Responsibility to protect data‑privacy** – Researchers must design training pipelines that prioritize the protection of confidential data, implement strict safeguards against leakage, and ensure that model outputs do not disclose personal information. (Legal Evalutions and Challenges of Large Language Models, A. Data privacy, p.7)

* **Need for rigorous review and ethical oversight** – A systematic data‑processing and output‑review mechanism is required to minimize privacy risks and to keep the dataset compliant with legal and ethical standards. (Legal Evalutions and Challenges of Large Language Models, A. Data privacy, p.7)

* **Recognition of implicit legal filtering** – Even though the source material is public, each source carries implicit filtering mechanisms derived from privacy and toxicity norms embedded in law. Curators must acknowledge these implicit filters and assess whether any sensitive material has escaped prior administrative scrutiny. (Pile of Law: Learning Responsible Data Filtering from the Law and a 256GB Open‑Source Legal Dataset, 2 Pile of Law, p.2‑3)

* **Responsibility to document and mitigate ethical concerns** – The dataset creators discuss ethics and propose mechanisms for content removal, emphasizing that open‑source legal data, while publicly available, still requires careful handling to avoid harm. (Pile of Law: Learning Responsible Data Filtering from the Law and a 256GB Open‑Source Legal Dataset, 2 Pile of Law, p.2‑3)

* **Obligation to provide transparent licensing and public availability** – All material in the dataset is under open licenses, but curators must ensure that licensing terms are respected and that the dataset is compiled in a way that supports responsible reuse by the community. (Pile of Law: Learning Responsible Data Filtering from the Law and a 256GB Open‑Source Legal Dataset, 2 Pile of Law, p.2‑3)

Together, these points highlight that building large legal corpora demands careful attention to privacy protection, ethical review, acknowledgment of existing legal filters, and transparent, responsible data curation.

**Sources**

* Legal Evalutions and Challenges of Large Language Models, A. Data privacy, p.7 – “Cases in the legal domain often involve individuals' sensitive information… there is a risk that the model may unintentionally expose people' sensitive information… the design and training processes of the model must prioritize the protection of data… implement a rigorous data processing and review mechanism…”.

* Pile of Law: Learning Responsible Data Filtering from the Law and a 256GB Open‑Source Legal Dataset, 2 Pile of Law, p.2‑3 – “Each of these data sources carries with it an implicit filtering mechanism formed under relevant legal standards of privacy and toxicity… we recognize that it may contain sensitive material that has escaped administrative scrutiny… We discuss the ethics of our work and our proposed mechanisms for content removal… All of the content is already entirely public and mostly available under permissive licenses…”.

### global

Building large legal datasets carries several important risks and responsibilities that the literature repeatedly highlights.

* **Bias and unfairness** – Because legal datasets are assembled from many heterogeneous sources, they can encode existing societal biases.  If a model trained on such data is used for case analysis, it may produce biased or discriminatory outputs, which is especially problematic in a domain that demands impartiality【Legal Evalutions and Challenges of Large Language Models, C. Ethical and moral issues, p.8】.  

* **Lack of transparency and interpretability** – Large‑scale legal corpora often lack clear documentation of provenance and annotation procedures.  This opacity makes it difficult for practitioners to understand why a model reaches a particular conclusion, undermining trust in legal decision‑support tools【Legal Evalutions and Challenges of Large Language Models, D. Technical limitations, p.8】.  

* **Legal liability** – When a model trained on a publicly released legal dataset provides advice or analysis that leads to adverse outcomes, it is unclear who is legally responsible.  Developers typically include disclaimer language, but unintended consequences can still arise, leaving open questions about liability for the dataset creators and model providers【Legal Evalutions and Challenges of Large Language Models, B. The definition of legal liability, p.7】.  

* **Data privacy and compliance** – Aggregating large amounts of legal texts (e.g., court opinions, contracts) may involve personal or sensitive information.  Different jurisdictions have varying data‑privacy regulations, so dataset curators must ensure that the collection and release of data comply with all relevant legal requirements to avoid privacy breaches【Legal Evalutions and Challenges of Large Language Models, E. Legislative differences, p.8】.  

* **Responsibility to provide comprehensive resources** – The release of datasets such as LawBench and CUAD is intended to serve as a foundation for future research, which implies a responsibility to maintain high‑quality annotations, open‑source code, and clear licensing so that downstream users can rely on the data responsibly【LawBench: Benchmarking Legal Knowledge of Large Language Models, 5 Conclusion, p.15】;【CUAD: An Expert-Annotated NLP Dataset for Legal Contract Review, 5 Conclusion, p.8】.  

Together, these points illustrate that building large legal datasets is not only a technical undertaking but also an ethical and legal one, requiring careful attention to bias mitigation, transparency, privacy compliance, and clear articulation of liability.  

**Sources**

* Legal Evalutions and Challenges of Large Language Models, C. Ethical and moral issues, p.8 – “Due to the diverse sources of data, these models can introduce biases… ensuring that models remain neutral… urgent concern.”
* Legal Evalutions and Challenges of Large Language Models, D. Technical limitations, p.8 – “Additionally, their lack of interpretability creates uncertainty for legal practitioners…”
* Legal Evalutions and Challenges of Large Language Models, B. The definition of legal liability, p.7 – “The delineation of legal liability when utilizing LLMs for legal advice… remains unclear… unintended consequences can still arise.”
* Legal Evalutions and Challenges of Large Language Models, E. Legislative differences, p.8 – “As LLMs are adopted globally, differences in regulatory policies… can create compliance risks…”
* LawBench: Benchmarking Legal Knowledge of Large Language Models, 5 Conclusion, p.15 – “We hope the release of LawBench can serve as a foundation for future research.”
* CUAD: An Expert-Annotated NLP Dataset for Legal Contract Review, 5 Conclusion, p.8 – “Overall, CUAD can accelerate research towards resolving a major real‑world problem, while also serving as a benchmark…”

### hybrid

**Answer**

Building large legal datasets carries several important risks and responsibilities:

1. **Privacy and Sensitive‑Information Leakage** – Legal documents often contain personal identifiers, financial details, medical records, or other confidential information. If such data are used for pre‑training without proper safeguards, models can unintentionally reproduce or expose that information in generated text, creating data‑leakage hazards. (Legal Evalutions and Challenges of Large Language Models, A. Data privacy, p.7)

2. **Bias, Toxicity and Copyright Concerns** – Pre‑training on massive, unfiltered corpora can embed biased, obscene, copyrighted, or otherwise harmful content in the model. This raises the risk of the model producing disallowed or offensive outputs and of violating intellectual‑property rights. (Pile of Law: Learning Responsible Data Filtering from the Law and a 256 GB Open‑Source Legal Dataset, Abstract, p.1)

3. **Implicit Legal Filtering Mechanisms** – Each source of legal text is typically subject to its own statutory or regulatory filtering (e.g., privacy‑protection rules, toxicity standards). Curators must recognise and respect these implicit filters, and must still apply additional review because some sensitive material may have escaped the original administrative scrutiny. (Pile of Law: Learning Responsible Data Filtering from the Law and a 256 GB Open‑Source Legal Dataset, 2 Pile of Law, p.2)

4. **Ethical Responsibility to Document and Communicate Filtering Policies** – Researchers are expected to make explicit the legal norms that guide what content is removed or retained, and to provide transparent documentation of the filtering process so that downstream users understand the dataset’s provenance and limitations. (Pile of Law: Learning Responsible Data Filtering from the Law and a 256 GB Open‑Source Legal Dataset, 2 Pile of Law, p.2)

5. **Balancing Transparency with Protection** – While open‑source legal data can accelerate access‑to‑justice research, curators must balance the public‑interest goal of transparency against the need to protect private or potentially harmful content, following the same contextual considerations that courts and governments apply. (Pile of Law: Learning Responsible Data Filtering from the Law and a 256 GB Open‑Source Legal Dataset, 2 Pile of Law, p.2)

Together, these points highlight that constructing large‑scale legal corpora is not merely a technical exercise; it requires careful legal analysis, privacy‑preserving practices, bias mitigation, and clear ethical documentation.

**Sources**

- (Legal Evalutions and Challenges of Large Language Models, A. Data privacy, p.7)  
- (Pile of Law: Learning Responsible Data Filtering from the Law and a 256 GB Open‑Source Legal Dataset, Abstract, p.1)  
- (Pile of Law: Learning Responsible Data Filtering from the Law and a 256 GB Open‑Source Legal Dataset, 2 Pile of Law, p.2)


---

## Q4. How did legal NLP methods change with the arrival of large language models?

### plain

**Answer**

The emergence of large language models (LLMs) has shifted legal‑NLP from relatively narrow, task‑specific tools toward much larger, more general‑purpose systems that are then fine‑tuned for legal work.  

* **From specialized pipelines to end‑to‑end models** – Earlier legal‑NLP relied on separate components (tokenizers, rule‑based extractors, classifiers, etc.) that were assembled to handle a single function such as entity extraction or case‑law retrieval.  With LLMs, a single model can perform many of these functions (understanding terminology, reasoning over provisions, generating text) in one pass, reducing the need for hand‑crafted pipelines.  

* **Domain‑specific pre‑training and fine‑tuning** – Researchers now start with massive, general‑purpose LLMs and then continue pre‑training or fine‑tune them on large legal corpora (e.g., Chinese legal texts, the “Pile of Law”, or curated Q&A datasets).  This produces legal‑specific models such as **LawGPT**, **ChatLaw**, **LAWGPT‑zh**, **Lawyer‑LLama**, **LexiLaw**, and **KL3M**, which show “superior capabilities in understanding legal concepts, conducting legal reasoning, and generating legal text” compared with earlier, non‑legal‑specific systems.  

* **Improved capabilities but new limitations** – The new models can handle tasks that previously required separate tools—summarization, drafting, legal research, and even zero‑shot reasoning for crime detection.  However, evaluations still reveal weaknesses: modest micro‑F1 scores on classification benchmarks, factual inaccuracies in legislative explanations, and quality inconsistencies in abstractive summarization.  These findings highlight that while LLMs broaden what is possible, they also introduce new challenges such as hallucination and the need for better domain‑specific supervision.  

* **Integration of retrieval and reasoning components** – Modern legal LLMs often combine the generative model with external knowledge sources (vector databases, knowledge graphs, retrieval‑augmented generation) to reduce hallucinations and improve factual grounding, a step that was not common in earlier purely statistical or rule‑based approaches.  

Overall, the arrival of LLMs has transformed legal NLP from a collection of isolated, narrowly scoped techniques into a unified, adaptable framework that leverages massive pre‑training, domain‑specific fine‑tuning, and retrieval‑augmented reasoning, while also prompting fresh research on accuracy, bias, and ethical concerns.

**Sources**

- (Legal Evalutions and Challenges of Large Language Models, C. Overview of legal‑specific LLMs, p.5) – Describes fine‑tuned legal models (LexNLP, LawGPT, ChatLaw) and their superior legal reasoning capabilities.  
- (Legal Evalutions and Challenges of Large Language Models, I. INTRODUCTION, p.1‑2) – Notes the shift toward LLMs in legal practice, the need for specialization, and the challenges of evaluating them across legal systems.  
- (Legal Evalutions and Challenges of Large Language Models, II. REVIEW OF LLMS IN THE LEGAL FIELD, p.2‑3) – Details the move from earlier NLP tasks to LLM‑driven summarization, drafting, research, and retrieval‑augmented methods, and cites performance limitations of early LLM evaluations.

### local

Legal natural‑language‑processing (NLP) has shifted from rule‑based or narrowly‑focused models toward the use of large, transformer‑based language models that can be fine‑tuned on legal corpora.  Early in the survey the authors note that the “breakthrough of deep learning technology in natural language processing (NLP), particularly the rapid advancement of Transformer technology, has led to the flourishing of LLMs” and that “in the legal field, LLMs are seen as a transformative force with the potential to revolutionize traditional legal services, owing to their comprehensive legal knowledge base and exceptional capabilities in natural language understanding and generation”【Legal Evalutions and Challenges of Large Language Models, I. INTRODUCTION, p.1‑2】.  

Subsequent analysis describes how these models are now being applied to core legal‑NLP tasks:  
* **Summarization** – generating concise contract or case‑opinion summaries【Legal Evalutions and Challenges of Large Language Models, II. REVIEW OF LLMS IN THE LEGAL FIELD, p.2‑3】.  
* **Drafting** – suggesting language improvements, modifying clauses, and producing initial document drafts【Legal Evalutions and Challenges of Large Language Models, II. REVIEW OF LLMS IN THE LEGAL FIELD, p.2‑3】.  
* **Legal research** – answering queries in plain language, synthesizing case law, and producing research memoranda【Legal Evalutions and Challenges of Large Language Models, II. REVIEW OF LLMS IN THE LEGAL FIELD, p.2‑3】.  

The arrival of LLMs also introduced new methodological concerns.  Researchers now evaluate models on multilingual benchmark suites (e.g., Chinese and U.S. case datasets) and report systematic testing that “LLMs often misinterpret legal language, resulting in inaccurate legal reasoning”【Legal Evalutions and Challenges of Large Language Models, II. REVIEW OF LLMS IN THE LEGAL FIELD, p.2‑3】.  Domain‑specific fine‑tuning improves handling of legal terminology, but “does not fully close the performance gap with larger, general‑purpose models” and “legal language’s high specialization and precision cause LLMs to generate content with non‑negligible factual and legal inaccuracies”【Legal Evalutions and Challenges of Large Language Models, I. INTRODUCTION, p.1‑2】.  

Finally, specialized legal LLMs (e.g., LexNLP, LawGPT, ChatLaw) have been built with modular architectures, knowledge‑graph integration, and retrieval‑augmented pipelines to reduce hallucinations and increase reliability【Legal Evalutions and Challenges of Large Language Models, C. Overview of legal‑specific LLMs, p.5‑5】.  

In sum, the arrival of large language models has expanded the scope of legal NLP from narrow, task‑specific tools to versatile, generative systems capable of summarization, drafting, and research, while also prompting new evaluation frameworks and mitigation strategies to address persistent accuracy and hallucination challenges.  

**Sources**  
- Legal Evalutions and Challenges of Large Language Models, I. INTRODUCTION, p.1‑2 – “In recent years, the breakthrough of deep learning technology in natural language processing (NLP), particularly the rapid advancement of Transformer technology… In the legal field, LLMs are seen as a transformative force…”.  
- Legal Evalutions and Challenges of Large Language Models, II. REVIEW OF LLMS IN THE LEGAL FIELD, p.2‑3 – Descriptions of summarization, drafting, and legal‑research applications, and the note that “LLMs often misinterpret legal language, resulting in inaccurate legal reasoning”.  
- Legal Evalutions and Challenges of Large Language Models, C. Overview of legal‑specific LLMs, p.5‑5 – Details on LexNLP, LawGPT, ChatLaw and their modular, retrieval‑augmented designs.

### global

Legal NLP methods have shifted markedly since large language models (LLMs) became widely available.  

* **Benchmarking and evaluation** – New, comprehensive benchmarks such as LEGALBENCH, LawBench, and CUAD have been created specifically to measure LLM‑based legal reasoning, issue‑spotting, rule‑application, and contract‑review performance (e.g., “LEGALBENCH: A COLLABORATIVELY BUILT BENCHMARK …” and “LawBench: Benchmarking Legal Knowledge …”) [LEGALBENCH: A COLLABORATIVELY BUILT BENCHMARK FOR MEASURING LEGAL REASONING IN LARGE LANGUAGE MODELS, 1 Introduction, p.4]; [LawBench: Benchmarking Legal Knowledge of Large Language Models, Abstract, p.1].  

* **Performance gains** – Closed‑source LLMs such as GPT‑4 now outperform earlier models on many legal tasks, especially interpretation and multi‑step reasoning, while open‑source models can be competitive on specific categories (e.g., “On the interpretation tasks, we find that on average GPT‑4 outperforms GPT‑3.5” [LEGALBENCH …, 5.3.5 Interpretation, p.17]; “Notably, GPT‑4 possesses emergent abilities … leading to more flexible and powerful task handling” [Legal Evalutions and Challenges of Large Language Models, A. Overview of leading non-open source LLMs, p.3]; “in some cases, their performance is on par with closed‑source models” [Legal Evalutions and Challenges of Large Language Models, B. Overview of leading open source LLMs, p.4]).  

* **Few‑shot and instruction‑tuning** – LLMs enable few‑shot prompting, allowing a single model to address many legal tasks without task‑specific fine‑tuning, a capability highlighted as missing from earlier benchmarks [LEGALBENCH …, 1 Introduction, p.4]. Instruction‑tuned variants (e.g., Incite‑7B‑Instruct) improve performance on several categories such as issue‑spotting and interpretation [LEGALBENCH …, 5.2 Performance trends, p.13].  

* **Adaptation strategies** – Researchers have explored lightweight adaptation methods (adapters, BITFIT, LNFIT) that fine‑tune only a tiny fraction of parameters yet remain competitive, showing that full model retraining is not always required [MultiEURLEX …, 4 Methods > 4.2 Cross‑lingual Adaptation Strategies, p.5]; “Interestingly, even adaptation strategies (BITFIT, LNFIT) that fine‑tune a very small fraction of parameters (<0.05%) are competitive” [MultiEURLEX …, 7 Conclusions and Future Work, p.9].  

* **Cross‑lingual transfer** – Zero‑shot cross‑lingual transfer has been investigated for legal document classification, demonstrating that multilingual LLMs can be adapted to many languages with modest gains [MultiEURLEX …, 6.2 Cross‑lingual Transfer (one‑to‑many), p.6]; “cross‑lingual transfer has not yet been explored in legal NLP” [MultiEURLEX …, 1 Introduction, p.1] indicating a new research direction opened by LLMs.  

* **Retrieval and RAG** – Legal retrieval benchmarks reveal that traditional lexical retrievers (e.g., BM25) struggle, prompting the use of dense retrieval and generative query‑expansion techniques alongside LLMs [A Reasoning‑Focused Legal Retrieval Benchmark, 1 Introduction, p.1]; “Our results suggest that legal RAG remains a challenging application” [A Reasoning‑Focused Legal Retrieval Benchmark, Abstract, p.1].  

* **Limitations and ethical concerns** – Despite gains, LLMs still have difficulty interpreting complex legal language, exhibit bias, and raise questions about liability and transparency [Legal Evalutions and Challenges of Large Language Models, VI. DISCUSSION, p.8]; “Their lack of interpretability creates uncertainty for legal practitioners” [Legal Evalutions and Challenges of Large Language Models, D. Technical limitations, p.8].  

Overall, the arrival of LLMs has expanded legal NLP from narrow, task‑specific models to versatile, few‑shot, and adaptable systems, spurred new benchmark creation, introduced novel adaptation techniques, and highlighted both performance improvements and persistent challenges.  

**Sources**  
- LEGALBENCH: A COLLABORATIVELY BUILT BENCHMARK FOR MEASURING LEGAL REASONING IN LARGE LANGUAGE MODELS, 1 Introduction, p.4  
- LEGALBENCH: A COLLABORATIVELY BUILT BENCHMARK FOR MEASURING LEGAL REASONING IN LARGE LANGUAGE MODELS, 5.3.5 Interpretation, p.17  
- LEGALBENCH: A COLLABORATIVELY BUILT BENCHMARK FOR MEASURING LEGAL REASONING IN LARGE LANGUAGE MODELS, 5.2 Performance trends, p.13  
- LEGALBENCH: A COLLABORATIVELY BUILT BENCHMARK FOR MEASURING LEGAL REASONING IN LARGE LANGUAGE MODELS, Table 6, p.14  
- Legal Evalutions and Challenges of Large Language Models, A. Overview of leading non-open source LLMs, p.3  
- Legal Evalutions and Challenges of Large Language Models, B. Overview of leading open source LLMs, p.4  
- Legal Evalutions and Challenges of Large Language Models, VI. DISCUSSION, p.8  
- Legal Evalutions and Challenges of Large Language Models, D. Technical limitations, p.8  
- LawBench: Benchmarking Legal Knowledge of Large Language Models, Abstract, p.1  
- LawBench: Benchmarking Legal Knowledge of Large Language Models, 5 Conclusion, p.15  
- MultiEURLEX -A multi-lingual and multi-label legal document classification dataset for zero-shot cross-lingual transfer, 4 Methods > 4.2 Cross‑lingual Adaptation Strategies, p.5  
- MultiEURLEX -A multi-lingual and multi-label legal document classification dataset for zero-shot cross-lingual transfer, 6.2 Cross‑lingual Transfer (one‑to‑many), p.6  
- MultiEURLEX -A multi-lingual and multi-label legal document classification dataset for zero-shot cross-lingual transfer, 7 Conclusions and Future Work, p.9  
- A Reasoning‑Focused Legal Retrieval Benchmark, 1 Introduction, p.1  
- A Reasoning‑Focused Legal Retrieval Benchmark, Abstract, p.1

### hybrid

Legal NLP has been transformed by the arrival of large‑language models (LLMs).  Early work focused on modest, task‑specific fine‑tuning of BERT‑style encoders, but the new generation of LLMs introduced several new methodological shifts:

* **Scale‑driven performance gains** – Researchers found that increasing model size consistently improves one‑shot legal reasoning, even if the gains are modest compared to scaling the amount of training data (LawBench, “Scaling up the model size results in better performance in one‑shot case” — LawBench, 4 Experiment > 4.4 Analysis, p.13).  

* **Data quantity as the dominant bottleneck** – Across many benchmarks (LegalBench, Multi‑EUR‑LEX, CUAD) the community observed that adding more labeled legal examples yields larger performance jumps than changing model families or architectures (Legal NL P Benchmarks and Model Adaptation, Summary – “data quantity is a primary bottleneck” — Legal NL P Benchmarks and Model Adaptation, p. – summary).  

* **Lightweight adaptation methods** – Techniques that fine‑tune only a tiny fraction of parameters (BITFIT, LNFIT, adapters) achieve competitive zero‑shot cross‑lingual transfer, preserving multilingual knowledge while requiring far less compute (Multi‑EUR‑LEX, “BITFIT (Zaken et al., 2021) keeps the whole network frozen during fine‑tuning, except for bias terms.” — Multi‑EUR‑LEX, 4 Methods > 4.2 Cross‑lingual Adaptation Strategies, p.5; “Interestingly, even adaptation strategies (BITFIT, LNFIT) that fine‑tune a very small fraction of parameters (<0.05%) are competitive.” — Multi‑EUR‑LEX, 7 Conclusions and Future Work, p.9).  

* **Progressive and reinforcement‑learning fine‑tuning pipelines** – Adding reinforcement learning from human feedback (RLHF) and staged fine‑tuning (single‑stage SFT → progressive SFT) yields further gains on English legal tasks (Evaluating Test‑Time Scaling LLMs, Table 7: “Progressive SFT” improves most tasks) — Evaluating Test‑Time Scaling LLMs, Table 7, p.9.  

* **Few‑shot and zero‑shot evaluation becomes central** – Many legal benchmarks (LegalBench, Multi‑EUR‑LEX) previously lacked few‑shot splits; the community now emphasizes few‑shot testing to stress the ability of LLMs to generalize from very little task‑specific data (Legal NL P Benchmarks and Model Adaptation, Summary – “many legal benchmarks lack few‑shot evaluation, making them valuable testbeds for few‑shot research” — Legal NL P Benchmarks and Model Adaptation, p. – summary).  

* **Multilingual joint fine‑tuning outperforms one‑to‑many** – Training a single model on all languages simultaneously (many‑to‑many) consistently beats separate language‑specific fine‑tuning, because the model can leverage annotated data across languages (Multi‑EUR‑LEX, “In the lower part of Table 5… many‑to‑many models largely outperform the one‑to‑many models” — Multi‑EUR‑LEX, 6.3 Multilingual Fine‑tuning (many‑to‑many), p.9).  

* **Domain‑specific pre‑training adds only modest benefit** – Pre‑training on large unlabeled legal corpora (e.g., contracts) yields small improvements compared with scaling data or model size (Legal NL P Benchmarks and Model Adaptation, Summary – “domain‑specific pre‑training on unlabeled contracts adds only a small improvement” — Legal NL P Benchmarks and Model Adaptation, p. – summary).  

* **Open‑source models close the gap** – Open‑source LLMs (e.g., Llama 3, Mistral Large, Gemma 2) now achieve performance that rivals commercial models on many tasks, though gaps remain on complex rule‑conclusion tasks (Legal Benchmarks and Model Adaptation, Summary – “lightweight adaptation methods… achieve competitive zero‑shot results” and “open‑source LLMs such as Llama 3, Mistral Large, and Qwen2 can achieve state‑of‑the‑art performance” — Legal Benchmarks and Model Adaptation, p. – summary; LEGALBENCH, 5.2 Performance trends, p.13).  

* **Toolkits for legal text processing emerge** – Specialized libraries such as LexNLP provide modular pipelines for cleaning, tokenizing, and extracting legal entities, enabling rapid prototyping of legal NLP applications (Legal Evalutions and Challenges of Large Language Models, C. Overview of legal‑specific LLMs, p.5).  

Overall, the advent of LLMs has shifted legal NLP from narrowly‑tuned, small‑scale models toward large, adaptable architectures that benefit from massive data, parameter‑efficient adaptation, multilingual joint training, and progressive fine‑tuning strategies, while also spurring the creation of open‑source tools and benchmarks to measure these advances.  

**Sources**

- LawBench, 4 Experiment > 4.4 Analysis, p.13.  
- Legal NL P Benchmarks and Model Adaptation, Summary, p. – summary.  
- Multi‑EUR‑LEX, 4 Methods > 4.2 Cross‑lingual Adaptation Strategies, p.5.  
- Multi‑EUR‑LEX, 7 Conclusions and Future Work, p.9.  
- Evaluating Test‑Time Scaling LLMs for Legal Reasoning, Table 7: English Legal Tasks Performance, p.9.  
- LEGALBENCH, 5.2 Performance trends, p.13.  
- Multi‑EUR‑LEX, 6.3 Multilingual Fine‑tuning (many‑to‑many), p.9.  
- Legal Evalutions and Challenges of Large Language Models, C. Overview of legal‑specific LLMs, p.5.


---

## Q5. Does making a model bigger reliably improve legal task performance?

### plain

**Answer**

Increasing a model’s size tends to improve legal‑task performance, but the improvement is not guaranteed in every setting.  

* In the **LawBench** study, larger models generally achieve higher scores and lower abstention rates in *one‑shot* scenarios, indicating that scaling helps when a few examples are provided. However, the same trend is weaker in *zero‑shot* conditions, and there are notable exceptions (e.g., the larger ChatLaw model performed worse than its smaller counterpart). The authors conclude that “simply increasing the model size may not automatically lead to better performance” in zero‑shot cases.  

* The **LEGALBENCH** analysis reports that “within LLM families, larger models usually outperform smaller models” across most reasoning categories, though the size‑related gap varies by family and task. This suggests a positive but not uniform effect of scaling.

Taken together, the evidence shows that **model size is a strong factor for better performance, especially when some prompting (one‑shot) is used, but it is not a reliable guarantee across all tasks or evaluation settings**.

---

**Sources**

1. *LawBench: Benchmarking Legal Knowledge of Large Language Models*, Section 4.4 Analysis, pp. 13‑15.  
   - “Scaling up the model size results in better performance in one-shot case… In zero-shot scenarios, mixed results are observed, simply increasing the model size may not automatically lead to better performance.”  

2. *LEGALBENCH: A Collaboratively Built Benchmark for Measuring Legal Reasoning in Large Language Models*, Section 5.2 Performance trends, pp. 13‑15.  
   - “Within LLM families, we observe that larger models usually outperform smaller models… the margin of the gap varies across LLM families and reasoning categories.”

### local

Increasing the size of a language model tends to raise its legal‑task performance, but the improvement is not guaranteed in every setting.

* **LawBench (LawBench: Benchmarking Legal Knowledge of Large Language Models)** reports that scaling up model size “usually improves the performance, but the improvement is more consistent in the one‑shot than in the zero‑shot scenario” and that larger models have lower abstention rates, indicating better instruction following. However, the paper also notes mixed results in zero‑shot settings and cites an outlier (ChatLaw) where a larger model performed worse【LawBench: Benchmarking Legal Knowledge of Large Language Models, 4 Experiment > 4.4 Analysis, p.13‑15】.  

* **LEGALBENCH (LEGALBENCH: A COLLABORATIVELY BUILT BENCHMARK FOR MEASURING LEGAL REASONING IN LARGE LANGUAGE MODELS)** finds that “within LLM families, larger models usually outperform smaller models” across most reasoning categories, though the margin varies by family and task【LEGALBENCH: A COLLABORATIVELY BUILT BENCHMARK FOR MEASURING LEGAL REASONING IN LARGE LANGUAGE MODELS, 5.2 Performance trends, p.13‑15】.

Together, the evidence suggests that larger models generally achieve higher scores on legal benchmarks, especially in one‑shot or within‑family comparisons, but the benefit can be inconsistent for zero‑shot evaluations or specific model families.

**Sources**

* LawBench: Benchmarking Legal Knowledge of Large Language Models, 4 Experiment > 4.4 Analysis, p.13‑15 – “scaling up the model size results in better performance in one‑shot case… scaling up the model size usually improves the performance, but the improvement is more consistent in the one‑shot than in the zero‑shot scenario… mixed results are observed… ChatLaw is an outlier…”.
* LEGALBENCH: A COLLABORATIVELY BUILT BENCHMARK FOR MEASURING LEGAL REASONING IN LARGE LANGUAGE MODELS, 5.2 Performance trends, p.13‑15 – “Within LLM families, larger models usually outperform smaller models…”.

### global

The provided passages do not contain a clear, systematic claim that increasing a model’s size (e.g., using more parameters) reliably leads to better performance on legal tasks. The excerpts include performance tables for specific models (such as Gemma2‑9B) and observations that some open‑source models can be “on par with closed‑source models,” but they do not present a general relationship between model scale and legal‑task accuracy across multiple model families.

**Sources**

- The tables showing performance of Gemma2‑9B on English and Chinese legal texts report its scores but do not compare them to larger or smaller variants, so no conclusion about size can be drawn from them. [Legal Evalutions and Challenges of Large Language Models, TABLE II PERFORMANCE OF LLMS ON ENGLISH LEGAL TEXTS, p.7]  
- The statement that “in some cases, their performance is on par with closed‑source models” refers to open‑source models generally, without linking performance to model size. [Legal Evalutions and Challenges of Large Language Models, B. Overview of leading open source LLMs, p.4]  

Since the context lacks a direct assessment of how model size affects legal task performance, a reliable answer cannot be given from the available information.

### hybrid

Increasing a model’s parameter count can help, but it does not guarantee better performance on every legal benchmark.  

* On the CUAD contract‑review benchmark, the very large DeBERTa‑xlarge model attains a 44 % Precision@80 % Recall, far surpassing BERT‑base (8.2 %) and BERT‑large (7.6 %) and being the only model with non‑zero Precision@90 % Recall. This shows that a larger, more recent architecture can markedly improve precision at high recall levels (CUAD, 4.2 Results, p.7).  

* However, scaling does not always translate into gains. In the LawBench analysis the authors observe that “scaling up the model size results in better performance in one‑shot case… In zero‑shot scenarios, mixed results are observed, simply increasing the model size may not automatically lead to better performance” (LawBench, 4 Experiment > 4.4 Analysis, p.13).  

* Moreover, a 20‑fold increase in parameters for ALBERT yields only about a 3 % improvement in AUPR, and BERT‑large shows negligible improvement over BERT‑base (CUAD, Table 2, p.6).  

Taken together, the evidence suggests that larger models often perform better—especially in one‑shot settings and when the architecture is substantially upgraded—but the benefit is not uniform across tasks, datasets, or evaluation regimes. Model size alone is therefore not a reliable guarantee of higher legal‑task performance.  

**Sources**  
- CUAD: An Expert‑Annotated NLP Dataset for Legal Contract Review, 4 Experiments > 4.2 Results, p.7  
- CUAD: An Expert‑Annotated NLP Dataset for Legal Contract Review, Table 2, p.6  
- LawBench: Benchmarking Legal Knowledge of Large Language Models, 4 Experiment > 4.4 Analysis, p.13
