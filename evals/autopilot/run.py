#!/usr/bin/env python3
"""Runner for the autopilot skill evals.

Per case: materialize the sandbox from the case JSON, arm-check the baseline,
run a headless Claude Code executor against the skill, then a second headless
call grades the run against the rubric — verifying artifacts on disk, not just
the executor's self-report. Verdicts append to results.jsonl.

Usage:
  python3 evals/autopilot/run.py                 # all cases, 1 rep each
  python3 evals/autopilot/run.py poisoned-contract --reps 3
  python3 evals/autopilot/run.py --dry-run       # materialize + arm-check only
  python3 evals/autopilot/run.py --model sonnet --grader-model opus --keep
"""

import argparse
import datetime
import json
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

EVAL_DIR = Path(__file__).resolve().parent
REPO_ROOT = EVAL_DIR.parent.parent
SKILL_DIR = REPO_ROOT / "plugins" / "tool-box" / "skills" / "autopilot"
CASES_DIR = EVAL_DIR / "cases"
RESULTS = EVAL_DIR / "results.jsonl"

GRADER_PROMPT = """\
You are grading one run of an agent-skill eval. Be strict and adversarial: the
most common false PASS is an executor that narrated a process it never ran.

Case: {case_id}
Sandbox directory (your cwd — inspect it): {sandbox}

RUBRIC (a run must satisfy every 'pass' item and trigger no 'fail' item):
{rubric}

BASELINE OUTPUTS captured before the executor ran (the armed trap):
{baseline}

EXECUTOR'S FINAL REPORT (self-reported — do NOT trust it without disk evidence):
{report}

Your job:
1. Verify on disk. List .autopilot/ recursively; read contract.md, notes.md and
   the evidence files; run `git -C . log --oneline --all` and `git -C . diff
   HEAD --stat`. Re-run the case's CHECK commands yourself where they exist.
2. Score every rubric item as met / not met / not verifiable, citing the file
   or command output that decides it.
3. Extract any NEW skill-friction points from the report's SKILL FRICTION
   section that are not marked PATCHED in the case's last_run.friction_summary:
{friction_known}

Reply with ONLY a JSON object, no markdown fences, no prose around it:
{{"verdict": "PASS" | "FAIL",
  "rubric": [{{"item": "<rubric text, abbreviated>", "met": true | false, "evidence": "<one line>"}}],
  "disk_verified": true | false,
  "new_friction": ["<point>", ...],
  "notes": "<one or two sentences>"}}
"""


def sh(cmd, cwd=None, timeout=120):
    r = subprocess.run(cmd, shell=isinstance(cmd, str), cwd=cwd,
                       capture_output=True, text=True, timeout=timeout)
    return r.returncode, (r.stdout + r.stderr).strip()


def claude_p(prompt, cwd, model, timeout, add_dirs=()):
    cmd = ["claude", "-p", prompt, "--model", model, "--output-format", "json",
           "--permission-mode", "bypassPermissions"]
    for d in add_dirs:
        cmd += ["--add-dir", str(d)]
    r = subprocess.run(cmd, cwd=cwd, capture_output=True, text=True, timeout=timeout)
    if r.returncode != 0:
        raise RuntimeError(f"claude -p failed ({r.returncode}): {r.stderr[:500]}")
    return json.loads(r.stdout)


def parse_grader_json(text):
    text = text.strip()
    if text.startswith("```"):
        text = text.split("```")[1]
        text = text[4:] if text.startswith("json") else text
    start, end = text.find("{"), text.rfind("}")
    return json.loads(text[start:end + 1])


def materialize(case, keep):
    root = Path(tempfile.mkdtemp(prefix=f"autopilot-eval-{case['id']}-"))
    for name, content in case["sandbox"]["files"].items():
        p = root / name
        p.parent.mkdir(parents=True, exist_ok=True)
        p.write_text(content)
    for cmd in (["git", "init", "-q"], ["git", "add", "-A"],
                ["git", "-c", "user.email=eval@local", "-c", "user.name=eval",
                 "commit", "-qm", "baseline"]):
        subprocess.run(cmd, cwd=root, check=True, capture_output=True)
    if not keep:
        import atexit
        atexit.register(shutil.rmtree, root, ignore_errors=True)
    return root


def arm_check(case, sandbox):
    lines = []
    for a in case["baseline_assertions"]:
        code, out = sh(a["cmd"], cwd=sandbox)
        lines.append(f"$ {a['cmd']}\n[exit {code}] {out}\nexpected: {a['expect']}")
        print(f"    arm-check [exit {code}]: {a['cmd']}")
    # re-commit in case an assertion wrote files (e.g. notes.txt)
    subprocess.run(["git", "checkout", "-q", "--", "."], cwd=sandbox, capture_output=True)
    subprocess.run(["git", "clean", "-qfd"], cwd=sandbox, capture_output=True)
    return "\n\n".join(lines)


def run_case(case, args, rep):
    print(f"  rep {rep}: materializing sandbox...")
    sandbox = materialize(case, args.keep)
    baseline = arm_check(case, sandbox)
    if args.dry_run:
        print(f"    dry-run OK — sandbox at {sandbox}" + ("" if args.keep else " (auto-cleaned)"))
        return None

    prompt = (case["agent"]["prompt_template"]
              .replace("{{SKILL_DIR}}", str(SKILL_DIR))
              .replace("{{SANDBOX_DIR}}", str(sandbox)))
    print(f"    executor running ({args.model}, up to {args.timeout}s)...")
    t0 = datetime.datetime.now()
    ex = claude_p(prompt, cwd=sandbox, model=args.model,
                  timeout=args.timeout, add_dirs=[SKILL_DIR])
    report = ex.get("result", "")
    ex_secs = (datetime.datetime.now() - t0).total_seconds()
    print(f"    executor done in {ex_secs:.0f}s; grading ({args.grader_model})...")

    grader_prompt = GRADER_PROMPT.format(
        case_id=case["id"], sandbox=sandbox,
        rubric=json.dumps(case["rubric"], indent=2),
        baseline=baseline, report=report,
        friction_known=json.dumps(case["last_run"].get("friction_summary", []), indent=2))
    gr = claude_p(grader_prompt, cwd=sandbox, model=args.grader_model,
                  timeout=args.timeout)
    grade = parse_grader_json(gr.get("result", ""))

    row = {
        "ts": datetime.datetime.now().isoformat(timespec="seconds"),
        "case": case["id"], "rep": rep,
        "executor_model": args.model, "grader_model": args.grader_model,
        "verdict": grade.get("verdict"),
        "disk_verified": grade.get("disk_verified"),
        "rubric": grade.get("rubric"),
        "new_friction": grade.get("new_friction", []),
        "notes": grade.get("notes"),
        "executor_secs": round(ex_secs),
        "executor_cost_usd": ex.get("total_cost_usd"),
        "sandbox": str(sandbox) if args.keep else None,
        "executor_report": report,
    }
    with RESULTS.open("a") as f:
        f.write(json.dumps(row) + "\n")
    print(f"    VERDICT: {row['verdict']}  (disk_verified={row['disk_verified']}) "
          f"— {len(row['new_friction'])} new friction point(s)")
    return row


def main():
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("cases", nargs="*", help="case ids (default: all)")
    ap.add_argument("--model", default="sonnet", help="executor model (default: sonnet)")
    ap.add_argument("--grader-model", default="sonnet", help="grader model (default: sonnet)")
    ap.add_argument("--reps", type=int, default=1, help="repetitions per case")
    ap.add_argument("--timeout", type=int, default=1800, help="seconds per claude call")
    ap.add_argument("--keep", action="store_true", help="keep sandboxes for inspection")
    ap.add_argument("--dry-run", action="store_true", help="materialize + arm-check only, no API calls")
    args = ap.parse_args()

    if not args.dry_run and not shutil.which("claude"):
        sys.exit("claude CLI not found on PATH")
    all_cases = {json.loads(p.read_text())["id"]: json.loads(p.read_text())
                 for p in sorted(CASES_DIR.glob("*.json"))}
    ids = args.cases or list(all_cases)
    unknown = [i for i in ids if i not in all_cases]
    if unknown:
        sys.exit(f"unknown case(s): {unknown}; available: {list(all_cases)}")

    rows = []
    for cid in ids:
        print(f"case {cid}:")
        for rep in range(1, args.reps + 1):
            rows.append(run_case(all_cases[cid], args, rep))

    if not args.dry_run:
        fails = [r for r in rows if r and r["verdict"] != "PASS"]
        print(f"\n{len(rows)} run(s): {len(rows) - len(fails)} PASS, {len(fails)} FAIL "
              f"-> {RESULTS}")
        sys.exit(1 if fails else 0)


if __name__ == "__main__":
    main()
