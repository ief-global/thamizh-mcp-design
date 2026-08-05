# CODE-STATUS — what's live in the `thamizh-mcp` repo

> Read-across from the **code side** so the design side can see the real state of the server without
> reading the repo. Mirror of the code repo's `CLAUDE.md` "Current state" — if the two disagree, the
> code repo wins and this needs updating. Last updated **2026-08-05**.
> Code: `github.com/ief-global/thamizh-mcp` (`main`). **171 tests pass** (169 without live foma).

## Shape

Nine MCP tools + web/REST + CLI over **one engine** (blueprint §8 — the web head needed zero engine
changes, which validated that design).

| Layer | What |
|---|---|
| Anchors | ThamizhiMorph FST (foma) · curated verb paradigms · pinned Tholkappiyam + Nannūl · cited grammar rule tables |
| Evolving | ta.wiktionary (meanings) · **en.wiktionary (etymology → source language)** · I2PT (native equivalents) |
| Store | zero-config SQLite, per-claim provenance + `transactions` gold log |

**Tools:** `analyze_word` `classify_origin` `get_root` `get_meaning` `suggest_native_equivalent`
`enrich_word` `explain_formation` `explain_grammar` `refresh_sources`. Only optional
`validate_pure_tamil`/`generate_forms`/`transliterate` remain from blueprint §6.

Live at **http://minnaham:8080** (systemd, 24/7). Terminals cannot shape Tamil — use the browser.

## Measured quality — 108-word everyday sweep (2026-08-05)

`uv run python scripts/quality_sweep.py` in the code repo. This is the only honest read on quality;
the expected labels inside it are **assessments, not authority**, and need Saran's eye.

| | 2026-08-02 start | Session 2 end | now |
|---|---|---|---|
| **Origin** correct | 59 | 82 | **87** |
| honest `unknown` | 30 | 23 | **18** |
| **wrong** | 17 | 1 | **1** |
| **Formation** decoded | — | 26/30 | 26/30 |

16 of the 108 words now carry a **per-sense** origin breakdown (`origin.senses[]`).

Formation gaps: `கொடுக்க` `கொடுத்து` `கொடுக்கும்` (non-finite) and `வீட்டிற்கு` (noun dative).

## What changed in Session 2 (2026-08-02 → 08-05)

**D-011 CLOSED.** Tholkappiyam (1486 நூற்பா) and Nannūl (462) pinned from **Project Madurai** as
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
Phase-4 eval re-measure (D-005) · **no CI yet** (`.github/workflows/` absent) · version still `0.1.0`,
no release rung shipped.
