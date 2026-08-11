# CLAUDE.md — Thamizh MCP **design** repo (developer context for Claude Code)

The design/docs companion to [`ief-global/thamizh-mcp`](https://github.com/ief-global/thamizh-mcp).
This repo carries the *why* — design, decision log, grammar reference, roadmap, eval, source
provenance. The code repo carries the *what*.

**PUBLIC since 2026-08-02.** It was private until then, and some text still assumes privacy —
if you find "this private repo" phrasing, fix it. Being public is deliberate: the linguistics
should be auditable by Tamil scholars, and contributions are wanted.

## Git identity — use everywhere, no exceptions
Commit as **Saran Saravanan <saravanan3@duck.com>**, GitHub **ssaravanan3**.
NEVER commit under the legacy `asaravanan75@gmail.com` / `asaravanan75-eng`.
Verify: `git log --format='%an <%ae>' -1`.

## Branch workflow — same as the code repo
`main` = stable. `develop` = integration. Loop: work on **`develop`** → push → open PR
`develop → main` → **Saran merges**. Do not commit straight to `main`.

Historical note so the drift is not re-diagnosed: 26 of the first 28 commits went directly to `main`,
which is why `develop` kept falling behind and looked like a missing PR. It was not — `develop` was
vestigial. The develop→PR→main flow starts 2026-08-02 and is now the same in both repos, so there is
one cadence to remember, not two.

## What lives here

| Path | What |
|---|---|
| `DESIGN.md` | Program design. **§4a = Tholkappiyam-first priority + citation format.** |
| `Glossary.md` | **Computational-linguistics vocabulary mapped onto Tamil grammar terms** — for scholars who know வேற்றுமை/விகுதி but not "lemma"/"FST"/"treebank". Added 2026-08-10. Read §1.1 and the §8 worked examples first. |
| `Thamizh-MCP-blueprint.md` | Server architecture. |
| `thamizh-mcp-builder/references/DECISIONS.md` | Decision log, D-001…D-014. Append, never rewrite history. |
| `thamizh-mcp-builder/references/tamil-grammar.md` | Grammar reference + **source-priority table** (which authority governs which topic). |
| `DECODER-AUDIT-D014.md` | Audit of surface-vs-classical naming drift in the decoder. |
| `sources/` | Provenance: `classical/` (pinned Tholkappiyam + Nannūl), `tva/` (course books, **gitignored**). |
| `CODE-STATUS.md` | Read-across of what is live in the server. Keep in sync with the code repo's CLAUDE.md "Current state". |
| `thamizh-eval/` | Phase-4 eval harness, fixtures, results. |
| `BRAND.md`, `deck/`, `PRESENTATION-SOURCE.md` | Public-facing material. |

## Grammar rules (do not violate)

- **Tholkappiyam-first.** Primary for word classes, வேற்றுமை, புணர்ச்சி. Nannūl is fallback — and
  genuinely primary only where Tholkappiyam does not cover the ground (it does not enumerate the six
  பகுபத உறுப்பு). This drifted once because the TVA lessons quote Nannūl; the fix was a
  **mechanism**, not a restatement — every `data/grammar/*.json` in the code repo carries a
  `source_priority` block and `tests/test_citations.py` fails without one.
- **NEVER write a நூற்பா number from memory, or from a secondary source.** TVA renumbers: its
  336/319/136 are **337/320/137** in the pinned edition. Look verses up in the code repo's
  `data/classical/*.json`.
- **தொல்காப்பியம் numbers restart per இயல்** — cite அதிகாரம் › இயல் › நூற்பா. நன்னூல் is
  continuous 1–462, so a bare number is unambiguous.
- **Record divergence, don't collapse it.** Tholkappiyam's third-case உருபு is ஒடு
  (வேற்றுமையியல் 12); Nannūl 297 gives ஆல், ஆன், ஒடு, ஓடு. Both are true; say so.
- **Honesty over guessing.** A verse the pinned edition does not print is `verse: null` with a note.

## Source materials — what may be redistributed

- **Project Madurai** (Tholkappiyam, Nannūl): free distribution **provided the header stays intact**.
  So the derived artifacts ship publicly in the code repo, header included.
- **TVA course books** (Government of Tamil Nadu): no redistribution grant. The ePUBs are
  **gitignored** and stay local; only derived, cited rule tables ship. Do not commit them — check
  `git check-ignore` before adding anything under `sources/tva/`.
- Third-party papers reproduced here are for research reference and remain their authors' property.

## Gotchas

- This repo is **public now** — assume anything committed is world-readable. Check before adding
  personal identifiers, internal hostnames, or third-party documents.
- Never nest this repo inside `thamizh-mcp`, and never commit design docs into the code repo.
- `CODE-STATUS.md` is a mirror, not a spec — the code repo's `CLAUDE.md` is authoritative for code
  state. If they disagree, the code repo wins and this one needs updating.
