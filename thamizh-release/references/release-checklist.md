# Release checklists (command level)

## 1. Gate 0 — license audit worksheet

| Item | Where | Check | Status/date |
|---|---|---|---|
| ThamizhiMorph attribution | NOTICE, README, CITATION.cff | citation string present | |
| I2PT upstream license | github.com/narVidhai/Indic-To-Pure-Tamil | LICENSE file really MIT; record commit | OPEN (PINS.md "verify") |
| Wiktionary cache | .gitignore; hosted-serving position | cache not in repo; position doc for rung 2 | |
| Madras Lexicon terms | DSAL terms page | written OK for snapshot+serve, else exclude | OPEN |
| TVA கலைச்சொல் terms | tva source page | same | OPEN |
| foma .debs | data/vendor/ | upstream license verified; NOTICE line | |
| Repo hygiene | LICENSE/NOTICE/AUTHORS | current year, all contributors | |

## 2. Rung 0 — runnable from git

- [ ] Clean-VM test: install foma (`apt install foma` — NOT foma-bin), `uvx --from git+…` runs, stdio
      MCP handshake OK (MCP Inspector), analyze_word(மரம்) returns schema-valid output
- [ ] README quickstart: Claude Desktop + Claude Code + Cursor JSON config blocks, foma install per OS
- [ ] Actionable error when flookup missing (exact message tested)
- [ ] PR develop→main, tag v0.x, GitHub release notes

## 3. Rung 1 — PyPI + Docker

- [ ] `uv build`; check name availability; publish to TestPyPI first; `uvx thamizh-mcp` from TestPyPI
- [ ] Entry point `thamizh-mcp` (pyproject [project.scripts]); wheels are py3-none (FSTs are data files —
      confirm package_data includes data/fst + equivalents)
- [ ] Docker: build from repo Dockerfile (foma inside); smoke-test `docker run … | MCP Inspector`;
      push GHCR `ghcr.io/ief-admin/thamizh-mcp:vX.Y` + `:latest`; README docker config block
- [ ] Post-publish: fresh-machine install test of the real PyPI package

## 4. Rung 2 — Cloud Run + Cloudflare (per thamizh-mcp-hosting-plan.md)

- [ ] Transport: streamable HTTP mode behind a flag/env (stdio remains default for local)
- [ ] `gcloud run deploy thamizh-mcp --image ghcr.io/... --region <pick> --allow-unauthenticated
      --memory 512Mi --min-instances 0 --max-instances 3` (raise memory only if flookup needs it;
      Stanza excluded from single-word path)
- [ ] Custom domain: Cloud Run domain mapping api.ief-global.org; Cloudflare DNS proxied; SSL mode Full
- [ ] Cloudflare: cache rule on GET word lookups; rate-limit rule (start ~30 req/min/IP); WAF on
- [ ] Activate Google-for-Nonprofits Cloud credits BEFORE traffic; billing alert at $5
- [ ] Load sanity: 20 concurrent analyze_word, no event-loop stall (non-blocking rule blueprint §7)
- [ ] Decide + log min-instances warm vs cold (D-entry)

## 5. Rung 3 — listings

- [ ] Official registry: server.json per registry.modelcontextprotocol.io spec; namespace proof via
      ief-global.org DNS/GitHub; validate + publish
- [ ] Smithery (`smithery mcp publish`) · mcp.so claim · Glama claim · PulseMCP (auto-crawl, verify)
- [ ] PR to awesome-mcp-servers; PR to narVidhai/tamil-nlp-catalog (top priority, same community)
- [ ] Demo: 2-min video or GIF (Claude analyzing மரத்தில் + கம்ப்யூட்டர்→கணினி with provenance shown);
      bilingual announcement post (Tamil first) — run prose through anti-AI writing rules
- [ ] Positioning wording check (D-003 exact claim)

## 6. Rung 4 — web tool

- [ ] FastAPI head on the same engine (GET /analyze?word=…, JSON = word-analysis object); OpenAPI on
- [ ] Cloudflare Pages page at ief-global.org/thamizh: input box → rendered analysis (Tamil-first UI,
      English toggle); cache-friendly GETs
- [ ] Same rate-limit/cache rules; monitor free-tier GB-seconds after launch week
