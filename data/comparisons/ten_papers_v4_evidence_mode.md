# Retrieval comparison — 2026-08-13 15:10

Answering model `openai/gpt-oss-120b` at temperature 0.0, embeddings `openai/text-embedding-3-small`, top_k=5. Extraction ran on `openai/gpt-oss-120b`.

- **plain** — nearest chunks only, no graph. The control.
- **local** — nearest chunks, plus the claims each one grounds.
- **global** — community summaries only.
- **hybrid** — community summaries, plus each theme's claims and the verbatim passage behind them, plus the nearest chunks.
- **evidence** — the verbatim spans nearest the question, at most two per paper.


---

## Q1. How do multilingual or cross-lingual legal NLP tasks differ from English-only ones?

### plain

Multilingual and cross‑lingual legal NLP tasks differ from English‑only (monolingual) tasks in several ways that are highlighted by the MultiEURLEX papers:

* **Scope of languages** – While most prior legal‑topic work has been limited to English legislation (e.g., “Legal topic classification has been studied for EU legislation … in a monolingual setting (English)”) (“MultiEURLEX – Related Work”, p.2‑3), MultiEURLEX expands the problem to **23 official EU languages** covering seven language families (Fig. 1) (“MultiEURLEX – Introduction”, p.1‑2).

* **Zero‑shot cross‑lingual transfer** – The multilingual setting aims to **reuse a classifier trained on a resource‑rich source language to classify documents in a target language that has no labeled data**. This is framed as “zero‑shot cross‑lingual transfer” and is used as the main testbed for the dataset (“MultiEURLEX – Abstract”, p.1‑1; “MultiEURLEX – Introduction”, p.1‑2).

* **Model adaptation challenges** – Fine‑tuning a multilingual pretrained model on a single source language causes **catastrophic forgetting of multilingual knowledge**, leading to poor transfer performance (“MultiEURLEX – Abstract”, p.1‑1; “MultiEURLEX – Introduction”, p.1‑2). To mitigate this, the authors explore **adaptation strategies** such as partial fine‑tuning, adapters, BITFIT, and LNFIT, which are not required for English‑only experiments.

* **Temporal concept drift** – Because the dataset spans many years, the authors note that **chronological splits are needed** to reflect real‑world drift, whereas many English‑only studies use random splits that can over‑estimate performance (“MultiEURLEX – Introduction”, p.1‑2; “MultiEURLEX – Conclusions”, p.9).

* **Evaluation of multilingual vs. monolingual models** – Experiments show that **multilingual models can be competitive with monolingual ones** in a one‑to‑one set‑up, and a single multilingual model jointly fine‑tuned on all languages can also perform well (“MultiEURLEX – Conclusions”, p.9). This comparison is unnecessary in English‑only work.

In short, multilingual/cross‑lingual legal NLP must handle many languages, rely on zero‑shot transfer, address catastrophic forgetting through adaptation techniques, and consider temporal drift, whereas English‑only tasks operate in a single‑language, often static setting without these additional complexities.

**Sources**

1. *MultiEURLEX – A multi‑lingual and multi‑label legal document classification dataset for zero‑shot cross‑lingual transfer*, **Related Work**, pp. 2‑3.  
2. *MultiEURLEX – A multi‑lingual and multi‑label legal document classification dataset for zero‑shot cross‑lingual transfer*, **Introduction**, pp. 1‑2.  
3. *MultiEURLEX – A multi‑lingual and multi‑label legal document classification dataset for zero‑shot cross‑lingual transfer*, **Abstract**, p. 1.  
4. *MultiEURLEX – A multi‑lingual and multi‑label legal document classification dataset for zero‑shot cross‑lingual transfer*, **Conclusions and Future Work**, p. 9.

### local

Multilingual or cross‑lingual legal NLP tasks differ from English‑only ones in several ways.  

* **Scope of languages and data** – English‑only research on legal topic classification has traditionally used monolingual corpora of EU legislation (e.g., Chalkidis et al., 2019) and other English datasets, whereas multilingual work must handle documents that are officially translated into many languages (23 EU languages in MULTI‑EURLEX) and often relies on parallel or comparable corpora to enable cross‑lingual learning【MultiEURLEX –A multi‑lingual and multi‑label legal document classification dataset for zero‑shot cross‑lingual transfer, 2 Related Work, p.2‑3】.  

* **Cross‑lingual transfer setting** – In multilingual settings the goal is to train a model on labeled data in one (or several) source language(s) and then apply it to target languages without any target‑language annotations (zero‑shot transfer). This contrasts with English‑only tasks where training and testing are performed in the same language【MultiEURLEX –A multi‑lingual and multi‑label legal document classification dataset for zero‑shot cross‑lingual transfer, 1 Introduction, p.1‑2】.  

* **Model adaptation challenges** – Fine‑tuning a multilingual pretrained model (e.g., XLM‑ROBERTA, MT5) on a single source language tends to cause catastrophic forgetting of the multilingual knowledge that the model acquired during pre‑training, leading to poor performance on unseen languages. English‑only fine‑tuning does not face this issue because the model is not required to retain knowledge for other languages【MultiEURLEX –A multi‑lingual and multi‑label legal document classification dataset for zero‑shot cross‑lingual transfer, Abstract, p.1】.  

* **Adaptation strategies** – To mitigate forgetting, multilingual legal NLP employs adaptation techniques such as partial fine‑tuning, adapters, BITFIT, and LNFIT, which selectively update only a small subset of parameters and preserve multilingual representations. These strategies are unnecessary for English‑only tasks, where standard full fine‑tuning suffices【MultiEURLEX –A multi‑lingual and multi‑label legal document classification dataset for zero‑shot cross‑lingual transfer, 1 Introduction, p.1‑2】.  

* **Temporal concept drift** – Multilingual legal corpora span many years and languages, making temporal concept drift a pronounced problem; chronological train/dev/test splits are required to obtain realistic estimates of performance. English‑only datasets often use random splits, which can over‑estimate results because they ignore such drift【MultiEURLEX –A multi‑lingual and multi‑label legal document classification dataset for zero‑shot cross‑lingual transfer, 1 Introduction, p.1‑2】.  

* **Evaluation setups** – Multilingual legal NLP evaluates both “one‑to‑many” (train in one language, test in many) and “many‑to‑many” (joint training across languages) scenarios, whereas English‑only work evaluates only monolingual setups【MultiEURLEX –A multi‑lingual and multi‑label legal document classification dataset for zero‑shot cross‑lingual transfer, Abstract, p.1】.  

These differences reflect the additional linguistic, methodological, and evaluation complexities introduced when extending legal NLP beyond English.  

**Sources**  

- MultiEURLEX –A multi‑lingual and multi‑label legal document classification dataset for zero‑shot cross‑lingual transfer, 2 Related Work, p.2‑3.  
- MultiEURLEX –A multi‑lingual and multi‑label legal document classification dataset for zero‑shot cross‑lingual transfer, 1 Introduction, p.1‑2.  
- MultiEURLEX –A multi‑lingual and multi‑label legal document classification dataset for zero‑shot cross‑lingual transfer, Abstract, p.1.

### global

Multilingual or cross‑lingual legal NLP tasks involve additional challenges and opportunities that are not present in English‑only settings.  

* **Data availability** – Many legal corpora exist only for a single language, and cross‑lingual transfer has rarely been studied in the legal domain. The authors of the MultiEURLEX benchmark note that “cross‑lingual transfer has not yet been explored in legal NLP” (MultiEURLEX – A multi‑lingual and multi‑label legal document classification dataset for zero‑shot cross‑lingual transfer, 1 Introduction, p.1).  

* **Training strategies** – When documents are available in several languages, models can be fine‑tuned jointly across languages. In the MultiEURLEX study, a “many‑to‑many” multilingual fine‑tuning regime randomly selects a language for each batch and shows that adapter modules “consistently improve performance” (MultiEURLEX – …, 6.3 Multilingual Fine‑tuning (many‑to‑many), p.9).  

* **Zero‑shot cross‑lingual adaptation** – Even without any target‑language training data, adding a lightweight adaptation layer can raise performance. The same benchmark reports that “adaptation zero‑shot (All) performance … improves compared to no adaptation (end‑to‑end fine‑tuning), approx. +0.3 → +1.6 → +4.2 → +3.6” (MultiEURLEX – …, 6.2 Cross‑lingual Transfer (one‑to‑many), p.6).  

* **Parameter efficiency** – Some cross‑lingual adaptation methods (e.g., BITFIT, LNFIT) fine‑tune only a tiny fraction of parameters (<0.05 %) yet remain competitive, highlighting that effective multilingual transfer can be achieved with very few trainable weights (MultiEURLEX – …, 7 Conclusions and Future Work, p.9).  

Together, these points illustrate that multilingual legal NLP must contend with heterogeneous language coverage, rely on joint or adapter‑based fine‑tuning to share knowledge across languages, and can achieve meaningful zero‑shot gains even when target‑language data are scarce—issues that do not arise in purely English‑only tasks.  

**Sources**  
- MultiEURLEX – A multi‑lingual and multi‑label legal document classification dataset for zero‑shot cross‑lingual transfer, 1 Introduction, p.1  
- MultiEURLEX – …, 6.3 Multilingual Fine‑tuning (many‑to‑many), p.9  
- MultiEURLEX – …, 6.2 Cross‑lingual Transfer (one‑to‑many), p.6  
- MultiEURLEX – …, 7 Conclusions and Future Work, p.9

### hybrid

Multilingual and cross‑lingual legal NLP tasks pose challenges that are largely absent from English‑only benchmarks.  

* **Zero‑shot transfer** – The goal is to train a classifier on a resource‑rich language (usually English) and then apply it to documents in many other languages without any target‑language training data.  This requires the model to retain the multilingual knowledge it acquired during pre‑training, which is not an issue for monolingual English tasks that are evaluated only on the language they were trained on. (Multi‑EURLEX, 1 Introduction, p.1)  

* **Catastrophic forgetting** – Fine‑tuning a multilingual model on a single source language quickly erodes the multilingual representations, leading to very poor performance on the target languages.  English‑only datasets do not suffer from this problem because they never leave the English sub‑space. (Multi‑EURLEX, 1 Introduction, p.1)  

* **Adaptation strategies** – To mitigate forgetting, researchers use partial fine‑tuning, adapters, BITFIT or LNFIT, which keep most of the pretrained multilingual parameters fixed while only updating a small subset.  These techniques are unnecessary for English‑only tasks, where standard fine‑tuning suffices. (Multi‑EURLEX, 7 Conclusions, p.9)  

* **Lexical overlap** – Even within English‑only benchmarks such as Bar Exam QA and Housing Statute QA, the queries and relevant passages have extremely low TF‑IDF cosine similarity (means of 0.07–0.08), forcing models to perform multi‑hop and analogical reasoning rather than rely on surface word matching.  Multilingual benchmarks add a further layer of difficulty because the same low‑overlap reasoning must be carried out across many languages with different vocabularies and scripts. (A Reasoning‑Focused Legal Retrieval Benchmark, 1 Introduction, p.1; 4 Comparison to Existing Tasks, p.4)  

* **Resource scarcity** – Hand‑annotated passage‑pair retrieval datasets are rare for English legal retrieval, and even scarcer for other languages, which makes multilingual evaluation harder and motivates the creation of large parallel corpora such as MULTI‑EURLEX (65 k EU laws in 23 languages).  English‑only tasks can rely on smaller, single‑language collections. (A Reasoning‑Focused Legal Retrieval Benchmark, 3 Datasets, p.2)  

In sum, multilingual legal NLP must handle cross‑lingual transfer, preserve multilingual knowledge during fine‑tuning, and operate on parallel corpora with many languages, whereas English‑only tasks focus solely on monolingual reasoning and do not need these additional adaptation mechanisms.  

**Sources**  
- Multi‑EURLEX – “Multilingual learning is an active field of research … cross‑lingual transfer …” (Multi‑EURLEX, 1 Introduction, p.1)  
- Multi‑EURLEX – “We find that fine‑tuning a multilingual model in a single source language leads to catastrophic forgetting …” (Multi‑EURLEX, 1 Introduction, p.1)  
- Multi‑EURLEX – “Adaptation strategies … help retain multilingual knowledge … substantially improving zero‑shot cross‑lingual transfer” (Multi‑EURLEX, 7 Conclusions, p.9)  
- A Reasoning‑Focused Legal Retrieval Benchmark – “We show that relative to existing benchmarks, ours captures query‑document distributions where the lexical similarity between the query and document is low.” (A Reasoning‑Focused Legal Retrieval Benchmark, 1 Introduction, p.1)  
- A Reasoning‑Focused Legal Retrieval Benchmark – “while those distributions for Bar Exam QA and Housing Statute QA are heavily skewed towards similarities < 0.10, with mean similarities of 0.07 and 0.08 (Table 2).” (A Reasoning‑Focused Legal Retrieval Benchmark, 4 Comparison to Existing Tasks, p.4)  
- A Reasoning‑Focused Legal Retrieval Benchmark – “To our knowledge, few (if any) English legal retrieval datasets were constructed with hand‑annotated passage pairs; existing datasets cover French or Chinese law.” (A Reasoning‑Focused Legal Retrieval Benchmark, 3 Datasets, p.2)

### evidence

Multilingual or cross‑lingual legal NLP tasks face challenges that are largely absent from English‑only tasks.  
First, cross‑lingual transfer for legal text has not been investigated, meaning that methods for leveraging knowledge from one language to another are still missing in the legal domain【MultiEURLEX -A multi-lingual and multi-label legal document classification dataset for zero-shot cross-lingual transfer, 1 Introduction, p.1】.  
Second, existing benchmarks such as LEGALBENCH focus exclusively on English and are heavily weighted toward American contract law, which restricts the ability to assess how models generalize to other jurisdictions, legal systems, or languages【LEGALBENCH: A COLLABORATIVELY BUILT BENCHMARK FOR MEASURING LEGAL REASONING IN LARGE LANGUAGE MODELS, 4.1 Construction process, p.9】.  

Together, these points indicate that multilingual or cross‑lingual legal NLP must address the lack of prior transfer research and the need for broader, multilingual evaluation data, whereas English‑only tasks can rely on existing resources and benchmarks that do not require handling language variation across legal systems.

**Sources**  
- MultiEURLEX -A multi-lingual and multi-label legal document classification dataset for zero-shot cross-lingual transfer, 1 Introduction, p.1  
- LEGALBENCH: A COLLABORATIVELY BUILT BENCHMARK FOR MEASURING LEGAL REASONING IN LARGE LANGUAGE MODELS, 4.1 Construction process, p.9


---

## Q2. What methods are used to extract structured information from contracts?

### plain

The papers describe two complementary ways of turning the free‑text of a contract into structured data:

* **Human‑driven clause annotation** –  In CUAD the contracts were read by law‑student annotators who were trained (70‑100 h) and given more than 100 pages of detailed labeling rules.  For each of the 41 label categories the annotators identified every clause that corresponded to that label and recorded the start‑ and end‑token positions of the span.  This “extraction” of the relevant clause text creates a structured representation (label → clause span) that can later be used for training or evaluation of models【CUAD: An Expert‑Annotated NLP Dataset for Legal Contract Review, 3 CUAD: A Contract Review Dataset, pp. 3‑4】.  

* **Model‑driven clause extraction** –  The same dataset is then used to train large‑language‑model (Transformer) classifiers that automatically predict the span of text for each label, i.e., they learn to “highlight” the portions of a contract that a lawyer should attend to.  In the “Better Call GPT” study the authors also define a contract‑review playbook (a checklist of legal standards) and give the LLM a system prompt that instructs it to locate, for every checklist item, the exact contract sentences that satisfy or violate the standard.  The model’s output is a JSON object that maps each checklist number to the corresponding contract lines, an explanation, and a “Met/Not met” flag, thereby turning the unstructured contract into a structured set of findings【Better Call GPT, Comparing Large Language Models Against Lawyers, Table 6, pp. 14‑14】.  

Together, these methods—manual clause labeling to create a gold‑standard structured dataset, and automated span‑prediction or checklist‑mapping by LLMs—constitute the approaches described for extracting structured information from contracts.  

**Sources**

* CUAD: An Expert‑Annotated NLP Dataset for Legal Contract Review, *3 CUAD: A Contract Review Dataset*, pp. 3‑4.  
* Better Call GPT, Comparing Large Language Models Against Lawyers, *Table 6*, pp. 14‑14.

### local

The papers describe two complementary approaches for turning the free‑form text of a contract into a structured, machine‑readable representation.

* **Span‑annotation and token‑level extraction** – In CUAD, expert annotators (law students and lawyers) marked every clause that corresponded to each of 41 predefined categories.  The task for a model is then to receive a contract together with a category description and to **output the start‑ and end‑token positions of the relevant span(s)**, i.e., to extract the exact text that fulfills the label.  This turn‑the‑text‑into‑structured‑spans approach is the core method used for building the CUAD benchmark.  (CUAD: An Expert‑Annotated NLP Dataset for Legal Contract Review, *CUAD Contract Page Lengths*, p. 4‑5)  

* **Prompt‑driven LLM extraction** – In the “Better Call GPT” study, contracts are supplied to a large language model together with a checklist of legal standards.  The model is prompted (as shown in Table 6) to **identify, for each checklist item, the specific contract sentences or paragraphs that satisfy or violate the standard**, and to return a JSON object containing the clause text, an explanation, and a “met/not‑met” flag.  This method extracts structured information (check‑list results, clause locations, explanations) from the contract by means of a carefully engineered system prompt.  (Better Call GPT, *Table 6*, p. 14)  

Thus, the extraction methods described are (1) token‑level span annotation driven by expert‑labeled data, and (2) instruction‑tuned large‑language‑model prompting that returns clause‑level information in a predefined JSON schema.  

**Sources**

- *CUAD: An Expert‑Annotated NLP Dataset for Legal Contract Review*, **CUAD Contract Page Lengths**, p. 4‑5 – “The model’s task is, given a contract and a category (presented as a short question/description), to output the start and end token positions of each relevant span.”  
- *Better Call GPT, Comparing Large Language Models Against Lawyers*, **Table 6**, p. 14 – Prompt example that asks the model to “identify ALL of the checks listed in the provided checklist… include… an array of sentences or clauses in the contract that corresponds to the check… ‘check_Met’: … ‘Not met’.”

### global

The provided passages do not contain any description of specific methods used to extract structured information from contracts. They mention the CUAD dataset for contract‑review annotation and that models are evaluated on contract‑related tasks, but no concrete extraction techniques (e.g., rule‑based parsing, named‑entity recognition, table extraction, or other approaches) are detailed in the cited material.  

**Sources**  
- The CUAD passages discuss the dataset and its purpose but do not specify extraction methods (e.g., “We address this bottleneck within the legal domain by introducing the Contract Understanding Atticus Dataset (CUAD)…”, CUAD: An Expert‑Annotated NLP Dataset for Legal Contract Review, Abstract, p.1).  
- No other cited papers in the context provide details on contract‑information extraction techniques.

### hybrid

The papers extract structured contract information by first **annotating contracts with expert‑defined clause categories** and then training models to **identify the start‑ and end‑token spans of those clauses**.  In CUAD, law‑student annotators (trained for 70‑100 hours) labeled each contract with 41 label categories and produced span annotations that mark the exact text for each clause; models are then asked to output the start and end tokens of the relevant span so that the clause can be highlighted and later processed as structured data【CUAD: An Expert‑Annotated NLP Dataset for Legal Contract Review, 3 CUAD: A Contract Review Dataset, p.3】.  The same dataset also notes that “Labeled clauses make up about 10 % of each contract on average,” emphasizing that the extraction task is essentially a **span‑labeling (highlighting) problem**【CUAD: An Expert‑Annotated NLP Dataset for Legal Contract Review, 3 CUAD: A Contract Review Dataset, p.3】.

In the “Better Call GPT” study, the contracts are reviewed against a **standardised checklist** derived from a contract‑review playbook.  The system prompt instructs the model to **output a JSON object** for each checklist item, containing the clause text (or an empty field if absent), an explanation, and a “check‑Met” flag.  This JSON format provides a **structured representation** of the extracted information that can be directly consumed by downstream applications【Better Call GPT, Comparing Large Language Models Against Lawyers, Table 6, p.14】.

Together, these works show that structured information is extracted from contracts by:

1. **Expert annotation of clause categories** and span‑level labeling of the contract text.  
2. **Training supervised models** (e.g., BERT, DeBERTa) to predict those spans.  
3. **Mapping the extracted spans to a predefined schema** (e.g., checklist items) and outputting them in a machine‑readable format such as JSON.

**Sources**

- CUAD: An Expert‑Annotated NLP Dataset for Legal Contract Review, 3 CUAD: A Contract Review Dataset, p.3  
- Better Call GPT, Comparing Large Language Models Against Lawyers, Table 6, p.14

### evidence

The primary way structured information is pulled from contracts in the cited work is through **human‑driven annotation**:

* **Senior lawyers read each contract, decide whether it meets predefined standards, and explicitly mark the exact clause(s) that support their judgment**. Their annotations are then aggregated (using majority consensus) to create ground‑truth labels that both indicate compliance and pinpoint the relevant contractual text【Better Call GPT, Comparing Large Language Models Against Lawyers, 3.3 Data Collection and Analysis, p.4】.  

* **The dataset’s overall task is to have annotators highlight the “salient portions” of a contract that a human reviewer should examine**, which provides a structured map of important clauses for downstream models【CUAD: An Expert‑Annotated NLP Dataset for Legal Contract Review, Abstract, p.1】.  

* **Annotation processes are deliberately modeled on a lawyer’s legal‑research workflow**, ensuring that the extracted sections reflect the way legal professionals locate and retrieve relevant information【A Reasoning‑Focused Legal Retrieval Benchmark, 1 Introduction, p.1】.  

Together, these methods rely on expert legal professionals to manually identify and label key contract segments, producing structured data that can be used to train and evaluate automated contract‑review systems.  

**Sources**

* Better Call GPT, Comparing Large Language Models Against Lawyers, 3.3 Data Collection and Analysis, p.4 – “Senior Lawyers were instructed to evaluate each contract … locate the specific sections of the contract that influence their judgments… aggregated to formulate benchmarks… majority consensus to determine … the precise location of the relevant contractual reference.”
* CUAD: An Expert‑Annotated NLP Dataset for Legal Contract Review, Abstract, p.1 – “The task is to highlight salient portions of a contract that are important for a human to review.”
* A Reasoning‑Focused Legal Retrieval Benchmark, 1 Introduction, p.1 – “annotation processes modeled off of a lawyer's legal research process.”


---

## Q3. What risks and responsibilities come with building large legal datasets?

### plain

**Answer**

Building large legal datasets carries several important risks and corresponding responsibilities:

| Risk | What the literature says |
|------|---------------------------|
| **Potential for harm from biased, obscene, copyrighted, or private material** – Pre‑training on such content can cause large language models to reproduce bias, offensive language, or violate intellectual‑property and privacy rights. | “One concern with the rise of large language models lies with their potential for significant harm, particularly from pretraining on biased, obscene, copyrighted, and private information.” (Pile of Law, *Abstract*, p.1) |
| **Leakage of sensitive personal information** – Legal cases often contain identifiers, financial data, or medical records; if a model is trained on them it may unintentionally reveal this information when generating text. | “When using this data for model training, there is a risk that the model may unintentionally expose people' sensitive information during content generation, potentially leading to data leakage.” (Legal Evalutions and Challenges of Large Language Models, *A. Data privacy*, p.7) |
| **Inclusion of material that escaped administrative scrutiny** – Even though the source documents are public, they may still contain sensitive details that were not filtered out by existing legal standards. | “While the underlying data in Pile of Law is already public record and has implicit filters, we recognize that it may contain sensitive material that has escaped administrative scrutiny.” (Pile of Law, *2 Pile of Law*, p.2‑3) |

**Responsibilities**

| Responsibility | What the literature says |
|----------------|---------------------------|
| **Apply legally grounded filtering** – Use the norms and implicit filters already embedded in legal sources (privacy, toxicity, copyright) as a baseline, and explicitly design additional filters to meet those standards. | “Each of these data sources carries with it an implicit filtering mechanism formed under relevant legal standards of privacy and toxicity… We discuss the ethics of our work and our proposed mechanisms for content removal.” (Pile of Law, *2 Pile of Law*, p.2‑3) |
| **Anonymize personal data** – Remove or mask identifying information from case documents before inclusion in the dataset. | “To ensure the objectivity and fairness of the research, we strictly anonymized all personal privacy information in the cases.” (Legal Evalutions and Challenges of Large Language Models, *A. Scope of the Study and Used Datasets*, p.5‑6) |
| **Implement rigorous review of model outputs** – Continuously monitor generated text for accidental disclosure of private information and have processes to correct or remove such content. | “The design and training processes of the model must prioritize the protection of data… implement a rigorous data processing and review mechanism for the model's outputs.” (Legal Evalutions and Challenges of Large Language Models, *A. Data privacy*, p.7) |
| **Document and share ethical considerations** – Provide transparent discussion of the dataset’s composition, licensing, and the steps taken to mitigate risks, enabling the community to assess and improve upon the work. | “We distill the legal norms that governments have developed to constrain the inclusion of toxic or private content into actionable lessons for researchers… discuss how our dataset reflects these norms.” (Pile of Law, *Abstract*, p.1) |

In sum, constructing large‑scale legal corpora demands careful attention to legal‑based filtering, privacy protection (including anonymization and output review), and transparent ethical documentation to mitigate the risks of bias, offensiveness, copyright infringement, and data leakage.  

---

**Sources**

- *Pile of Law: Learning Responsible Data Filtering from the Law and a 256GB Open-Source Legal Dataset*, **Abstract**, p.1.  
- *Pile of Law: Learning Responsible Data Filtering from the Law and a 256GB Open-Source Legal Dataset*, **2 Pile of Law**, p.2‑3.  
- *Legal Evalutions and Challenges of Large Language Models*, **A. Data privacy**, p.7.  
- *Legal Evalutions and Challenges of Large Language Models*, **A. Scope of the Study and Used Datasets**, p.5‑6.

### local

Building large legal datasets carries several important risks and corresponding responsibilities:

* **Risk of exposing sensitive personal information** – Legal documents often contain private details such as identities, financial status, or medical records. When these texts are used to train language models, the models can unintentionally reproduce or leak that information in generated output. (Legal Evalutions and Challenges of Large Language Models, A. Data privacy, p.7)  

* **Responsibility to protect data‑privacy** – Researchers must design training pipelines and output‑review mechanisms that prioritize the protection of confidential data, ensuring that generated text does not disclose personal information. (Legal Evalutions and Challenges of Large Language Models, A. Data privacy, p.7)  

* **Risk of including content that has escaped existing legal filters** – Even though the source material is public record and often under permissive licenses, it may still contain material that is sensitive, toxic, or otherwise subject to privacy or regulatory constraints. (Pile of Law: Learning Responsible Data Filtering from the Law and a 256GB Open‑Source Legal Dataset, 2 Pile of Law, p.2‑3)  

* **Responsibility to implement ethical review and content‑removal mechanisms** – The creators of the dataset discuss ethics and propose mechanisms for removing problematic content, acknowledging that implicit legal filters are not sufficient on their own. (Pile of Law: Learning Responsible Data Filtering from the Law and a 256GB Open‑Source Legal Dataset, 2 Pile of Law, p.2‑3)  

* **Responsibility to respect licensing and legal standards** – All material in the dataset must be publicly available and mostly under permissive licenses, and curators must ensure that the aggregation does not violate any restrictive licenses or legal norms. (Pile of Law: Learning Responsible Data Filtering from the Law and a 256GB Open‑Source Legal Dataset, 2 Pile of Law, p.2‑3)  

* **Risk of inadequate ad‑hoc filtering** – Conventional filtering approaches often ignore contextual nuances that legal norms address, leading to insufficient protection against bias, obscenity, copyright infringement, or privacy violations. (Pile of Law: Learning Responsible Data Filtering from the Law and a 256GB Open‑Source Legal Dataset, Abstract, p.1)  

* **Responsibility to develop context‑aware, law‑grounded filtering** – The authors propose grounding filtering in legal standards that balance privacy, toxicity, transparency, and completeness, and they encourage researchers to learn these implicit sanitization rules directly from the data. (Pile of Law: Learning Responsible Data Filtering from the Law and a 256GB Open‑Source Legal Dataset, Abstract, p.1)

**In summary**, building large legal corpora requires careful handling of privacy‑sensitive content, implementation of robust ethical and legal review processes, adherence to licensing constraints, and the development of context‑aware filtering methods that go beyond simple ad‑hoc approaches.

**Sources**

* Pile of Law: Learning Responsible Data Filtering from the Law and a 256GB Open‑Source Legal Dataset, 2 Pile of Law, p.2‑3.  
* Pile of Law: Learning Responsible Data Filtering from the Law and a 256GB Open‑Source Legal Dataset, Abstract, p.1.  
* Legal Evalutions and Challenges of Large Language Models, A. Data privacy, p.7.

### global

Building large legal datasets carries several important risks and responsibilities that the literature repeatedly highlights.

* **Bias and unfairness** – Because legal datasets are assembled from many heterogeneous sources, they can encode existing societal biases.  If a model trained on such data is used for case analysis, it may produce biased or discriminatory outputs, which is especially problematic in a domain that demands impartiality【Legal Evalutions and Challenges of Large Language Models, C. Ethical and moral issues, p.8】.  

* **Lack of transparency and interpretability** – Large‑scale legal corpora often lack clear documentation of provenance and annotation procedures.  This opacity makes it difficult for practitioners to understand why a model reaches a particular conclusion, undermining trust in legal decision‑support tools【Legal Evalutions and Challenges of Large Language Models, D. Technical limitations, p.8】.  

* **Legal liability** – When a model trained on a publicly released legal dataset provides advice or analysis that leads to adverse outcomes, it is unclear who is legally responsible.  Developers typically include disclaimer language, but unintended consequences can still arise, leaving the question of liability unresolved【Legal Evalutions and Challenges of Large Language Models, B. The definition of legal liability, p.7】.  

* **Data privacy and compliance** – Aggregating large amounts of legal texts (e.g., court opinions, contracts) may involve personal or sensitive information.  Different jurisdictions have varying data‑privacy regulations, so dataset creators must ensure that the collection and release of data comply with all relevant legal requirements【Legal Evalutions and Challenges of Large Language Models, E. Legislative differences, p.8】.  

* **Responsibility to support downstream use** – Providing not only the raw data but also model predictions, evaluation code, and additional annotations helps the community apply the dataset responsibly and reduces the risk of misuse【LawBench: Benchmarking Legal Knowledge of Large Language Models, Abstract, p.1】.  

* **Need for careful benchmark design** – Benchmarks that do not reflect the types of queries lawyers actually ask can lead to over‑optimistic performance estimates and misguide practitioners.  Designing datasets with hand‑annotated, realistic legal queries is therefore a responsibility of dataset builders【A Reasoning-Focused Legal Retrieval Benchmark, 1 Introduction, p.1】.  

Together, these points illustrate that constructing large legal datasets is not just a technical exercise; it requires attention to bias mitigation, transparency, legal compliance, clear liability framing, and the provision of comprehensive resources to enable responsible downstream use.  

**Sources**

* Legal Evalutions and Challenges of Large Language Models, C. Ethical and moral issues, p.8 – “Due to the diverse sources of data, these models can introduce biases… ensuring that models remain neutral…”
* Legal Evalutions and Challenges of Large Language Models, D. Technical limitations, p.8 – “Additionally, their lack of interpretability creates uncertainty for legal practitioners…”
* Legal Evalutions and Challenges of Large Language Models, B. The definition of legal liability, p.7 – “The delineation of legal liability when utilizing LLMs for legal advice… remains unclear… unintended consequences can still arise.”
* Legal Evalutions and Challenges of Large Language Models, E. Legislative differences, p.8 – “As LLMs are adopted globally, differences in regulatory policies… can create compliance risks…”
* LawBench: Benchmarking Legal Knowledge of Large Language Models, Abstract, p.1 – “All data, model predictions and evaluation code are released…”
* A Reasoning-Focused Legal Retrieval Benchmark, 1 Introduction, p.1 – “benchmarks rely on query‑document distributions… where queries do not correspond to the types of questions lawyers might actually ask.”

### hybrid

Building large legal corpora carries several concrete risks and attendant responsibilities for researchers:

* **Privacy and toxic‑content exposure.** Legal and administrative records often contain personally‑identifying information, medical or financial details, and potentially offensive language. When such material is harvested at scale it can be unintentionally reproduced by a model, leading to data‑leakage or the generation of harmful content (Legal Evalutions and Challenges of Large Language Models, A. Data privacy, p.7).  

* **Inconsistent or uneven content filtering.** Because the undesirability of a passage is highly contextual (e.g., a racial epithet may be benign or toxic depending on speaker, audience, or jurisdiction), automated filters can miss sensitive items or remove too much, thereby biasing the dataset or harming downstream performance (Pile of Law, 1 Introduction, p.1).  

* **Legal‑norm‑guided sanitisation.** Researchers are expected to respect the legal standards that already govern the source material (privacy statutes, toxicity regulations, licensing terms). The Pile of Law authors therefore catalogue the implicit filtering mechanisms embedded in each source and encourage the community to align its own sanitisation processes with those norms (Pile of Law, 2 Pile of Law, p.2).  

* **License and provenance compliance.** Although the Pile of Law consists of publicly available, mostly permissively‑licensed texts, careful verification of each source’s licensing is required to avoid infringing copyright or violating data‑use agreements (Pile of Law, 2 Pile of Law, p.2).  

* **Test‑data contamination.** When datasets are assembled from publicly crawled material, there is a risk that large pre‑trained models have already seen the exact test instances, inflating benchmark scores and obscuring true performance (LawBench, Limitations, p.16).  

* **Responsibility to the justice ecosystem.** Large‑scale legal pre‑training is promoted as a way to improve access‑to‑justice tools, but the community must ensure that the resulting models do not propagate biases, privacy breaches, or misinformation, and that any downstream applications are deployed with appropriate safeguards (Pile of Law, Abstract, p.1).  

Overall, building massive legal datasets obliges researchers to (1) conduct thorough privacy and toxicity audits, (2) implement transparent, norm‑aligned filtering pipelines, (3) respect licensing and provenance, (4) guard against data leakage in evaluation, and (5) consider the broader societal impact of the models that will be trained on these resources.

**Sources**

- Legal Evalutions and Challenges of Large Language Models, A. Data privacy, p.7  
- Pile of Law: Learning Responsible Data Filtering from the Law and a 256 GB Open‑Source Legal Dataset, 1 Introduction, p.1  
- Pile of Law: Learning Responsible Data Filtering from the Law and a 256 GB Open‑Source Legal Dataset, 2 Pile of Law, p.2  
- Pile of Law: Learning Responsible Data Filtering from the Law and a 256 GB Open‑Source Legal Dataset, Abstract, p.1  
- LawBench: Benchmarking Legal Knowledge of Large Language Models, Limitations, p.16

### evidence

Building large legal datasets carries significant privacy risks and corresponding responsibilities for researchers and developers.

* **Risk of data leakage** – Legal case collections often contain personally identifying details, financial information, and medical records. When such data are used to train large language models, the models can unintentionally reproduce this sensitive information in their outputs, creating a risk of exposing individuals’ private data【Legal Evalutions and Challenges of Large Language Models, A. Data privacy, p.7】.  

* **Responsibility to protect privacy** – To mitigate this risk, the design and training pipelines must prioritize data‑privacy safeguards. This includes implementing strict data‑processing and output‑review mechanisms that ensure generated text does not disclose personal information【Legal Evalutions and Challenges of Large Language Models, A. Data privacy, p.7】.  

* **Responsibility to collaborate and share responsibly** – Because much legal data is confidential, creating high‑quality legal LLMs requires coordinated effort among multiple institutions. Such collaboration helps pool resources, establish shared standards for data handling, and ensure that privacy and security practices are consistently applied【LawBench: Benchmarking Legal Knowledge of Large Language Models, 5 Conclusion, p.15】.  

* **Open‑source dataset provision** – The Pile of Law demonstrates an effort to make a large, open‑source legal corpus publicly available while acknowledging the need for responsible use. By openly releasing a ∼256 GB collection of English‑language legal and administrative texts, the authors aim to support research while encouraging the community to adopt the necessary privacy safeguards【Pile of Law: Learning Responsible Data Filtering from the Law and a 256GB Open-Source Legal Dataset, 1 Introduction, p.1】.

**In summary**, building large legal datasets entails the risk of unintentionally leaking sensitive personal information, and it obliges developers to embed robust privacy‑preserving measures, conduct thorough output reviews, and engage in multi‑institutional collaboration to manage confidentiality responsibly.  

**Sources**  
- Legal Evalutions and Challenges of Large Language Models, A. Data privacy, p.7  
- LawBench: Benchmarking Legal Knowledge of Large Language Models, 5 Conclusion, p.15  
- Pile of Law: Learning Responsible Data Filtering from the Law and a 256GB Open-Source Legal Dataset, 1 Introduction, p.1


---

## Q4. How did legal NLP methods change with the arrival of large language models?

### plain

**Answer**

The emergence of large language models (LLMs) has transformed legal‑NLP from a set of narrow, task‑specific tools into a broader, more flexible ecosystem that can handle many legal tasks with a single, adaptable model.  

* **From specialized toolkits to general‑purpose models** – Earlier legal‑NLP work relied on rule‑based pipelines or modest‑size neural models that were built for a single function (e.g., tokenisation, entity extraction, or classification).  The recent wave of LLMs provides a “one‑model‑many‑tasks” capability, allowing the same architecture to perform legal text cleaning, tokenisation, feature extraction, entity recognition, classification, summarisation, drafting, reasoning and question answering (see the description of LexNLP’s modular toolkit versus the newer LLM‑based systems)【Legal Evalutions and Challenges of Large Language Models, C. Overview of legal‑specific LLMs, p.5】.  

* **Fine‑tuning on large legal corpora** – Legal‑specific LLMs such as LawGPT, ChatLaw, LAWGPT‑zh, Lawyer‑LLama, LexiLaw, etc., are created by taking a large pre‑trained model (e.g., ChatGLM‑6B, GPT‑J) and further pre‑training or fine‑tuning it on massive collections of statutes, case law, contracts and Q‑A datasets.  This yields “superior capabilities in understanding legal concepts, conducting legal reasoning, and generating legal text” compared with earlier, smaller models that lacked such domain depth【Legal Evalutions and Challenges of Large Language Models, C. Overview of legal‑specific LLMs, p.5】.  

* **New functional possibilities** – LLMs now support higher‑level legal activities that were previously out of reach for traditional NLP pipelines:  
  * **Legal reasoning and judgment prediction** – systematic testing on English and Chinese cases shows LLMs can reason through legal issues and predict outcomes, albeit with limitations【Legal Evalutions and Challenges of Large Language Models, I. INTRODUCTION, p.1‑2】.  
  * **Zero‑shot and few‑shot performance** – studies report that GPT‑3.5 Turbo and GPT‑4 can be prompted to perform classification, summarisation, and terminology explanation without task‑specific training, though accuracy remains modest (e.g., micro‑F1 ≈ 49 % on LexGLUE)【Legal Evalutions and Challenges of Large Language Models, II. REVIEW OF LLMS IN THE LEGAL FIELD, p.2‑3】.  
  * **Hybrid retrieval‑augmented systems** – models such as ChatLaw combine vector‑database retrieval, knowledge graphs and multi‑agent architectures to reduce hallucinations and improve reliability when answering legal queries【Legal Evalutions and Challenges of Large Language Models, C. Overview of legal‑specific LLMs, p.5】.  

* **Performance trade‑offs** – While LLMs dramatically increase speed (seconds versus hours for contract review) and lower cost (up to 99.97 % reduction), they also inherit biases from their training data and can produce inaccurate or “hallucinated” legal statements, which raises ethical and technical concerns that were less prominent with earlier, more deterministic toolkits【Legal Evalutions and Challenges of Large Language Models, I. INTRODUCTION, p.1‑2】.  

Overall, the arrival of LLMs has shifted legal NLP from isolated, narrowly‑focused components toward large, adaptable models that can be fine‑tuned for legal domains, enabling richer reasoning, faster processing, and broader application—while also introducing new challenges around accuracy, bias, and accountability.  

**Sources**

1. *Legal Evalutions and Challenges of Large Language Models*, **C. Overview of legal‑specific LLMs**, p.5.  
2. *Legal Evalutions and Challenges of Large Language Models*, **I. INTRODUCTION**, p.1‑2.  
3. *Legal Evalutions and Challenges of Large Language Models*, **II. REVIEW OF LLMS IN THE LEGAL FIELD**, p.2‑3.

### local

The emergence of large‑language models (LLMs) has reshaped legal natural‑language‑processing in several ways.  

* **From narrow toolkits to end‑to‑end generative systems.**  Earlier legal‑NLP work relied on modular pipelines such as LexNLP, which provided “text cleaning, tokenization, feature extraction, entity recognition, and text classification” for tasks like contract analysis and regulatory compliance [Legal Evalutions and Challenges of Large Language Models, C. Overview of legal‑specific LLMs, p.5].  With LLMs, the same functions can be performed by a single model that is able to understand legal terminology, reason over statutes, and generate coherent legal text without hand‑crafted feature engineering.  

* **Broader functional scope.**  LLMs now support a wide range of legal activities that previously required separate systems:  
  * **Summarization** of contracts, litigation filings and judicial opinions [Legal Evalutions and Challenges of Large Language Models, II. REVIEW OF LLMS IN THE LEGAL FIELD, p.2‑3];  
  * **Drafting** of contract clauses and initial document drafts, including automatic language improvements [Legal Evalutions and Challenges of Large Language Models, II. REVIEW OF LLMS IN THE LEGAL FIELD, p.2‑3];  
  * **Legal research** that synthesizes case law and answers complex legal queries in plain language [Legal Evalutions and Challenges of Large Language Models, II. REVIEW OF LLMS IN THE LEGAL FIELD, p.2‑3];  
  * **Domain‑specific reasoning** through specialized legal LLMs (e.g., LawGPT, ChatLaw2‑MOE, LAWGPT‑zh) that are fine‑tuned on large corpora of Chinese or English case law, improving accuracy on legal reasoning benchmarks [Legal Evalutions and Challenges of Large Language Models, C. Overview of legal‑specific LLMs, p.5].  

* **Improved performance but new reliability concerns.**  While LLMs achieve higher scores on legal benchmarks and can surpass general‑purpose models such as GPT‑4 on certain tasks, systematic testing still shows “misinterpretation of legal language, resulting in inaccurate legal reasoning” and “non‑negligible factual and legal inaccuracies” [Legal Evalutions and Challenges of Large Language Models, II. REVIEW OF LLMS IN THE LEGAL FIELD, p.2‑3]; therefore, the field now also focuses on mitigation strategies like retrieval‑augmented generation to reduce hallucinations.  

* **Shift toward evaluation on multilingual, multi‑jurisdictional datasets.**  New benchmark suites evaluate LLMs on both Chinese and U.S. case sets, measuring ROUGE/BLEU similarity and human alignment, reflecting a move from single‑language, single‑task assessments to comprehensive, cross‑jurisdictional testing [Legal Evalutions and Challenges of Large Language Models, I. INTRODUCTION, p.1‑2].

**In summary**, large language models have turned legal NLP from a collection of specialized, rule‑based components into a set of versatile, generative systems that can handle summarization, drafting, research, and reasoning across multiple legal systems, while also introducing new challenges around accuracy and hallucination that the community is actively addressing.  

---  
**Sources**  

* Legal Evalutions and Challenges of Large Language Models, **C. Overview of legal‑specific LLMs**, p.5 – “LexNLP… offers a comprehensive suite of text analysis capabilities… Its modular design and flexible API allow users to customize functionalities…”.  
* Legal Evalutions and Challenges of Large Language Models, **II. REVIEW OF LLMS IN THE LEGAL FIELD**, p.2‑3 – Describes LLM applications in summarization, drafting, legal research, and notes systematic misinterpretation and factual inaccuracies.  
* Legal Evalutions and Challenges of Large Language Models, **C. Overview of legal‑specific LLMs**, p.5 – Mentions domain‑specific models (LawGPT, ChatLaw2‑MOE, etc.) that outperform general‑purpose models on legal benchmarks.  
* Legal Evalutions and Challenges of Large Language Models, **I. INTRODUCTION**, p.1‑2 – Highlights the new multilingual benchmark (13 Chinese and 13 U.S. cases) used to evaluate LLMs in legal tasks.

### global

Legal NLP methods have shifted markedly since large language models (LLMs) became available.  Early work focused on task‑specific neural architectures and hand‑crafted features, but the arrival of LLMs introduced several new trends:

* **Benchmark proliferation and richer evaluation** – New comprehensive benchmarks such as LEGALBENCH, LawBench, and CUAD have been created to measure LLM reasoning, multi‑step legal tasks, and contract‑review performance, expanding beyond earlier, narrower datasets [LEGALBENCH: A COLLABORATIVELY BUILT BENCHMARK FOR MEASURING LEGAL REASONING IN LARGE LANGUAGE MODELS, 1 Introduction, p.4]; [LawBench: Benchmarking Legal Knowledge of Large Language Models, Abstract, p.1].

* **Few‑shot and zero‑shot capabilities** – Researchers note that LLMs can perform many legal tasks with only a few examples, a capability not present in earlier models [LEGALBENCH: A COLLABORATIVELY BUILT BENCHMARK…, 1 Introduction, p.4]; “These benchmarks do not measure the aspects of LLMs which generate excitement for law‑namely, their ability to perform many different tasks using only few‑shot prompts.” [LEGALBENCH: A COLLABORATIVELY BUILT BENCHMARK…, 1 Introduction, p.4].

* **Improved performance on complex reasoning** – Closed‑source LLMs such as GPT‑4 show higher scores on issue‑spotting, rule‑conclusion, and interpretation tasks compared with earlier open‑source models, indicating that LLMs can handle multi‑step legal reasoning better than prior neural baselines [LEGALBENCH: A COLLABORATIVELY BUILT BENCHMARK…, Table 6, p.14]; “On the interpretation tasks, we find that on average GPT‑4 outperforms GPT‑3.5 (p < 0.01)” [LEGALBENCH: A COLLABORATIVELY BUILT BENCHMARK…, 5.3.5 Interpretation, p.17].

* **Adaptation and fine‑tuning strategies** – Even with LLMs, lightweight adaptation methods (e.g., adapters, BITFIT, LNFIT) that fine‑tune only a tiny fraction of parameters (< 0.05 %) remain competitive, showing that full model retraining is often unnecessary [MultiEURLEX…, BITFIT (Zaken et al., 2021) keeps the whole network frozen…, p.5]; “Interestingly, even adaptation strategies (BITFIT, LNFIT) that fine‑tune a very small fraction of parameters (<0.05 %) are competitive.” [MultiEURLEX…, 7 Conclusions and Future Work, p.9].

* **Cross‑lingual and multilingual transfer** – LLM‑based approaches have begun to explore zero‑shot cross‑lingual transfer for legal document classification, a direction previously unexplored in legal NLP [MultiEURLEX…, cross‑lingual transfer has not yet been explored in legal NLP, p.1]; adapter‑based multilingual fine‑tuning improves performance across 23 languages [MultiEURLEX…, 6.3 Multilingual Fine‑tuning…, p.9].

* **Recognition of limitations** – Despite gains, LLMs still struggle with accurate legal interpretation, exhibit bias, and lack transparency, prompting calls for better training methods, interpretability, and ethical safeguards [Legal Evalutions and Challenges of Large Language Models, VI. DISCUSSION, p.8]; “their limitations in accurately interpreting complex legal language and reasoning remain clear” [Legal Evalutions and Challenges of Large Language Models, VI. DISCUSSION, p.8].

Overall, the arrival of LLMs has expanded the scope of legal NLP from narrowly tuned models to versatile, few‑shot capable systems evaluated on large, multi‑task benchmarks, while also highlighting new challenges in interpretability, bias, and cross‑lingual robustness.  

**Sources**

- LEGALBENCH: A COLLABORATIVELY BUILT BENCHMARK FOR MEASURING LEGAL REASONING IN LARGE LANGUAGE MODELS, 1 Introduction, p.4  
- LEGALBENCH: A COLLABORATIVELY BUILT BENCHMARK FOR MEASURING LEGAL REASONING IN LARGE LANGUAGE MODELS, Table 6, p.14  
- LEGALBENCH: A COLLABORATIVELY BUILT BENCHMARK FOR MEASURING LEGAL REASONING IN LARGE LANGUAGE MODELS, 5.3.5 Interpretation, p.17  
- LEGALBENCH: A COLLABORATIVELY BUILT BENCHMARK FOR MEASURING LEGAL REASONING IN LARGE LANGUAGE MODELS, 5.2 Performance trends, p.13  
- LawBench: Benchmarking Legal Knowledge of Large Language Models, Abstract, p.1  
- MultiEURLEX -A multi-lingual and multi-label legal document classification dataset for zero-shot cross-lingual transfer, 1 Introduction, p.1  
- MultiEURLEX -A multi-lingual and multi-label legal document classification dataset for zero-shot cross-lingual transfer, BITFIT (Zaken et al., 2021) keeps the whole network frozen during fine‑tuning, except for bias terms., p.5  
- MultiEURLEX -A multi-lingual and multi-label legal document classification dataset for zero-shot cross-lingual transfer, 6.3 Multilingual Fine‑tuning (many‑to‑many), p.9  
- MultiEURLEX -A multi-lingual and multi-label legal document classification dataset for zero-shot cross-lingual transfer, 7 Conclusions and Future Work, p.9  
- Legal Evalutions and Challenges of Large Language Models, VI. DISCUSSION, p.8

### hybrid

Legal NLP has been transformed by the emergence of large language models (LLMs).  Early work focused on modest‑size, task‑specific models trained on relatively small, manually annotated corpora.  With LLMs the field has moved toward:

* **Scale‑driven performance gains** – larger models consistently improve one‑shot results, and scaling the amount of training data yields gains comparable to changing model families.  (“Scaling up the model size results in better performance in one‑shot case…”) (LawBench: Benchmarking Legal Knowledge of Large Language Models, 4 Experiment > 4.4 Analysis, p.13).

* **Zero‑shot and few‑shot evaluation** – many legal benchmarks now test models without any task‑specific fine‑tuning, exposing the strong out‑of‑the‑box reasoning abilities of LLMs.  (“many legal benchmarks lack few‑shot evaluation, making them valuable testbeds for few‑shot research”) (Legal NLP Benchmarks and Model Adaptation, Summary).

* **Lightweight adaptation strategies** – methods that fine‑tune only a tiny fraction of parameters (e.g., BITFIT, LNFIT) achieve competitive zero‑shot cross‑lingual transfer, preserving multilingual knowledge while requiring far less compute.  (“BITFIT (Zaken et al., 2021) keeps the whole network frozen during fine‑tuning, except for bias terms.”) (MultiEURLEX – A multi‑lingual and multi‑label legal document classification dataset for zero‑shot cross‑lingual transfer, 4 Methods > 4.2 Cross‑lingual Adaptation Strategies, p.5);  (“Interestingly, even adaptation strategies (BITFIT, LNFIT) that fine‑tune a very small fraction of parameters (<0.05 %) are competitive.”) (MultiEURLEX – …, 7 Conclusions and Future Work, p.9).

* **Progressive and reinforcement‑learning fine‑tuning** – pipelines that first fine‑tune on general‑domain data and then on legal data, or that incorporate human feedback, further boost accuracy on complex reasoning tasks.  (“reinforcement learning from human feedback and progressive fine‑tuning pipelines further boost results”) (Legal NLP Benchmarks and Model Adaptation, Summary).

* **Multilingual joint fine‑tuning** – training on all languages simultaneously (many‑to‑many) outperforms one‑to‑many approaches, leveraging annotated data across jurisdictions.  (“many‑to‑many models largely outperform the one‑to‑many models”) (MultiEURLEX – …, 6.3 Multilingual Fine‑tuning (many‑to‑many), p.9).

* **Task‑specific legal LLMs** – dedicated legal models (e.g., LawGPT, ChatLaw, LAWGPT) are fine‑tuned on large legal corpora and achieve superior understanding of legal concepts and reasoning.  (“LawGPT… is fine‑tuned on … Chinese legal text… provides comprehensive and accurate responses to complex legal inquiries”) (Legal Evalutions and Challenges of Large Language Models, C. Overview of legal‑specific LLMs, p.5).

* **Shift from pure model size to data and adaptation** – studies show that increasing parameters alone yields modest gains, whereas adding domain‑specific data or using adaptation methods produces larger, more consistent improvements.  (“Even though ALBERT‑xxlarge‑v2 has more than 20 times more parameters than its smallest version, it only performs around 3 % percent better.”) (CUAD: An Expert‑Annotated NLP Dataset for Legal Contract Review, 4 Experiments > 4.2 Results, p.7).

Overall, the arrival of LLMs has moved legal NLP from narrowly‑focused, heavily‑engineered pipelines toward scalable, data‑rich, and adaptable approaches that exploit massive pretrained models, lightweight fine‑tuning, and multilingual joint training to achieve stronger, more generalizable legal reasoning.

**Sources**

- LawBench: Benchmarking Legal Knowledge of Large Language Models, 4 Experiment > 4.4 Analysis, p.13  
- Legal NLP Benchmarks and Model Adaptation, Summary (no page needed)  
- MultiEURLEX – A multi‑lingual and multi‑label legal document classification dataset for zero‑shot cross‑lingual transfer, 4 Methods > 4.2 Cross‑lingual Adaptation Strategies, p.5  
- MultiEURLEX – …, 7 Conclusions and Future Work, p.9  
- MultiEURLEX – …, 6.3 Multilingual Fine‑tuning (many‑to‑many), p.9  
- Legal Evalutions and Challenges of Large Language Models, C. Overview of legal‑specific LLMs, p.5  
- CUAD: An Expert‑Annotated NLP Dataset for Legal Contract Review, 4 Experiments > 4.2 Results, p.7

### evidence

The emergence of large language models (LLMs) has shifted legal natural‑language‑processing from traditional rule‑based or task‑specific pipelines toward the use of both general‑purpose and legally fine‑tuned LLMs.  Researchers now evaluate models that are explicitly adapted to legal corpora, noting that these specialized systems can better capture legal concepts, reasoning, and terminology (Legal Evalutions and Challenges of Large Language Models, Overview of legal‑specific LLMs, p.5).  At the same time, empirical benchmarking shows that the newer legal‑specific LLMs do not automatically outperform strong general‑purpose LLMs, especially when the latter are built on more powerful foundation models (LawBench: Benchmarking Legal Knowledge of Large Language Models, Experiment > 4.4 Analysis, p.13).  

Developing high‑quality legal LLMs also now requires coordinated effort across multiple institutions because legal data are often confidential and heterogeneous (LawBench: Benchmarking Legal Knowledge of Large Language Models, Conclusion, p.15).  Despite these advances, the field still faces significant technical hurdles: LLMs can misinterpret legal terminology, lose case context, and produce unreliable analyses, which limits their trustworthiness for practitioners (Legal Evalutions and Challenges of Large Language Models, Technical limitations, p.8).  

Overall, the arrival of LLMs has introduced a new paradigm that emphasizes large, pre‑trained models—both generic and domain‑adapted—while highlighting the need for collaborative development and continued work on interpretability and domain‑specific robustness.  

**Sources**  
- Legal Evalutions and Challenges of Large Language Models, Overview of legal‑specific LLMs, p.5  
- LawBench: Benchmarking Legal Knowledge of Large Language Models, Experiment > 4.4 Analysis, p.13  
- LawBench: Benchmarking Legal Knowledge of Large Language Models, Conclusion, p.15  
- Legal Evalutions and Challenges of Large Language Models, Technical limitations, p.8


---

## Q5. Does making a model bigger reliably improve legal task performance?

### plain

**Answer**

Increasing a model’s size tends to improve legal‑task performance, but the improvement is not guaranteed across all settings.  

* In the **LawBench** study, scaling up model size *usually* raises scores and lowers abstention rates in one‑shot scenarios, yet the effect is less consistent in zero‑shot settings and there are notable exceptions (e.g., the larger ChatLaw model performed worse)【LawBench: Benchmarking Legal Knowledge of Large Language Models, 4.4 Analysis, pp.13‑15】.  
* The **LEGALBENCH** analysis reports that “within LLM families, larger models usually outperform smaller models” (e.g., Flan‑T5‑XXL (11 B) beats Flan‑T5‑XL (3 B); LLaMA‑2‑13B beats LLaMA‑2‑7B)【LEGALBENCH: A Collaboratively Built Benchmark for Measuring Legal Reasoning in Large Language Models, 5.2 Performance trends, pp.13‑15】. However, the authors also note considerable variation across families and that size alone does not fully determine performance.

Thus, while bigger models often give better results, the relationship is not perfectly reliable; performance also depends on the task setting (one‑shot vs. zero‑shot), the specific architecture, training regime, and fine‑tuning strategy.

**Sources**

1. *LawBench: Benchmarking Legal Knowledge of Large Language Models*, Section 4.4 Analysis, pp. 13‑15.  
2. *LEGALBENCH: A Collaboratively Built Benchmark for Measuring Legal Reasoning in Large Language Models*, Section 5.2 Performance trends, pp. 13‑15.

### local

Increasing a model’s size can help legal‑task performance, but the benefit is not guaranteed across all settings.

* **LawBench (LawBench: Benchmarking Legal Knowledge of Large Language Models)** finds that larger models usually give higher scores in **one‑shot** evaluations and lower abstention rates, indicating better instruction following. However, the same paper reports mixed results in **zero‑shot** scenarios, where simply scaling up does not always lead to better performance and even an outlier (ChatLaw) shows lower scores despite being larger【LawBench: Benchmarking Legal Knowledge of Large Language Models, 4 Experiment > 4.4 Analysis, p.13‑15】.  

* **LEGALBENCH (LEGALBENCH: A COLLABORATIVELY BUILT BENCHMARK FOR MEASURING LEGAL REASONING IN LARGE LANGUAGE MODELS)** observes a general trend that “within a given model family, larger models usually outperform smaller models” across several reasoning categories【LEGALBENCH: A COLLABORATIVELY BUILT BENCHMARK FOR MEASURING LEGAL REASONING IN LARGE LANGUAGE MODELS, 5.2 Performance trends, p.13‑15】. Yet the same analysis notes substantial performance gaps even among models of comparable size, indicating that factors such as pre‑training data, instruction‑tuning, and architecture also strongly affect results【LEGALBENCH: A COLLABORATIVELY BUILT BENCHMARK FOR MEASURING LEGAL REASONING IN LARGE LANGUAGE MODELS, 5.2 Performance trends, p.13‑15】.

**Conclusion:**  
Making a model bigger tends to improve legal‑task performance, especially in one‑shot settings, but the improvement is not uniformly reliable—zero‑shot performance can be mixed, and other design choices (training data, fine‑tuning, architecture) can outweigh size effects.

**Sources**

* LawBench: Benchmarking Legal Knowledge of Large Language Models, 4 Experiment > 4.4 Analysis, p.13‑15.  
* LEGALBENCH: A COLLABORATIVELY BUILT BENCHMARK FOR MEASURING LEGAL REASONING IN LARGE LANGUAGE MODELS, 5.2 Performance trends, p.13‑15.

### global

The provided passages do not contain a clear, evidence‑based answer to whether increasing a model’s size (e.g., more parameters or larger architecture) reliably leads to better performance on legal tasks. The excerpts discuss specific performance numbers for particular models, note gaps between open‑source and closed‑source systems, and describe various challenges and evaluation results, but none of them directly address a systematic relationship between model size and legal‑task accuracy.

**Sources**

- The context includes performance tables for individual models (e.g., Gemma2‑9B, GPT‑4, GPT‑3.5) and qualitative observations about gaps between model families, but no statement linking model size to consistent performance improvements. No citation directly supports the claim.

### hybrid

Increasing the size of a language model tends to raise its legal‑task performance, but the effect is not uniform across all settings.

* Within a model family, larger variants usually beat smaller ones. For example, the LEGALBENCH analysis reports that “larger models usually outperform smaller models” and gives concrete cases such as Flan‑T5‑XXL (11 B) beating Flan‑T5‑XL (3 B) and LLaMA‑2‑13B beating LLaMA‑2‑7B (LegalBench, 5.2 Performance trends, p.13).  
* The same trend is observed in one‑shot evaluations: the LawBench study finds that “scaling up the model size results in better performance in one‑shot case” and that “increasing the model size typically helps improve model performance in one‑shot settings” (LawBench, 4 Experiment > 4.4 Analysis, p.13).  
* However, the benefit is less reliable in zero‑shot scenarios. LawBench notes that “in zero‑shot scenarios, mixed results are observed, simply increasing the model size may not automatically lead to better performance” (LawBench, 4 Experiment > 4.4 Analysis, p.13).  

Thus, making a model bigger generally improves legal task performance, especially when the model is evaluated in one‑shot or when comparing models of the same family, but larger size does not guarantee gains in zero‑shot settings.

**Sources**

- *LegalBench: A collaboratively built benchmark for measuring legal reasoning in large language models*, 5.2 Performance trends, p.13.  
- *LawBench: Benchmarking Legal Knowledge of Large Language Models*, 4 Experiment > 4.4 Analysis, p.13.

### evidence

Increasing a model’s size tends to improve performance in one‑shot legal tasks, but the benefit is not consistent across all settings. The analysis of several models shows that larger models usually achieve higher accuracy and lower abstention rates in one‑shot scenarios, indicating they follow instructions better. However, in zero‑shot scenarios the results are mixed—simply scaling up does not automatically yield better performance, and an outlier (ChatLaw) even performed worse when made larger. Consequently, making a model bigger is not a universally reliable way to boost legal‑task performance; the effect depends on the evaluation setting and the specific model.  

**Sources**

- LawBench: Benchmarking Legal Knowledge of Large Language Models, 4 Experiment > 4.4 Analysis, p.13 – “Scaling up the model size results in better performance in one-shot case… we observe that increasing the model size typically helps improve model performance in one-shot settings… In zero-shot scenarios, mixed results are observed, simply increasing the model size may not automatically lead to better performance… ChatLaw is an outlier, a larger size results in lower performance.”
