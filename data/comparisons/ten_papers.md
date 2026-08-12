# Retrieval comparison — 2026-08-12 15:10

Answering model `openai/gpt-oss-120b` at temperature 0.0, embeddings `openai/text-embedding-3-small`, top_k=5. Extraction ran on `openai/gpt-oss-120b`.

- **plain** — nearest chunks only, no graph. The control.
- **local** — nearest chunks, plus the claims each one grounds.
- **global** — community summaries only.
- **hybrid** — community summaries, plus each theme's claims and the verbatim passage behind them.


---

## Q1. How do multilingual or cross-lingual legal NLP tasks differ from English-only ones?

### plain

Multilingual or cross‑lingual legal NLP tasks involve several challenges that are not present in English‑only (monolingual) settings:

* **Lack of prior work on cross‑lingual transfer in the legal domain.**  
  While legal topic classification has been explored for EU legislation in English, “cross‑lingual transfer has not been studied in the legal domain” (MultiEURLEX, 2 Related Work, p.2‑3).  

* **Need for models that retain knowledge across many languages.**  
  Fine‑tuning a multilingual pretrained model on a single source language causes “catastrophic forgetting of multilingual knowledge and, consequently, poor zero‑shot transfer to target languages” (MultiEURLEX, Abstract, p.1; 7 Conclusions, p.9).  

* **Adaptation strategies are required to preserve multilingual competence.**  
  Techniques such as partial fine‑tuning, adapters, BITFIT, and LNFIT “help retain multilingual knowledge from pretraining, substantially improving zero‑shot cross‑lingual transfer” (MultiEURLEX, 1 Introduction, p.1‑2; 7 Conclusions, p.9).  

* **Temporal concept drift interacts with multilingual splits.**  
  The dataset shows that “chronological, instead of random, splits” are important because “temporal concept drift” can otherwise over‑estimate performance, a factor that becomes more complex when the same legal concepts evolve across many languages (MultiEURLEX, 1 Introduction, p.1‑2; 7 Conclusions, p.9).  

* **Scale and diversity of languages.**  
  MULTI‑EURLEX covers “23 official EU languages … one of the most diverse, in terms of languages, classification datasets” (MultiEURLEX, 7 Conclusions, p.9), requiring models that can handle a much larger linguistic variety than English‑only corpora.

In contrast, English‑only legal NLP research typically trains and evaluates models on monolingual data, does not need to address cross‑lingual adaptation or catastrophic forgetting, and can rely on existing English‑focused resources and benchmarks (e.g., prior EU legislation classification studies cited in the related‑work paragraph).  

**Sources**

- MultiEURLEX – “Legal topic classification has been studied … in a monolingual setting (English). … cross‑lingual transfer has not been studied in the legal domain.” (Section 2 Related Work, p.2‑3).  
- MultiEURLEX – “We find that fine‑tuning a multilingual model in a single source language leads to catastrophic forgetting of multilingual knowledge and, consequently, poor zero‑shot transfer to other languages.” (Abstract, p.1).  
- MultiEURLEX – “Adaptation strategies … help retain multilingual knowledge from pretraining, substantially improving zero‑shot cross‑lingual transfer.” (Section 1 Introduction, p.1‑2).  
- MultiEURLEX – “We also used MULTI‑EURLEX to highlight the effect of temporal concept drift and the importance of chronological, instead of random, splits.” (Section 7 Conclusions, p.9).  
- MultiEURLEX – “To the best of our knowledge, this is one of the most diverse, in terms of languages, classification datasets.” (Section 7 Conclusions, p.9).

### local

Multilingual or cross‑lingual legal NLP tasks differ from English‑only (monolingual) tasks in several ways.

* **Scope of languages** – English‑only work typically trains and evaluates models on a single language (e.g., the EU‑legislation classification studies that used only English documents [MultiEURLEX – 1 Introduction, p.1‑2]).  Cross‑lingual research, by contrast, aims to transfer knowledge from a resource‑rich source language to one or more target languages that may have little or no labeled data.  The MULTI‑EURLEX dataset provides parallel EU laws in 23 official EU languages, enabling such zero‑shot transfer experiments [MultiEURLEX – Abstract, p.1‑1].

* **Training strategy** – In monolingual settings a model is fine‑tuned on the target language data directly.  When a multilingual pretrained model (e.g., XLM‑ROBERTA or MT5) is fine‑tuned on a single source language, it suffers catastrophic forgetting of the multilingual knowledge it acquired during pre‑training, leading to poor performance on other languages [MultiEURLEX – 1 Introduction, p.1‑2; MultiEURLEX – Abstract, p.1‑1].

* **Adaptation techniques** – Cross‑lingual legal NLP therefore relies on adaptation methods (partial fine‑tuning, adapters, BITFIT, LNFIT) that preserve multilingual knowledge and substantially improve zero‑shot transfer [MultiEURLEX – 1 Introduction, p.1‑2; MultiEURLEX – 7 Conclusions and Future Work, p.9‑9].  Such techniques are not required for English‑only tasks, where standard fine‑tuning of monolingual models is sufficient.

* **Evaluation considerations** – Legal topics evolve over time, so temporal concept drift must be accounted for.  Chronological train/dev/test splits are recommended for cross‑lingual legal classification because random splits can over‑estimate performance, a concern that is less pronounced in single‑language studies [MultiEURLEX – 1 Introduction, p.1‑2; MultiEURLEX – 7 Conclusions and Future Work, p.9‑9].

* **Resource availability** – While many legal NLP datasets exist for English (e.g., contract‑review or judgment‑prediction corpora), comparable multilingual resources have been scarce.  MULTI‑EURLEX is one of the first large‑scale, parallel, multilingual legal classification datasets, making cross‑lingual research feasible [MultiEURLEX – 2 Related Work, p.2‑3].

**Sources**

* MultiEURLEX – 1 Introduction, p.1‑2  
* MultiEURLEX – Abstract, p.1‑1  
* MultiEURLEX – 2 Related Work, p.2‑3  
* MultiEURLEX – 7 Conclusions and Future Work, p.9‑9

### global

The provided material does not contain any specific passages from individual papers that describe how multilingual or cross‑lingual legal NLP tasks differ from English‑only tasks. The themes summarize broad findings (e.g., that multilingual benchmarks emphasize low lexical overlap and that cross‑lingual transfer can suffer when shared lexical items are removed), but no citable sections or page numbers from particular papers are given for those claims. Therefore, I cannot supply a sourced answer to the question.  

**Sources**  
The context only includes thematic summaries without attributable paper sections or page numbers, so no citations can be provided.

### hybrid

Multilingual and cross‑lingual legal NLP tasks involve additional challenges that are not present in English‑only settings.  

* **Data availability** – While many English‑language legal benchmarks exist, parallel or comparable resources in other languages are scarce, so cross‑lingual transfer has rarely been explored in the legal domain. The authors note that “cross‑lingual transfer has not been studied in the legal domain” despite a growing body of multilingual NLP work (Citation: Multi‑EURLEX, Related Work, p.2).  

* **Language diversity** – Legal documents must be processed in up to 23 official EU languages, each with its own legal terminology, morphology and script. This diversity requires models that can retain multilingual knowledge across languages, which is difficult because fine‑tuning on a single source language often causes “catastrophic forgetting” and leads to poor zero‑shot transfer (Citation: Multi‑EURLEX, Introduction, p.1).  

* **Adaptation strategies** – To mitigate forgetting, researchers employ techniques such as partial fine‑tuning, adapters, BITFIT or LNFIT, which help preserve the multilingual representations learned during pre‑training and improve cross‑lingual performance (Citation: Multi‑EURLEX, Abstract, p.1).  

* **Temporal and label‑set effects** – Legal topic classification suffers from temporal concept drift, and the size of the label set influences how much adaptation helps; larger label sets yield larger gains in cross‑lingual transfer (Citation: Multi‑EURLEX, Conclusions, p.9).  

* **Evaluation differences** – Multilingual benchmarks like MULTI‑EURLEX are designed as testbeds for zero‑shot transfer, where a classifier trained on a resource‑rich language (e.g., English) is evaluated on languages with few or no training examples. This contrasts with English‑only benchmarks that typically provide ample labeled data for each task.  

Overall, multilingual legal NLP must contend with limited multilingual resources, the risk of losing cross‑lingual knowledge during fine‑tuning, and the need for specialized adaptation methods, whereas English‑only tasks can rely on abundant monolingual data and standard fine‑tuning pipelines.  

**Sources**  
- Multi‑EURLEX – “cross‑lingual transfer has not been studied in the legal domain” (Related Work, p.2)  
- Multi‑EURLEX – “fine‑tuning a multilingual model in a single source language leads to catastrophic forgetting…poor zero‑shot transfer” (Introduction, p.1)  
- Multi‑EURLEX – “adaptation strategies…help retain multilingual knowledge…substantially improving zero‑shot cross‑lingual transfer” (Abstract, p.1)  
- Multi‑EURLEX – “gains increase as the label set increases” (Conclusions, p.9)


---

## Q2. What methods are used to extract structured information from contracts?

### plain

The papers describe **annotation‑driven clause extraction** as the way structured information is pulled from contracts.  

* In CUAD the contracts are first **labeled by law‑students and quality‑checked by lawyers** for 41 clause categories.  For each label the annotators identify the exact start‑ and end‑tokens of the relevant clause, thereby turning the unstructured text into a set of **spans that correspond to structured legal concepts** (e.g., party names, governing law, liability limits).  Models are then trained to **output those token spans**, effectively extracting the structured information automatically (CUAD, “3 CUAD: A Contract Review Dataset”, pp. 3‑4).  

* The same approach is reiterated in the CUAD statistics: “For each label category, we identify every clause in every contract that is most relevant to that label category. We then have models extract the relevant clauses from a contract by outputting the start and end tokens that identify the span of text that relates to that label category” (CUAD, “3 CUAD: A Contract Review Dataset”, pp. 3‑4).  

Thus, the method used to obtain structured information is **manual expert annotation of clause spans followed by machine‑learning models that learn to predict those spans**, turning raw contract text into a structured set of labeled clauses.

**Sources**

- CUAD: An Expert‑Annotated NLP Dataset for Legal Contract Review, *3 CUAD: A Contract Review Dataset*, pp. 3‑4.  
- CUAD: An Expert‑Annotated NLP Dataset for Legal Contract Review, *3 CUAD: A Contract Review Dataset*, pp. 3‑4.

### local

**Answer**

The papers describe two complementary approaches for extracting structured information from contracts:

1. **Span‑based annotation and supervised learning** –  
   *Contracts are first manually annotated by trained law‑students and lawyers, who highlight every text span that corresponds to each of 41 predefined clause categories (e.g., Governing Law, Non‑Compete). The annotation process includes extensive training (70‑100 h) and detailed guidelines covering more than 100 pages.*  
   *A machine‑learning model is then trained to predict the start and end token positions of the relevant spans for a given clause category, effectively extracting the structured clause information from the raw contract text.*  
   *(CUAD: An Expert‑Annotated NLP Dataset for Legal Contract Review, “3 CUAD: A Contract Review Dataset”, p.3‑4; CUAD: An Expert‑Annotated NLP Dataset for Legal Contract Review, “CUAD Contract Page Lengths”, p.4‑5)*  

2. **Prompt‑driven large language model (LLM) extraction** –  
   *A system prompt is crafted to instruct an LLM (e.g., GPT‑4‑1106) to act as an experienced lawyer reviewing a contract from a specific party’s perspective. The prompt asks the model to identify every checklist item that is met or not met, to return the exact contract lines that support each decision, and to output the results in a structured JSON format (including fields such as checklist numbering, contract lines, explanation, check‑met flag, and assumptions). This prompt‑based approach extracts the same kind of clause‑level information without requiring explicit span annotations.*  
   *(Better Call GPT, Comparing Large Language Models Against Lawyers, “Table 6”, p.14)*  

Together, these methods provide both a supervised, annotation‑driven pipeline and a zero‑shot, prompt‑based pipeline for turning unstructured contract text into structured, machine‑readable clause information.  

**Sources**

- *CUAD: An Expert‑Annotated NLP Dataset for Legal Contract Review*, “3 CUAD: A Contract Review Dataset”, p.3‑4 – “Each example is a contract (full text) together with 41 predefined clause categories… annotators highlighted every span of text… The model’s task is… to output the start and end token positions of each relevant span.”  
- *CUAD: An Expert‑Annotated NLP Dataset for Legal Contract Review*, “CUAD Contract Page Lengths”, p.4‑5 – “We had contracts labeled by law students and quality‑checked by experienced lawyers… law students first went through 70‑100 hours of training… documentation… more than one hundred pages… ensures that labels are consistent.”  
- *Better Call GPT, Comparing Large Language Models Against Lawyers*, “Table 6”, p.14 – “System Prompt… Your goal is to identify any legal issues… For each section of the provided contract, carefully analyze it and identify ALL of the checks… Format your answer as a JSON object that includes… contract_Lines… explanation… check_Met… assumptions.”

### global

The provided context does not contain any specific information about the methods that are used to extract structured information from contracts. The excerpts focus on benchmark datasets, model performance, retrieval techniques, and evaluation frameworks, but they do not describe particular extraction approaches (e.g., rule‑based parsing, named‑entity recognition, sequence‑to‑sequence models, or other NLP pipelines) for structuring contract content.

**Sources**

The context includes thematic summaries of legal‑focused datasets and benchmark results, but none of the cited passages detail contract‑information‑extraction methods. Consequently, no citations can be provided for this question.

### hybrid

**Answer**  
The papers describe two complementary approaches for turning the unstructured text of contracts into structured information:

1. **Span‑level clause extraction** –  contracts are annotated with the exact start and end token positions of every clause that belongs to a predefined legal category (e.g., Governing Law, Non‑Compete).  Models are trained to predict these spans, thereby “highlighting” the salient portions of a contract that a lawyer should review.  This formulation turns a raw contract into a set of labeled spans that can be downstream‑processed as structured clause data. (CUAD: An Expert‑Annotated NLP Dataset for Legal Contract Review, 3 CUAD: A Contract Review Dataset, p.3)

2. **Prompt‑driven issue‑spotting with LLMs** –  a system prompt is given to a large language model that instructs it to act as an experienced lawyer, to read a contract, and to return, for each checklist item, the exact contract sentences or clauses that satisfy (or fail) the check, together with a JSON‑formatted explanation.  This “check‑list” prompting turns the contract into a structured list of identified issues, each linked to the corresponding contract text. (Better Call GPT, Comparing Large Language Models Against Lawyers, Table 6, p.14)

Together, these methods provide a pipeline that first locates relevant contract passages (span extraction) and then maps them to a predefined schema or checklist (prompt‑driven issue‑spotting), yielding structured representations of contract obligations, risks, and compliance items.  

**Sources**  
- CUAD: An Expert‑Annotated NLP Dataset for Legal Contract Review, 3 CUAD: A Contract Review Dataset, p.3  
- Better Call GPT, Comparing Large Language Models Against Lawyers, Table 6, p.14


---

## Q3. What risks and responsibilities come with building large legal datasets?

### plain

**Answer**

Building large legal datasets carries several intertwined risks and responsibilities:

1. **Risk of Harm from Sensitive or Restricted Content** –  
   Large‑scale pre‑training data can contain *biased, obscene, copyrighted, and private information* that, if left unchecked, may cause significant harm when models generate output (Abstract, Pile of Law, p.1).  

2. **Privacy Risks and Data Leakage** –  
   Legal documents often include *personal identity, financial status, and medical records*. When such data are used for training, there is a danger that a model could unintentionally reveal this sensitive information in its generations, leading to data leakage (A. Data privacy, Legal Evalutions and Challenges of Large Language Models, p.7).  

3. **Responsibility to Apply Legal‑Based Filtering** –  
   The authors argue that filtering should be *grounded in law*, drawing on the “legal norms that governments have developed to constrain the inclusion of toxic or private content” and turning those norms into actionable guidelines for researchers (Abstract, Pile of Law, p.1).  

4. **Ethical Duty to Remove or Mitigate Sensitive Material** –  
   Even though the underlying records are public, the dataset may still contain *sensitive material that has escaped administrative scrutiny*. The creators discuss *ethics of the work and propose mechanisms for content removal* (Section 2 Pile of Law, p.2‑3).  

5. **Ensuring Transparency and Ongoing Curation** –  
   Because the dataset is *public and mostly under permissive licenses*, the authors commit to *continuously adding material* and *characterizing the dataset in detail* so that the community can understand what is included and how it is filtered (Section 2 Pile of Law, p.2‑3).  

In sum, constructing a massive legal corpus requires careful **risk mitigation** (preventing exposure of private, copyrighted, or harmful content) and **responsible stewardship** (applying legally grounded filters, providing mechanisms for content removal, and maintaining transparent documentation).

**Sources**

- *Pile of Law: Learning Responsible Data Filtering from the Law and a 256GB Open-Source Legal Dataset*, Abstract, p.1.  
- *Pile of Law: Learning Responsible Data Filtering from the Law and a 256GB Open-Source Legal Dataset*, Section 2 Pile of Law, pp.2‑3.  
- *Legal Evalutions and Challenges of Large Language Models*, A. Data privacy, p.7.

### local

Building large legal datasets carries several important risks and corresponding responsibilities that the literature highlights.

**Risks**

1. **Privacy and data‑leakage** – Large language models trained on legal texts can unintentionally expose personal, financial, medical or other sensitive information that appears in the source documents.  This creates a risk of leaking individuals’ private data during generation. [Legal Evalutions and Challenges of Large Language Models, A. Data privacy, p.7]

2. **Toxic, biased or copyrighted content** – Pre‑training on massive collections of legal material may incorporate obscene, hateful, biased or copyrighted material, which can cause downstream harms when the model is deployed. [Pile of Law: Learning Responsible Data Filtering from the Law and a 256GB Open‑Source Legal Dataset, Abstract, p.1]

3. **Legal‑norm violations** – Because legal documents are often subject to specific statutory or regulatory restrictions (e.g., privacy statutes, confidentiality rules), indiscriminate inclusion of such material can breach those norms. [Pile of Law: Learning Responsible Data Filtering from the Law and a 256GB Open‑Source Legal Dataset, 2 Pile of Law, p.2‑3]

**Responsibilities**

1. **Context‑aware filtering grounded in law** – Dataset curators should adopt filtering mechanisms that reflect governmental legal standards for privacy, toxicity and copyright, rather than relying on ad‑hoc heuristics. [Pile of Law: Learning Responsible Data Filtering from the Law and a 256GB Open‑Source Legal Dataset, Abstract, p.1]

2. **Explicit ethical review and content‑removal processes** – The creation of a legal dataset must be accompanied by an ethics discussion and concrete mechanisms for removing or redacting sensitive material that escaped initial scrutiny. [Pile of Law: Learning Responsible Data Filtering from the Law and a 256GB Open‑Source Legal Dataset, 2 Pile of Law, p.2‑3]

3. **Rigorous data‑processing and output‑review pipelines** – Researchers should implement strict data‑processing pipelines and systematic review of model outputs to ensure that generated text does not disclose protected personal information. [Legal Evalutions and Challenges of Large Language Models, A. Data privacy, p.7]

4. **Transparency about licensing and public‑record status** – Since many legal sources are public records but may have varying license terms, curators must verify that all included material is under permissive or otherwise compatible licenses and clearly document this provenance. [Pile of Law: Learning Responsible Data Filtering from the Law and a 256GB Open‑Source Legal Dataset, 2 Pile of Law, p.2‑3]

In sum, building large legal corpora demands careful attention to privacy, bias, copyright, and compliance with legal norms, together with transparent, law‑grounded filtering, ethical oversight, and robust review mechanisms to mitigate these risks.

**Sources**

- *Pile of Law: Learning Responsible Data Filtering from the Law and a 256GB Open‑Source Legal Dataset*, Abstract, p.1 – “One concern with the rise of large language models lies with their potential for significant harm, particularly from pretraining on biased, obscene, copyrighted, and private information…”
- *Pile of Law: Learning Responsible Data Filtering from the Law and a 256GB Open‑Source Legal Dataset*, 2 Pile of Law, p.2‑3 – “Each of these data sources carries with it an implicit filtering mechanism formed under relevant legal standards of privacy and toxicity… We discuss the ethics of our work and our proposed mechanisms for content removal…”
- *Legal Evalutions and Challenges of Large Language Models*, A. Data privacy, p.7 – “Cases in the legal domain often involve individuals' sensitive information… there is a risk that the model may unintentionally expose people's sensitive information during content generation… the design and training processes of the model must prioritize the protection of data… implement a rigorous data processing and review mechanism for the model's outputs.”

### global

The provided context does not contain any specific passages that state the risks and responsibilities associated with building large legal datasets, nor does it give page‑level citations from individual papers that discuss these issues. The themes summarize general concerns (e.g., data confidentiality, privacy leaks, bias, and ethical accountability), but because no concrete, citable excerpts from a particular paper, section, and page are present, I cannot provide a sourced answer.  

**Sources**  
The context only includes thematic summaries without verifiable citations; therefore no specific source can be listed.

### hybrid

Building large legal datasets brings several important risks and responsibilities that the literature repeatedly emphasizes:

* **Privacy and data‑leakage risk** – Legal documents often contain personally identifying, financial, or medical information. When such data are used for model training, there is a real danger that a language model could unintentionally reproduce or expose that sensitive information in its outputs. Researchers must therefore design training pipelines, output‑filtering, and review procedures that prioritize the protection of private data and comply with privacy regulations. (Legal Evalutions and Challenges of Large Language Models, A. Data privacy, p.7)

* **Bias and fairness concerns** – Because legal corpora are assembled from many heterogeneous sources, they can embed historical biases, stereotypes, or systematic imbalances. If these biases are not identified and mitigated, models trained on the data may produce unfair or discriminatory predictions, which is especially problematic in a domain where impartiality is a core value. (Legal Evalutions and Challenges of Large Language Models, C. Ethical and moral issues, p.8)

* **Legal‑norm‑aware content filtering** – Large‑scale legal collections may include material that is obscene, copyrighted, or otherwise restricted. Curating a dataset therefore requires a careful, law‑grounded filtering strategy that respects intellectual‑property rights, toxicity standards, and other legal constraints. The curators of the Pile of Law explicitly discuss the need for responsible filtering and for documenting the implicit legal standards that govern each source. (Pile of Law: Learning Responsible Data Filtering from the Law and a 256 GB Open‑Source Legal Dataset, 2 Pile of Law, p.2)

* **Transparency and documentation** – Since the data are public but have never before been compiled at this scale, the creators must provide thorough documentation of the sources, licensing terms, and any preprocessing or filtering steps. This transparency enables downstream users to assess the provenance and legal compliance of the dataset and to reproduce or audit the preprocessing pipeline. (Pile of Law: Learning Responsible Data Filtering from the Law and a 256 GB Open‑Source Legal Dataset, Abstract, p.1)

* **Ethical stewardship** – Beyond technical safeguards, building such datasets entails an ethical responsibility to consider the broader societal impact of the resulting models, including potential misuse, the amplification of existing inequities, and the need for ongoing community oversight of data‑handling practices. (Pile of Law: Learning Responsible Data Filtering from the Law and a 256 GB Open‑Source Legal Dataset, 2 Pile of Law, p.2)

**Sources**

- Legal Evalutions and Challenges of Large Language Models, A. Data privacy, p.7  
- Legal Evalutions and Challenges of Large Language Models, C. Ethical and moral issues, p.8  
- Pile of Law: Learning Responsible Data Filtering from the Law and a 256 GB Open‑Source Legal Dataset, 2 Pile of Law, p.2  
- Pile of Law: Learning Responsible Data Filtering from the Law and a 256 GB Open‑Source Legal Dataset, Abstract, p.1


---

## Q4. How did legal NLP methods change with the arrival of large language models?

### plain

**Answer**

The emergence of large‑language models (LLMs) has shifted legal‑NLP from relatively narrow, rule‑based or task‑specific toolkits toward much broader, generative systems that can reason over legal texts, draft and summarize documents, and retrieve case law with far less hand‑crafted engineering.  

* **From specialized toolkits to general‑purpose generative models.**  
  Earlier work focused on open‑source toolkits such as **LexNLP**, which provided “text cleaning, tokenization, feature extraction, entity recognition, and text classification” for legal documents (Legal Evalutions…, C. Overview of legal‑specific LLMs, p.5). These systems were modular but required users to assemble pipelines for each downstream task.  

* **LLMs bring deep language understanding and cross‑modal abilities.**  
  The rapid progress of Transformer‑based LLMs (e.g., GPT‑3/4) has enabled “exceptional capabilities in natural language understanding and generation” that can be applied to legal reasoning, case retrieval, and question answering (Legal Evalutions…, I. INTRODUCTION, p.1‑2).  

* **Domain‑adapted LLMs now dominate legal NLP research.**  
  Researchers have begun fine‑tuning LLMs on large legal corpora, producing models such as **LawGPT**, **ChatLaw**, **LAWGPT‑zh**, **Lawyer‑LLama**, **LexiLaw**, etc. These models “exhibit superior capabilities in understanding legal concepts, conducting legal reasoning, and generating legal text” (Legal Evalutions…, C. Overview of legal‑specific LLMs, p.5).  

* **Expanded task coverage.**  
  Modern LLM‑based approaches are being evaluated on a wide range of tasks—summarization of judgments, drafting contract clauses, generating research memoranda, and even zero‑shot crime detection from textual descriptions—showing that LLMs can “assist legal professionals in tasks such as summarization, drafting, and legal research” (Legal Evalutions…, II. REVIEW OF LLMS IN THE LEGAL FIELD, p.2‑3).  

* **Performance gains and remaining limits.**  
  Benchmarks indicate that while LLMs often outperform earlier classifiers (e.g., GPT‑3.5 Turbo achieving a micro‑F1 of 49 % on LexGLUE, surpassing baseline guessing) they still struggle with nuanced legal language and factual precision (Legal Evalutions…, II. REVIEW OF LLMS IN THE LEGAL FIELD, p.2‑3).  

Overall, the arrival of LLMs transformed legal NLP from modular, narrowly‑focused pipelines to versatile, generative systems that can be fine‑tuned for domain‑specific knowledge, dramatically broadening the range of automatable legal tasks while introducing new challenges around accuracy, bias, and interpretability.

**Sources**

1. *Legal Evalutions and Challenges of Large Language Models*, **C. Overview of legal‑specific LLMs**, p.5.  
2. *Legal Evalutions and Challenges of Large Language Models*, **I. INTRODUCTION**, p.1‑2.  
3. *Legal Evalutions and Challenges of Large Language Models*, **II. REVIEW OF LLMS IN THE LEGAL FIELD**, p.2‑3.

### local

The emergence of large‑language models (LLMs) has turned legal natural‑language processing from a set of relatively narrow, rule‑ or pipeline‑based tools into a broader, generative approach that can both understand and produce legal text.

* **From modular toolkits to generative models.**  Earlier work relied on specialized NLP libraries such as LexNLP, which provide “text cleaning, tokenization, feature extraction, entity recognition, and text classification” for legal documents and are valued for their “modular design and flexible API” that let users build custom research or contract‑analysis pipelines [Legal Evalutions and Challenges of Large Language Models, C. Overview of legal‑specific LLMs, p.5].  

* **Fine‑tuned, domain‑specific LLMs.**  The same survey notes that, beyond general‑purpose LLMs, researchers have created models that are “fine‑tuned on extensive legal corpora” and that “exhibit superior capabilities in understanding legal concepts, conducting legal reasoning, and generating legal text” [Legal Evalutions and Challenges of Large Language Models, C. Overview of legal‑specific LLMs, p.5].  Examples include LawGPT, ChatLaw, and ChatLaw2‑MOE, which are built on large base models (e.g., ChatGLM‑6B) and then adapted with Chinese legal data and instruction tuning.

* **Expanded task coverage.**  LLMs now support a wider range of legal tasks such as case summarization, contract drafting, legal research, and question answering, which were previously handled by separate, narrowly‑focused modules [Legal Evalutions and Challenges of Large Language Models, II. REVIEW OF LLMS IN THE LEGAL FIELD, p.2‑3].

* **Performance gains and remaining limits.**  The papers report that these legal‑specific LLMs achieve higher accuracy on benchmark tasks than earlier toolkits, but they still suffer from “non‑negligible factual and legal inaccuracies” and hallucination risks, especially when interpreting highly specialized legal language [Legal Evalutions and Challenges of Large Language Models, I. INTRODUCTION, p.1‑2]; [Legal Evalutions and Challenges of Large Language Models, II. REVIEW OF LLMS IN THE LEGAL FIELD, p.2‑3].

In sum, the arrival of LLMs shifted legal NLP from rule‑based, modular processing toward large, fine‑tuned generative models that can perform richer reasoning and text generation, while introducing new challenges around accuracy and reliability.

**Sources**

- Legal Evalutions and Challenges of Large Language Models, *C. Overview of legal‑specific LLMs*, p.5 – passage describing LexNLP’s modular toolkit and the emergence of fine‑tuned legal LLMs such as LawGPT and ChatLaw.  
- Legal Evalutions and Challenges of Large Language Models, *I. INTRODUCTION*, p.1‑2 – passage noting the transformative potential of LLMs in legal services and the persistent issues of factual and legal inaccuracies.  
- Legal Evalutions and Challenges of Large Language Models, *II. REVIEW OF LLMS IN THE LEGAL FIELD*, p.2‑3 – passage outlining the expanded capabilities of LLMs for summarization, drafting, research, and the continuing concerns about hallucinations and accuracy.

### global

The provided context does not contain any specific passages from individual papers that describe how legal‑NLP methods changed with the arrival of large language models. The themes summarize overall trends, but they do not include citable sections or page numbers from particular papers that could be referenced. Therefore, I cannot give a sourced answer to the question.

### hybrid

Legal natural‑language‑processing (NLP) in the legal domain has moved from narrow, task‑specific toolkits toward large, general‑purpose language models that are either used directly or fine‑tuned on legal corpora.  

* Early work focused on rule‑based pipelines and small‑scale models (e.g., LexNLP) that provided tokenisation, entity extraction and classification for legal texts.  These systems were modular but limited to the narrow functions they were programmed to perform.  

* The rapid progress of transformer‑based LLMs (e.g., GPT‑3/4, Claude, Gemini) introduced models with broad linguistic competence that can understand and generate legal language, perform summarisation, drafting, question answering and reasoning across many tasks.  Researchers have begun to evaluate these models on legal benchmarks (LEGALBENCH, LawBench, case‑analysis datasets) and to compare them with human lawyers.  

* Because generic LLMs lack domain expertise, a new wave of **legal‑specific LLMs** has emerged.  These models are fine‑tuned on large legal corpora such as the Pile of Law or on curated Chinese legal datasets, yielding “superior capabilities in understanding legal concepts, conducting legal reasoning, and generating legal text” (Legal Evalutions and Challenges of Large Language Models, C. Overview of legal‑specific LLMs, p.5).  

* Pre‑training on the Pile of Law has been shown to improve downstream performance on legal tasks that could increase access to justice (Pile of Law: Learning Responsible Data Filtering from the Law and a 256 GB Open‑Source Legal Dataset, Abstract, p.1).  

* The arrival of LLMs has also shifted evaluation practices: researchers now benchmark models on multi‑task legal suites (LEGALBENCH, LawBench) and study the impact of prompting, in‑context examples and context‑window size, rather than relying solely on handcrafted rule sets.  

* At the same time, new challenges have appeared—biases inherited from training data, factual inaccuracies, privacy leakage, and the need for robust content‑filtering—prompting calls for ethical review mechanisms and better data‑sanitisation (Legal Evalutions and Challenges of Large Language Models, C. Ethical and moral issues, p.8).  

Overall, the field has transitioned from narrowly engineered NLP pipelines to large, adaptable language models that can be specialised for law through fine‑tuning and prompting, while also confronting novel technical and ethical issues.

**Sources**

- Legal Evalutions and Challenges of Large Language Models, C. Overview of legal‑specific LLMs, p.5  
- Pile of Law: Learning Responsible Data Filtering from the Law and a 256 GB Open‑Source Legal Dataset, Abstract, p.1  
- Legal Evalutions and Challenges of Large Language Models, I. INTRODUCTION, p.1  
- Legal Evalutions and Challenges of Large Language Models, C. Ethical and moral issues, p.8


---

## Q5. Does making a model bigger reliably improve legal task performance?

### plain

**Answer**

Increasing a model’s size tends to improve legal‑task performance, but the improvement is not guaranteed across all settings.  

* In the **LawBench** study, scaling up model size *usually* raises scores and lowers abstention rates in one‑shot scenarios, yet the effect is less consistent in zero‑shot settings and there are notable exceptions (e.g., the larger ChatLaw model performed worse)【LawBench: Benchmarking Legal Knowledge of Large Language Models, 4.4 Analysis, pp.13‑15】.  
* The **LEGALBENCH** analysis reports that, *within the same model family*, larger models “usually outperform smaller models” on average across reasoning categories, though the margin varies and some families show only modest gains【LEGALBENCH: A COLLABORATIVELY BUILT BENCHMARK…, 5.2 Performance trends, pp.13‑15】.  

Thus, while bigger models often deliver better results, the relationship is not perfectly reliable; performance gains depend on the prompting regime (one‑shot vs. zero‑shot), the specific architecture, and the training/fine‑tuning approach.

---

**Sources**

1. *LawBench: Benchmarking Legal Knowledge of Large Language Models*, Section 4 Experiment > 4.4 Analysis, pp. 13‑15.  
2. *LEGALBENCH: A COLLABORATIVELY BUILT BENCHMARK FOR MEASURING LEGAL REASONING IN LARGE LANGUAGE MODELS*, Section 5.2 Performance trends, pp. 13‑15.

### local

Increasing the size of a language model tends to raise its performance on legal tasks, but the improvement is not guaranteed in every setting.

* **Within a model family, larger models usually beat smaller ones.** LEGALBENCH reports that “larger models usually outperform smaller models” and gives concrete examples such as Flan‑T5‑XXL (11 B) beating Flan‑T5‑XL (3 B) and LLaMA‑2‑13B beating LLaMA‑2‑7B across most reasoning categories【LEGALBENCH, 5.2 Performance trends, p.13‑15】.  

* **The gain is more consistent in one‑shot prompting.** The LawBench analysis finds that “scaling up the model size results in better performance in one‑shot case” and that the improvement is “more consistent in the one‑shot than in the zero‑shot scenario”【LawBench, 4 Experiment > 4.4 Analysis, p.13‑15】.  

* **Zero‑shot performance shows mixed results.** The same LawBench passage notes that “simply increasing the model size may not automatically lead to better performance” in zero‑shot settings, and cites an outlier (ChatLaw) where a larger model performed worse【LawBench, 4 Experiment > 4.4 Analysis, p.13‑15】.  

Thus, larger models generally provide better legal‑task performance—especially when evaluated in one‑shot or when compared within the same architecture family—but the benefit is not uniformly reliable across all prompting regimes or model families.  

**Sources**

* LEGALBENCH: “Within a model family, larger models usually outperform smaller models… Flan‑T5‑XXL (11B) outperforms Flan‑T5‑XL (3B)… LLaMA‑2‑13B outperforms LLaMA‑2‑7B” (Section 5.2 Performance trends, p.13‑15).  
* LawBench: “Scaling up the model size results in better performance in one‑shot case… scaling up the model size usually improves the performance, but the improvement is more consistent in the one‑shot than in the zero‑shot scenario… simply increasing the model size may not automatically lead to better performance” (Section 4 Experiment > 4.4 Analysis, p.13‑15).

### global

The evidence is mixed.  Across the legal‑LLM literature, larger architectures tend to achieve higher scores on many benchmarks (for example, DeBERTa‑xlarge consistently yields the best precision‑recall trade‑offs on contract‑review tasks, and ultra‑long‑context models such as Claude 2.0/2.1 and Gemini 1.5 improve performance on very long documents).  However, size alone does not guarantee better results: domain‑specific legal models that are larger but built on weaker base models often fail to outperform smaller, general‑purpose Chinese LLMs, and performance remains highly sensitive to prompting, context‑window limits, and the quality of in‑context examples.  Consequently, while increasing model size can help, it is not a reliable sole predictor of legal task performance.

**Sources**

- Legal Retrieval and Question‑Answering Benchmarks, “Model size and architecture matter: DeBERTa‑xlarge consistently attains the highest precision‑recall trade‑offs on contract‑review tasks (CUAD) …”  
- Long‑Context Legal Reasoning with Large Language Models, “Recent models with ultra‑long context windows (Claude 2.0/2.1, Gemini 1.5) … improve scalability.”  
- Legal Reasoning and Task Performance of Large Language Models, “domain‑specific legal LLMs often do not surpass general‑purpose Chinese LLMs, likely because they are built on weaker base models.”  
- Legal Large Language Model Evaluation and Training, “results remain highly sensitive to prompting choices, context‑window size, and the quality of in‑context examples.”

### hybrid

Increasing the size of a language model tends to raise its legal‑task performance, but the improvement is not guaranteed in every setting.  

* In the LawBench experiments the authors observe that “scaling up the model size usually improves the performance, but the improvement is more consistent in the one‑shot than in the zero‑shot scenario” (LawBench, 4 Experiment > 4.4 Analysis, p.13).  
* A broader survey of LEGALBENCH results reports that “within LLM families, larger models usually outperform smaller models” (LEGALBENCH, 5.2 Performance trends, p.13).  

Together these findings indicate that bigger models are generally beneficial, especially when a few‑shot prompt is available, yet size alone does not automatically yield better results for all evaluation conditions (e.g., zero‑shot).  

**Sources**  
- LawBench: Benchmarking Legal Knowledge of Large Language Models, 4 Experiment > 4.4 Analysis, p.13  
- LEGALBENCH: A Collaboratively Built Benchmark for Measuring Legal Reasoning in Large Language Models, 5.2 Performance trends, p.13
