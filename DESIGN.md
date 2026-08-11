# Thamizh MCP — DESIGN (top-level program document)

> The front door of `ief-global/thamizh-mcp-design`.
> Revised **2026-08-10** (second review: status reconciliation + generation track added).
> Supersedes `TAMIL-HIGH-RESOURCE-ROADMAP.md` as the program map.
>
> **Companion docs** — `Thamizh-MCP-blueprint.md` (server spec) · `CODE-STATUS.md` (what is actually
> built, written from the code side) · `Glossary.md` (morphology terms in Tamil-grammar language —
> read this if any term below is unfamiliar) · `thamizh-mcp-builder/references/DECISIONS.md`
> (append-only decision log, D-000…D-013) · the four skills (builder v6, eval, data-curation, release).

## How to read this document

| Section | What it answers |
|---|---|
| §1 Objectives | What we are trying to achieve and why it matters |
| §2 Operating model | Which repo does what; how design and code stay in sync |
| §3 Current status | What is actually built as of today |
| §4 Source strategy | Which Tamil sources we ground on, and their state |
| §5 GitHub × Hugging Face | Where code lives vs where data lives |
| §6 Roadmap | The numbered work list — NEAR / MEDIUM / LONG, with status |
| §7 Risks and open items | What could go wrong; what is undecided |
| §8 Generation track | How the word analyser grows into a sentence maker and predictor |

**Status legend** used throughout:

- ✅ **DONE** — built, tested, merged. Nothing further required.
- 🟡 **PARTIAL / IN PROGRESS** — real progress exists; the remainder is named explicitly.
- 🔲 **OPEN** — not started.
- ⛔ **BLOCKED** — cannot start until a named item finishes.

---

## 1. Objectives

**Program goal.** Move Tamil from a low-resource language toward a first-class language in the LLM
ecosystem. Concretely: a native Tamil speaker should get the same grounded, fluent, efficient AI
experience an English speaker gets today.

**Product, v1 (unchanged).** Given a single Tamil word, return a grounded, authentic analysis covering
five things: origin (இயற்சொல் vs borrowed), root + meaning, formation (பகுபதம் / புணர்ச்சி), grammar
(Tholkappiyam-first), and an attested native equivalent when the word is borrowed.

**Product, beyond v1 (new, §8).** The same engine extends from *analysing* one word to *understanding
a sentence* and then to *producing* correct Tamil. That track is now written down (§8) so it stops
being folklore, but v1 scope is unchanged and nothing in §8 is scheduled yet.

**Non-negotiables (unchanged, all five).**

1. **Tholkappiyam first** — தொல்காப்பியம் is the authority for grammar; நன்னூல் only where Tholkappiyam
   does not enumerate the point (chiefly the six-part பகுபதம் decomposition). Always say which was used.
2. **Self-enriching, not hand-maintained** — coverage grows from rule-based morphology plus evolving
   internet sources, never from a giant hand-curated word list.
3. **Attested-only equivalents** — never invent a native coinage; if no authority attests one, say so.
4. **Provenance on every claim** — each field carries its source, tier, and retrieval date.
5. **Honest gaps, never LLM-as-source** — if no source covers a field, return a gap, not a fluent guess.

**Evidence the gap is real (unchanged).** ILAKKANAM (arXiv:2511.12387): frontier models score 71–80% on
820 Tamil school-exam linguistics questions, decline sharply as complexity rises, and their accuracy does
not correlate with their ability to identify a question's linguistic category — performance is exposure,
not understanding. Separately, BPE tokenizers fragment agglutinated Tamil, costing roughly 3–5× more
context than English for the same content ("token explosion"). See `Glossary.md` for both terms.

---

## 2. Operating model

Two repos, two roles, one loop:

| | `thamizh-mcp-design` (private) | `thamizh-mcp` (public) |
|---|---|---|
| Role | **Design** — Cowork with a high-end model: plan, architect, decide, revise | **Build** — Claude Code on minnaham: implement, test, PR |
| Carries | blueprint, DESIGN.md, glossary, decision log, skills, research digests | code, tests, pinned anchor data, CLAUDE.md, LICENSING.md |
| Sync direction | reads CODE-STATUS.md to learn the real state | reads the skills + DESIGN/blueprint to learn the intent |

**Rules.** Never nest the repos. Design docs never enter the public repo. Decisions land in DECISIONS.md
(append-only — supersede, never edit history) *before* they land in code. Git runs only on Saran's own
machines: the Cowork sandbox corrupts `.git` on the `E:\` mount, so Cowork authors files via bash and
Saran commits. Both repos live under the **`ief-global`** GitHub org (D-010).

---

## 3. Current status — as of CODE-STATUS 2026-07-26

> ⚠️ **This section reflects a 2026-07-26 snapshot.** Sessions 3–5 (2026-08-05 → 08-08) landed
> D-015…D-018 and are NOT reflected below. For the current state read `CODE-STATUS.md` and the
> code repo's `CLAUDE.md`, which are authoritative. Headline as of 2026-08-08: origin
> **94 correct / 11 unknown / 1 wrong** on the 108-word sweep, formation 26/29 in-scope,
> 218 tests, and நூற்பா are quoted at runtime (D-018).

**Verdict: the design principles hold.** Every divergence between design and code is an *honest-minimal*
implementation (does less, truthfully) rather than a principle violation.

### 3.1 What is built ✅

- **9 MCP tools live**, covering all of blueprint §6 core: `analyze_word`, `classify_origin`, `get_root`,
  `get_meaning`, `suggest_native_equivalent`, `explain_formation`, `explain_grammar`, `enrich_word`,
  `refresh_sources`. **109 tests pass** (107 without a live foma install).
- **Engine shape matches blueprint §8** — a plain-Python `Engine` with a uniform `SourceAdapter`
  interface, a thin MCP head over it, linguistic rules isolated in `core/decoder.py` and
  `core/classifier.py` so the model never re-derives them.
- **Transaction logging on by default** (2026-07-18) with the `eval_fixture` contamination guard. The
  gold-data flywheel is running: every resolved analysis is captured for future dataset export.
- **Web / REST head live** (2026-07-26) — FastAPI + browser UI over the *same engine, with zero engine
  changes*, which proves the "many heads, one engine" design. Runs 24/7 on minnaham at
  `http://minnaham:8080`. This exists **ahead of schedule** (it was a MEDIUM item). Reason it mattered:
  terminals do not shape Tamil script correctly (vowel signs detach and reorder), so CLI output was
  unusable for demonstration; browsers render it properly. It is now the main manual-test surface, and
  every word tested there feeds the gold log.
- **FST coverage for common verbs closed** (2026-07-20) — `analyze_word` had been returning `unknown`
  for many everyday verbs because the FSTs lacked those lemmas and irregular tense stems. Guesser FSTs
  were rejected (they return *wrong* lemmas — கொடுத் for கொடு — i.e. confident errors instead of honest
  gaps). Fix: a curated anchor paradigm table consulted only on an FST miss. Sweep result: past 24/24,
  present 18/18, future 18/18.
- **Licensing settled** (D-012, 2026-07-26) — every source we ship is cleared for use *including* the
  public hosted service, under a mixed-licence, per-source-classification model. The old
  "Gate-0 blocks every public rung" framing is dead; `thamizh-mcp/LICENSING.md` is the canonical answer.

### 3.2 Known divergences the design side must keep in view 🟡

1. **`classify_origin` is a rule-based subset** of the D-002 design. It uses Grantha-character detection,
   Tholkappiyam முதல்/இறுதி எழுத்து phonotactics, FST native-parse, and I2PT attestation — but **not** the
   Thamizhi Word Validator and **not** a loanword dataset (neither is vendored yet). Consequence:
   borrowings that carry no orthographic marker return an honest `unknown` — புத்தகம் (Sanskrit but written
   in pure Tamil script) is the canonical example. Fixing this is roadmap item **N5**.
2. **Sandhi (புணர்ச்சி) naming is deliberately conservative.** Joins are named only where a confident
   classical rule fires; harder விகாரம் — notably verb-root changes such as வா→வந் — are left unnamed
   rather than invented. Correct under the no-invented-split rule, but below the linguistic standard the
   product should eventually meet. Fixing this is roadmap item **M4**, and it becomes a hard prerequisite
   for the generation track (§8).
3. **Grammar citations are section-level, not verse-level.** The schema now carries an optional
   `SourceRef.verse` field (D-011, landed), but no நூற்பா numbers are populated because no digitized
   Tholkappiyam/Nannūl edition is pinned yet. **Until that lands, public claims must say "section-level"
   honestly.** Roadmap item **N8**, blocked on **N7**.

### 3.3 The most important finding so far — invocation, not quality 🟡

The Phase-4 eval smoke run (2026-07-18) produced a result that changes how we think about the product:
**under a neutral prompt, a model with the thamizh tools attached called them 0% of the time.** A wiring
probe confirmed the server returns the *correct* answer when it is invoked. So spontaneous morphological
lift was ≈ 0 — not because the tools were wrong, but because nothing made the model reach for them.

A tool-description fix landed (code PR #10) and re-validation shows the previously failing questions now
invoke the tools and answer correctly. Two consequences are now permanent design commitments:

- **Tool descriptions are a product surface, not documentation.** They must state that this server *is*
  the de-agglutination layer and earns a call on *any* Tamil word task, not only explicit grammar
  questions.
- **Every eval needs a grounded-prompt arm** alongside the neutral arm, so we measure both what happens
  spontaneously and what the achievable ceiling is.

### 3.4 Current working mode (agreed 2026-07-26)

**Testing-driven development.** Saran exercises the live web app and brings back observed gaps,
clarification questions, and UI tweaks; those findings drive the next build, rather than working the
backlog blind. The Phase-4 eval stays paused — note its achievable ceiling rose with the coverage fixes,
so a re-measure is now more informative than the earlier run would have been.

---

## 4. Source strategy

Sources sit in one of two tiers, because they are maintained completely differently:

- **Anchor tier** — stable, authoritative, version-pinned. Ground truth. Pin the *version*.
- **Evolving tier** — community-contributed, internet-fed, growing. Fills coverage the anchors miss.
  Pin the *retrieval date and provenance* instead of a version.

### 4.1 Locked and pinned ✅

- **ThamizhiMorph FSTs** @ commit `adbacced` — morphological analysis and lemma. Anchor.
- **Indic-To-Pure-Tamil (I2PT)** @ `f734646`, 2,063 mappings — native-equivalent suggestions. Anchor,
  but **deliberately provisional**: the upstream project is stale (years since last activity) and is to
  be superseded by authenticated gold sources (TVA / government கலைச்சொல்). The `SourceAdapter`
  interface makes that a drop-in swap. MIT, cleared (D-012).
- **Tamil Wiktionary** — meanings and `{{சொல்வளம்N}}` synonym templates. Evolving tier. CC BY-SA,
  cleared for public serving with attribution; the content stays CC BY-SA and is never relicensed.
- **Curated verb paradigm table** — anchor tier, consulted only on FST miss (see §3.1).

### 4.2 Adopted but not yet obtained 🔲

- **Aalamaram** (D-008) — the largest public Tamil treebank, ~10k sentences with POS, NER, morphological
  parsing and dependency annotation, UD-adjusted for Tamil clitics and segmentation (WILDRE@LREC 2024;
  Sarveswaran co-author, same lineage as ThamizhiMorph and ILAKKANAM). **It is a treebank, not an
  equivalents dataset** — the earlier "replace I2PT with Aalamaram" framing was wrong and is corrected in
  the decision log. What it grounds: cross-checking FST analyses at scale, eval fixtures with real
  sentence context, phrase-level v2, and future SLM training. **Blocking pre-step:** locate the actual
  data distribution and verify its licence — not on Hugging Face, no public GitHub repo found; the paper
  PDF and its authors are the lead.
- **Madras University Tamil Lexicon** and **TVA / government கலைச்சொல் glossaries** — offline snapshots,
  anchor tier. Terms still to be confirmed. These are the authenticated sources that will retire I2PT's
  provisional status.
- **Digitized Tholkappiyam + Nannūl** — Saran chose **Project Madurai** (2026-07-19) as the edition to
  pin, enabling நூற்பா-level citation. No verse numbers are to be hardcoded from memory.

All four are batched into a single **network-open sourcing session** (roadmap item **N7**).

### 4.3 Where equivalents coverage actually grows

Not from Aalamaram. From: TVA/government கலைச்சொல் snapshots (anchor) + Tamil Wiktionary synonym-template
mining (evolving; the adapter already parses the template format) + I2PT as-is.

---

## 5. GitHub × Hugging Face architecture (D-009)

| Platform | Carries | Why there |
|---|---|---|
| GitHub `ief-global` | code (public), design (private), pinned anchor data, releases | version control, PRs, registry listings |
| HF `ief-global` | curated gold datasets (gold / silver / disputed splits, cards, versions) · Spaces demo · eventually the SLM | data versioning and discovery where the ML community actually looks; free demo hosting |

**White-space finding (2026-07-18 survey).** Hugging Face's Tamil shelf is speech/ASR/TTS, raw corpora,
sentiment datasets, and the tamil-llama / Tamil-Mistral model family. There is **no morphological
segmentation gold set, no loanword→equivalent dataset, and no origin-label dataset** — which is precisely
our three planned exports. Being first here is the org's credibility anchor and the future SLM's
training base.

**The flywheel.** Server usage → `transactions` log → `thamizh-data-curation` (verify, licence-gate,
contamination-guard) → versioned HF datasets → community use and tokenizer/SLM training → better Tamil AI
→ more server usage. Hugging Face is also an *input*: existing corpora (textbook datasets, cleaned OSCAR,
Wikipedia dumps) feed SLM-era pretraining.

**Not adopted:** mirroring third-party models under the org — maintenance surface, no near-term value.

---

## 6. Roadmap

Absorbs and supersedes `TAMIL-HIGH-RESOURCE-ROADMAP.md`. Every item is numbered so it can be referenced
in conversation and in commits. Each item states **what it is**, **why it matters**, and **what "done"
looks like**, because cryptic one-liners have proven unreadable a month later.

Horizons are *effort and dependency* estimates, not deadlines: NEAR = buildable now with what we have;
MEDIUM = needs a prerequisite or a sourcing session first; LONG = needs corpus scale, compute, or funding
that the earlier work creates.

### NEAR — ship the grounding layer and prove the lift

**N1 — Transaction logging** ✅ **DONE** (2026-07-18)
Every resolved analysis is written to a `transactions` table with full provenance and an `eval_fixture`
contamination flag. *Why:* the training corpus for everything later accumulates for free, as a by-product
of ordinary use. *Done:* logging on by default, non-fatal on failure, growth metrics available.

**N2 — FST coverage for common verbs** ✅ **DONE** (2026-07-20), 🟡 remainder open
A curated anchor paradigm table, consulted only when the FST misses, closed the everyday-verb gap.
*Why:* `analyze_word` was returning `unknown` on ordinary words, which is fatal for user trust.
*Done:* past 24/24, present 18/18, future 18/18 on the common-verb sweep. *Still open:* non-finite forms
(கொடுக்க / கொடுத்து / கொடுக்கும்) and additional lemmas.

**N3 — Web / REST head + browser UI** ✅ **DONE** (2026-07-26, ahead of schedule)
FastAPI head and browser UI over the same engine. *Why:* terminals mis-render Tamil script, so we had no
usable demonstration surface; also every word tested feeds the gold log. *Done:* running 24/7 on
minnaham. This pulled forward what had been a MEDIUM item and unblocks M2 and M3.

**N4 — Licensing cleared** ✅ **SETTLED** (D-012, 2026-07-26)
Mixed-licence product with per-source classification; everything we ship is cleared including public
serving. *Why:* the old Gate-0 framing was blocking every distribution rung unnecessarily. *Done:*
`thamizh-mcp/LICENSING.md` is canonical; stale "verify before redistribution" flags removed everywhere.

**N5 — Origin-classifier accuracy lift** 🔲 **OPEN — top code item**
Wire in the **Thamizhi Word Validator** and vendor a **loanword dataset**, so borrowings that carry no
orthographic marker stop returning `unknown`. *Why:* origin classification is objective 1 of the product,
and the புத்தகம் class of word — Sanskrit-derived but written in pure Tamil script — is exactly what a
Tamil user will test first. *Done:* புத்தகம் and கம்ப்யூட்டர் classify correctly with cited attestation, and
the honest-`unknown` rate on a held-out borrowing list drops measurably.

**N6 — Morphological-lift eval, full run** 🟡 **IN PROGRESS (paused)**
Bare LLM vs LLM + thamizh-mcp on ILAKKANAM-style questions, scored per linguistic category and grade.
*Why:* this is the v1 north-star metric (D-005) — the number that proves the product matters.
*Progress:* harness built (28 anchor-verified fixtures, Claude-first A/B runner); smoke run complete;
tool-invocation fix landed and re-validated; scoring hardened. *Remaining:* the full 3-run A/B over all
28 fixtures, now with a **grounded-prompt arm** added alongside the neutral arm (see §3.3). *Note:* the
achievable ceiling rose after N2, so re-measuring is more informative than the earlier attempt.

**N7 — Network-open sourcing session** 🔲 **OPEN — unblocks four other items**
One focused session with network access, to obtain and pin: Madras University Tamil Lexicon snapshot ·
TVA / government கலைச்சொல் snapshots · the Aalamaram treebank distribution plus its licence · the
Project Madurai digitized Tholkappiyam and Nannūl. *Why:* four separate roadmap items are all waiting on
the same kind of work, so batching it is the efficient move. *Done:* each source either pinned in `data/`
with its licence recorded, or explicitly marked unobtainable with the reason.

**N8 — நூற்பா-level grammar citations** 🟡 **PARTIAL** · ⛔ blocked on N7
*Progress:* the optional `SourceRef.verse` schema field landed (D-011, PR #11). *Remaining:* populate
actual நூற்பா numbers, which requires the pinned edition from N7. *Why:* today FST claims are
commit-pinned but grammar claims cite only a section name — an inconsistency a Tamil scholar will notice
immediately. *Done:* rule-table source references carry verse numbers; no number is ever written from
memory.

**N9 — Release rungs 0–1** 🔲 **OPEN** (unblocked by N4)
Ship installable artifacts: `uvx`-from-git, then PyPI, then Docker image on GHCR. *Why:* until this
happens, nobody outside the project can run the server. *Done:* a Tamil speaker with Claude Desktop or
Cursor can install and use it in one command.

**N10 — Create Hugging Face org + dataset v0** 🔲 **OPEN**
Create `huggingface.co/ief-global` and publish a first curated export from the live `transactions` table
— even a few hundred verified records. *Why:* locks the namespace, establishes the dataset-card and
versioning discipline early, and claims the white space identified in §5 before anyone else does.
*Done:* org exists; one versioned, licence-gated, contamination-guarded dataset published with a card.

**N11 — Registry listings** 🔲 **OPEN** (after N9)
List on the official MCP registry, mcp.so, Smithery, Glama, PulseMCP, awesome-mcp-servers, and the
tamil-nlp-catalog. *Why:* discovery — an unlisted MCP server is invisible. *Done:* listings live and
pointing at the released artifact.

**N12 — Testing-driven fixes from live use** 🟡 **ONGOING — current working mode**
Saran exercises the web app, reports gaps and UI issues, and those findings set the next build item.
*Why:* real use exposes the problems that matter, in an order the backlog cannot predict. *Done:* not a
finishable item — it is how work is currently prioritised.

### MEDIUM — reach real users, publish data, deepen the linguistics

**M1 — Storage abstraction: SQLite default, Postgres optional** 🔲 **OPEN** (required by D-013)
Introduce a thin storage layer in `store/knowledge.py`, which is currently SQLite-coupled
(`import sqlite3`, `INSERT OR REPLACE`, `AUTOINCREMENT`), and test both backends. *Why:* the hosted app
needs Postgres, but **nobody installing `thamizh-mcp` should ever be required to run containers or a
database.** Zero-config local install is a feature we protect deliberately. *Done:* both backends pass
the same test suite; SQLite remains the default with no configuration.

**M2 — The public app at `thamizh-ai.org`** 🔲 **OPEN** (domain purchased ✅; UI exists ✅ via N3)
A multi-user, long-running deployment: browser UI → FastAPI head → the same engine → Postgres, with
pinned anchor data baked into the container image. No queue, no load balancer; it is a small app.
*Naming note (D-013):* hyphenated because the joined form `thamizhai` reads as **தமிழை** — the accusative
of தமிழ் — to a native speaker, which buries the "AI" signal. *Hosting:* minnaham for now (real disk, no
cold starts, native foma), public access via Tailscale Funnel first. Cloud vendor deliberately not chosen
— containerising keeps the door open; decide with real traffic rather than with credits. *Why:* this is
the first channel that reaches ordinary Tamil speakers who will never install an MCP client. *Done:*
publicly reachable, with a privacy note stating that analyses are logged as linguistic data.

**M3 — Hugging Face Spaces demo** 🔲 **OPEN**
A demo Space that calls the same hosted API rather than bundling foma into the Space. *Why:* one backend,
and it puts the tool where ML researchers browse. *Done:* Space live, linked from the dataset cards.

**M4 — Full புணரியல் sandhi engine** 🔲 **OPEN — recorded product-quality goal**
Replace the conservative v1 behaviour (§3.2 item 2) with a proper Tholkappiyam புணரியல் engine that names
every விகாரம் — தோன்றல், திரிதல், கெடுதல் — across all cases, including verb-root changes such as வா→வந்.
*Why:* the product should stand on its own linguistic merit rather than on honest minimalism, and a Tamil
scholar judges us on exactly this. *Also:* it is a hard prerequisite for the generation track (§8), where
joining words correctly is not optional. *Done:* every join in the eval fixture set is named with its
Tholkappiyam rule; nothing is left unnamed except genuinely disputed cases, which are reported as disputed.

**M5 — Aalamaram integration** 🔲 **OPEN** · ⛔ blocked on N7 (licence)
Use the treebank to cross-check FST analyses at scale and to build eval fixtures that have real sentential
context. *Why:* today we validate morphology one word at a time against rules; a treebank lets us validate
against 10k annotated sentences. *Done:* a cross-check report over the treebank exists, and L3/L4 eval
fixtures are drawn from real sentences.

**M6 — Phrase and sentence support (v2)** 🔲 **OPEN** · ⛔ soft-blocked on M5
Add ThamizhiPOSt / ThamizhiLIP contextual disambiguation so the server can take a sentence, split it into
words, and choose the right analysis for each word *in context* rather than returning every possible
analysis. *Why:* Tamil surface forms are massively ambiguous in isolation; context resolves most of it.
This is also **Stage A of the generation track (§8)** — nothing further in §8 is possible without it.
*Done:* `analyze_sentence` returns one contextually-chosen analysis per word, with alternatives retained
and provenance intact.

**M7 — RAG over de-agglutinated roots** 🔲 **OPEN**
Embed lemma-and-morpheme sequences instead of raw agglutinated text, using multilingual-E5-class
embedders, and measure retrieval improvement with the same A/B method as N6. *Why:* embeddings of
BPE-fragmented Tamil miss the semantic root, so retrieval quality degrades before the LLM ever sees the
text. *Done:* a measured retrieval-lift number on a Tamil retrieval set.

**M8 — Instruction-tuning dataset exports** 🔲 **OPEN**
Template-generated question/answer records built from verified analyses — no LLM-invented content.
*Why:* this is the training data a future Tamil model needs, and it costs nothing but curation because
the underlying analyses already exist. *Done:* a versioned instruction dataset on Hugging Face.

**M9 — Central gold accumulation** 🟡 **PARTIALLY UNBLOCKED by M2** · relates to D-007 (still open)
Local installs accumulate gold data only locally. Central accumulation therefore happens through the
hosted instance plus versioned HF datasets: Git carries code and anchors, Hugging Face carries the grown
corpus. *Still open:* whether and how to pool contributions from *other people's* installs — that needs a
consent, privacy, and licensing model designed first, and is not required for v1.

### LONG — native Tamil models. Marked, deliberately not solutioned.

Trigger to revisit (D-006): gold corpus ≥ ~100k verified records **and** eval infrastructure routine.
Until both hold, these stay unscheduled — the prerequisites are exactly what NEAR and MEDIUM create.

**L1 — Grammar-first tokenizer** 🔲 **OPEN**
A Tamil tokenizer whose units are morphemes rather than statistical byte-pair fragments, trained on our
own segmentation gold. *Why:* it directly attacks token explosion, and our segmentation data is precisely
its training input — which is the whole reason N1's logging matters.

**L2 — Tamil small language model (SLM)** 🔲 **OPEN**
Vocabulary expansion plus continued pretraining of a compact open model (Gemma / Llama class), then
instruction-tuning on our curated data (M8), with existing HF Tamil corpora joining the pretraining mix.

**L3 — Hybrid serving** 🔲 **OPEN**
SLM/LLM routing, speculative decoding with a Tamil draft model, MoLoRA adapters. Architecture survey in
`Tamil-Small-Language-Models-by-Gemini.md`.

**L4 — Tanglish and code-mixed input** 🔲 **OPEN**
Tamil written in Latin script, and Tamil–English code-switching. Very common in real use; entirely
unhandled today.

**L5 — Mobile and on-device analyser** 🔲 **OPEN**
An offline analyser on a phone. Depends on L1/L2 producing something small enough to run there.

---

## 7. Standing risks and open items

**Sourcing (not blockers — tasks).** Aalamaram licence, unknown until the data is located (D-008) ·
TVA snapshot terms. Licensing itself is **settled** (D-012) — do not reintroduce Gate-0 language.

- **Madras Lexicon RESOLVED 2026-08-07 (D-016):** CC BY-NC-ND 2.0, © University of Madras, **and
  `robots.txt` disallows `/cgi-bin/`, the only query endpoint.** Consult-and-cite only, never
  bundled, adapter opt-in and off by default. Permission letters to TVA and DSAL are drafted in
  `sources/correspondence/`, not yet sent. Method for any lexicon:
  `sources/INTEGRATING-A-LEXICON.md`.
- **D-011 CLOSED 2026-08-02:** the Project Madurai Tholkappiyam/Nannūl editions ARE pinned. No
  longer an open task.
- **S2PT licence gap (D-017):** the வடசொல் word-lists we vendor have **no stated upstream
  licence**; an earlier "MIT" claim was withdrawn. The one genuine licence gap we ship.

**Honesty debt — say it out loud until fixed.** Sandhi joins are unnamed where no confident rule
fires (M4). Defensible, but only if we state it rather than let a user assume otherwise.

Two entries formerly on this list are **discharged** and should not be restated as debt:
- *Citations are section-level.* **Fixed by D-018 (2026-08-08):** `core/classical.py` serves the
  pinned texts at runtime, `SourceRef.verse_text` carries the நூற்பா verbatim, and the web app
  quotes it with Project Madurai attribution. Three decoder citations still carry `verse=null`
  because their நூற்பா are unverified — that residue is the honest remainder.
- *Origin returns `unknown` for unmarked borrowings.* **Largely fixed** across D-015…D-017:
  82 → **94 correct**, 23 → **11 unknown**, 1 wrong. Remaining unknowns are mostly modern loans
  absent from every source we hold.

**D-007 remains OPEN.** Pooling gold data contributed from other people's installs needs a consent,
privacy, and licensing design before any feature is built. The hosted instance's own logging is covered
by D-012 and a privacy note; that is a different question.

**ILAKKANAM release watch.** The dataset was still not public as of 2026-07-18. If it publishes, it
becomes our held-out test set and our own fixtures are demoted to dev. Re-check at every eval cycle.

**Tool invocation.** Fixed once (§3.3), but it can regress with any tool-description edit and it is
invisible unless measured. Treat "did the model call the tool at all?" as a first-class eval metric
forever, not a one-time bug.

**Unchanged from blueprint §10.** Origin classification is genuinely disputed for some words · evolving
sources vary in quality · objective 5 (native equivalents) is the highest hallucination-risk surface in
the product. Defences unchanged: report disagreement, carry provenance, attested-only.

**Not yet recorded as decisions.** The two generation-track landmines in §8.4 should become D-014 and
D-015 when — and only when — that track is actually scheduled. They are written down here so they are
not rediscovered late.

---

## 8. Generation track — from word analyser to sentence maker

**Status: written down, not scheduled.** Nothing in this section is committed work. Its purpose is to
record the architecture so the near-term choices do not accidentally foreclose it. v1 scope (§1) is
unchanged.

### 8.1 The reframe

`thamizh-mcp` does not become a language model by accretion. But "predict the next Tamil word" decomposes
into three separate problems, and only one of them is statistical:

| | The question | What answers it |
|---|---|---|
| 1 | Which **concept** comes next? | Semantics and discourse — genuinely needs a trained model |
| 2 | What **grammatical shape** must it take? | Case government, agreement, tense chaining — largely rule-governed; Tholkappiyam plus a treebank cover most of it |
| 3 | What **surface string** is that? | Inflection plus புணர்ச்சி — fully deterministic |

**We already own problem 3 and do not use it.** ThamizhiMorph is an analyser *cum generator*: the foma
FST runs in both directions. The server currently uses only the analysis direction. A Tamil word realizer
is sitting unused in the repository.

So the target architecture is not "a Tamil LLM". It is: **the model predicts a lemma plus a feature
bundle; the server deterministically realizes the surface form.** This is the generation-side version of
the de-agglutination argument we already make for analysis — instead of predicting over a 3–5×
fragmented BPE stream, prediction happens over a smaller space of meaningful units, and the hard,
error-prone morphology is handled by rules that cannot hallucinate.

### 8.2 The stages

Ordering matters in one specific way: **Stage C must precede Stage E.** A predictor without a realizer
just reproduces fragmented output.

| Stage | What it is | Roadmap tier | Depends on |
|---|---|---|---|
| **A** | Word → word-in-context: sentence segmentation and contextual disambiguation | = M6 | M5 |
| **B** | Structure: dependency parse of a Tamil sentence | MEDIUM (new) | A, M5 |
| **C** | The realizer: flip the FST — generate a surface form from lemma + features | MEDIUM (new) | M4 |
| **D** | The validator: check LLM-produced Tamil against the grammar | MEDIUM (new) | B, C |
| **E** | First real predictor: a statistical LM over morpheme units | LATE MEDIUM (new) | A, C |
| **F** | Grammar-first tokenizer → SLM | = L1, L2 | A, C, E and corpus scale |

**Stage A — word-in-context.** `segment_sentence`, `analyze_sentence`. Already on the roadmap as M6.
Non-negotiable prerequisite: "the next word" is undefined until "word in running text" is defined.

**Stage B — structure.** `parse_sentence` over Aalamaram's UD-adjusted dependency annotation. This lets
us ask *what grammatical slot comes next*, not merely *what token*. Unlocks C and D.

**Stage C — the realizer. Highest leverage-to-effort item in this section.**
`generate_form(lemma, features)` plus `join_words` — புணர்ச்சி applied constructively rather than
analytically. **This needs zero training.** An LLM that knows *what* to say but mangles Tamil morphology
can emit a lemma and a feature bundle and receive a correct surface form. This is where "sentence maker"
actually begins. Its hard prerequisite is M4: you cannot join words correctly if you cannot name the join.

**Stage D — the validator.** `validate_sentence`: is every form FST-parseable? does agreement hold? is
case government correct? Return corrections with rule citations. This is a **Tamil grammar checker**, and
it is shippable as a product in its own right — plausibly wanted by more people than the MCP server is.
It also supplies the quality metric that generation work needs.

**Stage E — the first genuine predictor, and it is cheap.** With A and C in place, a corpus can be
de-agglutinated into sequences of (lemma, feature-bundle) units. Train a modest language model over
*those units* — an n-gram model (KenLM) or a small neural one. `predict_next(context)` returns ranked
candidate lemma-plus-feature bundles; the Stage-C realizer turns the chosen one into a surface form.
Laptop-scale, no GPU, weeks rather than months. This is a native Tamil next-word predictor.

**Stage F — tokenizer and SLM.** Already L1 and L2. The Stage-A segmentation gold *is* the tokenizer's
training input, which is why transaction logging (N1) was worth doing first.

### 8.3 The cheap probe — recommended before committing to any of L1/L2

Before any SLM investment, run this experiment: take Tamil Wikipedia, de-agglutinate it with the existing
FST, train two n-gram language models — one over BPE tokens, one over morpheme units — and compare
**bits per character** and next-unit accuracy.

If morpheme-level prediction wins clearly, the entire long-term thesis is empirically de-risked and we
hold a publishable result nobody has produced. If it does not, we have saved a year. It costs a few days
and it is the highest-information-per-hour experiment available to the project. Best sequenced right
after N6, since it reuses the same measurement discipline.

### 8.4 Two landmines to settle before building any of this

**Landmine 1 — honest gaps do not survive generation.** "No attested analysis" is a valid output for an
analyser. Mid-sentence it is not: generation must always emit *something*. A fallback policy has to be
chosen deliberately — refuse the whole sentence? emit with a confidence flag? fall back to the LLM's own
form, explicitly marked as ungrounded? Without this decided in advance, non-negotiable #5 (honest gaps,
never LLM-as-source) erodes quietly. → record as **D-014** when the track is scheduled.

**Landmine 2 — attested-only versus rule-generated.** A realizer necessarily produces surface forms that
no lexicon has ever recorded. That is correct Tamil, but it is *rule*-attested, not *source*-attested.
Non-negotiable #3 (never invent a coinage) must be scoped narrowly to **lexical items** — coining a new
word — so that it does not accidentally forbid legitimate inflection of an existing word. The two
attestation classes need distinct names in the schema and distinct provenance handling.
→ record as **D-015** when the track is scheduled.

### 8.5 Why this is the right shape

Stages A–E are each independently shippable, each useful to real users on their own, and each a
prerequisite for F. There is no wasted motion in doing them in order — and if the SLM never happens, the
work still stands.

More importantly: the endpoint is a **hybrid**, not a replacement. A frontier LLM handles semantics; our
engine handles morphology and realization. That combination is plausibly better than a Tamil SLM alone
would ever be, and permanently cheaper to run. "Become an LLM" was never the goal; "be the half of the
system that Tamil most needs" is.

---

## 9. Key sources

- **ILAKKANAM** — *From Phonemes to Meaning: Evaluating LLMs on Tamil*, arXiv:2511.12387 (also published
  via ResearchGate). Local extraction: `From_Phonemes_to_Meaning.md`.
- **ThamizhiMorph** — Sarveswaran, Dias & Butt (2021), *Machine Translation* 35:37–70.
- **Aalamaram** — aclanthology.org/2024.wildre-1.11 (WILDRE @ LREC 2024).
- **Token explosion / de-agglutination argument** — `tamil_llm_tokenization_analysis_gemini.md`.
- **SLM feasibility and serving architectures** — `Tamil-Small-Language-Models-by-Gemini.md`.
- **Hugging Face Tamil shelf survey** — 2026-07-18, rationale recorded in D-009.
- Living channel/hosting docs: `distribution-roadmap.md`, `thamizh-mcp-hosting-plan.md` (note: the
  latter's Cloud Run recommendation is no longer the default — see D-013 and M2).
