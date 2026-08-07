# Research grounding — the two anchor papers and the architectural argument

Digest for the builder. Read the papers at source — Jeyarajalingam, Velayuthan, Karunakaran, Rasan & Sarveswaran (2025), *From Phonemes to Meaning: Evaluating Large Language Models on Tamil* (ILAKKANAM benchmark, University of Jaffna), [arXiv:2511.12387](https://arxiv.org/abs/2511.12387); ThamizhiMorph:
Sarveswaran, Dias & Butt (2021), *Machine Translation* 35:37–70. Added 2026-07-10 (v6).

> A verbatim copy of the ILAKKANAM paper was previously committed here as
> `From_Phonemes_to_Meaning.md`. It was removed 2026-08-07: arXiv's default licence does not
> grant redistribution, and this repo is public. Cite and link — do not re-add the text.

## 1. ThamizhiMorph (Sarveswaran, Dias & Butt 2021, Machine Translation 35:37–70)

What we wrap (D-001) and why it's trustworthy:

- **Design:** morphological analyser *cum generator* as a foma FST; a high-level meta-language
  compiles Tamil inflectional morphology from paradigms — verbal paradigm tables + nominal paradigms
  (incl. 38 pronoun classes), following Lehmann (1993) and traditional grammars. Handles sandhi
  (morphophonological joining) in both directions. Generation direction matters to us twice: form
  generation (later tool) and **round-trip validation** of segmentations (data-curation skill).
- **Evaluation (612-word school-textbook corpus vs IIIT shallow parser):** analysis found 93.3%
  (IIIT 95.6), but among successful analyses: right analysis 100% (IIIT 96.2), right lemma 97.9%
  (IIIT 94.4). Residual failures are mostly **OOV lexicon gaps** — easily fixable by adding stems.
- **Implications for the server:** (a) when the FST fails, the correct move is the enrichment loop /
  honest gap, never a guess — the guesser FSTs stay excluded by policy (blueprint Phase 1);
  (b) OOV failures are *addable* — log them; a periodically reviewed OOV list is legitimate,
  bounded lexicon maintenance (stems only — not the banned hand-maintained word list, which was
  about inflected forms); (c) the paper itself notes UD's feature inventory can't express rationality,
  euphonic increments, or sandhi effects — our schema keeps them (they're Tholkappiyam categories).
- **2021 context:** "There are currently no benchmark data sets available for Tamil." ILAKKANAM (below)
  is the field answering that, four years later — and our eval strategy rides on it.

## 2. ILAKKANAM / From Phonemes to Meaning (arXiv 2511.12387; Univ. of Jaffna, incl. Sarveswaran)

First Tamil-specific linguistic benchmark: **820 questions** hand-curated from Sri Lankan school
Tamil exam papers, Grades 1–13, linguist-annotated into **L1 phonetics · L2 phonology · L3 morphology ·
L4 syntax · L5 semantics · F fact**; nine question types (QT01–QT09); scoring preserves per-question
exam weights; misses manually reviewed for acceptable alternatives.

- **Results (zero-shot, 2025):** Gemini 2.5 **79.6** · Grok 4 78.2 · GPT-5 75.9 · Claude Sonnet 4.5
  **71.1** · Llama 4 60.7 · DeepSeek-V3 58.0 · Qwen 2.5-72B 37.9.
- **Finding 1 — complexity cliff:** all models do well on lower grades, decline as linguistic
  complexity rises. The gap is worst exactly where this server grounds: morphology and upper-grade
  material.
- **Finding 2 — exposure, not understanding:** overall accuracy does not correlate with the ability
  to identify a question's linguistic category → models pattern-match from exposure. Grounding via
  tools is the architectural counter.
- **Finding 3 — open-source lag:** 20–40 points behind frontier models; the MCP layer plausibly helps
  *them* most (relevant to the long-term SLM track).
- **Dataset availability:** NOT public as of 2026-07-10 — re-check before eval work; the
  `thamizh-eval` skill owns the check-else-build-fixtures procedure.

## 3. The de-agglutination argument (tokenization analysis doc)

Why an MCP layer beats retraining (from `tamil_llm_tokenization_analysis_gemini.md`): BPE tokenizers
trained on English shatter agglutinated Tamil words into meaningless fragments — **token explosion**.
Consequences: context windows exhaust ~3–5× faster; long fragmented sequences degrade reasoning; RAG
embeddings of fragments miss the semantic root, wrecking retrieval. The fix is architectural, not
data-scale: a **de-agglutination layer** (this server) hands the LLM clean roots + explicit grammar
rules at query time. Four-phase pipeline: (1) this MCP server → (2) RAG over de-agglutinated roots →
(3) synthesis integration → (4) transaction logs become gold training data. Phases 2–4 are owned by
the roadmap (`TAMIL-HIGH-RESOURCE-ROADMAP.md`) and sibling skills, not this one.

## 4. What this changes in the build (checklist)

- Tool descriptions should say the server *is* the de-agglutination layer — it earns tool calls on any
  Tamil word task, not just explicit grammar questions.
- Log every transaction (store already provenance-tags claims) — data is a first-class output.
- Keep an OOV-miss log surfaced via a small report path (feeds bounded stem additions + enrichment).
- North-star metric is morphological lift per category (D-005) — build choices that plausibly move L3
  lift outrank cosmetic ones.
