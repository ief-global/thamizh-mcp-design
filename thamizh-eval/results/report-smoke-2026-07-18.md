# Morphological-lift report — SMOKE run — 2026-07-18

> **Smoke run, not the official measurement.** 6 questions, 1 run/arm, to validate the pipeline and
> get a directional signal. The full run is 3 runs/arm over the whole `fixtures/v1.jsonl` (28 Q).

**Model:** Claude Code default (Opus, via `claude -p`) · **Server:** `thamizh-mcp` @ `837e068`
· **FST pins:** `data/PINS.md` @ adbacced · **Fixtures:** `v1.jsonl` subset (TE-0001/0002/0009/0013/0021/0026)
· **Runs/arm:** 1 · **Store:** fresh eval-store.

| Category | control SP | test SP | lift |
|---|---|---|---|
| OVERALL | 50.0 | 37.5 | −12.5* |
| L3 morphology | 40.0 | 20.0 | −20.0* |
| L5 semantics | 0.0 | 0.0 | 0 |
| L1 phonetics | 100.0 | 100.0 | 0 |
| F fact | 100.0 | 100.0 | 0 |

**test-arm tool-call rate: 0.0%** · median tokens/q: control 16 vs test 56.

\* Not a real negative lift — a 6-question / 1-run sample is within noise, and TE-0001's test answer
("இல் (ஏழாம் வேற்றுமை உருபு)") is *correct* but auto-scored MISS on extra text (scoring artifact).

## The finding (this is the headline)

**The model does not spontaneously call the thamizh-mcp tools under a neutral prompt — even when they
are attached (0/6).** So the test arm ≈ the control arm, and both get the hard items wrong:
- TE-0002 (பகுபத உறுப்பு split): control → `மரம் + இல் …` (drops சாரியை); test → `மரம் + த் + இல்`
  (`த்` not `அத்து`). Both wrong.
- TE-0013 (ஜன்னல் → தனித்தமிழ்): control → `வாதில்`, test → `வளி மறை` — both hallucinated.

**The server is NOT the problem.** A direct wiring probe (explicitly instructing tool use) returned
`num_turns: 3` and the **correct** answer: *"பகுதி மரம் + சாரியை அத்து + விகுதி இல் (திரிதல் ம்→த்)"*.
The bottleneck is **tool invocation, not tool quality** — the model is overconfident on Tamil
morphology and answers directly (wrongly) instead of reaching for the grounding tool.

## Routed actions (per the growth loop — fix the reference, not the one answer)

1. **Measure two lifts, not one.** Keep the neutral-prompt *spontaneous lift* (faithful to ILAKKANAM
   zero-shot; today ≈ 0 at 0% tool-call rate) AND add a *grounded-prompt* arm ("if a Tamil
   word-analysis tool is available, use it") to measure the **achievable ceiling** when the tool IS
   called. The gap between them = the **invocation gap**, which is the real thing to close.
2. **Lift the invocation rate (code):** make the MCP tool descriptions more compelling / clearly the
   authoritative path for Tamil word-grammar, so a model reaches for them unprompted. This is the top
   eval-routed code item.
3. **Harden scoring:** exact-match is too strict for short Tamil answers with parenthetical gloss
   (TE-0001 false negative). Use contains-match on the normalized gold + keep the manual-review pass.
4. **Token note:** attaching the tools cost +40 median tokens/q even unused — real but modest; the
   token-explosion win is on the *input* side (de-agglutination), measured separately.

## Pipeline status

✅ End-to-end validated: fixtures → both arms via `claude -p` → auto-score → per-category SP/lift +
tool-call rate + tokens. Ready for the full 3-run measurement (and the grounded-arm addition).
