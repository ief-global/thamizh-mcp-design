# THAMIZH MCP Server — Planning Blueprint (v1, for sign-off)

**Status:** Draft for approval. No code is written until you sign off on Section 11.
**Prepared:** 2026-06-28
**Owner:** You. **Scope of this doc:** the planning phase only — what you need, what we're building, the contract, and the boundaries.

---

## 0. One-line description

THAMIZH is a Model Context Protocol (MCP) server that exposes a single tool: give it **one Tamil word**, and it returns a structured linguistic analysis — whether the word is **native (தனித்தமிழ்) or borrowed (கடன்சொல்)**, its **root and meaning**, its **morphology (how the word is built)**, and the **grammar** that governs it.

---

## 1. What "done" looks like (the acceptance test)

You hand the server a word like **`மரத்தில்`** and get back, reliably and in a fixed shape:

- **Origin:** native Tamil.
- **Root:** `மரம்` (maram) = "tree".
- **Formation:** `மரம்` + locative case suffix `இல்`, with the euphonic insertion `மரம் → மரத்து` (the *attu* sandhi for nouns ending in `-ம்`).
- **Meaning:** "in/on the tree".
- **Grammar:** noun, neuter (அஃறிணை), locative case (இடப்பொருள் / ஏழாம் வேற்றுமை).

If that round-trips correctly for a representative set of test words (Section 9), v1 is done.

---

## 2. What you need before any code (the readiness checklist)

This is the "what do I actually need to begin" answer. Tick each item; the project is blocked until the must-haves are green.

### 2.1 Decisions you must make (I've pre-filled defaults — change or confirm)
| # | Decision | Default I'm choosing | Why |
|---|----------|----------------------|-----|
| D1 | Language/runtime | **Python 3.11+ with FastMCP (the official `mcp` SDK)** | Best Tamil NLP ecosystem (open-tamil, indic-nlp), fastest path, easiest to test. |
| D2 | Transport | **stdio** for v1 (local). Add streamable-HTTP later if you host it. | stdio is the standard for desktop MCP clients (Claude Desktop, Cursor). Zero network surface. |
| D3 | Knowledge source strategy | **Hybrid:** a curated local lexicon/rule-base first; LLM reasoning as a fallback/enrichment layer, clearly flagged. | Pure-LLM answers drift and hallucinate etymology. Pure-dictionary can't handle inflected forms. Hybrid is honest and testable. |
| D4 | Input script | **Tamil script (UTF-8) as primary**; accept ISO 15919 / romanized as a secondary input with auto-transliteration. | Real users type Tamil; romanized is a convenience. |
| D5 | Scope of "word" | **One orthographic word** (may be inflected/compound). Not sentences, not phrases. | Keeps the tool contract sharp; matches your brief. |
| D6 | Confidence & honesty | Every field carries a **confidence** and a **source** ("lexicon" / "rule" / "inferred"). Unknown → say "unknown", never guess silently. | Etymology is genuinely contested; the tool must not fabricate. |
| D7 | Etymology granularity | Native vs borrowed, plus **donor language** when borrowed (Sanskrit, English, Persian/Urdu, Portuguese, etc.). | Matches "native or borrowed" and adds the obvious next question for free. |

### 2.2 Data / assets you need to gather
- **A seed lexicon** of Tamil root words with: lemma, gloss (Tamil + English), part of speech, gender/class (உயர்திணை/அஃறிணை), and an origin tag (native / loan + donor). Start with ~500–2,000 high-frequency entries; grow over time.
- **A loanword list** — Sanskrit-derived (வடசொல்), English, Persian/Arabic, Portuguese, Dutch — to power the origin classifier.
- **Morphological rule tables:** case suffixes (வேற்றுமை உருபு), the sandhi/euphonic-insertion rules (சந்தி: அத்து, இன், இற்று saari), plural `-கள்`, tense markers, pronominal/verbal endings.
- **A transliteration map** (Tamil ↔ ISO 15919) for romanized input and for output labels.
- **Licensing note:** confirm the license of any dictionary data you import (e.g., Madras University Tamil Lexicon, University of Madras / DSAL, Wiktionary). Wiktionary (CC BY-SA) and DSAL are the safest starting points. *This is a must-check before shipping.*

### 2.3 Environment / tooling
- Python 3.11+, a virtual env, and the `mcp` package (FastMCP).
- `open-tamil` and/or `indic-nlp-library` for tokenization, transliteration, and basic morphology.
- An MCP client to test against (Claude Desktop or the `mcp` dev inspector).
- `pytest` + a golden-file test set (Section 9).

### 2.4 Skills/knowledge in the room
- Tamil grammar literacy (or a reviewer who has it) to validate the rule tables — this is the single biggest risk to correctness. **Recommend: line up one Tamil-grammar reviewer before building the rule base.**

---

## 3. The tool contract (the heart of the blueprint)

### 3.1 Tool: `analyze_tamil_word`

**Description (for the model that calls it):** "Analyze a single Tamil word. Returns its origin (native or borrowed), root, meaning, morphological breakdown, and grammatical features."

**Input schema**
```json
{
  "word": "string  — one Tamil word, in Tamil script or romanized (required)",
  "input_script": "enum [tamil, romanized, auto]  — default: auto",
  "include": "array — optional subset of [origin, root, meaning, morphology, grammar]; default: all"
}
```

**Output schema (v1 — stable contract)**
```json
{
  "input": { "raw": "மரத்தில்", "normalized": "மரத்தில்", "script_detected": "tamil" },
  "origin": {
    "classification": "native | borrowed | uncertain",
    "donor_language": "string|null",     // e.g. "Sanskrit", "English"
    "evidence": "string",                // why we think so
    "confidence": 0.0
  },
  "root": {
    "lemma": "மரம்",
    "transliteration": "maram",
    "part_of_speech": "noun | verb | adjective | ...",
    "confidence": 0.0
  },
  "meaning": {
    "gloss_ta": "மரம்",
    "gloss_en": "tree",
    "inflected_sense": "in/on the tree",
    "confidence": 0.0
  },
  "morphology": {
    "segments": [
      { "form": "மரம்", "type": "root", "gloss": "tree" },
      { "form": "அத்து", "type": "euphonic_increment (சந்தி)", "gloss": "linking augment" },
      { "form": "இல்", "type": "case_suffix (வேற்றுமை உருபு)", "gloss": "locative" }
    ],
    "process": "root + locative case with -att- augment",
    "confidence": 0.0
  },
  "grammar": {
    "word_class": "noun",
    "gender_class": "அஃறிணை (neuter/non-rational)",
    "number": "singular",
    "case": "locative (ஏழாம் வேற்றுமை / இடப்பொருள்)",
    "tense": null,
    "person": null,
    "notes": "string",
    "confidence": 0.0
  },
  "meta": {
    "sources": ["lexicon", "rule-engine", "inferred"],
    "warnings": ["..."],
    "schema_version": "1.0"
  }
}
```

### 3.2 Why a single tool (not five)
Your brief asks five questions about one word. Bundling them into **one call with an optional `include` filter** keeps the calling model's life simple, returns one coherent object, and avoids five round-trips. We can split later if needed — the `include` field is the escape hatch.

### 3.3 Error & edge behavior (non-negotiable)
- Empty/multi-word input → structured error: `"Provide exactly one Tamil word."`
- Word not in lexicon → still return morphology + grammar from rules; mark `root`/`meaning` confidence low and `sources: ["inferred"]`.
- Ambiguous word (multiple analyses, e.g. `ஆடு` = "goat" / "dance/play") → return the **top analysis plus an `alternatives` array**; never silently pick one and hide the rest.
- Non-Tamil input → `origin.classification: "uncertain"` with a clear warning, not a crash.

---

## 4. How the analysis actually works (pipeline, conceptual)

```
word in
  → 1. Normalize  (Unicode NFC, strip ZWJ/ZWNJ, detect script, transliterate if romanized)
  → 2. Segment    (split into root + suffixes using morphological rules + lexicon longest-match)
  → 3. Lemmatize  (recover the dictionary root from the inflected form; undo sandhi)
  → 4. Lexicon lookup (root → gloss, POS, gender, origin tag)
  → 5. Origin classify (native vs loan; if loan, identify donor — by lexicon tag, then by
                        phonological cues, e.g. presence of grantha letters ஜ ஷ ஸ ஹ க்ஷ → likely Sanskrit/loan)
  → 6. Grammar assemble (map suffixes → case/tense/person/number/gender)
  → 7. Confidence + sourcing (tag every field; collect warnings)
  → structured JSON out
```

Each stage is independently testable. Stages 2–3 (segmentation + sandhi reversal) are the hardest and where most bugs will live.

---

## 5. Linguistic coverage for v1 (scope fence)

**In scope (v1):**
- Nouns: all 8 vEtRumai cases, singular/plural, the major sandhi augments (அத்து, இன், etc.), gender/class.
- Verbs: basic tense (past/present/future), person/number/gender endings, common forms.
- Origin: native vs borrowed; donor identification for Sanskrit, English, Persian/Arabic, Portuguese.
- Compounds: split common புணர்ச்சி (compound) joins where rules allow.

**Out of scope (v1 — explicitly deferred):**
- Full poetic/literary (செய்யுள்) morphology and rare classical forms.
- Sentence-level parsing, multiple words, idioms.
- Dialectal and spoken-colloquial variation as first-class (note them, don't fully model them).
- Exhaustive etymological chains (we give the proximate donor, not the full Indo-European tree).

These are roadmap, not v1.

---

## 6. Architecture & repo layout (proposed)

```
thamizh-mcp/
├── server.py            # FastMCP app; defines analyze_tamil_word
├── pipeline/
│   ├── normalize.py     # script detect, NFC, transliteration
│   ├── segment.py       # morphological segmentation
│   ├── lemmatize.py     # sandhi reversal → root
│   ├── origin.py        # native/loan classifier
│   ├── grammar.py       # suffix → grammatical features
│   └── confidence.py    # scoring + sourcing
├── data/
│   ├── lexicon.json     # roots: lemma, gloss, pos, gender, origin
│   ├── loanwords.json   # donor-language tags
│   ├── suffixes.json    # case/tense/person tables
│   └── sandhi.json      # euphonic rules
├── tests/
│   ├── golden/          # word → expected JSON
│   └── test_pipeline.py
├── pyproject.toml
└── README.md            # install + MCP client config
```

---

## 7. Build phases (after sign-off)

| Phase | Deliverable | Exit criterion |
|-------|-------------|----------------|
| P0 | Skeleton FastMCP server, `analyze_tamil_word` returns a stub | Tool shows up + callable in an MCP client |
| P1 | Normalize + transliteration + script detection | Romanized and Tamil input both normalize correctly |
| P2 | Lexicon lookup + meaning + POS for **uninflected** roots | Root words return correct gloss/POS |
| P3 | Morphology: segmentation, sandhi reversal, grammar features | Inflected nouns (cases, plural) parse correctly |
| P4 | Origin classifier (native/borrowed + donor) | Test loanwords classified correctly |
| P5 | Verbs (tense/person/number) | Common verb forms parse |
| P6 | Confidence, sourcing, alternatives, errors | Golden test set passes; honest "unknown" behavior verified |
| P7 | Docs, packaging, client config, license sign-off | Installs clean on a fresh machine |

Recommend shipping a usable internal milestone at **end of P4** (nouns + origin + meaning), then iterating.

---

## 8. Risks & how we de-risk

| Risk | Severity | Mitigation |
|------|----------|------------|
| **Etymology is contested** — sources disagree on native vs Sanskrit | High | Cite the source, return confidence, allow "uncertain". Never assert as fact what the field disputes. |
| **Sandhi reversal is hard** — many forms, irregularities | High | Rule tables + lexicon longest-match + golden tests; accept partial coverage in v1 and flag low confidence. |
| **Ambiguity** — one form, many analyses | Medium | `alternatives` array; surface, don't hide. |
| **Lexicon licensing** | Medium | Confirm license before importing any dictionary; default to CC-licensed sources (Wiktionary/DSAL). |
| **LLM hallucination** if used for enrichment | Medium | LLM output is clearly tagged `source: "inferred"` and lower confidence; never overrides lexicon/rules. |
| **Unicode pitfalls** — ZWJ, grantha letters, normalization | Medium | Normalize to NFC early; explicit handling of grantha (ஜ ஷ ஸ ஹ) as loan signals. |
| **Scope creep into sentences/poetry** | Low | Section 5 fence is the contract; defer politely. |

---

## 9. Test plan (golden set — define these before coding)

A small, hand-validated set covering each behavior. Examples:

| Word | Tests |
|------|-------|
| `மரம்` (maram) | native, root=self, meaning=tree, noun, neuter, nominative |
| `மரத்தில்` (marattil) | locative case + att- sandhi |
| `புத்தகம்` (puttakam) | **borrowed** (Sanskrit pustaka), meaning=book |
| `பஸ்` / `பேருந்து` | English loan vs native coinage — origin contrast |
| `வந்தான்` (vandhaan) | verb, past tense, 3rd person masculine singular |
| `பூக்கள்` (pookkal) | plural `-கள்` |
| `ஆடு` (aadu) | **ambiguity:** goat (noun) vs play/dance (verb) → alternatives |
| `xyz` / English junk | graceful "uncertain" + warning |

Each row → an expected JSON file in `tests/golden/`. CI passes only if all match.

---

## 10. Open questions for you (answer at sign-off; I've defaulted them all)

1. **Runtime:** OK with **Python + FastMCP**? (default: yes)
2. **First lexicon source:** OK to start from **Wiktionary (CC BY-SA) + DSAL**, license confirmed before import? (default: yes)
3. **LLM enrichment:** allow an LLM fallback for unknown words, clearly flagged as inferred — or **rules/lexicon only** for v1? (default: allow, flagged)
4. **Output language of labels:** grammar terms in **both Tamil and English** (e.g. "locative (ஏழாம் வேற்றுமை)")? (default: both)
5. **First milestone:** ship at **end of P4** (nouns + origin + meaning) as internal v0.5? (default: yes)
6. **Reviewer:** do you have a Tamil-grammar reviewer to validate rule tables, or should I scope the rules conservatively? (default: scope conservatively until a reviewer is named)

---

## 11. Sign-off

By approving, you're agreeing to:
- The **single-tool contract** in Section 3 and its output schema (v1.0).
- The **scope fence** in Section 5 (one word; nouns+verbs; deferrals listed).
- The **defaults** in Sections 2.1 and 10 (Python/FastMCP, stdio, hybrid knowledge, honesty-first confidence/sourcing).
- The **phase plan** in Section 7, shipping an internal milestone at end of P4.

**Approve as-is** → I scaffold P0 (skeleton server + stub tool) next.
**Approve with changes** → tell me which defaults in Section 10 to flip.

---

### Appendix A — Glossary (so the schema reads cleanly)
- **தனித்தமிழ் / native:** word of Tamil origin, no foreign root.
- **கடன்சொல் / borrowed:** loanword; **வடசொல்** specifically = Sanskrit-derived.
- **வேற்றுமை (vEtRumai):** the case system (8 cases).
- **உருபு (urupu):** case/grammatical suffix.
- **சந்தி (sandhi) / புணர்ச்சி:** euphonic changes and augments at morpheme/word boundaries (e.g. `மரம் + இல் → மரத்தில்`).
- **உயர்திணை / அஃறிணை:** rational (human/divine) vs non-rational (everything else) gender-class — the backbone of Tamil agreement.
- **grantha letters (ஜ ஷ ஸ ஹ க்ஷ ஶ):** characters used mainly to write loan sounds; a useful (not definitive) signal of borrowing.
