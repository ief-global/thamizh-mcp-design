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
`transliterate`. **109 tests pass** (107 without foma). Transaction logging on by default (see #4 below).

## Web/REST head live — 2026-07-26 (blueprint §8 "heads over one engine" now proven)

FastAPI head + browser UI over the **same engine — zero engine changes were needed**, which validates
the one-engine/many-heads design. `GET /` UI · `GET /api/analyze` · `GET /healthz`; network/meaning OFF
by default. **Why:** terminals do not shape Tamil script (vowel signs detach/reorder), so CLI output is
unusable for demos; browsers shape it correctly. Runs 24/7 on minnaham (systemd) at
**http://minnaham:8080** — now the project's main manual-test surface, and every word tested there
feeds the `transactions` gold log. Also fixed a real packaging bug: the Dockerfile installed the empty
transitional `foma-bin`, so the container had **no working FST**.

**This unblocks design items early:** the REST head (DESIGN.md §6 item 7) exists ahead of schedule, and
the public web tool / HF Spaces demo (item 8) now have a working front end to build on.

## FST coverage gaps closed — 2026-07-20 (was the top-priority product gap)

`analyze_word` had been returning `unknown` for many everyday verbs. Cause: the primary FSTs lack those
lemmas / irregular tense stems. Guesser FSTs were rejected — they return **wrong lemmas** (கொடுத் for
கொடு), i.e. confident errors instead of honest gaps. Fix: a curated **ANCHOR** paradigm table
(`data/verb_paradigms.json`), consulted **only on an FST miss**, closed (unlisted → honest gap), same
grounding model as the decoder rule tables (D-011). Coverage on the common-verb sweep: **past 24/24,
present 18/18, future 18/18**. Causative இடைநிலை decode fixed too (செய்வித்தான் → செய்+வி+த்+ஆன்).
Future 3sgn is deliberately excluded — Tamil future neuter `-உம்` is tagged nonfinite by the FST itself.
**Still open:** non-finite forms (கொடுக்க / கொடுத்து / கொடுக்கும்) and more lemmas.

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
public repo `ief-global/thamizh-mcp-design`; the code is `ief-global/thamizh-mcp`. Keep them separate —
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

## Phase-4 eval — smoke run finding (2026-07-18)

The eval harness is built (`thamizh-eval/`: `fixtures/v1.jsonl` — 28 anchor-verified Qs; `assets/run_ab.py`
Claude-first A/B; `assets/mcp.json`). A 6-Q smoke ran end-to-end. **Headline finding — the bottleneck is
tool *invocation*, not tool quality:** under a neutral prompt the model calls the thamizh tools **0% of the
time** even when attached, so spontaneous lift ≈ 0. A wiring probe proves the server returns the *correct*
answer when invoked (`turns:3`, correct `அத்து` on the மரத்தில் split). **Routes a CODE item:** make the MCP
tool descriptions compelling enough that a model reaches for them unprompted. Also: add a "grounded-prompt"
eval arm to measure the achievable ceiling; harden scoring (contains-match). Full report:
`thamizh-eval/results/report-smoke-2026-07-18.md`.

**Update (2026-07-19):** ✅ tool-description fix landed (code PR #10) — re-validation shows the two failing
smoke questions now invoke the tools + answer correctly. Scoring hardened (contains-match for gold ≥3 chars,
fixes short-answer-with-gloss false negatives). **Full 3-run A/B over all 28 fixtures is running now**;
lift report to follow. ✅ D-011 schema part landed (PR #11 — optional `SourceRef.verse`); verse *numbers*
await pinning a digitized edition — **Saran chose Project Madurai** (2026-07-19), batched into the
network-open session (with Madras Lexicon + TVA + Aalamaram). No verse numbers hardcoded from memory.

## ▶ Next direction (agreed 2026-07-26): TESTING-DRIVEN development

Saran is testing the live web app (http://minnaham:8080) and will bring back observed gaps,
clarification questions, and UI tweaks. **Those findings drive the next build** — fix what real use
exposes, rather than working the backlog blind. Design side: expect fix/tweak requests grounded in
actual usage, and treat the web app as the shared reference surface when discussing behaviour.

The Phase-4 eval stays paused; note its achievable ceiling rose with the coverage fixes, so a
re-measure is more meaningful than before. Other queued work is listed under "Agreed direction
(2026-07-18)" above, unchanged.
