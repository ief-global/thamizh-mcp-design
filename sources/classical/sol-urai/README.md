# சொல்லதிகாரம் commentaries — pinned scans (D-027, D-028)

Local mirror of the three classical commentaries on தொல்காப்பியம் சொல்லதிகாரம் that the code repo
builds `data/classical/tholkappiyam_sol_urai_*.json` from. All are Tamil Digital Library items in
Tamil Virtual Academy's archive.org collection: **CC BY-SA 4.0** (D-021). Attribution: Tamil Digital
Library, Tamil Virtual Academy, Government of Tamil Nadu.

The files themselves are **not in git** (see `.gitignore`); this README records what they are, so a
copy can be checked or restored. archive.org's own MD5s matched every file on download (2026-11-25).

| File | From | sha256 |
|---|---|---|
| `nacchinarkkiniyar_scan.pdf` (766 leaves, 267,617,873 B) | [dli.jZY9lup2kZl6TuXGlZQdjZM3kZpy.TVA_BOK_0008472](https://archive.org/details/dli.jZY9lup2kZl6TuXGlZQdjZM3kZpy.TVA_BOK_0008472) · சரசுவதி மகால் நூலகம், தஞ்சாவூர், 1999 | `8e71d5a3f7b9695374794339c54f7153f88a6bd6e97400c2792f78371ea3670d` |
| `nacchinarkkiniyar_djvu.xml` (OCR, read by the build) | ″ | `a9e7819f5b9e2581f5f3726a8a6689ca47d8062b922d1ddcb98ede19e6539ec0` |
| `nacchinarkkiniyar_page_numbers.json` | ″ | `a6be52bceec7cf02ccbb22dc65d8d6652d9992eaa550878934161467ddc9a99e` |
| `nacchinarkkiniyar_djvu.txt` (plain OCR, reference only) | ″ | `2a59d4acdc556fd6fdeb9e85316c00f89a0d64e705d048efe1d45463f843015c` |
| `ilampuranar_scan.pdf` (526 leaves, 211,340,206 B) | [dli.jZY9lup2kZl6TuXGlZQdjZMdlupy](https://archive.org/details/dli.jZY9lup2kZl6TuXGlZQdjZMdlupy) · தமிழ்ப் பல்கலைக்கழகம், தஞ்சாவூர், 1988 | `3a731b6b3f44b475a205faea2e9e120b56f100e49686ff80f3b6905fdfb1712d` |
| `ilampuranar_djvu.xml` | ″ | `92f1d32b660acecaa996c6cdb2316157cc2195195fcd3031ab2164d5214440ae` |
| `ilampuranar_page_numbers.json` | ″ | `ae3c88f34e056b6d53d43fe6bcb9ba5162e80d596e49c99d06cca3ef3437eb88` |
| `ilampuranar_djvu.txt` | ″ | `255bd565588fcdfdc79f8cfb98b26e98659e2ad1e81c6368ff74e9a5c65f9503` |
| `senavaraiyar1_scan.pdf` (vol. 1, கிளவியாக்கம் … பெயரியல்; typeset PDF, 385 pages, 10,184,202 B) | [tdl.49552-6-1](https://archive.org/details/tdl.49552-6-1) · தொல்காப்பிய உரைத்தொகை 6, தமிழ்மண் பதிப்பகம், 2018 (சி. கணேசையர் 1938) | `aedd5ceb6020e6c7e89899475b72894c2a5705c859b21678da8e3c18f0f30470` |
| `senavaraiyar1_djvu.xml` | ″ | `6475353d5b1bdfa477d0b0a9c909c013a1100db1b1ae276adafa014bb38a6e76` |
| `senavaraiyar1_page_numbers.json` | ″ | `1fea04f99697eaf3949c4d66b3d97848cc492586310a2ac4fbeb7a30b182a200` |
| `senavaraiyar1_djvu.txt` | ″ | `8c669e07519e11aaf59a2ddc273ec75501d046841f9f92739ac0deca14184c0b` |
| `senavaraiyar2_scan.pdf` (vol. 2, வினையியல் … எச்சவியல்; typeset PDF, 409 pages, 10,071,951 B) | [tdl.49554-7-2](https://archive.org/details/tdl.49554-7-2) · தொல்காப்பிய உரைத்தொகை 7 | `2f98b6632fb746cadcf2e37b8b72ef61bc9f8f4f8a10fdf8617d3312e7f71ba4` |
| `senavaraiyar2_djvu.xml` | ″ | `1b3d3fcdd6ff8ee1abfa0cf8f519eccb7eb5122f737f73ec690efcfb3962108b` |
| `senavaraiyar2_page_numbers.json` | ″ | `87daf051431364b55cc67d09a23ac27adcca7abb6a76a6b7a5c180449ee80871` |
| `senavaraiyar2_djvu.txt` | ″ | `e8912747c3286b3d28cee663f8084053858105650e6ee6848dcd175db32cd942` |

Why these formats: the `_djvu.xml` OCR keeps each line's scan leaf, so every commentary unit can
name the page it came from; the plain `_djvu.txt` does not. The PDF is the page images, kept so a
quotation can be read against the print before a rule cites it (the OCR is not proof-read). The
EPUB and "PDF with text" are derived from the same OCR and add nothing. The சேனாவரையர் PDFs hold
typeset text, not page images, so a passage is checked by rendering the page (e.g. PyMuPDF).

Rebuild from this mirror (code repo):

    uv run python scripts/build_sol_urai.py --mirror ~/projects/thamizh-mcp-design/sources/classical/sol-urai

Restore a file: download it from the archive.org item above and check its sha256 here.
