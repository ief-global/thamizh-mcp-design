# Source materials

Reference documents used to build (and audit) the grammar rule tables that ship in the **public**
`thamizh-mcp` repo. **These documents stay in this private repo.** Only the *derived, cited rule
tables* ship publicly.

## Why the split

The rule tables encode **facts about Tamil grammar** — the inventory of இடைநிலை, the eight வேற்றுமை,
the six பகுபத உறுப்பு. Facts aren't copyrightable, and citing the source is scholarship. Redistributing
complete third-party textbooks is a different act with a different licence question, so we don't.

## Layout

```
sources/
├── tva/                    Tamil Virtual Academy (Govt. of Tamil Nadu, degree-level accredited)
│   ├── A011-eluthu/        எழுத்து — A0111 மொழி அமைப்பு · A0112 எழுத்தின் பிறப்பும் பத இலக்கணமும்
│   │                                A0113 புணர்ச்சி-1 · A0114 புணர்ச்சி-2
│   ├── A021-sol/           சொல்   — A0211 பெயர்ச்சொல் · A0212 வினைச்சொல்
│   │                                A0213 இடைச்சொல், உரிச்சொல் · A0214 சொற்றொடரியல்
│   └── CITATION.md         how to cite a TVA lesson inside a rule table
└── classical/              future: pinned digitised Tholkappiyam / Nannūl editions (D-011)
```

## Formats — prefer ePUB

- **ePUB — best.** A zip of XHTML with real Unicode text; extracts cleanly.
- **Kindle/mobi** — workable, convertible.
- **PDF — problematic.** The TVA PDFs embed **TAU-Valluvar**, a pre-Unicode font, so text extraction
  yields legacy TSCII/TAB bytes that the standard converters do not cleanly rescue. Keep the PDFs for
  human reading; use ePUB for machine extraction.
- **Website HTML** — authoritative but slow/unreliable and spread over very many pages.

## How these become code

1. Read the lesson section that defines a rule inventory (e.g. the நிகழ்கால இடைநிலை list).
2. Encode it as a cited table in the public repo under `data/grammar/*.json`, carrying `authority`,
   the TVA lesson id, `verified_by` and `verified_date`.
3. The decoder consumes the table; every claim it emits can then name its source.
4. A Tamil scholar can audit the linguistics by reading the JSON — no Python required.

First table built this way: `data/grammar/idainilai.json` (tense markers), after the
வருகிறான் → வா + **கிறு** + ஆன் correction on 2026-08-02.
