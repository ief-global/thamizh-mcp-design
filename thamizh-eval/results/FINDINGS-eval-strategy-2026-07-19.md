# Eval strategy — findings & recommended pivot (2026-07-19)

After Set 1 (Opus, 10 L3 fixtures) + a server-capability probe, three findings reshape how we should
measure morphological lift. **For the design side (Fable) to weigh in.**

## Finding 1 — On frontier Opus, the lift headroom is tiny
Bare Opus 4.8 scores **~97%** on basic Tamil morphology (roots, cases, tense, word class, உருபு) and
invokes the server **~3%** of the time. There is almost no room for grounding to *raise* correctness,
and the model rarely reaches for the tool. Measuring "spontaneous lift on Opus" will keep reading ~0 —
**not because the server is weak, but because the target is already near-ceiling.**

## Finding 2 — Real headroom is on WEAKER models (where the program's value lives)
ILAKKANAM baselines: Sonnet 71%, Llama 4 61%, DeepSeek 58%, Qwen-72B 38% — vs Opus 79.6%. The server's
correctness lift should be **large on the models that actually need it** (Sonnet, open-source, and the
future Tamil SLM), small on Opus. That matches the program thesis (raise Tamil for the broad ecosystem,
not the one frontier model). **But** weaker models don't invoke tools spontaneously (Sonnet: 0%). The
**grounded-prompt arm** (now built: `--grounded`) closes that — it invites tool use, so we measure
achievable lift *when the tool is consulted*.

**→ Recommended pivot:** measure **control (weak model, no tools) vs grounded (weak model, tools + "use
them" prompt)** on **Sonnet** first. It is ~5× cheaper than Opus, has genuine headroom, and the grounded
arm removes the invocation confound. This is cheap enough to run the full 28 fixtures within budget.
Keep an Opus spot-check for the record, but Opus should not be the primary lift target.

## Finding 3 — The server itself has FST coverage gaps (a CODE item)
The probe found common verbs returning **`unknown`**: `கொடுத்தான்`, `விற்றான்`, `கற்றான்` (irregular
க்/ற் stems). The primary FSTs (guessers excluded by policy) don't cover them, so `analyze_word` gives an
honest gap where a user expects an answer. This caps the achievable lift (the server can't help where it
also fails) and is a real product limitation. **Route to thamizh-mcp-builder:** investigate verb-class
coverage / whether a vetted subset of the guesser FSTs (or an open-tamil stemmer fallback) should fill
these, without reintroducing unsourced guesses. Also: causatives (`செய்வித்தான்`) decode without the
பிறவினை இடைநிலை (வி) — the formation decoder misses the causative marker.

## Net
The morphological-lift story is real but **model-dependent**: big on weak models + grounded, ~0 on
frontier Opus. Next cheap step = Sonnet control-vs-grounded on the existing fixtures. Harder Opus-hard
fixtures are low-value (Opus is near-ceiling; where it fails, the FST often fails too — Finding 3).
