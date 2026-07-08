# Loop patterns — picking the right loop type

The architecture rule, memorize it: **timer outside, condition inside, skill
innermost.** A timer (`/loop`) re-arms the work on a schedule, a condition
(`/goal`) defines verified-done so the run can't stop early, and a skill does the
actual work well. Never invert this — a timer can't drive work to a finish, and a
condition can't watch a clock.

First, check what your environment actually has: `/loop` and `/schedule` are
Claude Code built-ins; `/goal` exists in recent versions and in Codex. If a
primitive is missing, the *shape* still holds — you run the same cycle manually
(Phase 3's cycle log IS a hand-rolled condition loop).

## The four loop types

| Type | Trigger | Stops when | Reach for it when | Never use it for |
|---|---|---|---|---|
| **Turn-based** (no command) | you prompt | the agent judges done | exploration, Phases 0–2, anything needing judgment per step | work that needs verified-done — the agent stops at "good enough" |
| **Condition loop** (`/goal`) | manual, once | a fast evaluator confirms the condition, or the turn cap hits | driving to a verifiable finish — Phase 3's inner loop | vague outcomes ("improve UX"), watching external systems |
| **Timer loop** (`/loop`) | interval | you stop it (Esc) or its own end-state is met | watching external state on a clock: CI, PRs, flaky reruns | driving a task to completion — each firing restarts, nothing accumulates toward done |
| **Scheduled** (`/schedule`) | cron, in the cloud | per-run | recurring maintenance that must survive your laptop being off | one-off tasks |

The 10-second router: *Can a command verify done?* → condition loop. *Am I
watching something change on its own clock?* → timer loop. *Does it recur
daily/weekly, unattended?* → schedule. *Still figuring out what done means?* →
turn-based; you have no business looping yet — go finish the contract.

## Rules for any condition you write

These are the same rules as the contract's acceptance criteria, because a `/goal`
condition IS a mini-contract:

1. Deterministic, binary or numeric — exit codes, HTTP statuses, thresholds. The
   evaluator is a fast model; give it something it can't rationalize.
2. **Always append a turn cap** (`stop after N turns`). No cap = grinding hours
   for 2%. This is rule 4 of the skill wearing a different hat.
3. The condition should point at the frozen checks, not restate a vibe of them.
4. `/goal` completing does NOT skip Phase 4. The goal evaluator is a stop
   condition, not an independent verifier — it confirms the checks ran green, it
   doesn't grade blind. The verifier gate still runs.
5. Try ONE clean `/goal` before any multi-agent setup. A single condition loop
   with a clear finish line routinely beats an orchestration harness; earn
   orchestration only when work splits into slices sharing no files.

## Good examples

**Drive Phase 3 from a frozen contract** — the canonical autopilot inner loop:

```
/goal every CHECK in .autopilot/add-password-reset/contract.md passes when run —
work in cycles, log each cycle in notes.md per the autopilot format — stop after
10 turns
```

**Ship a PR until CI is green** — condition loop spanning implement → push → fix:

```
/goal a PR is open for this change and every CI check passes — implement, test
locally, push, open the PR with `gh pr create`, then keep fixing failures
(re-check with `gh pr checks`) until green; stop after 10 turns
```

**Migrate an API** — a countable, greppable end state:

```
/goal every file importing from `./legacy-api` now imports from `./v2-api`, all
tests pass, and `npm run typecheck` is clean — stop after 30 turns
```

**Reach a numeric threshold**:

```
/goal test coverage is at least 80% with all tests passing — add focused tests
for the least-covered files, re-run coverage each turn — stop after 12 turns
```

**Watch CI after delivering** — external state on a clock, so timer loop:

```
/loop 10m run `gh pr checks 1234`; if all pass, tell me it's ready to merge; if
any fail, summarize which and why
```

**Kill flaky tests** — self-paced timer with a provable end state:

```
/loop run the test suite 20 times, collect every intermittent failure, fix or
quarantine the flaky ones, and don't stop until 5 consecutive fully-green runs
```

**The full nested shape** — timer outside, condition inside, skill innermost:

```
/loop 30m /goal all PR review comments resolved via /review, stop after 10 turns
```

**Recurring, laptop-off** — cloud cron:

```
/schedule every weekday at 9am, label new issues from the last 24h by area and
priority, and post a one-line summary on each
```

## Anti-examples — wrong loop, wrong condition

```
/goal improve the UX of the settings page
```
No check a fast evaluator can run. The loop halts whenever the agent feels done.
Rewrite as observable criteria first ("settings save without page reload, axe
reports 0 violations"), then loop.

```
/goal all tests pass
```
Right condition, no turn cap. On a genuinely hard failure this grinds
indefinitely. Append `— stop after N turns`, always.

```
/loop 15m implement the checkout feature
```
Timer loop driving a finish. Every 15 minutes it re-fires with no accumulated
"done" condition — it will re-litigate its own work forever. This is `/goal`'s
job.

```
/goal 100% test coverage
```
A target that invites gaming — trivial assert-true tests satisfy the number
without testing anything. Pair every gameable metric with a fence: "coverage ≥
80% AND no test lacks a meaningful assertion", and remember rule 2: the builder
never edits the checks to pass them.
