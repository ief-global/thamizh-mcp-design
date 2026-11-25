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

### Update — 2026-08-02 · Tholkappiyam edition PINNED; verse-level citation is live

**Edition pinned: Project Madurai**, chosen for the community validation effort behind its texts.

| அதிகாரம் | URL |
|---|---|
| எழுத்ததிகாரம் | https://tamilnation.org/literature/grammar/mp100a |
| சொல்லதிகாரம் | https://tamilnation.org/literature/grammar/mp100b |
| பொருளதிகாரம் | https://tamilnation.org/literature/grammar/mp100c |

Attribution is required and recorded in `sources/classical/README.md` (© Project Madurai 1999-2001;
etext Dr. K. Kalyanasundaram; proof-reading N. D. Logasundaram). We cite verses and credit the project;
we do not redistribute the full text publicly.

**Citation format — நூற்பா numbers RESTART in every இயல்,** so they collide both across அதிகாரம் and
across இயல் within one அதிகாரம். A bare number is unusable. Qualify to the இயல்:
`தொல்காப்பியம், எழுத்ததிகாரம், புணரியல், நூற்பா 7`. Nannūl numbering *is* continuous, so
`நன்னூல், நூற்பா 244` is unambiguous. Nannūl verses arrive via TVA's verbatim quotations, so no
separate Nannūl edition is pinned yet.

**Why this got re-opened:** the first four TVA-derived rule tables cited Nannūl as `authority` for
வேற்றுமை and புணர்ச்சி — topics `tamil-grammar.md` assigns to **Tholkappiyam** — purely because TVA
quotes Nannūl. Design rule #1 had drifted in practice while reading correctly on paper. Fixed at the
source: every `data/grammar/*.json` now carries a **`source_priority`** block naming its governing
authority and why, and the three affected tables were restructured to Tholkappiyam-primary with Nannūl
as a cited `fallback`. A table without `source_priority` is incomplete. See DESIGN.md §4a.

**Substantive finding:** the authorities differ, and the difference is content. Tholkappiyam gives the
third-case உருபு as **ஒடு** alone (வேற்றுமையியல் 12); Nannūl 297 gives ஆல், ஆன், ஒடு, ஓடு. Likewise
Tholkappiyam names the three விகாரம் as `மெய் பிறிது ஆதல் மிகுதல் குன்றல்` (புணரியல் 7) where Nannūl 154
says `தோன்றல், திரிதல், கெடுதல்`. Record both; never collapse one into the other.

### Update — 2026-08-02 (later) · BOTH texts version-locked; TVA renumbering caught

Saran's call: pin **Nannūl** from Project Madurai too, since TVA quotes only the handful of verses
its lessons need and real usage will hit verses outside that set. Project Madurai publishes the
complete work (1–462) as a single page. Both texts are now local artifacts:

`thamizh-mcp/data/classical/{tholkappiyam,nannul}.json` — built by `scripts/build_classical.py`,
raw-byte SHA256 per source in `data/PINS.md`, `--verify` re-derives from upstream to detect drift.
They ship in the **public** repo because Project Madurai grants free distribution with the header
intact; the header and edition credits travel inside each artifact. That licence distinction — not
the content — is why these ship where the TVA books do not (`LICENSING.md`).

**The pinning immediately proved its worth: TVA's Nannūl numbering is unreliable.** Three verse
numbers already written into tables or notes were wrong — இர்/ஈர் is **337** not 336, தெரிநிலை-வினை
is **320** not 319, the 23 வினைப் பகாப்பதம் is **137** not 136. Corrected. This vindicates the
standing rule (never write a verse number from memory *or from a secondary source*) and adds a
mechanism: `tests/test_citations.py` asserts that every நூற்பா cited by any `data/grammar/*.json`
resolves in the pinned artifacts, and that every table declares `source_priority`. The bad-citation
guard was verified by deliberately breaking a citation and watching it fail.

**Upstream data quality, recorded:** the three Tholkappiyam pages declare `charset=windows-1252`
while serving UTF-8, baking 28 U+FFFD into the text; every Tamil-context one is **ஃ** — the only
character that transcode lost — and three are ©. The build repairs this mechanically and records the
counts (25 ஃ, 3 ©); no other substitution is made. Nannūl needed none. Nannūl நூற்பா 73 and 176 are
absent from the upstream etext itself and are recorded as gaps, never reconstructed.

*Status: CLOSED. Both golden sources are local, checksummed, licence-cleared and test-enforced —
no further sourcing work is needed to cite either authority at verse level.* *Links: DESIGN.md
§4a/§6/§7; `sources/classical/README.md`; `thamizh-mcp/data/PINS.md`, `LICENSING.md`,
`scripts/build_classical.py`, `tests/test_citations.py`; D-014 (cited rule tables).*

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

## D-013 · 2026-07-26 · The public app is a separate deliverable from the MCP product

Domain **`thamizh-ai.org`** purchased (Cloudflare, under IEF). Hyphenated over `thamizhai.org`: the
joined form reads as **தமிழை** (accusative of தமிழ்) to native speakers, which buries the "AI" signal;
the hyphen also matches the existing `ief-global.org`. Brand may still be styled **Thamizh-AI / தமிழ்AI**.

**Two things, deliberately separate — do not conflate their requirements:**

| | `thamizh-mcp` (the product others install) | `thamizh-ai.org` (our app) |
|---|---|---|
| How it runs | `uvx` / `pip` / Docker, local, stdio | long-running service, multi-user |
| Data store | **SQLite, zero-config** (a file on first run) | **Postgres** in a container |
| Requires | Python + foma + bundled pinned data | container runtime + Postgres |
| Corpus | the user's own local cache | the shared gold corpus (D-007 accumulation point) |

**Nobody installing `thamizh-mcp` will ever be required to run containers or Postgres.** Zero-config
local install is a feature we protect. Postgres is an **optional backend for server deployments**;
SQLite stays the default. This needs a thin storage abstraction in `store/knowledge.py` (currently
SQLite-coupled: `import sqlite3`, `INSERT OR REPLACE`, `AUTOINCREMENT`) with both backends tested.

**Layers of the app:** browser UI → FastAPI head → the same plain-Python engine → Postgres (growing
data) + pinned anchor data baked into the container image. No queue, no load balancer — it is a small app.

**Hosting:** runs on **minnaham** for now (real disk, no cold starts, foma native). Public access, when
needed, via **Tailscale Funnel** first (Saran also wants to learn it). Cloud vendor deliberately NOT
chosen yet — containerising keeps that door open; decide with real traffic, not credits.

*Status: active.* *Links: `thamizh-mcp-hosting-plan.md` (its Cloud Run recommendation is no longer the
default), D-007 (central accumulation), D-012 (licensing settled).*

## D-014 · 2026-08-02 · Grammar rules are cited DATA tables, normalising FST surface → Nannūl உறுப்பு

**Trigger.** Reviewing the deck, Saran (formal TVA A021 coursework) found வருகிறான் split as
வா + **கிற்** + ஆன். `கிற்` is not a valid நிகழ்கால இடைநிலை — the three valid ones are **கிறு, கின்று,
ஆநின்று**. Correct: வா + **கிறு** + ஆன். Present tense was wrong in every case.

**Root cause — architectural, not a typo.** We conflated ThamizhiMorph's **computational
segmentation** (the surface morph where the string splits) with **பகுபத உறுப்பிலக்கணம்** (the named
grammatical constituent). The decoder already normalised FST tags for POS and வேற்றுமை; இடைநிலை had no
such layer, so a surface morph was emitted as if it were a grammatical label.

**Decision.**
1. **Every FST output passes through a normalisation layer** before it is presented as grammar. The
   FST is an *anchor for morphological analysis*, not an authority on classical grammatical naming.
2. **Grammar rules live in cited JSON tables** (`data/grammar/*.json`), each carrying its `authority`
   (Nannūl/Tholkappiyam), the TVA lesson verified against, `verified_by` and `verified_date`. Encoded
   as data so a Tamil scholar can **audit the linguistics without reading Python** — the same
   provenance discipline we apply to answers, applied to our own rules.
3. **வல்லினம் doubling is சந்தி, not part of the இடைநிலை** (Saran's ruling): படிக்கிறான் =
   படி + க்(சந்தி) + கிறு(இடைநிலை) + ஆன். சந்தி may fall before or after the இடைநிலை.
4. **Unmapped forms pass through unchanged, never guessed** — consistent with the honest-gap rule.

**Source materials.** TVA course PDFs/ePUBs live in the PRIVATE design repo under `sources/tva/`
(structure + citation convention tracked; the documents themselves gitignored pending a redistribution
check). Only derived cited rule tables ship in the public repo — grammar facts are citable
scholarship; redistributing complete Govt-of-Tamil-Nadu textbooks is a separate question.
**Prefer ePUB**: the TVA PDFs embed TAU-Valluvar (pre-Unicode), so extraction yields legacy TSCII/TAB
bytes, not Unicode.

**Known gap (recorded, not fabricated):** strong-verb PAST doubling (படித்தான் = படி + த்[சந்தி] +
த்[இடைநிலை] + ஆன்) is not recoverable from the FST tag, which reports only `past=த்`.

### Outcome — 2026-08-02, second pass

The normalisation layer generalised past இடைநிலை. **Four more cited tables** now sit beside it, each
carrying its நூற்பா: `vikuthi.json` (140 — the closed 37→40 inventory; 336), `sariyai.json` (133, 243,
244 — the seventeen பொதுச் சாரியை), `verrumai_urubu.json` (240–242, 291–303, 315), `vikaram.json`
(153, 154, 157 — the three விகாரம்).

**Auditing every other decoder emission found eight further instances of the same confusion**, which
settles the open question in the Decision above: the இடைநிலை bug was not an isolated typo but the
first symptom found. Full evidence, with live-FST tag surfaces, in `DECODER-AUDIT-D014.md`. Summary:
`euph=` (a சாரியை) dropped entirely, so வந்தனன் loses an உறுப்பு · `கள்` emitted as part of the
விகுதி (நூற்பா 336 gives ஈர்/ஆர் alone; கள் is a modern accretion) · `3pln=அன` is சாரியை அன் + விகுதி
அ, and `3pln` is unmapped · `opt=` (வியங்கோள்) dropped · case உருபு truncated to one form per case ·
சொல்லுருபு (`உடைய`, `இலிருந்து`) displayed as if it were the உருபு · மரம்→மரத்து misnamed திரிதல்
when it is கெடுதல் + தோன்றல் · `SandhiEvent.type` uses a term that is not one of Nannūl's three.

**Source correction:** the எழுத்து course is **C021** (C0211–C0214), not A011. And the rules do not
live where the topic name suggests — **விகுதி and சாரியை are not in A021-sol at all**; C0212 is the
பதவியல் lesson and the authority for பகுபத உறுப்பு. See `sources/README.md`.

**Open, needs Saran's ruling (label unchanged meanwhile):** is causative `வி` an **இடைநிலை** (what we
emit — Nannūl defines இடைநிலை positionally, and வி does sit medially in செய்+வி+த்+ஆன்) or a **விகுதி**
(TVA C0212 §6.1.7 and A0212 both list வி, பி, கு, சு, டு, து, பு, று as பிறவினை **விகுதி**)?

**Second known gap:** the நான்காம் வேற்றுமை நூற்பா is not quoted anywhere in TVA A0211 — recorded as
`verse: null`, never filled from memory.

*Status: active.* *Links: `thamizh-mcp/data/grammar/{idainilai,vikuthi,sariyai,verrumai_urubu,vikaram}.json`;
`DECODER-AUDIT-D014.md`; `sources/README.md`; D-011 (verse citations); D-012 (licensing).*

## D-015 · 2026-08-05 · Origin: orthography proves NON-NATIVENESS, etymology proves PROVENANCE

**Trigger.** A 108-word everyday sweep — the first real measurement of origin quality — found the
classifier wrong on **17 of the 76 words where it committed to an answer**, and 11 of those at its
*highest* confidence (0.9). All one defect: Grantha letters (ஸ ஷ ஜ ஹ ஶ) were read as a Sanskrit
signal, so பஸ், ஸ்கூல், ஹோட்டல், ஆபீஸ், நர்ஸ், ஸ்டேஷன், கிளாஸ், ஹாஸ்பிட்டல் (English), ஜன்னல்
(Portuguese) and ஜாமீன், ஜில்லா (Urdu) all came back **வடசொல்**.

**The premise was wrong, not the tuning.** Grantha is how Tamil writes sounds its own எழுத்து set
lacks — from *any* language. The diagnostic that made this obvious: the classifier was simultaneously
**over**-calling வடசொல் on Grantha-spelled English and **under**-calling it on naturalised Sanskrit
written without Grantha (புத்தகம், ஆசிரியர், சூரியன் were already `unknown`). One letter set cannot
carry both jobs.

**Decision — separate the two questions.**
1. **Is it native?** Orthography answers this well: Grantha and a முதல் எழுத்து violation both prove
   *not native*. Neither may assert a source language. Both now return "borrowed, source
   undetermined" with வடசொல் and loanword as alternatives.
2. **Which language?** Needs positive evidence. `adapters/etymology.py` reads en.wiktionary's
   machine-readable templates — `{{bor+|ta|pt|janela}}`, `{{inh+|ta|dra-pro|*maran}}`. The inherited
   case matters as much as the borrowed one: it is positive proof a word IS native, which the
   native-by-default branch never had.

**Exception, deliberately kept.** The இறுதி எழுத்து rule still asserts `loanword`. It turns on
morphological *assimilation*, not letters: Sanskrit borrowings are adapted and take Tamil endings
(ரூபம், யோகம், மனிதன்), so a bare vallinam final really is evidence of a non-Sanskrit loan.
Reviewable — if a Sanskrit borrowing keeps a bare vallinam final, it joins the other two.

**Result.** correct 59 → **82**, honest unknown 30 → 23, wrong **17 → 1**.

**Interim cost, recorded honestly.** Fixing the rules *before* the lexicon landed pushed unknowns to
51 of 108 — worse as a product, even though every answer was defensible. Saran's checkpoint caught
this: *"marking a lot of them as unknown will also reduce trust for this product."* **Honesty is a
floor, not a goal.** Removing a wrong answer without adding evidence moves the failure from *wrong*
to *useless*. Sequence the evidence source with the rule fix in future.

**Tiering.** en.wiktionary is `evolving` — evidence, not authority. Crowd-edited and some etymologies
are contested (பசு is given as Sanskrit *paśu* while a Dravidian *pacu* is also argued). Confidence
caps at 0.8, the competing class always stays in `alternatives`, and the citation always travels.
**Madras Tamil Lexicon** (dsal.uchicago.edu) is the intended ANCHOR upgrade — not a replacement for
citing this honestly.

**Two traps found by measuring, not reading.** Both have regression tests.
- **Homographs.** A headword carries one Etymology section *per sense* and they disagree: கால் = leg
  (inherited) AND time (Skt काल); பூ = flower AND earth; சாலை = road (native சால்+ஐ) AND hall
  (Skt शाला); கார் = black (native) AND car (English). Ranking by template strength picks `bor` over
  `inh` every time, so **four core native words were labelled வடசொல் at 0.8** — the kind of error a
  Tamil scholar would never forgive, and it nearly shipped. Now reported as ambiguous.
  `Origin.is_native` became `Optional`: a homograph is neither native nor not.
- **Dravidian sub-family codes.** மழை is `{{inh+|ta|dra-sdo-pro|*maẓay}}`. An enumerated native-code
  list missed that branch and reported the word as *borrowed from a language called "dra-sdo-pro"*.
  Matched by prefix now.

**▶ CLOSED 2026-08-05 (Session 3) — origin is now modelled per SENSE.** Shape (a) from the
options above: `Origin.senses[]`, a new `SenseOrigin` mirroring the existing `Meaning.senses`.
Purely additive, so no existing field changed meaning and no consumer broke.

**The structural half.** The parser read the whole ==Tamil== section at once and ranked templates
across it. That is what picks `bor` over `inh` every time. en.wiktionary actually separates senses
into `===Etymology N===` blocks, so each block is now parsed on its own, and the sense LABEL comes
off the page machine-readably — `{{ety|ta|id=leg|…}}` where present, else the relation template's
gloss (`{{bor|ta|sa|काल|t=time}}`), else the block's first definition line. Measuring against the
real pages showed the data is richer than this entry assumed: கால் has **six** etymology blocks
(leg, canal, forest, wind, time, a conjunction), not two.

**Saran's ruling — the Tamil sense leads.** *"When there is a homograph between Tamil and Sanskrit,
Tamil meaning wins. It's a Thamizh MCP after all. But we'll cite the Sanskrit meaning as well
below."* So the headword class takes the Tamil sense, and the borrowed sense is never suppressed:
it rides in the evidence string, in `alternatives`, and in full in `senses[]`. Confidence 0.7 —
below a clean single-etymology 0.8, because the headword class is a **reporting ruling layered on
the evidence**, not the evidence alone. Where no Tamil sense exists at all (கிளாஸ் = English
class AND English glass) the headword stays `unknown`; nothing in the ruling picks a winner there.
A sense whose block states no relation — கால் 'wind' (bare cognates), கார் 'to darken' ("From the
above") — is omitted rather than padded in as an unknown sense (Saran's call).

**Two defects the change exposed, both fixed here.**
- The native short-circuit in `_fill_native_equivalent` gated on `is_native` alone. A homograph
  leading native would therefore have silently dropped the attested equivalents of its BORROWED
  sense. Now gated on native AND no borrowed sense — பசு's 'cow' sense keeps ஆ / உயிர்.
- `force_refresh` reached only the meaning cache, never etymology. `refresh_sources` did nothing
  for origin, so a parser upgrade left old-shape cached dicts served forever — which would have
  made this very change unmeasurable without clearing the store by hand.

**Result.** correct 82 → **87**, honest unknown 23 → **18**, wrong **1** (unchanged), formation
26/30 (unchanged). 16 of the 108 sweep words now carry a per-sense breakdown, printed as its own
sweep section.

**Ruling extended — ANY source language, not Sanskrit only (Saran, 2026-08-05).** கார் was first
parked in the sweep's *uncertain* bucket, because the ruling had been stated for Tamil-vs-Sanskrit
while கார் is Tamil-vs-English. Saran resolved it: *"We should follow the same rule for both
Tamil-vs-Sanskrit and Tamil-vs-English — or any other transliteratory words from Urdu, Marathi,
Telugu etc. Always prioritize the native Tamil word but give the other meanings from Sanskrit,
English etc., so the user is aware of both."* கார் therefore leads native (blackness / monsoon —
கார்காலம்) and is a ruled expectation, not an open question.

**Consequence he also asked for: the borrowed sense hands back its Tamil word.** *"Sometimes the
user meant the English word, that he can pick up from the 2nd choice word, but now he knows the
native equivalent of it."* So `SenseOrigin.tamil_alternatives` carries them per sense — கார் 'car'
→ மகிழுந்து / சீருந்து / தானுந்து; கிளாஸ் → வகுப்பு ('class') and கண்ணாடி ('glass'); சாலை's Sanskrit
'hall' → வீடு / மனை / இல்லம். Source is the page's own `{{syn|ta|…}}`, collected per Etymology block
so synonyms cannot leak across senses.

**Filtered, because a synonym can itself be a borrowing.** en.wiktionary lists ரோடு — English
"road" — as a synonym of சாலை's road sense. `classifier.looks_orthographically_native` drops those,
reusing the D-015 insight that orthography proves NON-nativeness.

**Named `tamil_alternatives`, not `native_equivalents`, deliberately.** That same insight caps what
may be claimed: the rules prove non-nativeness only, so naturalized Sanskrit passes them — தானம்
'place' yields சுவர்க்கம் (< स्वर्ग) and சக்தி (< शक्ति), மந்திரம் yields மண்டபம் (< मण्डप). Labelling
those "pure Tamil" would over-claim in exactly the place D-015 says we cannot. Evolving tier,
confidence 0.6. **The loanword lexicon (Madras Tamil Lexicon) is what would let this assert
nativeness — do not re-label until it lands.**

**They also feed the headword `native_equivalent` when I2PT misses.** I2PT is keyed on borrowed
HEADWORDS, so it has no கார் row at all — கார் is a native word that merely shares its form — which
means `suggest_native_equivalent` was silent for every homograph before this.

**Also fixed in passing (its own commit):** `inh+` and `lbor+` were missing from the "stated"
certainty list while `bor+` was in it, so every `{{inh+}}` word scored 0.65 against 0.8 for
Sanskrit/English `{{bor+}}` borrowings — a systematic tilt against native words. Only `der`/`der+`
are genuinely a weaker relation. Labels unaffected; confidences only.

**Final sweep: correct 82 → 87, honest unknown 23 → 18, wrong 1 (unchanged), formation 26/30.**

*Status: CLOSED 2026-08-05 (homograph handling landed per-sense; ruling covers every source language).* *Links: `thamizh-mcp/src/thamizh_mcp/adapters/etymology.py`,
`core/classifier.py`, `tests/test_etymology.py`, `scripts/quality_sweep.py`; D-008 (Aalamaram),
D-012 (licensing), D-014 (cited rule tables).*

## D-016 · 2026-08-07 · Madras Lexicon is CC BY-NC-ND — sources need a REDISTRIBUTION MODE, not just a tier

**Trigger.** Session 4 opened on the loanword lexicon — the intended anchor upgrade that would finally
close the `native-by-default` branch in origin classification. Before designing the adapter we read
DSAL's actual terms, which D-012 had listed as *"still genuinely open (sourcing tasks, NOT blockers)"*.

**Finding.** The Madras University Tamil Lexicon at `dsal.uchicago.edu/dictionaries/tamil-lex/` is
published under **Creative Commons BY-NC-ND 2.0**, copyright **University of Madras** (original
1924–1936), digitization last refreshed **September 2023**. There is no public API.

Both trailing terms bite:
- **ND (NoDerivatives)** — parsing entries into a restructured store and serving them is plausibly a
  derivative work.
- **NC (NonCommercial)** — `thamizh-mcp` is Apache-2.0 and anyone may run it, including commercially.
  Bundling NC data inside it pushes a restriction onto downstream users who never agreed to it —
  the same error as relicensing CC BY-SA Wiktionary text, which D-012 forbids.

This **closes an option the code stub had left open**: `adapters/lexicon.py` proposed "scrape-at-query
vs offline digitized copy (blueprint §10)". The offline copy is not available to us.

**Decision — tier and licence are INDEPENDENT axes.** We had been treating "how much do we trust it"
and "what may we do with the bytes" as one property. They are not. Every source now declares BOTH a
`tier` (anchor / evolving) and a **redistribution mode**:

| Mode | Example | Permitted |
|---|---|---|
| **Redistribute** | Project Madurai classical; I2PT (MIT) | ship the data as a version-locked artifact |
| **Serve with attribution** | Tamil Wiktionary (CC BY-SA) | cache + serve, attribution travels, never relicensed |
| **Consult and cite** | **Madras Tamil Lexicon (CC BY-NC-ND)** | consult to establish a fact; store the FACT + citation, never the entry text |

A consult-and-cite source is not second-class — MTL is the most authoritative lexicon we have. The
mode constrains **distribution**, not **trust**.

**Why consult-and-cite is legitimate, not a workaround.** It is the same facts-vs-expression argument
already applied to the TVA course books in `sources/README.md`: *"Facts aren't copyrightable, and
citing the source is scholarship."* That a word is attested as an English borrowing is a fact; the
lexicon's wording of its entry is expression. We record the former and cite where we verified it.

**Consequences for the MTL adapter (Saran's call, 2026-08-07 — proceed on this basis):**
- no bundled copy in the code repo; query-time lookup only
- cached in the machine-local, gitignored `data/knowledge.sqlite3` — a private cache is not distribution
- store the derived claim + citation URL, never the entry text
- excluded from the gold-corpus export (D-012's per-source classification makes this a filter)
- **opt-in, disabled by default**, so the shipped Apache-2.0 product carries no NC dependency
- courteous access: descriptive UA, rate limiting, `robots.txt`, cache-once

**Recorded honestly: this is the cautious reading.** We are not lawyers and NC/ND is where a cautious
and a permissive reading diverge. **Saran is approaching the University of Chicago / DSAL for written
permission** for this specific use. If granted, the mode widens; until then it does not.

**Also decided:** the method is documented **source-agnostically** — `sources/INTEGRATING-A-LEXICON.md`,
written for scholars, with MTL as the worked example rather than the subject. This is risk management,
not tidiness: if permission is refused, Cologne OTL or another lexicon takes MTL's place under the same
architecture and the document still stands.

**Still open.** Aalamaram licence (D-008) — unchanged. DESIGN.md §7's "Gate-0 blocks every public rung"
framing remains superseded by D-012.

*Status: active; adapter implementation next, permission request in parallel.* *Links:
`sources/INTEGRATING-A-LEXICON.md`; `thamizh-mcp/src/thamizh_mcp/adapters/lexicon.py` (stub),
`core/classifier.py` (the native-by-default branch this closes); D-008 (Aalamaram), D-012 (licensing),
D-015 (origin per sense — `tamil_alternatives` is capped pending exactly this lexicon).*

---

## D-017 · 2026-08-08 · The S2PT licence claim is WITHDRAWN — and provenance becomes a REGISTRY, not prose

*Recorded 2026-08-11. The decision was taken on 2026-08-08 and implemented across Sessions 5–6; the log
entry was missed at the time, while seven documents had already begun citing "D-017". That gap is itself
an instance of what this entry is about.*

**Trigger.** A routine check of the vendored வடசொல் word lists ahead of wiring `suggest_native_equivalent`
more widely. `LICENSING.md` and `data/PINS.md` both recorded the source as **MIT — cleared for use and
redistribution**.

**Finding.** It is not. Upstream — `github.com/narVidhai/Sanskrit-To-Pure-Tamil-Dictionary` — has **no
LICENSE file** and states no terms in its README. Its four sub-lists are scraped from community sites
(viruba.com, tamilchol.com, thamizhdna.org, tamilmantram.com) whose own terms are also unstated. Last
upstream commit: 2020. Sibling repos in the same org *do* carry explicit MIT, which suggests an omission
rather than an intent to restrict — **but an omission is not a grant.** The MIT claim is withdrawn.

Two related corrections landed with it: the source had been called **"I2PT" / Indic-To-Pure-Tamil**, and
GitHub's silent redirect from the renamed repo hid the drift for weeks; and its scope is specifically
**வடசொல்** (its README is titled "வடசொல் to தமிழ்"), so membership is evidence of a *Sanskrit* source, not
of "borrowed" in general.

**What we do about it (unchanged from the 2026-08-08 disposition).** The lists stay vendored and used —
they are attested and unique at their job — but every claim they support is **confidence-capped at 0.55**,
the lowest committing score in the classifier; the evidence string **names the weakness in the answer
itself**; an en.wiktionary etymology always outranks them; and they are **marked for supersession** by
authenticated sources (TVA / government கலைச்சொல் glossaries). Treat S2PT as a working placeholder, never
an anchor.

**The systemic decision — this is the part that matters.** The defect was never that we shipped a weak
source. Weak sources are fine and always will be; the project cannot wait for a complete, impeccably
licensed Tamil corpus that does not exist. The defect was that **the weakness was not declared anywhere a
machine could read.** Licence and quality facts lived in three prose locations — `LICENSING.md`,
`data/PINS.md`, per-adapter docstrings — and *nothing checked that a shipped adapter had been through any
of them*. A source could become load-bearing without ever being reviewed.

So: **every source gets a registry entry, and omission fails the build.**

| Field | What it records |
|---|---|
| `grade` (A–D) | **Evidential standing only.** A = primary authority (the classical text, or a table carrying its நூற்பா); B = scholarly/institutional publication; C = community-edited and revisable; D = unattributed, unmaintained compilation. |
| `confidence_cap` | The ceiling that grade supports — A 0.95, B 0.85, C 0.80, D 0.55. A **ceiling, never a score**: it can only lower a confidence, never invent one. |
| `redistribution` | D-016's three modes: redistribute / serve-with-attribution / consult-and-cite. |
| `licence` + `licence_status` | `"unstated"` is a **passing** value. Recording "we do not know" is an honest fact; silence is not. |
| `maintenance`, `pin`, `supersession` | Is anyone still maintaining it, which bytes we ship, and what is meant to replace it. |

⚠️ **`grade` and `redistribution` are INDEPENDENT axes**, and the registry is where D-016's finding becomes
mechanical rather than remembered. The **Madras Tamil Lexicon is grade A *and* consult-and-cite** — the most
authoritative lexicon we have and the most restrictively licensed. S2PT is grade D and freely servable.
Deriving either axis from the other is exactly the error D-016 was written to correct, and there is a test
asserting the two have not collapsed.

**Framing to carry forward:** *authenticity comes from every claim carrying a graded, citable provenance the
user can check — not from every source being impeccable.* A grade D source is fine to ship, as long as the
answer says it is grade D. The grade is now stamped onto every `SourceRef` and shown beside the source name
in the web app, so a reader can tell Nannūl from a scraped community list at a glance — which a
comma-separated list of names never allowed.

*Status: active; registry shipped 2026-08-11 (`data/sources.json`, `core/sources.py`,
`tests/test_sources_registry.py`). The S2PT licence gap itself remains OPEN and is the one genuine licence
gap we ship.* *Links: `thamizh-mcp/data/sources.json`; `thamizh-mcp/LICENSING.md` (reasoning; the registry
holds the machine-checkable facts); D-016 (redistribution modes — the axis split this generalises), D-012
(licensing settled), D-015 (origin per sense), D-008 (Aalamaram, still unlocated).*

---

## D-018 · 2026-08-08 · The pinned நூற்பா are served at RUNTIME, so a claim QUOTES its authority

*Recorded 2026-08-11, with D-017, for the same reason.*

**Trigger.** Settling what the second `த்` in வா + த் + த் + ஏன் is called took several exchanges. The
answer — **நன்னூல் 133**, which names all six பகுபத உறுப்பு including சந்தி — had been in the repo the
whole time. It had to be grepped by hand.

**Finding.** D-011 pinned Tholkappiyam and Nannūl, but `data/classical/` was read **only** by
`tests/test_citations.py` — a design-time guard proving every cited நூற்பா number resolves. Nothing in
`src/` opened it. `SourceRef.verse` was therefore always `None`, the 462 Nannūl verses and Tholkappiyam's
1,486 sat unused at runtime, and a user asking *"on whose authority?"* got a chapter name.

**Decision.** `core/classical.py` serves verses at runtime. `SourceRef.verse_text` carries the நூற்பா
verbatim and the web app displays it.

- **Nannūl** is continuous 1–462 → `classical.nannul_verse(133)`.
- **Tholkappiyam** numbers RESTART per இயல் and collide, so there is deliberately **no bare-number API** —
  `classical.tholkappiyam_verse(அதிகாரம், இயல், n)`. A bare number is a bug, not a shortcut, and the module
  offers no way to pass one.
- **Quoting obliges attribution.** Project Madurai grants distribution provided its header travels with the
  text, so any surface that quotes must show the credit (`classical.attribution`).
- **Only VERIFIED verses are wired.** An unconfirmed citation keeps `verse=None` and cites the section.
  *Completed 2026-08-11:* the last three decoder `SourceRef`s were verse-cited, so every one now quotes.
  Note that Tholkappiyam states the four word classes across **two** நூற்பா — பெயரியல் 4 (பெயர், வினை) and
  5 (இடை, உரி) — and both travel, rather than crediting one verse with classes it does not name.

**Why this is a decision and not a feature.** The project's promise is that every grammatical claim is
grounded in Tholkappiyam and Nannūl. Until now that promise was kept at *design* time and merely asserted at
*answer* time. A citation tells a scholar where to look; the verse shows them. The related discipline is
recorded as a standing rule because it has already failed once: **quote from `data/classical/`
programmatically, never retype a verse.** The verbatim-quote test caught **five** நூற்பா transcriptions
drifting minutes after they were read — confabulation is indistinguishable from derivation from the inside,
so the mechanism, not the intention, is what holds.

*Status: active; shipped. Extended 2026-08-11 — all decoder `SourceRef`s verse-cited, and
`tests/test_citations.py` now asserts both that they quote a நூற்பா and that the quote matches the pinned
edition verbatim.* *Links: `thamizh-mcp/src/thamizh_mcp/core/classical.py`,
`thamizh-mcp/tests/test_citations.py`, `thamizh-mcp/data/PINS.md`; D-011 (verse-level grounding — this
closes its runtime half), D-014 (cited rule tables).*

## D-019 · 2026-08-18 · The public design site is a PHASE, and it ends when the app ships

**Trigger.** The deck (`PRESENTATION-SOURCE.md`) did not explain the project to Tamil scholars. Its
spine was a demo — ten slides, six of them worked word examples — so a reader finished it knowing
the tool splits மரத்தில் correctly and still not knowing what the project is. Rather than re-cut the
deck, the material moves to a public site at `thamizh-ai.org`, structured around four layers
(இலக்கணம் → பகுபத உறுப்பிலக்கணம் → மூலம் → பகிர்வு) and a horizon.

**Decision.** The site launches on the apex, and **the app overwrites it when M2 ships.** Saran's
reasoning, recorded because it inverts the usual instinct: once there is a working tool, the tool
should speak for itself. A scholar should be using it and judging it, not bookmarking a design page
and re-reading it. How we got here is history.

**Consequences, all decided now so they are not improvised on launch day:**

- **URL permanence is not a design constraint.** No path reservation, no `/design` prefix, no
  subdomain. Content sits at clean top-level paths.
- **Letters cite the design repo alongside the site.** `github.com/ief-global/thamizh-mcp-design` is
  the address that still resolves in five years; the site URL is the readable one. This matters
  because the TVA and DSAL letters will quote a URL and a reply may land a year later.
- **On app day every old page redirects to the app**, rather than 404ing. Cloudflare bulk redirects.
- **The archive is a git tag plus a `dist/` snapshot** on a GitHub release.
- **The site says this about itself** on `/about`. Publishing an expiry date is consistent with a
  project whose pitch is honesty about its own state.

**Also settled in the same session.** English-first with a Tamil mirror for the four pages an
outreach letter links · a page per institution (`/sources/thamizhimorph` most carefully, since it is
the page Sarveswaran reads if he is written to) · the S2PT licence gap stays named in public ·
**hero photography is IN**, which amends `BRAND.md`'s "no temples, the typography is the culture"
rule: photography of primary Tamil sources and monuments is welcome and carries its citation like
any other claim, while generic stock imagery, kolam borders and AI-brain art stay banned. The two
images chosen are public domain (a palm-leaf manuscript of தொல்காப்பியம்) and CC0 (a வட்டெழுத்து
inscription at Thanjavur).

*Status: active; site repo created and session 1 shipped 2026-08-18.* *Links: `WEBSITE-PLAN.md`,
`github.com/ief-global/thamizh-ai`, D-013 (the app is a separate deliverable, and it is what
eventually takes this domain), `BRAND.md` (needs the imagery amendment).*

## D-020 · 2026-08-18 · Site prose is CC BY-SA 4.0; site code stays Apache-2.0

**Trigger.** A new public repo needed a licence, and one licence could not sensibly cover both Astro
components and scholarly prose about Tamil grammar.

**Decision.** Two licences in `ief-global/thamizh-ai`, stated in `LICENSE-CONTENT.md`: **Apache-2.0**
for the code, matching the server repo so there is one software licence across the project, and
**CC BY-SA 4.0** for the prose and diagrams.

**Why share-alike rather than CC BY.** Tamil Wiktionary content is already CC BY-SA and it is one of
the sources the writing describes, so share-alike avoids a licence-compatibility question before it
arises. And scholarship about a shared language should stay reusable on the terms it was built from.
Photography on the site is public domain or CC0 only, recorded in `public/img/CREDITS.md`, so no
image inherits an attribution obligation the site could quietly break.

*Status: active.* *Links: `WEBSITE-PLAN.md` §7, D-012 (licensing settled for the server), D-019.*

## D-021 · 2026-11-24 · TVA material is CC BY-SA 4.0

**Trigger.** The licence question put to the Tamil Virtual Academy in the 2026-08-08 letter (never
sent) was answered during Saran's visit to TVA, Chennai, in November 2026.

**Evidence.** In writing, on tamilvu.org (the கணித்தமிழ்ப் பேரவை page): *"தமிழ்ப்பெருங்களஞ்சியத்தில் உள்ள
ஆக்கங்கள் படைப்பாக்கப் பொதுமங்கள் (CC BY-SA 4.0) என்னும் உரிமத்தின் கீழ் அளிக்கப்படுகின்றது."* That
statement names the works of the தமிழ்ப்பெருங்களஞ்சியம். It is **extended to all TVA materials**:
course books, கலைச்சொல் glossaries, the annotated corpus, and the archive.org collection.

**Decision.**
- TVA material is **CC BY-SA 4.0**, redistribution mode **serve-with-attribution** (D-016). The code
  repo's registry (`data/sources.json`, D-017) and `LICENSING.md` record it, and a test asserts they
  agree.
- TVA-derived data (rule tables, glossary entries, corpus extracts) may ship with attribution and
  stays share-alike, never Apache-2.0.
- The course books stay out of git for **size**, no longer for licence. The `.gitignore` patterns
  stay: a source document is still ignored by default and committed deliberately.
- **TVA's servers are unreliable**, and TVA cannot restore them quickly. Read from tamilvu.org when it
  is up and from `archive.org/details/TamilVirtualAcademy` (98,920 items, no licence metadata of its
  own) when it is not. Proposed, not yet decided: a mirrored, checksummed corpus of TVA material in the
  app's Postgres (raw bytes → decoded text → parsed units), so a TVA outage never blocks us.

**What it unblocks.** The கலைச்சொல் glossaries can now replace S2PT, the one unlicensed source we ship,
once they are found as data. The annotated corpus becomes usable as evaluation gold.

*Status: active.* *Links: D-016, D-017, `sources/correspondence/`, code repo `LICENSING.md`.*

## D-022 · 2026-11-24 · பிராகிருதம் is its own origin class, not வடசொல்

**Trigger.** en.wiktionary changed மனிதன்'s etymology on 2026-08-25 from Sanskrit to **Prakrit**
(`{{bor+|ta|pra|…}}`). The classifier had two borrowed classes, வடசொல் for Sanskrit and `loanword` for
everything else, so it called மனிதன் a loanword and the 2026-11-24 sweep counted it wrong.

**Ruling (Saran, 2026-11-24).** Prakrit (பிராகிருதம்) is **not** வடசொல். Where there is enough evidence
that a word is from Prakrit, it gets its own class.

**Decision.**
- New origin class **பிராகிருதம்**, outside Tholkappiyam's four like `loanword`. Assigned only when a
  source names Prakrit: Wiktionary codes `pra`, `pmh`, `psu`, `pka`. No மொழிமரபு verse is cited for
  it, since Tholkappiyam's frame does not name it; the evidence is the etymology itself.
- **Pali (`pi`) is not included.** The ruling named Prakrit, and extending it to a related language
  would be our inference. Pali stays `loanword` until ruled.
- மனிதன் moves to பிராகிருதம்; the sweep goes from 91/12/3 to **92/12/2**.

*Status: active.* *Links: D-015 (orthography proves non-nativeness, etymology proves provenance).*

## D-023 · 2026-11-24 · A split must rebuild its word; ambiguities are settled by texts, not rulings

**Trigger.** Two linked problems. (1) The decoder builds a split from FST tags and never rebuilds
the word, so material absent from the tags is dropped in silence: காத்திருந்தாள் decodes without its
ந். (2) What the doubled consonant of a strong verb is called (வா + த் + த் + ஏன்) had three different
answers in our own records, including two "rulings" that contradicted each other.

**Decision 1: round-trip validity is a fundamental rule (Saran).** A word split is valid only if
joining its parts back, under the **same** rule tables, rebuilds the word. Split and join follow one
rule set. A split that does not rebuild its word declares a gap and never drops material. This is
the definition of the defect-1 fix, and it gives the engine one rule set used in both directions.

**Decision 2: grammar ambiguities are resolved from the texts.** Saran's direction: he will not
settle an ambiguity by ruling, because a ruling made without a source becomes a rule nobody can
check. The engine must follow a rule it can cite with confidence. Until that rule is found, the
question is **parked**, and the engine names what it can ground and declares the rest a gap.

**Applied now.** The doubled-consonant label is parked. The 2026-08-02 ("it is சந்தி") and 2026-08-08
("it is not சந்தி") entries in `idainilai.json` are withdrawn as rulings. The சந்தி the decoder still
emits is marked as an unruled label until the round-trip work replaces it. Rulings that do rest on a
source stand.

**Where the rules will come from.** The நூற்பா are terse; the classical உரை explain them with worked
examples. Project Madurai's எழுத்ததிகாரம் with நச்சினார்க்கினியர் உரை (pmuni0516, same distribution
terms as our pinned texts) has 485 units, 373 of them with `எ-டு … என வரும்` examples. Those examples
are the natural fixtures for the round-trip engine. It numbers verses continuously and divides two
இயல் differently from our pin, so it must be aligned by verse text, never by number.

*Status: active.* *Links: D-014 (grammar rules as cited tables), D-018 (verse grounding), code repo
`CLAUDE.md` KNOWN DECODER DEFECTS.*

## D-024 · 2026-11-24 · Tholkappiyam is pinned from its publisher, and the classical உரை joins the pins

**Trigger.** Pinning நச்சினார்க்கினியர்'s commentary on எழுத்ததிகாரம் (Project Madurai pmuni0516) as a
source of textual rules (D-023) meant comparing it with our pinned Tholkappiyam. That exposed 21 of
our verses carrying a literal `?` where ஃ belongs. The source we had pinned, the tamilnation.org
mirror, was also returning HTTP 503 that day. Project Madurai hosts the same etext itself
(pmuni0100), so the two were diffed verse by verse.

**Finding.** The mirror was lossy, far beyond the 21 verses. Against Project Madurai's own page it
had: ஃ lost as U+FFFD (repaired in August) and as `?` (never repaired); the vowel sign ொ dropped in
85 verses (`மெய்யடு` for `மெய்யொடு`); about 130 verses missing other characters; four verses glued
into a neighbour and therefore not addressable; and பொருளதிகாரம்'s மரபியல் filed under செய்யுளியல்,
with the real செய்யுளியல் absent. **In the other direction, every character of the old pin is present
in the new one.** These verses were being quoted to users verbatim (D-018).

**Decision.**
1. **Pin from the publisher, never from a mirror.** Tholkappiyam is re-pinned from pmuni0100: 1,602
   verses in 27 இயல் (was 1,486 in 26), every இயல் gap-free. The retired mirror and the reason are
   recorded inside the artifact.
2. **Pin the classical உரை.** நச்சினார்க்கினியர் on எழுத்ததிகாரம் ships as its own artifact, 480 units
   with verse, commentary, worked examples and footnotes, under the same Project Madurai terms.
3. **Align commentaries by text, never by number.** This edition numbers continuously and divides two
   இயல் differently. Result: 479 of 483 verses aligned (median similarity 0.98), one printed merged
   with its neighbour, three absent from the etext. Every verse is accounted for, and the builder
   refuses to write the artifact if that stops being true.
4. **Assert that text is clean, not that a repair ran.** The old test checked a repair counter and so
   could never see the `?` corruption. The guard now asserts the absence of corruption directly.

**Also found.** Project Madurai's Nannūl page was revised upstream after we pinned it, and our parser
reads the revision into a different text for all but 14 verses. The builder now refuses to overwrite
the verified Nannūl pin. Adopting the revision is open work, to be done the same way: verse by verse.

**Why it matters beyond this PR.** Two of our three classical sources changed or failed underneath
us in three months, and the archive.org mirror was offline the same day. This is the case for the
mirrored corpus proposed under D-021.

*Status: active.* *Links: D-011, D-018, D-021, D-023; code repo `data/PINS.md`, `tests/test_urai.py`.*

## D-025 · 2026-11-25 · The round-trip engine: the split is found by synthesis over cited joins

**Trigger.** D-023 made round-trip validity a fundamental rule. This records how the code meets it,
and which calls the implementation had to make.

**Decision 1: split and join are one rule set by construction.** The split is not computed and then
checked. It is *found* by joining: `core/punarchi.py` tries the join rules of
`data/grammar/punarchi.json` at each boundary between the FST's parts and keeps a split only when the
join reproduces the word exactly. Underneath, letters ↔ phonemes is Tholkappiyam's own pair:
எழுத்ததிகாரம் › புணரியல் 36 (a vowel after a pulli fuses with it: the join) and 37 (strip the vowel
and the consonant takes back its own form: the split). A guard re-renders all 1,602 pinned verses
through that bijection.

**Decision 2: every join rule cites its நூற்பா by address, Tholkappiyam first; the verse is quoted at
runtime.** Seven classical rules: புணரியல் 12, 23, 31, 38, உருபியல் 13, குற்றியலுகரப்புணரியல் 6, with
Nannūl 162, 183, 252 alongside. Two rest on Nannūl alone (164 உகரம் கெடுதல், 219 ம் → nasal) because a
search of எழுத்ததிகாரம் found no Tholkappiyam verse for them; the table records that search, and a
test fails a Nannūl-only rule that does not. The commentary's own worked examples are fixtures:
under உருபியல் 13 நச்சினார்க்கினியர் gives மரத்தை, மரத்தொடு and says they are finished by புணரியல் 31 and
23 together, which are exactly the two rules the engine applies.

**Decision 3: three statuses, shown to the reader.** `classical` (a நூற்பா states it), `textbook`
(a TVA course book states it verbatim; CC BY-SA 4.0, D-021), `parked` (the material is named so
nothing is dropped, but no cited rule labels it). Every join step in the answer carries its status
and its quoted source.

**Decision 4: the ந் of வந்தான் is a சந்தி த் surfacing as ந் (`textbook`).** TVA C0212 §5.3.6 states
it verbatim: "வா என்னும் பகுதி வ எனக் குறுகியும், த் என்னும் சந்தி ந் என்று மாற்றம் அடைந்தும்,
விகாரமாகியுள்ளன". It agrees with Saran's 2026-08-11 ruling and with நன்னூல் 142, which lists the past
இடைநிலை as த்/ட்/ற்/இன் only. The same section gives வா → வ as குறுகல்.

**Decision 5: the strong-verb doubled consonant is named, with no part label (`parked`).** It is a
component with `part: null`, so படிக்கிறான் = படி + க் + கிறு + ஆன் rebuilds without claiming what
the க் is. The previous சந்தி label and its மிகுதல் event are removed. The strongest text found is
TVA C0212 §5.3.5, which defines சந்தி by position ("சந்தி பெரும்பாலும் முதனிலை (பகுதி)க்கும்
இடைநிலைக்கும் இடையில் வரும்", e.g. நட + த் + தல்) — close to the withdrawn 2026-08-08 entry. It is a
course book, not a நூற்பா or a classical உரை, so it is recorded and not applied. **Whether a TVA course
book is enough to settle ruling (d) is Saran's call.**

**Decision 6: the engine decodes the first FST analysis that rebuilds the word.** The FST's order is
not a judgement: it lists செய்தான் as the noun செய் + a focus tag first, which cannot account for
-தான். If no analysis rebuilds, the answer carries a formation Gap naming the letters nothing accounts
for.

**Result.** The sweep's formation figure is still 26/29 in-scope, but it now means "rebuilds its word":
17 on cited joins alone, 9 with one parked element (eight doubled consonants; சொன் from a curated
paradigm, ruling (a)). Five of the 26 (வந்தான், வந்தனன், வந்தார்கள், வந்தீர்கள், நடந்தன) used to pass with
the ந் missing. The number did not fall as predicted because the engine names the material instead of
failing on it.

*Status: active; Decision 5 superseded by D-026.* *Links: D-014, D-018, D-021, D-023, D-024; code repo `core/punarchi.py`,
`data/grammar/punarchi.json`, `tests/test_roundtrip.py`.*

## D-026 · 2026-11-25 · The doubled consonant is a சந்தி on the TVA course book, until a classical உரை says otherwise (SUPERSEDED by D-028)

**Trigger.** D-025 left the strong-verb doubled consonant (படி + க் + கிறு + ஆன்) named with no part
label (ruling (d), parked under D-023). The strongest text found was TVA C0212 §5.3.5, a course book.
D-025 asked whether a course book is enough.

**Decision 1: yes, for now (Saran, 2026-11-25).** The slot is labelled **சந்தி** on TVA C0212 §5.3.5:
"சந்தி பெரும்பாலும் முதனிலை (பகுதி)க்கும் இடைநிலைக்கும் இடையில் வரும். பகுதிக்கும் விகுதிக்கும்
இடையிலும் சிறுபான்மை வரக்கூடும். உறுப்புகளின் இணைவில் (சந்தி), அவற்றை இணைக்க வருவது சந்தி." Its own
example is நடத்தல் = நட + த் + தல். The rule (`irattitha_otru` in `punarchi.json`) moves from `parked` to
`textbook`, quotes that passage, and cites நன்னூல் 133 alongside, which names சந்தி among the six உறுப்பு
but does not say where it comes. There is no மிகுதல் event, because the text names an உறுப்பு and not a
change. The 2026-08-02 and 2026-08-08 entries stay withdrawn: the label rests on the text, not on them.

**Decision 2: a classical commentary takes precedence.** If an authentic classical உரை on தொல்காப்பியம்
சொல்லதிகாரம் names this slot, it overrides the course book, whatever it says. The rule records that in
`supersede_when`. Finding and pinning such an உரை is an **open item to resolve soon**. Pin it from its
publisher, checksum it and align it by verse text, as D-024 did for the எழுத்ததிகாரம் உரை. The same
commentary would also bear on rulings (a) and (c), which are verb questions.

**Decision 3: D-023's rule is refined, not reversed.** Ambiguities are still settled from texts. A TVA
course book that states the analysis verbatim can now carry a label **provisionally**, and a நூற்பா or
classical உரை found later outranks it. In code, when both a நூற்பா and a course book rebuild a word,
the search takes the நூற்பா.

**Result.** The sweep is unchanged at 26/29 in scope. 25 of the 26 now have every step cited, through a
நூற்பா or a course book quoted verbatim. Only சொன்னான் keeps a parked step, because its curated stem
falls under ruling (a). Previously 9 had a parked step.

*Status: active, provisional (see Decision 2).* *Links: D-021 (TVA licence), D-023, D-024, D-025; code
repo `data/grammar/punarchi.json` → `irattitha_otru`, `CLAUDE.md` Next tasks 1.*

## D-027 · 2026-11-25 · The சொல்லதிகாரம் உரை is pinned from TVA scans; what it says on the verb slot

**Trigger.** D-026 labelled the strong-verb doubled consonant சந்தி on a TVA course book, provisionally,
and made finding a classical உரை on சொல்லதிகாரம் an open item to resolve soon. Project Madurai holds
நச்சினார்க்கினியர் on எழுத்ததிகாரம் and பொருளதிகாரம், but not on சொல்லதிகாரம். tamilvu.org's own
Tholkappiyam library did not respond. Saran pointed to two Tamil Digital Library scans in TVA's
archive.org collection.

**Decision 1: pin both commentaries.** நச்சினார்க்கினியர் (சரசுவதி மகால் நூலகம், 1999) reads uniformly
with the எழுத்ததிகாரம் உரை of D-024. இளம்பூரணர் (தமிழ்ப் பல்கலைக்கழகம், 1988) is the earliest
commentator. Licence: CC BY-SA 4.0 under D-021.

**Decision 2: the pinned text is archive.org's OCR, and it is labelled as OCR.** No typed etext of
either commentary was found. The build (`scripts/build_sol_urai.py`, code repo) reads the `_djvu.xml`
OCR, because it keeps each line's scan leaf. It aligns the OCR to our 463 verses by text: நச்சினார்க்கினியர்
463/463, இளம்பூரணர் 462/463. Every unit names its scan pages. The scans, the OCR and the page maps are
pinned by sha256 and mirrored in `sources/classical/sol-urai/`, outside git. The registry grades the pin
**B**, not A, because the text is not proof-read; the commentators themselves are not in question.

**Decision 3: a passage may back a rule only after it is read against the scan.** Passages checked
that way are listed in `data/classical/verified_quotations.json` (code repo), transcribed as printed,
the edition's misprints included. A test keeps each one findable in its unit.

**Finding (scan-verified, all நச்சினார்க்கினியர்).**
- He never calls any part of a verb **சந்தி**. His parts are முதனிலை, the tense letter, இடைநிலை எழுத்து,
  ஈறு, and விகாரம.
- Tense letters: "இக் கட தறக்கள் முதனிலையை யடுத்து வருங்கா லிறப்பு மீற்றினை யடுத்து வருங்கா
  லெதிர்வு முணர்த்தும்" (வினையியல் 5, p. 205).
- வந்தான்: "முதனிலை குறுகி, கால வெழுத்திற் கேற்ற விடை நிலை யெழுத்துப் பெற்று" (p. 467). The letter TVA
  calls a சந்தி த் surfacing as ந் is, for him, an இடைநிலை letter suited to the tense letter.
- Causatives (நடப்பித்தான் …): "இடை நிலையாகிய வெழுத்துக்களும் பெற்று", and the இ of வி becomes an
  இடைநிலை (p. 237). This agrees with the 2026-08-02 ruling that வி is an இடைநிலை.
- Feminine nouns: "தகர வொற்றிரட்டியு மிரண்டிடை நிலை யெழுத்துக்களைப் பெற்றும் … இடைநிலை
  யெழுத்துக்களும் பெற்று" (p. 174). A doubled த ஒற்று is among the இடைநிலை letters, in nouns.
- Ruling (a), ல்/ள் roots: "லகாரம் னகாரமாய்த் திரிந்து, தனக்கேற்ற றகர வொற்றுப் பெற்று" (கொன்றான்,
  சென்றான், வென்றான்); "ளகாரம் ணகாரமாயும்" (கொண்டான்) (p. 467).
- He does **not** split a strong verb's two த் (கொடுத்தான்) explicitly. இளம்பூரணர் says nothing on tense
  letters. நச்சினார்க்கினியர் names சேனாவரையர் as one who separates them; that commentary is not pinned.

**Open (Saran).** Under D-026 a classical commentary that names the slot outranks the course book.
Whether these passages name the strong-verb slot, and whether `santhi_tha_na`'s ந் should follow, is
Saran's call. Nothing in the engine changes until then. The same holds for ruling (a).

*Status: active; its Open item is resolved by D-028.* *Links: D-021, D-024, D-026, D-028; code repo
`scripts/build_sol_urai.py`, `data/classical/tholkappiyam_sol_urai_*.json`,
`data/classical/verified_quotations.json`.*

## D-028 · 2026-11-25 · A classical commentary always outranks the course book; சேனாவரையர் pinned; the verb slots are இடைநிலை

**Trigger.** D-027 pinned நச்சினார்க்கினியர் and இளம்பூரணர் and asked whether their passages name the
strong-verb slot. Saran answered: a commentary by நச்சினார்க்கினியர், இளம்பூரணர் or சேனாவரையர் takes
precedence over TVA, so fix the labels from the commentaries, always. Quoting these scholars gives
the authenticity; a course book can make mistakes. He also pointed to சேனாவரையர்'s commentary in TVA's
archive.org collection, and asked that archive.org's TVA collection be searched FIRST for sources
from now on.

**Decision 1: precedence, as a standing rule.** நூற்பா > classical உரை > TVA course book. The
round-trip engine has a new join status `urai`: the analysis is stated by a commentary, in a passage
read against its page image and listed by id in `data/classical/verified_quotations.json`. A rule's
`urai_scope` says exactly how far the passage reaches. When two splits rebuild a word, the engine
prefers fewer `textbook` steps, then fewer `urai` steps.

**Decision 2: pin சேனாவரையர்.** தொல்காப்பிய உரைத்தொகை 6 and 7 (தமிழ்மண் பதிப்பகம், 2018, reprinting
சி. கணேசையர்'s 1938 edition with his notes), archive.org `tdl.49552-6-1` and `tdl.49554-7-2`. It is the
publisher's typeset PDF rather than a scan, so its OCR is clean. Two volumes are read as one text and
every page names its volume. கணேசையர்'s notes follow each இயல்; units stop at "… முற்றிற்று" and at his
note headings, so the notes are not part of the commentary text. 461/463 verses align (விளிமரபு 13 and
உரியியல் 27 do not). The three-volume உரைக்கொத்து (`tdl.41274/41279/41281`, all commentators side by
side) was not needed. Licence as D-021; the 2018 edition's own prefaces are not used.

**Decision 3: the two verb slots are இடைநிலை, on நச்சினார்க்கினியர்.** None of the three commentators
calls any part of a verb சந்தி.
- **வந்தான்'s ந்** is "கால வெழுத்திற் கேற்ற இடைநிலை யெழுத்து" (சொல். எச்சவியல் 67, p. 467). Rule
  `idainilai_na` (was `santhi_tha_na`). This supersedes TVA C0212 §5.3.6 and Saran's 2026-08-11 ruling
  (a சந்தி த் surfacing as ந்). நன்னூல் 142 lists the TENSE-SHOWING இடைநிலை only, so it does not exclude
  this letter.
- **The strong-verb doubled consonant** (படி + க் + கிறு + ஆன்) is an இடைநிலை எழுத்து. Rule
  `irattitha_otru`. Its support, stated with its limits: he counts a doubled த ஒற்று among "இரண்டு
  இடைநிலை எழுத்துக்கள்" in feminine nouns (பெயரியல் 11, p. 174), calls the ச/த/ட of such nouns
  இடைநிலை (p. 468), and calls the ஆ of உண்ணாநின்றான் an "இடைநிலை எழுத்து" (p. 469). That is his only
  name for a letter between the முதனிலை and the ஈறு. **No commentator splits a strong verb's two த்
  explicitly**; the label applies his name for a medial letter to the first of them. This supersedes
  D-026's சந்தி on TVA C0212 §5.3.5.
- **வா → வ and வா → வரு** are both "முதனிலை குறுகி" in the same passage, so both stem alternants
  now carry குறுகல் on the commentary. The second had no named change before.

**Finding: சேனாவரையர** (vol. 2, read against the rendered page).
- He names the tense letters "the letters that stand above the ஈறு": "நெறிப்பாடாவது அவ் வீற்றுமிசை
  நிற்கும் எழுத்து வேறுபாடு" (வினையியல் 4, p. 11). He does not split them further. கணேசையர் notes that,
  unlike Nannūl, he does not call them இடைநிலை (note 7, p. 56). So he neither confirms nor contradicts
  Decision 3.
- நில் in the present: "நில்லென்பது லகாரம் னகாரமாய் றகாரம் பெற்று நிற்கும்" (வினையியல் 5, p. 13). This
  has the same shape as நச்சினார்க்கினியர் on கொல்/செல்/வெல்.
- கணேசையர் also notes that சேனாவரையர் seems to take the ஆ of உண்ணாநின்றான் as a சாரியை. நச்சினார்க்கினியர்
  calls it an இடைநிலை எழுத்து. That ஆ is not decoded by the engine, so nothing turns on it yet.

**Not changed: ruling (a).** The commentaries give the ல்/ள் shape (ல் → ன் + ற்; ள் → ண்) for கொல்,
செல், வெல், நில், கொள். None of the three analyses சொல், கல், கேள் or வில்/விற். The paradigm
restructure lands as one change, so `verb_paradigms.json` is untouched.

**Effect.** Sweep unchanged (origin 92 / 12 / 2; formation 26/29). Every sweep step that rested on
the course book now rests on the commentary; only காண் → கண் is still `textbook`.

*Status: active.* *Links: D-021, D-023, D-026 (superseded), D-027; code repo `data/grammar/punarchi.json`
(`idainilai_na`, `irattitha_otru`), `data/classical/verified_quotations.json`,
`data/classical/tholkappiyam_sol_urai_senavaraiyar.json`.*
