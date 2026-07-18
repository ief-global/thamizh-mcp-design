# Thamizh MCP — Distribution Roadmap

> Living doc. Created 2026-06-28. Captures how to publish/distribute the Thamizh MCP server once it's built,
> tested, and ready. Goal: wide adoption, **not** monetization. Update as decisions firm up and questions come in.
>
> **See also:** `thamizh-mcp-hosting-plan.md` — concrete hosting plan for IEF (Cloudflare edge + Google Cloud Run backend, costs, nonprofit credits).

## Core mental model (read this first)

An MCP server is **not** a product end-users touch — it's an adapter that lets AI assistants (Claude, Cursor,
etc.) call your logic. So don't treat "the MCP server" as the thing you distribute. Treat it as **one of
several thin "heads" on a single reusable core.**

- Build the analysis engine **once** as a plain Python library — `analyze_word(word) -> WordAnalysis` — holding
  the foma/ThamizhiMorph calls, lexicon lookups, knowledge store, and Tholkappiyam authority logic.
- Then add thin adapters on top: an **MCP server** (AI tools), a **REST API** (apps + websites), maybe a **CLI**.
- Decide this in Phase 3. If the logic is baked *into* the MCP server, every other channel below means a painful
  refactor. If it's a clean core, all three channels become cheap.

---

## 1. Publishing the MCP server (for adoption)

Two separate jobs: make it **runnable**, and make it **discoverable**.

**Runnable**
- Open-source the repo on GitHub.
- Package so people install without cloning: publish to **PyPI** (`pip` / `uvx`), and optionally ship a
  **Docker image** (GHCR or Docker Hub). Most MCP clients add a server by pointing at a `pip`/`uvx`/`docker`
  command, so these two cover almost everyone.

**Discoverable — list in multiple registries (audiences barely overlap):**
- **Official MCP Registry** (`registry.modelcontextprotocol.io`) — publish a `server.json` under a name you
  prove you own; many clients read this feed.
- **mcp.so**, **Smithery**, **Glama**, **PulseMCP** — browse-able discovery directories. Smithery has a
  `smithery mcp publish` step; the others largely crawl and let you claim your listing.
- **`awesome-mcp-servers`** (GitHub list) — still a real discovery surface.

**Your niche's highest-leverage channel — the Tamil-NLP community:**
- Add the project to **`tamil-nlp-catalog`** (narVidhai) — the same catalog you source from.
- Post in Tamil developer / linguistics communities; a short write-up or demo video helps.
- If you produce trained models or cleaned datasets, host them on **Hugging Face** (a discovery channel itself).

**⚠️ Do a license / data audit BEFORE any public release (this gates everything):**
Your own code can be MIT/Apache, but you stand on others' data with different terms:
- **ThamizhiMorph** — Apache-2.0; just attribute (see session-state memory for the citation).
- **Madras Tamil Lexicon, AU-KBC WordNet, Kaggle loanword sets** — each has its own terms.
- **Tamil Wiktionary — CC BY-SA (share-alike / copyleft)** — the sharpest one: redistributing or *serving* its
  content carries obligations. Calling a source live at query time vs. bundling its data are very different
  legally. Sort this early.

**Hosting note:** a server others self-run costs you nothing. A *hosted/remote* MCP endpoint costs you hosting.

---

## 2. Mobile apps (Android / iOS)

Feasible, but you ship a **thin app over a hosted backend**, not the MCP server.
- **Why not on-device:** foma/`flookup` is a native C binary, Stanza is heavy, and the lexicon + web-enrichment
  layer wants a server. On-device (especially iOS) is impractical. Realistic shape: *app → your REST API → core
  engine*. The phone sends a word, renders the JSON analysis.
- **Build:** native (Kotlin/Swift) or cross-platform (**Flutter** / **React Native**) for one codebase, both stores.
- **Publish:** Apple Developer Program (~$99/yr) + Google Play (~$25 one-time); both review apps. "Free" is fine,
  but you still pay the dev fees **plus** backend hosting.
- **Offline app** = a much larger, later project (on-device FST subset + packaged dictionary).

---

## 3. Web integration

**Easiest path and best for reaching ordinary Tamil speakers** (most will never install an AI client or app).
- Expose the core as a **REST API** — **FastAPI** pairs naturally with the Python/FastMCP stack, and you can
  serve the MCP endpoint and the REST endpoint from the **same codebase**.
- Front-end options once the HTTP API exists: your own **"Tamil word analyzer" web page**; an **embeddable
  widget / iframe** other Tamil sites drop in; a **browser extension** (highlight a Tamil word → popup
  analysis); integration into existing dictionary / language-learning sites. All call the one API.

---

## Recommended sequencing (adoption, no monetization)

1. Build the clean **core engine** (Phase 3).
2. Add the **MCP server** (already in progress).
3. Add a small **FastAPI REST** layer (same codebase).
4. Stand up a simple public **web tool** — fastest route to real end-users.
5. **List** across the MCP registries + the Tamil-NLP catalog.
6. **Mobile** last.

**Cost & adoption model to decide up front:** self-hostable + open-source keeps *your* cost at zero (others run
it). A hosted API / web tool / mobile backend is what costs money even when it's free to users. Choose which
model you want before building the hosting in.

---

## Open questions / decisions (fill in as we go)
- License model for your own code? (MIT vs Apache-2.0)
- Hosting: self-host VPS vs serverless vs free tier vs grant/community funding?
- Web Wiktionary data — call live (lower legal risk) vs cache/serve (CC BY-SA obligations)?
- Which front-end first: standalone web tool, widget, or browser extension?
- (add more here)

## Sources (2026-06-28)
- Official MCP Registry — https://registry.modelcontextprotocol.io/
- Listing on MCP Registry / Smithery / Glama / PulseMCP (Tallyfy) — https://tallyfy.com/how-to-list-mcp-server-registry-smithery-glama-pulsemcp/
- MCP Registries in 2026: where to list (RoxyAPI) — https://roxyapi.com/blogs/mcp-registries-where-to-list-your-server
