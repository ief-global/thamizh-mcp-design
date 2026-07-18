---
name: thamizh-data-curation
description: "Turn the Thamizh MCP server's provenance-tagged knowledge store and transaction logs into gold-standard Tamil datasets — morphological segmentation pairs, origin/loanword labels, loanword→native-equivalent pairs, and template-generated instruction-tuning records — verified, license-audited, contamination-guarded, and publishable to Hugging Face. This gold corpus is the deliberate bridge to the long-term Tamil SLM. Use whenever the user wants to export, curate, verify, or publish Tamil data from the server, set up or inspect transaction logging, prepare fine-tuning or tokenizer-training data, or check dataset growth/coverage metrics. Triggers: 'export the gold data', 'build the Tamil dataset', 'publish to Hugging Face', 'curate the knowledge store', 'training data for the SLM'. Do NOT trigger for building server features (thamizh-mcp-builder), running benchmarks (thamizh-eval), releasing/hosting the server (thamizh-release), or scraping new sources (the server's own enrichment layer owns that)."
license: Internal project skill for the THAMIZH MCP project. (v1 — created 2026-07-10.)
---

# Thamizh Data Curation — from transaction logs to gold datasets

## Why this exists

High-resource languages are high-resource because of *data*. The scarcest assets for a future Tamil SLM
are exactly what the running server produces as a by-product: verified word→morphology segmentations
(the training input a grammar-first tokenizer needs), origin labels, and attested loanword→equivalent
pairs — each already carrying source, tier, and retrieval date in the knowledge store (blueprint §5,
§12 data addendum). This skill turns that exhaust into publishable gold. Nothing here trains a model —
the SLM is explicitly long-term (`TAMIL-HIGH-RESOURCE-ROADMAP.md`); this skill makes sure that when
that day comes, the corpus already exists.

## Pipeline (run in this order, every export)

1. **Extract** from the SQLite knowledge store + transaction log: one candidate record per resolved
   claim, carrying word (NFC-normalized), field, value, source, tier, retrieval date.
2. **Verify — three bins, by provenance tier:**
   - *Anchor-grounded* (ThamizhiMorph, pinned lexicon/கலைச்சொல் snapshots, rule table) → auto-gold.
   - *Evolving-grounded* (Wiktionary, community lists) → gold only if the blueprint's cross-check
     discipline passed (consistent with an anchor or classical rule); else hold in a `silver` split,
     clearly labelled.
   - *Disputed/low-confidence* (origin disputes, contested equivalents) → hold; may ship as an
     explicitly-labelled `disputed` split with all competing claims — that split is a *feature* for
     researchers, never merged into gold.
3. **Round-trip validate segmentations:** a segmentation record is gold only if the FST *regenerates*
   the surface form from the claimed parts (generation direction of ThamizhiMorph). Catches decoder bugs
   before they become published errors.
4. **Dedupe & normalize:** key on (word, field, value); keep earliest provenance; NFC everywhere.
5. **Contamination guard:** drop every record whose word is flagged `eval_fixture=1` in the store
   (thamizh-eval sets the flag). No eval word ever appears in a published dataset. Non-negotiable.
6. **License filter:** per-source redistribution rules (`references/dataset-formats.md` §3). The hard
   rule: we publish *derived structured analyses with citations*, never bulk third-party text. Records
   whose only source forbids redistribution are excluded from exports (they still serve users at query
   time — export and serving are different rights).
7. **Export** to the JSONL shapes in `references/dataset-formats.md` §1 (segmentation / origin /
   equivalents / instruction), each row carrying `sources[]` — provenance is a mandatory column, not
   metadata.
8. **Dataset card + version:** HF-style card per §4 of the reference; semantic version the dataset;
   record counts per split; state the license mix explicitly.

## Instruction-tuning records: template-only rule

Instruction records (Q/A about a word) are generated **only by filling fixed templates with verified
fields** — e.g. "'X' என்ற சொல்லின் வேர்ச்சொல் என்ன?" → verified lemma. No LLM free-generation of answers:
an LLM may rephrase a *question* surface, never produce an *answer* fact. This is the no-LLM-as-source
principle extended to data. Templates live beside the exporter; every record cites the underlying claim.

## Quality bars (all must hold for the gold split)

- Every record traceable to at least one named source with tier + date; zero LLM-originated facts.
- Segmentations round-trip through the FST; equivalents each carry an attestation source.
- Uneven language coverage is expected and stated in the card (mirrors the server's honest-gap stance) —
  do not pad thin categories with lower-quality records to look balanced.

## Metrics to track per export

Store growth (words, claims), gold/silver/disputed ratio, coverage per field, low-confidence rate trend
(the blueprint's evolving-source quality guardrail), and % excluded by license — if that number is high,
it's a signal to prioritize openly-licensed anchor snapshots, route that to the decision log.

## Reference files

- `references/dataset-formats.md` — the four JSONL schemas with worked examples, per-source license
  table, HF dataset-card checklist.
