# Lexicon sources — what has been assessed

No lexicon is integrated yet. This file records what was evaluated and why it failed, so the same
1.25 GB download does not happen twice. Method for integrating any lexicon:
[INTEGRATING-A-LEXICON.md](../INTEGRATING-A-LEXICON.md). Licence findings: D-016, D-017.

## Assessed 2026-08-08 — and rejected

### archive.org DLI scan — `in.ernet.dli.2015.85194` ("Tamil Lexicon", U. Madras, 1939)

Downloaded as a 1.25 GB ePub and **deleted after assessment**. Unusable:

| | |
|---|---|
| Composition | **1,301 MB of JPEG page images** vs 1.2 MB of HTML |
| Pages | 463 — the Lexicon proper runs to **six volumes** |
| **Tamil codepoints in the whole book** | **0** |
| OCR output | garbled Latin — `UNIVERSy LIBRARY OU 172139`, `kalpu, n. KAv'dh. qalf.` |
| Rights on the item | **none stated** — no `rights`, no `licenseurl` field |

Page images with a Latin-only OCR pass. Same pre-Unicode font failure documented for the TVA PDFs in
[../README.md](../README.md). Machine lookup needs Unicode Tamil; there is none.

### TVA collection on archive.org — the full six volumes + Supplement

Better than the DLI scan: real Tamil OCR (43–47% Tamil codepoints) and substantial text layers
(Vol 1 Part 1 ≈ 2.5 MB, Vol 4 Part 1 ≈ 4.4 MB). Still cannot ground **origin**:

- **Tamil headwords** — mostly legible (அமரம், அமரர், அமரகோசம்), but with errors (`திநப்பும்` for
  `திருப்பும்`, dropped pulli), so exact headword matching is unreliable.
- **English glosses** — destroyed; OCR'd into Tamil glyphs (`க௱காக௱, ஈ. ௦4. சரசா.`).
- **Etymology markers — ZERO survive** across 1.3 M characters. No `[Skt.`, no `[Arab.`, no `<`
  derivations. The etymology sits inside the bracketed English, which is exactly what the OCR
  destroyed. This is the field we need, and it is the field that is gone.
- **Rights** — none stated on any item.

### Cologne (`sanskrit-lexicon.uni-koeln.de`, `csl-santam`)

Bulk-downloadable, CC BY-NC-SA 3.0, 117,773 Tamil entries — and **glosses only**. 70 entries mention
"Skt" and all are incidental prose ("a Skt. adverbial preposition"); zero `<` derivations, zero
bracketed language tags. Improves `meaning`, cannot ground `origin`. Note `MWScan/tamil` is the same
data, not a Sanskrit→Tamil lexicon.

### DSAL (`dsal.uchicago.edu/dictionaries/tamil-lex/`)

CC BY-NC-ND 2.0, © University of Madras (D-016) — **and `robots.txt` has `Disallow: /cgi-bin/`**,
which is the only query endpoint. We have made no automated requests. Awaiting a reply to
[../correspondence/2026-08-08-dsal-uchicago.md](../correspondence/2026-08-08-dsal-uchicago.md).

## The conclusion that matters

A 1924–39 lexicon is the **right tool for the wrong problem** right now. Measured against our 13
modern-loan gaps: 1 present in modern spelling, 3 only in older naturalised forms, 7 absent, and
**2 false friends** — பட்டன் is in there as *"learned man, scholar; brahmin priest"* (Skt *bhaṭṭa*),
NOT English "button", so naive matching would turn one honest-ish wrong into a confident one.

Its real strength is classical and literary vocabulary, and it would clear 5 of our 6 non-loan
unknowns. Worth having later; it does not close the current gap.

## Rule

⚠️ **Nothing binary goes in this folder.** `sources/**/*.{pdf,epub,mobi,djvu,zip,tar}` is gitignored
by extension — a source document is ignored by default and cleared deliberately, never the reverse.
Record findings here; keep the artefacts out of git.
