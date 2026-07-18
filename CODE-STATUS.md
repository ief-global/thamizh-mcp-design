# CODE-STATUS — what's live in the `thamizh-mcp` repo

> Written from the **code side** (Claude Code on minnaham) so the design side (Cowork / Fable)
> can see the real state of the server without reading the repo. Mirror of the repo's `CLAUDE.md`
> "Current state". Last updated **2026-07-18**. Authoritative code lives at
> `github.com/ief-admin/thamizh-mcp` (`main`); this doc is a read-across, not a spec.

## Tool surface — v1 core COMPLETE (8 of 8)

All blueprint §6 core tools are built, tested, and merged to `main`:

| Tool | Status | Notes |
|---|---|---|
| `analyze_word` | ✅ | workflow tool; composes the rest, per-section gaps |
| `classify_origin` | ✅ | see divergence #1 below |
| `get_root` | ✅ | FST lemma/POS, keeps all analyses |
| `get_meaning` | ✅ | store → Tamil Wiktionary pull, provenance-tagged |
| `suggest_native_equivalent` | ✅ | I2PT, attested-only; gated on origin |
| `explain_formation` | ✅ | பகுபத உறுப்பு decode (2026-07-18) |
| `explain_grammar` | ✅ | word class + வேற்றுமை + verb tense/முற்று |
| `enrich_word` | ✅ | forces pull→write-back; non-readOnly |
| `refresh_sources` | ✅ | batch force-refresh (words / stale sweep); non-readOnly (2026-07-18) |

**9 tools live.** Not yet built (blueprint §6): optional `validate_pure_tamil`, `generate_forms`,
`transliterate`. **87 tests pass** (85 without foma). Transaction logging on by default (see #4 below).

## Engine shape (matches blueprint §8)

Plain-Python `Engine` (`core/engine.py`) with a uniform `SourceAdapter` interface; thin MCP head
(`server.py`). Anchors: ThamizhiMorph FST (foma). Evolving: Tamil Wiktionary + I2PT lists, cached
in the SQLite `KnowledgeStore` with per-claim provenance. Linguistic rules live in `core/decoder.py`
(POS, வேற்றுமை, formation) and `core/classifier.py` (origin) — decoded once, never re-derived by the model.

## Divergences the design side should know about

1. **`classify_origin` is a rule-based *subset* of the §4/D-002 design.** Built from open-tamil
   Grantha detection + Tholkappiyam முதல்/இறுதி எழுத்து phonotactics + FST native-parse + I2PT
   attestation. It does **not** yet use the **Thamizhi Word Validator** or a **loanword dataset**
   (neither is installed/vendored). Consequence: many real borrowings that carry no orthographic
   marker return an honest `unknown` (e.g. புத்தகம் Sanskrit-but-pure-script, கம்ப்யூட்டர்). Wiring
   the Validator + a loanword list is the clear next lift for origin accuracy.
2. **Formation `விகாரம்/சந்தி` is deliberately conservative.** The FST hands over verb tense/PNG
   surface forms and noun case tags, but NOT the exact join changes. So joins are named only where a
   confident classical rule applies (-அம் noun ம்→த் திரிதல்; ம்→ங் before கள்; dative க்கு doubling).
   Harder joins (e.g. verb root வா→வந்) are left **unnamed**, per the "no invented split" rule —
   not wrong, just honest-minimal vs the tamil-grammar.md worked examples.
3. **Schema extended:** `FormationComponent` and `SandhiEvent` gained an optional `authority`
   field (Nannūl for six-part labels, Tholkappiyam for sandhi) to match `tool-design.md`.
4. ~~Transaction logging is NOT built yet.~~ **DONE (2026-07-18, PR #8).** Every resolved
   `analyze()` is logged to a `transactions` table (full WordAnalysis + tool label + `eval_fixture`
   flag), on by default, non-fatal. `data/eval_fixtures.json` is the contamination registry —
   **`thamizh-data-curation`/`thamizh-eval` should read/extend it**, and read `transactions` directly
   for extraction (step 1 of the curation pipeline). `KnowledgeStore.transaction_stats()` gives
   growth metrics. This captures the segmentation/origin gold the `claims` cache never held.

## Anchors / data locked

ThamizhiMorph FSTs @ `adbacced` + I2PT 2,063 mappings @ `f734646` (pins in `data/PINS.md`). Still
OPEN (network-open session): Madras Lexicon + TVA கலைச்சொல் offline snapshots.

## Recorded product-quality goal — full six-part sandhi decoder

The v1 formation decoder ships the **detect-but-don't-overclaim** option (join named only where a
confident classical rule fires). Saran has recorded the **fuller option as a near/long-term goal**:
a proper Tholkappiyam புணரியல் sandhi engine that names every விகாரம்/சந்தி (தோன்றல்/திரிதல்/கெடுதல்)
for all cases — including verb-root changes like வா→வந் — so the product stands on its own linguistic
merit rather than the honest-minimal v1. Not scheduled yet; captured so it isn't lost.

## Org / repos

All repos now live under the **`ief-global`** GitHub org (was `ief-admin`, a user, until 2026-07-18).
`ief-admin` is now an admin user *inside* `ief-global`; `ssaravanan3` (Saran's personal account) is an
additional org owner. Remotes use `git@github.com:ief-global/<repo>.git`. This design folder is its own
private repo `ief-global/thamizh-mcp-design`; the code is `ief-global/thamizh-mcp`. Keep them separate —
never nest, never commit design docs into the public code repo.

## Workflow (so history stays clean)

Build on `develop` → PR to `main` (PR title = commit subject) → Saran **squash-merges**. After each
merge, `develop` is realigned onto `main`. No AI attribution in commits/PRs. Identity: Saran
Saravanan <saravanan3@duck.com> / GitHub `ssaravanan3`.

## Agreed direction (2026-07-18)

Two tracks, run together, one item at a time:
- **Low-hanging fruit first (now):** transaction logging (gold-corpus flywheel, #4), `refresh_sources`,
  then lifting `classify_origin` with the Thamizhi Validator + a loanword dataset (#1).
- **Flagship high-value (start immediately):** Phase-4 **morphological-lift eval** (`thamizh-eval`,
  D-005) — bare-LLM vs LLM+MCP on ILAKKANAM-style questions, per category/grade. This is what proves
  the product matters.

Also still OPEN (network session): Madras Lexicon + TVA கலைச்சொல் offline snapshots.
