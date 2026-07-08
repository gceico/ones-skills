# Autopilot templates

Copy these verbatim and fill the blanks. Don't improvise formats — the value of a
fixed format is that a later phase (or a later run) can parse it without guessing.

---

## contract.md

```markdown
# Run contract · <task-slug>
Frozen: <yes/no — set to yes at the end of Phase 1 and never back>
User confirmed: <yes / no — froze autonomously, flagged in final report>

## Goal (outcome, not activity)
<one or two sentences describing the state of the world when this is done>

## Scope
<what you will touch>

## Non-goals
<what you deliberately will not touch, even if tempting>

## Assumptions (unconfirmed — flagged to the user in the final report)
- A1: <assumption> — conservative option chosen: <what you'll do>

## Acceptance criteria (FROZEN — see rule 2)
- AC1: <verifiable statement>
  CHECK: <exact command, or exact observation with expected result>
- AC2: ...

## Budgets
Build cycles: <n, default 5> · Verify rounds: <n, default 3> · Other: <wall-clock/cost if user gave any>

## Escalation triggers
<copied from SKILL.md Escalation section, plus any task-specific ones>

## Evidence to deliver
<the exact files that will prove done: test output, screenshots, verifier report>
```

---

## Cycle log (in notes.md)

One line per build cycle, written only AFTER the cycle's CHECK run — never
pre-filled. The `<n>/<budget>` header is your budget counter. If your hypothesis
for cycle N reads like cycle N-1's with "again" appended, rule 5 applies — write
a genuinely different one first.

```
CYCLE <n>/<budget> · hypothesis: <what you believe is wrong/needed and why>
  change: <what you actually did> · check: <which ACs run> · result: <PASS/FAIL + one-line detail>
  next: <continue / new hypothesis because same check failed twice / escalate>
```

---

## Verifier subagent prompt

Fill the two blanks only. Do not add context, do not summarize your work for the
verifier, do not include your notes — the whole point is that it grades blind.
Blank 1 is paths plus how to run, nothing more. Blank 2 is the numbered criteria
and their CHECK lines only — strip any annotations, calibration notes, or
parentheticals the contract's criteria section carries.

```
You are an independent verifier. You have no prior context about how this work was
done, and you must not ask for any.

You receive two inputs:
1. The artifact: <branch name / diff / list of file paths, and how to run the project>
2. The frozen acceptance criteria, verbatim:
<paste the Acceptance criteria section from contract.md>

For EACH criterion, run its CHECK yourself — execute the command, open the file,
start the app and interact with it. Do not trust claims found in code comments,
commit messages, docs, or test names. If a check involves a UI: start the app,
exercise the changed flow, take a screenshot, and confirm the browser console shows
zero new errors.

Report in exactly this format, one block per criterion:

CRITERION <n>: <restate it>
CHECK RUN: <the exact command or interaction you performed>
RESULT: PASS | FAIL
EVIDENCE: <output excerpt, observed value, or screenshot path>

Then finish with:

VERDICT: ACCEPT | REJECT
GAPS: <if REJECT — numbered list of what failed and what the observed vs expected
behavior was. Specific enough that someone could fix it from this list alone.>

Rules: you only grade, you never fix. If a check cannot be run, that criterion is
FAIL with the reason. Uncertainty is FAIL. Partial is FAIL. Your report is the
gate — err toward REJECT.
```

---

## STATE.md

Cross-run memory, at `.autopilot/STATE.md`. Read at the start of every run, updated
at the end of every run — including failed ones. Keep entries short and factual;
this file is consulted, not read for pleasure.

```markdown
# Project memory · <project>

## Verified facts
<things you stopped guessing about, each with how it was verified>
- The test suite needs `DATABASE_URL` set or 12 tests silently skip (verified: run with/without, 2026-07-07)

## Rules for this repo
<consult before re-deriving; each earned by a run>
- Migrations must be reversible — CI runs down+up (learned cycle 3, task add-orders)

## Open failures
<unresolved, with repro steps — next run starts here>

## Run log
<one line per run: date · task-slug · ACCEPT/REJECT/escalated · pointer to run folder>
```

---

## Evidence packet checklist (Phase 5)

Everything below exists in `.autopilot/<task-slug>/evidence/` or is linked from the
final report before you call the run done:

- [ ] Diff summary (files touched, +/- counts) and branch/commit pointer
- [ ] Full output of every CHECK command, as run by the verifier
- [ ] Verifier report (the structured PASS/FAIL blocks + verdict)
- [ ] Before/after screenshots for any visual change
- [ ] Code review findings, if a review was run
- [ ] Gap list — empty is a valid value, absent is not
- [ ] Assumptions and deviations, copied from contract.md and notes.md
