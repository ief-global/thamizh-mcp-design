# Pinned classical editions (D-011)

The **primary** grammatical authority for this project is **Tholkappiyam**. Nannūl is the fallback and
expansion. See `DESIGN.md` §4a for the per-topic priority table and the citation format.

## Tholkappiyam — pinned edition: Project Madurai

Pinned 2026-08-02. Project Madurai is an open, volunteer, worldwide initiative that prepares electronic
texts of Tamil literary works and distributes them free. The community has put substantial effort into
validating these texts and removing transcription errors, which is why it is the chosen gold source.

| அதிகாரம் | URL |
|---|---|
| எழுத்ததிகாரம் | https://tamilnation.org/literature/grammar/mp100a |
| சொல்லதிகாரம் | https://tamilnation.org/literature/grammar/mp100b |
| பொருளதிகாரம் | https://tamilnation.org/literature/grammar/mp100c |

**Required attribution.** Reproduce this header wherever the text or its derived citations are
redistributed:

```
© Project Madurai 1999-2001

Project Madurai is an open, voluntary, worldwide initiative devoted to preparation
of electronic texts of tamil literary works and to distribute them free on the
Internet. Details of Project Madurai are available at the website
http://www.projectmadurai.org
You are welcome to freely distribute this file, provided this header page is kept
intact.
```

Edition credits recorded in the source: *Etext Preparation & PDF version:* Dr. K. Kalyanasundaram,
Lausanne, Switzerland. *Proof-reading & Web version:* Mr. N. D. Logasundaram, Chennai, Tamilnadu.

We cite verses and credit Project Madurai; we do not redistribute the full text from the public repo.
Where the project does surface Project Madurai material, the header above travels with it.

## Verse numbering — READ THIS BEFORE CITING

**நூற்பா numbers restart at 1 in every இயல்.** They collide across அதிகாரம் *and* across இயல் within a
single அதிகாரம். A bare number is ambiguous and unusable. Always qualify:

```
தொல்காப்பியம், எழுத்ததிகாரம், புணரியல், நூற்பா 7
தொல்காப்பியம், சொல்லதிகாரம், வேற்றுமையியல், நூற்பா 3
```

Verified இயல் structure and verse counts:

| எழுத்ததிகாரம் | | சொல்லதிகாரம் | |
|---|---|---|---|
| நூல் மரபு | 1–33 | கிளவியாக்கம் | 1–62 |
| மொழி மரபு | 1–49 | வேற்றுமையியல் | 1–22 |
| பிறப்பியல் | 1–21 | வேற்றுமைமயங்கியல் | 1–35 |
| **புணரியல்** | **1–40** | விளிமரபு | 1–37 |
| தொகைமரபு | 1–30 | பெயரியல் | 1–43 |
| உருபியல் | 1–30 | வினையியல் | 1–49 |
| உயிர்மயங்கியல் | 1–93 | இடையியல் | 1–63 |
| புள்ளிமயங்கியல் | 1–110 | உரியியல் | 1–98 |
| குற்றியலுகரப்புணரியல் | 1–77 | எச்சவியல் | 1–67 |

**Nannūl numbering is continuous** across the whole work, so a bare நூற்பா number is unambiguous
there — `நன்னூல், நூற்பா 244`. Nannūl verses reach us through the TVA course material, which quotes
them verbatim with their numbers (`sources/tva/`), so no separate Nannūl edition is pinned yet.

## Verses used by the shipped rule tables

Extracted verbatim from the pinned edition on 2026-08-02.

**தொல்காப்பியம், சொல்லதிகாரம், வேற்றுமையியல்** → `data/grammar/verrumai_urubu.json`

| நூற்பா | text |
|---|---|
| 1 | வேற்றுமைதாமே ஏழ் என மொழிப. |
| 2 | விளி கொள்வதன்கண் விளியடு எட்டே. |
| 3 | அவைதாம், பெயர் ஐ ஒடு கு இன் அது கண் விளி என்னும் ஈற்ற. |
| 4 | அவற்றுள், எழுவாய் வேற்றுமை பெயர் தோன்று நிலையே. |
| 10 | இரண்டாகுவதே, ஐ எனப் பெயரிய வேற்றுமைக் கிளவி … |
| 12 | மூன்றாகுவதே, ஒடு எனப் பெயரிய வேற்றுமைக் கிளவி வினைமுதல் கருவி அனை முதற்று அதுவே. |
| 14 | நான்காகுவதே, கு எனப் பெயரிய வேற்றுமைக் கிளவி எப் பொருள் ஆயினும் கொள்ளும் அதுவே. |
| 16 | ஐந்தாகுவதே, இன் எனப் பெயரிய வேற்றுமைக் கிளவி இதனின் இற்று இது என்னும் அதுவே. |
| 18 | ஆறாகுவதே, அது எனப் பெரிய வேற்றுமைக் கிளவி … கிழமைத்து அதுவே. |
| 20 | ஏழாகுவதே, கண் எனப் பெயரிய வேற்றுமை கிளவி வினை செய் இடத்தின் நிலத்தின் காலத்தின் … |
| 21 | கண் கால் புறம் அகம் உள் உழை கீழ் மேல் பின் சார் அயல் புடை தேவகை எனாஅ முன் இடை கடை தலை வலம் இடம் எனாஅ அன்ன பிறவும் அதன் பால என்மனார். |

**தொல்காப்பியம், எழுத்ததிகாரம், புணரியல்** → `data/grammar/vikaram.json`, `sariyai.json`

| நூற்பா | text |
|---|---|
| 6 | … மூன்றே திரிபு இடன் ஒன்றே இயல்பு என ஆங்கு அந் நான்கே மொழி புணர் இயல்பே. |
| 7 | அவைதாம், மெய் பிறிது ஆதல் மிகுதல் குன்றல் என்று இவ் என மொழிப திரியும் ஆறே. |
| 10 | வேற்றுமை குறித்த புணர்மொழி நிலையும் வேற்றுமை அல்வழிப் புணர்மொழி நிலையும் எழுத்தே சாரியை ஆயிரு பண்பின் ஒழுக்கல் வலிய புணரும் காலை. |
| 11 | ஐ ஒடு கு இன் அது கண் என்னும் அவ் ஆறு என்ப வேற்றுமை உருபே. |
| 12 | வல்லெழுத்து முதலிய வேற்றுமை உருபிற்கு ஒல்வழி ஒற்று இடை மிகுதல் வேண்டும். |

### Two findings worth carrying forward

1. **Tholkappiyam names the three விகாரம் first.** புணரியல் 7 — `மெய் பிறிது ஆதல் மிகுதல் குன்றல்` —
   is the primary; Nannūl 154's `தோன்றல், திரிதல், கெடுதல்` is the later restatement. Map
   பிறிது ஆதல்→திரிதல், மிகுதல்→தோன்றல், குன்றல்→கெடுதல்.
2. **The authorities genuinely differ on the third case.** Tholkappiyam gives **ஒடு** only
   (வேற்றுமையியல் 12); Nannūl 297 gives ஆல், ஆன், ஒடு, ஓடு. Record the difference; do not collapse it.

## Still open

- Mirror the Project Madurai text into `data/` as a version-locked artifact (currently URL-referenced).
- No separate Nannūl edition pinned — Nannūl arrives via TVA quotation. Pin one if a claim ever needs a
  நூற்பா that TVA does not print (e.g. the நான்காம் வேற்றுமை நூற்பா, absent from A0211).
