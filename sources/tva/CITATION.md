# Citing TVA material in rule tables

Tamil Virtual Academy, Government of Tamil Nadu — degree-level accredited course material.

**In a rule table** (`data/grammar/*.json`):

```json
"authority": "Nannūl — <section>; verified against Tamil Virtual Academy course
              <id> <title> (Government of Tamil Nadu, degree-level accredited material).",
"verified_by": "<who>", "verified_date": "YYYY-MM-DD"
```

**Course ids seen so far**

| id | title | governs |
|---|---|---|
| C0211 | மொழி அமைப்பு | language structure |
| C0212 | எழுத்தின் பிறப்பும் பத இலக்கணமும் | **பதவியல்** — பகுபதம்/பகாப்பதம், the six உறுப்பு (133), **விகுதி (140)**, இடைநிலை (142–145) |
| C0213 | புணர்ச்சி – 1 | புணர்ச்சிப் பாகுபாடு, **விகாரம் (153, 154, 157)**, உயிர் ஈறு, குற்றியலுகரம், எண்ணுப்பெயர் |
| C0214 | புணர்ச்சி – 2 | மெய் ஈறு, **உருபு புணர்ச்சி (240–242)**, **சாரியை (243, 244)**, வல்லினம் மிகும்/மிகா இடம் |
| A0211 | பெயர்ச்சொல் | nouns, **வேற்றுமை உருபு (291–303, 315)** |
| A0212 | வினைச்சொல் | verbs, இடைநிலை (142–144), விகுதி (336), வினையெச்சம் (343) |
| A0213 | இடைச்சொல், உரிச்சொல் | particles, qualifiers |
| A0214 | சொற்றொடரியல் | syntax |

⚠️ **The எழுத்து course is `C021`, not `A011`.** This table previously listed `A0111`–`A0114`; those ids
do not exist. Corrected 2026-08-02.

Cite **Nannūl/Tholkappiyam as the authority** and TVA as the *verified-against* reference — the
classical text is the grammar's source; TVA is the accredited modern presentation of it.

**நூற்பா numbers are now available.** The TVA lessons quote Nannūl verbatim *with* verse numbers, so a
rule table can carry verse-level citation (D-011) without a separately pinned classical edition. Cite
the நூற்பா the lesson actually prints — **never fill a verse number from memory**. Where a lesson states
a rule but does not quote its நூற்பா, record `verse: null` with a note (e.g. the நான்காம் வேற்றுமை
நூற்பா is nowhere in A0211).
