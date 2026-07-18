# Thamizh MCP — Hosting Plan (IEF / ief-global.org)

> Living doc. Created 2026-06-28. Companion to `distribution-roadmap.md` (that file = how to publish for adoption; this file = how/where to actually host the service). For IEF (International Educational Foundation Inc.), an existing nonprofit that owns ief-global.org (domain + site on Cloudflare, free plan) and now has **Google for Nonprofits** (Workspace) status. Goal: free public service, minimal cost + minimal volunteer maintenance. Update as decisions firm up.

## TL;DR recommendation

Front-end on **Cloudflare Pages** (free, uses the domain you already own) + back-end engine on **Google Cloud Run** (scale-to-zero, real free tier, runs your Docker image) + **Cloudflare edge** (cache + rate-limit) in front. At your scale this is plausibly **$0/month**, with **up to $10k/yr Google nonprofit credits** as a backstop. This is a clean layered "hybrid," NOT risky multi-cloud.

## The hard constraint (don't fight it)

Cloudflare **Workers cannot run native binaries or heavy Python** — only JS/WASM. Your engine needs `flookup`/foma (native C binary) and (optionally) Stanza (PyTorch). So the **form page is easy on Cloudflare, but the engine needs a real Linux container** somewhere. Everything below follows from this.

## Recommended architecture (one edge, one backend)

- **Front-end page** — `ief-global.org/thamizh` (or a subdomain) on **Cloudflare Pages** (free). Static page +  form; calls the API.
- **Edge layer** — **Cloudflare** (already in place): DNS, CDN, **caching** (huge — repeated word lookups
  served free at the edge), **rate-limiting** (caps abuse + cost), WAF.
- **Back-end engine** — **Google Cloud Run**: your Docker image (Python + foma + lexicon + knowledge store),
  exposed at `api.ief-global.org`. Cloudflare proxies that subdomain to the Cloud Run URL.
- **Seam:** Cloudflare → Cloud Run is a single, well-defined hop. One-time config: Cloud Run custom-domain
  mapping behind Cloudflare's proxy, SSL mode = **Full**. ~15 min, then done.

## Why Cloud Run (vs Cloudflare Containers)

| | Google Cloud Run | Cloudflare Containers |
|---|---|---|
| Runs your Docker image (foma/Python) | Yes | Yes |
| Scale-to-zero, no idle charge | Yes | Yes (sleeps after timeout) |
| Real always-free tier | **2M requests/mo + compute allowances** | No free tier; needs Workers Paid $5/mo base |
| Nonprofit credits available | **Up to $10k/yr (Google for Nonprofits)** | CF nonprofit credit program (recurs; last window closed Dec 2025) |
| Fit for IEF right now | **Best** — you already have the nonprofit status | Viable, but no free tier |

→ For IEF, Cloud Run wins because of the free tier **plus** the nonprofit credits you can already access.

## Cost picture
- **Front-end:** $0 (Cloudflare Pages, free plan).
- **Edge:** $0 (Cloudflare free plan; caching/rate-limit included).
- **Back-end:** likely **$0** — a word-lookup service should fit inside Cloud Run's free tier; scale-to-zero means no idle charge. **$10k/yr Google nonprofit credits** cover any overflow or a pinned warm instance.
- **The real cost is volunteer maintenance time**, not dollars. Cloud Run minimizes it (managed, no server to patch) vs a VPS.
- **Cost levers:** cache hard at the edge; rate-limit; **trim Stanza** on the single-word path (lean on
  ThamizhiMorph + light POS) to stay within the free tier's memory-time (GB-seconds) and cut cold-starts.

## Is the hybrid too complex?

No — it's standard layering: each provider does its best thing, meeting at one seam (Cloudflare → Cloud Run).
**Guardrail to keep it simple:** ONE backend host (Cloud Run) + Cloudflare as the edge you already own. Do **not** also run a second backend on Cloudflare Containers, and do **not** split data/state across clouds — that's what would turn "hybrid" into real complexity. Cold-start note: first request after idle is slow; pin one warm instance (min-instances=1) if you want snappiness — nonprofit credits easily absorb that.

## Self-host vs hosted (adoption model)

Most end users want a free click-to-use service, not to self-host. So: **IEF hosts one reference instance** (small, cached, rate-limited) as a free public good = the adoption driver; **also ship the Docker image + docs** so universities/other orgs can self-host = sustainability + an exit if IEF ever stops hosting.

## Nonprofit credit programs to activate / watch

- **Google for Nonprofits → Google Cloud credits**: up to **$10,000/yr** for compute/hosting/databases.
  You already have the nonprofit status (Workspace) — activate the Cloud product to get the credits.
- **Cloudflare for Nonprofits credits**: up to $250k credits program (last application window closed
  2026-... i.e. Dec 1, 2025); recurs — watch for the next class.
- **Cloudflare Project Galileo**: free security for qualifying civil-society orgs (education not explicitly
  listed — check eligibility, don't assume).

## Open decisions (fill in as we go)

- Pin a warm Cloud Run instance (snappy, uses credits) vs pure scale-to-zero (free, cold-starts)?
- Drop Stanza on the single-word path to stay in the free tier? (recommended)
- Front-end: keep on Cloudflare Pages vs Firebase Hosting (all-Google)? (Cloudflare Pages is fine + free)
- Subdomain name for the API (api.ief-global.org? thamizh.ief-global.org?).
- Activate Google Cloud credits now or when the engine is build-ready?
- (add more here)

## Sources (2026-06-28)

- Cloudflare Workers — no native binaries (JS/WASM only): https://developers.cloudflare.com/workers/reference/security-model/
- Cloudflare Containers overview + pricing: https://developers.cloudflare.com/containers/ , https://developers.cloudflare.com/containers/pricing/
- Google for Nonprofits — Google Cloud credits: https://support.google.com/nonprofits/answer/16245748
- Google Cloud Run pricing + free tier (scale-to-zero, 2M req/mo): https://cloud.google.com/run/pricing
- Cloudflare Project Galileo: https://www.cloudflare.com/galileo/
