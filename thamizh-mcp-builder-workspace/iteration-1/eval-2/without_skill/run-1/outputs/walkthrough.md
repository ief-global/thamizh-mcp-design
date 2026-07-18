# How the THAMIZH MCP server analyzes மரத்தில்

A step-by-step trace of one word through the server. The word is **மரத்தில்** ("in the tree"). For each
tool call you get: what the agent sends, what the tool returns, and — the whole point of this project — which
**authentic source** grounds that part of the answer. No claim in the final output comes from the LLM's own
guess; every field is attributable.

The shape of the final answer is the `ThamizhWordAnalysis` object (`assets/word_analysis_schema.json`). The
tools that fill it are defined in `references/tool-design.md`. The grounding sources are catalogued in
`references/sources.md`, and the grammar terms come from `references/tamil-grammar.md`.

---

## Step 0 — Normalize the input (runs before any analysis)

Tamil letters are multi-codepoint grapheme clusters, so the same visible word can arrive in different byte
sequences. Bad normalization corrupts every downstream lookup, so this happens first, inside `analyze_word`
before it fans out to the focused tools.

- **Input:** `மரத்தில்`
- **Action:** Unicode-normalize and verify grapheme splitting.
- **Output:** `normalized: "மரத்தில்"` and the grapheme sequence `ம ர த் தி ல்`.
- **Grounded by:** **open-tamil** (`get_letters` for correct Tamil grapheme splitting) and/or Google
  **Nisaba** for Brahmic-script normalization. *(sources.md §5 Supporting utilities)*

This is plumbing, not analysis — but it is the reason the lexicon and FST lookups that follow actually match.

---

## Step 1 — `classify_origin` → where the word comes from

The agent asks: is this native Tamil or borrowed?

- **Input:** `{ "word": "மரத்தில்" }`
- **Returns:**

```json
{
  "class": "இயற்சொல்",
  "is_native": true,
  "borrowed_from": null,
  "adaptation": null,
  "evidence": "Stem மரம் passes pure-Tamil validation; appears in the lexicon with no source-language tag; falls in Tholkappiyam's இயற்சொல் class (ordinary native words in common use).",
  "confidence": 0.95,
  "alternatives": [],
  "sources": [
    { "name": "Thamizhi Word Validator", "ref": "github.com/sarves/thamizhi-validator" },
    { "name": "Madras Tamil Lexicon", "ref": "dsal.uchicago.edu/dictionaries/tamil-lex/" },
    { "name": "Tholkappiyam — Collatikāram (origin classes)", "ref": "இயற்சொல் rule" }
  ]
}
```

**Which source grounds what here:**

- The native-vs-borrowed *signal* comes from the **Thamizhi Word Validator** — the stem `மரம்` is a
  well-formed pure-Tamil word, which is the strong evidence that it is not a borrowing.
- The cross-check that it carries **no source-language tag** comes from the **Madras University Tamil
  Lexicon** etymology notes.
- The *vocabulary* of the answer — calling it **இயற்சொல்** rather than a bare "native" boolean — comes from
  **Tholkappiyam's** four origin classes (இயற்சொல் / திரிசொல் / திசைச்சொல் / வடசொல்). மரம் is an ordinary
  native word in common use, which is exactly the definition of இயற்சொல். *(tamil-grammar.md §2)*

The `alternatives` array is empty because the authorities agree here. For a contested word (the honesty rule
in the SKILL), competing origin claims would be returned in that array rather than silently resolved.

---

## Step 2 — `get_root` → the lemma / வேர்ச்சொல்

The agent asks: strip the inflection down to the dictionary form.

- **Input:** `{ "word": "மரத்தில்" }`
- **Action under the hood:** the surface word is sent to the **ThamizhiMorph** finite-state transducer via
  `flookup`, conceptually `echo மரத்தில் | flookup tamil-nouns.fst`.
- **Returns:**

```json
{
  "lemma": "மரம்",
  "all_analyses": [
    { "lemma": "மரம்", "pos": "noun", "tags": ["noun", "loc", "sg"] },
    { "lemma": "மரம்", "pos": "noun", "tags": ["noun", "abl", "sg"] }
  ],
  "sources": [
    { "name": "ThamizhiMorph", "ref": "github.com/sarves/thamizhi-morph (Apache-2.0)" }
  ]
}
```

**Which source grounds what here:**

- The root **மரம்** comes from **ThamizhiMorph**, the primary morphological engine. It is the only maintained
  Tamil analyser that handles Sandhi, which is what lets it reverse மரத்தில் back to மரம் correctly.
  *(sources.md §1)*
- Note **two analyses are returned, not one.** ThamizhiMorph returns every valid reading when it cannot
  disambiguate — the `இல்` suffix is ambiguous (more in Step 5). The server keeps both per the "separate
  analysis from disambiguation" rule; it does not silently pick locative.
- **open-tamil's** stemmer is the documented fallback if ThamizhiMorph is unavailable. *(sources.md §6)*

---

## Step 3 — `get_meaning` → the dictionary sense

The agent asks: what does the root mean?

- **Input:** `{ "word": "மரம்", "lang": "both" }` (the agent passes the lemma from Step 2, not the inflected
  surface form, so it hits the dictionary headword).
- **Returns:**

```json
{
  "senses": [
    {
      "gloss_ta": "செடியினும் பெரிய, அடிமரமும் கிளைகளும் உடைய தாவரம்",
      "gloss_en": "tree; a large woody plant with a trunk and branches",
      "pos": "noun",
      "citation": "Madras Tamil Lexicon, s.v. மரம்"
    }
  ],
  "sources": [
    { "name": "Madras University Tamil Lexicon (via DSAL, U. Chicago)", "ref": "dsal.uchicago.edu/dictionaries/tamil-lex/" },
    { "name": "AU-KBC Tamil WordNet", "ref": "cfilt.iitb.ac.in/indowordnet/" }
  ]
}
```

**Which source grounds what here:**

- The authoritative definition comes from the **Madras University Tamil Lexicon** (1924–1936, via DSAL /
  University of Chicago) — the gold-standard scholarly dictionary and the project's primary `meaning` source.
- The **AU-KBC Tamil WordNet / IndoWordNet** synset is the cross-check, giving a structured sense useful for
  disambiguation. **Cologne OTL** is the documented second-dictionary opinion. *(sources.md §2, §6)*

The lookup is on the lemma `மரம்`, which is why Step 2 had to run first — the dictionary is keyed by
headword, not by inflected form.

---

## Step 4 — `explain_formation` → how the word is built (பகுபத உறுப்பு)

The agent asks: break the surface word into its grammatical parts.

- **Input:** `{ "word": "மரத்தில்" }`
- **Action under the hood:** decode the **ThamizhiMorph** FST tags from Step 2 back into Nannūl's
  பகுபத உறுப்புகள் using the mapping logic in `tamil-grammar.md §3`.
- **Returns:**

```json
{
  "word_type": "பகுபதம்",
  "components": [
    { "part": "பகுதி",  "form": "மரம்",  "role": "root / base (the noun stem carrying meaning)" },
    { "part": "சாரியை", "form": "அத்து", "role": "euphonic augment joining stem to case suffix" },
    { "part": "விகுதி", "form": "இல்",   "role": "case suffix (ஏழாம் வேற்றுமை உருபு / locative)" }
  ],
  "sandhi": [
    { "type": "திரிதல்", "detail": "மரம் → மரத் — final ம் changes (விகாரம்) before the அத்து சாரியை." }
  ],
  "sources": [
    { "name": "ThamizhiMorph (FST analysis, handles Sandhi)", "ref": "github.com/sarves/thamizhi-morph" },
    { "name": "Nannūl — பகுபத உறுப்பிலக்கணம்", "ref": "six-part word-formation rules" }
  ]
}
```

**Which source grounds what here:**

- The *split itself* — that மரத்தில் decomposes at all, and where the morpheme boundaries fall — comes from
  **ThamizhiMorph**, because it handles Sandhi. Re-deriving sandhi by hand is exactly what we avoid.
  *(tamil-grammar.md §5)*
- The *labels* on each part (**பகுதி / சாரியை / விகுதி**, and the **விகாரம் → திரிதல்** classification of the
  ம்→த் change) come from **Nannūl's** பகுபத உறுப்பிலக்கணம் — the standard medieval grammar for word
  formation. That is what makes the explanation authentic Tamil grammar rather than a plausible paraphrase.
- This matches the worked fixture in `tamil-grammar.md §6`: பகுதி `மரம்`, சாரியை `அத்து`
  (with விகாரம்: மரம் → மரத்), விகுதி `இல்`. The word is **பகுபதம்** (analyzable), not பகாப்பதம், because it
  splits into these grammatical parts.

---

## Step 5 — `explain_grammar` → the grammatical category and case

The agent asks: what kind of word is this and what case is it in?

- **Input:** `{ "word": "மரத்தில்" }`
- **Returns:**

```json
{
  "word_class": "பெயர்",
  "case": { "number": 7, "name": "ஏழாம் வேற்றுமை", "function": "locative / இடப்பொருள் (\"in / at / on\")" },
  "tense": null,
  "person_number_gender": "ஒருமை (singular)",
  "notes": "The suffix இல் also marks the 5th case (ஐந்தாம் வேற்றுமை, ablative / \"from\"); both readings are valid from the word alone and are returned together — the server does not guess which one context intends.",
  "sources": [
    { "name": "ThamizhiMorph (POS + case tag)", "ref": "github.com/sarves/thamizhi-morph" },
    { "name": "Tholkappiyam / Nannūl — வேற்றுமை system", "ref": "eight-case scheme" }
  ]
}
```

**Which source grounds what here:**

- The **POS tag** (noun → பெயர்ச்சொல்) and the **raw case tag** come from **ThamizhiMorph** (with
  **ThamizhiPOSt** available for contextual POS if the input were a phrase). The **UD Tamil treebank** is the
  documented evaluation cross-check. *(sources.md §6)*
- The *naming and meaning* of the case — **ஏழாம் வேற்றுமை**, locative, இடப்பொருள் — comes from the
  **Tholkappiyam / Nannūl** eight-வேற்றுமை scheme. *(tamil-grammar.md §4)*
- The honest ambiguity in `notes` is required by the grammar primer: the suffix **இல்** marks *both* the 7th
  case (locative, "in") and the 5th case (ablative, "from"). The server cannot resolve this from the word in
  isolation, so it returns both readings with provenance rather than manufacturing certainty.
  *(tamil-grammar.md §4, ambiguity note)*

---

## The composed `analyze_word` result

`analyze_word` is the workflow tool the agent calls most often — "tell me everything about மரத்தில்" in one
call. It runs Steps 0–5, merges the provenance from each, and returns the full `ThamizhWordAnalysis` object.
If one source had missed (e.g. no lexicon entry), that section would carry an explicit gap instead of failing
the whole response.

```json
{
  "word": "மரத்தில்",
  "normalized": "மரத்தில்",
  "origin": {
    "class": "இயற்சொல்", "is_native": true, "borrowed_from": null, "adaptation": null,
    "confidence": 0.95,
    "sources": [ { "name": "Thamizhi Word Validator" }, { "name": "Madras Tamil Lexicon" }, { "name": "Tholkappiyam" } ]
  },
  "lemma": "மரம்",
  "all_analyses": [
    { "lemma": "மரம்", "pos": "noun", "tags": ["noun","loc","sg"] },
    { "lemma": "மரம்", "pos": "noun", "tags": ["noun","abl","sg"] }
  ],
  "pos": "பெயர்ச்சொல்",
  "meaning": {
    "senses": [ { "gloss_ta": "…பெரிய தாவரம்", "gloss_en": "tree", "citation": "Madras Tamil Lexicon, s.v. மரம்" } ],
    "sources": [ { "name": "Madras Tamil Lexicon" }, { "name": "AU-KBC Tamil WordNet" } ]
  },
  "formation": {
    "word_type": "பகுபதம்",
    "components": [
      { "part": "பகுதி", "form": "மரம்" },
      { "part": "சாரியை", "form": "அத்து" },
      { "part": "விகுதி", "form": "இல்" }
    ],
    "sandhi": [ { "type": "திரிதல்", "detail": "மரம் → மரத் (ம் changes)" } ],
    "sources": [ { "name": "ThamizhiMorph" }, { "name": "Nannūl" } ]
  },
  "grammar": {
    "word_class": "பெயர்",
    "case": { "number": 7, "name": "ஏழாம் வேற்றுமை", "function": "locative / இடப்பொருள்" },
    "person_number_gender": "ஒருமை",
    "notes": "இல் also reads as 5th case (ablative) — both returned.",
    "sources": [ { "name": "ThamizhiMorph" }, { "name": "Tholkappiyam / Nannūl" } ]
  },
  "gaps": [],
  "sources": [
    { "name": "ThamizhiMorph", "ref": "github.com/sarves/thamizhi-morph" },
    { "name": "Madras Tamil Lexicon", "ref": "dsal.uchicago.edu/dictionaries/tamil-lex/" },
    { "name": "Thamizhi Word Validator", "ref": "github.com/sarves/thamizhi-validator" },
    { "name": "AU-KBC Tamil WordNet", "ref": "cfilt.iitb.ac.in/indowordnet/" },
    { "name": "Tholkappiyam / Nannūl", "ref": "classical grammar tradition" }
  ]
}
```

---

## Summary — five answers, five grounded sources

| Concern | Tool | Answer for மரத்தில் | Grounded by (authentic source) |
|---|---|---|---|
| **Origin** | `classify_origin` | இயற்சொல் (native) | Thamizhi Word Validator + Madras Tamil Lexicon etymology, framed by **Tholkappiyam's** four origin classes |
| **Root** | `get_root` | மரம் | **ThamizhiMorph** FST (Sandhi-aware); open-tamil stemmer fallback |
| **Meaning** | `get_meaning` | tree / பெரிய தாவரம் | **Madras University Tamil Lexicon**; AU-KBC WordNet cross-check |
| **Formation** | `explain_formation` | பகுதி மரம் + சாரியை அத்து + விகுதி இல் (விகாரம்: ம்→த்) | **ThamizhiMorph** split, decoded into **Nannūl's** பகுபத உறுப்பு labels |
| **Grammar** | `explain_grammar` | பெயர்ச்சொல், ஏழாம் வேற்றுமை (locative), ஒருமை — *also* 5th case | **ThamizhiMorph** POS/case tag, named via **Tholkappiyam / Nannūl** வேற்றுமை scheme |

**Two behaviours that make this trustworthy rather than just fluent:**

1. **Every field cites its source.** The agent can truthfully say: "root per ThamizhiMorph; meaning per
   Madras Tamil Lexicon; origin per Tholkappiyam's இயற்சொல் class; formation labelled per Nannūl."
2. **Ambiguity is reported, not hidden.** The இல் suffix is genuinely both locative (7th) and ablative (5th);
   the word alone cannot decide. The server returns both readings with provenance instead of guessing — which
   is the single most important behaviour the project tests for. Likewise, if no source covered the word, the
   answer would be an honest gap, never an invented value.
