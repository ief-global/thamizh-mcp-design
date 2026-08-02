# Thamizh-AI — brand brief

> Paste this into Claude Design (or any design tool) **alongside `PRESENTATION-SOURCE.md`**.
> `/design-sync` is not useful for this project — it reads design tokens and React components from a
> codebase, and this repo holds documents, not components. This file is the replacement: it states the
> identity explicitly instead of hoping a tool infers it.
>
> The values below are the **real tokens already shipping** in the live web app
> (`thamizh-mcp/src/thamizh_mcp/static/index.html`) and the HTML deck (`deck/index.html`). Reusing them
> makes the deck, the app and the site read as one product.

## What this is

**Thamizh-AI** (`thamizh-ai.org`) — a project of **International Educational Foundation Inc.**, a
nonprofit. It grounds AI answers about Tamil words in classical grammar (தொல்காப்பியம் first, நன்னூல்
where Tholkappiyam doesn't codify the point), cites every claim, and returns an honest gap rather than
a guess. Open source, Apache-2.0.

**Wordmark:** **தமிழ்AI** (preferred — the script switch makes the point instantly) or **Thamizh-AI**.
Never "Tamil AI" (we use the *Thamizh* transliteration throughout) and never "ThamizhAI" unhyphenated
in prose — joined, it reads as **தமிழை**, the accusative of தமிழ், which buries the AI signal.

## Audience & tone

Tamil scholars, teachers, students, and developers building Tamil apps. They are grammar-literate and
**will fact-check the Tamil on screen**.

- **Scholarly, calm, confident** — a research group sharing work, not a startup pitching.
- **Understated over emphatic.** No hype words, no "revolutionary", no growth-deck energy.
- Honesty is the brand: we say what doesn't work yet, and that *builds* credibility with this audience.
- Tamil term first, English gloss in parentheses — e.g. "பகுபத உறுப்பு (formation)".

## Colour

| Token | Value | Use |
|---|---|---|
| `--accent` | `#7a1f2b` | primary — deep maroon; headings, kickers, the one emphasised word |
| `--accent2` | `#2f3d6b` | secondary — indigo; structural accents, part borders, diagrams |
| `--ink` | `#241c1c` | body text |
| `--muted` | `#6f6260` | captions, source lines, secondary text |
| `--bg` | `#fbf8f5` | page background — warm off-white |
| `--card` | `#ffffff` | raised surfaces |
| `--line` | `#e2d9d3` | hairline borders |
| `--ok` | `#1f6b4a` | correct / verified |
| `--warn` | `#8a6a1f` | honest gaps — a *neutral* signal, never an error red |

Dark variants (app only, viewer-toggled): ink `#f0e9e4`, bg `#1a1615`, card `#241f1d`,
accent `#e08a96`, accent2 `#9fb0e6`.

**Rules.** Light background by default — projectors wash out dark themes. Maroon and indigo are the
only chromatic colours; everything else is warm neutral. **Never** neon, gradients, or "AI purple".
Gaps use amber, not red — an honest gap is a *feature*, not a failure.

## Typography

```
Tamil:  "Noto Sans Tamil", "Latha", "Nirmala UI", "Tamil Sangam MN", "Lohit Tamil", sans-serif
UI:     system-ui, -apple-system, "Segoe UI", sans-serif      ← labels, kickers, numbers only
Mono:   ui-monospace, "Cascadia Mono", Menlo, Consolas, monospace   ← tool output
```

- **Tamil is the primary typeface — set body and headings in it**, not in a Latin font that falls back.
- Latin UI font is for *labels, small caps kickers, and figures* only.
- Kickers: uppercase, letter-spacing ~0.18em, small, in maroon.
- Numbers: tabular figures.

## ⚠️ Tamil rendering — the highest-risk item

Tamil is a complex script requiring proper text shaping. Many deck tools and templates break it.

- **Test before building the whole deck.** Put these on slide 1 and inspect at full size:
  **ற்ற · ன்ற · க்ஷ · ஸ்ரீ · மரத்தில் · வந்தான் · கொடுத்தான்**
- Failure looks like: detached or reordered vowel signs, tofu boxes (□), or broken conjuncts.
- If the tool can't render Tamil correctly, **put the Tamil in images** rather than shipping broken
  glyphs. A scholar spots it in one slide and it costs credibility immediately.
- Never letter-space Tamil text; never force uppercase (Tamil has no case).

## Layout

- Generous whitespace; one idea per slide; large type (deck body ≈ 2.7vh, headings ≈ 5vh).
- Tool output belongs in a **monospace block with a left accent rule** — the raw, unpolished honesty of
  the output is the persuasive element. Don't beautify it into marketing copy.
- Formation shown as **discrete parts joined by `+`**, each labelled with its grammatical role and
  authority — mirrors how it's taught, and how the product renders it.
- Tables: hairline bottom borders only, no zebra striping, no boxes.
- Cite sources in small muted text under the claim, never in a footnote nobody reads.

## Don'ts

- No stock photography of "AI" (glowing brains, circuit boards, robots).
- No Indian-cultural clip art — no temples, no kolam borders, no diyas. The typography is the culture.
- No emoji in slide bodies.
- No claims not present in `PRESENTATION-SOURCE.md` — every figure and Tamil form there is verified
  against the live build. **Do not invent examples**; a fabricated Tamil example in a deck about not
  fabricating Tamil would be fatal.
- Read the "Accuracy guardrails" section of `PRESENTATION-SOURCE.md` before generating: notably
  **ஜன்னல் must not be used as an origin example** (the tool says வடசொல், but it is a Portuguese loan).
