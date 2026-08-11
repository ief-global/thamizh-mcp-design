# Thamizh MCP — Project Blueprint

> Phase 0 deliverable. Drafted 2026-07-02 from `thamizh-mcp-builder` assets/planning-blueprint-template.md.
> Status: **SIGNED OFF and BUILT.** Phases 0–3 are complete and the server has been running since
> 2026-07; Phase 4 (eval) is paused and resumable. The header used to read *"DRAFT — awaiting
> Saran's sign-off. No code until this is approved"*, which was the single most misleading line in
> the repo by 2026-08.
>
> **This document is the Phase-0 PLAN and is kept as that record.** Its section numbers are cited
> throughout the code (`blueprint §2`, `§3`, `§4`, `§6`, `§8`, `§10`, `§12`), so they are never
> renumbered. Where a plan has since been superseded, the change is annotated in place rather than
> rewritten away — see the as-built notes below and §13.
>
> **Authoritative for CURRENT state:** `CODE-STATUS.md`, `DECISIONS.md` (D-001…D-018), and the code
> repo's `CLAUDE.md`. As of 2026-08-11: nine MCP tools + web/REST + CLI, **218 tests**, origin
> **94 correct / 11 unknown / 1 wrong** on the 108-word sweep, formation 26/29 in-scope, and நூற்பா
> quoted at runtime (D-018).

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

- Contract: **`thamizh-mcp/src/thamizh_mcp/schema.py` is authoritative** (Pydantic), mirrored as JSON
  Schema in `thamizh-mcp/schemas/word_analysis_schema.json`.
  ⚠️ **As-built note:** the builder skill's `assets/word_analysis_schema.json` was the Phase-0 seed
  and has since DIVERGED — it is ~7.8 KB against the shipped 15 KB and lacks `verse_text` (D-018),
  `tamil_alternatives` and the shared `equivalent_candidate` definition (D-015). Treat the skill
  asset as a historical template, never as the contract. Same reasoning as `DECISIONS.md` moving to
  the repo root: a live artifact should not be frozen into a skill package.
- Sources carry `tier` (anchor/evolving) + `authority` (Tholkappiyam/Nannūl) + `retrieved` (ISO date or version pin). Schema changes get logged here.

## 4. Grounding sources (per output field, with tier)

| Field | Tier | Chosen source | Cross-check | Failure mode |
|---|---|---|---|---|
| normalized | — | open-tamil (NFC + grapheme split) | Nisaba (only if needed) | reject non-Tamil input with clear error |
| origin.class | evolving+anchor | **AS BUILT:** en.wiktionary etymology templates (D-015, primary) → Sanskrit-To-Pure-Tamil வடசொல் lists (D-017, provisional, conf 0.55) → Google Dakshina English-loan artifact (anchor, gated) → Tholkappiyam orthographic rules. *Planned but NOT wired:* Thamizhi Validator, Kaggle loanword set | **Tholkappiyam** four-class rule; per-SENSE origin for homographs (D-015) | `class: "unknown"` + evidence collected so far |
| origin.borrowed_from | evolving | loanword datasets | Indo-Aryan loanword scholarship (cite as contestable) | `null` + gap note |
| lemma / root | anchor | ThamizhiMorph FST via flookup | open-tamil stemmer | no analysis → gap; never guess a lemma |
| meaning | evolving | **AS BUILT:** Tamil Wiktionary pull only. Madras Lexicon is NOT wired and is BLOCKED (D-016 — CC BY-NC-ND *and* robots.txt disallows its only query endpoint) | AU-KBC WordNet, Cologne OTL — Cologne assessed 2026-08-08: glosses only, no etymology | `senses: []` + gap note |
| formation | anchor | ThamizhiMorph tags → Tholkappiyam elements + Nannūl six-part labels | — | untagged form → gap (no invented split) |
| grammar | anchor | **Tholkappiyam** (Nannūl fallback), encoded rule table | UD Tamil treebank (eval only) | `word_class` unknown → gap |
| native_equivalent | evolving | **AS BUILT:** Sanskrit-To-Pure-Tamil (S2PT) lists + per-sense `tamil_alternatives` from Wiktionary synonyms (D-015). TVA/govt கலைச்சொல் is the intended ANCHOR upgrade but is still a stub — permission letter drafted, not sent | attestation required per candidate | `candidates: [], note: "no attested equivalent"` |

Access notes (Phase 1 to make concrete): ~~Madras Lexicon has no official API — decide scrape-at-query vs offline digitized copy~~ **ANSWERED 2026-08-07 (D-016): NEITHER is available.** The ND term rules out an offline digitized copy and `robots.txt` disallows `/cgi-bin/`, which is the only query endpoint. Consult-and-cite only, pending written permission. Method for any lexicon: `sources/INTEGRATING-A-LEXICON.md`. TVA glossaries likewise need a snapshot; ThamizhiMorph FSTs are downloadable (Apache-2.0, pin release + cite Sarveswaran/Dias/Butt 2021).

### Phase 1 status (2026-07-02)

- **ThamizhiMorph — LOCKED.** foma 0.10.0 + FSTs pinned @ `adbacced` in `thamizh-mcp/data/fst/` (pins:  `data/PINS.md`). Verified live: மரம்→nom; மரத்தில்→loc|soc both kept. Guesser FSTs excluded by policy.
- **Sanskrit-To-Pure-Tamil (S2PT) — LOCKED, but PROVISIONAL.** 2,063 mappings pinned @ `f734646`. Renamed 2026-08-08: upstream is `narVidhai/Sanskrit-To-Pure-Tamil-Dictionary` and GitHub's redirect hid the old name. ⚠️ **The "MIT" licence claim was WITHDRAWN (D-017)** — upstream has no LICENSE file. The one genuine licence gap we ship.
- **Tamil Wiktionary — adapter built and LIVE** (httpx, timeout→honest NoEntry). The sandbox-unreachable note is obsolete: it runs against the real source on minnaham. **en.wiktionary etymology** was added later as a separate adapter and is now the primary origin signal (D-015).
- **Madras Lexicon — CLOSED as unavailable (D-016);** see the access note above. **TVA கலைச்சொல் — still OPEN**, now with a drafted permission letter (`sources/correspondence/`) rather than a scraping plan.
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

- ~~**Madras Lexicon access**~~ — **RESOLVED 2026-08-07 (D-016):** CC BY-NC-ND 2.0 *and* robots-blocked. Consult-and-cite only; neither scraping nor an offline copy is open to us.
- **TVA/govt கலைச்சொல் access** — **still OPEN**, and now the highest-value sourcing task: it would retire the S2PT licence gap. Permission letter drafted (`sources/correspondence/`), not sent. A CC0 precedent exists via TVA's Wikimedia collaboration.
- ~~**Wiktionary licence**~~ — **RESOLVED 2026-07-26 (D-012):** CC BY-SA is cleared for use *including public serving*, with attribution, never relicensed. Caching is fine. Do not reintroduce this as a blocker.
- **NEW — source provenance is not yet systematic (D-017 ask, unbuilt).** S2PT was quietly load-bearing with no stated licence for weeks. The fix is a machine-readable source registry with confidence capped by source GRADE and the grade surfaced in the answer. Framing: authenticity comes from every claim carrying a graded, citable provenance the user can check — not from every source being impeccable.
- **Evolving-source quality** — cross-check discipline is the guardrail; monitor the low-confidence rate.
- **Objective 5 hallucination risk** — highest in the server; attested-only + merge-layer drop is the defense.
- **Origin disputes** — report competing claims in `alternatives`; never adjudicate.
- **Ambiguity** — ThamizhiMorph returns multiple analyses; keep all, disambiguation is downstream.
- ~~**E:\ tooling gotcha**~~ — obsolete: the build moved to minnaham (Linux). The *current* tooling gotchas are different and live in the code repo's `CLAUDE.md`: the Edit tool fails to match blocks containing Tamil text (Unicode normalization — patch via a `python3` script instead), and `gh pr create/edit` is broken here (use `gh api`).

## 11. Milestones

1. ✅ Blueprint signed off (Phase 0 — this doc)
2. ✅ Anchors reachable + SQLite knowledge store stood up (Phase 1)
3. ✅ Tool surface finalized incl. enrichment (Phase 2) — nine tools live
4. ✅ Server runs locally: scaffold → adapters → engine → tools, non-blocking throughout (Phase 3).
   Went further than planned: web/REST + CLI heads over the same engine, and CI gating every PR.
5. ⏸ Eval set passes incl. honest-gap + enrichment behaviours (Phase 4) — **paused, harness
   resumable** (D-005). The 108-word quality sweep (`scripts/quality_sweep.py`) is the interim
   measurement and is not a substitute for it.

~~First implementation move after sign-off: scaffold `thamizh-mcp/` + stub `analyze_word`~~ — done
2026-07. The `core/adapters/store` split held and is still the shape of the code.

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

## 13. As-built addendum — decisions after Phase 0 (added 2026-08-11)

Phase 0 could not have anticipated these; they are recorded here so this document does not read as
current when it is a plan. Full rationale in `DECISIONS.md`.

- **D-011 — classical texts PINNED** (Project Madurai, verse-addressable, checksummed). Closes the
  "citations are section-level" honesty debt at the data layer.
- **D-014 — grammar rules are cited DATA tables** (`data/grammar/*.json`), each with a
  `source_priority` block, enforced by `tests/test_citations.py`.
- **D-015 — origin is per SENSE, not per headword.** A homograph is two words sharing a form; கால் is
  leg (inherited) *and* time (Sanskrit). Saran's ruling: **the Tamil sense leads at headword level for
  ANY source language**, and the borrowed sense still hands back its Tamil word. This changed the
  canonical output (`Origin.senses[]`, `tamil_alternatives`) — §3's contract grew accordingly.
- **D-016 — tier and licence are INDEPENDENT axes.** Every source now declares a *redistribution
  mode*: redistribute / serve-with-attribution / consult-and-cite. §4's table records tier only; the
  mode lives in `LICENSING.md` and `sources/INTEGRATING-A-LEXICON.md`.
- **D-017 — the S2PT licence claim was withdrawn**, and the systemic fix (a source registry with
  graded confidence) is still unbuilt. §10 carries it as an open risk.
- **D-018 — the pinned texts are read at RUNTIME.** `SourceRef.verse_text` quotes the நூற்பா and the
  web app displays it with Project Madurai attribution. Until this landed, `data/classical/` was only
  read by a test — the promise of Tholkappiyam-first grounding was kept at design time but not shown
  to a user.
- **Grammar concept map** (`thamizh-mcp/data/grammar/concept_map.json`) — every concept the decoder
  relies on, tied to the நூற்பா that *states* it, with anything merely *inferred* marked as such and
  awaiting ruling. Built because recall had already been mistaken for citation once.
