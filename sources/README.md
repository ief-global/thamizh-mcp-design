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
│   ├── C021-eluthu/        எழுத்து — C0211 மொழி அமைப்பு · C0212 எழுத்தின் பிறப்பும் பத இலக்கணமும்
│   │                                C0213 புணர்ச்சி-1 · C0214 புணர்ச்சி-2
│   ├── A021-sol/           சொல்   — A0211 பெயர்ச்சொல் · A0212 வினைச்சொல்
│   │                                A0213 இடைச்சொல், உரிச்சொல் · A0214 சொற்றொடரியல்
│   └── CITATION.md         how to cite a TVA lesson inside a rule table
└── classical/              future: pinned digitised Tholkappiyam / Nannūl editions (D-011)
```

⚠️ The எழுத்து course is **C021**, not A011. This file previously said `A011-eluthu` / `A0111`–`A0114`;
those ids do not exist. Corrected 2026-08-02 against the actual TVA material.

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

**Where the rules actually live.** The lesson that governs a rule is not always the one the topic name
suggests — check before extracting:

| rule table | authority நூற்பா | extracted from |
|---|---|---|
| `idainilai.json` | 142, 143, 144 | A0212 §6.2 **and** C0212 §6.2 (two independent attestations) |
| `vikuthi.json` | **140** (closed 37→40 inventory), 336 | **C0212 §6.1**, A0212 §3.2.1 |
| `sariyai.json` | 133, **243**, **244** | **C0214 §4.2**, C0212 §5.3.4 |
| `verrumai_urubu.json` | 240–242, 291–303, 315 | A0211 §§5–6, C0214 §4.1 |
| `vikaram.json` | 153, **154**, 157 | **C0213 §1.6**, C0212 §5.3.6 |

**C0212 (எழுத்தின் பிறப்பும் பத இலக்கணமும்) is the பதவியல் lesson** — it, not the சொல் course, is the
authority for the six பகுபத உறுப்பு (நூற்பா 133) and for the விகுதி / இடைநிலை inventories. விகுதி and
சாரியை are *not* in A021-sol at all. C0212 also re-quotes நூற்பா 142/143 independently, which
re-confirms the இடைநிலை fix from a second lesson.

First table built this way: `data/grammar/idainilai.json` (tense markers), after the
வருகிறான் → வா + **கிறு** + ஆன் correction on 2026-08-02. Four more followed the same day
(விகுதி, சாரியை, வேற்றுமை உருபு, விகாரம்) — see `DECODER-AUDIT-D014.md`.
