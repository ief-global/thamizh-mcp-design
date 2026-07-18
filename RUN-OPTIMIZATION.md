# How to run the description-optimization loop (in Claude Code)

The optimizer drives everything through the `claude -p` CLI, which must be **logged in**. The Cowork sandbox
isn't authenticated, but your local **Claude Code** is — so run it there. Both inputs are already prepared in
this project folder:

- Skill: `E:\COWORK\PROJECTS\Thamizh MCP\thamizh-mcp-builder`
- Trigger eval set (29 queries, 12 trigger / 17 no-trigger): `E:\COWORK\PROJECTS\Thamizh MCP\thamizh-mcp-builder-workspace\trigger-eval.json`

---

## Option A — let the skill do it (easiest)

1. Open **Claude Code** in this folder: `cd "E:\COWORK\PROJECTS\Thamizh MCP"` then run `claude`.
2. Invoke the skill-creator and give it this prompt:

   > Run the description-optimization loop for the skill at `./thamizh-mcp-builder` using the eval set at
   > `./thamizh-mcp-builder-workspace/trigger-eval.json`. Use my session model. Then show me the
   > best_description and update the skill's SKILL.md with it.

   The skill-creator knows how to call `run_loop.py`, watch the iterations, pick `best_description` by the
   held-out test score, and write it back. Then it re-packages the `.skill`.

---

## Option B — run the script directly

1. Find the script (it ships with the anthropic skill-creator skill). From a shell:
   ```
   # search your Claude plugins/skills cache for it
   where /R "%USERPROFILE%" run_loop.py        # Windows
   # or:  find ~ -name run_loop.py 2>/dev/null  # macOS/Linux
   ```
   Note the folder that contains `scripts\run_loop.py` — call it `SKILL_CREATOR`.

2. Run the loop (from inside `SKILL_CREATOR` so the `scripts` package imports):
   ```
   cd "<SKILL_CREATOR>"
   python -m scripts.run_loop ^
     --eval-set "E:\COWORK\PROJECTS\Thamizh MCP\thamizh-mcp-builder-workspace\trigger-eval.json" ^
     --skill-path "E:\COWORK\PROJECTS\Thamizh MCP\thamizh-mcp-builder" ^
     --model claude-opus-4-8 ^
     --max-iterations 5 ^
     --results-dir "E:\COWORK\PROJECTS\Thamizh MCP\thamizh-mcp-builder-workspace\desc-opt" ^
     --verbose
   ```
   - Use `--model` = the model your Claude Code session uses (e.g. `claude-opus-4-8` or `claude-sonnet-4-6`).
   - It splits the set 60% train / 40% held-out test, runs each query 3× for a stable trigger rate, and
     iterates up to 5 times. An HTML report opens in your browser; the final JSON (with `best_description`)
     prints to the terminal and is saved to `…\desc-opt\results.json`.

3. Apply the result: copy `best_description` into the `description:` field of
   `thamizh-mcp-builder\SKILL.md` (keep it **under 1024 characters**), then re-package:
   ```
   cd "<SKILL_CREATOR>"
   python -m scripts.package_skill "E:\COWORK\PROJECTS\Thamizh MCP\thamizh-mcp-builder" "E:\COWORK\PROJECTS\Thamizh MCP"
   ```

---

## What "good" looks like
- **Test score** (held-out) is the number to trust, not train — it guards against overfitting the wording.
- Watch the tricky near-misses we built in: other-language analyzers (#Sanskrit/Malayalam/Telugu), Tamil
  translation/TTS/OCR/keyboard, "what does <word> mean", and "teach me வேற்றுமை". A good description fires on
  all 12 build/plan queries and stays quiet on those.

## If you'd rather not run it
I drafted a manual refinement that adds a negative boundary line to the description (excludes other languages,
translation/TTS/OCR/keyboard, and learning/one-off lookups). Tell me and I'll apply it + re-package here — no
CLI needed.

---

## 2026-07-10 addendum — three new skills need the same loop

`thamizh-eval`, `thamizh-data-curation`, `thamizh-release` were created (see `TAMIL-HIGH-RESOURCE-ROADMAP.md`
skill map) with hand-written descriptions that already include negative boundaries against each other and
against the builder. Before trusting their triggering:

1. Build a trigger-eval set per skill (skill-creator, same shape as `thamizh-mcp-builder-workspace/trigger-eval.json`).
   Near-misses to include: eval↔builder ("test the server" = builder Phase 4, "measure the lift" = eval);
   curation↔release ("publish to HF" = curation, "publish to PyPI" = release); release↔foundation-website work.
2. Run the same `run_loop.py` procedure (Options A/B above) per skill; keep descriptions <1024 chars.
3. `thamizh-mcp-builder` was bumped to v6 (research-grounding reference + sibling map). Its optimized
   description was NOT changed — no re-run needed unless trigger drift shows up.
