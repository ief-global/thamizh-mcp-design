# THAMIZH MCP — Project Blueprint

> Phase 0 deliverable. This is the document to sign off on **before any code is written**. It locks scope,
> the canonical output contract, the grounding sources, the tool surface, and the stack. Where the brief left
> a choice open, I made a reasonable call and stated it under **Decision** — change any of these and the rest
> of the plan adapts.
>
> **The one rule behind everything here:** every claim the server makes traces back to a real Tamil
> linguistic authority — an analyser, a lexicon, or a classical grammar rule — never to the model's own
> guess. A confident-but-unsourced Tamil grammar answer is the exact failure this project exists to remove.

---

## 0. What you actually need to begin (the "start checklist")

Before Phase 1 (locking sources) you need five things settled. All five are decided in this blueprint:

1. **A locked scope** — what the v1 answers and, just as importantly, what it does not. → Section 1.
2. **A frozen output contract** — the shape of one word analysis, so tools/sources/evals all serve the same
   object. → Section 2, backed by `assets/word_analysis_schema.json`.
3. **A source-to-field map** — every output field tied to at least one authentic source, with how you reach
   it and what happens when it has no entry. → Section 3.
4. **A tool surface** — the MCP tools and their boundaries. → Section 4.
5. **A stack decision** — language + transport, with the reasoning. → Section 5.

Concrete prerequisites to have in hand before Phase 1 coding (not blockers for sign-off, but the first
shopping list):

- A machine that can run **`foma` + `flookup`** (the ThamizhiMorph FST engine) and **Python 3.10+**.
- The **ThamizhiMorph** repo (`sarves/thamizhi-morph`, Apache-2.0) cloned and its FST models built locally.
- **`open-tamil`** installed (pip) for normalization and grapheme splitting.
- A decision on **lexicon access** (Madras Tamil Lexicon has no official API) — see Section 8, risk #1.
- Sign-off on this blueprint.

---

## 1. Objective & scope

- **One-line objective:** Given a single Tamil word, return a grounded, authentic analysis of its origin,
  root + meaning, formation, and grammar — every field attributable to a real Tamil source.

- **In scope (v1):** **single-word analysis** producing four things the user asked for:
  1. **Origin** — native vs borrowed, expressed in Tholkappiyam's four-way frame
     (இயற்சொல் / திரிசொல் / திசைச்சொல் / வடசொல்), plus modern loanword languages outside that scheme.
  2. **Root + meaning** — the lemma (வேர்ச்சொல்) and its dictionary gloss.
  3. **Formation** — how the surface word is built from its parts (பகுபத உறுப்பிலக்கணம், புணர்ச்சி / sandhi).
  4. **Grammar** — the word class and grammatical features (சொல் வகை, வேற்றுமை, tense, PNG).

- **Borrowed source languages the v1 will detect and label:**
  - **Sanskrit / வடசொல்** — the classical case, with adaptation type தற்சமம் (tatsama) vs தற்பவம் (tadbhava).
  - **English** — the dominant modern loanword source; high practical value.
  - **Other Indo-Aryan (Hindi/Urdu), Perso-Arabic, Telugu/Dravidian-regional** — **detected and labelled when
    a source covers them, but not guaranteed.** They fall under the generic `loanword` class with
    `borrowed_from` set to the source language.
  - **Decision:** v1 commits to Sanskrit and English as first-class, everything else best-effort. Reason:
    those two carry the overwhelming majority of real queries and have the best dataset coverage; over-promising
    on Perso-Arabic/Telugu etymology would force unsourced guesses, which violates the core rule.

- **Out of scope (v1) — stated deliberately so the boundary is clean:**
  - **Phrase / sentence parsing.** Input is one word. *Reason:* the four concerns are word-level; sentence
    parsing multiplies ambiguity and pulls in syntax (தொடரியல்), a different problem. Context-aware POS via
    ThamizhiPOSt is a Phase-2+ extension, not v1.
  - **Form generation** (producing inflected forms from a lemma). ThamizhiMorph *can* generate, and it's
    valuable for spell-check / data augmentation later — but v1 is an **analyser**, not a generator.
  - **Spell-check / correction**, **transliteration as a primary feature**, and **a UI**. All later.

- **Primary users:** Tamil speakers, learners, and teachers who want grounded, authentic answers about a
  word — and an LLM agent that should cite a Tamil authority instead of improvising.

- **Why single-word v1 is the right call (defending it):** the value proposition is *depth + provenance on
  one word*, not breadth. A narrow, fully-grounded analyser is shippable, testable against hand-verified
  fixtures, and demonstrates the core differentiator (authenticity over fluency) before any scope creep.

---

## 2. Canonical output — the word analysis object

- **Contract:** `assets/word_analysis_schema.json` (`ThamizhWordAnalysis`, JSON Schema draft-07). Frozen for
  v1. Any change is logged in this section with a reason and date.

- **Shape, in one breath:** a top-level object with `word`, `normalized`, then the four concern blocks
  `origin`, `lemma`/`all_analyses`/`pos`, `meaning`, `formation`, `grammar`, plus a `gaps` array and a
  top-level `sources` array. Every concern block carries its own `sources`.

- **Non-negotiable contract properties (these encode the authenticity rules):**
  - **Provenance on every claim.** Each filled field carries a `sources` entry of `{name, ref, retrieved}`.
    The agent must be able to say "root per ThamizhiMorph; meaning per Madras Tamil Lexicon; origin per
    Tholkappiyam's வடசொல் rule."
  - **Explicit gaps, never fabrication.** If no source covers a field, it goes in `gaps` as
    `{field, note}` (e.g. "no lexicon entry found") — the model does not fill it.
  - **All analyses, not one.** `all_analyses` holds every valid morphological reading when the surface form
    is ambiguous; `origin.alternatives` holds competing origin claims when authorities disagree. The server
    does not silently disambiguate.
  - **Authentic vocabulary.** Enums use the real Tamil grammatical terms (பகுதி, விகுதி, இடைநிலை, சாரியை,
    சந்தி, விகாரம்; the eight வேற்றுமை; the four origin classes) — that is what makes output authentic rather
    than a plausible paraphrase.

- **Worked target outputs** (also the eval fixtures — see Section 7): மரத்தில், வந்தான், புத்தகம்,
  கம்ப்யூட்டர். Their expected `formation`/`grammar` are spelled out in `references/tamil-grammar.md` §6 and
  carried into Section 7 below.

---

## 3. Grounding sources (per output field)

Each output field is mapped to a primary authentic source and a cross-check, with access, licence, and the
**failure mode** — what the tool returns when the source has no entry. Rule of thumb from the catalog: a
field with no source here is a field the server cannot honestly fill yet.

| Field | Primary source | Cross-check | Access | Licence | Failure mode |
|---|---|---|---|---|---|
| `normalized` | open-tamil (`get_letters`) / Nisaba | — | local pip lib / native | MIT/GPL (verify in repo) | Normalization is mandatory and deterministic; if input is malformed Unicode, return error before any lookup (bad normalization corrupts everything downstream). |
| `origin.class` (இயற்சொல்/…/வடசொல்/loanword) | Thamizhi Word Validator + loanword/etymology data | Madras Lexicon etymology notes; Tholkappiyam rule | local lib + datasets | Validator: see `sarves/thamizhi-validator` repo | `origin.class = "unknown"`, record what was checked in `evidence`; do **not** default to native. |
| `origin.borrowed_from` | loanword datasets (Kaggle "tamil-loan-words", `narVidhai/Indic-To-Pure-Tamil`) | Indo-Aryan loanword scholarship (cite as contestable) | downloadable datasets | per-dataset (verify) | `borrowed_from = null`; if class is `loanword`/`வடசொல்` but language unknown, say so in `evidence`. |
| `lemma` / root | **ThamizhiMorph** (foma / `flookup`) | open-tamil stemmer | local FST binary + models | **Apache-2.0** | If FST returns no analysis: report gap; fall back to open-tamil stemmer and label the lemma as low-confidence with that provenance. |
| `all_analyses` / `pos` | ThamizhiMorph (keep **all** analyses) + ThamizhiPOSt for context | UD Tamil treebank | local | Apache-2.0 | Multiple analyses → return all; zero analyses → `pos = "unknown"`, gap recorded. |
| `meaning` | **Madras University Tamil Lexicon** (DSAL, U. Chicago) | AU-KBC Tamil WordNet; Cologne OTL | web interface / offline copy (no official REST API) | scholarly, check redistribution terms | `meaning.senses = []` + gap "no lexicon entry"; never synthesize a definition. |
| `formation.components` | ThamizhiMorph FST tags → **Nannūl உறுப்பு** decoder | — | local | Apache-2.0 (engine) + n/a (rules) | If word is `பகாப்பதம்` (unanalyzable) say so; if borrowing, flag that decomposition belongs to the source language, not Tamil. |
| `formation.sandhi` (புணர்ச்சி) | ThamizhiMorph (it handles Sandhi) decoded into விகாரம் types | Nannūl rules | local | Apache-2.0 | Empty `sandhi` array when no juncture effect; never invent one. |
| `grammar` (rule explanation, case, tense, PNG) | **Tholkappiyam (சொல்லதிகாரம்) / Nannூல்** rules, encoded; case/POS tags from ThamizhiMorph | UD treebank | encoded in code | n/a (classical authority) | Report which feature couldn't be determined; the இல் case ambiguity (5th vs 7th வேற்றுமை) is returned as **both** readings, not resolved. |

**Phase-1 v1 grounding stack, summarized by concern (the recommended minimum to integrate first):**

- **Origin:** Thamizhi Validator + a loanword/etymology dataset, cross-checked against lexicon etymology
  notes; classify into Tholkappiyam's four classes.
- **Root + meaning:** ThamizhiMorph (lemma) + Madras Tamil Lexicon (gloss).
- **Formation:** ThamizhiMorph FST analysis (sandhi-aware) decoded into the six பகுபத உறுப்புகள்.
- **Grammar:** ThamizhiMorph POS + case tag, explained through the classical rules.

**Reproducibility:** every source is **pinned to a version / commit / data-refresh date** and recorded in
each `sources[].retrieved`. Reproducibility is part of authenticity — prefer the locally-runnable, pinnable
option over a live web call wherever both exist.

---

## 4. Tool surface

One focused tool per concern (so an agent can compose), plus one workflow tool that returns the whole object.
All tools are **read-only**: `readOnlyHint: true`, `openWorldHint: true` (results depend on external
linguistic data), `destructiveHint: false`. Every tool reports provenance and reports gaps honestly.

**v1 — build these:**

- [x] **`analyze_word`** *(workflow / main entry point)* — `{ word, include? }` → the full
  `ThamizhWordAnalysis` object. Composes the focused tools and merges provenance; returns per-section gaps
  rather than failing whole if one source misses. *This matches the dominant agent intent ("tell me
  everything about this word") in one call.*
- [x] **`classify_origin`** — `{ word }` → `{ class, is_native, borrowed_from, adaptation, evidence,
  confidence, alternatives, sources }`. Returns competing claims in `alternatives` when authorities disagree.
- [x] **`get_root`** — `{ word }` → `{ lemma, all_analyses[], sources }`. Keeps **all** analyses when
  ambiguous (ThamizhiMorph primary; open-tamil stemmer fallback).
- [x] **`get_meaning`** — `{ word, lang? }` → `{ senses[{gloss_ta, gloss_en, pos, citation}], sources }`
  (Madras Lexicon primary; AU-KBC WordNet / Cologne OTL cross-check).
- [x] **`explain_formation`** — `{ word }` → `{ word_type, components[], sandhi[], sources }` (FST tags
  decoded into Nannூல் உறுப்புகள்).
- [x] **`explain_grammar`** — `{ word }` → `{ word_class, case?, tense?, person_number_gender?, notes,
  sources }`.

**Optional / later (out of v1 scope, listed so the surface is clear):**

- [ ] `validate_pure_tamil` — `{ word }` → `{ is_pure_tamil, reason, source }` (Thamizhi Validator). Cheap;
  may pull into v1 if origin classification needs it as a sub-call.
- [ ] `generate_forms` — `{ lemma, features }` → surface forms (ThamizhiMorph generator) for
  spell-check / data augmentation.
- [ ] `transliterate` — `{ text, scheme }` for romanized I/O and English-loanword matching.

**Shared conventions (carried into every tool description and the agent system prompt):**

- Every analysis carries a `sources` array; every claim is attributable.
- Source miss → `{ status: "no_entry", source, note }`, an honest gap — never a fabricated value.
- Ambiguous analysis → return all in `alternatives` / `all_analyses`; do not silently disambiguate.

---

## 5. Stack decision

- **Recommendation: Python core, FastMCP, stdio transport for v1.**

- **Why Python:** the entire Tamil-NLP ecosystem this project must ground against is Python or native-binary.
  - **ThamizhiMorph** is a `foma` finite-state transducer queried via `flookup` (callable from any language,
    but its driver, ThamizhiPOSt, and ThamizhiLIP are Python).
  - **open-tamil**, **ThamizhiLIP**, and most analysers/validators ship as Python packages.
  - So the analysis logic *wants* to live in Python — putting the MCP server there too keeps it to one
    language with direct library calls.

- **The tradeoff (your call to make):**
  1. **Python MCP server (FastMCP)** — simplest; one language, direct library calls. **Recommended for v1.**
  2. **TypeScript MCP SDK calling a Python analysis service** — choose only if there's a strong reason to
     prefer the TS SDK (a specific deployment target). It adds an inter-process boundary for **no linguistic
     benefit** at this stage.

- **Decision (stated, change if you disagree):** **Python + FastMCP, stdio transport.** Stdio because v1 is
  a local tool an agent launches as a subprocess; switch to streamable HTTP only when you need a remote/hosted
  deployment. The build mechanics (SDK setup, tool registration, schemas, Inspector, eval harness) come from
  the **`mcp-builder`** skill in Phase 3 — this blueprint stays on the domain layer.

---

## 6. Architecture sketch

```
                ┌──────────────────────────── MCP tool layer (FastMCP) ────────────────────────────┐
   Agent ──▶    │ analyze_word · classify_origin · get_root · get_meaning · explain_formation ·     │
                │ explain_grammar    (read-only; provenance + honest-gap contract on every tool)     │
                └───────────────────────────────────┬──────────────────────────────────────────────┘
                                                     │
                       ┌─────────────────────────────▼─────────────────────────────┐
                       │  Analysis core (one well-tested module — NOT in prompts)   │
                       │  • normalizer (open-tamil get_letters / Nisaba)            │
                       │  • FST-tag → பகுபத உறுப்பு decoder (Nannூல்)                │
                       │  • வேற்றுமை / case-tag mapper, PNG + tense decoder          │
                       │  • origin classifier (4-way + loanword) w/ alternatives    │
                       │  • provenance + gap assembler → ThamizhWordAnalysis object │
                       └───────┬───────────┬───────────┬───────────┬───────────────┘
                               │           │           │           │
                    ┌──────────▼─┐ ┌───────▼────┐ ┌────▼──────┐ ┌──▼───────────────┐
                    │ ThamizhiMorph│ │ Madras Lex │ │ Validator │ │ loanword/etym    │
                    │ (foma/flookup)│ │ (offline)  │ │           │ │ datasets         │
                    └──────────────┘ └────────────┘ └───────────┘ └──────────────────┘
                       each wrapped in a small ADAPTER with a uniform interface:
                       input = normalized Tamil word; output = fields it can fill + its own provenance
```

- **Adapters:** one per source, uniform interface (in: a normalized Tamil word; out: the fields it can fill +
  its provenance). Adding/swapping a source is a contained change.
- **Analysis core lives in code, not prompts.** The FST-tag→உறுப்பு decoder and the case/tense/PNG mappers
  are the project's linguistic IP; re-deriving them on every run is wasted work and a correctness risk, so
  they are one well-tested module.
- **Normalization runs first, always.** Tamil letters are multi-codepoint; bad normalization corrupts every
  downstream lookup.
- **Version pinning** at the adapter boundary feeds `sources[].retrieved`.

---

## 7. Evaluation plan (Phase 4)

Goal: prove an LLM *using the server* gives authentic, sourced answers — and an honest gap where no source
exists. Fixtures are chosen to exercise each concern; expected analyses are hand-verified against the sources
before locking (per `references/tamil-grammar.md` §6).

| Fixture | Why it's in the set | Hand-verified expected (origin · root · formation · grammar) |
|---|---|---|
| **மரம்** | clearly native, simple | origin இயற்சொல் (native) · root மரம் · `பகாப்பதம்` (simple) · பெயர்ச்சொல், எழுவாய்/nominative |
| **மரத்தில்** | inflected, needs sandhi-aware split + case ambiguity | origin இயற்சொல் · root மரம் · `பகுபதம்`: பகுதி மரம் + சாரியை அத்து (விகாரம்: ம்→ change) + விகுதி இல் · grammar **ஏழாம் வேற்றுமை (locative/இடப்பொருள்), ஒருமை — also readable as ஐந்தாம் (ablative); return both** |
| **புத்தகம்** | Sanskrit வடசொல் | origin **வடசொல்**, Sanskrit *pustaka*, adaptation தற்பவம் · meaning "book" (cite lexicon) · formation: treat as `பகாப்பதம்` in Tamil; flag decomposition belongs to source language · பெயர்ச்சொல் |
| **கம்ப்யூட்டர்** | modern English loanword, outside classical scheme | origin **loanword, source English**; say it's outside the four-way scheme · meaning "computer" · formation: not analyzable by Tamil morphology (transliterated borrowing) · பெயர்ச்சொல் |
| **ஆசிரியர்** *(disputed-origin pick)* | contested native-vs-வடசொல் case | return **competing origin claims with evidence** in `origin.alternatives`; do not adjudicate — this fixture specifically tests "name uncertainty" |

- **Pass criterion (per fixture):** the agent's answer **matches the verified analysis AND cites the right
  source**; where no source covers a field, it returns an honest gap with **no fabrication**. The
  no-fabrication check is the single most important behaviour to test.
- **Negative fixture:** at least one nonsense / out-of-vocabulary string to confirm the server returns gaps
  rather than a fluent invented analysis.
- **Harness:** use `mcp-builder`'s evaluation guide in Phase 4.

---

## 8. Open questions & risks

1. **Madras Tamil Lexicon has no official REST API.** *Decision for sign-off:* plan for an **offline copy of
   the digitized data** (pinnable, reproducible, no live-scrape fragility) with a queried web interface as
   fallback. Confirm redistribution terms before bundling data. — *needs your go/no-go.*
2. **Origin is genuinely contested for some words.** The server **reports competing claims and their
   evidence; it does not adjudicate.** `origin.alternatives` is a first-class field, not an edge case.
3. **ThamizhiMorph returns multiple analyses** for one surface form. **Keep all of them**; disambiguation is
   a downstream concern, not the server's job.
4. **Licence verification** still owed for open-tamil (MIT/GPL — check repo) and the loanword datasets
   (per-dataset) before bundling anything. Apache-2.0 for ThamizhiMorph is confirmed.
5. **Modern non-English loanwords** (Perso-Arabic, Hindi/Urdu, Telugu) are best-effort in v1 — flag the
   limit in tool descriptions so the agent doesn't over-claim.
6. **`foma`/`flookup` runtime dependency** is a native binary — confirm it builds/runs on the deployment
   target early in Phase 1 (it's the linchpin of root, formation, and grammar).

---

## 9. Milestones

1. **Blueprint signed off** (Phase 0 — *this document*) →
2. **Sources reachable** (Phase 1): ThamizhiMorph FST runs locally; lexicon access decided; loanword data +
   validator integrated; each source pinned with a recorded failure mode →
3. **Tools designed** (Phase 2): finalized tool list + schemas, adapted to the sources actually locked →
4. **Server runs locally** (Phase 3): FastMCP server, adapters + analysis core, verified in MCP Inspector →
5. **Eval set passes** (Phase 4): the five fixtures + negative case pass on match-and-cite, with honest gaps
   and no fabrication.

---

## 10. Sign-off

| Item | Decision in this blueprint | Approve? |
|---|---|---|
| Scope = single-word, 4 concerns, Sanskrit+English first-class | Section 1 | ☐ |
| Output contract frozen (`word_analysis_schema.json`) | Section 2 | ☐ |
| Source-to-field map + failure modes | Section 3 | ☐ |
| Tool surface (6 v1 tools, optional 3 later) | Section 4 | ☐ |
| Stack = Python + FastMCP, stdio | Section 5 | ☐ |
| Lexicon access = offline copy (pending terms check) | Risk #1 | ☐ |

> Approve the rows above (or redline any) and Phase 1 begins: making the grounding sources concretely
> reachable. No code is written before this sign-off.
