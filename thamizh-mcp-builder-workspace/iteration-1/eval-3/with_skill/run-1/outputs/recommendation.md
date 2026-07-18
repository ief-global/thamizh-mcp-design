# THAMIZH MCP — language, data sources, and how to stop it hallucinating

This answers three things for a Tamil word-analysis MCP server: which programming language to build it in, which specific data sources ground each kind of answer, and the architecture that keeps it from inventing Tamil grammar the way a plain chatbot would.

The whole point of this server over a bare LLM is that **every claim traces back to a real Tamil linguistic authority** — a morphological analyser, a classical grammar rule, a standard lexicon, or an etymology dataset — not to the model's own guesses. A confident-but-unsourced Tamil grammar answer is exactly the failure this product exists to remove. The recommendations below are built around that bar.

---

## 1. Programming language: **Python**

**Recommendation: build the analysis core in Python, and run it as a Python MCP server (FastMCP) for v1.**

The reason is not preference — it is where the Tamil-NLP ecosystem actually lives. Every authentic source this server must ground against is either a Python package or a native binary with Python tooling around it:

- **ThamizhiMorph** (the primary morphological engine) is a `foma` finite-state transducer. Its core `flookup` binary is callable from any language, but its surrounding tooling — the tokeniser, the `thamizhi-morph-parse-2.py` driver, the ThamizhiPOSt POS tagger — is Python, and it depends on `stanza`. *(Verified: the repo is 100% Python with an Apache-2.0 licence.)*
- **open-tamil**, **ThamizhiLIP / ThamizhiPOSt**, and most other analysers and validators ship as Python packages (pip-installable).

So the linguistic logic wants to live in Python. You have two viable shapes:

| Option | When to choose it |
|---|---|
| **(A) Python MCP server (FastMCP)** — one language, direct library calls. | **Recommended for v1.** Simplest path; no inter-process boundary. |
| (B) TypeScript MCP server calling a Python analysis service. | Only if a specific deployment target forces the TS MCP SDK. It adds a process boundary for **zero linguistic benefit** at this stage. |

Pick (A) unless there is a hard external reason to prefer the TypeScript SDK. Keep the linguistic decoding logic (turning FST tags into பகுபத உறுப்பு parts, mapping case tags to வேற்றுமை names) in one well-tested Python module rather than re-deriving it per request.

---

## 2. Data sources, mapped to what each one grounds

A word analysis has four concerns the user cares about: **origin** (native vs borrowed), **root + meaning**, **formation** (how the word is built), and **grammar** (class, case, tense). Each concern gets its own authentic source — and a cross-check, because origin in particular is genuinely contested for many words.

### Origin — native (இயற்சொல்) vs borrowed (வடசொல் / English / other)
- **Primary:** Thamizhi Word Validator (a word that fails pure-Tamil validation is a borrowing candidate) + loanword/etymology datasets — the **Indic-To-Pure-Tamil** mappings (Sanskrit-origin → pure Tamil) and the Kaggle **Tamil loan-words classification** set (English↔Tamil).
- **Cross-check:** the etymology notes in the Madras Tamil Lexicon, plus Tholkappiyam's வடசொல் rule.
- **Classify into the authentic four-way scheme**, not a native/loan boolean: **இயற்சொல்** (core native), **திரிசொல்** (literary/shifted native), **திசைச்சொல்** (regional), **வடசொல்** (Sanskrit/Indo-Aryan). For வடசொல் record the adaptation type — **தற்சமம்** (little change) vs **தற்பவம்** (adapted to Tamil phonology). For modern borrowings outside the classical scheme (English, etc.), label as loanword and name the source language, and say explicitly that the classical scheme predates them.

### Root + meaning
- **Root / lemma (வேர்ச்சொல்):** **ThamizhiMorph** (cross-check: open-tamil stemmer).
- **Meaning:** **Madras University Tamil Lexicon** (the gold-standard scholarly dictionary, 1924–1936, hosted via DSAL / U. Chicago — *verified, last data refresh Sep 2023, CC BY-NC-ND, no official REST API so plan an offline copy or queried interface*). Cross-check with **AU-KBC Tamil WordNet** (structured synsets/glosses) and the **Cologne Online Tamil Lexicon** as a second opinion.

### Formation — how the surface word is built (பகுபத உறுப்பு, sandhi)
- **ThamizhiMorph FST analysis**, decoded into Nannūl's six உறுப்புகள் (பகுதி, விகுதி, இடைநிலை, சாரியை, சந்தி, விகாரம்).
- ThamizhiMorph matters here specifically because it is **the only maintained Tamil analyser that handles Sandhi** *(verified against the project README)* — and Sandhi is what you must decode to explain word formation honestly. Decode its tags back into the classical terms rather than re-deriving sandhi from scratch.

### Grammar — word class, case, tense
- **ThamizhiMorph POS + case tags** (with ThamizhiPOSt for context when the input is more than a bare word), explained through the **classical grammar rules** of **Tholkappiyam (Collatikāram)** and **Nannūl** — these supply the authentic output vocabulary (the four சொல் classes, the eight வேற்றுமை names).

### Before any lookup: normalization
- Run **open-tamil `get_letters`** (correct Tamil multi-codepoint grapheme splitting) or Google **Nisaba** first. Bad Unicode normalization silently corrupts every downstream lookup.

### Field → source map

| Output field | Primary source | Cross-check |
|---|---|---|
| `normalized` | open-tamil / Nisaba | — |
| `origin.class` | Thamizhi Validator + loanword data | Lexicon etymology, Tholkappiyam rule |
| `origin.borrowed_from` | Indic-To-Pure-Tamil, Kaggle loanword set | Indo-Aryan loanword scholarship |
| `lemma` / root | ThamizhiMorph | open-tamil stemmer |
| `pos` / `grammar.case` | ThamizhiMorph (+ ThamizhiPOSt) | UD Tamil treebank |
| `meaning` | Madras Tamil Lexicon | AU-KBC WordNet, Cologne OTL |
| `formation.components` | ThamizhiMorph FST tags → Nannūl உறுப்பு decoding | — |
| `grammar` (rule explanation) | Tholkappiyam / Nannūl | — |

**Rule of thumb:** a field with no source in this table is a field the server cannot honestly fill yet. Either find a source or have the tool report the gap.

*(Tip: `narVidhai/tamil-nlp-catalog` is the meta-catalog of all these resources — use it to discover more as the project grows.)*

---

## 3. How to make sure it does not hallucinate Tamil grammar

A plain chatbot hallucinates because it is *the source of its own answer*. The architecture below removes that property — the model can only relay what a source produced. Four principles, all enforced in the tools and the system prompt, not just in the build process:

1. **Provenance on every claim.** Each filled field carries which source produced it, so the agent can say "root per ThamizhiMorph; meaning per Madras Tamil Lexicon; origin per Tholkappiyam's வடசொல் rule." A claim with no attached source is a bug, not an answer. Wrap each source behind a small adapter with a uniform interface (input: a normalized word; output: the fields it can fill + its own provenance).

2. **An honest gap beats a fluent guess.** If no grounding source covers a word, the correct output is `{ "status": "no_entry", "source", "note" }` — for example "no lexicon entry found" — **never** a smooth invented answer. This is the single most important behaviour to test for, because it is the exact failure mode a chatbot falls into. Give every tool an actionable error path that names which source was missing.

3. **Separate analysis from disambiguation — return all valid readings.** Tamil is morphologically rich; one surface form often has several valid analyses, and ThamizhiMorph itself returns all of them when it cannot disambiguate. Keep them all rather than silently picking one. (Concrete case: the suffix இல் marks both the 5th வேற்றுமை / ablative "from" and the 7th / locative "in" — the word alone cannot resolve which, so return both with provenance.)

4. **Name uncertainty; do not manufacture certainty.** Origin classification is genuinely contested — a word called இயற்சொல் by one authority may be argued வடசொல்/தற்பவம் by another. Report the competing claims and their evidence in an `alternatives` field; do not pick one silently.

### The tool surface that enforces this
- One focused, read-only tool per concern — `classify_origin`, `get_root`, `get_meaning`, `explain_formation`, `explain_grammar` — each returning a `sources` array and an honest-gap status.
- Plus one composed **`analyze_word`** workflow tool returning the whole word-analysis object at once (the dominant agent intent is "tell me everything about this word"), which merges provenance and returns per-section gaps rather than failing whole if one source misses.
- A canonical JSON contract where every analytical field is `required` to carry provenance and gaps are explicit — so a missing source surfaces structurally instead of being papered over by fluent text.

### Prove it works (evaluation)
Build the eval set from real words chosen to exercise each concern, and hand-verify the correct answer against the sources before locking it:
- a clearly native word (e.g. **மரம்**),
- an inflected form needing sandhi-aware splitting (e.g. **மரத்தில்**),
- a Sanskrit loanword / வடசொல் (e.g. **புத்தகம்** / **ஆசிரியர்**),
- an English loanword (e.g. **கம்ப்யூட்டர்** / **பஸ்**),
- an ambiguous or disputed case.

The headline pass/fail test: **when given a word no source covers, does an LLM using the server report the gap, or does it hallucinate a confident answer?** If it reports the gap, the grounding is working.

---

## One-paragraph answer

Build it in **Python** (a Python FastMCP server for v1), because ThamizhiMorph and essentially every authentic Tamil-NLP source is Python or a native binary with Python tooling. Ground **origin** in the Thamizhi Word Validator plus loanword datasets (Indic-To-Pure-Tamil, Kaggle) cross-checked against lexicon etymology and Tholkappiyam; **root and formation** in ThamizhiMorph (the only maintained analyser that handles Sandhi); **meaning** in the Madras University Tamil Lexicon with AU-KBC WordNet as cross-check; and **grammar** in ThamizhiMorph's tags explained through Tholkappiyam and Nannūl. It avoids chatbot-style hallucination by making the LLM a *relayer*, never a *source*: every field carries provenance, an unsupported word returns an explicit "no entry found" gap instead of a guess, ambiguous forms return all valid readings, and contested origins report the disagreement — all enforced by the JSON contract and proven by an eval that specifically checks the server reports gaps rather than inventing answers.
