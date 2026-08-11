# Integrating a lexicon

How a dictionary or lexicon becomes a grounded source inside Thamizh MCP — written to be read by a
Tamil scholar, not only by an engineer. The **Madras University Tamil Lexicon** runs through as the
worked example, but nothing here is specific to it: the same three questions and the same checklist
apply to the Cologne Online Tamil Lexicon, a TVA கலைச்சொல் glossary, a WordNet, or a lexicon that does
not exist yet.

> **Companion documents.** `README.md` (this folder) — what source materials we hold and why some
> ship and some do not. `../thamizh-mcp-builder/references/sources.md` — the catalog of individual
> sources and the field they each ground. `../DECISIONS.md` — D-016
> records the licence finding that produced the third question below.

---

## 1. What a lexicon is — and what it is not

The server already has a morphological engine: **ThamizhiMorph**, a finite-state transducer. It is
tempting to describe adding a lexicon as "extending the FST." That would be the wrong picture, and
the distinction matters for understanding what a lexicon can and cannot fix.

| | Finite-state morphology (ThamizhiMorph) | A lexicon |
|---|---|---|
| Kind of knowledge | **generative** — paradigms and rules | **enumerative** — facts, one headword at a time |
| The question it answers | how does *வந்தான்* decompose into பகுபத உறுப்பு? | what does *கார்* mean, and where did it come from? |
| How it scales | millions of forms from a finite rule set; no per-word maintenance | grows only as entries are written |
| Can it give origin? | **No — and it never could.** A transducer describes form, not history. | Yes. That is its central job. |

They are complementary. A lexicon is **not** loaded into the FST; it joins the analysis pipeline
*beside* the FST, and the engine merges what each contributes.

There is exactly one genuine point of contact. A lexicon knows headwords the FST's own word list
lacks, so it can produce a **gap list** — the same role the curated `data/verb_paradigms.json`
already plays when the FST misses an irregular verb.

### Why this matters for origin specifically

Origin classification (இயற்சொல் / வடசொல் / loanword) has one remaining unprincipled branch:
**native-by-default**. If a word shows no Grantha letter, breaks no முதல்/இறுதி எழுத்து rule, and no
source attests it as borrowed, the classifier currently assumes it is native.

That is an *absence of evidence* dressed as a finding. Orthography can prove a word is **not**
native; it can never prove that it **is**. Only a lexicon — a positive record that a word is or is
not attested as a borrowing — closes that branch. This is the single largest reason to integrate one.

---

## 2. Three questions, asked in this order

### Question 1 — what can it ground?

Map the source to the output fields it can legitimately fill: `origin`, `meaning`,
`native_equivalent`, lemma/`formation`. A source that is excellent for meaning may say nothing about
origin; claiming otherwise is how unsourced answers get in. The field → source map lives in
`../thamizh-mcp-builder/references/sources.md` §8.

### Question 2 — how far should it be trusted?

Every source carries a **tier**:

- **anchor** — stable, authoritative, version-pinned. The ground truth other claims are checked
  against. Pin a *version*.
- **evolving** — community-maintained, internet-fed, pulled at query time. You cannot pin a version,
  so pin the *retrieval date* of each fact.

Tier is not a judgement of scholarly quality; it is a statement about **stability and citability**.
Tamil Wiktionary is often right and is still `evolving`, because the sentence it asserts today may
not be the sentence it asserts next year.

### Question 3 — what may we do with the bytes?

**This is a separate question from tier, and it must be answered before any code is written.**

Tier says how much to trust a source. It says nothing about what copyright permits. We learned this
the expensive way: the Madras Tamil Lexicon is an impeccable `anchor` source whose licence forbids
the integration we had assumed (D-016). So every source also declares a **redistribution mode**:

| Mode | Licence example | What we may do |
|---|---|---|
| **Redistribute** | Project Madurai classical etexts; I2PT (MIT) | ship the data itself as a version-locked artifact in the code repo |
| **Serve with attribution** | Tamil Wiktionary (CC BY-SA) | cache and serve the text, attribution travelling with it, never relicensed |
| **Consult and cite** | Madras Tamil Lexicon (CC BY-NC-ND) | consult it to establish a fact; record the **fact and the citation**, never the entry text |

A source in the third mode is not second-class. It can be the most authoritative thing we have. The
mode constrains *distribution*, not *trust*.

---

## 3. Facts, expression, and why "consult and cite" is scholarship

The third mode rests on a distinction this project already applies to the TVA course books, stated
in `README.md` in this folder:

> The rule tables encode **facts about Tamil grammar** — the inventory of இடைநிலை, the eight
> வேற்றுமை, the six பகுபத உறுப்பு. Facts aren't copyrightable, and citing the source is scholarship.
> Redistributing complete third-party textbooks is a different act with a different licence question,
> so we don't.

The same reasoning governs a lexicon:

- *"பட்டன் is a borrowing from English **button**"* is a **fact**. We may record it and say where we
  verified it.
- The lexicon's **wording** of its entry — its definition, its phrasing, its arrangement — is
  **expression**. That belongs to its publisher.

So a consult-and-cite integration stores a claim shaped like this:

```json
{
  "class": "loanword",
  "borrowed_from": "English",
  "sources": [{
    "name": "Madras Tamil Lexicon",
    "tier": "anchor",
    "ref": "https://dsal.uchicago.edu/cgi-bin/app/tamil-lex_query.py?qs=…",
    "retrieved": "2026-08-07"
  }]
}
```

and never the entry text. A reader who wants the wording follows the citation to the publisher —
which is what a footnote has always done, and it sends the reader to the source rather than around it.

---

## 4. The integration seam

Every source in the system — FST, classical text, dictionary, word list — hides behind one interface:

```python
class SourceAdapter(ABC):
    name: str          # provenance label carried on every claim
    tier: Tier         # "anchor" | "evolving"

    async def lookup(self, normalized_word: str) -> AdapterResult | NoEntry
```

Two properties of this contract carry the design:

1. **An adapter never guesses.** No entry means `NoEntry`, and the engine records an explicit gap.
   A gap is a valid, publishable answer. A fabricated one is not.
2. **Every claim leaves with its provenance.** `AdapterResult` carries `SourceRef`s. This is what
   makes answers auditable by a scholar — and, as it turns out, what makes licences classifiable
   *per record*, so a mixed-licence corpus can be exported per source (D-012).

Adding a lexicon therefore means implementing one method. The engine, the MCP tools, the REST head
and the CLI need no changes — that is the point of the seam.

---

## 5. When two sources disagree

Adding an anchor lexicon means, often for the first time, two sources contesting the same field. The
resolution rule:

1. **Anchor outranks evolving** for the reported class.
2. **The loser is never deleted.** It moves to `alternatives`, visible to the reader.
3. **Both citations travel**, so a scholar can see who said what.
4. **Agreement raises confidence.** A crowd-edited etymology alone is capped (0.8); the same claim
   corroborated by an anchor lexicon has earned more.

Point 4 is a real gain and not merely bookkeeping: independent corroboration is evidence, and the
confidence number should say so.

Where the disagreement is *genuine scholarly dispute* rather than one source being wrong — பசு is
argued as Sanskrit *paśu* and as a Dravidian *pacu* — neither side is suppressed. The answer reports
the dispute. Recording a controversy accurately is a better answer than resolving it by fiat.

---

## 6. Worked example — the Madras University Tamil Lexicon

The standard scholarly Tamil dictionary (University of Madras, 1924–1936), digitized by the Digital
South Asia Library at the University of Chicago.

**Question 1 — what can it ground?** `origin` (its entries carry etymology and source-language
tags), `meaning`, and a headword gap list for the FST.

**Question 2 — tier?** `anchor`. Published, stable, citable by entry; DSAL's digitization was last
refreshed September 2023, which is the version we pin.

**Question 3 — what may we do with the bytes?** DSAL publishes it under
**CC BY-NC-ND 2.0**, copyright the University of Madras. There is no public API.

- **ND (NoDerivatives)** — parsing entries into a restructured store and serving them is plausibly a
  derivative work.
- **NC (NonCommercial)** — `thamizh-mcp` is Apache-2.0 and anyone may run it, including
  commercially. Bundling NC-licensed data inside it would push a restriction onto downstream users
  who never agreed to it — the same error as relicensing CC BY-SA text, which D-012 forbids.

**Therefore: consult and cite.** Which settles a question the code stub had left open — it proposed
"scrape-at-query **vs** offline digitized copy". The offline copy is not available to us.

What that means concretely:

- **No bundled copy** of the lexicon in the code repo.
- **Query-time lookup**, cached in the machine-local `data/knowledge.sqlite3` — already gitignored.
  A private cache on one machine is not distribution.
- **Store the derived claim and the citation URL, never the entry text.**
- **Excluded from the gold-corpus export.** D-012's per-source classification already makes this a
  filter rather than new machinery.
- **Opt-in, disabled by default**, so the shipped Apache-2.0 product does not depend on an NC source
  and no downstream user inherits the restriction unknowingly.
- **Courteous access**, since there is no API: a descriptive User-Agent, rate limiting, honouring
  `robots.txt`, and caching so a word is fetched once.

**Being explicit about the limits of this reading.** We are not lawyers, and NC/ND terms are exactly
where a cautious reading and a permissive one diverge. The design above is deliberately the cautious
one. The clean resolution is written permission from the University of Madras / DSAL for this
specific use, which IEF is pursuing separately. If it is granted, the mode can be widened; until
then it is not.

---

## 7. Checklist for adding any lexicon

1. **Fields** — which outputs can it legitimately ground? Extend the field → source map.
2. **Tier** — anchor or evolving?
3. **Licence and redistribution mode** — *before writing code.* Read the actual terms; do not infer
   them from the fact that a page is publicly reachable.
4. **Pin** — a version (anchor) or a retrieval date per fact (evolving).
5. **Implement `SourceAdapter.lookup`** — `NoEntry` on a miss, always under a timeout, never a guess.
6. **Precedence** — declare how it resolves against existing sources for every overlapping field.
7. **Provenance** — every claim carries a `SourceRef` naming the source, tier and citation.
8. **Export policy** — does it reach the published gold corpus, or is it filtered out?
9. **Tests** — offline fixtures, the `NoEntry` path, and where the mode is restricted, a
   **licence-compliance test** asserting the restricted text is never persisted or served.
10. **Measure** — re-run `scripts/quality_sweep.py` and report the delta honestly, including where
    it made nothing better.

Step 3 sits deliberately above step 5. Discovering a licence constraint after the adapter is written
means throwing the adapter away.

---

## 8. Swapping the source later

Because the seam is one interface and the constraints are declared per source, replacing a lexicon
is a contained change: implement a new adapter, declare its tier, mode and precedence, re-run the
sweep. Nothing in the engine, the tools or the schema moves.

This is not a hypothetical convenience. If permission for the Madras Lexicon is not granted, the
Cologne Online Tamil Lexicon, a TVA glossary or an openly-licensed successor takes its place under
the same architecture, and everything in this document still holds. That is the reason it is written
about *lexicons* rather than about one lexicon.
