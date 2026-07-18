# **Feasibility, Algorithmic Frameworks, and Architectural Integration of Morphologically-Optimized Tamil Small Language Models**

The deployment of massive, general-purpose large language models has transformed natural language processing, yet these systems suffer from a pronounced typological bias. Standard tokenization algorithms, such as Byte-Pair Encoding and WordPiece, operate under script-agnostic assumptions that optimize for languages with analytic or fusional morphologies. Consequently, highly agglutinative languages—such as the Dravidian family, represented prominently by Tamil—face severe performance degradation, token inflation, and increased inference costs.  
This report evaluates the computational and linguistic feasibility of constructing a specialized monolingual Small Language Model optimized for the Tamil language. It details rule-based morphological parsing systems, evaluates the impact of grammar-first tokenization, and describes the architectural integration pathways required to connect a specialized monolingual model with a large multilingual target system.

## **The Linguistic Challenge of Dravidian Agglutination**

Tamil is characterized by an extremely rich, concatenative, and productive morphological structure. In Tamil syntax, a single orthographic word frequently encodes information that English distributes across entire phrases, including the lexical root, tense, aspect, mood, case markings, and person-number-gender agreement. For example, the inflected verb படித்துக்கொண்டிருக்கிறேன் ("I am studying") comprises five distinct morphemes fused into a single orthographic unit.  
When standard statistical tokenizers encounter such highly productive word-formation patterns, they fail to recognize morphemic boundaries. Because statistical merges are driven strictly by byte or character co-occurrence frequencies, the tokenizer fragments agglutinative chains into arbitrary byte sequences. This structural mismatch leads to three fundamental failure modes:

* **Morpheme Boundary Violation**: The tokenizer cuts across natural linguistic junctions (e.g., splitting the Tamil word வீடுகளுக்கு, meaning "for the houses," into the invalid segments வீட|ு களுக்கு), which disrupts the semantic coherence of the subword units.  
* **Extreme Sequence Inflation**: Because the tokenizer fails to compress the text effectively, the average number of tokens generated per word (the fertility rate) escalates significantly. High fertility rates saturate the transformer's attention window and inflate operational costs.  
* **Semantic and Syntactic Degradation**: The model's embedding layers must spend parameter capacity reconstructing basic word-level syntax, which reduces the parameters available for high-level textual reasoning and logical completion.

To resolve these limitations, Zipf's Principle of Least Effort can be used to formalize the tokenization challenge. The objective function of a linguistically aware tokenizer balances the total token count against the vocabulary size:  
C(\\text{tokenization}) \= \\alpha N\_{\\text{tokens}} \+ \\beta N\_{\\text{types}}  
In this equation, N\_{\\text{tokens}} represents the total token count (reflecting operational memory load), N\_{\\text{types}} represents the vocabulary size (reflecting long-term parameter storage costs), and \\alpha, \\beta \\ge 0 are system efficiency weights. Agglutinative languages require tokenizers that prioritize grammatical rules as a prior over statistical frequencies. This approach ensures that N\_{\\text{tokens}} is minimized without expanding the vocabulary to an unmanageable size.

## **Feasibility of Monolingual Tamil Small Language Models**

Developing a highly specialized monolingual Small Language Model for Tamil is computationally feasible and highly effective. This approach addresses the data scarcity and vocabulary limitations of multilingual architectures. Historically, models like LLaMA 2 allocated less than 0.21% of their training corpora to underrepresented languages, requiring Tamil characters to be represented as multiple UTF-8 bytes. This led to severe sequence inflation, where a single Tamil character required three to four times the token length of its English equivalent.  
The feasibility of monolingual adaptation has been validated by projects such as Tamil-LLaMA. Rather than training a model from scratch, developers can expand the vocabulary of an open-source base architecture (such as LLaMA or Gemma) and perform parameter-efficient continued pre-training.  
The technical pipeline for constructing a monolingual Tamil SLM comprises three main phases:

* **Vocabulary Resizing**: A specialized Tamil tokenizer is trained on a contemporary Tamil corpus using SentencePiece. These new tokens (typically 16,000 entries) are appended to the base model's embedding layers, expanding the vocabulary matrix while preserving the original English weights. This modification reduces the sequence length of tokenized Tamil text to 20%–25% of the original baseline.  
* **Continued Pre-Training (CPT)**: The model undergoes low-rank continued pre-training on a high-quality Tamil corpus (such as CulturaX or Wikipedia). This step adapts the model's inner representations to the morphosyntactic structures of the target language.  
* **Instruction Fine-Tuning**: The model is aligned using translated instruction sets, such as the Stanford Alpaca and OpenOrca datasets, to enable zero-shot task execution and instruction-following in native script.

| Model Configuration | Base Model | Vocabulary Expansion | Continued Pre-Training Data | Downstream Performance Outcome |
| :---- | :---- | :---- | :---- | :---- |
| **Tamil-LLaMA 7B** | LLaMA 2 | \+16,000 Tamil tokens | 12 GB (CulturaX subset) | 80.12% headlines classification accuracy vs. 50.5% for base LLaMA 2\. |
| **Tamil-LLaMA 13B** | LLaMA 2 | \+16,000 Tamil tokens | 12 GB (CulturaX subset) | Outperforms GPT-3.5-Turbo on Tamil creative writing and question answering. |
| **Tamil Gemma 2B** | Gemma 2B | None (uses native 256k vocabulary) | Full Tamil Wikipedia corpus | Top performance on open leaderboards for models under 3B parameters. |

## **Grammar-First Tokenization and Morphological Parsing Frameworks**

To capture the syntactic structure of agglutinative languages, tokenizers must incorporate grammatical rules directly into their segmentation pipelines. The primary model for this paradigm is the VerChol (வேர்ச்சசொல்) architecture, which utilizes a four-tier pipeline to ensure that every generated token represents a linguistically valid unit.  
`Raw Tamil Text ──> [ Tier 0: Whole-Word Lookup ] ──(Match)──> Emit 1 Token`  
                         `│`  
                      `(Miss)`  
                         `▼`  
      `[span_15](start_span)[span_15](end_span)       [ Tier 1: Morphological Decomposition ] ──(Match)──> Emit Morpheme Tokens`  
                         `│`  
                      `(Miss)`  
                         `▼`  
             `[ Tier 2: Syllable Segmentation ] ──(Match)──> Emit CV/CVC Syllables`  
                         `│`  
                      `(Miss)`  
                         `▼`  
             `[ Tier 3: Character Fallback ] ──(Match)──> Emit Unicode Graphemes`

In the first stage, known as Tier 0, the word is checked against a structured vocabulary file containing base linguistic units, morphologically generated combinations, and high-frequency whole words. If a match occurs, it is emitted as a single token.  
If Tier 0 misses, the pipeline falls back to Tier 1, which performs rule-based morphological decomposition into roots and suffixes. This process separates inflected forms into contiguous spans that reconstruct perfectly to the original text. For verbs, VerChol recognizes complex chains, decomposing auxiliary verbs, aspect, mood, and person-number-gender markers.  
A critical component of this morphological analysis is the execution of Sandhi rules. Sandhi refers to phonological changes that occur at the boundaries of joined morphemes, including:

* **Glide Insertion**: Inserting a semi-vowel (such as \-v- or \-y-) when a root ending in a vowel joins a suffix beginning with a vowel.  
* **Consonant Doubling (Germination)**: Doubling the final consonant of monosyllabic words with a Consonant-Vowel-Consonant (CVC) structure when a suffix is attached.  
* **Assimilation and Deletion**: Modifying or removing boundary characters based on morphotactic constraints.

Historically, rule-based systems suffered from failures when encountering out-of-vocabulary words. To resolve this, modern implementations pair rule-based engines with machine learning models trained to learn noun declensions and morphophonemic rules directly from corpus data.  
If morphological decomposition fails, the tokenizer falls back to Tier 2 (phonotactic syllable segmentation) and Tier 3 (character fallback). This progression ensures that words are segmented into phonologically valid consonant-vowel (CV) or consonant-vowel-consonant (CVC) syllables before defaulting to raw characters.  
These rule-based morphological pipelines are supported by a rich ecosystem of Tamil natural language processing libraries:

* **Open-Tamil**: An open-source Python library developed since the early 2010s. It includes numerical parsing algorithms that translate numbers to spoken Tamil words with O(n) complexity, spell-checking engines (solthiruthi), and Unicode converters.  
* **VaaniNLP and TamilNLP**: Specialized libraries designed to parse morphotactic constraints and execute grammatical rules.  
* **ThamizhiLIP**: A linguistic processing library providing morphological analysis and generation.  
* **Stanza**: Stanford University's natural language processing library, which supports Tamil dependency parsing and part-of-speech tagging.

Using these tools to build a grammar-first tokenizer yields significant efficiency gains. When evaluated on the full Tamil Wikipedia corpus (30.5 million word occurrences), the VerChol tokenizer achieved a fertility rate of 1.86 tokens per word. This represents a 35% reduction in token count compared to standard SentencePiece BPE, and a 47% reduction compared to production-grade Indic-optimized BPE tokenizers.

## **The Challenge of Romanized Code-Mixed Text (Tanglish)**

While native-script tokenizers optimize processing for formal text, real-world communication among the 80+ million Tamil speakers frequently utilizes Romanized code-mixed text, commonly referred to as Tanglish. Tanglish combines Tamil grammatical structures with English vocabulary, written entirely in the Latin script.  
Standard multilingual language models and language identification tools (langdetect) consistently fail when processing Tanglish. Because character-level n-gram models do not recognize the phonetics of Romanized Tamil, they often misclassify Tanglish as Tagalog, Somali, or English. This misclassification introduces a severe lexical gap, causing sentence embedding models to assign near-zero similarity scores to semantically identical sentences.  
To resolve this limitation, specialized models such as Morgan-Tanglish-v7 employ custom morphological filtering gates rather than standard language identifiers:

* **Length Filter (G1)**: Restricts inputs to 5–60 tokens to eliminate noise.  
* **Script Filter (G2)**: Rejects inputs containing more than 10% Tamil Unicode, ensuring the target text is Romanized.  
* **Lexicon Match (G3)**: Verifies the presence of high-frequency transliterated words using a validated reference lexicon.  
* **Pattern Analyzer (G4)**: Inspects strings for Tamil morphological patterns expressed in Latin script, such as dative suffixes (-ku), locative suffixes (-la), possessive markers (-oda), and auxiliary verb families (pannu verbs like *workpanren*).  
* **Deduplication (G5)**: Performs exact deduplication across sources to clean the corpus.

| Evaluation Dataset | Morgan-Tanglish-v7 (118M) | BAAI/bge-m3 (570M) | L3Cube-IndicSBERT | all-MiniLM-L6-v2 (22.7M) |
| :---- | :---- | :---- | :---- | :---- |
| **TanglishSTS Benchmark** | **0.8689** | 0.7583 | 0.7642 | 0.7510 |
| **Nuanced STS Benchmark** | **0.5451** | 0.1204 | 0.1514 | 0.2062 |
| **Domain-Specific Average** | **0.7446** | 0.6804 | 0.5729 | 0.6094 |

As shown in the table above, models trained on formal multilingual corpora struggle to capture the semantics of Romanized code-mixed text. Conversely, integrating morphological filtering gates allows compact models to outperform much larger architectures. This highlights the need for specialized routing systems that can distinguish between formal Tamil script, native English, and Romanized code-mixed Tamil.

## **Architectural Integration with Multilingual Models**

Integrating a specialized monolingual Tamil Small Language Model with a large multilingual model can be achieved through three main architectural paradigms. These approaches balance computational latency, deployment complexity, and task performance.

### **Paradigm 1: Dynamic Language Routing and Cascading**

In a cascading architecture, an upstream router acts as a lightweight decision engine. Rather than using an expensive LLM call for routing, the system uses in-memory feature extraction to identify the language and complexity of incoming queries.  
If the router detects native Tamil script or Tanglish patterns (via morphological filters), it directs the query to the monolingual Tamil SLM. Simple tasks, such as classification or information extraction, are resolved locally by the SLM.  
If the query is highly complex or requires cross-lingual reasoning, the router escalates it to the larger multilingual LLM. This dynamic cascade maintains response quality while reducing average operational costs by more than 50%.

### **Paradigm 2: Heterogeneous Speculative Decoding**

Speculative decoding accelerates inference by pairing a small, fast draft model with a large target model. The draft model proposes a sequence of candidate tokens, which the target model verifies in parallel in a single forward pass.  
Historically, this required both models to share an identical tokenizer. However, recent cross-vocabulary techniques allow models with mismatched tokenizers to be paired. This enables a monolingual Tamil SLM (using a VerChol tokenizer) to act as a draft model for a target LLM (using a generic BPE tokenizer).  
`[ Draft Model (VerChol Tokenizer) ] ──> Generates Morphemic Tokens`  
                                             `│`  
                                             `▼`  
                              `[ Token-Level Intersection ]`  
                                             `│`  
                                             `▼`  
                             `[ Cross-Vocabulary Mapper (TLI) ]`  
                                             `│`  
                                             `▼`  
                              `Maps to Target BPE Token IDs`  
                                             `│`  
                                             `▼`  
`[ Target LLM (BPE Tokenizer) ] ─────> Parallel Verification Step`

This cross-vocabulary mapping is executed using **Token-Level Intersection (TLI)** or **cross-tokenizer likelihood scoring**. The TLI framework identifies overlapping vocabulary regions using text normalization and constrains the draft model to propose tokens within this intersection.  
For arbitrary vocabularies, cross-tokenizer scoring utilizes the recursive structure of Byte-Pair Encoding to map draft tokens back to raw bytes, which are then grouped into target BPE representations. This allows the target model to verify the draft sequence in parallel, significantly reducing inference latency.

### **Paradigm 3: Mixture of Low-Rank Adaptations (MoLoRA)**

The MoLoRA framework integrates language-specific capabilities directly into the parameters of a frozen multilingual model. Rather than maintaining two separate networks, developers train specialized low-rank adapter modules (LoRA experts) for different languages.  
During inference, a gating network or a lightweight fusion MLP calculates routing weights based on the input query. When Tamil text is detected, the gating mechanism activates the Tamil LoRA expert.  
This architecture alleviates parameter competition in the low-rank space, which often degrades multilingual performance in standard LoRA models. It also allows new languages to be integrated incrementally by training a new adapter and updating the routing layers.

## **Advanced Inference Optimization and Dynamic Speculation**

To deploy these hybrid architectures in production, systems must optimize the drafting and verification steps of speculative decoding. Several advanced optimization techniques can be used to improve performance:

### **Offline n-gram Draft Lookups (DictSpec)**

Instead of running a neural network for draft generation, systems can construct a static n-gram lookup table offline from an unlabeled monolingual corpus. This mechanism requires no trainable parameters or GPU resources and adds less than 5 MB of memory overhead.  
The lookup engine searches backward through the prompt to find previous occurrences of the current token sequence and proposes the subsequent tokens. This approach is highly effective for non-Latin scripts where tokenizer fertility is high, yielding up to a 1.76x speedup when integrated into inference engines like vLLM.

### **Feature-Level Extrapolation (EAGLE-3)**

The EAGLE-3 framework speeds up speculative decoding by operating at the feature level. Instead of using a separate draft model, it builds a lightweight drafting network that extrapolates from the hidden states of the target model's output head. This design uses context-aware dynamic draft trees to propose multiple candidate paths, bypasses the bottleneck of sequential autoregressive generation, and maintains high token acceptance rates.

### **Multi-Token Prediction (MTP)**

Popularized by architectures like DeepSeek, Multi-Token Prediction integrates speculative generation directly into the primary model. The model is trained with multiple decoding heads, where each head predicts a different future token in parallel. The target model then verifies these predictions internally, removing the need to deploy and manage a separate draft network.

### **Adaptive Speculative Parameters**

Most speculative decoding systems use a fixed candidate length, which can be inefficient if the draft model's predictions diverge from the target model. Adaptive frameworks, such as SGLang and TurboSpec, resolve this by dynamically adjusting speculative parameters at runtime:

* **Draft-Token Entropy**: Monitors the uncertainty of the draft model's predictions and halts generation if entropy exceeds a defined threshold.  
* **Jensen-Shannon (JS) Distance**: Measures the divergence between the draft and target probability distributions, adjusting the candidate length to maximize the token acceptance rate.

## **Architectural Conclusions and Implementation Roadmap**

Developing a morphologically optimized monolingual Small Language Model for Tamil is highly feasible and offers significant advantages over general-purpose multilingual architectures. By incorporating grammar-first tokenizers like VerChol, developers can resolve the token inflation and boundary violations that degrade standard statistical tokenizers.  
For production deployments, the choice of integration architecture depends on system constraints and task requirements:

| Integration Strategy | Computational Overhead | Token Acceptance Rate | Primary Use Case |
| :---- | :---- | :---- | :---- |
| **Dynamic Routing (Cascaded SLM/LLM)** | Minimal (\<1 ms routing latency) | — | Cost-effective scaling of routine customer support and query classification. |
| **Heterogeneous Speculative Decoding** | Low (5 MB memory overhead for n-gram drafts) | High (enhanced by monolingual draft models) | Low-latency text generation on edge devices and local servers. |
| **MoLoRA with Dynamic Gating** | Moderate (requires loading active LoRA experts) | — | Unified multilingual systems requiring high translation accuracy. |

To build and deploy this system, organizations should follow a structured execution roadmap:

* **Tokenizer Initialization**: Combine a rule-based parsing library (such as Open-Tamil) with a grammar-first tokenizer (such as VerChol) to construct a Tamil vocabulary. This step establishes phonotactic syllable parsing and explicit morphophonemic sandhi rules, ensuring that root-suffix boundaries are preserved.  
* **Model Adaptation**: Expand the embedding layers of a compact open-source model (such as LLaMA 3.1 8B or Gemma 2B) and perform continued pre-training on a high-quality Tamil corpus.  
* **Routing and Serving Integration**: Deploy the adapted Small Language Model using vLLM, configured for cross-vocabulary speculative decoding. Implement an upstream rule-based script filter to identify native Tamil script or Romanized Tanglish, routing incoming queries to the specialized pipeline to minimize latency and operational costs.

#### **Works cited**

1\. Typologically-Informed Candidate Reranking for LLM-based Translation into Low-Resource Languages \- arXiv, https://arxiv.org/html/2602.01162v1 2\. Language-Specific Tokenizer Design \- Emergent Mind, https://www.emergentmind.com/topics/language-specific-tokenizer-design 3\. வேர்ச்சசொல் (VerChol) \- arXiv, https://arxiv.org/pdf/2603.05883 4\. Why Non-English Speakers Pay More for AI | by Craig Trim | Medium, https://medium.com/@craigtrim/why-non-english-speakers-pay-more-for-ai-eb6db7d5b67c 5\. MACHINE LEARNING OF PHONOLOGICALLY CONDITIONED NOUN DECLENSIONS FOR TAMIL MORPHOLOGICAL GENERATORS \- arXiv, https://arxiv.org/pdf/1402.3382 6\. MORPHOLOGICAL ANALYZER FOR CLASSICAL TAMIL TEXT: A RULE-BASED APPROACH, http://www.arpnjournals.org/jeas/research\_papers/rp\_2015/jeas\_1115\_2876.pdf 7\. VerChol \-- Grammar-First Tokenization for Agglutinative Languages \- ResearchGate, https://www.researchgate.net/publication/401691777\_VerChol\_--\_Grammar-First\_Tokenization\_for\_Agglutinative\_Languages 8\. \[2311.05845\] Tamil-Llama: A New Tamil Language Model Based on Llama 2 \- ar5iv \- arXiv, https://ar5iv.labs.arxiv.org/html/2311.05845 9\. abhinand5/tamil-llama: A New Tamil Large Language Model (LLM) Based on Llama 2 \- GitHub, https://github.com/abhinand5/tamil-llama 10\. Breaking Language Barriers: Introducing Tamil LLaMA v0.2 and Its Expansion to Telugu and Malayalam \- Abhinand, https://abhinand05.medium.com/breaking-language-barriers-introducing-tamil-llama-v0-2-and-its-expansion-to-telugu-and-malayalam-deb5d23e9264 11\. Tamil-Llama: A New Tamil Language Model Based on Llama 2 \- Semantic Scholar, https://www.semanticscholar.org/paper/Tamil-Llama%3A-A-New-Tamil-Language-Model-Based-on-2-Balachandran/61902976473384dc87e58a45d880de173c96c801 12\. Modern Tamil Word Formation Rules in NLP \- International Journal of Engineering Research & Technology, https://www.ijert.org/research/modern-tamil-word-formation-rules-in-nlp-IJERTCONV3IS33020.pdf 13\. INFITTOfficial/awesome-tamil: தமிழில் உள்ள பொதுவெளி தரவுகள், நிரல் திரட்டுகள், மற்றும் மென்பொருள்கள். \- GitHub, https://github.com/INFITTOfficial/awesome-tamil 14\. Tamil Text Processing with Open-Tamil – தமிழில் நிரல் எழுது, https://ezhillang.wordpress.com/2020/05/21/tamil-text-processing-with-open-tamil/ 15\. Generation and Parsing of Number to Words in Tamil, https://ezhillang.wordpress.com/wp-content/uploads/2020/06/generation-and-parsing-of-number-to-words-in-tamil\_jun15.pdf 16\. Tamil Internet 2017 25-27, Toronto, Canad CONFERENCE PROCEEDINGS \- INFITT, https://www.infitt.org/conference\_papers/tic2017\_papers.pdf 17\. Organized by Tamil University, Thanjavur, Tamilnadu, India Periyar Maniyammai Institute of Science and Technology, Thanjavur, Ta \- INFITT Page, https://uttamam.org/papers/tic2022.pdf 18\. Morgan-Tanglish-v7: Sentence Embeddings for Romanised Tamil-English Code-Mixed Text, https://www.researchgate.net/publication/407468354\_Morgan-Tanglish-v7\_Sentence\_Embeddings\_for\_Romanised\_Tamil-English\_Code-Mixed\_Text 19\. vishnu-n/Morgan-Tanglish-v7 \- Hugging Face, https://huggingface.co/vishnu-n/Morgan-Tanglish-v7 20\. Understanding the Limitations of Zero-Shot Large- Language Models on Hinglish and Tanglish Text \- IJFMR, https://www.ijfmr.com/papers/2026/3/76882.pdf 21\. LLM routing strategies for quality in AI applications \- n8n Blog, https://blog.n8n.io/llm-routing/ 22\. \[Feature\]: Universal Speculative Decoding for Heterogeneous Vocabularies (TLI / Token-Level Intersection) · Issue \#38173 \- GitHub, https://github.com/vllm-project/vllm/issues/38173 23\. MoLoRA: Boosting LLM-based End-to-end Speech Translation with Mixture of Low-rank Experts \- AAAI Publications, https://ojs.aaai.org/index.php/AAAI/article/view/40769/44730 24\. A Low-Latency Routing Pattern for Multiple Small Language Models \- DZone, https://dzone.com/articles/low-latency-llm-routing 25\. LLM vs SLM for AI Agents: Notch's Hybrid Playbook, https://www.notch.cx/post/llm-vs-slm-for-ai-agents-notchs-hybrid-playbook 26\. OrchestraLLM: Efficient Orchestration of Language Models for Dialogue State Tracking \- arXiv, https://arxiv.org/html/2311.09758v3 27\. Small Language Models vs Large Language Models Explained | SLM vs LLM (AI Comparison) | ResearchGate, https://www.researchgate.net/post/Small\_Language\_Models\_vs\_Large\_Language\_Models\_Explained\_SLM\_vs\_LLM\_AI\_Comparison 28\. An Introduction to Speculative Decoding for Reducing Latency in AI Inference, https://developer.nvidia.com/blog/an-introduction-to-speculative-decoding-for-reducing-latency-in-ai-inference/ 29\. Speculative Decoding in vLLM: Complete Guide to Faster LLM Inference | Jarvis Labs Blog, https://jarvislabs.ai/blog/speculative-decoding-vllm-faster-llm-inference 30\. All about Speculative Decoding \- Knowledge Articles \- SambaNova Developer Community, https://community.sambanova.ai/t/all-about-speculative-decoding/1172 31\. Cross-Tokenizer Likelihood Scoring Algorithms for Language Model Distillation, https://openreview.net/forum?id=hD69qj15Os\&noteId=hBQjMmSW9T 32\. LLM Adapters: Modular Fine-Tuning \- Emergent Mind, https://www.emergentmind.com/topics/large-language-model-adapters-llm-adapters 33\. Incremental Multilingual Text2Cypher with Adapter Combination \- arXiv, https://arxiv.org/html/2601.16097v2 34\. Adapter Fusion for Multilingual Text2Cypher with Linear and Learned Gating \- arXiv, https://arxiv.org/html/2601.16097v1 35\. MoE-Spec: Expert Budgeting for Efficient Speculative Decoding \- arXiv, https://arxiv.org/html/2602.16052v1 36\. Efficient LLM System with Speculative Decoding by Xiaoxuan Liu A dissertation submitted in partial satisfaction of the requireme \- EECS, https://www2.eecs.berkeley.edu/Pubs/TechRpts/2025/Archive/EECS-2025-224.pdf 37\. Speculative Decoding Across Languages \- arXiv, https://arxiv.org/pdf/2605.30580 38\. Dictionary-Based Speculative Decoding for Non-Latin-Script Languages \- ACL Anthology, https://aclanthology.org/2026.unlp-1.15.pdf 39\. Speculative decoding | LLM Inference Handbook \- BentoML, https://bentoml.com/llm/inference-optimization/speculative-decoding 40\. Dynamic Model Routing and Cascading for Efficient LLM Inference: A Survey \- arXiv, https://arxiv.org/html/2603.04445v2