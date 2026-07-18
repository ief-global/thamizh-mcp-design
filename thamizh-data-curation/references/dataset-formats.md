# Dataset formats, license table, and card checklist

## 1. The four JSONL shapes

All rows: NFC Unicode, `sources` mandatory, one row per (word, claim).

**a) Morphological segmentation** — tokenizer/SLM training input; FST round-trip validated.
```json
{"word": "மரத்தில்", "lemma": "மரம்", "parts": [
   {"form": "மரம்", "role": "பகுதி"}, {"form": "அத்து", "role": "சாரியை"}, {"form": "இல்", "role": "உருபு"}],
 "sandhi_note": "மகர ஈறு கெட்டது", "pos": "NN", "case": "ஏழாம் வேற்றுமை (loc)",
 "authority": "Nannūl (labels) / Tholkappiyam (case)", "fst_roundtrip": true,
 "sources": [{"name": "ThamizhiMorph", "tier": "anchor", "ref": "data/PINS.md@adbacced", "date": "2026-07-02"}]}
```

**b) Origin labels** — for classifier training/eval.
```json
{"word": "புத்தகம்", "origin_class": "வடசொல்", "borrowed_from": "Sanskrit (pustaka)",
 "confidence": "attested", "alternatives": [],
 "sources": [{"name": "Indic-To-Pure-Tamil", "tier": "evolving", "ref": "f734646", "date": "2026-07-02"}]}
```
Disputed words go to the `disputed` split with ALL competing claims in `alternatives`, none promoted.

**c) Loanword → native equivalents** — ranked, attested-only (gold split drops unattested candidates).
```json
{"word": "கம்ப்யூட்டர்", "language": "English", "equivalents": [
   {"form": "கணினி", "register": "everyday", "attestation": "TVA கலைச்சொல்"},
   {"form": "கணிப்பொறி", "register": "technical", "attestation": "கலைச்சொல் glossary"}],
 "sources": [{"name": "TVA", "tier": "anchor", "ref": "<snapshot pin>", "date": "…"}]}
```

**d) Instruction records** — template-generated only (see SKILL.md rule).
```json
{"instruction": "'மரத்தில்' என்ற சொல்லின் வேர்ச்சொல் என்ன?", "output": "மரம்",
 "template_id": "root-q-01", "claim_ref": "மரத்தில்/lemma",
 "sources": [{"name": "ThamizhiMorph", "tier": "anchor", "ref": "…", "date": "…"}]}
```

## 2. Splits

`gold` (anchor-grounded or cross-checked, round-trip valid) · `silver` (evolving-only, labelled) ·
`disputed` (competing claims, research split). Never mix. eval_fixture-flagged words appear in none.

## 3. Per-source license/redistribution table (check before every export)

| Source | License | May redistribute derived records? |
|---|---|---|
| ThamizhiMorph FST output | Apache-2.0 | Yes, with attribution (cite Sarveswaran/Dias/Butt 2021) |
| Our own analyses/decoder output | Apache-2.0 (repo) | Yes |
| Indic-To-Pure-Tamil CSVs | MIT — **still "verify" per data/PINS.md** | After verification: yes, attribute |
| Tamil Wiktionary | CC BY-SA | Derived facts: yes with attribution AND the dataset (or split) must be BY-SA-compatible; never bulk-copy entry text |
| Madras Tamil Lexicon (DSAL) | Check terms — unresolved (blueprint §10) | NOT until resolved; exclude or hold |
| TVA / govt கலைச்சொல் | Check per glossary | Attested single-term facts generally citable; verify before bulk export |

Rule of thumb: short structured facts with citation ≈ safe; reproduced prose/entries ≈ not. When mixed
licenses force it, publish per-source subsets rather than diluting the whole dataset's license.

## 4. HF dataset card checklist

- [ ] Name, version, date, counts per split/shape; languages: ta (+ source languages for loans)
- [ ] Provenance section: source list with tiers, pins/dates; link to thamizh-mcp repo + PINS.md
- [ ] License section: per-subset licenses from §3 table; overall license = most restrictive included
- [ ] Method: how records were verified (anchor tiers, FST round-trip, cross-check discipline)
- [ ] Known limitations: uneven coverage by source language; disputed split explanation; silver caveats
- [ ] Contamination statement: eval-fixture words excluded; held-out set never published
- [ ] Citation block (repo CITATION.cff) + ThamizhiMorph citation
- [ ] Intended use: tokenizer training, morphological analysis, loanword research; NOT a complete lexicon
