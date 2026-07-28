# THAMIZH MCP — Decision Log

Append-only record of resolved project decisions. Newest entries at the bottom. Never rewrite a past entry;
if a decision changes, add a new entry that **supersedes** it and update the old entry's Status line only.

**Entry format:** `ID · date · decision` → rationale · status · links.

---

## D-000 · pre-existing (recorded 2026-07-04) · Standing commitments carried in from the skill

These were settled before the log existed; recorded here so the log is complete from day one.

- **Stack: Python core via FastMCP.** The entire Tamil-NLP ecosystem to ground against (ThamizhiMorph/foma,
  open-tamil, ThamizhiLIP, Stanza) is Python or native-binary, so the analysis logic and the MCP server sit
  in one process — no IPC boundary. TypeScript-calling-a-Python-service was considered and rejected absent a
  hard external constraint. *Status: settled.*
- **Tholkappiyam first, Nannūl fallback (grammar).** தொல்காப்பியம் is the golden authority for objectives
  1/3/4; Nannūl only where Tholkappiyam does not enumerate the point (chiefly the six-part பகுபதம்). Every
  grammar claim records which authority it used. *Status: settled.*
- **Suggest only attested native equivalents (objective 5).** Never invent a coinage; recommend an
  equivalent only when a கலைச்சொல்/தனித்தமிழ் authority attests it, else return an honest gap. Authority here
  is the terminology tradition, not Tholkappiyam. *Status: settled.*
- **Single-word analysis is v1 scope.** Phrases/sentences and generation are later. *Status: settled for v1.*
- **Self-enriching, two-tier sources.** Anchors (version-pinned) vs evolving (pulled at query time, cached
  with provenance + retrieval date). No hand-maintained dictionary. *Status: settled.*

---

## D-001 · 2026-07-04 · Wrap ThamizhiMorph; do not build a new morphological analyser

The #1 grounding need is a morphological analyser, but ThamizhiMorph already fills it — a rule-based foma FST
that returns lemma + POS + inflection and, uniquely among maintained Tamil analysers, decodes **sandhi**.

Rationale: rebuilding it would duplicate mature, Apache-2.0 research for no gain. The server's value is the
*orchestration* layer above it, which ThamizhiMorph does not attempt. The ThamizhiMorph team did not build an
MCP server because (a) the Thamizhi work is 2018–2021 research and MCP did not exist until Nov 2024, (b) an
MCP server is an integration/agent layer, not a linguistics resource, and (c) ThamizhiMorph is morphology-only.

*Status: active.* *Links: `references/tool-design.md` → "Reused Tamil-NLP components → MCP tool map".*

## D-002 · 2026-07-04 · Reuse the wider Thamizhi suite for specific fields

Beyond ThamizhiMorph: use **ThamizhiPOSt / ThamizhiLIP** for contextual POS/UD disambiguation (when input
exceeds a bare word), and the **Thamizhi Word Validator** as the native-vs-borrowed signal into
`classify_origin`. open-tamil (Ezhil LF, not the Thamizhi team) covers normalization, a stemmer fallback, and
transliteration.

Rationale: each maps cleanly to a tool already in the surface; reuse beats re-implementation for a
low-resource language where these are the state of the art.

*Status: active.* *Links: `references/tool-design.md` component map; `references/sources.md` §1.*

## D-003 · 2026-07-04 · Positioning — "first Tamil சொல்-analysis MCP server," stated precisely

A prior-art scan found a rich Tamil-NLP ecosystem (ThamizhiMorph, open-tamil, pytamil, Stanza models) and
generic language/translation MCP servers, but no MCP server doing Tamil word-grammar analysis.

Rationale/guardrail: claim only "plausibly the first Tamil **சொல்-analysis MCP server**," not "first Tamil
NLP tooling." Absence of a search hit is not proof; state the claim with that caveat in any public framing.

*Status: active.* *Links: blueprint positioning section (to be written in Phase 0).*

## D-004 · 2026-07-10 · Skill suite: three sibling skills instead of growing the builder

Created `thamizh-eval`, `thamizh-data-curation`, `thamizh-release` as separate skills; `thamizh-mcp-builder`
(bumped v6) stays the build/domain layer.

Rationale: the improvement-loop routing rule prefers enriching the existing skill, but these three are
genuinely separate capabilities with their own trigger vocabularies (benchmark/lift · export/publish data ·
release/deploy/list) and would bloat + confuse the builder's trigger if folded in. Each description carries
explicit negative boundaries against its siblings.

*Status: active.* *Links: skill folders in project root; `TAMIL-HIGH-RESOURCE-ROADMAP.md` skill map.*

## D-005 · 2026-07-10 · Morphological lift is the v1 north-star product metric

lift = SP(model+thamizh-mcp) − SP(model alone) on ILAKKANAM-style Tamil linguistics questions, reported per
linguistic category (L1–L5, F) and grade band — never as one blended number. Claude-first harness
(`claude -p`), model-agnostic storage. Fixtures self-built (ILAKKANAM dataset not public as of 2026-07-10;
re-check before eval runs). Fixture words flagged `eval_fixture=1` in the store and excluded from any
published dataset.

Rationale: ILAKKANAM (arXiv 2511.12387) shows frontier models score 71–80% and decline with complexity,
driven by exposure not understanding — the exact gap the server grounds. Server regression evals (builder
Phase 4) prove tools are honest; lift proves the product matters. Both are needed; they stay separate.

*Status: active.* *Links: `thamizh-eval/SKILL.md`; blueprint §12 eval addendum.*

## D-006 · 2026-07-10 · Tamil SLM is long-term; near-term = MCP + eval + data accumulation

The SLM (grammar-first tokenizer, continued pretraining, hybrid serving) is explicitly NOT being solutioned
now — heavy prerequisites (corpus scale, compute, funding). Near-term work is chosen so its by-products ARE
the prerequisites: transaction logging → gold corpus; eval infra → benchmark; adoption → community. Revisit
when the gold corpus is ≥ ~100k verified records. No SLM skill exists by design; don't create one yet.

Rationale: `TAMIL-HIGH-RESOURCE-ROADMAP.md` (evidence + sequencing); Saran's directive 2026-07-10 (mark
long-term, don't work it).

*Status: active.* *Links: `TAMIL-HIGH-RESOURCE-ROADMAP.md`; blueprint §12.*

## D-007 · 2026-07-18 · OPEN — how the gold corpus aggregates centrally (community contribution path)

Transaction logging (server PR #8) accumulates gold data in **each running instance's local SQLite
DB**, which is gitignored and machine-local by design (CC BY-SA cache can't ship in the Apache-2.0
repo; the store is regenerable; avoids binary-in-git merge conflicts). **Consequence:** a local /
community install accumulates only *its own* usage — there is no mechanism to pool that gold into a
shared corpus. Central accumulation today = **only the hosted reference instance** (Cloud Run,
medium-term), whose DB sees all its users' queries; the durable, forward-carried artifact = the
**versioned Hugging Face datasets** exported by `thamizh-data-curation`. Git carries code + anchors;
HF carries the grown corpus. (See CODE-STATUS.md → transaction logging.)

**Open question (decide before any "contribute your data" feature):** if we want community installs to
feed the shared corpus — accelerating the SLM's training data — we need an *explicit, opt-in, consented*
contribution path. Unresolved sub-decisions: consent + notice model; query-text/PII privacy review;
per-record license compatibility (evolving-tier text vs derived structured facts); server-side dedup +
cross-check verification of contributed records; provenance/attribution of contributors; abuse/poisoning
guardrails. Not needed for v1 (local capture + hosted accumulation suffice); flag so it isn't lost.

*Status: OPEN.* *Revisit when the hosted instance is live and/or community adoption creates pressure to
pool data — decide the consent + licensing model first.* *Links: blueprint §12; `thamizh-data-curation`
SKILL.md (contamination guard, license filter); `distribution-roadmap.md`; server `data/eval_fixtures.json`.*

## D-008 · 2026-07-18 · Source-strategy revision: keep I2PT; adopt Aalamaram for what it is

I2PT is stale (small, inactive) but stays — pinned, attested, unique at its one job (Indic→pure-Tamil
mappings). Equivalents coverage grows via TVA கலைச்சொல் snapshots + Wiktionary {{சொல்வளம்N}} mining, not by
replacing I2PT. **Aalamaram** (WILDRE@LREC 2024; ~10k-sentence Tamil treebank: POS/NER/morphology/deps;
Sarveswaran co-author) is ADOPTED as a new anchor-tier source for morphology cross-checks, L3/L4 eval
fixtures, phrase-level v2, and SLM corpus.

Correction recorded: the proposal "replace I2PT with Aalamaram" conflated data types — Aalamaram is a
treebank, not an equivalents dataset; the acl-org/acl-anthology URL/license belongs to the ACL Anthology
site, not to Aalamaram's data. **Blocking pre-step:** locate Aalamaram's actual distribution + verify its
license (not on HF; no public repo found from the sandbox) — network-open job, batched with Madras/TVA.

*Status: active (adoption conditional on license).* *Links: DESIGN.md §4; sources.md (entry added).*

## D-009 · 2026-07-18 · Hugging Face org `ief-global`: datasets + Spaces demo

Create hf.co/ief-global. GitHub carries code + pinned anchors + design; HF carries the versioned curated
datasets (gold/silver/disputed) and a Spaces demo that calls the Cloud Run API (no second backend). Survey
2026-07-18: HF has NO Tamil morphological-segmentation gold, NO loanword→equivalent dataset, NO origin-label
dataset — our three exports are first-movers. Publish dataset v0 near-term to lock namespace + card
discipline. NOT adopted: mirroring third-party models under the org. Long-term the SLM lives here.

*Status: active.* *Links: DESIGN.md §5; thamizh-data-curation SKILL.md; D-007 (central accumulation).*

## D-010 · 2026-07-18 · Operating model formalized: design repo (private) ↔ code repo (public)

Cowork (Fable/high-end) plans/architects/decides in `ief-global/thamizh-mcp-design`; Claude Code implements
in `ief-global/thamizh-mcp`. Sync: CODE-STATUS.md (code→design) · DESIGN.md/blueprint/skills (design→code).
Never nest; design docs never enter the public repo; git only on Saran's boxes; decisions land here before
code. Records the GitHub org move ief-admin (user) → **ief-global** (org) done 2026-07-18. DESIGN.md is the
design repo's top-level doc, superseding TAMIL-HIGH-RESOURCE-ROADMAP.md as program map.

*Status: active.* *Links: DESIGN.md §2; CODE-STATUS.md "Org / repos".*

## D-011 · 2026-07-19 · Verse-level (நூற்பா) grounding for Tholkappiyam/Nannūl citations

Gap identified by Saran: the encoded rule table cites authorities only at **section level** (e.g.
"Tholkappiyam, வேற்றுமையியல்") and no digitized edition of either classical text is pinned as anchor
data — so grammar claims aren't auditable to the exact verse, unlike FST claims (pinned commit).

Decision: **verse-level grounding is now part of the design.** Two steps, to execute during build:
(1) pin a digitized **Tholkappiyam** and **Nannūl** edition as version-locked anchor artifacts in
`data/` (candidate sources: Project Madurai, Tamil Virtual Academy — final gold source chosen at
pinning time, with edition/recension recorded, since editions vary); (2) upgrade the rule table's
`SourceRef`s from section names to **நூற்பா numbers** (keeping the section name for readability:
"தொல்காப்பியம், சொல்லதிகாரம், வேற்றுமையியல், நூற்பா <n>"). Schema impact: SourceRef gains an optional
`verse` field — additive, non-breaking. The LLM chain is unchanged (it still just relays citations);
this hardens what the citation *is*.

Clarification recorded with it: neither the LLM nor the runtime "reads" Tholkappiyam — grounding =
human-encoded rule table (design time) + per-claim citations (runtime). Verse pinning completes that
chain end-to-end.

*Status: active — scheduled, not yet built.* *Links: DESIGN.md §4/§6/§7; tamil-grammar.md source-priority
note; kb sources-provenance + roadmap articles.*

## D-012 · 2026-07-26 · Licensing SETTLED — mixed-licence product, cleared for public serving

Earlier docs framed licensing as an open blocker ("Gate-0 licence audit blocks every public rung";
per-file "verify before redistribution" flags). **Saran, for IEF (project owner), settled this on
2026-07-26: every source we ship is cleared for use INCLUDING the public hosted service.**

- **I2PT** — MIT, openly redistributable (upstream aggregates openly-licensed community lists).
  Cleared. But deliberately **PROVISIONAL**: to be superseded by authenticated gold sources
  (TVA/govt கலைச்சொல் and comparable); the `SourceAdapter` interface makes that a drop-in swap.
- **Tamil Wiktionary** — CC BY-SA, cleared for use *and public serving*, with attribution; the content
  stays CC BY-SA and is never relicensed under Apache-2.0.
- **The model:** a mixed-licence product with **per-source classification**. This works precisely
  because every claim already carries its source — the provenance machinery that makes answers
  auditable also makes licences classifiable per record. Exports ship per-source subsets rather than
  diluting one dataset's licence.
- **`meaning` stays ENABLED in the public app.** Surfacing meanings — including wrong ones — is a
  *purpose* of the public demo: scholars pinpoint errors so the data improves. Disabling it would
  remove the feedback loop that the whole scholar-engagement strategy depends on.
- **Privacy:** a short privacy note goes in the thamizhai GitHub project / site (analyses are logged
  as linguistic data). Relates to D-007, which remains open only for *pooling contributions from other
  installs*, not for the hosted instance's own logging.

Authority in code: **`LICENSING.md` in the thamizh-mcp repo** — written to be the canonical answer so
this is not re-litigated. Stale flags cleared from NOTICE, data/PINS.md, CLAUDE.md, CONTRIBUTING.md,
TESTING-ON-LINUX.md.

Still genuinely open (sourcing tasks, NOT blockers): Madras Lexicon (DSAL) terms · Aalamaram licence
(D-008) · pinning a digitised Tholkappiyam/Nannūl edition for நூற்பா citations (Project Madurai chosen).

*Status: settled.* *Supersedes the Gate-0-as-blocker framing in DESIGN.md §6/§7.* *Links:
`thamizh-mcp/LICENSING.md`; D-007 (data pooling); D-008 (Aalamaram); D-011 (verse citations).*
