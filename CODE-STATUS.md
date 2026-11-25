# CODE-STATUS — what's live in the `thamizh-mcp` repo

> Read-across from the **code side** so the design side can see the real state of the server without
> reading the repo. Mirror of the code repo's `CLAUDE.md` "Current state" — if the two disagree, the
> code repo wins and this needs updating. Last updated **2026-11-24**.
> Code: `github.com/ief-global/thamizh-mcp` (`main`). **440 tests pass** (the FST tests skip without live foma). CI runs them on every PR; `ci-ok` is the required check on `main`.

## Shape

Nine MCP tools + web/REST + CLI over **one engine** (blueprint §8 — the web head needed zero engine
changes, which validated that design).

| Layer | What |
|---|---|
| Anchors | ThamizhiMorph FST (foma) · curated verb paradigms · pinned Tholkappiyam + Nannūl, **read at RUNTIME so claims QUOTE their நூற்பா** (D-018) · cited grammar rule tables |
| Evolving | ta.wiktionary (meanings) · **en.wiktionary (etymology → source language)** · **S2PT** (native equivalents — renamed from "I2PT"; licence UNSTATED, D-017) |
| Store | zero-config SQLite, per-claim provenance + `transactions` gold log |
| Registry | **`data/sources.json` (D-017)** — every source's evidential GRADE (A–D) and legal REDISTRIBUTION MODE as independent axes; the grade is stamped on every `SourceRef` and shown in the app |

**Tools:** `analyze_word` `classify_origin` `get_root` `get_meaning` `suggest_native_equivalent`
`enrich_word` `explain_formation` `explain_grammar` `refresh_sources`. Only optional
`validate_pure_tamil`/`generate_forms`/`transliterate` remain from blueprint §6.

Live at **http://minnaham:8080** (systemd, 24/7). Terminals cannot shape Tamil — use the browser.

## Measured quality — 108-word everyday sweep (re-measured 2026-11-24)

`uv run python scripts/quality_sweep.py` in the code repo. This is the only honest read on quality;
the expected labels inside it are **assessments, not authority**, and need Saran's eye.

| | 2026-08-02 start | Session 2 end | Session 3 | 2026-08-11 | 2026-11-24 | **2026-11-25** |
|---|---|---|---|---|---|---|
| **Origin** correct | 59 | 82 | 87 | 94 | 92 | **92** |
| honest `unknown` | 30 | 23 | 18 | 11 | 12 | **12** |
| **wrong** | 17 | 1 | 1 | 1 | 2 | **2** |
| **Formation** decoded | — | 26/30 | 26/30 | 26/29 in-scope ⚠️ | 26/29 in-scope ⚠️ | **26/29 in-scope, all rebuild** |

The 2026-11-24 column is after ruling (e); measured before it, the same day gave 91 / 12 / 3.

**The 2026-11-24 drop is upstream drift, not a code change.** No code that affects analysis merged
between the two measurements (#30 touched docs only). en.wiktionary, our evolving etymology source,
was edited under three sweep words:

| Word | Upstream edit | What we now return |
|---|---|---|
| மனிதன் | 2026-08-25: etymology now `{{bor+\|ta\|pra\|…}}`, i.e. borrowed from **Prakrit**, no longer Sanskrit | **RESOLVED by ruling (e), D-022:** பிராகிருதம் is not வடசொல் and is now its own class. மனிதன் → பிராகிருதம். |
| காலம் | 2026-11-10: Sanskrit origin rewritten in the new `{{ety\|…}}` / `{{af\|ta\|sa:काल\|-அம்}}` style | `இயற்சொல்` 0.60. Our parser reads only `bor`/`inh`/`der`, sees no relation, and falls through to native-by-default. **A parser gap, ours to fix.** |
| கொடு | etymology now states Kannada/Malayalam cognates only, no `inh` template | honest `unknown`. Defensible: a cognate is not a stated inheritance. |

This is exactly the risk the evolving tier carries, and why the sweep is re-run rather than trusted.

**From 2026-11-25 the formation figure counts a word only if its split rebuilds the word (D-023,
D-025).** Before that, a word counted when it yielded more than one component, and five past-tense
forms passed with a letter missing (`வந்தான்` as `வா + த் + ஆன்`, no ந்). The round-trip engine now
finds that ந் and names it: `வா(வ) + ந்(இடைநிலை) + த்(இடைநிலை) + ஆன்`. Since D-028 that ந் and the
strong-verb doubled consonant are both இடைநிலை எழுத்து on நச்சினார்க்கினியர்'s உரை, superseding the TVA
course book's சந்தி (D-026). All 26 have every step cited, through a நூற்பா or a commentary quoted as
read on the page; none is parked. Since D-030 a verb's stem change comes from one rule catalogue tried
on every verb, not from a list, so சொன்னான் is cited and verbs outside the sweep (கொன்றான், சென்றான்,
நீண்டது, வாழ்ந்தான்) rebuild too.

The 2026-08-11 re-measure was taken after the D-017 registry landed and is **unchanged** from
2026-08-08 — by design. The registry's confidence caps are ceilings that all currently sit at or
above what the classifier emits, so they bind nothing yet; they start binding the day someone
raises a confidence past what its source can support.

16 of the 108 words now carry a **per-sense** origin breakdown (`origin.senses[]`).

Formation gaps: `கொடுக்க` `கொடுத்து` `கொடுக்கும்` (non-finite — **blocked on a pending ruling**, see
`thamizh-mcp/data/grammar/concept_map.json` → `concepts.விகாரம்.inferred`). `வீட்டிற்கு` is **out of
scope** for பகுபத உறுப்பிலக்கணம் — the புணர்ச்சி engine owns it (Saran's ruling), hence 26/**29**.

## What changed in Session 2 (2026-08-02 → 08-05)

**D-011 CLOSED.** Tholkappiyam (1486 நூற்பா; **1602 since the 2026-11-24 re-pin, D-024**) and Nannūl (462) pinned from **Project Madurai** as
version-locked, verse-addressable artifacts in `data/classical/`, checksummed in `data/PINS.md`,
rebuildable via `scripts/build_classical.py --verify`. They ship publicly because Project Madurai
grants distribution with its header intact — unlike the TVA books.

**D-014 CLOSED.** Five cited grammar tables (இடைநிலை, விகுதி, சாரியை, வேற்றுமை உருபு, விகாரம்), each
with a `source_priority` block; all eight decoder audit findings fixed. `tests/test_citations.py`
enforces that every cited நூற்பா resolves in the pinned texts.

**Origin rebuilt (D-015).** See the decision log — the short version is that orthography can prove a
word is *not native* but never *which language*, and en.wiktionary now supplies the source.

## What changed in Session 3 (2026-08-05)

**D-015 CLOSED — origin is modelled per SENSE.** `Origin.senses[]` mirrors the existing
`Meaning.senses`; the etymology parser reads each `===Etymology N===` block on its own instead of
ranking templates across the whole Tamil section (the defect that picked `bor` over `inh`). Sense
labels come off the page machine-readably. **Saran's ruling: the Tamil sense leads at headword
level for EVERY source language** (Sanskrit, English, Urdu, Marathi, Telugu) — a Thamizh server
points the reader at the Tamil word first — with the borrowed sense always cited in the evidence,
in `alternatives`, and in full in `senses[]`. A borrowed sense also hands back its Tamil word via
`SenseOrigin.tamil_alternatives` (கார் 'car' → மகிழுந்து), filtered so a synonym that is itself
borrowed (ரோடு) cannot surface. Deliberately NOT called `native_equivalents`: orthography proves
non-nativeness only, so naturalized Sanskrit still passes — the loanword lexicon is the real fix.

Two defects it exposed, both fixed: the native short-circuit dropped the equivalents of a
homograph's borrowed sense, and `force_refresh` never reached the etymology cache (so
`refresh_sources` did nothing for origin).

## Standing traps (all cost real time to find)

- **Never take a நூற்பா number from a secondary source.** TVA's 336/319/136 are **337/320/137** in
  the pinned edition. Three shipped tables were wrong before `data/classical/` existed.
- **Tholkappiyam நூற்பா RESTART per இயல்** — cite அதிகாரம் › இயல் › நூற்பா. Nannūl is continuous 1–462.
- **Grantha marks a non-native SOUND, not Sanskrit.** ஜன்னல் is Portuguese, பஸ் is English.
- **Homographs differ in origin by sense** — கால் = leg (native) *and* time (Sanskrit). Origin is
  per-SENSE (`origin.senses[]`); the headword leads with the Tamil sense, borrowed senses are
  cited, never suppressed. Ranking etymology templates across a whole page re-creates the bug.
- **A cached etymology is a PARSE, not raw source.** An adapter upgrade leaves old-shape dicts
  served forever unless `force_refresh` reaches the etymology cache — it did not, until Session 3.
- The quality sweep **must** use `default_engine()`; a hand-built `Engine` omits the curated-paradigm
  fallback and 12 covered verbs look like FST gaps.

## Not done

Non-finite FST coverage · full புணர்ச்சி sandhi engine · storage backend abstraction (D-013) ·
Phase-4 eval re-measure (D-005) · one catalogued stem change not applied (முதல் நீளல்; D-030) ·
`{{af}}`/`{{ety}}` etymology templates not yet parsed · version still `0.1.0`, no release rung shipped.
