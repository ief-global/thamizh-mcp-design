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
