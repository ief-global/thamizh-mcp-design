# Draft letter — Digital South Asia Library, University of Chicago

**Status:** DRAFT for Saran's review and sending. Not yet sent.
**Revised 2026-08-19** — the project description is now a link, since
`thamizh-ai.org/sources/madras-lexicon` sets out our reading of the licence in public. The diligence
sections stay in full: they are the substance of the request, not context.
**To:** Digital South Asia Library (DSAL), University of Chicago — project contact for the
Tamil Lexicon. (Find the current address on `dsal.uchicago.edu`; a general DSAL / Southern Asia
collections contact is fine. Do not guess at an individual's name.)
**From:** Saran Saravanan, on behalf of the International Educational Foundation (IEF)
**Two asks:** (1) a factual question — does the edition carry machine-readable etymology fields?
(2) permission for rate-limited programmatic query, storing derived claims and citations only.

> **Notes for Saran before sending**
> - **Send the TVA letter first.** It is the easier yes and targets our actual licence gap. This one
>   is narrower and its value is uncertain until they answer question 1.
> - **Question 1 is the point.** We cannot verify whether DSAL's edition carries source-language
>   tags, because those pages are `robots.txt`-disallowed and we have not requested them. The other
>   digitisation of the same lexicon (Cologne) turned out to be glosses only. If DSAL's edition is
>   also glosses only, permission buys us nothing and we should not spend their goodwill on it.
>   Asking both questions in one email costs one round trip instead of two.
> - The letter states plainly that we noticed the robots.txt rule and did not scrape. That is true
>   and worth saying — it is the difference between a request and a fait accompli.

---

Dear DSAL colleagues,

I am writing on behalf of the **International Educational Foundation**, a non-profit, about the
**Tamil Lexicon** (University of Madras, 1924–1936) hosted at
`dsal.uchicago.edu/dictionaries/tamil-lex/`. I have one factual question and one request, and I would
be glad of an answer to the first even if the second is refused.

## What we are building, briefly

**Thamizh MCP** is a free, open-source tool that analyses a single Tamil word and returns its grammar
from cited sources: origin, root, meaning and word formation. Its purpose is to stop AI assistants
answering Tamil grammar questions from memory — they currently do, confidently and often wrongly —
and make them cite Tamil scholarship instead. Every claim names the source that grounds it, and where
no source can ground a field it returns an explicit gap rather than a guess.

The design is public at **`thamizh-ai.org`**. Our reading of your licence, and the reason we have not
acted on it, is set out at **`thamizh-ai.org/sources/madras-lexicon`** rather than only in this
letter. The code is Apache-2.0; the service is free; there is no commercial product.

## First, a factual question

**Does the DSAL Tamil Lexicon edition carry the entries' etymological and source-language
information in a structured, machine-readable field?**

I ask because we have not been able to determine this, and the answer decides whether the request
below is worth your time at all. The print lexicon does carry etymological notes in its bracketed
matter. But the other major digitisation of the same work — the Cologne Online Tamil Lexicon — turns
out to contain headwords and English glosses only: of its 117,773 entries, 70 mention "Skt" and all
of those are incidental prose rather than a per-entry tag. We also assessed the archive.org scans,
including the Tamil Virtual Academy's; there the Tamil OCR is serviceable but the bracketed
etymological portions do not survive OCR at all.

If DSAL's edition is likewise glosses only, then it cannot serve the purpose we have in mind, and I
would rather learn that from one email than pursue a permission we do not need.

## Second, a request — and what we have deliberately not done

**We have made no automated requests to your site.** Your `robots.txt` disallows `/cgi-bin/`, and
`/cgi-bin/app/tamil-lex_query.py` is the only query endpoint, so we stopped and wrote to you instead.

If the etymological data does exist, we would like permission for **rate-limited programmatic lookup**
of individual headwords, under constraints we would hold to whether or not you require them:

- **No bulk copy and no local corpus.** Query-by-word only, never a crawl of the dictionary.
- **We would store the derived fact and a citation URL — never your entry text.** For example, that
  a given Tamil word is recorded as a borrowing from a particular language, plus a link back to your
  entry. A reader who wants the wording follows the citation to you.
- **Courteous access**: a descriptive User-Agent identifying the project and a contact address,
  conservative rate limiting, and a local cache so any given word is fetched once.
- **Excluded from any published dataset.** Our project does publish derived Tamil datasets, and
  material from your edition would be filtered out of them. Our per-source licence classification
  already makes this a filter rather than a promise.
- **Off by default.** The relevant component would ship disabled, so no downstream user of our
  open-source code inherits an obligation to you without choosing it.

## Why we are asking rather than assuming

Your edition is published under **CC BY-NC-ND 2.0**, with copyright held by the University of Madras.
We read that carefully and concluded, cautiously, that it does not permit what we want:

- the **NoDerivatives** term appears to preclude parsing entries into a restructured store;
- the **NonCommercial** term sits badly with an Apache-2.0 codebase that anyone may run, including
  commercially — bundling NC-licensed material into it would push a restriction onto downstream users
  who never agreed to it.

We are aware that the underlying 1924–1936 work is likely out of copyright, and that a
public-domain scan is therefore usable without anyone's permission. That is not what we are asking
for. What has scholarly value here is precisely your **structured digital edition** — the work of
digitisation, correction and organisation that DSAL and its contributors performed. That is yours,
and we would rather ask than route around it.

If a broader arrangement is easier for you than a query permission — for instance sharing a derived
extract of headwords with their source-language tags, under terms of your choosing — we would welcome
that and cite it exactly as you specify.

I am happy to provide any further technical detail, to submit to whatever review you would find
appropriate, or to accept narrower terms than those proposed. And if the answer to the first question
is that the etymological data is not machine-readable, simply telling me so would be a real help.

With thanks for the Digital South Asia Library, which has been a considerable service to Tamil
scholarship,

**Saran Saravanan**
President, International Educational Foundation
`thamizh@ief-global.org`
Site: `thamizh-ai.org` · Code: `github.com/ief-global/thamizh-mcp`

---

## Appendix — what we determined, for the record

| Finding | Detail |
|---|---|
| Licence on the DSAL Tamil Lexicon | CC BY-NC-ND 2.0, © University of Madras; data refreshed Sep 2023 |
| Query endpoint | `/cgi-bin/app/tamil-lex_query.py` — the search form's own `ACTION` |
| `robots.txt` | `User-agent: *` → `Disallow: /cgi-bin/`. **No automated requests made.** |
| Cologne digitisation of the same work | 117,773 entries, CC BY-NC-SA 3.0, bulk-downloadable, **glosses only — no etymology** |
| archive.org DLI scan (1939) | 1.25 GB of page images, **zero Tamil codepoints** in its OCR layer |
| TVA archive.org scans | real Tamil OCR (43–47%), but **zero etymology markers survive** across 1.3 M characters |

Recorded in the project's decision log as D-016 (licence finding) and D-017, and published at
`thamizh-ai.org/sources/madras-lexicon` — including the sentence that we noticed the `robots.txt`
rule and stopped. We would rather state that publicly than only in a letter asking you for
something.
