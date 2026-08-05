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

**▶ OPEN — the Session 3 objective.** Homograph origin is currently reported as `unknown` + both
alternatives. That is honest but discards real information (5 of the 23 remaining unknowns).
**Origin is modelled per-HEADWORD but is really per-SENSE.** The adapter already parses both senses;
only the schema and presentation need deciding. Options: (a) `Origin.senses[]`, (b) headword-level
class + a `senses` breakdown, (c) caller passes a sense hint. `Meaning.senses` already exists —
aligning origin to it is the natural move.

*Status: active; homograph handling open.* *Links: `thamizh-mcp/src/thamizh_mcp/adapters/etymology.py`,
`core/classifier.py`, `tests/test_etymology.py`, `scripts/quality_sweep.py`; D-008 (Aalamaram),
D-012 (licensing), D-014 (cited rule tables).*
