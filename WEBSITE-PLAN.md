# thamizh-ai.org — public design & architecture site

> Plan, drafted 2026-08-18 and revised the same day. **Session 1 is built and shipped** —
> `github.com/ief-global/thamizh-ai`, PR #1. Decisions recorded as D-019 and D-020.
> Replaces the deck as the canonical way this project explains itself.
> Companion docs: `DESIGN.md` (program), `Thamizh-MCP-blueprint.md` (server),
> `BRAND.md` (identity + Tamil rendering rules), `distribution-roadmap.md`,
> `anti-ai-writing-style.md` (**binding for every word of site copy**).

## 0. Why the deck failed, and what changes

`PRESENTATION-SOURCE.md` is accurate and well sourced. Its problem is structural: its spine is a
**demo**. Ten slides, six of them worked word examples. A Tamil scholar reads it and learns that the
tool splits மரத்தில் correctly. They do not learn what the project *is*, why it exists, what it is
made of, or where it goes.

The fix is not fewer examples. It is a different spine.

**New spine: four layers and a horizon.** Each layer is one page, each page answers one question, and
the layers visibly stack. Word examples appear **once**, on the morphology page, used as anatomy
rather than as proof. Everything else is the argument.

```
   layer 1   இலக்கணம்              grammar        what makes an answer true
   layer 2   பகுபத உறுப்பிலக்கணம்   morphology     how a word is taken apart
   layer 3   மூலம்                 sources        what it grounds on
   layer 4   பகிர்வு                distribution   how it reaches people
   ──────────────────────────────────────────────────────────────────────
   horizon   தமிழ் மொழி மாதிரி       a Tamil-native model     not scheduled

   Read top to bottom, layer 1 first. Every use feeds verified data back down.
```

The single sentence the whole site exists to land:

> இலக்கணம் alone is a book — it knows the rules but cannot apply them to the word you just typed.
> Morphology alone is a machine — it splits words but cannot tell you which authority says the split
> is right. Put them together and you get an answer that is computed *and* citable. That is the
> product.

## 1. Feedback on the idea itself

**Do it.** Static pages on Cloudflare Pages cost nothing, the domain is already owned (D-013), and a
public, citable design site is worth more than a deck for three reasons:

1. **It makes the sourcing letters land.** The TVA and DSAL letters are drafted and unsent
   (`sources/correspondence/`). A letter that says "here is our architecture, our sources, our
   licence position, and what we are asking you for" with one URL is a different letter from one that
   points at a GitHub repo of Markdown. Same for writing to Sarveswaran about ThamizhiMorph,
   Aalamaram and ILAKKANAM. **N7 is blocked on people replying to us, and this is the thing that
   makes replying easy.** That puts the site on the critical path, not beside it.
2. **Scholars read at their own pace.** A deck needs a presenter. Pages get forwarded, quoted, and
   argued with — which is exactly the correction loop `README.md` asks for.
3. **Nothing gets thrown away later.** These pages become the app's design and documentation section
   when the app ships (§2). Same repo, same tokens, a nav change rather than a rewrite. There is no
   archiving decision to make later.

**Four conditions, all of them real:**

- **Freeze the content URLs on day one.** The app takes the apex later (§2), so every page has to be
  published at the address it will still have in two years, and the app's paths have to be reserved
  before anything else claims them.
- **Do not restate a number the design repo already owns.** A third copy of "266 tests" will go stale
  within a month. Mechanism in §6, not willpower.
- **Timebox it.** Three build sessions. If it starts eating the N5 origin work or the N6 eval, stop
  and ship what exists behind a "draft" banner. A site is not the product.
- **Public means the guardrails tighten.** A wrong நூற்பா on a deck is embarrassing for an hour. On
  a site it is quotable forever. `BRAND.md`'s accuracy rules and the ஜன்னல் trap carry over
  unchanged, and every Tamil string on the site gets checked against the pinned texts or the live
  build before it ships.

## 2. Domain — the site is a phase, and it ends (DECIDED 2026-08-18)

Saran's call, and the reasoning matters more than the mechanics: **once the app is live, the app should
speak for itself.** How we got here is history. A scholar should not be bookmarking a design page and
coming back to re-read it. They should be using the tool and judging it.

So this site is deliberately temporary. It carries the design and architecture while there is nothing
public to use, and when the app takes the apex, this becomes an archive.

**What that changes:** URL permanence stops being a design constraint, which removes a lot of
complexity. No path reservation, no `/design` prefix, no subdomain gymnastics. Content sits at clean
top-level paths and the app overwrites them when it arrives.

**What still has to be planned, because letters outlive websites:** the TVA and DSAL letters will quote
a URL, and a reply may land a year later. Three cheap moves cover it, all decided now so they are not
improvised on launch day:

1. **Letters cite the GitHub repo alongside the site.** `github.com/ief-global/thamizh-mcp-design` is
   the durable address and it is already public. The site URL is the readable one; the repo URL is the
   one that still resolves in 2029.
2. **On app day, every old page redirects to the app home** rather than 404ing. Cloudflare bulk
   redirects, one afternoon. A scholar following an old link lands on the working tool, which is
   exactly the outcome Saran wants.
3. **The archive is a git tag plus a static snapshot** of `dist/` attached to a GitHub release. Anyone
   who genuinely wants the design history has it, and it costs nothing to keep.

**The site says this about itself.** `/about` carries one line: this site documents how the tool was
designed, and it will be archived when the tool goes live. Publishing an expiry date is on-brand for
a project whose whole pitch is honesty about its own state.

Record as **D-019**.

## 3. Stack

**Astro 5**, TypeScript, content in Markdown/MDX, deployed to Cloudflare Pages.

Why:

- Ships **zero JavaScript** unless a page asks for it. Most pages here are prose and an SVG. The
  audience includes people on a mid-range Android in Chennai on a bad connection, and that matters
  more than any framework feature.
- Content is Markdown, which is what this repo already writes. Moving a section from `DESIGN.md` into
  a page is a copy-edit, not a port.
- Islands (`client:visible`) for the three or four things that genuinely need interaction, written in
  plain TypeScript. No React, no Tailwind, no component library.
- i18n routing is built in, so the Tamil mirror (§5) is a directory, not a second site.
- Builds to plain static files. Cloudflare Pages serves them free, with a preview deploy per PR —
  which means Saran reviews the rendered Tamil before merge, not after.

Rejected: Next.js (server runtime we do not need), Docusaurus/VitePress (docs-shaped; the diagrams
would fight the theme), plain hand-written HTML like `deck/index.html` (fine at 14 slides, painful at
11 pages with shared nav, a Tamil mirror, and a status file), Slidev/reveal.js (still a deck).

**Fonts are the highest-risk item, same as the deck.** Self-host Noto Sans Tamil as woff2 in the
repo (SIL OFL, redistributable). No Google Fonts CDN: it is a third-party dependency, a privacy
question for an audience in India, and the one failure that costs credibility instantly. Preload the
Tamil face, `font-display: swap`, and keep the BRAND.md conjunct test (ற்ற ன்ற க்ஷ ஸ்ரீ) as a
literal test page at `/_render-check` that never gets linked but is checked every deploy.

## 4. Page map

**Sixteen pages: ten core, six source pages.** Each answers a single question, and every page footer
names the design-repo document it derives from.

| Path | Question it answers | Diagram |
|---|---|---|
| `/` | What is this and what is it made of? | **D1 layer stack** (clickable, it *is* the nav) |
| `/why` | Why does a language with 2,000 years of codified grammar count as "low-resource"? | **D2 token explosion** |
| `/grammar` | What makes an answer true here? (இலக்கணம், Tholkappiyam-first, citation) | **D3 நூற்பா → cited rule table → answer** |
| `/morphology` | பகுபத உறுப்பிலக்கணம் — how is a Tamil word taken apart, and why can a dictionary never do it? | **D4 பகுபத உறுப்பு anatomy** (the one example) |
| `/engine` | **What have we actually built?** The nine tools, what each is for, how they chain. | **D6 engine map + tool chain** |
| `/sources` | What do we ground on, and what may we use it for? | **D5 grade × redistribution ledger** |
| `/distribution` | How does this reach a Tamil speaker who will never install anything? | **D7 one engine, many heads** |
| `/horizon` | Where does this go, and what is honestly not scheduled? | **D8 flywheel + stages A–F** |
| `/status` | What works today, what does not, measured. | table from `status.json` |
| `/glossary` | What does this term mean in Tamil grammar? | — |
| `/about` | Who is doing this, under what licence, and how do I write to them? | — |

**Source pages, one per institution or project.** Each states what it is, who made it, what we use it
for, what terms govern it, and what we are asking for. A letter can then link one page instead of
explaining itself.

| Path | Subject | Why it has its own page |
|---|---|---|
| `/sources/thamizhimorph` | **ThamizhiMorph** — Sarveswaran, Dias & Butt (2021) | **The build starts here.** The FST we wrap is the engine's morphological anchor. Also the doorway to the wider Thamizhi suite (§4.2). |
| `/sources/project-madurai` | The pinned Tholkappiyam and Nannūl | Every grammar claim quotes a நூற்பா from these editions. Explains the pin, the checksum, and the header-intact redistribution grant. |
| `/sources/tva` | **Tamil Virtual Academy** கலைச்சொல் | The open ask that matters most. Retires the one licence gap we ship. |
| `/sources/aalamaram` | The Tamil treebank (WILDRE @ LREC 2024) | Adopted, not obtained. States exactly what we would do with it and what we need to know about its terms. |
| `/sources/ilakkanam` | The Tamil linguistics benchmark (arXiv:2511.12387) | It is how we measure ourselves, and it is not public yet. Watch page. |
| `/sources/madras-lexicon` | Madras University Tamil Lexicon | Closed with a reason, published. CC BY-NC-ND and robots-disallowed. Consult-and-cite only. |

### 4.2 The Thamizhi suite — how we credit it

`/sources/thamizhimorph` is the most important source page on the site, and not only because the FST is
load-bearing. It is also the page Sarveswaran will read if he is written to, so it gets built with that
in mind: accurate, credited, and specific about what we took and what we did not.

What it carries:

- **ThamizhiMorph** (`github.com/sarves/thamizhi-morph`, Apache-2.0) — the analyser *and generator*
  we wrap. Cite Sarveswaran, Dias & Butt, *Machine Translation* 35:37–70 (2021), with the paper's own
  measured numbers on its 612-word textbook corpus rather than our paraphrase. Say plainly that we use
  only the analysis direction today, and that the generation direction is what the whole `/horizon`
  track is waiting on.
- **Why we excluded the guesser FSTs** — they return confident wrong lemmas (கொடுத் for கொடு), and we
  would rather have an honest gap. This is a design compliment to the tool, not a criticism, and it
  shows we read it properly.
- **The wider suite, and where each one lands on our roadmap:**
  - **ThamizhiPOSt** (`sarves/thamizhi-pos`, Apache-2.0) — neural POS tagger. Needed for M6, contextual
    disambiguation, which is Stage A of the generation track.
  - **ThamizhiLIP** (`sarves/thamizhilip`, Apache-2.0) — linguistic processing pipeline. Same track.
  - **Thamizhi Validator** (`sarves/thamizhi-preprocessor`) — the native-vs-borrowed signal named in
    D-002 and still unwired. It is roadmap item **N5**, our top open code item.
  - **ThamizhiUDp** (`sarves/thamizhi-udp`) — UD parser for Tamil. Stage B, dependency structure.
  - **Aalamaram / IWTTA** — same lineage, own page.
- **One more paper worth citing on `/why`:** *Egalitarian Language Representation in Language Models: It
  All Begins with Tokenizers* (COLING 2025, materials at `sarves/tokenizers-coling2025`). It is the
  tokenizer argument our `/why` page makes, from the same research group whose FST we build on.
  ⚠️ **Verify the author list and the exact venue citation before it ships** — we do not cite from a
  repo description, same rule as நூற்பா numbers.

### 4.3 What goes on each page

**`/` home.** A hero, the wordmark தமிழ்AI, one paragraph, the layer stack, a four-number status strip
(tools, tests, origin accuracy, last verified date), two repo links. Nothing else.

**The stack is the navigation**, and it reads **top to bottom, layer 1 first**, ending at the horizon.
Two levels of disclosure, both on the home page:

- **Click a layer** and it expands in place to show what its page carries. Cheap, no JS framework, works
  without JavaScript if the detail ships as a `<details>` element.
- **"Explain this layer"** opens a small dialog with a fuller plain-language explanation, written for
  someone who knows Tamil grammar and has never met an FST. This is where a scholar decides whether the
  project is serious, so the dialog copy gets the same care as `/why`.

Native `<dialog>`, focus trapped, Escape closes, no library.

**`/why` — the history, and the gap.** This is the page that carries the soul, so it gets written
first and hardest.

The argument, in order:

1. Tamil grammar has been written down and argued over since Tholkappiyam. The rules are not missing.
2. "Low-resource" is a claim about **machine-readable data**, not about literature. Say this
   explicitly, because a Tamil scholar hears "low-resource" as an insult and it is not one — it is a
   description of a pipeline failure.
3. What an LLM actually does with Tamil: BPE tokenizers trained on English shred agglutinated words
   into fragments that mean nothing. Roughly 3–5× the context for the same content
   (`tamil_llm_tokenization_analysis_gemini.md`), embeddings that miss the root, reasoning that
   degrades over long fragmented sequences.
4. Measured evidence, not vibes: ILAKKANAM (arXiv:2511.12387), 820 school-exam questions, Grades
   1–13. Best frontier model 79.6%. Accuracy falls as the grade rises. The paper's own conclusion:
   performance tracks exposure, not understanding.
5. What we are not doing: retraining a base model. That costs money nobody here has and fixes
   nothing about citation.
6. What we are doing instead: put the grammar where the model can look it up, and make every answer
   name its source.

**`/grammar`.** Tholkappiyam first, Nannūl where Tholkappiyam does not codify the point. Grammar
rules ship as **cited data tables**, not code (D-014), so the linguistics can be audited without
reading Python. The pinned texts are read at runtime, so a claim quotes its நூற்பா (D-018). Where
the two authorities differ we record the difference rather than collapsing it. And the trap worth
telling scholars about: நூற்பா numbers from secondary sources are wrong often enough that we pinned
the full editions (TVA's 336/319/136 are 337/320/137).

**`/morphology`.** The bridge page the whole site needs:

- பகுபத உறுப்பிலக்கணம் **is** what computational linguists call morphological analysis. Same job,
  different vocabulary, 2,000 years apart.
- Tamil is agglutinative: one root generates thousands of surface forms. Number them if it helps.
  A dictionary cannot list them, which is why the core is a rule engine rather than a database.
- An FST is a machine that runs a வாய்பாடு in both directions — it can take a word apart and it can
  build one. We use one direction today; the other is the whole generation track.
- Credit **ThamizhiMorph** (Sarveswaran, Dias & Butt 2021) prominently and by name, with the
  measured coverage numbers from the paper. We wrap it; we did not rebuild it.
- **Then the join:** grammar supplies the authority, morphology supplies the mechanism, and neither
  is a product on its own. One anatomy figure of a single verified word, each part labelled with its
  role and the authority that names it. One word, once.

**`/sources`.** The index and the ledger. Every source in one table with its evidential **grade (A–D)**
and its **redistribution mode** as independent axes (D-016, D-017). That model is genuinely unusual and
scholars will recognise why it matters: a source can be excellent evidence and still be one we may only
consult and cite.

Three groups, each row linking to its own page where it has one: **pinned** (Project Madurai classical
texts, ThamizhiMorph, Tamil Wiktionary, our verb paradigms) · **asked for** (TVA கலைச்சொல், Aalamaram,
ILAKKANAM) · **closed with a reason** (Madras Lexicon).

Stated plainly on this page, per Saran's call: the S2PT word lists we ship have **no stated upstream
licence** (D-017). It is the one genuine gap, we know it, and the TVA ask is what retires it. Saying it
in public is what makes the rest of the page believable.

**`/engine`. The scorecard, and the page Saran cares most about.** What exists, what each piece is
for, and how the pieces chain. Written so a scholar can judge the work without reading Python, and so a
developer can see the shape before installing anything.

Three parts:

1. **The nine tools, each with its objective in one line.** Grouped by what they are for, not
   alphabetically:
   - `analyze_word` — the front door. Composes every other tool into one grounded answer and merges
     the provenance. This is the only tool most callers ever need.
   - `classify_origin` · `get_root` · `get_meaning` — the three fact-finders: where the word came from,
     what its lemma is, what it means.
   - `explain_formation` · `explain_grammar` — the two grammar tools: the six பகுபத உறுப்பு with the
     புணர்ச்சி at each join, and the word class, வேற்றுமை, tense and person-number-gender.
   - `suggest_native_equivalent` — conditional, non-native words only, attested candidates only.
   - `enrich_word` · `refresh_sources` — the two writers, one word and one batch. They are how coverage
     grows without anyone maintaining a word list.
2. **How they interconnect, drawn (D6).** `analyze_word` fans out to the six read tools; all of them sit
   on one engine; the engine reads anchors first, falls back to evolving sources, writes back to the
   knowledge store with provenance, and every path can return a gap instead of an answer. The two
   writers feed the same store from the side. Show the store's `transactions` log leaving the diagram
   toward `/horizon`, because that link is the whole long-term argument.
3. **What each tool refuses to do.** This is the part that earns trust with this audience, and every
   line of it is already true in the code: ambiguous morphology returns *all* analyses rather than a
   silent pick · a join the FST cannot determine is left unnamed rather than invented · திரிசொல் and
   திசைச்சொல் are never guessed · a coinage with no attestation never surfaces · no FST analysis means
   an honest gap, not a stemmer's best effort.

Also on the page: the design point that the web head needed **zero engine changes**, which is the
evidence that "one engine, many heads" was real rather than a diagram.

**`/distribution`.** MCP server for AI assistants, REST for apps, a browser page for people who will
never install anything, CLI, mobile last. Registries and where the code will be installable from.
Hugging Face datasets as a second output. Adoption, not monetisation — say it, because the audience
will wonder.

**`/horizon`.** Stages A–F from `DESIGN.md` §8, with the honesty intact: written down, not
scheduled. The flywheel — every analysis becomes provenance-tagged gold data, gold data becomes
published datasets, datasets train a morpheme-first tokenizer, and that is the actual road to a
Tamil SLM. And the reframe that keeps it sane: the endpoint is a **hybrid**, where a frontier model
handles meaning and our engine handles morphology and realisation.

**`/status`.** Rendered from `status.json`. Working, not working, measured numbers, date verified.
The "not done yet" list from `PRESENTATION-SOURCE.md` slide 8 lives here permanently and stays
current.

**`/glossary`.** `Glossary.md` is already the right document and it is 579 lines of exactly what
this audience needs: computational vocabulary mapped onto வேற்றுமை/விகுதி/சாரியை. Publishing it is
close to free and it is plausibly the most-linked page on the site within a year.

**`/about`.** IEF, Apache-2.0 code, content licence (§7), how to contribute a correction, and a
contact address that a government office is willing to write back to. Plus the line from §2: this site
documents how the tool was designed, and it will be archived when the tool goes live.

## 4b. Visual direction — hero imagery (CHANGED 2026-08-18)

Saran's call: the site should impress a first-time visitor, with a hero image and colour, drawn from
classical Tamil material.

**This overrides `BRAND.md`.** That file currently says "no Indian-cultural clip art, no temples, the
typography is the culture", written for a projector deck. It needs amending rather than ignoring, so
the rule does not get re-litigated every time someone reads it. Proposed replacement rule:

> Photography of **primary Tamil sources and monuments** is welcome and must carry its citation like
> any other claim. Generic "Indian culture" stock imagery, kolam borders, diyas and AI-brain art stay
> banned.

That keeps the discipline and gets the warmth. And it does something better than decoration: **the hero
image cites itself**, which is the same promise the product makes about every grammar claim.

**Two images chosen, both verified 2026-08-18 and both free of licence friction:**

| Image | Licence | Where |
|---|---|---|
| Palm-leaf manuscript of **தொல்காப்பியம்** (Commons, uploaded from tamilvu) | **Public domain** | The strip under the hero. It is literally the text the project is grounded on. |
| **வட்டெழுத்து** inscription, Brihadeeswara temple, Thanjavur (Commons, by "deadrat") | **CC0** | Full-bleed hero, warm rose granite, darkened under the wordmark. |

Public domain and CC0 mean no attribution obligation, and we attribute anyway with a link to the
Commons file page. A nonprofit site that quietly used an unlicensed photo while lecturing about source
provenance would be a bad joke.

**Colour.** The brand palette holds — maroon `#7a1f2b` and indigo `#2f3d6b` on warm neutrals — and the
stone image brings the rose and ochre that make the page feel warm without a new accent fighting the
old ones. One added token, an ochre for hero eyebrows and rules. Still no gradients, no neon, no
"AI purple".

**Where images appear, and where they do not.** Hero on `/` only, a narrow source strip on `/grammar`
and `/sources/project-madurai`, and a portrait on each source page where one exists and is properly
licensed. Diagram pages stay image-free: **D1 to D8 are typography and SVG**, because a photo behind a
diagram is decoration and this audience reads diagrams closely.

## 5. Language (DECIDED 2026-08-18)

**English-first with Tamil terms inline**, structured for a Tamil mirror from day one (`/` and `/ta/`).

Reasoning: licensing and architecture language needs precision, and the developer audience is
English-reading. But TVA is a Tamil institution, the scholars are the point, and an English-only
site asking for Tamil government glossaries reads badly.

So: build the i18n routing in session 1 even though `/ta/` is empty. Translate `/`, `/why`,
`/morphology` and `/sources` first — the four pages an outreach letter would link. Saran corrects
the Tamil; nothing goes live in Tamil unreviewed.

## 6. Keeping it honest — the anti-drift mechanism

Two repos already work to stay in sync. A third copy of the same claims is the obvious way this goes
wrong, so the site is built as a **view**, never a fork:

- **`src/data/status.json` is the only place a number lives.** Test count, sweep results, tool count,
  each with `verified_on` and a link to `CODE-STATUS.md`. Pages read from it. No number is typed into
  prose anywhere.
- **`src/data/sources.json`** is a committed snapshot of the code repo's registry, refreshed by
  `npm run sync:sources`. Deterministic builds, one command to update.
- **Every page footer names its source document** in the design repo. If the page and the doc
  disagree, the doc wins.
- **A line in both repos' `CLAUDE.md`:** when a measured number changes, `status.json` changes in the
  same session.
- The accuracy guardrails currently at the bottom of `PRESENTATION-SOURCE.md` (ஜன்னல், no invented
  lift %, "plausibly the first சொல்-analysis MCP server", ThamizhiMorph attribution) move into the
  site repo's `CLAUDE.md` and become build-time rules.

## 7. Repo, licence, cost

- **New repo `ief-global/thamizh-ai`.** Site now, and the app's front-end later when M2 ships — same
  tokens, same components, so nothing gets rebuilt.
- Branch flow identical to the other two: work on `develop`, PR to `main`, Saran merges. Cloudflare
  Pages builds a preview per PR and the apex from `main`.
- **Licence:** code Apache-2.0 (matches the code repo). Prose and diagrams **CC BY-SA 4.0** — it is
  the safe choice given Wiktionary-derived text is already CC BY-SA, and share-alike is the right
  signal for a nonprofit publishing scholarship. Record as **D-020**.
- **Cost: $0.** Cloudflare Pages free tier, domain already owned. No backend, no database, no forms.
- **Contact:** a plain `mailto:` to an address IEF controls. No form, so no backend and no spam
  pipeline to babysit. Needs one decision: which address.

## 8. Build sequence

Four sessions now, since the site went from 11 pages to 16. Each one ends deployable.

**Session 1 — skeleton, hero, and the argument. ✅ DONE 2026-08-18.** Repo, Astro, tokens from `BRAND.md` plus the ochre,
self-hosted Tamil font, `/_render-check` conjunct page, layout and nav, i18n routing, `status.json`,
Cloudflare Pages connected. Pages: `/` with the hero, **D1** the layer stack with its dialogs, and
`/why` with **D2**. Ship behind a draft banner.

**Session 2 — the layers.** `/grammar` (D3), `/morphology` (D4), `/engine` (D6). The engine page is the
scorecard and the diagram is the most detailed on the site, so it gets the room.

**Session 3 — the sources.** `/sources` (D5) and all six source pages, ThamizhiMorph first and most
carefully. This is the outreach session, and it is what the TVA and DSAL letters will link.

**Session 4 — close it out.** `/distribution` (D7), `/horizon` (D8), `/status`, `/glossary`, `/about`.
Link checker in CI, full Tamil proofread, remove the draft banner.

**Session 5, separate and optional — the Tamil mirror** for `/`, `/why`, `/morphology` and `/sources`.

**Measurement to run before D2 can be honest:** we currently quote "3 to 5× more context" from a
secondary analysis. Nobody has published that table for Tamil with a named tokenizer and a date. Run it
ourselves, over a fixed sentence set, with `tiktoken` (o200k and cl100k) plus one open multilingual
tokenizer, and publish the numbers with the tokenizer version and the date. It costs an hour, and the
COLING 2025 tokenizer paper (§4.2) is the scholarly companion to our own measurement.

## 9. What this does to the existing material

- `PRESENTATION-SOURCE.md` stops being the canonical narrative and gets a header saying so. Its
  verified examples stay useful as a fact-checked pool for `/morphology` and `/engine`.
- `deck/index.html` stays as-is for in-person talks. It is a good deck for a room with a projector,
  which is a different job from a site.
- `BRAND.md` needs two amendments: the **imagery rule** in §4b, which reverses a current "don't", and
  web-specific rules (self-hosted fonts, dark mode, minimum tap target, the `/_render-check` page).
  Amend the file rather than working around it, or the next reader follows the old rule.

## 10. Decisions

**Settled 2026-08-18:**

1. **Domain (§2)** — the site is a phase and it ends. The app takes the apex, old URLs redirect to it,
   the archive is a git tag plus a release snapshot, and letters cite the repo alongside the site
   → **D-019**.
2. **Language (§5)** — English-first, Tamil mirror for the four outreach pages, nothing published in
   Tamil unreviewed.
3. **Layer 3 is `மூலம்`**, and the stack reads top to bottom from layer 1 (§0).
4. **A page per institution** rather than one combined sources page (§4), with
   `/sources/thamizhimorph` treated as the most important of them.
5. **Hero imagery is in** (§4b), which amends `BRAND.md`. Public-domain and CC0 sources only, cited.
6. **The S2PT licence gap stays public** on `/sources`.

**Still open:**

7. Content licence (§7) — recommend CC BY-SA 4.0 → **D-020**.
8. Contact address for `/about`. A government office has to be willing to write back to it.
9. Repo name `ief-global/thamizh-ai` — confirm, and confirm who creates it under the org.
10. The COLING 2025 tokenizer citation (§4.2) — author list and venue to be verified before it ships.
