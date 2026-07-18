# THAMIZH MCP — Continuous-Improvement Loop

A small, repeatable process for turning good discussions into durable project improvement as understanding
grows. The aim is that no useful insight is lost and no insight lands in the wrong place.

## The routing rule (where does an insight go?)

After any substantive discussion, sort each takeaway into exactly one destination:

1. **A decision or fact about *this specific build*** → `DECISIONS.md` (and, if it changes the spec, the
   blueprint). Examples: choice of stack, "wrap ThamizhiMorph," positioning claims.
2. **Reusable procedure or domain knowledge Claude should apply automatically** → update the *existing*
   `thamizh-mcp-builder` skill's reference files (`sources.md`, `tool-design.md`, `tamil-grammar.md`).
   Examples: a component→tool map, a new authoritative source, a grammar rule clarification.
3. **A genuinely separate capability that would trigger on its own** → only then, a *new* skill. Rare. A
   second skill overlapping the existing one causes trigger confusion, so default to enriching what exists.
4. **Neither durable nor reusable** → let it go. Not everything needs to be written down.

Quick test: *"Would a fresh session need this to do the job well?"* Yes → skill reference. *"Is this a choice
we made?"* Yes → decision log. Both can be true.

## The triage step (do this each session)

A 30-second pass at the end of a working discussion:

- Name each takeaway in one line.
- Route it with the rule above.
- Write it where it belongs *now*, while context is fresh — deferred capture is lost capture.

## Decision-log discipline

- Append-only. Never rewrite history; supersede with a new entry and flip the old **Status** line.
- Every entry carries a rationale, not just the decision — the *why* is what future-you needs.
- Link each entry to the doc/reference it affects, so a decision and its implementation stay connected.

## Skill versioning

- The skill is versioned (currently v3). When a reference file changes materially, bump the version in the
  skill's front-matter `license`/notes line and state what the bump added.
- Keep the change legible: "v4 — adds Thamizhi component→tool map to tool-design.md."

## Eval-driven hardening (from Phase 4 onward)

- When an eval fails, fix the *reference*, not just the one answer — encode the correction so it generalizes.
- Add the failing word/case to the eval set so the regression is caught next time.
- Prefer hardening against *real* observed failures over imagined ones; it keeps the skill lean.

## Roles at a glance

| Artifact | Holds | Changes when |
|---|---|---|
| `blueprint` (Phase 0) | what we're building + why | scope/spec decisions |
| `DECISIONS.md` | the choices + rationale, over time | any decision is made or reversed |
| skill `references/*` | reusable how-to + authoritative facts | procedure or domain knowledge improves |
| eval set | proof the server stays honest | a new failure mode is found |
| `IMPROVEMENT-LOOP.md` (this doc) | the process itself | the process itself improves |
