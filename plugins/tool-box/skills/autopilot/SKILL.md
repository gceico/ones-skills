---
name: autopilot
description: >
  Own a feature, bugfix, or refactor end-to-end and return a finished, independently
  verified deliverable with evidence — not a chat reply. ALWAYS invoke when the user
  hands over a task to run without supervision: "autonomously build/ship/fix X",
  "take this end-to-end", "run this on autopilot", "I'm walking away — deliver X",
  or they name this skill plus a task. Do NOT use for quick edits, questions,
  explorations, or tasks with no verifiable outcome — if you can't state a check
  that proves it's done, this skill doesn't fit.
---

# Autopilot

You own this task end-to-end. Your output is a working deliverable plus the evidence
that proves it works — produced through a contract, a bounded build loop, and an
independent verification gate. This skill is written to be executed exactly: when a
rule below conflicts with your instinct to improvise, follow the rule. The rules
exist because agents predictably grade their own work too kindly, retry the same
failing idea, and grind past their budget. The structure is the defense.

## Non-negotiable rules

1. **The builder never grades its own work.** Every acceptance check is run by an
   independent verifier subagent with fresh context that sees only the artifact and
   the frozen criteria — never your reasoning, plan, or notes. Self-review does not
   count as verification, no matter how careful.
2. **Acceptance criteria freeze at the end of Phase 1.** After the freeze you may not
   edit the criteria, weaken a check, or modify a test that encodes a criterion in a
   way that makes it easier to pass. If a criterion turns out to be wrong or
   unachievable, stop and escalate — changing the goalposts is the user's call.
3. **Every criterion must be checkable.** Each one names an exact command to run or
   an exact observation to make. "Works well" is not a criterion; "`npm test` exits
   0" and "POST /orders returns 201 with an `id` field" are. If you can't write the
   check, rewrite the criterion until you can.
4. **Budgets are hard stops.** Default: 5 build cycles, 3 verification rounds. Use
   the user's numbers if given. When a budget is exhausted, stop and deliver what
   you have with an honest gap list — a bounded partial beats an unbounded grind.
5. **Two failed attempts at the same check means the approach is wrong.** Before a
   third attempt, write a new hypothesis in the cycle log that is not "same idea,
   tried harder" — different mechanism, different layer, or different diagnosis.
   Three distinct approaches failed → escalate with what you learned.
6. **Every run ends with a write-back.** Update `STATE.md` and finish the run log
   before delivering, even on failure — especially on failure. A run that doesn't
   record what it learned forces the next run to relearn it.

## Run artifacts

Create `.autopilot/<task-slug>/` in the repo at the start (suggest adding
`.autopilot/` to `.gitignore` if it isn't ignored). Everything lives there:

```
.autopilot/
  STATE.md               # cross-run project memory — read first, write last
  <task-slug>/
    contract.md          # Phase 1 output — frozen criteria live here
    notes.md             # plan, cycle log, deviations
    evidence/            # test output, screenshots, verifier reports
```

Templates for every file are in `references/templates.md` — read it when you reach
each phase rather than inventing formats.

---

## Phase 0 — Recon (before any code)

Read `.autopilot/STATE.md` if it exists — it holds verified facts and failure modes
from earlier runs; don't re-derive or re-trip them.

Then hunt what you don't know. Unknowns found now cost minutes; found in cycle 4
they cost the whole budget. Run whichever of these apply, skip what's already clear:

- **Conventions read.** Find 2–3 files in the repo that do something similar to the
  task and read them fully. Match their patterns — naming, error handling, test
  style. The repo's existing code outranks your habits.
- **Blindspot pass.** Ask yourself explicitly, and write the answers into
  `notes.md`: what is this task assuming about the environment, the data, or the
  load that nobody said out loud? What would a maintainer of this repo warn me
  about? What part of my understanding is thinnest?
- **Interview — only if it changes the architecture.** If the user is present, ask
  questions in one batch, and only questions whose answer would change the data
  model, an interface, or the UX flow. Everything smaller: pick the conservative
  option, log it as an assumption, keep moving. If the user is absent, every
  architecture-level ambiguity becomes a flagged assumption in the contract.

Output: an unknowns list in `notes.md`, each entry resolved or converted to an
explicit assumption.

## Phase 1 — Contract (the freeze point)

Write `contract.md` from the template. It has one job: define done so precisely
that a stranger could grade the run. It contains:

- **Goal** — an outcome, not an activity. "Users can reset their password via
  email," not "add password reset code."
- **Scope and non-goals** — what you will and deliberately won't touch.
- **Assumptions** — everything from Phase 0 the user hasn't confirmed.
- **Acceptance criteria** — numbered, each with its exact CHECK command or
  observation (rule 3). Prefer binary and mechanical: exit codes, HTTP statuses,
  pixel diffs, grep hits. For visual work, the check is a described observation
  against a screenshot, not "looks right."
- **Budgets** — build cycles, verify rounds, and wall-clock/cost limits if the
  user gave any.
- **Escalation triggers** — the specific conditions under which you stop and ask
  (see Escalation below).

If the user is present, show them the contract and get a yes before freezing. If
not, freeze it yourself and flag that in the final report. Either way: after this
point the criteria do not move (rule 2).

**Calibrate the instruments before building anything.** Run every CHECK command
once, now, against the current code. Each must execute and be capable of failing —
a check that errors with "command not found" or trivially passes on the broken
baseline cannot gate anything. Fix the check, not later.

## Phase 2 — Plan

Write a short plan in `notes.md`, ordered by what's expensive to change later:
data models and schemas first, then interfaces and contracts between components,
then UX flows, then the mechanical work last. For each decision that's hard to
reverse, note the alternative you rejected and why in one line.

Then execute the plan yourself for a bounded task. Split into parallel subagents
only when the work divides into slices that share no files — and then each
subagent works in its own git worktree, never the same checkout. Two agents
editing one file produces silent merge damage. If slices overlap, do them
sequentially; orchestration is a cost you must earn.

## Phase 3 — Build loop

The inner loop, per cycle: state a hypothesis → make the change → run the relevant
CHECKs → log the result. One line per cycle in `notes.md` using the cycle-log
format from the templates. The log is not bureaucracy — it's what makes rule 5
enforceable, because "same idea, tried harder" is visible in your own log.

If your environment has loop primitives (`/goal`, `/loop`, `/schedule`), run this
phase as a condition loop instead of hand-driving each cycle — read
`references/loop-patterns.md` first to pick the right type and copy a proven
shape. The architecture rule there is binding: timer outside, condition inside,
skill innermost; a condition loop drives work to a verifiable finish, a timer
loop only watches external state. A `/goal` completing does not skip Phase 4 —
its evaluator is a stop condition, not an independent verifier.

While looping:

- Write or extend tests before implementation where the repo has a test culture;
  match its style either way.
- When reality forces a deviation from the plan, take the conservative option, log
  it under "Deviations" in `notes.md`, and continue. Don't silently drift.
- Never touch the criteria or their encoding tests to make a check pass (rule 2).
  The temptation is the signal that something is wrong — investigate or escalate.
- Watch the budget. At each cycle boundary note cycles remaining. At zero, stop
  (rule 4).

Exit the loop only when every CHECK passes when you run it. That earns you the
gate — it does not mean you're done.

## Phase 4 — Independent verification (the gate)

Spawn a verifier subagent with fresh context. It receives exactly two things: the
artifact (branch, diff, or paths) and the frozen criteria copied verbatim from
`contract.md`. It does not receive your notes, your reasoning, or your claim that
things pass. Use the verifier prompt in `references/templates.md` word for word,
filling only the blanks.

The verifier re-runs every check itself and returns a structured PASS/FAIL per
criterion with evidence, then an ACCEPT/REJECT verdict. Its rules: uncertainty is
FAIL, partial is FAIL, and it never fixes anything — it only grades.

For anything with a UI: the verifier must start the app, interact with the changed
flow, capture before/after screenshots into `evidence/`, and confirm zero new
console errors. A text-only check on visual work is not verification.

- **REJECT** → take the gap list back to Phase 3. This consumes one verification
  round. Rounds exhausted → stop, deliver with gaps (rule 4).
- **ACCEPT** → save the verifier's report to `evidence/` and proceed.

If subagents are unavailable in your environment, the pattern still holds: output
the filled verifier prompt and ask the user to run it in a fresh session, and say
plainly that the work is unverified until then. Do not quietly substitute
self-review.

## Phase 5 — Deliver and compound

Run a fresh-context code review if the environment has one (e.g. `/code-review`);
save findings to `evidence/`. Then assemble the deliverable:

- **Evidence packet** — diff summary, test output, screenshots, the verifier
  report, review findings, and the honest gap list. The user gets evidence, not
  just a summary; a summary can be wrong in ways evidence can't.
- **Write-back** (rule 6) — update `.autopilot/STATE.md`: facts you verified about
  this codebase, rules worth consulting next run, open failures with repro steps,
  and a resume pointer. Lessons that generalize beyond this project belong in a
  skill, not STATE.md — say so in the report rather than burying them.
- **Final report** — lead with the verdict: what was delivered, verifier ACCEPT or
  the gaps if not. Then the criteria table with results, deviations and assumptions
  made, and where every artifact lives. Surface only the decisions that genuinely
  need a human; everything else is in the files.

If the run failed, the report says so plainly, with the strongest diagnosis you
have. A clear failure report is a successful deliverable; a dressed-up one is not.

## Escalation — stop and ask when

- A frozen criterion is wrong, contradictory, or unachievable as written.
- You discover mid-build that an architecture-level assumption from Phase 0 is
  false and the fix changes scope.
- Any budget is exhausted with criteria unmet.
- The next step is destructive, hard to reverse, or outward-facing (deploys,
  pushes to shared branches, data migrations, anything leaving the machine) and
  the user didn't explicitly pre-authorize it.

When escalating, deliver the current state first — contract, log, evidence so far —
so the user decides from facts, not from a question in a vacuum.
