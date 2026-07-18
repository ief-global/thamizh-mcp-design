# Thamizh MCP — resume here next session

Last worked: 2026-07-03. Everything below is on disk and in git; the repo is PUBLIC.

## Git identity — SETTLED 2026-07-03 (use everywhere, every session)

Canonical for ALL commits + all machines/sessions: **Saran Saravanan** /
**saravanan3@duck.com** / GitHub **ssaravanan3**. (Duck alias forwards to the gmail
and strips trackers; keeps the gmail out of public repos.) Legacy
`asaravanan75@gmail.com` / GitHub **asaravanan75-eng** = family/legacy — never
commit under it. `git config --global` is set to the duck identity on both boxes,
and history was rewritten so every thamizh-mcp commit is under ssaravanan3.

## Where we are

- **Phase 1 core DONE** — FastMCP server, `analyze_word` end-to-end, ThamizhiMorph
  FST anchor, SQLite per-claim store + enrichment loop, Wiktionary adapter (UA fix
  + real ta.wiktionary parser). 27 tests pass (25 without live foma).
- **Repo PUBLIC + hardened:** github.com/ief-admin/thamizh-mcp (nonprofit org),
  Apache-2.0. Hygiene files in place (LICENSE, NOTICE, AUTHORS, CITATION.cff,
  .gitignore, .gitattributes, CONTRIBUTING.md). Docs read "Thamizh MCP".
- **Branching:** `main` = stable, protected (PR-only, no force-push, no delete,
  0 required reviews) + `develop` = integration. Loop: author on E:\ → push to
  `develop` from Windows → Linux pulls `develop` to test → PR `develop → main` at
  milestones. minnaham is on `develop`, aligned with origin.

## Done today (2026-07-03, later session)

Git go-public + Linux re-clone + uv.lock added; pytest moved to
`[dependency-groups]`; "THAMIZH MCP" → "Thamizh MCP" doc rename; identity
consolidated (filter-repo --mailmap rewrite → all commits under ssaravanan3);
CONTRIBUTING.md added; `develop` branch + `main` protection.

## ➡️ Next (build — Phase 1 tail + Phase 2/3)

1. **Confirm** `main` branch protection is actually enabled (finish if not).
2. **Kalaichol / equivalents adapter** over the pinned I2PT CSVs
   (`data/equivalents/`, 2,063 rows) — LOCAL data, buildable immediately; fuels
   `suggest_native_equivalent`. Also mine ta.wiktionary `{{சொல்வளம்N|...}}`
   synonym templates as an evolving equivalent source.
3. **Origin classifier** — Thamizhi Validator + I2PT + loanword data → four
   Tholkappiyam classes (இயற்சொல் / வடசொல் / …).
4. **Remaining MCP tools:** classify_origin, get_root, get_meaning,
   explain_formation, explain_grammar, suggest_native_equivalent, enrich_word.
5. **Formation decoder** (FST tags → பகுபத உறுப்பு) — Phase 3.
6. **Network-open jobs** (server / Claude Code): Madras Lexicon + TVA கலைச்சொல்
   snapshots → pin in `data/` (blueprint §10; offline-pinned route recommended).

## ⚠️ Open license items (repo is already public — do promptly)

- **I2PT = MIT "verify"** (`data/PINS.md`): the CSVs are vendored and public now;
  confirm upstream (github.com/narVidhai/Indic-To-Pure-Tamil) is really MIT.
- **Wiktionary CC BY-SA share-alike:** the sqlite cache is gitignored (not
  shipped), so lower urgency, but resolve before distributing any cached text.

## ⚠️ Gotchas (all still apply)

- **E:\ mount = truncation (>~3.3KB) AND write-but-no-delete** → author files via
  bash heredoc + verify nulls; **git runs ONLY on Saran's boxes** (the sandbox
  corrupts `.git`). Watch for stray null bytes appended on mount writes.
- **foma on Ubuntu:** install package `foma` (NOT `foma-bin` — empty transitional).
- **Wikimedia UA policy:** descriptive UA lives in the adapter (env `THAMIZH_HTTP_UA`).
- **Git Bash + git-filter-repo:** pass a REAL file to `--mailmap`, not `<(...)`
  process substitution (native Python can't read /dev/fd); use `--force`.
- **After a history rewrite,** other clones must `git reset --hard origin/main`,
  NOT merge/rebase.
- `--include meaning` skips morphology by design (empty lemma there is not a bug).

## Where things live

- Blueprint: `THAMIZH-MCP-blueprint.md` · Runbook: `thamizh-mcp/TESTING-ON-LINUX.md`
  · Pins: `thamizh-mcp/data/PINS.md` · Demo CLI: `thamizh-mcp/scripts/analyze.py`
- Hosting: `thamizh-mcp-hosting-plan.md` · Distribution: `distribution-roadmap.md`
- Builder skill (installed + done): `thamizh-mcp-builder/`, `thamizh-mcp-builder-v4.skill`
