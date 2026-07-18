# Thamizh MCP — Project Blueprint

> Phase 0 deliverable. Drafted 2026-07-02 from `thamizh-mcp-builder` assets/planning-blueprint-template.md.
> Status: **DRAFT — awaiting Saran's sign-off.** No code until this is approved.

## 1. Objective & scope

- **One-line objective:** Ground LLM answers about Tamil words in authentic Tamil sources, and grow coverage by self-enriching from evolving internet Tamil data (no hand-maintained dictionary).
- **In scope (v1):** single-word analysis → origin, root+meaning, formation, grammar, native equivalent   (for non-native words; attested-only). Single-word is the right v1: it matches the five objectives exactly, every grounding source is word-keyed, and it keeps the eval surface small and verifiable.
- **Borrowed languages to detect / suggest equivalents for:** Sanskrit (வடசொல்) · English · Urdu/Persian ·  Portuguese · Marathi · Telugu · Hindi. Coverage of equivalents is uneven by design; thin languages will often return "no attested equivalent" — that is an acceptable, common answer, not a failure.
- **Out of scope (v1):** phrase/sentence parsing (needs contextual POS — ThamizhiPOSt/LIP, later);
  word-form *generation* (`generate_forms` listed as optional/later); spell-check; transliterated
  (romanized) input; batch/corpus analysis.
- **Primary users:** native Tamil speakers wanting grounded, authentic answers via AI assistants (MCP head first; REST/web heads later per `distribution-roadmap.md`).

## 2. Design commitments (non-negotiable)

- **Tholkappiyam first** for every grammar claim; Nannūl only where Tholkappiyam does not codify the point  (chiefly the six-part பகுபத உறுப்பு labels). Every grammar output records `authority`.
- **Self-enriching, not hand-maintained:** rule-based morphology (ThamizhiMorph FST) for forms — no per-word upkeep; evolving internet sources for meaning/etymology/coverage/equivalents, cached with provenance into a knowledge store that grows with use.
- **Attested-only native equivalents (objective 5):** a candidate without an attestation source is dropped by the merge layer. Purist coinages are surfaced but marked `attestation: "proposed"` with register.
- **Provenance on every claim; honest gaps; no LLM-as-source; return all ambiguous analyses.**

## 3. Canonical output

- Contract: `word_analysis_schema.json` (from the builder skill's assets; copied into the repo at
  `src/thamizh_mcp/schema.py` as Pydantic models + kept as JSON Schema in `schemas/`).
- Sources carry `tier` (anchor/evolving) + `authority` (Tholkappiyam/Nannūl) + `retrieved` (ISO date or version pin). Schema changes get logged here.

## 4. Grounding sources (per output field, with tier)

| Field | Tier | Chosen source | Cross-check | Failure mode |
|---|---|---|---|---|
| normalized | — | open-tamil (NFC + grapheme split) | Nisaba (only if needed) | reject non-Tamil input with clear error |
| origin.class | evolving+anchor | Thamizhi Validator + loanword datasets (Kaggle, Indic-To-Pure-Tamil) | **Tholkappiyam** four-class rule; lexicon etymology tags | `class: "unknown"` + evidence collected so far |
| origin.borrowed_from | evolving | loanword datasets | Indo-Aryan loanword scholarship (cite as contestable) | `null` + gap note |
| lemma / root | anchor | ThamizhiMorph FST via flookup | open-tamil stemmer | no analysis → gap; never guess a lemma |
| meaning | anchor→evolving | Madras Tamil Lexicon (DSAL, pinned Sep-2023) → Tamil Wiktionary pull | AU-KBC WordNet, Cologne OTL | `senses: []` + gap note |
| formation | anchor | ThamizhiMorph tags → Tholkappiyam elements + Nannūl six-part labels | — | untagged form → gap (no invented split) |
| grammar | anchor | **Tholkappiyam** (Nannūl fallback), encoded rule table | UD Tamil treebank (eval only) | `word_class` unknown → gap |
| native_equivalent | anchor→evolving | TVA/govt கலைச்சொல் glossaries → Indic-To-Pure-Tamil, Wiktionary, தனித்தமிழ் lists | attestation required per candidate | `candidates: [], note: "no attested equivalent"` |

Access notes (Phase 1 to make concrete): Madras Lexicon has no official API — decide scrape-at-query vs offline digitized copy; TVA glossaries likewise need a scraped/offline snapshot pinned as anchor data; ThamizhiMorph FSTs are downloadable (Apache-2.0, pin release + cite Sarveswaran/Dias/Butt 2021).

### Phase 1 status (2026-07-02)

- **ThamizhiMorph — LOCKED.** foma 0.10.0 + FSTs pinned @ `adbacced` in `thamizh-mcp/data/fst/` (pins:  `data/PINS.md`). Verified live: மரம்→nom; மரத்தில்→loc|soc both kept. Guesser FSTs excluded by policy.
- **Indic-To-Pure-Tamil — LOCKED.** 2,063 mappings pinned @ `f734646` in `data/equivalents/`.
- **Tamil Wiktionary — adapter built** (httpx, timeout→honest NoEntry); NOT reachable from the Cowork sandbox (network allowlist) — unit tests mocked; live integration deferred to a network-open environment (Claude Code local / Cloud Run).
- **Madras Lexicon / TVA கலைச்சொல் — OPEN.** Also unreachable from this sandbox; recommend offline pinned snapshots (anchor discipline) — sourcing the digitized data is the next network-open-session job.
- **KnowledgeStore — DONE.** SQLite per-claim provenance, WAL, serialized writes; enrichment loop  (pull → write-back → cache-hit) proven by tests.

## 5. Enrichment & maintenance strategy

- **Knowledge store:** SQLite, keyed by normalized word; each resolved field stored with source, tier, retrieval date. Single-writer discipline (serialize writes).
- **Lookup order:** cache → anchors → evolving sources → write back (provenance-tagged).
- **Cross-check discipline:** an evolving fact is kept only if attributable AND consistent with an anchor or classical rule; otherwise surfaced low-confidence, never promoted to a grounded claim.
- **Refresh:** `enrich_word` (force re-pull one word) + `refresh_sources` (batch re-pull, e.g. recent misses).
- **NOT maintained by hand:** the word list. Forms come from the FST; lexical coverage accumulates from pulls.

## 6. Tool surface (from tool-design.md — confirmed)

- [x] `analyze_word` — workflow tool, main entry point; composes the rest, merges provenance, per-section gaps.
- [x] `classify_origin` · [x] `get_root` · [x] `get_meaning` · [x] `explain_formation` · [x] `explain_grammar`
- [x] `suggest_native_equivalent` — conditional (non-native only); attested-only hard rule.
- [x] `enrich_word` · [x] `refresh_sources` — local-cache writers (`readOnlyHint: false`).
- [ ] Optional/later: `validate_pure_tamil`, `generate_forms`, `transliterate`.

## 7. Stack decision

- **Committed: Python core + FastMCP, in-process.** The whole grounding stack (ThamizhiMorph/foma,  open-tamil, Stanza) is Python or native binary; no IPC boundary.
- **Packaging: uv** (pyproject.toml + uv.lock) — uvx-friendly for later MCP distribution.
- **Python deps:** fastmcp, httpx, anyio, pydantic, open-tamil, stanza (trim/defer on the single-word path per hosting plan). **System dep:** foma/flookup (documented in README + Dockerfile; not pip-installable).
- **Rejected:** TS MCP SDK + separate Python service (IPC for no benefit). Reopen only on a hard constraint.
- **Transport:** stdio (local v1) → streamable HTTP (Cloud Run, per `thamizh-mcp-hosting-plan.md`).
- **Concurrency (Phase 3 rule):** flookup subprocess + sync libs wrapped in `anyio.to_thread.run_sync`;
  `httpx.AsyncClient` for evolving pulls; bounded concurrency; timeout on every external call → honest gap on timeout; SQLite writes serialized.

## 8. Architecture sketch

```
input word → normalize (open-tamil)
  → knowledge store (SQLite cache: hit? serve with provenance)
  → miss: source adapters (uniform interface: word → fields + provenance + tier)
      anchors: ThamizhiMorph(flookup) · Madras Lexicon · Tholkappiyam rule table · TVA கலைச்சொல்
      evolving: Tamil Wiktionary · loanword datasets · தனித்தமிழ் lists
  → analysis core (FST-tag→உறுப்பு decoder · case→வேற்றுமை mapper · authority tagger · attestation filter)
  → merge + write back to store
  → heads: MCP tools (v1) | FastAPI REST (later) | CLI (later) — all over one plain-Python engine
```

Core engine stays a plain library (`analyze_word(word) -> WordAnalysis`) so the heads stay thin
(per `distribution-roadmap.md`). Pin anchor versions; pin retrieval date + provenance for evolving facts.

## 9. Evaluation plan (Phase 4)

- Fixture words: மரம் (native, simple) · மரத்தில் (inflected, sandhi split) · புத்தகம் (வடசொல் → நூல்) ·
  கம்ப்யூட்டர் (English → கணினி) · ஜன்னல் (Portuguese → சாளரம்) ·
  a loan with NO attested equivalent (candidate: ஜிலேபி or similar Urdu/Hindi food loan — hand-verify in
  Phase 4 that no கலைச்சொல்/Wiktionary equivalent exists before locking) ·
  a disputed-origin word (candidates: உலகம் (உலகு vs Skt loka) or அரசன் (அரசு vs Skt rājan) — both have real
  scholarly dispute; hand-verify and pick one).
- Hand-verify every expected value against sources + authority before locking answers.
- Behavioural tests: anchor-miss triggers evolving pull (cached, provenance-tagged); miss-everywhere returns
  explicit gap; unattested equivalent returns empty candidates + note — no fabrication, no invented coinage.
- Run baselines isolated from the project folder (can't read skill files).

## 10. Open questions / risks

- **Madras Lexicon access** — no official API: scrape at query time vs offline copy. (Phase 1 decision.)
- **TVA/govt கலைச்சொல் access** — same question; these are anchors, so an offline pinned snapshot is cleaner.
- **Wiktionary licence** — CC BY-SA share-alike: live query vs cache/serve has legal weight; the knowledge store DOES cache — resolve before any public release (flagged in `distribution-roadmap.md` audit).
- **Evolving-source quality** — cross-check discipline is the guardrail; monitor the low-confidence rate.
- **Objective 5 hallucination risk** — highest in the server; attested-only + merge-layer drop is the defense.
- **Origin disputes** — report competing claims in `alternatives`; never adjudicate.
- **Ambiguity** — ThamizhiMorph returns multiple analyses; keep all, disambiguation is downstream.
- **E:\ tooling gotcha (build-process risk)** — Write/Edit truncate >~3.3KB on this mount; all repo files are written via bash to the mount path and verified on disk (wc/tail) before being trusted.

## 11. Milestones

1. Blueprint signed off (Phase 0 — this doc) →
2. Anchors reachable + SQLite knowledge store stood up (Phase 1) →
3. Tool surface finalized incl. enrichment (Phase 2) →
4. Server runs locally: scaffold → adapters → engine → tools, non-blocking throughout (Phase 3) →
5. Eval set passes incl. honest-gap + enrichment behaviours (Phase 4).

First implementation move after sign-off (already agreed): scaffold `thamizh-mcp/` (uv, src layout,
core/adapters/store split) + stub `analyze_word` returning a schema-valid, all-gaps object.

## 12. Research grounding & program context (added 2026-07-10)

Two papers now anchor the *why* of this server; digests live in the builder skill's
`references/research-grounding.md`.

- **ILAKKANAM (arXiv 2511.12387)** — first Tamil linguistic benchmark (820 school-exam questions,
  Grades 1–13, categories L1 phonetics / L2 phonology / L3 morphology / L4 syntax / L5 semantics / F fact).
  Findings: best frontier model 79.6% (Gemini 2.5), Claude Sonnet 4.5 71.1%, open-source 37.9–60.7%;
  accuracy declines with grade; performance reflects exposure, not understanding. **Implication:** the
  server's grounding targets exactly the weak spots (L3 morphology, higher grades).
- **ThamizhiMorph (Sarveswaran/Dias/Butt 2021)** — the FST anchor we wrap (D-001). On a 612-word textbook
  corpus: 93.3% analysis coverage, 100% right-analysis and 97.9% right-lemma among successes; residual
  errors mostly OOV → OOV words route to the enrichment loop, never to guesses (guesser FSTs stay excluded).
- **De-agglutination rationale** (`tamil_llm_tokenization_analysis_gemini.md`): BPE token explosion costs
  Tamil ~3–5× context and misaligns RAG embeddings; this server is the architectural fix — a grounding +
  de-agglutination layer in front of any LLM, no base-model retraining required.

**Eval addendum (extends §9):** §9's fixtures remain *server regression* evals. The *product* metric is
**morphological lift** — SP(model + thamizh-mcp) − SP(model alone) on ILAKKANAM-style questions, per
category and grade band (D-005). Owned by the `thamizh-eval` skill (Claude-first harness; self-built
fixtures until the ILAKKANAM dataset is published). Fixture words are flagged in the knowledge store so
they never leak into published training data.

**Data addendum (extends §5):** transaction logging is a first-class output, not telemetry — every
resolved analysis accumulates provenance-tagged gold data (future SLM corpus). Curation/publishing rules
are owned by the `thamizh-data-curation` skill; release/hosting by `thamizh-release` (D-004).

**Program roadmap:** near/medium/long-term tracks (SLM explicitly long-term, not being solutioned) live in
`TAMIL-HIGH-RESOURCE-ROADMAP.md`.
