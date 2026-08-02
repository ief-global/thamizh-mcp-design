# Decoder audit — surface-vs-classical naming (D-014), 2026-08-02

Method: read every emission point in `src/thamizh_mcp/core/decoder.py`, then probe the LIVE FST on
minnaham for the actual tag surfaces, then check each against the TVA ePUB sources. No finding below
is inferred from memory — every one cites the lesson that settles it.

Observed FST tags (real `flookup` output, this box):

| word | tags |
|---|---|
| வந்தான் | `fin sim strong past=த் 3sgm=ஆன்` |
| வந்தனன் | `fin sim strong past=த் euph=அன் 3sgm=அன்` |
| வந்தீர்கள் | `fin sim strong past=த் 2pl=ஈர்கள்` |
| வந்தார்கள் | `fin sim strong past=த் 3sghe=ஆர்கள்` / `3ple=ஆர்கள்` |
| நடந்தன | `fin sim strong past=த் 3pln=அன` |
| வாழ்க | `fin sim opt=க` |
| செய்வித்தான் | `fin sim caus=வி past=த் 3sgm=ஆன்` |
| மரத்தில் | `infInc loc` / `infInc soc` |

---

## A. CONFIRMED — same bug class as கிற்/கிறு

### A1. `euph=` is dropped entirely — the சாரியை உறுப்பு vanishes
`decoder.py:255` iterates only `_PNG_ROLE`; there is no handler for `euph`. வந்தனன் therefore
decodes as வா + த் + அன், **losing an உறுப்பு**.

TVA C0212 §5.3.4 and C0214 §4.2.1 both give the split verbatim:
> வந்தனன் — வா(பகுதி) + த்(சந்தி) + த்(இடைநிலை) + **அன்(சாரியை)** + அன்(விகுதி)

The FST calls it "euphonic"; Nannūl names it சாரியை (நூற்பா 133 lists it among the six உறுப்பு;
நூற்பா 244 lists அன் among the seventeen பொதுச் சாரியை). Fix: `sariyai.json` → `from_fst["euph=அன்"]`.

**This also closes the recorded strong-verb-past-doubling gap partially** — TVA's வந்தனன் split shows
the doubled த் explicitly as சந்தி + இடைநிலை. The FST still reports only `past=த்`, so the doubling
itself remains unrecoverable, but the சாரியை half is now recoverable and cited.

### A2. `கள்` is emitted as part of the விகுதி
`decoder.py:258` emits `feats[pcode]` raw, so வந்தீர்கள் → விகுதி **ஈர்கள்**, வந்தார்கள் → **ஆர்கள்**.

TVA A0212 §3.2.1, quoting நூற்பா 336 (`இர் ஈர் ஈற்ற இரண்டும் இருதிணைப் பன்மை முன்னிலை`):
> முன்னிலைப் பன்மைக்குரிய வினைமுற்று விகுதிகள் **இர், ஈர்** என்பனவாகும். … இன்றைய வழக்கில்
> நிற்கிறீர்கள், பேசினீர்கள் என்பன போல ரகர ஒற்றும் **கள் விகுதியும் சேர்த்துப்** பேசும் முறையே
> மிகுதியாக உள்ளது. … இந்த வினைமுற்றுகள் முற்காலத்தில் இர், ஈர் என்னும் விகுதிகளை **மட்டும்**
> பெற்றிருந்தன.

The classical விகுதி is ஈர்/ஆர்; கள் is a modern plural accretion and should be its own உறுப்பு.
Exactly the கிற்/கிறு shape: surface morph presented as the grammatical name.
Fix: `vikuthi.json` → `modern_plural` field.

### A3. `3pln=அன` is two உறுப்புகள் reported as one — and currently as none
`3pln` is not in `_PNG_ROLE` at all (`decoder.py:125–133`), so நடந்தன gets **no விகுதி**.
TVA C0214 §4.2.1:
> நடந்தன — நட(பகுதி) + த்(ந்) சந்தி விகாரம் + த்(இடைநிலை) + **அன்(சாரியை)** + **அ(விகுதி)**

Fix: `vikuthi.json` → `from_fst["3pln=அன"]` yields விகுதி அ + சாரியை அன்.

### A4. `opt=` is dropped — வியங்கோள் விகுதி missing
வாழ்க gives `opt=க`; not in `_PNG_ROLE`, so no விகுதி is emitted. நன்னூல் 140 lists க, ய, ஈயர்;
TVA C0212 §6.1 gives நிற்க–க, வாழிய–ய, நிலீயர்–ஈயர். Fix: `vikuthi.json` class `opt`.

### A5. வேற்றுமை உருபு inventories are truncated to one form per case
`_CASE_URUBU` (`decoder.py:136–138`) lists a single உருபு per case. Nannūl gives more:

| case | code has | Nannūl / TVA | நூற்பா |
|---|---|---|---|
| inst | ஆல் | **ஆல், ஆன்** | 297 |
| abl | இன் | **இன், இல்** | 299 |
| gen | அது | **அது, ஆது, அ** (number-conditioned) | 300 |
| loc | இல் | **கண்** ஆதியாக 27 forms (இல் among them) | 301, 302 |
| acc / dat / soc | ஐ / கு / ஒடு | correct | 296 / — / 297 |

Consequence: `_select_urubu` (`decoder.py:210`) can only ever match one string, so வீட்டின்
(abl இன்) and a genuine இல்-ablative are conflated, and a locative in கண்/வயின்/உள் etc. falls back
to the wrong canonical form. Fix: `verrumai_urubu.json` `cases[*].urubu` lists.

### A6. சொல்லுருபு presented as உருபு
`_CASE_MAP` (`decoder.py:52–62`) names case 6 "ஆறாம் வேற்றுமை (**அது/உடைய**)" and case 5
"ஐந்தாம் வேற்றுமை (**இன்/இலிருந்து**)".

`உடைய` is a **சொல்லுருபு** (TVA A0211 §6.2) and `இலிருந்து` is a modern colloquial form that is not
in Nannūl at all. Both sit in the same display slot as the real உருபு. This is the surface/classical
confusion in its purest form and a scholar will catch it. The two categories are kept apart in
`verrumai_urubu.json` (`urubu` vs `sollurubu`).

### A7. மரம் → மரத்து விகாரம் is misnamed
`decoder.py:184–186` emits `திரிதல் — ம் changes to த்`. TVA C0214 §4.2.1 writes the join as:
> மரம் + ஐ > **மர + அத்து + ஐ** = மரத்தை

The ம் **drops** (கெடுதல்); the த் comes from the சாரியை **அத்து** (தோன்றல்). Nothing turns into
anything. Fix: `sariyai.json` → `oblique_increment.vikaram`.

### A8. `SandhiEvent.type` uses a term that is not one of the three விகாரம்
`decoder.py:205, 248` emit `type="வல்லினம்மிகுதல்"`. நூற்பா 154 names exactly three:

> தோன்றல், திரிதல், கெடுதல் விகாரம் மூன்றும் மொழிமூ இடத்தும் இயலும் (154)

TVA C0213 §1.6.2 classifies வல்லினம் doubling under **தோன்றல்** explicitly
(`யானை + கொம்பு = யானைக் கொம்பு — க் என்ற எழுத்துத் தோன்றியது`), and a சாரியை appearing at a join
under தோன்றல் too (`ஆ + பால் = ஆவின் பால் — இன் என்ற சாரியை தோன்றியது`). "வல்லினம்மிகுதல்" is a
description of the event, not its classical name. Fix: `vikaram.json` — keep the description in
`detail`, set `type` to the நூற்பா-154 name.

---

## B. FLAGGED — needs Saran's ruling, not a unilateral change

### B1. Is the causative வி an இடைநிலை or a விகுதி?
`decoder.py:121` labels `caus=வி` / `pass=` as **இடைநிலை** (செய்வித்தான் → செய்+வி+த்+ஆன்).

TVA calls வி/பி something else, twice:
- C0212 §6.1.7 "**பிறவினை விகுதிகள்** … வி, பி, கு, சு, டு, து, பு, று"
- A0212 "பிறவினையாகும்போது **வி, பி ஆகிய விகுதிகளில்** ஒன்று சேர்ந்து வருவதும் உண்டு"

But வி sits medially (செய் + **வி** + த் + ஆன்), and நன்னூல் defines இடைநிலை positionally as what
stands between முதனிலை and இறுதிநிலை (C0212 §5.3.3). So the positional definition says இடைநிலை and
TVA's own list says விகுதி. Recorded as a conflict in `vikuthi.json.known_gaps`; label unchanged
until Saran rules.

---

## C. CLEAN — checked, no finding

- `_POS_MAP` / `_WORD_CLASS` (`decoder.py:40–48`) — the four Tholkappiyam classes, correctly named.
- இடைநிலை (`map_idainilai`) — already normalised by the D-014 fix; re-verified against C0212 §6.2,
  which quotes நூற்பா 142 and 143 identically to A0212. Independent second attestation.
- `_TENSE_ROLE` — இறந்தகாலம்/நிகழ்காலம்/எதிர்காலம் matches நூற்பா 382 (`இறப்பு எதிர்வு நிகழ்வு எனக்
  காலம் மூன்றே`), which C0212/A0212 quote.
- `word_type` பகுபதம்/பகாப்பதம் — matches C0212 §§5.1–5.2.
- `பகுதி` = lemma — correct as far as it goes; the வா→வ் விகாரம் remains the already-recorded
  honest boundary (TVA C0212 §5.3.6 names it, the FST does not hand it over).

---

## D. Bonus: நூற்பா numbers now available (advances D-011)

Verified verbatim in the ePUBs, so they can be cited without a pinned edition:

| topic | நூற்பா | lesson |
|---|---|---|
| six பகுபத உறுப்பு | **133** | C0212 §5.3 |
| வினைப் பகாப்பதம், 23 மாதிரி | 136 | A0212 |
| இயல்பு புணர்ச்சி | **153** | C0213 §1.6.1 |
| three விகாரம் | **154** | C0213 §1.6.2 |
| several விகாரம் in one join | **157** | C0213 §1.6.2 |
| விகுதி inventory (37 → 40) | **140** | C0212 §6.1 |
| இறந்தகால இடைநிலை | 142 | C0212 §6.2, A0212 §6.2.1 |
| நிகழ்கால இடைநிலை | 143 | C0212 §6.2, A0212 §6.2.1 |
| காலம் காட்டும் விகுதி | **145** | C0212 §6.3 |
| உருபு forty forms | **240** | C0214 §4.1.1 |
| உருபு placement | **241** | C0214 §4.1.2 |
| உருபு புணர்ச்சி | **242** | C0214 §4.1.3 |
| சாரியை occurrence | **243** | C0214 §4.2.1 |
| seventeen பொதுச் சாரியை | **244** | C0214 §4.2.2 |
| வேற்றுமை definition (eight) | **291** | A0211 §5.1 |
| எழுவாய் உருபு takes the six | **293** | C0214 §4.1 |
| 1st / 2nd / 3rd வேற்றுமை | **295 / 296 / 297** | A0211 §§5.2–5.4 |
| 5th / 6th / 7th / 8th வேற்றுமை | **299 / 300 / 301+302 / 303** | A0211 §§6.1–6.4 |
| முதல்/சினை உருபு | **315** | A0211 §6.5 |
| தெரிநிலை வினை six பொருள் | 319 | A0212 §1.1.1 |
| முன்னிலைப் பன்மை விகுதி இர்/ஈர் | **336** | A0212 §3.2.1 |
| வினையெச்ச வாய்பாடு (12) | 343 | A0212 §5.6.1 |
| சினைவினை | 345 | A0212 §5.7.1 |
| வினையெச்ச மாற்றம் | 346 | A0212 §5.8.6 |
| முக்காலம் | 382 | A0212 §6.1 |

Not found in the ePUBs (do NOT fill from memory): the **நான்காம் வேற்றுமை** நூற்பா — A0211 §5.5
gives the உருபு கு and the seven பொருள் but never quotes the verse.
