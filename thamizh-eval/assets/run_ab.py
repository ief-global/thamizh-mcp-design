#!/usr/bin/env python3
"""Morphological-lift A/B harness (Claude-first sketch).

Usage:
  python run_ab.py --fixtures fixtures/v1.jsonl --arm control --out results/
  python run_ab.py --fixtures fixtures/v1.jsonl --arm test --mcp-config mcp.json --out results/
  python run_ab.py --score results/control.jsonl results/test.jsonl

Design notes (see SKILL.md):
- Model-agnostic storage; Claude-first execution via `claude -p`. Add other runners as functions.
- 3 runs per question per arm; run control where thamizh-mcp is unreachable.
- Scoring: normalized exact match vs answer+alternatives; misses go to manual review
  (write review file, human marks acceptable -> merged back into fixtures).
"""
import argparse, json, statistics, subprocess, sys, unicodedata
from collections import defaultdict
from pathlib import Path

RUNS = 3
PROMPT = ("பின்வரும் வினாவிற்கு சுருக்கமாக விடையளிக்கவும். இறுதி விடையை மட்டும் "
          "'விடை:' என்ற முன்னொட்டுடன் தருக.\n\n{q}")

def norm(s: str) -> str:
    s = unicodedata.normalize("NFC", s).strip().lower()
    return "".join(ch for ch in s if ch.isalnum() or 0x0B80 <= ord(ch) <= 0x0BFF)

def run_claude(question: str, mcp_config: str | None) -> str:
    cmd = ["claude", "-p", PROMPT.format(q=question), "--output-format", "text"]
    if mcp_config:
        cmd += ["--mcp-config", mcp_config]  # test arm: thamizh-mcp attached
    r = subprocess.run(cmd, capture_output=True, text=True, timeout=300)
    return r.stdout.strip()

def extract(resp: str) -> str:
    for line in reversed(resp.splitlines()):
        if "விடை" in line:
            return line.split(":", 1)[-1].strip()
    return resp.strip()

def run_arm(fixtures: list[dict], arm: str, mcp_config: str | None, out: Path):
    rows = []
    for fx in fixtures:
        for i in range(RUNS):
            resp = run_claude(fx["question"], mcp_config if arm == "test" else None)
            got = extract(resp)
            ok = norm(got) == norm(fx["answer"]) or any(norm(got) == norm(a) for a in fx.get("alternatives", []))
            rows.append({"id": fx["id"], "arm": arm, "run": i, "got": got, "auto_correct": ok,
                         "category": fx["category"], "grade": fx["grade"], "score": fx["score"]})
            print(f'{fx["id"]} run{i} {arm}: {"OK" if ok else "MISS"}', file=sys.stderr)
    out.mkdir(parents=True, exist_ok=True)
    (out / f"{arm}.jsonl").write_text("\n".join(json.dumps(r, ensure_ascii=False) for r in rows), "utf-8")
    misses = [r for r in rows if not r["auto_correct"]]
    (out / f"{arm}.review.jsonl").write_text(  # human marks {"accepted": true} + merge to fixtures
        "\n".join(json.dumps(r, ensure_ascii=False) for r in misses), "utf-8")

def sp(rows, key=None, val=None):
    rows = [r for r in rows if key is None or r[key] == val]
    if not rows: return None
    per_q = defaultdict(list)
    for r in rows: per_q[r["id"]].append(r)
    got = sum(statistics.mean(1.0 if x["auto_correct"] else 0.0 for x in v) * v[0]["score"] for v in per_q.values())
    tot = sum(v[0]["score"] for v in per_q.values())
    return round(100 * got / tot, 2)

def score(control_f: str, test_f: str):
    c = [json.loads(l) for l in Path(control_f).read_text("utf-8").splitlines() if l]
    t = [json.loads(l) for l in Path(test_f).read_text("utf-8").splitlines() if l]
    print(f'overall  control={sp(c)}  test={sp(t)}  lift={round(sp(t)-sp(c),2)}')
    for cat in sorted({r["category"] for r in c}):
        print(f'{cat}  control={sp(c,"category",cat)}  test={sp(t,"category",cat)}')

if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--fixtures"); ap.add_argument("--arm", choices=["control", "test"])
    ap.add_argument("--mcp-config"); ap.add_argument("--out", default="results")
    ap.add_argument("--score", nargs=2)
    a = ap.parse_args()
    if a.score: score(*a.score)
    else:
        fx = [json.loads(l) for l in Path(a.fixtures).read_text("utf-8").splitlines() if l]
        run_arm(fx, a.arm, a.mcp_config, Path(a.out))
