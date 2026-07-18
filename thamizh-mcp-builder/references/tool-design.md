# THAMIZH MCP — proposed tool surface

A starting design for the MCP tools. Adapt to the sources actually locked in Phase 1. Principle: one focused
tool per concern (so an agent can compose), plus one workflow tool (`analyze_word`) that returns the whole
word analysis object, because the agent usually wants everything about a word at once. Every tool reports its
provenance (source, tier, retrieval date) and reports gaps honestly instead of letting the model invent an
answer.

All read tools are `readOnlyHint: true`, `openWorldHint: true` (results depend on external + evolving
linguistic data), `destructiveHint: false`.

## Reused Tamil-NLP components → MCP tool map

The server does not build a morphological analyser — it **wraps** the Thamizhi suite (Sarveswaran, Dias &
Butt; University of Moratuwa / Konstanz) and orchestrates it with the lexical, etymological, and classical-
grammar sources. This table fixes which existing component powers which MCP tool, so it is never re-derived.

| Thamizhi / Tamil-NLP component | What it provides | MCP tool(s) it powers |
|---|---|---|
| **ThamizhiMorph** (foma FST analyser + generator) | lemma, POS/morph tags, **sandhi** decode, form generation | `get_root`, `explain_formation`, feeds `explain_grammar`; `generate_forms` |
| **ThamizhiPOSt / ThamizhiLIP** (neural POS, UD pipeline) | contextual POS + dependency parse | disambiguation layer behind `explain_grammar` and `get_root` when input exceeds a bare word |
| **Thamizhi Word Validator** (pure-Tamil check) | native-vs-borrowed well-formedness signal | signal into `classify_origin`; standalone `validate_pure_tamil` |
| *open-tamil* (Ezhil LF — related, not Thamizhi) | grapheme-split, stem, transliterate | normalization pre-step, `get_root` fallback, `transliterate` |

**Coverage boundary (why this project exists on top of Thamizhi):** ThamizhiMorph powers the three
*structural* tools (root, formation, grammar) but touches **none** of `classify_origin`'s decision,
`get_meaning`, or `suggest_native_equivalent`. Those are filled by lexicons (Madras Lexicon, Wiktionary),
etymology/loanword data, கலைச்சொல்/தனித்தமிழ் glossaries, and Tholkappiyam rules — see `references/sources.md`.
That gap *is* the server's contribution.

## Self-enriching flow (applies to every lexical tool)

Lookups follow: **cache → anchors → evolving sources → write back**. On a miss in the local knowledge store,
query the anchors (ThamizhiMorph, Madras Lexicon, Tholkappiyam rules); if still thin, pull from the evolving
tier (Tamil Wiktionary, Wikisource, community datasets); merge, tag provenance, and write the result back so
the store enriches itself. Morphology (FST) is stateless and skips the cache. See `references/sources.md`.

## `analyze_word` (workflow tool — the main entry point)
- **Input:** `{ word: string (Tamil, required), include?: string[] (subset of
  ["origin","root","meaning","formation","grammar","native_equivalent"], default all),
  allow_enrichment?: boolean (default true) }`
- **Note:** `native_equivalent` is computed only when `origin` resolves to non-native; for a native word it is
  returned as not-applicable.
- **Output:** the full word analysis object (see `assets/word_analysis_schema.json`). Composes the focused
  tools below and merges provenance. Returns per-section gaps rather than failing whole if one source misses.

## `classify_origin`
- **Input:** `{ word: string }`
- **Output:** `{ class: "இயற்சொல்|திரிசொல்|திசைச்சொல்|வடசொல்|loanword",
  is_native: boolean, borrowed_from: string|null, adaptation: "தற்சமம்|தற்பவம்|null",
  evidence: string, confidence: number, alternatives: [...], sources: [...] }`
- **Sources:** Thamizhi Validator + loanword datasets (evolving) cross-checked against **Tholkappiyam's**
  வடசொல் framework + lexicon etymology. Return competing claims in `alternatives` when authorities disagree.

## `get_root`
- **Input:** `{ word: string }`
- **Output:** `{ lemma: string, all_analyses: [{lemma, pos, tags}], sources: [...] }`
- **Sources:** ThamizhiMorph (rule-based; keep *all* analyses when ambiguous); open-tamil stemmer fallback.

## `get_meaning`
- **Input:** `{ word: string, lang?: "ta"|"en" (default both), allow_enrichment?: boolean }`
- **Output:** `{ senses: [{gloss_ta, gloss_en, pos, source, tier, citation, retrieved}], sources: [...] }`
- **Sources:** Madras Tamil Lexicon (anchor) → Tamil Wiktionary (evolving) on a miss; AU-KBC WordNet.

## `explain_formation`
- **Input:** `{ word: string }`
- **Output:** `{ word_type: "பகுபதம்|பகாப்பதம்",
  components: [{part: "பகுதி|விகுதி|இடைநிலை|சாரியை|சந்தி|விகாரம்", form, role, authority}],
  sandhi: [{type: "தோன்றல்|திரிதல்|கெடுதல்|வல்லினம்மிகுதல்", detail, authority}], sources: [...] }`
- **Sources:** ThamizhiMorph FST tags decoded into the six parts. Authority: **Tholkappiyam** for the
  underlying elements (sandhi/suffixes); **Nannūl** for the six-part labels (see `tamil-grammar.md`).

## `explain_grammar`
- **Input:** `{ word: string }`
- **Output:** `{ word_class: "பெயர்|வினை|இடை|உரிச்சொல்", case?: {number, name, function},
  tense?, person_number_gender?, notes, authority: "Tholkappiyam|Nannūl", sources: [...] }`
- **Authority:** Tholkappiyam first (word classes, வேற்றுமை); Nannūl only as fallback.

## `suggest_native_equivalent`  (objective 5 — conditional)
- **Input:** `{ word: string, origin?: object (from classify_origin; if omitted the tool calls it first),
  allow_enrichment?: boolean }`
- **Output:** `{ applicable: boolean (false for native words),
  candidates: [{ equivalent: string, source: string, tier: "anchor|evolving", register: "technical|literary|everyday",
  attestation: "attested|proposed", confidence: number, citation: string }],
  note?: string (e.g. "no attested equivalent found"), sources: [...] }`
- **Sources:** கலைச்சொல்/TVA/govt terminology (anchor) → Indic-To-Pure-Tamil, Tamil Wiktionary, தனித்தமிழ்
  lists (evolving). See `references/sources.md` §6.
- **Hard rule:** every candidate must carry an attestation `source`; the merge layer drops any candidate
  without one, so a self-invented coinage can never surface. If nothing is attested, return
  `applicable: true, candidates: [], note: "no attested equivalent"`. Mark purist/movement coinages with
  `attestation: "proposed"` and their register, so established usage is distinguishable from advocacy.

## Enrichment / maintenance tools
- `enrich_word` — `{ word }` → force a fresh pull from the evolving sources for a thin/stale entry; writes
  provenance-tagged results to the knowledge store. Honors the cross-check discipline (evolving facts kept
  only if attributable + consistent with an anchor/classical rule).
- `refresh_sources` — `{ scope? }` → re-pull a batch (e.g. recently-missed words) so coverage grows.
- *(annotations: these write to the local cache, not to any external service — still safe/non-destructive to
  the outside world, but mark `readOnlyHint: false` since they mutate local state.)*

## Optional / later
- `validate_pure_tamil` — `{ word }` → `{ is_pure_tamil, reason, source }` (Thamizhi Validator).
- `generate_forms` — `{ lemma, features }` → surface forms (ThamizhiMorph generator) for spell-check/data aug.
- `transliterate` — `{ text, scheme }` for romanized I/O and English-loanword matching.

## Shared output conventions
- Every analysis carries a `sources` array of `{name, tier, ref, retrieved}`; every claim is attributable,
  and grammar claims also carry `authority` (Tholkappiyam / Nannūl).
- When a source has no entry: `{ status: "no_entry", source, note }` — an honest gap, never a fabricated value.
- When analyses are ambiguous: return all in `alternatives`/`all_analyses`; do not silently disambiguate.
