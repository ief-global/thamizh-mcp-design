# Walkthrough: How the THAMIZH MCP server analyzes மரத்தில்

**Word:** மரத்தில் ("in the tree")
**Type:** an inflected, sandhi-bearing noun — exactly the case the server exists to handle, because a plain LLM will happily guess the split and the case without grounding either.

This walks through one `analyze_word` call, tracing how the server fans it out to five focused tools, what each returns, and **which authentic source grounds each part** of the answer. The whole point of this server over a bare LLM is that every claim below carries provenance — root per ThamizhiMorph, meaning per Madras Tamil Lexicon, origin per Tholkappiyam's rule — and gaps are reported, never invented.

---

## Step 0 — Normalization (before any tool runs)

The agent calls `analyze_word({ word: "மரத்தில்" })`. Before any lookup, the input is Unicode-normalized and grapheme-split.

- **What happens:** the raw string is canonicalized so every downstream FST and dictionary lookup sees the same bytes. Tamil letters are multi-codepoint, so naive splitting corrupts lookups.
- **Grounding source:** open-tamil `get_letters` (correct Tamil grapheme splitting), optionally Google Nisaba for Brahmic normalization.
- **Output:** `normalized: "மரத்தில்"` — clean, ready for lookup.

> Why this matters: bad normalization silently breaks every later step, so it is done first and pinned to a version.

---

## Step 1 — `classify_origin` → the ORIGIN answer

**Question answered:** is this a native Tamil word or a borrowing?

- **What the tool returns:**
  - `class: "இயற்சொல்"` (the native class)
  - `is_native: true`
  - `borrowed_from: null`, `adaptation: null`
  - `evidence:` the base word மரம் passes pure-Tamil validation and appears in the lexicon with no source-language tag.
  - `confidence:` high
  - `alternatives: []` (no competing authority claims this as a loan)
- **Grounding sources:**
  - **Thamizhi Word Validator** — confirms மரம் is a well-formed pure Tamil word (a word that *fails* this check would be a borrowing candidate).
  - **Loanword datasets** (Kaggle English-loanword set, Indic-To-Pure-Tamil) — மரம் is absent, so it is not flagged as a borrowing.
  - **Madras Tamil Lexicon etymology notes** — the entry carries no வடசொல்/Sanskrit source tag.
  - **Tholkappiyam (சொல்லதிகாரம்)** — supplies the authentic four-way frame (இயற்சொல் / திரிசொல் / திசைச்சொல் / வடசொல்) the class name comes from, rather than a bare native/loan boolean.

> Honesty note built into the design: origin is contested for many words. Here it is not — but if any authority called மரம் a borrowing, the tool would return that as an `alternatives` entry with its evidence, not silently pick a side.

---

## Step 2 — `get_root` → the ROOT answer

**Question answered:** what is the lemma / வேர்ச்சொல் under this inflected surface form?

- **What the tool returns:**
  - `lemma: "மரம்"`
  - `all_analyses:` keeps every valid morphological parse ThamizhiMorph emits (the FST handles sandhi, so it correctly strips the locative inflection back to the base noun rather than treating மரத்தில் as an unanalyzable string).
  - For மரத்தில், the analysis resolves to lemma மரம் + noun + locative inflection.
- **Grounding sources:**
  - **ThamizhiMorph** (foma finite-state transducer, queried via `flookup`) — the primary engine, and the *only* maintained Tamil analyser that handles Sandhi, which is what makes the மரம் → மரத்தில் decomposition trustworthy.
  - **open-tamil stemmer** — fallback / cross-check.

> Design rule honored here: when the analyser returns more than one valid analysis, the tool keeps them all in `all_analyses` instead of silently disambiguating.

---

## Step 3 — `get_meaning` → the MEANING answer

**Question answered:** what does the word mean, per an authentic dictionary?

- **What the tool returns** (meaning is looked up on the **lemma** மரம், not the inflected surface form):
  - `senses: [{ gloss_ta: "மரம் (a tree / wood)", gloss_en: "tree; wood, timber", pos: "noun", citation: <Madras Tamil Lexicon entry> }]`
  - The locative inflection adds "in / at" to the surface reading ("in the tree"), but the dictionary sense belongs to the lemma.
- **Grounding sources:**
  - **Madras University Tamil Lexicon** (via DSAL, U. Chicago) — the authoritative scholarly definition (gold standard for an "authentic" gloss).
  - **AU-KBC Tamil WordNet** — structured synset/sense, good for a clean `meaning` field.
  - **Cologne Online Tamil Lexicon (OTL)** — second dictionary opinion.

---

## Step 4 — `explain_formation` → the FORMATION answer

**Question answered:** how is the surface word built from its parts? This is the heart of the analysis, and where sandhi-aware grounding pays off.

- **What the tool returns:**
  - `word_type: "பகுபதம்"` (an analyzable/derived word, not a simple பகாப்பதம்)
  - `components:` (labeled with Nannūl's பகுபத உறுப்பு names, in order)

    | # | part (உறுப்பு) | form | role |
    |---|---|---|---|
    | 1 | பகுதி (root/base) | மரம் | the core noun carrying the meaning |
    | 2 | சாரியை (euphonic augment) | அத்து | inserted to join base to the case suffix; மரம் → மரத்து |
    | 3 | விகுதி (terminal suffix) | இல் | the locative case marker (ஏழாம் வேற்றுமை உருபு) |

  - `sandhi:` `[{ type: "திரிதல்", detail: "மரம் → மரத் — final ம் changes at the join (விகாரம்: திரிதல்)" }]`

- **Grounding sources:**
  - **ThamizhiMorph FST tags** — the raw decomposition (handles the sandhi at the மரம்/அத்து/இல் junctures).
  - **நன்னூல் (பகுபத உறுப்பிலக்கணம்)** — supplies the authentic உறுப்பு labels (பகுதி, சாரியை, விகுதி, விகாரம்) so the explanation reads in real Tamil grammatical terms, not a paraphrase. The FST tags are *decoded into* these Nannūl names by the server's linguistic-logic module.

> This matches the hand-verified fixture in the skill's grammar primer: பகுதி மரம் + சாரியை அத்து (with விகாரம் மரம்→மரத்) + விகுதி இல்.

---

## Step 5 — `explain_grammar` → the GRAMMAR answer

**Question answered:** what is the grammatical category and the case feature behind the word?

- **What the tool returns:**
  - `word_class: "பெயர்"` (noun / பெயர்ச்சொல்)
  - `case: { number: 7, name: "ஏழாம் வேற்றுமை", function: "locative / இடப்பொருள் (in / at / on)" }`
  - `person_number_gender:` ஒருமை (singular)
  - `notes:` **the suffix இல் is genuinely ambiguous** — it marks both the 7th case (locative, "in") and the 5th case (ablative, "from"). The word alone cannot resolve this.
  - `alternatives:` `{ number: 5, name: "ஐந்தாம் வேற்றுமை", function: "ablative (from)" }` — returned, not discarded.
- **Grounding sources:**
  - **ThamizhiMorph POS + case tag** — the POS (noun) and inflection class.
  - **Tholkappiyam / நன்னூல்** — the eight-வேற்றுமை system that names the 7th case ஏழாம் வேற்றுமை and defines the இல் உருபு (and the documented இல் = 5th/7th overlap).

> Honesty note honored: rather than guessing locative over ablative, the tool returns **both readings with provenance** — the honest answer is "this is locative, but the same form is also readable as ablative."

---

## The merged result (`analyze_word` output)

`analyze_word` composes the five tools above into one **word analysis object** (per `word_analysis_schema.json`) and merges provenance:

| Concern | Answer | Grounded by |
|---|---|---|
| **normalized** | மரத்தில் | open-tamil `get_letters` / Nisaba |
| **origin** | இயற்சொல் — native, not borrowed | Thamizhi Validator + loanword datasets + Lexicon etymology + Tholkappiyam rule |
| **root (lemma)** | மரம் | ThamizhiMorph (sandhi-aware), open-tamil fallback |
| **meaning** | tree; wood/timber | Madras Tamil Lexicon (+ AU-KBC WordNet, Cologne OTL) |
| **formation** | பகுபதம்: பகுதி மரம் + சாரியை அத்து (விகாரம் திரிதல்: மரம்→மரத்) + விகுதி இல் | ThamizhiMorph FST tags → decoded into Nannūl உறுப்புகள் |
| **grammar** | பெயர்ச்சொல், ஏழாம் வேற்றுமை (locative, singular); *also* ஐந்தாம் வேற்றுமை (ablative) | ThamizhiMorph POS/case + Tholkappiyam/Nannūl |

Every section carries a `sources` array (`{name, ref, retrieved}`), so the agent can say in plain words:

> "மரத்தில் is the native Tamil word மரம் ('tree') in the locative case. Root and case per **ThamizhiMorph**; meaning per the **Madras Tamil Lexicon**; the formation labels (பகுதி / சாரியை / விகுதி, with the மரம்→மரத் change) per **Nannūl**; the native (இயற்சொல்) classification per **Tholkappiyam** and the pure-Tamil **Validator**. The locative suffix இல் is also readable as ablative — both are reported."

---

## What grounding buys you on this exact word

Three failure modes a plain LLM hits on மரத்தில், and how the grounded design avoids each:

1. **Wrong split.** A model might guess மர + த்தில் or treat the word as a single root. ThamizhiMorph's sandhi-aware FST gives the correct மரம் + அத்து + இல், and Nannūl labels it.
2. **Silent case guess.** A model will usually just say "locative" and stop. The server reports the documented இல் = locative/ablative ambiguity and returns **both** readings rather than manufacturing certainty.
3. **Unsourced confidence.** Every claim above names its authority. If any source had *no* entry for மரத்தில் (or its lemma), the server would emit an explicit gap — `{ status: "no_entry", source, note }` — instead of a fluent guess. That honest-gap behavior is the single most important property this server is built to guarantee.

---

### Sources referenced in this walkthrough

- **ThamizhiMorph** — foma FST analyser/generator (root, formation, POS/case; handles sandhi). GitHub `sarves/thamizhi-morph`, Apache-2.0.
- **Thamizhi Word Validator** — pure-Tamil validity check (origin signal). GitHub `sarves/thamizhi-validator`.
- **Madras University Tamil Lexicon** — authoritative meaning. DSAL, U. Chicago `dsal.uchicago.edu/dictionaries/tamil-lex/`.
- **AU-KBC Tamil WordNet / Cologne OTL** — meaning cross-checks.
- **Loanword datasets** — Kaggle Tamil loan-words, `narVidhai/Indic-To-Pure-Tamil` (origin cross-check).
- **open-tamil** — normalization / grapheme splitting / fallback stemmer. `Ezhil-Language-Foundation/open-tamil`.
- **Tholkappiyam (சொல்லதிகாரம்)** — word classes, the four origin classes, the eight வேற்றுமை.
- **நன்னூல்** — பகுபத உறுப்பிலக்கணம் (the six word-formation parts) and புணர்ச்சி (sandhi) rules.
