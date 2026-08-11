# Glossary — morphology terms in Tamil-grammar language

> Part of `ief-global/thamizh-mcp-design`. Created **2026-08-10**.
> Companion to `DESIGN.md` (program map) and `Thamizh-MCP-blueprint.md` (server spec).

## Who this is for

You know Tamil grammar. You know what a வேற்றுமை is, what a விகுதி does, and why புணர்ச்சி matters.
What you do **not** necessarily know is the vocabulary that computational linguistics uses for those same
things — "lemma", "morpheme", "feature bundle", "FST", "treebank", "token" — which this project's
documents use constantly and without explanation.

That is the gap this file closes. Every entry does four things:

1. says what the technical term means in plain language,
2. names the Tamil grammar concept it corresponds to,
3. gives a Tamil example,
4. says where it shows up in *this* project.

Where a term does **not** map cleanly onto Tamil grammar, that is flagged explicitly — those mismatches
are where most confusion (and some real linguistic argument) lives. See §7, "False friends".

**If you read only one thing, read §1.1 and the two worked examples in §8.** Almost every other term is
a label for some part of those two diagrams.

---

## Quick reference

| Technical term | Nearest Tamil concept | One line |
|---|---|---|
| Morphology | சொல் இலக்கணம் (word-internal structure) | How words are built out of parts |
| Morpheme | உறுப்பு (as in பகுபத உறுப்பு) | The smallest piece that carries meaning or grammar |
| Agglutinative | ஒட்டுநிலை மொழி | Parts chain onto a word, each keeping its own identity |
| Surface form | the word as actually written | மரத்தில் |
| Lemma | அகராதி வடிவம் — the headword | மரம் |
| Stem | the form suffixes attach to | மரத்- |
| Root | வேர்ச்சொல் | the historical seed of a word family |
| Affix / suffix | விகுதி, இடைநிலை, சாரியை | a part added to a stem |
| Inflection | same word, different grammatical form | மரம் → மரத்தில் |
| Derivation | a new word made from an old one | செய் → செயல் |
| Feature | இலக்கணக் கூறு | one grammatical property (tense, case, பால்…) |
| Feature bundle | the full grammatical description | "noun, அஃறிணை, singular, 7th வேற்றுமை" |
| POS tag | சொல் வகை | பெயர் / வினை / இடை / உரி |
| Case | வேற்றுமை | the eight |
| Sandhi | புணர்ச்சி | sound change where two forms join |
| Analysis | பகுத்தல் | word → parts |
| Generation | ஆக்கல் | parts → word |
| Segmentation | பிரித்தல் | marking where the parts divide |
| Disambiguation | choosing among possible readings | which analysis of a form is right *here* |
| Paradigm | வாய்பாடு / inflection table | the full set of forms for a word class |
| Corpus | தொகுப்பு | a large collection of text |
| Treebank | grammatically annotated sentence collection | Aalamaram |
| Token | whatever unit a model counts | usually *not* a word |
| OOV | out of vocabulary | a word the system has never seen |

---

## 1. Words and their parts

### 1.1 Morphology (சொல் இலக்கணம், word-internal structure)

**What it means.** The study of how a word is built out of smaller meaningful pieces — as opposed to
*syntax*, which studies how words combine into sentences.

**In Tamil grammar.** This is largely what தொல்காப்பியம்'s சொல்லதிகாரம் and நன்னூல்'s பகுபத
உறுப்பிலக்கணம் are about: not the meaning of a word, but its construction.

**Why the whole project rests on it.** English carries grammar mostly in separate words ("in the tree" =
three words). Tamil carries it *inside* the word (மரத்தில் = one word). A system that treats a Tamil word
as an opaque string therefore throws away most of the grammar. Recovering it is what `thamizh-mcp` does.

### 1.2 Morpheme (உறுப்பு)

**What it means.** The smallest unit that carries meaning or grammatical function. Not a letter, not a
syllable — a *meaning-bearing* piece.

**In Tamil grammar.** Exactly the உறுப்புகள் of பகுபத உறுப்பிலக்கணம். In மரத்தில், the morphemes are
மரம் (the thing), அத்து (a linking increment), and இல் (the locative marker). Three morphemes, one word.

**Careful.** எழுத்து (letter/sound) is *not* a morpheme. த் in மரத்தில் is an எழுத்து that appears as
part of a விகாரம்; it is not itself a meaning-bearing unit.

### 1.3 Agglutinative language (ஒட்டுநிலை மொழி)

**What it means.** A language where grammatical pieces attach in a chain, each staying recognisably
itself, so one word can carry what another language needs a whole phrase for.

**Example.** படித்துக்கொண்டிருந்தார்கள் — "they were reading" — is one Tamil word carrying root, aspect,
tense, person, number and honorific.

**Why it matters here.** Agglutination is why Tamil words are long, why there are effectively unlimited
word forms (so a fixed dictionary can never cover them — see non-negotiable #2 in DESIGN.md §1), and why
tokenizers built for English break on Tamil (§5.2).

### 1.4 பகுபதம் and பகாப்பதம்

**In Tamil grammar, already familiar.** A **பகுபதம்** is a word that can be split into parts
(மரத்தில், செய்தான்). A **பகாப்பதம்** is a word that cannot (மரம், கை, நீ).

**Technical equivalent.** "Complex / analysable word" vs "simple / monomorphemic word".

**In the project.** `explain_formation` returns a decomposition for a பகுபதம் and correctly returns
"no decomposition" — not an error — for a பகாப்பதம்.

### 1.5 The six பகுபத உறுப்புகள்

The standard நன்னூல் six-part scheme, with the technical name for each:

| Tamil | Technical name | What it is | In மரத்தில் / செய்வித்தான் |
|---|---|---|---|
| பகுதி | stem / base | the part everything attaches to | மரம் / செய் |
| விகுதி | terminal suffix | the final ending, usually carrying person-number-gender or case | இல் / ஆன் |
| இடைநிலை | medial affix | sits between பகுதி and விகுதி; carries tense or voice | — / வி, த் |
| சாரியை | euphonic increment | a linking piece with no meaning of its own, inserted to make the join work | அத்து / — |
| சந்தி | juncture | the point where two parts meet | ம்+அத்து / — |
| விகாரம் | change at the juncture | the sound actually changing at that point | ம் → த் / — |

**Note on authority.** Tholkappiyam is our first authority for grammar generally, but this specific
six-part enumeration is நன்னூல்'s. The project always records which authority a claim came from — see
DESIGN.md §1 non-negotiable #1.

### 1.6 Lemma, stem, and root — three different things

This trio causes more confusion than any other, because Tamil grammar and computational linguistics slice
it differently. Keep them apart:

**Lemma (அகராதி வடிவம்).** The dictionary headword — the form you would look up. For மரத்தில், the lemma
is **மரம்**. For செய்வித்தான், the lemma is **செய்**. A lemma is a *convention*, chosen so that all forms
of one word gather under one entry.

**Stem (பகுதி).** The actual form that suffixes attach to, which may differ from the lemma. In மரத்தில்
the stem is **மரத்-**, not மரம். The FST works with stems; the user searches with lemmas.

**Root (வேர்ச்சொல்).** The historical seed a whole family of words grew from. செய் is the root behind
செயல், செய்கை, செய்தி, செய்வித்தான். A root is an *etymological* claim, not a mechanical one.

**Practical rule for reading our docs:** when a tool returns "root", it almost always means **lemma** in
the technical sense above. `get_root` returns the FST's lemma. Where we mean வேர்ச்சொல் in the
etymological sense, the docs say so explicitly.

### 1.7 Inflection vs derivation

**Inflection** — the same word in a different grammatical form. மரம் → மரத்தில் → மரங்கள். Still the noun
"tree". Inflection is what the FST generates, and it is unbounded.

**Derivation** — a *new* word built from an old one. செய் (verb, "do") → செயல் (noun, "deed"). Different
word, different dictionary entry.

**Why the distinction is load-bearing here.** Inflected forms are rule-derivable, so we never store them —
that is precisely how we avoid a hand-maintained word list. Derived words are lexical facts and *do* need
a source. Mixing the two is how projects like this drown in maintenance.

---

## 2. Describing grammar: features and tags

### 2.1 Feature and feature bundle (இலக்கணக் கூறு)

**What it means.** A **feature** is one grammatical property with a value: tense = past. Case = locative.
A **feature bundle** is the complete set for one word.

For மரத்தில்: `{POS: noun, திணை: அஃறிணை, எண்: ஒருமை, வேற்றுமை: 7}`.
For செய்வித்தான்: `{POS: verb, காலம்: இறந்த, வினை: பிறவினை, இடம்: படர்க்கை, பால்: ஆண்பால், எண்: ஒருமை}`.

**Why this term matters for §8 of DESIGN.md.** The generation track's central idea is that a model should
predict **a lemma plus a feature bundle** — செய் plus that bundle — and let the server produce
செய்வித்தான். The feature bundle is the interface between the statistical part and the rule part.

### 2.2 POS tag (சொல் வகை)

**What it means.** "Part of speech" — the word's grammatical class.

**In Tamil grammar.** Tholkappiyam's four: **பெயர்ச்சொல்** (noun), **வினைச்சொல்** (verb),
**இடைச்சொல்** (particle), **உரிச்சொல்** (qualifier). Computational tagsets usually use a longer list
(noun, proper noun, pronoun, verb, auxiliary, adjective, adverb, postposition…), which does not divide the
same way — see §7.

### 2.3 PNG — person, number, gender (இடம், எண், பால்)

**What it means.** The three properties a Tamil finite verb agrees with its subject in. The abbreviation
"PNG" appears constantly in Tamil NLP writing.

- **Person / இடம்** — தன்மை (1st), முன்னிலை (2nd), படர்க்கை (3rd)
- **Number / எண்** — ஒருமை, பன்மை
- **Gender / பால்** — ஆண்பால், பெண்பால், பலர்பால், ஒன்றன்பால், பலவின்பால்

**Careful:** Tamil's பால் system is not the European masculine/feminine/neuter system, because it is
crossed with திணை (§2.4). Any tool that says "gender: neuter" for a Tamil word is compressing something.

### 2.4 Rationality (திணை)

**What it means.** The உயர்திணை / அஃறிணை distinction — whether the referent is a rational being or not.

**Why it is called out separately.** This is a genuine, well-documented mismatch: the ThamizhiMorph paper
itself notes that Universal Dependencies (§5.5) has no way to express rationality, euphonic increments, or
sandhi effects. Our schema keeps all three, because they are Tholkappiyam categories and dropping them
would mean the analysis is no longer Tamil grammar — it would be Tamil forced into an English-shaped box.

### 2.5 Case (வேற்றுமை)

**What it means.** The grammatical role of a noun, marked by a suffix. Tamil's eight, in the traditional
order: 1 எழுவாய் · 2 ஐ · 3 ஆல் / ஒடு · 4 கு · 5 இன் · 6 அது · 7 கண் · 8 விளி.

The marker itself is the **வேற்றுமை உருபு** ("case marker" / "case suffix"). In மரத்தில், இல் is a
7th-case உருபு.

**Careful:** the 1st (எழுவாய்) and 8th (விளி) are not really *marked* cases in the way 2–7 are. Tagsets
that list "8 cases" flatly are papering over that.

### 2.6 Finite vs non-finite (முற்று vs எச்சம்)

**Finite (வினைமுற்று)** — a verb that can end a sentence: செய்தான்.
**Non-finite (எச்சம்)** — a verb form that cannot: **வினையெச்சம்** (செய்து, adverbial) and
**பெயரெச்சம்** (செய்த, adjectival).

**Where this appears in the project.** CODE-STATUS lists non-finite forms (கொடுக்க / கொடுத்து /
கொடுக்கும்) as still-open FST coverage. Also relevant: Tamil future neuter `-உம்` is tagged non-finite by
the FST itself, which is why "future 3sgn" is deliberately excluded from our coverage sweep.

### 2.7 Clitic

**What it means.** A small piece that attaches to a word but is not part of its inflection — it modifies
emphasis or meaning at the phrase level.

**In Tamil.** ஏ, ஓ, உம், தான், கூட — as in அவனே, வந்தானா, நானும்.

**Why it is annoying.** Clitics attach to *any* word class, so they blur the boundary of "the word",
which matters for segmentation and tokenization. Aalamaram specifically adjusts Universal Dependencies to
handle Tamil clitics — that is one of the reasons it is worth adopting.

---

## 3. Joining and sound change

### 3.1 Sandhi (புணர்ச்சி)

**What it means.** Sound change that happens when two forms are joined. Sanskrit grammar's term "sandhi"
is used universally in the technical literature for what Tamil grammar calls **புணர்ச்சி**.

**The Tamil classification** (Tholkappiyam, எழுத்ததிகாரம் — புணரியல்):

- **இயல்பு புணர்ச்சி** — the forms join with no change.
- **விகார புணர்ச்சி** — something changes, in one of three ways:
  - **தோன்றல்** — a sound *appears* (insertion)
  - **திரிதல்** — a sound *changes* into another (substitution)
  - **கெடுதல்** — a sound *disappears* (elision)

**Example.** மரம் + இல் → மரத்தில். The ம் becomes த் — a திரிதல் — and the சாரியை அத்து is involved in
the join.

**Why it is the hardest part of the project.** Analysis has to *undo* sandhi to find the parts; generation
has to *apply* it to produce a correct word. The v1 server names a join only where a confident classical
rule fires and leaves harder ones unnamed rather than inventing an explanation (DESIGN.md §3.2). Item M4
is the commitment to do this properly.

### 3.2 Euphonic increment (சாரியை)

**What it means.** A linking element inserted purely to make a join pronounceable, carrying no meaning of
its own. அத்து, இன், அன், கள் in certain positions.

**Why it is called out.** Universal Dependencies has no feature for it, so a UD-only analysis silently
loses it. Ours does not. If you see "euphonic increment" in a paper, read சாரியை.

### 3.3 Surface form vs underlying form

**Surface form** — the word as actually written: மரத்தில்.
**Underlying form** — the sequence of parts before sandhi applied: மரம் + அத்து + இல்.

The FST's job is to convert between these two, in either direction. Analysis is surface → underlying.
Generation is underlying → surface.

---

## 4. The machinery

### 4.1 Morphological analysis (பகுத்தல்) and generation (ஆக்கல்)

**Analysis** — given மரத்தில், return: lemma மரம், parts மரம் + அத்து + இல், features {noun, அஃறிணை,
singular, 7th case}.

**Generation** — given lemma மரம் and features {noun, singular, 7th case}, return மரத்தில்.

**The key fact for DESIGN.md §8.** ThamizhiMorph is an analyser *cum generator* — the same machine runs
both ways. The server currently uses only analysis. Generation is already there, unused.

### 4.2 FST — finite-state transducer

**What it means.** A rule machine that converts one string into another by following a network of states
and transitions. "Transducer" because it *translates* between two levels — here, surface form and
underlying form plus tags.

**Why it suits Tamil.** Tamil inflection is highly regular and rule-governed. Rather than list millions
of forms, you write the paradigms and the sandhi rules once and the machine derives every form. This is
the technical mechanism behind non-negotiable #2, "self-enriching, not hand-maintained".

**The property that matters most:** an FST is **bidirectional**. Build it for analysis and you get
generation free.

### 4.3 foma and `flookup`

**foma** is the open-source software that compiles and runs FSTs; **`flookup`** is its command-line
lookup tool. ThamizhiMorph ships as foma files, so our server calls `flookup` as a subprocess.

**Practical notes from the build:** install the Ubuntu package `foma`, *not* `foma-bin` (an empty
transitional package — this caused a real bug where the Docker container had no working FST). Because
`flookup` is a subprocess call, it must be pushed off the async event loop or it stalls other requests.

### 4.4 Paradigm (வாய்பாடு)

**What it means.** The complete inflection table for a class of words — all the forms a verb of a given
type takes across tense, person, number and gender.

**In the project.** ThamizhiMorph compiles Tamil morphology from paradigm tables (verbal paradigms plus
nominal paradigms, including 38 pronoun classes). Separately, we added a curated
`data/verb_paradigms.json` **anchor** table that is consulted *only* when the FST misses — the fix that
closed the everyday-verb coverage gap (DESIGN.md §3.1).

### 4.5 Guesser FST — and why we refuse to use one

**What it means.** A fallback FST that guesses an analysis for a word it does not know, by pattern
similarity.

**Our position: rejected by policy.** Guessers return *wrong* lemmas — கொடுத் instead of கொடு — which is a
confident error rather than an honest gap. That directly violates non-negotiable #5. When the FST misses,
the correct behaviour is the enrichment loop or an explicit gap.

### 4.6 Disambiguation

**What it means.** One surface form often has several valid analyses. Choosing the right one *for this
sentence* is disambiguation.

**Our rule.** Analysis and disambiguation are kept separate. In isolation the server returns **all** valid
analyses with provenance rather than silently picking one, because there is no honest basis for picking.
Contextual disambiguation arrives with sentence support (M6 / generation Stage A), where context supplies
that basis.

### 4.7 OOV — out of vocabulary

A word the system has no entry for. ThamizhiMorph's residual failures are mostly OOV lexicon gaps — which
is good news, because stems are *addable*. Logging OOV misses and periodically adding stems is legitimate,
bounded maintenance; it is not the banned hand-maintained word list, which was about *inflected forms*.

---

## 5. Data, text, and measurement

### 5.1 Corpus (தொகுப்பு)

A large body of text used as evidence or training data. Tamil Wikipedia, a collection of school
textbooks, or our own accumulated `transactions` log are all corpora.

### 5.2 Token, tokenization, and subwords

**What it means.** Before a language model sees text, the text is chopped into **tokens** — the units the
model actually counts and predicts. Modern models use **subword** tokenization, usually **BPE**
(byte-pair encoding), which learns frequent character sequences from training data.

**The Tamil problem — "token explosion".** BPE vocabularies are learned mostly from English. A long
agglutinated Tamil word matches nothing in that vocabulary, so it shatters into meaningless fragments —
pieces that are not morphemes and carry no grammar. Consequences:

- Tamil consumes roughly **3–5× more context** than English for the same content.
- Long fragmented sequences degrade the model's reasoning.
- Embeddings of fragments miss the semantic root, so retrieval (RAG) finds the wrong things.

**Crucially, a token is not a morpheme.** BPE splits by statistics; morphology splits by meaning. The
project's core architectural claim is that giving the model *morphemes* instead of fragments is the fix —
and that this is an architectural change, not something more training data solves.

### 5.3 Segmentation

Marking where a word divides into its parts: மரத்தில் → மரம் | அத்து | இல். Our accumulated segmentation
data is one of the three planned Hugging Face datasets, and it is exactly the training input a
grammar-first tokenizer (DESIGN.md L1) needs.

### 5.4 Treebank

**What it means.** A corpus where every sentence has been annotated by linguists with its grammatical
structure — parts of speech, morphology, and the syntactic relations between words ("tree" as in the
sentence's structure tree).

**In the project.** **Aalamaram** is the largest public Tamil treebank, ~10k sentences. It is a
*treebank*, not an equivalents dataset — an earlier framing got this wrong and D-008 corrects it.

### 5.5 UD — Universal Dependencies

**What it means.** A cross-language standard for annotating grammar, so the same tagset works for many
languages.

**The tension.** Uniformity across languages is bought by dropping language-specific categories. UD cannot
express Tamil's திணை (rationality), சாரியை (euphonic increments), or sandhi effects. Aalamaram adjusts UD
for Tamil clitics and segmentation; our own schema keeps the Tholkappiyam categories UD lacks. When you
read "UD-adjusted" in our docs, this is what is being adjusted for.

### 5.6 Dependency parse, head, and dependent

**What it means.** A representation of a sentence as links between words: each word is attached to a
**head** it depends on. In "மரத்தில் பறவை அமர்ந்தது", the verb அமர்ந்தது is the head, and மரத்தில்
attaches to it as a locative dependent.

**Why we would want it.** Generation Stage B (DESIGN.md §8.2): you cannot ask "what grammatical slot comes
next" without a notion of structure.

### 5.7 Gold, silver, and disputed data

**Gold** — verified, high-confidence, suitable as ground truth. **Silver** — automatically produced,
plausible, unverified. **Disputed** — cases where authorities genuinely disagree (common in origin
classification and in native-equivalent choice).

We publish all three as separate splits rather than quietly dropping the awkward ones. Reporting a dispute
as a dispute *is* the honest answer.

### 5.8 Benchmark, fixture, and contamination

**Benchmark** — a fixed question set used to measure a system. **ILAKKANAM** is the first Tamil-specific
linguistics benchmark: 820 questions from Sri Lankan school exams, Grades 1–13.

**Fixture** — one test item in our own eval set, with its answer hand-verified against an anchor source.

**Contamination** — when test items leak into training or reference data, so the system appears to know
answers it has actually memorised. Our guard: every fixture word is flagged in `data/eval_fixtures.json`
and excluded from published datasets. Fixture words must never appear in an export.

### 5.9 Perplexity and bits per character

**What they measure.** How surprised a language model is by real text — lower means the model predicts it
better. **Bits per character** normalises this so that models using *different tokenizations* can be
compared fairly.

**Why the project needs it.** The "cheap probe" in DESIGN.md §8.3 compares a BPE-token model against a
morpheme-unit model. Comparing them by per-token perplexity would be meaningless, because they count
different units; bits per character is the honest comparison.

### 5.10 A/B evaluation and "lift"

**A/B** — run the same questions two ways (bare LLM vs LLM with our server attached) and compare.
**Lift** — the improvement attributable to the second arm.

**Morphological lift** is this project's north-star metric (D-005): how much better an LLM answers Tamil
linguistics questions when it can call our tools. Reported per linguistic category, because the whole
argument is that the gain concentrates in morphology.

### 5.11 Zero-shot, fine-tuning, continued pretraining

**Zero-shot** — asking a model to do a task with no examples and no training. ILAKKANAM's published
scores are zero-shot.
**Fine-tuning** — further training on task-specific examples. Our planned instruction dataset (M8) is for
this.
**Continued pretraining** — taking an existing model and training it further on a lot of new-language
text, usually after expanding its vocabulary. This is the L2 route to a Tamil SLM.

### 5.12 SLM, LLM, RAG

**LLM** — large language model. **SLM** — small language model; compact enough to train and run cheaply,
which is the only realistic route to a Tamil-specific model for a project this size.
**RAG** — retrieval-augmented generation: fetch relevant documents, then answer from them. Item M7 is
about making retrieval work on Tamil by embedding de-agglutinated roots instead of fragmented text.

---

## 6. Terms this project coined or uses in a specific way

**Anchor tier / evolving tier.** Our two-tier source model. Anchors are stable and version-pinned
(ThamizhiMorph, the Tamil Lexicon, pinned Tholkappiyam editions). Evolving sources are
community-contributed and grow (Tamil Wiktionary). Anchors are pinned by *version*; evolving sources by
*retrieval date*.

**Provenance.** The record attached to every claim: which source produced it, which tier, and when it was
retrieved. This is what lets the agent say "root per ThamizhiMorph; வேற்றுமை per Tholkappiyam
வேற்றுமையியல்; equivalent கணினி per the TVA கலைச்சொல், retrieved 2026-06-28."

**Attested.** A claim some authority actually records — as opposed to one the model produced. The
attested-only rule governs native equivalents specifically: never invent a coinage. Note the distinction
raised in DESIGN.md §8.4: an inflected form produced by the FST is *rule*-attested, not *source*-attested,
and the two must not be confused.

**Honest gap.** Returning "no source covers this" instead of a fluent guess. The single most important
behaviour the project tests for.

**De-agglutination layer.** What the server *is*, framed by its function: it takes agglutinated Tamil and
hands the LLM clean roots plus explicit grammar. Framing it this way is deliberate — it is why the server
earns a tool call on *any* Tamil word task, not only explicit grammar questions.

**Morphological lift.** See §5.10.

**Realizer.** The generation-direction component (DESIGN.md §8, Stage C): given a lemma and a feature
bundle, produce the correct surface form, sandhi included. "Surface realization" is the standard term in
the literature.

---

## 7. False friends — where the technical term does *not* fit Tamil

These are the mismatches worth arguing about. They are not pedantry; each one is a place where using the
imported term uncritically would misdescribe Tamil.

| Technical term | Why it does not simply equal the Tamil concept |
|---|---|
| "root" | Used loosely in NLP for what is really the **lemma**. வேர்ச்சொல் is an etymological claim about a word family; a lemma is a lookup convention. Our tools return lemmas. |
| "stem" | Often used interchangeably with lemma in casual writing, but பகுதி is a distinct thing — மரத்- is the stem, மரம் the lemma. |
| "gender" | Tamil's பால் is crossed with திணை (rationality). "Neuter" is not a faithful translation of ஒன்றன்பால். |
| "case" | Maps well for வேற்றுமை 2–7. The 1st (எழுவாய்) and 8th (விளி) are not marked in the same way, so a flat list of eight overstates the parallel. |
| "part of speech" | Standard tagsets have a dozen classes; Tholkappiyam has four (பெயர்/வினை/இடை/உரி), carved differently. Neither maps cleanly onto the other. |
| "token" | Not a word, not a morpheme — an artefact of how a model was trained. Most Tamil confusion in LLM discussions comes from conflating these three. |
| "affix" | English affixes include prefixes; Tamil is overwhelmingly suffixing. விகுதி, இடைநிலை and சாரியை are three functionally distinct kinds of suffix that "affix" flattens into one. |
| "sandhi" | Borrowed from Sanskrit grammar. புணர்ச்சி's own three-way தோன்றல்/திரிதல்/கெடுதல் classification is more specific than the generic term, and we keep it. |
| "morpheme" | Fine as a concept, but do not equate it with எழுத்து. A single எழுத்து may be a morpheme, part of one, or purely the residue of a விகாரம். |

---

## 8. Two worked examples

Everything above is a label for some part of these two diagrams. If a term is unclear, find it here first.

### 8.1 மரத்தில் — "in the tree"

```
Surface form        மரத்தில்
Lemma               மரம்                    (the dictionary headword)
Stem (பகுதி)         மரத்-                   (what the suffix attaches to)
Morphemes           மரம்  +  அத்து  +  இல்
                     |        |         |
                   பகுதி    சாரியை     விகுதி / வேற்றுமை உருபு
                   stem    euphonic    case suffix
                           increment
Sandhi (புணர்ச்சி)    ம் → த்   — a திரிதல் (substitution) at the சந்தி
Feature bundle      POS: பெயர்ச்சொல் (noun)
                    திணை: அஃறிணை        (rationality — UD cannot express this)
                    எண்: ஒருமை
                    வேற்றுமை: 7 (கண் — locative)
```

**How the project handles it.** `get_root` returns மரம். `explain_formation` returns the three morphemes
plus the ம்→த் விகாரம், citing நன்னூல் for the six-part labels and Tholkappiyam for the sandhi rule.
`explain_grammar` returns the feature bundle. `classify_origin` returns இயற்சொல் (native). This word is
one of the project's eval fixtures — its அத்து split is the check used to prove the server answers
correctly when invoked.

### 8.2 செய்வித்தான் — "he had (it) done"

```
Surface form        செய்வித்தான்
Lemma               செய்
Morphemes           செய்  +  வி  +  த்  +  ஆன்
                     |       |      |      |
                   பகுதி   இடைநிலை இடைநிலை  விகுதி
                   stem   causative  past   person-number-gender
                          (பிறவினை)  tense
Feature bundle      POS: வினைச்சொல் (verb)
                    வினை வகை: பிறவினை (causative)
                    காலம்: இறந்த காலம் (past)
                    இடம்: படர்க்கை (3rd person)
                    பால்: ஆண்பால்
                    எண்: ஒருமை
                    முற்று/எச்சம்: வினைமுற்று (finite)
```

**How the project handles it.** Two stacked இடைநிலைகள் — causative வி and tense த் — which the v1
formation decoder initially got wrong and now decodes correctly (fixed 2026-07-20). This example is the
clearest illustration of why a **feature bundle** is the right interface for generation: a model that
wants to say "he had it done" should not have to produce the string செய்வித்தான் — it should produce
`செய் + {causative, past, 3sg masculine}` and let the realizer build the word.

---

## 9. Where to go next

- **The program map and roadmap** — `DESIGN.md`
- **The server specification** — `Thamizh-MCP-blueprint.md`
- **What is actually built right now** — `CODE-STATUS.md`
- **Why a past choice was made** — `DECISIONS.md`
- **Tamil grammar itself, with Tholkappiyam citations** —
  `thamizh-mcp-builder/references/tamil-grammar.md`
- **The research this rests on** — `thamizh-mcp-builder/references/research-grounding.md`,
  `From_Phonemes_to_Meaning.md`

*Corrections welcome and expected — if a mapping here misdescribes Tamil grammar, the mapping is wrong,
not the grammar.*
