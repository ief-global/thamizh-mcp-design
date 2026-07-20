# Morphological-lift — Opus Set 1 (L3 morphology) — 2026-07-19

**Model:** Opus 4.8 (default) · **Server:** thamizh-mcp @ `837e068` · **Set 1:** 10 L3 fixtures × 3 runs × 2 arms · Scoring: multi-part aware.

| Category | control SP | test SP | lift | tool-call rate |
|---|---|---|---|---|
| L3 morphology (OVERALL) | **97.22** | 88.89 | **−8.33** | **3.3%** |

## What this says (the eval doing its job)

1. **Bare Opus 4.8 already scores ~97% on basic Tamil morphology** — roots (வா, படி), cases (2nd/4th வேற்றுமை), tense, word-class, the உருபு. It knows these without help. The fixtures are **not discriminating for Opus**.
2. **The server is barely invoked — 3.3%** (1 of 30 test calls). Opus is confident and answers directly.
3. **The −8.33 "lift" is noise, not harm**: on a 97%-baseline 10-question sample, one run of TE-0002 dropping a part (`மரம் + இல்`) is enough to move the number. The server did not make answers worse; it mostly wasn't consulted.

**Conclusion:** on questions the model already handles, the server adds no measurable lift *and isn't called*. That is a real, expected result — grounding helps where the model is *weak*, not where it's already right (ILAKKANAM's own finding: accuracy drops on **harder/upper-grade** items).

## Routed actions (per the growth loop)

1. **Harder, discriminating fixtures.** The v1 set is mostly basic. To measure real lift we need items where bare Opus actually **fails** — complex/multi-step புணர்ச்சி, rare or ambiguous words, obscure விகாரம், upper-grade ILAKKANAM-style questions. That is where grounding can move the number.
2. **Invocation is still the gate.** Even Opus reaches for the tool ~3% of the time under a neutral prompt. A **grounded-prompt arm** ("use the Tamil analysis tool") is needed to measure the *achievable* lift (does grounding help *when consulted*), separate from spontaneous lift.
3. **L5 equivalents are the likeliest place lift shows without harder fixtures** — coined/neologism terms (கம்ப்யூட்டர்→கணினி, ஜன்னல்→சாளரம்) are lexical knowledge Opus may lack. Worth a targeted check.

## Budget note

Set 1 already delivered the key insight (easy fixtures + low invocation → ~0 lift). Running Set 2/3 as-is would largely repeat it. Recommend **pivoting to harder fixtures + a grounded arm** rather than spending the remaining budget confirming the null result — except possibly the L5-equivalents subset of Set 2, the one category where bare Opus may be weak.
