# Benchmark design — ILAKKANAM-style fixtures for morphological lift

## 1. Fixture schema (mirror of the paper's design fields)

One JSON object per question, stored in `fixtures/*.jsonl`:

```json
{
  "id": "TE-0001",
  "source": "public exam paper / textbook / self-built — cite precisely",
  "grade": 8,
  "question_type": "QT07",
  "category": "L3",
  "question": "…Tamil question text…",
  "answer": "…ground truth…",
  "alternatives": ["…linguist-verified acceptable variants…"],
  "score": 2,
  "verified_against": ["ThamizhiMorph", "Tholkappiyam rule table"],
  "verified_date": "2026-07-10",
  "held_out": false
}
```

Question types (from the paper): QT01 fill-in-the-blanks · QT02 answer from given letters/words ·
QT03 order words/letters · QT04 Q&A · QT05 sentence completion · QT06 rewrite with punctuation ·
QT07 MCQ · QT08 Q&A on a paragraph · QT09 true/false. Prefer QT07/QT09/QT01 early — cheapest to
score automatically.

Categories: L1 phonetics · L2 phonology · L3 morphology · L4 syntax · L5 semantics · F fact.

## 2. Target distribution (v1, ~50–100 questions)

Weight where the server should produce lift, keep controls elsewhere:

| Category | Share | Note |
|---|---|---|
| L3 morphology | ~40% | பகுபத உறுப்பு splits, sandhi, case (வேற்றுமை), lemma/root, word-class |
| L5 semantics | ~15% | word meaning, loanword equivalents (கம்ப்யூட்டர்→கணினி style) |
| L2 phonology | ~15% | புணர்ச்சி rules stated as questions |
| L4 syntax | ~10% | control — server is word-level v1; expect little lift; that's fine |
| L1 phonetics | ~10% | control |
| F fact | ~10% | control — lift here would suggest leakage, investigate |

Grade bands: ~25% Grades 1–5, ~50% Grades 6–11, ~25% Grades 12–13 (the paper shows the drop-off is
in the upper bands — that's where the measurement is most informative).

## 3. Sourcing & verification

- Public Sri Lankan school Tamil papers (e.g. noolaham.school archives), Tamil Nadu state-board
  textbook exercises, teacher-published question banks. Record the exact source per fixture; respect
  each source's terms (fixtures quote short exam questions — keep sets private if terms are unclear;
  publishing the fixture set is NOT required for the lift experiment).
- Every `answer` is hand-verified against an anchor before locking: morphology answers against
  ThamizhiMorph output + the Tholkappiyam/Nannūl rule table; meanings against the lexicon; equivalents
  against attested கலைச்சொல் sources. A fixture that can't be anchor-verified doesn't go in.
- Seed reuse: the blueprint §9 words (மரம் · மரத்தில் · புத்தகம் · கம்ப்யூட்டர் · ஜன்னல் · no-equivalent loan ·
  disputed-origin word) each generate 2–4 questions across categories — but mark them `held_out: false`
  and NEVER publish them in datasets (they're already flagged eval words in the store).

## 4. ILAKKANAM published baselines (context, zero-shot, 2025)

Gemini 2.5 79.55 · Grok 4 78.15 · GPT-5 75.94 · Claude Sonnet 4.5 71.09 · Llama 4 60.67 ·
DeepSeek-V3 58.04 · Qwen 2.5-72B 37.93 (SP /820). Use these only as *context* — our fixture set is
not ILAKKANAM, so never present our SP as comparable to theirs; only our own control-vs-test delta
is a claim we can make.

## 5. Report template

```
# Morphological lift report — <date>
Model: <name+version> · Server: <git SHA> · FST pins: <data/PINS.md ref> · Fixtures: <version/hash, N>
Runs per question per arm: 3 · Store state: <fresh|snapshot-id>

| Category | N | SP control | SP test | Lift | Tool-call rate |
| L3 … |
| Grade band | … |

Overall: … (last, least important)
Notable failures (both arms): …
Negative/null-lift categories and routed action: …
Token usage: control median X tok/question vs test Y (+MCP overhead Z)
```

## 6. Growth loop

Every real-world failure observed in use → becomes a fixture → re-run → fix routes to tool
descriptions / sources / rule table (per `IMPROVEMENT-LOOP.md`: fix the reference, not the one answer).
