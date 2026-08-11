---
name: thamizh-mcp-builder
description: "Plan and build the THAMIZH MCP server — a Model Context Protocol server (and agent) for Tamil word-grammar (சொல் இலக்கணம்) analysis that grounds answers in authentic Tamil sources (Tholkappiyam-first) and self-enriches from evolving internet Tamil data instead of a hand-maintained dictionary. Use whenever the user is planning, scoping, or implementing a Tamil-language MCP server or agent that works on Tamil words: classifying native (இயற்சொல்) vs borrowed (வடசொல்/Sanskrit/English), suggesting a loanword's native Tamil equivalent (e.g. கணினி for computer), finding a word's root/lemma and meaning, word formation (பகுபத உறுப்பு, புணர்ச்சி/sandhi), or grammar (வேற்றுமை, சொல் வகை). Trigger even when the user only says 'THAMIZH MCP', 'Tamil word analyzer', or 'சொல் இலக்கணம் tool'. Do NOT trigger for other-language analyzers (Sanskrit/Malayalam/Telugu), Tamil translation/TTS/OCR/keyboard apps, or merely learning Tamil grammar or a one-off word lookup."
license: Internal project skill for the THAMIZH MCP project. (v6 — adds references/research-grounding.md (ILAKKANAM + ThamizhiMorph digests, de-agglutination rationale) and the sibling-skill map; syncs the reference list.)
---

# THAMIZH MCP Builder

## What this skill is for

This skill carries the THAMIZH MCP project from a blank page to a working, source-grounded MCP server and
the agent that sits on top of it. The product's job is narrow and deep: given a single Tamil word (சொல்),
return a **grounded, authentic** analysis covering five things the user cares about —

1. **Origin** — is it a native Tamil word (இயற்சொல்) or borrowed (வடசொல் / English / other)?
2. **Root + meaning** — the lemma / வேர்ச்சொல் and its dictionary meaning.
3. **Formation** — how the surface word is built up from its parts (பகுபத உறுப்பிலக்கணம், புணர்ச்சி/sandhi).
4. **Grammar** — the grammatical category and features behind the word (சொல் வகை, வேற்றுமை, etc.).
5. **Native equivalent** — if the word is *not* native, suggest the attested native Tamil equivalent(s)
   (e.g. கம்ப்யூட்டர் → கணினி, புத்தகம் → நூல், ஜன்னல் → சாளரம்). Applies to all borrowings — வடசொல்
   (Sanskrit), திரிசொல்/திசைச்சொல், and modern loans from English, Urdu/Persian, Portuguese, Marathi, etc.

"Grounded and authentic" is the whole point. The value of this server over a plain LLM is that every claim
traces back to a real Tamil linguistic authority — a morphological analyser, a classical grammar rule, a
standard lexicon, an etymology dataset, or an attested terminology glossary — not to the model's own guesses.
Keep that bar in front of you at every phase. A confident-but-unsourced Tamil answer is exactly the failure
mode this project exists to remove.

Three design commitments shape everything below; treat them as non-negotiable defaults:

- **Tholkappiyam first.** தொல்காப்பியம் is the golden authority for Tamil *grammar* (objectives 1/3/4) —
  prefer it over நன்னூல். (Note: objective 5's authority is the கலைச்சொல்/தனித்தமிழ் terminology tradition,
  not Tholkappiyam — see below.)
- **Self-enriching, not hand-maintained.** The tool grows its coverage from evolving internet Tamil sources;
  nobody hand-builds and babysits a giant static word list.
- **Suggest only attested equivalents (objective 5).** Never invent a native coinage. Recommend an equivalent
  only when an authority attests it; otherwise report an honest gap.

All three are spelled out in "Grounding & authenticity principles" below.

## How to use this skill

Work the phases in order. Each phase has a concrete deliverable, so the user always has something to react
to. Phase 0 is where you'll usually start — the user has asked to begin with planning.

This skill is the *domain* layer. For the generic mechanics of building any MCP server (SDK setup, transport,
tool registration, schemas, the MCP Inspector, evaluation harness) lean on the **`mcp-builder`** skill —
read its `SKILL.md` when you reach Phase 3/4. This skill supplies the Tamil-specific knowledge that
`mcp-builder` cannot: which sources are authoritative, what a word analysis must contain, and how Tamil
grammar actually works.

**Sibling skills (added 2026-07-10, D-004)** — hand off rather than absorb:
`thamizh-eval` (product benchmarks + the morphological-lift A/B — the v1 north-star metric, D-005) ·
`thamizh-data-curation` (knowledge-store/transaction-log → gold datasets, license-gated, HF publishing) ·
`thamizh-release` (license audit, PyPI/Docker, Cloud Run hosting, registry listings). This skill stays the
build/domain layer. Program-level sequencing lives in `TAMIL-HIGH-RESOURCE-ROADMAP.md`; research context in
`references/research-grounding.md`.

---

## Phase 0 — Planning & blueprint  ← usually start here

Goal: produce a written **project blueprint** the user can approve before any code exists. Do not skip to
tooling; the planning artifact is itself the deliverable.

Steps:

1. **Confirm scope.** Lock the answers to: which source languages count as "borrowed" (Sanskrit/வடசொல் is the
   classic case; also English, Urdu/Persian, Portuguese, Marathi, Telugu, etc.); whether input is a single
   word only or also phrases/sentences; whether the server should also *generate* word forms. For objective 5,
   confirm the attested-only policy and that uneven coverage across source languages is expected and acceptable.
   Single-word analysis is the right v1 — say so and defend it.
2. **Fix the canonical output.** Agree on the shape of a single word analysis (the "word analysis object").
   Use the schema in `assets/word_analysis_schema.json` as the starting contract. Everything downstream —
   tools, sources, evals — serves this object.
3. **Catalog the grounding sources.** Map each field of the output object to at least one authentic source
   that can fill it, and sort each source into **anchor** vs **evolving** (see Phase 1). Read
   `references/sources.md` for the vetted catalog and which field each one grounds.
4. **Draft the tool surface.** Decide the MCP tools and their boundaries. Read `references/tool-design.md`
   for a proposed surface and input/output schemas.
5. **Take a stack position.** Recommend a language/transport with reasons (see "Stack decision" below), and
   include the self-enriching knowledge layer in the architecture sketch.
6. **Write the blueprint.** Fill in `assets/planning-blueprint-template.md` and save it as the project's
   planning doc. Walk the user through it and get sign-off before Phase 1.

Deliverable: a completed planning blueprint (`THAMIZH-MCP-blueprint.md`) saved to the project folder.

---

## Phase 1 — Lock the grounding sources

Goal: turn the catalog into concrete, reachable integrations.

For each source, record in the blueprint: what field(s) it grounds, how you reach it (local library,
downloadable data, FST binary, queried web source), its licence, and its failure mode (what to return when it
has no entry for the word). Then sort every source into one of **two tiers**, because they are maintained
very differently:

- **Anchors** — stable, authoritative, version-pinned. Tholkappiyam rules (Nannūl as fallback), the Madras
  University Tamil Lexicon, the ThamizhiMorph FST, and official கலைச்சொல் (terminology) glossaries. These are
  the ground truth you cross-check against. Pin their versions; reproducibility is part of authenticity.
- **Evolving sources** — community-contributed, internet-fed, growing. Tamil Wiktionary, Tamil
  Wikisource/Wikipedia, loanword/glossary datasets, தனித்தமிழ் equivalent lists. The server pulls from these
  *at query time* to fill coverage the anchors miss, then caches and accumulates the result so it gets broader
  over time. For these, pin the **retrieval date + provenance** of each fact instead of a version.

This two-tier split is what lets the tool grow without anyone hand-maintaining a dictionary (see the
self-enriching principle). `references/sources.md` flags tier, licence, and access for each.

A good v1 grounding stack, mapped to the five output concerns:

- **Origin (native vs borrowed):** Thamizhi Word Validator + a loanword/etymology dataset, cross-checked
  against lexicon etymology notes. Classify into Tholkappiyam's four word-origin classes
  (இயற்சொல் / திரிசொல் / திசைச்சொல் / வடசொல்) — see `references/tamil-grammar.md`.
- **Root + meaning:** ThamizhiMorph (lemma, rule-based — no per-word upkeep) + Madras Tamil Lexicon / Tamil
  Wiktionary (gloss, enriched from the evolving tier).
- **Formation:** ThamizhiMorph FST analysis (handles Sandhi) decoded into பகுபத உறுப்புகள்
  (பகுதி, விகுதி, இடைநிலை, சாரியை, சந்தி, விகாரம்).
- **Grammar:** ThamizhiMorph POS + case tag, explained through Tholkappiyam's rules (Nannūl fallback).
- **Native equivalent:** triggered only when origin ≠ native. Look up attested equivalents in
  Indic-To-Pure-Tamil (Sanskrit/Indic), official கலைச்சொல் / Tamil Virtual Academy terminology, Tamil
  Wiktionary, and தனித்தமிழ் lists — return ranked candidates with source + register; explicit gap when none.

---

## Phase 2 — Design the MCP tool surface

Goal: a finalized tool list with schemas. Read `references/tool-design.md`, then adapt it to the sources you
actually locked in Phase 1. Favor comprehensive coverage (one focused tool per concern) plus one composed
`analyze_word` workflow tool that returns the whole word analysis object, because the agent will most often
want everything about a word at once. The native-equivalent tool runs conditionally (only when the word is
non-native). Include the enrichment path (cache lookup → anchors → evolving sources → write back) and an
explicit refresh/enrich tool. Give every tool an actionable error path: when a source can't ground a field,
the tool says so (with which source was missing) rather than letting the model invent an answer.

---

## Phase 3 — Implement

Goal: a running server. Now read the **`mcp-builder`** skill's `SKILL.md` and its language-specific reference
(`reference/python_mcp_server.md` or `reference/node_mcp_server.md`) for the build mechanics, and follow its
Phase 2. This skill's `references/tool-design.md` tells you *what* the tools do; `mcp-builder` tells you
*how* to register them, define schemas, and wire transport.

Wrap each grounding source behind a small adapter with a uniform interface (input: a normalized Tamil word;
output: the fields it can fill + its own provenance + tier). Keep the linguistic logic (decoding FST tags into
பகுபத உறுப்பு, mapping case tags to வேற்றுமை names) in one well-tested module — every test run that
re-derives this is wasted work, so it belongs in the codebase, not the prompt.

Add a **knowledge store + enrichment layer** between the adapters and the tools: a local cache (e.g. SQLite)
keyed by normalized word that records every resolved field with its source, tier, and retrieval date. On a
cache miss, query the **anchors first**, then the **evolving** internet sources; merge, tag provenance, and
write the result back so the store enriches itself with use. Expose a refresh/enrich path so thin or stale
entries can be re-pulled. Rule-based morphology stays stateless (the FST needs no cache); the cache exists for
the lexical / etymology / meaning / native-equivalent layers, which is exactly where coverage must grow.

**Keep the server non-blocking.** FastMCP tool handlers run on a single async event loop, but the heavy work
here is blocking: `flookup`/foma is a subprocess call, and the evolving-tier lookups (Tamil Wiktionary,
datasets) are network I/O. Calling either directly inside a handler lets one slow lexicon fetch stall every
other in-flight request. Push blocking work off the loop — wrap subprocess and synchronous-library calls in
`anyio.to_thread.run_sync` (or `loop.run_in_executor`), and use an async HTTP client (`httpx.AsyncClient`)
for the evolving pulls. Bound the concurrency (a small thread pool / semaphore) and put a **timeout on every
external call**, returning an honest gap when a source times out rather than hanging the request. The FST is
stateless so it parallelises freely; serialize only the cache writes (SQLite is single-writer). This is the
main reason Python/FastMCP needs deliberate concurrency handling — don't skip it.

For native-equivalent suggestion specifically, the adapter must return candidates **with their attestation
source**; the merge logic drops any candidate that has no source, so the LLM can never promote a self-invented
coinage to a suggestion.

---

## Phase 4 — Evaluate

Goal: prove an LLM using the server gives authentic answers. Use `mcp-builder`'s evaluation guide. Build the
eval set from real words chosen to exercise each concern: a clearly native word (e.g. மரம்), an inflected
form needing sandhi-aware splitting (e.g. மரத்தில்), a Sanskrit loanword with an attested equivalent
(புத்தகம் → நூல்), an English loanword with an attested equivalent (கம்ப்யூட்டர் → கணினி), a loanword from a
thinner-coverage language (e.g. Portuguese ஜன்னல் → சாளரம்), and a borrowing with **no** attested native
equivalent (to test the honest gap). For each, hand-verify the expected origin, root, meaning, formation,
grammar, and equivalent against the sources before locking the answer. Also test the **honesty + enrichment**
behaviours directly: a word missing from the anchors should trigger an evolving-source pull (cached,
provenance-tagged); a word missing everywhere — and an equivalent with no attestation — must return an
explicit gap, never a fabricated analysis or invented coinage.

> Eval note for this project: treat the **eval-1 with-skill** blueprint as the reference standard for a good
> Phase 0 output. Run baselines in isolation from the project folder so they can't read these skill files.
>
> Phase 4 here covers **server regression** evals only. The *product* metric — morphological lift on
> ILAKKANAM-style questions (bare LLM vs LLM+server) — is owned by the `thamizh-eval` skill; keep the two
> layers separate and never publish fixture words into datasets.

---

## Stack decision

**Decision: Python core (FastMCP) is the committed default for v1.** Saran confirmed Python fits the project
best, and the entire Tamil-NLP ecosystem this project must ground against is Python or native-binary, so there
is no real ambiguity to keep open —

- **ThamizhiMorph** is a foma finite-state transducer queried via `flookup` (callable from any language, but
  the surrounding tooling, ThamizhiPOSt, and ThamizhiLIP are Python).
- **open-tamil**, **ThamizhiLIP**, **Stanza**, and most analysers/validators ship as Python packages.

The analysis logic lives in Python, and the MCP server sits in the **same process via FastMCP** — direct
library calls, one language, no inter-process boundary.

**Rejected alternative (documented, not chosen):** a TypeScript MCP server calling a separate Python analysis
service. It adds an IPC boundary for no linguistic benefit at this stage. Reopen this choice **only** if a
hard external constraint appears — e.g. the server must be embedded in an existing Node/TS codebase, or a
deployment target mandates the TS MCP SDK. Absent such a trigger, treat the stack as settled and do not
re-litigate it.

Whichever shape, include the **self-enriching knowledge store** (cache + enrichment loop) as a first-class
component, not an afterthought.

---

## Grounding & authenticity principles

These are the rules that make the product trustworthy. Carry them into the server's tool descriptions and
system prompt, not just the build process.

- **Tholkappiyam first, Nannūl as fallback (grammar).** தொல்காப்பியம் is the golden authority for Tamil
  grammar — cite it first for every grammar claim it codifies: the word classes (Collatikāram —
  பெயர்/வினை/இடை/உரியியல்), the four origin classes (இயற்சொல்/திரிசொல்/திசைச்சொல்/வடசொல்), the eight வேற்றுமை
  (வேற்றுமையியல்), and புணர்ச்சி/sandhi (எழுத்ததிகாரம், புணரியல்). Use **நன்னூல்** only where Tholkappiyam does
  not enumerate the point — chiefly the formal six-part பகுபதம் decomposition — and always say which authority
  you used. This rule governs objectives 1, 3, 4; it does **not** govern objective 5.
- **Self-enriching, not hand-maintained.** Do not plan to build and babysit a giant static word list — that
  upkeep becomes a nightmare and is the wrong shape for this project. Two moves avoid it: (1) get word *forms*
  from rule-based morphology (ThamizhiMorph's FST generates millions of inflections from paradigms — no
  per-word upkeep); (2) get *meaning, etymology, coverage, and native equivalents* by pulling from evolving,
  community-contributed internet Tamil sources at query time, then caching and accumulating into a local
  knowledge store that grows and enriches itself. Every enriched entry carries provenance and is cross-checked
  against the anchors, so growth never means drift into unsourced guesses.
- **Suggest only attested native equivalents (objective 5).** The equivalent-suggestion feature is the
  highest hallucination risk in the server, because a fluent model will happily coin a plausible-but-fake
  Tamil word. The rule: recommend an equivalent **only** when an authority (a கலைச்சொல்/terminology glossary,
  a தனித்தமிழ் lexicon, an attested dictionary/Wiktionary entry, Indic-To-Pure-Tamil) attests it. Return
  ranked candidates with their source and register (technical / literary / everyday); when none is attested,
  return an explicit "no attested equivalent" — do not invent one. Its authority is the கலைச்சொல்/தனித்தமிழ்
  tradition, not Tholkappiyam. Equivalents are often debated and one-to-many — surface the options, don't
  adjudicate.
- **Provenance on every claim.** Each filled field carries which source produced it, its tier (anchor /
  evolving), and when it was retrieved. The agent should be able to say "root per ThamizhiMorph; meaning per
  Madras Tamil Lexicon (anchor); origin per Tholkappiyam's வடசொல் rule; native equivalent கணினி per the Tamil
  Virtual Academy கலைச்சொல், pulled 2026-06-28."
- **Separate analysis from disambiguation.** Tamil is morphologically rich; one surface form often has
  several valid analyses. Return all of them with their provenance rather than silently picking one.
- **Name uncertainty.** Origin classification (and native-equivalent choice) is genuinely contested for some
  words. Report the disagreement and the evidence; don't manufacture certainty.
- **Don't let the LLM be the source.** If no grounding source covers a field — not the anchors, not an
  evolving pull — the correct output is an honest gap, not a fluent guess. This is the single most important
  behaviour to test for in Phase 4.

---

## Reference files

- `references/sources.md` — the authentic-source catalog, each tagged anchor vs evolving and mapped to the
  output field it grounds, with access + licence; includes the evolving/self-enriching internet sources and
  the native-equivalent (கலைச்சொல்/தனித்தமிழ்) sources.
- `references/tamil-grammar.md` — a working primer on சொல் இலக்கணம் with Tholkappiyam-first citations: word
  classes, the four origin classes, the eight வேற்றுமை, பகுபத உறுப்பிலக்கணம், and a note on native equivalents.
- `references/tool-design.md` — proposed MCP tool surface with input/output schemas, including the
  native-equivalent, enrichment, and refresh tools. Opens with the **Thamizhi component→tool map** fixing
  which existing tool powers which MCP tool ("wrap, don't rebuild").
- `references/research-grounding.md` — digests of the two anchor papers (ThamizhiMorph 2021; ILAKKANAM
  arXiv 2511.12387) plus the token-explosion/de-agglutination argument, and what each changes in the build.
- **`DECISIONS.md` — at the REPO ROOT, not in `references/`** (moved 2026-08-10). Append-only log of
  resolved decisions with rationale + date. Read first when a past choice is in question; append a
  superseding entry rather than editing history. It sits at the root deliberately: it is a *living
  program record* — the most-edited file in the repo — cited from README, DESIGN, Glossary and the
  code repo, not skill teaching material. It is therefore **not bundled into the packaged skill**; a
  frozen snapshot of a decision log would be wrong by the next session. Read it from the repo.
- `references/IMPROVEMENT-LOOP.md` — the continuous-improvement playbook: routing rule for where each new
  insight goes, per-session triage, skill versioning.
- `assets/word_analysis_schema.json` — canonical JSON contract for one word analysis.
- `assets/planning-blueprint-template.md` — fill this in for the Phase 0 deliverable.
