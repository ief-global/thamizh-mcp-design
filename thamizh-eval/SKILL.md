---
name: thamizh-eval
description: "Measure whether the Thamizh MCP server actually improves LLM Tamil competence — build ILAKKANAM-style Tamil linguistics benchmarks and run A/B 'morphological lift' evaluations (bare LLM vs LLM + thamizh-mcp). Use whenever the user wants to evaluate or benchmark LLM performance on Tamil, measure morphological lift, build/extend/verify the Tamil eval fixture set, run or reference the ILAKKANAM benchmark, compare models on Tamil grammar questions, or check whether a thamizh-mcp change moved downstream answer quality. Triggers: 'run the Tamil eval', 'measure the lift', 'benchmark Claude on Tamil', 'ILAKKANAM', 'did the MCP help'. Do NOT trigger for the server's own unit/regression tests (thamizh-mcp-builder Phase 4 owns those), general Tamil learning or grammar questions, non-Tamil benchmarks, or generic MCP-server testing."
license: Internal project skill for the THAMIZH MCP project. (v1 — created 2026-07-10.)
---

# Thamizh Eval — morphological lift & Tamil benchmarks

## What this skill is for

The Thamizh MCP server exists to make LLM answers about Tamil grounded and authentic. This skill proves
(or disproves) that claim with numbers. Its product is the **morphological lift** measurement — the v1
north-star metric (decision D-005):

```
lift = SP(model + thamizh-mcp) − SP(model alone)      SP = score obtained / score attainable × 100
```

computed on Tamil-linguistics questions, reported **per linguistic category and grade band**, never as a
single blended number.

Two evaluation layers exist in this project. Keep them separate:

| Layer | Question it answers | Owner |
|---|---|---|
| Server regression evals | "Does each tool return correct, grounded, honest output?" | `thamizh-mcp-builder` Phase 4 (`evals.json`, fixture words மரம், மரத்தில், புத்தகம்…) |
| Product lift evals (this skill) | "Does an LLM with the server answer real Tamil questions better than without?" | this skill |

## Research grounding (why this design)

ILAKKANAM (arXiv 2511.12387, Univ. of Jaffna, incl. Sarveswaran — the ThamizhiMorph author) is the first
Tamil linguistic benchmark: 820 questions hand-curated from Sri Lankan school Tamil exams, Grades 1–13,
annotated by linguists into L1 phonetics, L2 phonology, L3 morphology, L4 syntax, L5 semantics, F fact.
Published results (zero-shot, 2025): Gemini 2.5 79.6 · Grok 4 78.2 · GPT-5 75.9 · Claude Sonnet 4.5 71.1 ·
Llama 4 60.7 · DeepSeek-V3 58.0 · Qwen 2.5-72B 37.9. Two findings shape this skill: accuracy declines as
grade/complexity rises, and category-identification ability does not correlate with accuracy — models ride
exposure, not understanding. So the lift experiment concentrates fixtures where grounding should matter
most: **L3 morphology and Grades 6–13**, with L1/L2/L4/L5 present as controls.

## Step 1 — Get a question set

1. **Check whether ILAKKANAM itself has been released** (search: `ILAKKANAM dataset huggingface github
   site:arxiv.org 2511.12387`; authors' pages at Univ. of Jaffna). As of 2026-07-10 it was NOT public.
   If released: use it under its license, never redistribute it, and keep our fixture set as the
   development set (ILAKKANAM becomes the held-out test).
2. **Otherwise build an ILAKKANAM-style fixture set** per `references/benchmark-design.md` — same fields
   (source, question type QT01–QT09, category L1–L5/F, question, answer, alternatives, score, grade),
   sourced from public school exam papers and textbook exercises, answers hand-verified against the
   anchors (ThamizhiMorph, lexicon, Tholkappiyam rule table) before locking. Start at ~50–100 questions;
   grow via the eval-driven-hardening loop (every observed failure becomes a fixture).

## Step 2 — Run the A/B protocol

- **Same model, same prompt, zero-shot, both arms.** Control = no MCP access; Test = thamizh-mcp attached.
- **Isolation:** run the control arm where the server is genuinely unreachable, and run everything outside
  the project folder so no skill/reference files leak into context (same rule as the builder's eval note).
- **Repetition:** 3 runs per question per arm (ILAKKANAM's protocol); score each, keep the mean.
- **Scoring:** normalized exact-match first; then manually review every "incorrect" for linguistically
  acceptable alternatives (Tamil often has several valid surface answers); verified alternatives get added
  to the fixture's `alternatives` list permanently. Never let the model-under-test grade itself.
- **Also record per question (test arm):** did the model actually call thamizh-mcp tools; which tools;
  latency; token counts both arms (the token-explosion delta is itself reportable evidence).

## Step 3 — Report

Report SP per arm and lift, split by category (L1–L5, F) and grade band (1–5, 6–11, 12–13); overall last.
Report **negative or null lift honestly** — a category where the MCP doesn't help is a finding that routes
work (usually to tool descriptions or a missing source), not a number to bury. Include: model + version,
date, fixture-set version/hash, N runs, tool-call rate. Template in `references/benchmark-design.md` §5.

## Step 4 — Claude-first runner

`assets/run_ab.py` is the harness sketch: fixtures in, two arms via `claude -p` (test arm adds
`--mcp-config` pointing at thamizh-mcp), results JSONL out, SP/lift computed. Storage is model-agnostic —
adding GPT/Gemini/open-source runners later means adding a `runner` function, nothing else (D-005 chose
Claude-first execution). Run it on a network-open box (minnaham / local Claude Code), not the Cowork
sandbox (control-arm isolation + `claude` CLI auth live there).

## Honesty & hygiene rules

- **Contamination guard:** every fixture word/question gets flagged in the knowledge store
  (`eval_fixture=1`) so `thamizh-data-curation` excludes it from any published dataset; keep a small
  held-out subset that is never published anywhere.
- The enrichment loop may legitimately *learn* fixture words during the test arm — that's the product
  working — but wipe or snapshot-restore the knowledge store between benchmark runs so run N+1 doesn't
  inherit run N's cache warmth unless cache-warm behaviour is what you're measuring (say which).
- Pin everything: model version, server git SHA, FST pins, fixture-set hash. A lift number without pins
  is not reproducible and doesn't count.

## Reference files

- `references/benchmark-design.md` — fixture schema, category definitions, sourcing guidance, target
  distribution, ILAKKANAM baseline table, report template.
- `assets/fixture-template.json` — three worked fixture examples in the exact storage shape.
- `assets/run_ab.py` — the A/B harness sketch (Claude-first).
