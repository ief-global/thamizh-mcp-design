# Nannūl commentaries — pinned scan (D-029)

Local mirror of நன்னூல் உரைவளம், தொகுதி 5 (பதவியல்), ed. முனைவர் இரா. கண்ணன், உலகத் தமிழாராய்ச்சி
நிறுவனம், சென்னை, 2010. It prints every commentator on each பதவியல் நூற்பா side by side: மயிலைநாதர்,
சங்கர நமச்சிவாயர் with சிவஞான முனிவர், கூழங்கைத் தம்பிரான், விசாகப் பெருமாளையர், ஆறுமுக நாவலர் and
later ones. It is a Tamil Digital Library scan in Tamil Virtual Academy's archive.org collection:
**CC BY-SA 4.0** (D-021). Attribution: Tamil Digital Library, Tamil Virtual Academy, Government of
Tamil Nadu.

The code repo builds `data/classical/nannul_uraivalam_padaviyal.json` from this mirror, but it keeps
only the OCR of the pages a rule cites (`scripts/build_nannul_uraivalam.py`, `LEAVES`). The files
themselves are **not in git** (see `.gitignore`). archive.org's own MD5s matched every file on download
(2026-11-25).

| File | From | sha256 |
|---|---|---|
| `uraivalam5_scan.pdf` (scan, 152,227,490 B) | [tdl.6041-5](https://archive.org/details/tdl.6041-5) | `299da0ea203d88263332a9b78dc0cd794e1ce6edc34173352ba1361202b07196` |
| `uraivalam5_djvu.xml` (OCR, read by the build) | ″ | `3fbda381be962ca92e2b2b5ab917eb84a558e858ba5333a0159c6887c4bdddb3` |
| `uraivalam5_page_numbers.json` | ″ | `53a82da4cd8bb4b56c311978f3ee9596d09e455f6a346a02ce04fe08faeffb4e` |
| `uraivalam5_djvu.txt` (plain OCR, reference only) | ″ | `611471c26d50a63038038a055b64776c8948cc09a6dd91d6f808c651c9e1a44d` |

In this volume the leaf number equals the printed page. Its நூற்பா numbers run one lower than our
pinned Nannūl in places (its 138 is our 139); quotations are filed under OUR number.

Rebuild from this mirror (code repo):

    uv run python scripts/build_nannul_uraivalam.py --mirror ~/projects/thamizh-mcp-design/sources/classical/nannul-urai

Restore a file: download it from the archive.org item above and check its sha256 here.
