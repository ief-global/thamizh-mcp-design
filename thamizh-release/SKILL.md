---
name: thamizh-release
description: "Ship the Thamizh MCP server to real users: run the blocking license/data audit, package for PyPI + uvx + Docker (GHCR), deploy the IEF hosted instance (Google Cloud Run behind Cloudflare edge at ief-global.org), list on MCP registries (official registry, mcp.so, Smithery, Glama, PulseMCP, awesome-mcp-servers) and the tamil-nlp-catalog, and stand up the public web tool. Use whenever the user wants to publish, release, deploy, host, package, version, or announce the thamizh-mcp server, run the pre-release license audit, set up api.ief-global.org, or activate Google nonprofit credits for it. Triggers: 'release v1', 'publish to PyPI', 'deploy to Cloud Run', 'list on the MCP registry', 'license audit', 'make it public for users'. Do NOT trigger for building server features (thamizh-mcp-builder), benchmarks (thamizh-eval), dataset publishing (thamizh-data-curation), or the foundation's main website content work."
license: Internal project skill for the THAMIZH MCP project. (v1 — created 2026-07-10.)
---

# Thamizh Release — packaging, hosting, distribution

## Canonical docs first

Two living strategy docs in the project folder remain the source of truth — read them before acting,
update them after decisions:

- `distribution-roadmap.md` — channels, registries, adoption model (open-source + free hosted instance).
- `thamizh-mcp-hosting-plan.md` — the committed architecture: Cloudflare Pages front-end + Cloudflare
  edge (cache/rate-limit) + **Google Cloud Run** backend (scale-to-zero, free tier, IEF's $10k/yr
  Google-for-Nonprofits credits). One backend, one seam; do not add a second cloud.

This skill is the *procedure* layered on those docs: the order, the gates, the checklists.

## Gate 0 — License/data audit (BLOCKING — nothing ships past it)

Run before every rung that exposes code, data, or served content (checklist detail:
`references/release-checklist.md` §1):

1. ThamizhiMorph FSTs — Apache-2.0: attribution present in NOTICE + README + CITATION.cff.
2. Indic-To-Pure-Tamil CSVs — vendored & public already; **verify upstream MIT** (open item in
   `data/PINS.md` and NEXT-SESSION) — do this first, it's overdue.
3. Tamil Wiktionary — CC BY-SA: cache is gitignored (not shipped) — keep it that way; a *hosted*
   instance serving cached Wiktionary-derived text triggers share-alike/attribution duties → resolve
   before rung 2, document the position in the repo.
4. Madras Lexicon / TVA snapshots — confirm terms *before* the snapshots land in `data/` (blueprint §10).
5. foma vendored .debs — verify upstream license & keep the .deb redistribution note in NOTICE.
6. Own code Apache-2.0 — LICENSE/NOTICE/AUTHORS current.

## The release ladder (rungs in order; each is independently shippable)

- **Rung 0 — runnable from git (now):** `uvx --from git+https://github.com/ief-admin/thamizh-mcp
  thamizh-mcp` works on a clean machine with foma installed; README quickstart for Claude
  Desktop/Code + Cursor config blocks; cut `v0.x` tag from `main` (PR develop→main).
- **Rung 1 — PyPI + Docker:** `uv build` + publish (name check: `thamizh-mcp`); Docker image (repo
  Dockerfile bundles foma — the escape hatch for the system-dep) pushed to GHCR. The foma requirement
  is THE support burden: server must fail with an actionable message when flookup is absent, and docs
  must lead with the Docker path for non-Python users.
- **Rung 2 — hosted reference instance:** Cloud Run deploy per hosting plan (streamable-HTTP transport;
  scale-to-zero; Stanza stays off the single-word path); `api.ief-global.org` behind Cloudflare (SSL
  Full), edge cache on word-lookups + rate limits BEFORE announcing; activate Google Cloud nonprofit
  credits. Decide min-instances (warm vs free) and log it in the decision log.
- **Rung 3 — discoverability:** official MCP Registry `server.json` (namespace under ief-global.org
  domain proof), then mcp.so / Smithery / Glama / PulseMCP / awesome-mcp-servers; **tamil-nlp-catalog
  (narVidhai) is the highest-leverage single listing** — same community the data comes from; short
  demo write-up in Tamil + English.
- **Rung 4 — web tool for non-technical users:** FastAPI REST head beside MCP on the same engine;
  static page on Cloudflare Pages at ief-global.org/thamizh calling it. This is the rung that reaches
  ordinary native speakers (roadmap medium-term).

## Positioning guardrail (D-003)

Public claim is exactly: *"plausibly the first Tamil சொல்-analysis MCP server"* — never "first Tamil
NLP tool". Grounded-and-honest is the differentiator; marketing copy must not promise coverage the
honest-gap design deliberately refuses to fake.

## Version & rollback discipline

- Tags from `main` only (protected; PR from develop). SemVer: schema changes to the word-analysis
  object bump MINOR pre-1.0 and get a blueprint §3 log line.
- Rollback: PyPI = yank + patch release (never delete); Cloud Run = `gcloud run services
  update-traffic --to-revisions=PREV=100` (keep previous revision warm through each release);
  data-license problem post-release = pull the affected data/dataset, ship a data-less patch, keep code
  up; write the incident to DECISIONS.md.
- Announce only after the rung's checklist is fully green — a broken quickstart at announcement time
  costs more adoption than a week's delay.

## Reference files

- `references/release-checklist.md` — command-level checklists per rung (audit, PyPI, Docker, Cloud
  Run + Cloudflare, registry listings, announcement).
