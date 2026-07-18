# THAMIZH MCP — Project Blueprint

> Fill this in during Phase 0 and get the user's sign-off before writing code. Save the completed copy as
> `THAMIZH-MCP-blueprint.md` in the project folder.

## 1. Objective & scope
- **One-line objective:** Ground LLM answers about Tamil words in authentic Tamil sources, and grow coverage
  by self-enriching from evolving internet Tamil data (no hand-maintained dictionary).
- **In scope (v1):** single-word analysis → origin, root+meaning, formation, grammar, native equivalent
  (for non-native words; attested-only).
- **Borrowed languages to detect / suggest equivalents for:** Sanskrit (வடசொல்) · English · Urdu/Persian ·
  Portuguese · Marathi · Telugu · [others?] — coverage of equivalents is uneven; thin languages will often
  return "no attested equivalent".
- **Out of scope (v1):** [phrase/sentence parsing? form generation? spell-check?]
- **Primary users:** native Tamil speakers wanting grounded, authentic answers.

## 2. Design commitments (non-negotiable)
- **Tholkappiyam first** for every grammar claim; Nannūl only as fallback (record `authority`).
- **Self-enriching, not hand-maintained:** rule-based morphology for forms (no upkeep) + evolving
  internet sources for meaning/etymology/coverage, cached into a growing knowledge store.

## 3. Canonical output
- Contract: `assets/word_analysis_schema.json` (sources carry `tier` + `authority`). Changes logged here.

## 4. Grounding sources (per output field, with tier)

| Field | Tier | Chosen source | Cross-check | Failure mode |
|---|---|---|---|---|
| normalized | — | open-tamil / Nisaba | — | |
| origin.class | evolving+anchor | Thamizhi Validator + loanword data | **Tholkappiyam** வடசொல் rule | |
| origin.borrowed_from | evolving | loanword datasets | Indo-Aryan scholarship | |
| lemma / root | anchor | ThamizhiMorph (rule-based, no upkeep) | open-tamil stemmer | |
| meaning | anchor→evolving | Madras Lexicon → Tamil Wiktionary | AU-KBC WordNet | |
| formation | anchor | ThamizhiMorph → Tholkappiyam elements + Nannūl labels | | |
| grammar | anchor | **Tholkappiyam** (Nannūl fallback) | | |
| native_equivalent (non-native only) | anchor→evolving | கலைச்சொல்/TVA/govt → Indic-To-Pure-Tamil, Wiktionary, தனித்தமிழ் | attestation required | "no attested equivalent" |

## 5. Enrichment & maintenance strategy
- **Knowledge store:** local cache (e.g. SQLite) keyed by normalized word; each field stored with source,
  tier, retrieval date.
- **Lookup order:** cache → anchors → evolving sources → write back.
- **Cross-check discipline:** an evolving-source fact is kept only if attributable AND consistent with an
  anchor or classical rule; otherwise surfaced as low-confidence, never promoted to a grounded claim.
- **Refresh:** `enrich_word` / `refresh_sources` to re-pull thin or stale entries so coverage grows.
- **What is NOT maintained by hand:** the word list. Forms come from the FST; lexical coverage from pulls.

## 6. Tool surface
- From `references/tool-design.md`: [ ] analyze_word [ ] classify_origin [ ] get_root [ ] get_meaning
  [ ] explain_formation [ ] explain_grammar [ ] suggest_native_equivalent [ ] enrich_word [ ] refresh_sources
  [ ] (optional) validate_pure_tamil / generate_forms / transliterate

## 7. Stack decision
- **Decision (committed): Python core (FastMCP).** Tamil-NLP ecosystem (ThamizhiMorph, open-tamil, Stanza) is
  Python/native-binary; MCP server runs in-process — no IPC boundary.
- **Rejected:** TS MCP SDK + separate Python service — adds IPC for no linguistic benefit. Reopen only on a
  hard constraint (must embed in an existing Node/TS codebase, or deployment mandates the TS SDK).
- **Transport:** stdio (local) / streamable HTTP (remote).

## 8. Architecture sketch
- Source adapters (uniform interface, tier-aware) → knowledge store + enrichment loop → analysis core
  (FST-tag → உறுப்பு decoder, case mapper, Tholkappiyam-first authority tagger) → MCP tool layer → agent.
- Pin anchor versions; pin retrieval date + provenance for evolving facts.

## 9. Evaluation plan (Phase 4)
- Fixture words: மரம் (native simple) · மரத்தில் (inflected, sandhi) · புத்தகம் (வடசொல் → நூல்) ·
  கம்ப்யூட்டர் (English → கணினி) · ஜன்னல் (Portuguese → சாளரம்) · [a loan with NO attested equivalent] ·
  [one disputed-origin word].
- Hand-verify expected origin/root/meaning/formation/grammar/native-equivalent with sources + authority.
- Also test: a word missing from anchors triggers an evolving pull (cached, provenance-tagged); a word
  missing everywhere — and an equivalent with no attestation — returns an explicit gap (no fabrication, no
  invented coinage).
- Reference standard for a good Phase 0 blueprint: the eval-1 with-skill output. Run baselines isolated from
  the project folder.

## 10. Open questions / risks
- Lexicon access has no official API — scrape vs offline copy for the Madras Lexicon anchor.
- Evolving-source quality control — the cross-check discipline is the guardrail; monitor low-confidence rate.
- Native-equivalent (obj 5) — highest hallucination risk; enforce attested-only + drop unsourced candidates.
  Coverage is uneven by source language; "no attested equivalent" must be an acceptable, common answer.
- Origin disputes — server reports competing claims, doesn't adjudicate.
- ThamizhiMorph returns multiple analyses — keep all; disambiguation is downstream.

## 11. Milestones
1. Blueprint signed off (Phase 0) → 2. Anchors reachable + knowledge store stood up (Phase 1) →
3. Tools designed incl. enrichment (Phase 2) → 4. Server runs locally (Phase 3) → 5. Eval set passes (Phase 4).
