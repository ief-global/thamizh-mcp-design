# Draft letter — Tamil Virtual Academy

**Status:** DRAFT for Saran's review and sending. Not yet sent.
**To:** Tamil Virtual Academy (Govt. of Tamil Nadu) — Director / Content & Licensing
**From:** Saran Saravanan, on behalf of the International Educational Foundation (IEF)
**Two asks:** (1) a written licence statement covering the TVA archive.org collection;
(2) the கலைச்சொல் glossaries in machine-readable form.

> **Notes for Saran before sending**
> - The body is in English because it contains licensing language where precision matters. Given
>   you are a TVA alumnus writing to a Tamil institution, **a Tamil version would land better** —
>   say the word and I will draft one for you to correct. The salutation and closing are already in
>   Tamil.
> - **The Wikimedia precedent is the strongest lever in this letter** (its own section below).
>   Verified 2026-08-08: TVA material is already on Tamil Wikisource under **CC0 1.0**, with the
>   collaboration documented at `ta.wikisource.org/s/4kx`. Asking them to extend terms they have
>   already granted elsewhere is a much easier request than asking for a new policy.
> - **Ask 2 is the one that matters most to the project.** It would let us retire an unlicensed
>   community word-list — the only genuine licence gap we currently ship — and replace it with a
>   government glossary. Ask 1 is cheap for them and unblocks the course books too.
> - Everything factual below is verifiable in the public repos. Please correct anything about your
>   own standing or your relationship with the institution before sending.

---

வணக்கம்,

I am writing both as an alumnus of the Tamil Virtual Academy — I completed my B.A. in Tamilology
through TVA — and on behalf of the **International Educational Foundation (IEF)**, a non-profit,
about a Tamil language-technology project where TVA's materials would make a decisive difference.

## What we are building

**Thamizh MCP** is a free, open-source server that analyses a single Tamil word and returns its
grammar: its origin (இயற்சொல் / வடசொல் / loanword), its root and meaning, its formation
(பகுபத உறுப்பு, புணர்ச்சி), and its grammatical categories. It is designed so that AI assistants stop
guessing about Tamil grammar and instead answer from cited Tamil sources.

Two design rules govern it, and they are why I am writing to you rather than simply scraping what is
available:

1. **Tholkappiyam-first.** Every grammatical claim cites its authority — Tholkappiyam before Nannūl —
   down to the நூற்பா number, from version-pinned editions.
2. **Every claim carries its source.** The server never returns an unsourced answer. Where no source
   can ground a field, it returns an explicit gap rather than a guess.

The code is Apache-2.0 and public (`github.com/ief-global/thamizh-mcp`), the service is free to use,
and there is no commercial product built on it.

## Why I am writing

Our origin classifier needs a list of **வடசொல்** and their தனித்தமிழ் equivalents. We currently use a
community-compiled aggregation of four purist word-lists. It works, but it has two problems we are
not willing to live with in a tool meant to be authoritative:

- it has **no stated licence**, and its own upstream sources' terms are unknown;
- it has been **unmaintained since 2020**.

Anyone who inspects our sources will find that, and they would be right to think less of the tool for
it. We would much rather cite an authenticated glossary from the Government of Tamil Nadu.

## Two requests

**1. A written licence or permission statement for the TVA collection on archive.org.**

The collection at `archive.org/details/TamilVirtualAcademy` is a remarkable public service. However,
the individual items carry **no rights or licence metadata** — we checked. Because our repository is
public, we treat an absent licence as "not cleared", so we currently cite TVA lessons as sources but
keep the files themselves out of our repository and redistribute nothing.

A short written statement of the terms — even simply confirming that the material may be used and
cited for non-commercial educational purposes, and whether derived data may be redistributed with
attribution — would let us represent TVA's position accurately instead of conservatively guessing at
it.

**2. The கலைச்சொல் glossaries in machine-readable form.**

If TVA's technical-terminology glossaries could be shared as data — CSV, XML, JSON, a database
export, anything structured rather than page scans — they would become the authenticated backbone of
this part of the tool. Specifically we need the pairing of a borrowed or Sanskrit-derived term with
its accepted Tamil equivalent.

We have found that scanned images do not serve this purpose: we assessed the archive.org scans of the
Madras University Tamil Lexicon, including those in TVA's own collection, and while the Tamil OCR is
far better than other scans available, the bracketed etymological and English portions do not survive
OCR at all. Structured data avoids that problem entirely.

## A precedent you have already set

I should say that I am not asking TVA to do something new in kind. The Global Tamil Wikimedia
Community's collaboration with TVA has already placed TVA material on Tamil Wikisource under the
**CC0 1.0 Universal Public Domain Dedication** — the works carry the note *"This book is uploaded as
part of the collaboration between Global Tamil Wikimedia Community and Tamil Virtual Academy"*, and
the collaboration itself is documented at `ta.wikisource.org/s/4kx`.

That collaboration is, I think, exactly the right instinct: material released freely so that others
can build on it. What I am asking for is the same instinct applied to the கலைச்சொல் glossaries as
structured data. If the terms extended to the Wikisource collaboration could simply be extended here,
that would settle the question entirely — and we would be glad to accept CC0, CC BY, or any narrower
terms you prefer.

I mention it also because the position is currently uneven: some TVA-related works on Wikisource carry
that CC0 dedication and others carry no licence statement at all, so a good-faith user cannot tell
which is which. A single statement of terms for the collection would resolve that for everyone, not
only for us.

## What we would do with it

- **Attribution on every claim.** Each answer names the source that grounds it, so a TVA glossary
  entry would be visible as such to every user, with the glossary and lesson cited.
- **Per-source licensing, never relicensed.** Our product deliberately mixes licences and classifies
  them per record. Apache-2.0 covers our own code and rule tables only; third-party material keeps
  its own terms and is documented in a public `LICENSING.md`. We would honour whatever terms you set,
  including "cite but do not redistribute".
- **Corrections returned.** Where our users or reviewers identify an error, we would be glad to
  report it back rather than silently patch our copy.
- **No commercial use** without returning to you first.

## Why this matters beyond our project

Tamil is under-represented in the language models people now use daily, and those models answer Tamil
grammar questions confidently and often wrongly. The most effective correction is not more training
data but authoritative sources the models must cite. TVA's materials, made machine-readable, would be
doing exactly that — and every tool built afterwards would be citing TVA rather than guessing.

I am happy to travel, present the work, or answer any technical question. If it is easier, I can also
send this in Tamil.

மிக்க நன்றி,

**Saran Saravanan**
President, International Educational Foundation
`saravanan3@duck.com`
Project: `github.com/ief-global/thamizh-mcp`

---

## Appendix — facts a reviewer may want to check

| Claim | Where to verify |
|---|---|
| Apache-2.0, public repository | `github.com/ief-global/thamizh-mcp` |
| Per-source licence classification | `LICENSING.md` in that repository |
| Sources and version pins | `data/PINS.md` |
| Tholkappiyam-first citation rule, with நூற்பா numbers | `data/grammar/*.json`, `data/classical/` |
| The unlicensed list we want to replace | `data/equivalents/sanskrit-to-pure-tamil/`, and the S2PT section of `LICENSING.md` |
| Design and decision record | `github.com/ief-global/thamizh-mcp-design` |
