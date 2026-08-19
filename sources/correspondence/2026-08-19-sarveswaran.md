# Draft letter — Dr. Kengatharaiyer Sarveswaran

**Status:** DRAFT for Saran's review and sending. Not yet sent.
**To:** Dr. Kengatharaiyer Sarveswaran — Senior Lecturer in Computer Science, University of Jaffna;
visiting researcher, Computational Linguistics Group, University of Konstanz.
(Find the current address on `sarves.github.io`. Do not guess at one.)
**From:** Saran Saravanan, on behalf of the International Educational Foundation (IEF)
**This is not a permission request.** ThamizhiMorph is Apache-2.0 and we are well inside it. This
letter introduces the work, credits it properly, offers something back, and asks three questions.

> **Notes for Saran before sending**
>
> - **The opening fact is real and worth leading with.** While verifying a citation we found that
>   four of this project's external pillars trace to him: ThamizhiMorph (the analyser we run),
>   ILAKKANAM (the benchmark we would be judged by — he is senior author), Aalamaram (the treebank we
>   want), and the COLING 2025 tokenizer paper (whose argument our `/why` page makes). We did not
>   plan that. It emerged from following the sources.
> - **He is both a computer scientist and formally trained in Tamil** — his page lists Tamil Junior
>   Pundit (Bala Pundit), 2016. That combination is rare and is exactly what this project keeps
>   needing. Worth a light touch, not flattery.
> - **Lead with what we give, not what we want.** The corrected-misses offer is the real content of
>   this letter. Everything else is context.
> - Do not overcommit on collaboration on my behalf. The letter opens the door and lets him set the
>   size of it.
> - Aalamaram's lead authors are elsewhere (Abirami et al.), so he may not be the data holder. The
>   question is phrased as "who should I ask", not "please send it".

---

Dear Dr. Sarveswaran,

I am writing on behalf of the **International Educational Foundation**, a non-profit, about a Tamil
language-technology project that is built on your work — and to offer you something back from it
before I ask you anything.

## First, an accounting

We built a source-grounded Tamil word-grammar analyser. While checking a citation last week we
noticed something we had not registered while building it: **four of the things this project stands
on are yours.**

- **ThamizhiMorph** is the morphological anchor of our engine. We wrap it; we did not attempt to
  rebuild it.
- **ILAKKANAM** (*From Phonemes to Meaning*) is the benchmark by which we intend to be judged, and
  its central finding — that model performance reflects exposure rather than understanding — is the
  reason this project exists in the shape it does.
- **Aalamaram** is the treebank we have adopted in our design and have not yet been able to obtain.
- **Egalitarian Language Representation** (COLING 2025) makes, from the tokenizer side, the argument
  our own public page makes from the measurement side.

None of that was planned. It emerged from following our sources honestly, and it is the clearest
evidence I have that Tamil is computable today because a small number of people did unglamorous work
for years. I wanted to say so plainly rather than quietly benefit from it.

## What we built

**Thamizh MCP** is a free, open-source server that analyses a single Tamil word and returns its
origin, root, meaning, formation (பகுபத உறுப்பு, புணர்ச்சி) and grammar — with every claim naming
the source that grounds it, and an explicit gap wherever no source can. It exists so that AI
assistants stop answering Tamil grammar questions from memory.

The design and the current state are public at **thamizh-ai.org**, and the page most relevant to you
is **thamizh-ai.org/sources/thamizhimorph**, which sets out exactly how we use your analyser and
where the rest of the Thamizhi suite sits on our roadmap.

Two decisions you may want to check, since they are about your tool:

- **We keep the guesser FSTs switched off.** On கொடு a guesser returns the lemma கொடுத், and a
  confident wrong lemma is the failure mode this whole project exists to remove. A word the analyser
  does not know routes to our enrichment layer and comes back as an honest gap. I record this as a
  compliment to the design: making the guessers separate and opt-in is what let us make that choice
  at all.
- **Where the FST and a நூற்பா disagree, the நூற்பா governs.** We grade ThamizhiMorph as a
  scholarly computational model rather than as primary authority — not a judgement on its quality,
  but on what kind of thing it is.

If either reading is wrong, I would rather hear it from you than keep publishing it.

## What we can give back

This is the part I actually care about.

**1. Corrected misses, hand-checked.** Every analysis our server resolves is logged with its
provenance, so the words the FST does not cover accumulate as a by-product of ordinary use, together
with what we eventually determined and on what authority. That list is yours if it is useful. We
would rather it improved the analyser everyone uses than sat in our database.

**2. Everything else we have already published, and anything we have not.** Our grammar rule tables
ship as cited JSON, each carrying its நூற்பா, checked against version-pinned Project Madurai
editions by a test that fails if a citation does not resolve verbatim. Along the way that test found
that the Tamil Virtual Academy course books renumber Nannūl — their 336, 319 and 136 are 337, 320
and 137 in the pinned edition — which is the kind of thing that is invisible from inside a syllabus.

**3. One measurement you may find mildly interesting.** In our own evaluation, a frontier model with
our tools attached, under a neutral prompt, called them **0% of the time** while answering the same
questions incorrectly from memory. The server was returning correct answers. Nothing was telling the
model to ask. We now treat tool descriptions as a product surface and "did the model invoke the tool
at all" as a permanent metric. If your group ever measures retrieval-augmented Tamil performance,
that null result may save you a confusing week.

## Three questions

1. **Aalamaram** — where is the corpus distributed, and under what terms? We could not locate it, and
   since the lead authors are elsewhere I would welcome a pointer to whom I should ask rather than
   any effort on your part.
2. **ILAKKANAM** — is the dataset likely to be released? We currently test against fixtures we wrote
   ourselves, which catch regressions but cannot be an independent measurement, since we wrote both
   the questions and the thing being tested. If it publishes, we would demote our own fixtures to
   development data and hold yours out. We would also want to tell you that our fixture words are
   flagged so they can never leak into any dataset we publish.
3. **The rest of the suite** — our roadmap treats the Thamizhi Validator as the native-versus-borrowed
   signal we are missing, ThamizhiPOSt and ThamizhiLIP as the route to word-in-context
   disambiguation, and ThamizhiUDp as the step after that. Is that the ordering you would recommend,
   or has something superseded any of it?

## And, if it interests you

We are a small non-profit with no commercial product and no intention of one. If any part of this is
worth doing together — a shared dataset, an evaluation, a student project, or simply a periodic
sanity check on our linguistics — I would be glad to discuss it on whatever terms suit you. Equally,
if the answer is that you have quite enough to do, this letter has already served its purpose by
crediting the work properly.

நன்றி,

**Saran Saravanan**
President, International Educational Foundation
`thamizh@ief-global.org`
Site: `thamizh-ai.org` · Code: `github.com/ief-global/thamizh-mcp` · Design: `github.com/ief-global/thamizh-mcp-design`

---

## Appendix — what he can verify without asking us

| Claim | Where |
|---|---|
| How we use ThamizhiMorph, and the guesser decision | `thamizh-ai.org/sources/thamizhimorph` |
| Our current measured state, including what is wrong | `thamizh-ai.org/status` |
| The tokenizer measurement, beside his COLING paper | `thamizh-ai.org/why` |
| Every source with its evidential grade and licence | `thamizh-ai.org/sources` |
| Pinned analyser version | `data/PINS.md` — commit `adbacced` |
| Cited grammar tables and the citation test | `data/grammar/*.json`, `tests/test_citations.py` |
