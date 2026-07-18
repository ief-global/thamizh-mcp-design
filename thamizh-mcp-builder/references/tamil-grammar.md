# சொல் இலக்கணம் — a working primer for the THAMIZH MCP server

This is the grammatical backbone the server must reproduce *authentically*. Use the Tamil grammatical terms
below as the server's output vocabulary — that is what makes an answer authentic rather than a plausible
paraphrase.

## Source priority — Tholkappiyam first

**தொல்காப்பியம் (Tholkappiyam) is the golden authority; cite it first.** Fall back to **நன்னூல் (Nannūl)**
only where Tholkappiyam does not enumerate the point. Concretely:

| Topic | Cite first | Where in Tholkappiyam | Fallback |
|---|---|---|---|
| Word classes (பெயர்/வினை/இடை/உரி) | **Tholkappiyam** | சொல்லதிகாரம் — பெயர்/வினை/இடை/உரியியல் | Nannūl |
| Origin classes (இயற்/திரி/திசை/வடசொல்) | **Tholkappiyam** | சொல்லதிகாரம் (எச்சவியல்/மரபியல்) | Nannūl |
| வேற்றுமை (8 cases) | **Tholkappiyam** | சொல்லதிகாரம் — வேற்றுமையியல் | Nannūl |
| புணர்ச்சி / sandhi | **Tholkappiyam** | எழுத்ததிகாரம் — புணரியல் | Nannūl |
| Six-part பகுபதம் decomposition | Nannūl (Tholkappiyam doesn't enumerate the six) | — | — |

Always record which authority a grammar claim used, so the priority is auditable.

## Table of contents

- [1. சொல் — word classes](#1-சொல்--word-classes)
- [2. Word origin classes (native vs borrowed)](#2-word-origin-classes)
- [3. Word formation — பகுபதம் and its உறுப்புகள்](#3-word-formation)
- [4. வேற்றுமை — the eight cases](#4-வேற்றுமை--the-eight-cases)
- [5. புணர்ச்சி — sandhi](#5-புணர்ச்சி--sandhi)
- [6. Worked examples](#6-worked-examples)

---

## 1. சொல் — word classes

Tholkappiyam's சொல்லதிகாரம் sorts every word (சொல்) into four classes (பெயரியல், வினையியல், இடையியல்,
உரியியல்). The server's `pos`/`grammar` output should name one:

- **பெயர்ச்சொல்** (noun) — names a person, thing, place, quality. e.g. மரம், தமிழ், அன்பு.
- **வினைச்சொல்** (verb) — expresses an action or state, carries tense. e.g. வந்தான், படித்தாள்.
- **இடைச்சொல்** (particle/clitic) — cannot stand alone; case suffixes, conjunctions, postpositions, emphatics
  (உம், ஐ, கு, ஆல், தான்…). These attach to பெயர்/வினை.
- **உரிச்சொல்** (qualifier) — words that qualify nouns/verbs (adjective/adverb-like), e.g. நல்(ல), பெரு.

## 2. Word origin classes

Tholkappiyam classifies words by origin into **four** classes — this is the authentic frame for the
native-vs-borrowed decision, so prefer it over a bare "native/loan" boolean (authority: Tholkappiyam,
சொல்லதிகாரம்):

- **இயற்சொல்** — ordinary native Tamil words in common use, understood directly. (The core "native" class.)
- **திரிசொல்** — native Tamil words of restricted/literary use or with shifted form/meaning (poetic, archaic).
- **திசைச்சொல்** — words from other Tamil regions / neighbouring Dravidian areas (regional Tamil).
- **வடசொல்** — words from the north, i.e. **Sanskrit/Indo-Aryan loanwords**.

For வடசொல் (and loanwords generally), record the adaptation type:
- **தற்சமம் (tatsama)** — borrowed with little/no phonological change.
- **தற்பவம் (tadbhava)** — Sanskrit-origin word adapted to Tamil phonology over time.

For modern borrowings outside this scheme (English, Perso-Arabic, etc.), classify as a loanword and record
the source language explicitly; note that the classical four-way scheme predates them.

**Honesty note:** origin is contested for many words — a word claimed இயற்சொல் by one authority may be argued
வடசொல்/தற்பவம் by another. The server should report the competing claims and their evidence, not pick one
silently.

### 2.1 Native equivalents (தனித்தமிழ் / கலைச்சொல்) — objective 5

When a word is *not* native (வடசொல், திரிசொல்/திசைச்சொல், or a modern English/Urdu/Portuguese/etc. loan), the
server suggests its attested native Tamil equivalent. This is **not a grammatical derivation** — it is lexical
substitution grounded in the கலைச்சொல் (terminology) and தனித்தமிழ் traditions, *not* Tholkappiyam. Examples:

| Borrowed word | Source language | Native equivalent | Register |
|---|---|---|---|
| கம்ப்யூட்டர் | English | கணினி | technical (established) |
| தொலைஃபோன் | English | தொலைபேசி | technical (established) |
| புத்தகம் | Sanskrit (வடசொல்) | நூல் / ஏடு | literary / everyday |
| ஜன்னல் | Portuguese (janela) | சாளரம் | everyday |
| பஸ் | English | பேருந்து | everyday (established) |

Rules: suggest **only attested** equivalents, each with its source; equivalents are often **one-to-many** by
register (technical vs literary vs everyday) — return ranked candidates, don't adjudicate; when no authority
attests an equivalent (common for Portuguese/Urdu/Marathi loans), return an explicit "no attested equivalent"
rather than coining one. Mark purist/movement coinages as such so the user can tell established usage from
advocacy.

## 3. Word formation

First decide the word *type*:

- **பகாப்பதம்** — a simple/unanalyzable word (a single root that does not split into grammatical parts),
  e.g. மண், கல்.
- **பகுபதம்** — an analyzable/derived word that splits into grammatical parts (உறுப்புகள்).

A **பகுபதம்** is built from up to **six உறுப்புகள்**. Note on authority: the neat enumerated six-part scheme
is **Nannūl's** codification (பகுபத உறுப்பிலக்கணம்) — Tholkappiyam treats the underlying elements (suffixes,
tense markers, sandhi) across its எழுத்ததிகாரம் and சொல்லதிகாரம் but does not list "six parts." So follow the
Tholkappiyam-first rule by grounding the underlying elements (சந்தி/புணர்ச்சி, விகுதி) in **Tholkappiyam** and
using **Nannūl** for the six-part labels. Label each present part with these names:

1. **பகுதி** — the root/base (the core morpheme carrying meaning). e.g. வா- in வந்தான், மரம் in மரத்தில்.
2. **விகுதி** — the terminal suffix (person-number-gender ending on verbs; case suffix on nouns).
   e.g. -ஆன் (3rd-person masc. sg.), -இல் (locative).
3. **இடைநிலை** — the medial, chiefly the **tense marker** between root and ending.
   e.g. past -த்/-ந்த்/-இன், present -கிறு/-கின்ற், future -ப்/-வ்.
4. **சாரியை** — a euphonic augment inserted to join parts. e.g. அத்து in மரம்→மரத்து, இன், அன், அல்.
5. **சந்தி** — the juncture/glue consonant at a join (governed by Tholkappiyam's புணரியல்).
6. **விகாரம்** — modification at the join: **தோன்றல்** (a letter appears), **திரிதல்** (a letter changes),
   **கெடுதல்** (a letter drops). e.g. மரம் → மரத் (ம் changes), வா → வந் (form change).

Not all six appear in every word; label only those present, in order.

## 4. வேற்றுமை — the eight cases

Nouns inflect for eight cases (வேற்றுமை); authority: **Tholkappiyam, வேற்றுமையியல்**. Each has a number, a
name, a function, and a typical suffix (உருபு). The server's `grammar.case` should give the **ordinal name +
function**, and `formation` should expose the உருபு as a விகுதி.

| # | பெயர் | உருபு (suffix) | Function (English) |
|---|---|---|---|
| 1 | எழுவாய் வேற்றுமை | (none) | nominative / subject |
| 2 | ஐ | ஐ | accusative / object |
| 3 | ஆல் | ஆல், ஆன், ஒடு, உடன் | instrumental / sociative |
| 4 | கு | கு (க்கு) | dative ("to/for") |
| 5 | இன் | இல், இன் | ablative ("from") |
| 6 | அது | அது, ஆது, உடைய | genitive / possessive |
| 7 | கண் | கண், இல், இடம் | locative ("in/at/on") |
| 8 | விளி | (vocative form) | vocative / address |

**Ambiguity to handle:** the suffix இல் marks both the 5th (ablative, "from") and 7th (locative, "in"). The
server cannot resolve this from the word alone — return both readings with provenance rather than guessing.

## 5. புணர்ச்சி — sandhi

புணர்ச்சி is the rule system for how two words/morphemes join (authority: **Tholkappiyam, எழுத்ததிகாரம் —
புணரியல்**). It governs the சந்தி and விகாரம் seen in formation. The two effects to expose:

- **வல்லினம் மிகுதல் / மிகாமை** — whether a hard consonant (க், ச், ட், த், ப், ற்) is doubled at the join.
- **மெய் / உயிர் changes** — insertion, deletion, or change of letters at the boundary (the விகாரம் types).

ThamizhiMorph is valuable precisely because it handles Sandhi in its analysis — decode its output back into
these Tholkappiyam terms rather than re-deriving sandhi from scratch.

## 6. Worked examples

These show the target `formation` + `grammar` output, with the authority used. Use them as fixtures in
Phase 4 evals.

**மரத்தில்** ("in the tree") — பகுபதம், பெயர்ச்சொல்
- பகுதி: மரம்
- சாரியை: அத்து  (with விகாரம்: மரம் → மரத் — ம் changes; per Tholkappiyam புணரியல்)
- விகுதி: இல்  (ஏழாம் வேற்றுமை உருபு; per Tholkappiyam வேற்றுமையியல்)
- grammar: ஏழாம் வேற்றுமை (இடப்பொருள் / locative), ஒருமை; origin: இயற்சொல் (native)
- *also* readable as ஐந்தாம் வேற்றுமை (ablative) — return both.
- authority: Tholkappiyam (case + sandhi); six-part labels per Nannūl.

**வந்தான்** ("he came") — பகுபதம், வினைச்சொல்
- பகுதி: வா
- இடைநிலை: ந்த்  (இறந்தகாலம் / past tense)  — with விகாரம்: வா → வந்
- விகுதி: ஆன்  (படர்க்கை, ஆண்பால், ஒருமை — 3rd person masc. sg.)
- grammar: இறந்தகால வினைமுற்று; origin: இயற்சொல்
- authority: Tholkappiyam (வினையியல், புணரியல்); six-part labels per Nannūl.

**புத்தகம்** ("book") — borrowing
- origin: வடசொல் (Sanskrit pustaka), adaptation தற்பவம் (authority: Tholkappiyam names வடசொல்)
- meaning: book (cite lexicon / Wiktionary)
- formation: treat as பகாப்பதம் in Tamil unless a Tamil-internal derivation applies; flag that morphological
  decomposition belongs to the source language, not Tamil.

**கம்ப்யூட்டர்** ("computer") — modern loanword
- origin: loanword, source language English; not in the classical four-way scheme — say so.
- meaning: computer; formation: not analyzable by Tamil morphology (transliterated borrowing).
