# Authentic Tamil source catalog

Each grounding source below is mapped to the output field(s) it can fill, with how to reach it, its licence, and its **tier**. The tier matters because the two kinds are maintained differently:

- **Anchor** — stable, authoritative, version-pinned. The ground truth you cross-check against.
- **Evolving** — community-contributed, internet-fed, pulled at query time, cached, and accumulated so the tool's coverage grows by itself. You can't pin a version — pin the retrieval date + provenance of each fact.

When a word isn't covered by any source, that gap is a valid output — record the failure mode, don't paper over it.

## Table of contents

- [1. Morphological analysers (root, formation, grammar)](#1-morphological-analysers) — *anchor*
- [2. Lexicons & dictionaries (meaning)](#2-lexicons--dictionaries) — *anchor + evolving*
- [3. Etymology & loanword data (origin)](#3-etymology--loanword-data) — *evolving*
- [4. Classical grammar tradition — Tholkappiyam first](#4-classical-grammar-tradition) — *anchor*
- [5. Evolving / self-enriching internet sources](#5-evolving--self-enriching-internet-sources) — *evolving*
- [6. Native-equivalent sources — கலைச்சொல் / தனித்தமிழ்](#6-native-equivalent-sources) — *anchor + evolving*
- [7. Supporting utilities](#7-supporting-utilities)
- [8. Field → source map](#8-field--source-map)

---

## 1. Morphological analysers  *(anchor)*

These give the **root/lemma**, the **formation**, and **POS/case** tags. Crucially, they are **rule-based**,
so they need *no per-word maintenance* — the FST generates millions of forms from paradigms. This is the answer to "I don't want to hand-build a word list" for everything inflectional.

### ThamizhiMorph — primary engine
- **What it gives:** lemma + POS + inflection analysis for nouns, verbs, particles; **handles Sandhi** (the only maintained Tamil analyser that does), essential for decoding word formation. Also a *generator* (15M+ verbs, 10M+ nouns from paradigms).
- **How it works:** a foma finite-state transducer. `echo தமிழ் | flookup tamil-nouns.fst` →
  `தமிழ்\tதமிழ்+noun+nom` (lemma + pos + analysis after `+`). Python driver `thamizhi-morph-parse-2.py` adds tokeniser + POS context.
- **Access / licence:** GitHub `sarves/thamizhi-morph`, **Apache-2.0**. FST models, 80K-noun lexicon,
  18-class verb paradigm, meta-morph rules included. Web portal `http://nlp-tools.uom.lk/thamizhi-morph/`. Needs `foma` + `stanza`.
- **Note:** returns *all* valid analyses when it can't disambiguate — keep them all.

### ThamizhiLIP / ThamizhiPOSt
- Python APIs for POS + morphological tagging and Universal Dependency parsing; use for contextual POS when input is more than a bare word. `sarves.github.io/thamizhilip`, `github.com/nlpcuom/ThamizhiPOSt`.

### Thamizhi Word Validator — purity / native check
- Validates whether a string is a well-formed **pure Tamil** word — a strong native-vs-borrowed signal (a word that fails pure-Tamil validation is a borrowing candidate). GitHub `sarves/thamizhi-validator`.

### open-tamil (Ezhil Language Foundation)
- Lightweight stemmer, `get_letters` (correct multi-codepoint Tamil grapheme splitting), transliteration, encoding converters. `github.com/Ezhil-Language-Foundation/open-tamil`, pip-installable. Good for normalization and as a fallback stemmer.

---

## 2. Lexicons & dictionaries  *(anchor + evolving)*

These give **meaning** (and often etymology notes that help with origin).

### Madras University Tamil Lexicon (via DSAL, U. Chicago) — authoritative meaning *(anchor)*
- The standard scholarly Tamil dictionary (1924–1936), searchable; entries often include etymology and source-language tags. `https://dsal.uchicago.edu/dictionaries/tamil-lex/`; also the DDSA Tamil Lexicon apps. No official REST API — plan a queried interface or an offline copy of the digitized data. Treat as a pinned anchor (data last refreshed Sep 2023).

### Cologne Online Tamil Lexicon (OTL) *(anchor)*
- Comprehensive Tamil dictionary at the University of Cologne; TSCII interface, mirrored at
  `tamilelibrary.org/lexicon/`. A second dictionary opinion.

### AU-KBC Tamil WordNet / IndoWordNet — structured senses *(anchor)*
- Synsets, relations, glosses — structured meanings, better than a flat definition for a clean `meaning` field and sense disambiguation. 
- `cfilt.iitb.ac.in/indowordnet/`, 
- `au-kbc.org/nlp/lex_re.html`.

### Tamil Wiktionary — evolving meaning/coverage *(evolving)*
- Community-maintained, constantly growing dictionary with definitions, etymology, and inflection tables. Pull at query time to fill words the anchors miss; cache + provenance-tag the result. This is a primary engine of the self-enriching design for the *meaning* layer.

---

## 3. Etymology & loanword data  *(evolving)*

These serve the **origin** decision (native இயற்சொல் vs borrowed வடசொல்/English/other). Most are community
datasets that grow — treat as evolving and refresh periodically.

- **Tamil loan-words classification dataset (Kaggle, "muthua")** — labelled English↔Tamil loanword data;
  base for detecting English borrowings.
- **Indic-To-Pure-Tamil** (`narVidhai/Indic-To-Pure-Tamil`) — mappings from borrowed Indic (Sanskrit-origin)
  words to pure-Tamil equivalents; a practical native-vs-வடசொல் reference.
- **Tamil Glossary Dataset** (`osf.io/ngt6v`) — glossary data for origin/meaning cross-checks.
- **Indo-Aryan / Sanskrit loanword scholarship** — the framework + word lists. Tholkappiyam names Sanskrit
  borrowings **வடசொல்**; loanwords are **தற்சமம்** (little change) vs **தற்பவம்** (adapted to Tamil phonology).
  Wikipedia "Indo-Aryan loanwords in Tamil" is a usable starting list; individual claims are contestable —
  cite them as such.
- **narVidhai/tamil-nlp-catalog** — the meta-source cataloguing all of the above; mine it to discover new
  datasets as the tool enriches itself.

---

## 4. Classical grammar tradition — Tholkappiyam first  *(anchor)*

The rules that make an explanation *authentic*. These are not APIs — they are the authority you encode and
cite. **Citation priority is fixed: தொல்காப்பியம் first, நன்னூல் only as fallback.** Details in
`references/tamil-grammar.md`.

- **தொல்காப்பியம் (Tholkappiyam) — the golden source, cite first.** The oldest extant Tamil grammar. Its
  *சொல்லதிகாரம் (Collatikāram)* codifies the word classes (பெயர்/வினை/இடை/உரியியல்), the four origin classes
  (இயற்சொல்/திரிசொல்/திசைச்சொல்/வடசொல்), and the eight வேற்றுமை (வேற்றுமையியல்); its *எழுத்ததிகாரம்* codifies
  புணர்ச்சி/sandhi (புணரியல்). Use Tholkappiyam for all of these.
- **நன்னூல் (Nannūl) — fallback only.** The standard medieval grammar. Use it where Tholkappiyam does not
  enumerate the point — chiefly the formal six-part **பகுபத உறுப்பிலக்கணம்** (பகுதி/விகுதி/இடைநிலை/சாரியை/
  சந்தி/விகாரம்). Even then, ground the underlying elements (sandhi, suffixes) in Tholkappiyam and label the
  six parts per Nannūl, stating which authority gave which.

The server's grammar output should always record `authority: "Tholkappiyam"` or `"Nannūl"` so the
Tholkappiyam-first rule is visible and auditable.

---

## 5. Evolving / self-enriching internet sources  *(evolving)*

This tier is what lets the tool **grow without a hand-maintained dictionary**. Pull at query time, cache the
result with its retrieval date + provenance, and accumulate into the local knowledge store.

- **Tamil Wiktionary** — definitions, etymology, inflection tables (see §2).
- **Tamil Wikisource / Tamil Wikipedia** — usage, attestation, and entries for proper/rare words.
- **Community datasets in `tamil-nlp-catalog`** — loanword lists, glossaries, pure-Tamil mappings that get
  updated by contributors over time.
- **Enrichment discipline:** an evolving-source fact is only kept if it can be (a) attributed and (b)
  cross-checked against an anchor or a classical rule. Unverifiable internet data is surfaced as
  low-confidence with its source, never promoted to a grounded claim.

---

## 6. Native-equivalent sources  *(anchor + evolving)*

These ground **objective 5** — suggesting the attested native Tamil equivalent of a borrowed word (கணினி for
computer). The authority here is the **கலைச்சொல் / தனித்தமிழ் terminology tradition**, not Tholkappiyam.
Hard rule: only suggest an equivalent that one of these attests; never invent a coinage. Return ranked
candidates with source + register (technical / literary / everyday); explicit gap when none.

- **Indic-To-Pure-Tamil** (`narVidhai/Indic-To-Pure-Tamil`) *(evolving)* — Sanskrit/Indic வடசொல் → pure-Tamil
  equivalents. Primary map for வடசொல் substitution.
- **Tamil Virtual Academy (TVA) கலைச்சொல்** *(anchor)* — academic terminology glossaries; established
  technical coinages (கணினி, தொலைபேசி, மின்னஞ்சல்…). `tamilvu.org`.
- **Tamil Nadu Govt / Anna University கலைச்சொல் அகராதி** *(anchor)* — official scientific & administrative
  terminology. Stable, citable; a strong anchor for technical loans (esp. English).
- **Tamil Wiktionary** *(evolving)* — frequently lists தனித்தமிழ்/native equivalents and usage; pull + cache.
- **தனித்தமிழ் lexicons / movement lists** *(evolving)* — the Devaneya Pāvāṇar (மொழிஞாயிறு பாவாணர்) school and
  தனித்தமிழ் இயக்கம் equivalent lists. Useful but **opinionated** — mark register and note when a coinage is
  purist rather than common usage.
- **Loanword classification + glossary datasets** *(evolving)* — the Kaggle Tamil loan-words set, Tamil
  Glossary Dataset (`osf.io/ngt6v`), catalogued in `tamil-nlp-catalog`'s "Pure Tamil" section.

Coverage is honestly uneven: strong for English technical terms and common Sanskrit loans; thin for
Portuguese/Urdu/Marathi/Telugu loans, where "no attested equivalent" is a frequent and acceptable answer.

---

## 7. Supporting utilities

- **Normalization & grapheme splitting:** open-tamil `get_letters`; Google **Nisaba** (`google-research/nisaba`)
  for Brahmic normalization. Do this first — bad normalization corrupts every downstream lookup.
- **Transliteration:** AI4Bharat Xlit, Aksharamukha (has an API) — for romanized I/O and English-loanword matching.
- **POS corpora / treebanks:** AU-KBC POS corpus, Universal Dependencies Tamil treebank — for evaluating POS output.

---

## 8. Field → source map

| Output field | Tier | Primary source | Cross-check |
|---|---|---|---|
| `normalized` | — | open-tamil / Nisaba | — |
| `origin.class` (இயற்சொல்/…/வடசொல்) | evolving + anchor | Thamizhi Validator + loanword data | **Tholkappiyam** rule, lexicon etymology |
| `origin.borrowed_from` | evolving | loanword datasets (Kaggle, Indic-To-Pure-Tamil) | Indo-Aryan loanword scholarship |
| `lemma` / root | anchor | ThamizhiMorph (rule-based) | open-tamil stemmer |
| `pos` / `grammar.case` | anchor | ThamizhiMorph (+ ThamizhiPOSt) | UD treebank |
| `meaning` | anchor → evolving | Madras Tamil Lexicon → Tamil Wiktionary | AU-KBC WordNet, Cologne OTL |
| `formation.components` | anchor | ThamizhiMorph tags → **Tholkappiyam** elements, Nannūl six-part labels | — |
| `grammar` (rule explanation) | anchor | **Tholkappiyam** (Nannūl fallback) | — |
| `native_equivalent` (only if non-native) | anchor → evolving | கலைச்சொல்/TVA/govt terminology → Indic-To-Pure-Tamil, Wiktionary, தனித்தமிழ் lists | attestation required; explicit gap if none |

Rule of thumb: a field with no source here is a field the server cannot honestly fill yet — pull from the
evolving tier, and if that also misses, report the gap.

## Addendum 2026-07-18 — Aalamaram treebank (anchor, adoption conditional on license)

**Aalamaram** — largest public Tamil treebank (~10,000 sentences; POS, NER, morphological parsing,
dependency parsing; UD-based with Tamil-specific clitic/multi-word segmentation). Abirami et al.,
WILDRE@LREC 2024 (aclanthology.org/2024.wildre-1.11); Sarveswaran co-author. Grounds: morphology
cross-checks vs ThamizhiMorph, eval fixtures (L3/L4) with sentential context, phrase-level v2, SLM corpus.
NOT an equivalents source. Access/license: distribution not yet located (not on HF; no public GitHub repo
found) — verify before use (D-008). Tier: anchor once pinned.
