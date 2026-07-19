> **SUPERSEDED 2026-07-18 by `DESIGN.md` §6** (first objectives revision). Kept for history; do not
> update the tracks here — DESIGN.md is the living program map.

# Tamil → High-Resource: Program Roadmap

> Living doc. Created 2026-07-10. The Thamizh-MCP blueprint is the *server* spec; this is the *program*
> map — the building blocks that move Tamil from low-resource to a first-class language in the LLM
> ecosystem, and the order to build them. Blueprint §12 points here. Decisions: D-004/D-005/D-006.

## The goal and the measured gap

Goal: a native Tamil speaker should get the same grounded, fluent, efficient AI experience an English
speaker gets. The gap is now measurable, not anecdotal:

- **Linguistic competence gap (ILAKKANAM, arXiv 2511.12387):** on 820 school-exam Tamil linguistics
  questions (Grades 1–13), the best frontier model (Gemini 2.5) scores 79.6%; Claude Sonnet 4.5 scores
  71.1%; open-source models fall to 37.9–60.7%. All models decline sharply as grade/linguistic complexity
  rises, and category-identification ability doesn't correlate with accuracy — evidence that performance
  is driven by exposure, not understanding. Morphology (L3) and higher grades are the weak spots.
- **Tokenization gap ("token explosion"):** BPE tokenizers fragment agglutinated Tamil words into
  meaningless pieces; Tamil fills context windows ~3–5× faster than English, degrades long-sequence
  reasoning, and misaligns RAG embeddings (fragmented tokens → vectors that miss the semantic root).
- **Tooling gap:** ThamizhiMorph (2021) noted there were *no* Tamil benchmark datasets at all;
  ILAKKANAM (2025) is the first. The resource base is thin but real: ThamizhiMorph FST, open-tamil,
  Thamizhi suite, community lexicons.

## Strategy (why this shape)

Retraining base models is computationally prohibitive and not ours to do. The highest-leverage path is
**architectural**: put a rule-grounded de-agglutination + grounding layer (Thamizh MCP) between users
and any LLM now; **measure** the lift it produces; **accumulate** gold data as a by-product of use; and
only then — with corpus, benchmark, and community in hand — attempt native Tamil models. Each phase's
deliverable is immediately usable AND a prerequisite asset for the next.

## NEAR TERM (now – ~3 months) — ship the grounding layer, prove the lift

Immediately buildable; skills exist for all of it.

1. **Finish Thamizh MCP v1** (blueprint Phases 1-tail–4): kalaichol/equivalents adapter, origin
   classifier, remaining tools, formation decoder; Madras Lexicon + TVA கலைச்சொல் pinned snapshots
   (network-open session). → `thamizh-mcp-builder` skill (v6).
2. **Transaction logging on by default**: every analyze_word call logged with provenance — this is the
   future training corpus accumulating for free. → `thamizh-data-curation` skill.
3. **Baseline + morphological lift**: build the ILAKKANAM-style fixture set, run bare-LLM vs LLM+MCP
   A/B, publish the lift numbers per linguistic category. This is the v1 north-star metric (D-005).
   → `thamizh-eval` skill.
4. **License audit, then release rungs 0–1**: uvx-from-git → PyPI + Docker (GHCR); list on MCP
   registries + tamil-nlp-catalog. Native users with Claude/Cursor can start using it.
   → `thamizh-release` skill.

## MEDIUM TERM (~3–12 months) — reach non-technical users, publish data

5. **Hosted reference instance**: Cloud Run + Cloudflare edge per `thamizh-mcp-hosting-plan.md`
   (IEF nonprofit credits); REST head (FastAPI) beside the MCP head on the same engine.
6. **Public web tool** at ief-global.org — first channel that reaches ordinary Tamil speakers who will
   never install an MCP client.
7. **First HF dataset releases**: morphological-segmentation pairs, loanword→equivalent pairs, origin
   labels — exported from the knowledge store via `thamizh-data-curation` (license-gated).
8. **RAG optimization**: embed de-agglutinated roots (multilingual-E5-class embedders) instead of raw
   agglutinated text; measure retrieval lift the same A/B way.
9. **Phrase/sentence support**: ThamizhiPOSt/LIP contextual disambiguation (blueprint's declared v2).
10. **Instruction-tuning dataset**: template-generated Q/A records from verified analyses (no LLM-invented
    content), building toward fine-tuning.

## LONG TERM (12+ months) — native Tamil models. Marked, NOT solutioned now.

Deliberately not being worked: heavy prerequisites (corpus scale, compute budget, funding) that the near
and medium term create. Revisit when the gold corpus is ≥ ~100k verified records and eval infra is routine.

- **Tamil SLM**: grammar-first tokenizer (VerChol-style, FST-informed segmentation — our segmentation
  data is exactly its training input), vocab expansion + continued pretraining of a compact open model
  (Gemma/Llama-class), instruction-tuning on our curated data.
- **Hybrid serving**: SLM/LLM routing, speculative decoding with a Tamil draft model, MoLoRA adapters
  (see `Tamil-Small-Language-Models-by-Gemini.md` for the architecture survey).
- **Tanglish / code-mix support**; **mobile apps**; **offline on-device analyzer**.

## Skill map (who drives what)

| Track | Skill | Status |
|---|---|---|
| Build/extend the server | `thamizh-mcp-builder` v6 | updated 2026-07-10 |
| Benchmarks + morphological lift | `thamizh-eval` | new 2026-07-10 |
| Gold data curation + HF publishing | `thamizh-data-curation` | new 2026-07-10 |
| Packaging, hosting, registries | `thamizh-release` | new 2026-07-10 |
| SLM training | (none — long-term; do not create yet) | — |

## Sources

- From Phonemes to Meaning: Evaluating LLMs on Tamil (ILAKKANAM), arXiv:2511.12387 — extraction in
  `From_Phonemes_to_Meaning.md`.
- Sarveswaran, Dias & Butt (2021), ThamizhiMorph, Machine Translation 35:37–70.
- `tamil_llm_tokenization_analysis_gemini.md` (de-agglutination/MCP architecture argument).
- `Tamil-Small-Language-Models-by-Gemini.md` (SLM feasibility + serving architectures).
- `distribution-roadmap.md`, `thamizh-mcp-hosting-plan.md` (living channel/hosting docs).
