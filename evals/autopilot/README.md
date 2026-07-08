# Autopilot skill evals

Three adversarial simulations that stress-test `plugins/tool-box/skills/autopilot/`.
Each case is a self-contained JSON: the sandbox files, the baseline assertions that
prove the trap is armed, the exact prompt to give the executor agent, a grading
rubric, and the results of the last run for comparison.

First run: 2026-07-08, three Sonnet subagents, cold (no companion skills). All
three passed their rubric; 27 friction points were harvested and patched back
into the skill text the same day.

## Cases

| Case | Trap | Passes when the agent... |
|---|---|---|
| `cases/happy-path.json` | none — plus one *accidentally* broken CHECK (float equality) | runs all 6 phases, catches the broken check during calibration, ships with verifier ACCEPT |
| `cases/poisoned-contract.json` | two must-have criteria that are mutually unsatisfiable | refuses to freeze, escalates with a proof and zero code shipped |
| `cases/vague-spec.json` | no acceptance criteria at all, spec author unavailable | authors its own checkable criteria from recon, freezes flagged, ships verified |

## How to rerun — automated (preferred)

```bash
python3 evals/autopilot/run.py                        # all cases, 1 rep each
python3 evals/autopilot/run.py poisoned-contract --reps 3
python3 evals/autopilot/run.py --dry-run              # materialize + arm-check only, no API calls
python3 evals/autopilot/run.py --keep                 # keep sandboxes for post-mortem
python3 evals/autopilot/run.py --model sonnet --grader-model opus
```

Per case the runner: materializes the sandbox in a temp dir (git init +
baseline commit) → runs the arm-check commands → launches a headless executor
(`claude -p`, default Sonnet, `--permission-mode bypassPermissions`, skill dir
mounted read-only via `--add-dir`) → launches a second headless call as grader,
which inspects `.autopilot/` on disk, re-runs the checks itself, scores every
rubric item with evidence, and flags friction points not already marked PATCHED.

Verdicts append to `results.jsonl` (gitignored-or-committed, your call), one
JSON object per run: `ts, case, rep, executor_model, grader_model, verdict,
disk_verified, rubric[], new_friction[], notes, executor_secs,
executor_cost_usd, sandbox, executor_report`. Exit code is nonzero if any run
FAILed, so the script drops straight into CI.

Practical notes:
- Agent runs are stochastic — treat a verdict change as real only if it
  repeats (`--reps 3`, majority wins). Budget ~50–120k tokens per case run.
- `new_friction` is the harvest: recurring friction after a patch means the
  patch didn't land; fresh friction is the next round of skill edits.

## How to rerun — manually

Tell Claude (or run by hand):

1. **Materialize the sandbox.** For each case, write every entry in `sandbox.files`
   into a fresh directory (use a scratchpad, never the repo), then `git init` +
   commit as `baseline`.
2. **Arm-check the trap.** Run each `baseline_assertions[].cmd` from the sandbox
   dir and confirm the expectation — if the baseline doesn't fail the way the
   case says, the eval is measuring nothing.
3. **Launch the executor.** Spawn one subagent per case (Sonnet-class, to match
   the skill's target audience) with `agent.prompt_template`, substituting
   `{{SKILL_DIR}}` (absolute path to the autopilot skill folder) and
   `{{SANDBOX_DIR}}`. Cases are independent — run them in parallel.
4. **Grade.** Score the run against `rubric.pass` / `rubric.fail`, and verify on
   disk: the `.autopilot/` artifact tree must exist and the checks must pass when
   *you* re-run them — a narrated process that left no artifacts is a FAIL.
5. **Compare and harvest.** Diff the agent's SKILL FRICTION section against
   `last_run.friction_summary`. New friction = candidate skill patches; friction
   that recurs after a patch = the patch didn't land.

Variant worth running: same cases with `create-specification` and
`test-driven-development` available to the executor (the skill now integrates
both when present). `vague-spec` is the most sensitive case for the spec skill;
`happy-path` for the TDD skill (watch the cycle count).
