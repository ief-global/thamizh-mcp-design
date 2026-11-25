# தேவநேயப் பாவாணர் — pinned scans (D-031)

Local mirror of three books by ஞா. தேவநேயப் பாவாணர், all Tamil Digital Library scans in Tamil Virtual
Academy's archive.org collection: **CC BY-SA 4.0** (D-021). Attribution: Tamil Digital Library, Tamil
Virtual Academy, Government of Tamil Nadu. Saran ruled (D-031) that பாவாணர்'s statements are
authoritative and break ties where the classical sources are silent or disagree.

| Mirror stem | Book | archive.org |
|---|---|---|
| `kalanjiyam25` | பாவாணர் தமிழ்க் களஞ்சியம் 25: இயற்றமிழ் இலக்கணம் (தமிழ்மண் அறக்கட்டளை). Typeset PDF: render its pages; its font prints ய் as "-". | [tdl.48547-25](https://archive.org/details/tdl.48547-25) |
| `kalanjiyam19` | பாவாணர் தமிழ்க் களஞ்சியம் 19: வேர்ச்சொற் கட்டுரைகள் 3 | [tdl.48510-19-3](https://archive.org/details/tdl.48510-19-3) |
| `eluthu1972` | தொல்காப்பியம் எழுத்ததிகாரம், நச்சினார்க்கினியர் உரை, with பாவாணர்'s footnotes (தென்னிந்திய சைவசித்தாந்த நூற்பதிப்புக் கழகம், 1972; first edition 1944) | [dli.jZY9lup2kZl6TuXGlZQdjZMdl0Uy](https://archive.org/details/dli.jZY9lup2kZl6TuXGlZQdjZMdl0Uy) |

Each stem has `_scan.pdf`, `_djvu.xml` (OCR, read by the build), `_page_numbers.json` and
`_djvu.txt` (reference only). The files are **not in git** (see `.gitignore`). sha256 for every file
read by the build is in the code repo's `scripts/build_pavanar.py` and `data/PINS.md`; archive.org's
MD5s matched on download (2026-11-25).

The code repo builds `data/classical/pavanar_iyatramil_ilakkanam.json` from `kalanjiyam25`, keeping only
the pages a rule cites. The other two books are pinned by checksum with no page cited yet.

Rebuild from this mirror (code repo):

    uv run python scripts/build_pavanar.py --mirror ~/projects/thamizh-mcp-design/sources/classical/pavanar

Other volumes of the களஞ்சியம் series in the same collection that bear on this work: 17, 18, 20
(வேர்ச்சொற் கட்டுரைகள் 1, 2, 4), 21 (சொல்லாராய்ச்சிக் கட்டுரைகள்), 37 (சுட்டு விளக்கம்), 41 (இலக்கணக்
கட்டுரைகள்).
