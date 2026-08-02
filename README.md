# Thamizh MCP — design

The design, decisions and roadmap behind
[**thamizh-mcp**](https://github.com/ief-global/thamizh-mcp), a source-grounded Tamil word-grammar
(**சொல் இலக்கணம்**) analyser. This repo carries the *why*; the code repo carries the *what*.

It is public because the linguistics should be auditable. If you are a Tamil scholar, the interesting
question is not our Python — it is whether our grammar is right, and whether every claim names the
நூற்பா that settles it. **Corrections are welcome and valuable.** See [Contributing](#contributing).

Built by the nonprofit [International Educational Foundation](https://ief-global.org).

## Start here

| Document | What it is |
|---|---|
| [`DESIGN.md`](DESIGN.md) | The program design. **§4a** is the one to read first — Tholkappiyam-first priority, and how a citation is written. |
| [`Thamizh-MCP-blueprint.md`](Thamizh-MCP-blueprint.md) | Architecture of the server itself. |
| [`thamizh-mcp-builder/references/DECISIONS.md`](thamizh-mcp-builder/references/DECISIONS.md) | Decision log — every non-obvious choice, with its trigger and its consequences. |
| [`thamizh-mcp-builder/references/tamil-grammar.md`](thamizh-mcp-builder/references/tamil-grammar.md) | The grammar reference the code is built against, including the **source-priority table**. |
| [`DECODER-AUDIT-D014.md`](DECODER-AUDIT-D014.md) | A worked audit of where our output drifted from classical naming — the most concrete example of how this project checks itself. |
| [`sources/`](sources/) | Which texts ground which rule, how they are cited, and what we may redistribute. |
| [`CODE-STATUS.md`](CODE-STATUS.md) | What is actually live in the server, read across from the code side. |

## The rules this project does not bend

- **Tholkappiyam-first.** Tholkappiyam is the primary authority for word classes, வேற்றுமை and
  புணர்ச்சி; Nannūl is the fallback, and the primary only where Tholkappiyam does not cover the
  ground (it does not enumerate the six பகுபத உறுப்பு). Where the two differ, we record the
  difference rather than collapsing it — Tholkappiyam gives the third-case உருபு as **ஒடு**
  (வேற்றுமையியல் 12) where Nannūl 297 gives ஆல், ஆன், ஒடு, ஓடு.
- **Honesty over guessing.** An unknown is returned as an explicit gap. A verse number that the
  pinned edition does not print is recorded as absent, never inferred.
- **Every claim names its source.** Grammar rules ship as cited JSON tables in the code repo, so the
  linguistics can be audited as data without reading Python.

## Citing a நூற்பா — read this before quoting one

Both classical texts are pinned as version-locked artifacts in the code repo
(`data/classical/`), sourced from **Project Madurai**.

⚠️ **Tholkappiyam நூற்பா numbers restart at 1 in every இயல்** and collide across இயல் *and*
அதிகாரம். A bare number is unusable — always qualify it:

```
தொல்காப்பியம், சொல்லதிகாரம், வேற்றுமையியல், நூற்பா 3
தொல்காப்பியம், எழுத்ததிகாரம், புணரியல், நூற்பா 7
நன்னூல், நூற்பா 244        ← Nannūl numbering is continuous 1–462
```

And **do not take verse numbers from secondary sources**, however accredited. The Tamil Virtual
Academy course books quote Nannūl selectively and renumber: their 336, 319 and 136 are **337, 320
and 137** in the pinned edition. All three were wrong in our tables before we pinned the full text.

## How the two repos relate

```
ief-global/thamizh-mcp          code, rule tables, pinned classical texts, tests  (Apache-2.0)
ief-global/thamizh-mcp-design   this repo — design, decisions, roadmap, sources, eval
```

They are deliberately separate and must never be nested. Design docs do not go in the code repo;
code does not go here.

## Contributing

Especially welcome from Tamil scholars and teachers:

- **A grammar claim that is wrong**, or cited to the wrong நூற்பா. Please name the verse you would
  cite instead — open an issue, or a PR against `DECISIONS.md` / the relevant reference.
- **A place where Nannūl is cited but Tholkappiyam covers the ground**, or vice versa.
- **Corrections to the pinned texts** — those come from Project Madurai, so upstream errors should
  also go to them; tell us and we will re-pin.

Flow: branch from `develop` → PR to `develop` → we merge to `main` at milestones. Same cadence as the
code repo.

## Source materials and licensing

Some reference material here is **quoted for citation, not redistributed**. In particular the Tamil
Virtual Academy course books (Government of Tamil Nadu) are *gitignored* — only the derived, cited
rule tables ship. Project Madurai's classical etexts *are* redistributable and travel with their
header intact. See [`sources/README.md`](sources/README.md) and the code repo's `LICENSING.md`.

Third-party documents reproduced here for research reference remain the property of their authors
and are cited accordingly.
