# Thamizh MCP — presentation source (for Claude Design / deck generation)

> **Purpose:** feed this into Claude Design to generate a deck for **Tamil scholars and enthusiasts**.
> Every number, Tamil form, and quoted output below is **verified against the live build**
> (`thamizh-mcp` @ 2026-07-20, 9 tools, 104 tests). Do not add claims that aren't here — the whole
> credibility of this project with scholars rests on not overclaiming. Audience is Tamil-literate and
> grammar-literate; they will fact-check the Tamil.

---

## Slide 1 — Title

**தமிழ் MCP · Thamizh MCP**
*Grounding AI in authentic Tamil grammar*
Subtitle: An open-source grammar engine that lets any AI answer Tamil word questions from
Tholkappiyam and Nannūl — with citations, and with the honesty to say "I don't know."

Speaker note: One line to set the frame — "This is not a chatbot. It's the grammar layer underneath one."

---

## Slide 2 — The problem, shown not told

**AI speaks Tamil fluently. It gets Tamil grammar wrong — confidently.**

Recorded in our own tests, asked in Tamil, no tool attached:

| Question | AI's unaided answer | Correct |
|---|---|---|
| Split மரத்தில் into பகுபத உறுப்பு | மரம் + **த்து** + இல் | மரம் + **அத்து** + இல் |
| Pure-Tamil word for ஜன்னல்? | **"வளி மறை"**, **"வாதில்"** | **சாளரம்** |

Speaker note: The second row is the killer — those are **invented words**. Not a wrong answer from a
list of real options; fabricated Tamil, delivered fluently. That is the failure mode this project exists
to remove. (Both were real outputs recorded in our A/B runs.)

---

## Slide 3 — Why this happens (the evidence)

- **ILAKKANAM benchmark** (arXiv 2511.12387, Univ. of Jaffna — the first Tamil linguistics benchmark,
  820 school-exam questions, Grades 1–13): best frontier model **79.6%**; Claude Sonnet 4.5 **71.1%**;
  open-source models **37.9–60.7%**.
- Accuracy **falls as grade and complexity rise** — and the ability to *name* a category doesn't predict
  getting it *right*. The paper's conclusion: models ride **exposure, not understanding**.
- Tamil is agglutinative, so AI tokenizers shred words into meaningless fragments — Tamil burns roughly
  **3–5× more context** than English for the same content.

Speaker note: Cite the paper by name; this audience respects sources. Our tool doesn't fix the model —
it gives the model a place to look things up.

---

## Slide 4 — What we built

**A Tamil grammar engine that an AI can call.** Three layers:

1. **Analyzer** — takes a word apart: root, formation (பகுபத உறுப்பு), sandhi (புணர்ச்சி), case
   (வேற்றுமை), word class, tense, origin, meaning, pure-Tamil equivalent.
2. **Citations** — every claim carries its source, authority (Tholkappiyam / Nannūl), and date.
3. **Honest gaps** — when no source can ground an answer, it returns a *gap*. It never fills the
   silence with a guess.

Speaker note: Layer 3 is the product. Anyone can build layer 1.

---

## Slide 5 — Live demo (the heart of the talk)

**Run these live. All output verified 2026-07-20.**

**A. Formation — மரத்தில்**
```
பகுதி மரம் + சாரியை அத்து + விகுதி இல்
புணர்ச்சி: திரிதல் — மரம் → மரத் (ம் → த் before the சாரியை)
சொல் வகை: பெயர் · authority: Nannūl (labels) / Tholkappiyam (sandhi)
```

**B. Verb across tenses — வா**
```
வந்தான்    → வா + த்   + ஆன்   · இறந்தகாலம் · படர்க்கை ஆண்பால் ஒருமை
வருகிறான் → வா + கிற் + ஆன்   · நிகழ்காலம்
```
Note the suppletive stem: the surface is வரு-, the root is **வா**. The engine knows; a guesser would say "வரு".

**C. Pure-Tamil equivalents — அகராதி**
```
அகரவரிசை   [attested in: viruba, tamilmandram]
அகரநிரல்   [attested in: tamilmandram]
அகரமுதலி   [attested in: tamilmandram]
```
Every candidate names the glossary that attests it. Nothing coined by the machine.

**D. Origin by orthography — ரயில் / ஜோதி**
```
ரயில் → loanword — word-initial ‘ர்’ cannot begin a native Tamil word
                   (Tholkappiyam மொழிமரபு, முதல் எழுத்து rule)
ஜோதி  → வடசொல்  — contains the Grantha letter ஜ, outside the native Tamil எழுத்து set
```

**E. The honest gap — புத்தகம்**
```
origin: unknown — "attested as a borrowed word, but no orthographic marker distinguishes
                  வடசொல் from loanword — source language undetermined"
equivalents: நூல் · சுவடி நூல்   (attested)
```

Speaker note on E: **Land this one deliberately.** Everyone in the room knows புத்தகம் is from Sanskrit
*pustaka*. Our tool says "I can't prove it from my sources." That's the point — it reports what it can
ground, not what it can guess. Invite them to help close exactly this gap.

---

## Slide 6 — How it's built (for the technically curious)

- **ThamizhiMorph FST** (Sarveswaran, Dias & Butt 2021; Univ. of Moratuwa) — rule-based morphological
  analyser, version-pinned. We **wrap** it; we did not rebuild it.
- **Tholkappiyam / Nannūl rules** — hand-encoded once, in code, tested. Never re-derived by an AI.
- **Indic-To-Pure-Tamil** — 2,063 attested borrowed→pure-Tamil mappings.
- **Tamil Wiktionary** — consulted live for meanings, cached with provenance.
- **Our curated verb paradigms** — hand-verified table filling gaps in the FST's lexicon.

Key architectural point for a technical audience: **Tamil words are generated, not listed.** One root
yields thousands of forms, so no dictionary can enumerate them. That's why the core is a rule engine,
not a database — unlike almost every other MCP server.

---

## Slide 7 — Who it's for

- **App developers** — a Tamil grammar helper for school students becomes one API call. The developer
  needs no Tamil grammar expertise; the app can show the student *why*, and the teacher can check the citation.
- **Teachers & students** — answers that carry their authority, so they can be verified, not just trusted.
- **Scholars** — a machine-readable, citable encoding of classical grammar rules.
- **The Tamil language itself** — every analysis is logged as verified grammatical data, seeding the
  corpus that future Tamil-capable AI models will need. **Tamil is "low-resource" because it lacks data;
  this creates data by being used.**

---

## Slide 8 — Where we honestly are

**Working:** 9 tools · 104 automated tests · full formation/root/grammar/origin/equivalents pipeline ·
provenance on every claim · open source, Apache-2.0, under the IEF nonprofit.

**Not done yet (say this out loud):**
- Madras University Lexicon & TVA கலைச்சொல் glossaries not yet pinned
- Citations are **chapter-level**, not verse-level (நூற்பா) — a digitized edition must be pinned first
- Origin classification returns `unknown` more often than we'd like
- **Single words only** — no phrases or sentences yet

Speaker note: This slide *builds* credibility with scholars rather than costing it — and it's the
natural bridge to the ask.

---

## Slide 9 — The ask

- **Scholars:** help us encode rules correctly, and adjudicate disputed origins.
- **Teachers:** tell us the questions students actually ask, so we can test against them.
- **Developers:** build with it; every gap you hit makes it better.
- **Everyone:** which classical editions should we pin as the authority? That choice should be made by
  Tamil scholars, not by engineers.

---

## Slide 10 — Close

**"An AI that speaks Tamil should also know Tamil."**
Open source · Tholkappiyam-first · every claim cited · honest about what it doesn't know.
github.com/ief-global/thamizh-mcp

---

## ⚠️ Accuracy guardrails — do NOT put these in the deck

1. **Do not use ஜன்னல் as an origin example.** The tool classifies it **வடசொல்** because of the Grantha
   ஜ, but ஜன்னல் is a **Portuguese** loan (*janela*). The tool does record "a non-Sanskrit loan
   transliterated with Grantha letters" as an alternative, but the headline class is wrong and a scholar
   will catch it instantly. Its *equivalent* (ஜன்னல் → சாளரம்) is correct and safe to show.
2. **Don't claim we beat frontier models.** On *basic* morphology a strong model already scores ~97% in
   our tests. The honest claim is: models fail on **harder items and lexical facts** (invented
   equivalents), weaker/cheaper models fail far more, and only our answers are **citable and reproducible**.
3. **Don't quote a "lift %" yet.** The A/B measurement isn't complete; a number now would be unreliable.
4. **Don't call it "the first Tamil NLP tool."** The correct, defensible phrasing is "plausibly the first
   Tamil **சொல்-analysis MCP server**" — there's a rich Tamil NLP ecosystem we build on.
5. **Attribute ThamizhiMorph** wherever the analyser is shown. It's Apache-2.0 research by
   Sarveswaran, Dias & Butt (2021) and deserves visible credit.

## Design direction (for Claude Design)

Tone: scholarly, calm, confident — not a startup pitch. Tamil script must render in a proper Unicode
Tamil font at large sizes (Noto Sans Tamil or similar); **check every Tamil glyph renders**, especially
conjuncts like ற்ற, ன்ற, க்ஷ. Prefer the Tamil term first with English gloss in parentheses. Colour: deep
indigo/maroon with warm neutrals reads as scholarly; avoid neon/tech gradients. The demo slides should
show **monospace output blocks** — the raw honesty of the tool's output is the persuasive element.
