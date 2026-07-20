# Thamizh MCP — DESIGN (top-level)

> The front door of `ief-global/thamizh-mcp-design`. Revised **2026-07-18** (first early-stage objectives
> review). Supersedes `TAMIL-HIGH-RESOURCE-ROADMAP.md` as the program map (that file now points here).
> Companion docs: `Thamizh-MCP-blueprint.md` (server spec) · `CODE-STATUS.md` (code-side read-across) ·
> `thamizh-mcp-builder/references/DECISIONS.md` (decision log) · the four skills (builder v6, eval,
> data-curation, release).

## 1. Objectives (unchanged)

**Program goal:** move Tamil from low-resource toward a first-class language in the LLM ecosystem —
a native Tamil speaker should get the grounded, fluent, efficient AI experience an English speaker gets.

**Product (v1):** given a Tamil word, return a grounded, authentic analysis — origin (இயற்சொல் vs borrowed),
root+meaning, formation (பகுபதம்/புணர்ச்சி), grammar (Tholkappiyam-first), attested native equivalent.
Non-negotiables hold: Tholkappiyam first · self-enriching, not hand-maintained · attested-only equivalents ·
provenance on every claim · honest gaps, no LLM-as-source.

**Evidence of the gap (unchanged):** ILAKKANAM — frontier models 71–80% on Tamil linguistics, declining with
complexity, exposure-not-understanding; BPE token explosion (~3–5× context cost); thin-but-real tooling base.

## 2. Operating model (new, formalized 2026-07-18)

Two repos, two roles, one loop:

| | `thamizh-mcp-design` (private) | `thamizh-mcp` (public) |
|---|---|---|
| Owner role | **Design** — Cowork with Fable/high-end model: plan, architect, decide, revise | **Build** — Claude Code (minnaham): implement, test, PR |
| Carries | blueprint, DESIGN.md, decision log, skills, research digests | code, tests, pinned anchor data, CLAUDE.md |
| Sync in | `CODE-STATUS.md` written from the code side | skills + DESIGN/blueprint read from the design side |

Rules: never nest the repos; design docs never enter the public repo. Git runs only on Saran's boxes
(sandbox corrupts `.git` on the E:\ mount); Cowork authors files via bash and Saran commits. Decisions land
in DECISIONS.md (append-only) before they land in code. Both repos live under the **`ief-global`** GitHub
org (D-010 records the operating model + org move).

## 3. Progress review — do the design principles hold? (as of CODE-STATUS 2026-07-18)

**Verdict: they hold.** v1 core is COMPLETE — 9 MCP tools live (all of blueprint §6 core), 87 tests,
engine/adapters/store shaped exactly as blueprint §8, transaction logging on by default with the
`eval_fixture` contamination guard (the design's data-flywheel and eval-hygiene requirements, built as
specified). The two code divergences are *honest-minimal* implementations, not principle violations:

1. **`classify_origin` subset** — rule-based (Grantha detection + phonotactics + FST parse + I2PT
   attestation) without the Thamizhi Validator or a loanword dataset yet; pure-script borrowings like
   புத்தகம் return honest `unknown`. Consistent with gaps-not-guesses; scheduled as the next accuracy lift.
2. **Conservative sandhi naming** — joins named only where a confident classical rule applies; harder
   விகாரம் left unnamed rather than invented. Correct per the no-invented-split rule. The **full
   Tholkappiyam புணரியல் sandhi engine** (name every தோன்றல்/திரிதல்/கெடுதல், incl. வா→வந்) is now a recorded
   product-quality goal (medium-term, §6).

One structural insight from the code side is promoted to the design (D-007): local installs accumulate
gold data only locally; **central accumulation = the hosted instance + the versioned HF datasets**. Git
carries code + anchors; HF carries the grown corpus. A community "contribute your data" path stays OPEN
(consent/privacy/license model must be decided first — not needed for v1).

## 4. Source-strategy revision (2026-07-18)

**I2PT verdict:** stale (last activity years old, 2,063 rows) but keep — it is pinned (`f734646`), attested,
and does its one job (Indic→pure-Tamil mappings). Nothing replaces it; it gets *supplemented*:

- **Equivalents enrichment path (objective 5):** TVA/govt கலைச்சொல் offline snapshots (anchor; the open
  network job) + Tamil Wiktionary `{{சொல்வளம்N}}` synonym-template mining (evolving; adapter already parses
  the template format) + I2PT as-is. This is where equivalents coverage grows — not Aalamaram.
- **Aalamaram — ADOPTED as a new anchor-tier source (D-008), for what it actually is:** the largest public
  Tamil treebank (~10k sentences; POS, NER, morphological parsing, dependencies, UD-adjusted for Tamil
  clitics/segmentation; WILDRE@LREC 2024; Sarveswaran co-author — same lineage as ThamizhiMorph/ILAKKANAM).
  It is a **treebank, not an equivalents dataset** — the earlier "replace I2PT with Aalamaram" framing is
  corrected in the decision log. It grounds: cross-checking ThamizhiMorph analyses at scale, L3/L4 eval
  fixtures with real sentential context, phrase-level v2 (with ThamizhiPOSt), and SLM training corpus.
  **Blocking pre-step:** locate the actual data distribution + verify its license (not on HF; no public
  GitHub repo found from the sandbox; paper PDF / authors are the lead) — network-open job, same bucket as
  the Madras Lexicon + TVA snapshots.
- **Verse-level classical grounding (D-011, added 2026-07-19):** pin digitized **Tholkappiyam + Nannūl**
  editions (Project Madurai / Tamil Virtual Academy / better gold source at pinning time) as
  version-locked anchors, and upgrade rule-table `SourceRef`s from section names to **நூற்பா numbers**
  (optional `verse` field — additive). Closes the gap that grammar claims cite only at section level
  while FST claims are commit-pinned.
- **ILAKKANAM:** already fully incorporated (blueprint §12, thamizh-eval, D-005). The ResearchGate item
  ("Evaluating Linguistic Knowledge of LLMs in Tamil: The ILAKKANAM Benchmark") is the same work's
  published form. Dataset still not public as of 2026-07-18 — thamizh-eval's check-else-build-fixtures
  procedure stands; re-check at each eval cycle.

## 5. GitHub × Hugging Face architecture (new, D-009)

Create **huggingface.co/ief-global** (mirror of the GitHub org). Division of labor:

| Platform | Carries | Why |
|---|---|---|
| GitHub `ief-global` | code (public), design (private), pinned anchor data, releases | version control, PRs, registries |
| HF `ief-global` | **curated gold datasets** (gold/silver/disputed splits, cards, versions) · **Spaces demo** of the analyzer · (later) the SLM | data versioning + discovery where the ML community looks; free demo hosting |

**White-space finding (2026-07-18 survey):** HF's Tamil shelf is speech/ASR/TTS, raw corpora, sentiment,
and the tamil-llama/Tamil-Mistral family. There is **no morphological-segmentation gold, no
loanword→equivalent dataset, no origin-label dataset** — precisely our three exports. First-mover datasets
here are the org's credibility anchor and the SLM's future training base.

**The flywheel:** server usage → `transactions` log → `thamizh-data-curation` (verify, license-gate,
contamination-guard) → versioned HF datasets → community use + tokenizer/SLM training → better Tamil AI →
more server usage. HF is also an **input**: existing corpora (textbook datasets, cleaned OSCAR, Wikipedia
dumps) feed SLM-era pretraining, and HF benchmarks (MILU etc.) join the eval context. Not adopted now:
mirroring third-party models under the org (maintenance surface, no near-term value).

Sequencing: create org + publish dataset v0 (even small — hundreds of verified records) in the near term to
lock the namespace and the card/versioning discipline; the Spaces demo lands with/after the hosted instance
(it can call the Cloud Run API rather than bundling foma into the Space — one backend, per hosting plan).

## 6. Revised roadmap (absorbs TAMIL-HIGH-RESOURCE-ROADMAP.md)

**NEAR (now – ~3 mo):**
1. Origin-classifier lift: wire Thamizhi Word Validator + a vendored loanword dataset (fixes புத்தகம்-class
   honest-unknowns) — top code item.
2. **Run the morphological-lift eval** (thamizh-eval; fixtures → A/B → per-category report). Flagship.
3. Network-open sourcing session: Madras Lexicon + TVA கலைச்சொல் snapshots **+ locate/license Aalamaram**.
4. Pin digitized Tholkappiyam + Nannūl editions and add நூற்பா numbers to rule-table SourceRefs
   (D-011) — batch the text sourcing with the same network-open session.
5. License audit Gate-0 (I2PT MIT verify is overdue) → release rungs 0–1 (uvx → PyPI + Docker/GHCR).
6. **Create HF `ief-global` org**; first curation export (dataset v0) from the live transactions table.
7. Registry + tamil-nlp-catalog listings (after Gate-0).

**MEDIUM (~3–12 mo):**
8. Hosted reference instance (Cloud Run + Cloudflare, per hosting plan) + REST head → central gold
   accumulation begins (D-007).
9. Public web tool (ief-global.org) + **HF Spaces demo** calling the same API.
10. **Full புணரியல் sandhi engine** (the recorded product-quality goal — every விகாரம் named, verb-root
   changes included).
11. Aalamaram integration (cross-check + eval fixtures); phrase/sentence v2 (ThamizhiPOSt + Aalamaram).
12. RAG over de-agglutinated roots; instruction-dataset exports; dataset versions grow on HF.

**LONG (12+ mo — marked, NOT solutioned):** Tamil SLM (grammar-first tokenizer trained on our segmentation
gold; continued pretraining; instruction-tuning on our curated data; HF corpora join pretraining mix) ·
hybrid serving (routing/speculative/MoLoRA) · Tanglish · mobile · on-device. Trigger to revisit: gold corpus
≥ ~100k verified records + eval infra routine (D-006). Decide the D-007 community-contribution
consent/licensing model before any pooling feature.

## 7. Standing risks / open items

- **Licenses:** I2PT MIT verify (overdue, vendored+public) · Madras Lexicon + TVA terms before snapshots
  ship · Wiktionary CC BY-SA position before the hosted instance serves cached text · Aalamaram license
  unknown until located. Gate-0 blocks every public rung.
- **D-011 (scheduled):** grammar citations are section-level until the Tholkappiyam/Nannūl editions
  are pinned and நூற்பா numbers land in SourceRefs — say "section-level" honestly in public claims
  until then.
- **D-007 (OPEN):** community gold-pooling needs consent/privacy/license design first.
- **ILAKKANAM release watch** — if it publishes, it becomes the held-out test set (our fixtures stay dev).
- Origin disputes, evolving-source quality, objective-5 hallucination risk — unchanged from blueprint §10,
  defenses unchanged.

## Key sources

ILAKKANAM: arXiv:2511.12387 (+ published form on ResearchGate) · ThamizhiMorph: MT 35:37–70 (2021) ·
Aalamaram: aclanthology.org/2024.wildre-1.11 (WILDRE 2024) · HF survey 2026-07-18 (see D-009 rationale) ·
`distribution-roadmap.md`, `thamizh-mcp-hosting-plan.md` (living channel/hosting docs, unchanged).
