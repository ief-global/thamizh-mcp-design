#!/usr/bin/env python3
"""Morphological-lift A/B harness (Claude-first).

Usage:
  python run_ab.py --fixtures fixtures/v1.jsonl --arm control --out results/
  python run_ab.py --fixtures fixtures/v1.jsonl --arm test --mcp-config assets/mcp.json --out results/
  python run_ab.py --score results/control.jsonl results/test.jsonl

Design notes (see SKILL.md):
- Model-agnostic storage; Claude-first execution via `claude -p --output-format json` (captures the
  answer text, token usage, and num_turns — a proxy for whether MCP tools were called).
- 3 runs per question per arm (use --runs to override; smoke runs use 1). Run control where thamizh-mcp
  is unreachable (a neutral cwd + no --mcp-config); the test arm attaches it via --mcp-config.
- Scoring: normalized exact match vs answer+alternatives; misses go to a review file for manual marking
  of linguistically-acceptable variants (Tamil often has several) — accepted variants merge to fixtures.
- Isolation: run from outside the project folder so no skill/reference files leak into context.
"""
import argparse, json, statistics, subprocess, sys, unicodedata
from collections import defaultdict
from pathlib import Path

PROMPT = ("பின்வரும் வினாவிற்குச் சுருக்கமாக விடையளிக்கவும். இறுதி விடையை மட்டும் "
          "'விடை:' என்ற முன்னொட்டுடன் ஒரே வரியில் தருக.\n\n{q}")

# Read-only thamizh tools the test arm may use (auto-approved so `-p` doesn't block on a prompt).
THAMIZH_TOOLS = ("mcp__thamizh__analyze_word,mcp__thamizh__classify_origin,mcp__thamizh__get_root,"
                 "mcp__thamizh__get_meaning,mcp__thamizh__explain_formation,mcp__thamizh__explain_grammar,"
                 "mcp__thamizh__suggest_native_equivalent")


def norm(s: str) -> str:
    s = unicodedata.normalize("NFC", s).strip().lower()
    return "".join(ch for ch in s if ch.isalnum() or 0x0B80 <= ord(ch) <= 0x0BFF)


def matches(got: str, fx: dict) -> bool:
    """Correct if a gold (answer or alternative) equals the response, or — for golds of >=3 chars —
    appears within it (handles short Tamil answers wrapped in a gloss, e.g. 'இல் (ஏழாம் வேற்றுமை உருபு)').
    Short/numeric golds require exact match to avoid spurious substring hits. Misses still go to review."""
    gn = norm(got)
    for g in [fx["answer"], *fx.get("alternatives", [])]:
        gg = norm(g)
        if gg and (gg == gn or (len(gg) >= 3 and gg in gn)):
            return True
    return False


def run_claude(question: str, mcp_config: str | None) -> dict:
    cmd = ["claude", "-p", PROMPT.format(q=question), "--output-format", "json"]
    if mcp_config:
        cmd += ["--mcp-config", mcp_config, "--allowedTools", THAMIZH_TOOLS]
    try:
        r = subprocess.run(cmd, capture_output=True, text=True, timeout=300)
        d = json.loads(r.stdout)
        u = d.get("usage", {}) or {}
        return {"text": (d.get("result") or "").strip(),
                "tokens": (u.get("input_tokens", 0) or 0) + (u.get("output_tokens", 0) or 0),
                "turns": d.get("num_turns", 1)}
    except Exception as e:                       # harness must survive a single bad call
        return {"text": f"<error: {e}>", "tokens": 0, "turns": 0}


def extract(resp: str) -> str:
    for line in reversed(resp.splitlines()):
        if "விடை" in line:
            return line.split(":", 1)[-1].strip()
    return resp.strip()


def _done_pairs(path: Path) -> set:
    """(id, run) pairs already recorded in an arm's jsonl — the resume checkpoint."""
    done = set()
    if path.exists():
        for line in path.read_text("utf-8").splitlines():
            if line.strip():
                r = json.loads(line)
                done.add((r["id"], r["run"]))
    return done


def run_arm(fixtures: list[dict], arm: str, mcp_config: str | None, out: Path, runs: int):
    """Resumable: each result is appended and flushed the instant it completes, and any (question,run)
    already present is skipped. Killing the run and re-invoking the same command continues from where
    it stopped — no completed work is ever redone."""
    out.mkdir(parents=True, exist_ok=True)
    path = out / f"{arm}.jsonl"
    done = _done_pairs(path)
    if done:
        print(f"resuming {arm}: {len(done)} (question,run) results already present — skipping them",
              file=sys.stderr)
    with path.open("a", encoding="utf-8") as fh:
        for fx in fixtures:
            for i in range(runs):
                if (fx["id"], i) in done:
                    continue
                res = run_claude(fx["question"], mcp_config if arm == "test" else None)
                got = extract(res["text"])
                row = {"id": fx["id"], "arm": arm, "run": i, "got": got, "auto_correct": matches(got, fx),
                       "used_tools": res["turns"] > 1, "tokens": res["tokens"],
                       "category": fx["category"], "grade": fx["grade"], "score": fx["score"]}
                fh.write(json.dumps(row, ensure_ascii=False) + "\n")
                fh.flush()
                print(f'{fx["id"]} run{i} {arm}: {"OK " if row["auto_correct"] else "MISS"} '
                      f'tools={row["used_tools"]} «{got[:40]}»', file=sys.stderr)
    rows = [json.loads(l) for l in path.read_text("utf-8").splitlines() if l.strip()]
    misses = [r for r in rows if not r["auto_correct"]]
    (out / f"{arm}.review.jsonl").write_text(
        "\n".join(json.dumps(r, ensure_ascii=False) for r in misses), "utf-8")
    print(f"\n{arm}: {sum(r['auto_correct'] for r in rows)}/{len(rows)} auto-correct; "
          f"{len(misses)} to review → {out}/{arm}.review.jsonl", file=sys.stderr)


def sp(rows, key=None, val=None):
    rows = [r for r in rows if key is None or r[key] == val]
    if not rows:
        return None
    per_q = defaultdict(list)
    for r in rows:
        per_q[r["id"]].append(r)
    got = sum(statistics.mean(1.0 if x["auto_correct"] else 0.0 for x in v) * v[0]["score"] for v in per_q.values())
    tot = sum(v[0]["score"] for v in per_q.values())
    return round(100 * got / tot, 2)


def _toks(rows):
    t = [r["tokens"] for r in rows if r["tokens"]]
    return round(statistics.median(t)) if t else 0


def score(control_f: str, test_f: str):
    c = [json.loads(l) for l in Path(control_f).read_text("utf-8").splitlines() if l]
    t = [json.loads(l) for l in Path(test_f).read_text("utf-8").splitlines() if l]
    print(f"{'':13} {'control':>8} {'test':>8} {'lift':>8}")
    print(f"{'OVERALL':13} {sp(c):>8} {sp(t):>8} {round(sp(t)-sp(c),2):>8}")
    for cat in sorted({r["category"] for r in c}):
        cc, tt = sp(c, "category", cat), sp(t, "category", cat)
        lift = round((tt or 0) - (cc or 0), 2)
        print(f"{cat:13} {str(cc):>8} {str(tt):>8} {str(lift):>8}")
    tool_rate = round(100 * sum(r["used_tools"] for r in t) / len(t), 1) if t else 0
    print(f"\ntest-arm tool-call rate: {tool_rate}%  |  median tokens/q  control={_toks(c)}  test={_toks(t)}")


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--fixtures"); ap.add_argument("--arm", choices=["control", "test"])
    ap.add_argument("--mcp-config"); ap.add_argument("--out", default="results")
    ap.add_argument("--runs", type=int, default=3); ap.add_argument("--score", nargs=2)
    a = ap.parse_args()
    if a.score:
        score(*a.score)
    else:
        fx = [json.loads(l) for l in Path(a.fixtures).read_text("utf-8").splitlines() if l]
        run_arm(fx, a.arm, a.mcp_config, Path(a.out), a.runs)
