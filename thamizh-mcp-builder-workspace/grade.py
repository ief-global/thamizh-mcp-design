#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import json, re, os

BASE = os.path.join(os.path.dirname(os.path.abspath(__file__)), "iteration-1")

EVALS = {
  1: {
    "name": "planning-blueprint",
    "prompt": "Start the THAMIZH MCP project's planning phase and produce a sign-off-ready blueprint covering origin, root+meaning, formation, grammar.",
    "file": "blueprint.md",
    "assertions": [
      ("Names ThamizhiMorph as a grounding source", ["ThamizhiMorph"]),
      ("Maps fields to specific authentic sources (analyser + lexicon + classical grammar)", ["ThamizhiMorph", r"(?i)lexicon", r"(?i)tholkappiyam|nann"]),
      ("Uses Tholkappiyam's native/borrowed word classes", ["இயற்சொல்", "வடசொல்"]),
      ("Recommends a concrete stack (Python / FastMCP)", [r"(?i)python", r"(?i)fastmcp|stdio"]),
      ("Has sign-off-ready structure (scope + eval/test plan)", [r"(?i)scope", r"(?i)sign-?off|eval|test"]),
    ],
  },
  2: {
    "name": "word-walkthrough-marathil",
    "prompt": "Walk through how the server analyzes மரத்தில் — what each tool returns and which authentic source grounds each part.",
    "file": "walkthrough.md",
    "assertions": [
      ("Decomposes மரத்தில் into பகுதி + சாரியை + விகுதி", ["பகுதி", "சாரியை", "விகுதி"]),
      ("Identifies the locative case", [r"(?i)ஏழாம்|locative"]),
      ("Attributes root/formation to ThamizhiMorph", ["ThamizhiMorph"]),
      ("Surfaces the 5th/7th (ablative/locative) ambiguity", [r"(?i)ablative|ஐந்தாம்|ambigu"]),
      ("Classifies origin as இயற்சொல் (native Tamil)", ["இயற்சொல்"]),
      ("Names a standard lexicon for meaning", [r"(?i)lexicon"]),
    ],
  },
  3: {
    "name": "stack-and-grounding",
    "prompt": "Which language and which specific sources for a grounded Tamil word-analysis MCP, and how to avoid hallucinating grammar?",
    "file": "recommendation.md",
    "assertions": [
      ("Recommends Python", [r"(?i)python"]),
      ("Names ThamizhiMorph and a standard Tamil lexicon", ["ThamizhiMorph", r"(?i)lexicon"]),
      ("Anti-hallucination via provenance/citation + honest gaps", [r"(?i)provenance|citation|source", r"(?i)not found|no entry|gap|honest"]),
      ("Returns all analyses for ambiguous forms", [r"(?i)ambigu"]),
    ],
  },
}

CONFIGS = ["with_skill", "without_skill"]


def check(text, patterns):
    missing = [p for p in patterns if not re.search(p, text)]
    return (len(missing) == 0, missing)


def write_json(path, obj):
    f = open(path, "w", encoding="utf-8")
    json.dump(obj, f, ensure_ascii=False, indent=2)
    f.close()


summary = {}
for eid, ev in EVALS.items():
    for cfg in CONFIGS:
        cfg_dir = os.path.join(BASE, "eval-%d" % eid, cfg)
        run_dir = os.path.join(cfg_dir, "run-1")
        out = os.path.join(run_dir, "outputs", ev["file"])
        text = ""
        if os.path.exists(out):
            text = open(out, encoding="utf-8").read()
        exps = []
        for (atext, patterns) in ev["assertions"]:
            passed, missing = check(text, patterns)
            evidence = "all patterns matched" if passed else "missing: " + ", ".join(missing)
            exps.append({"text": atext, "passed": passed, "evidence": evidence})
        n_pass = sum(1 for e in exps if e["passed"])
        n_tot = len(exps)
        grading = {"eval_id": eid, "config": cfg, "expectations": exps,
                   "summary": {"pass_rate": round(n_pass / n_tot, 4) if n_tot else 0.0,
                               "passed": n_pass, "failed": n_tot - n_pass, "total": n_tot}}
        write_json(os.path.join(run_dir, "grading.json"), grading)
        meta = {"eval_id": eid, "eval_name": ev["name"], "prompt": ev["prompt"],
                "assertions": [a[0] for a in ev["assertions"]]}
        write_json(os.path.join(cfg_dir, "eval_metadata.json"), meta)
        write_json(os.path.join(run_dir, "eval_metadata.json"), meta)
        summary["eval-%d/%s" % (eid, cfg)] = "%d/%d" % (n_pass, n_tot)

print(json.dumps(summary, indent=2, ensure_ascii=False))
