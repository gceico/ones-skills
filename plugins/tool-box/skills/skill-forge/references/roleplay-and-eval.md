# Prove it works: role-play first, then the full eval loop

Two stages, cheap before expensive. The role-play is a fast unit test that the skill fires and
runs in order. The skill-creator handoff is the rigorous, quantitative benchmark.

## Stage 1 — Role-play a mock user (fast)

Before any benchmark, confirm the skill actually triggers and executes its phases. The trick:
let the **current agent play a realistic end-user** so the human watches the skill run on a
prompt they'd really type, without doing the typing themselves.

1. Write 1–2 test prompts the way a real user talks — concrete, with backstory, file names,
   casual phrasing. Not "format this data" but "my boss dropped a Q4 sales xlsx in my downloads
   and wants a profit-margin column, revenue's in C, costs in D." Show them to the user first.
2. Spawn a sub-agent (`Agent`) with access to the new skill. Give it the test prompt as if it
   were the user, and ask it to **complete the task using the skill**, then report:
   - Did the skill trigger? (If not, the description is the bug.)
   - Which phases/steps fired, in what order, with a one-line evidence quote each.
   - Where did it get stuck, guess, or skip a step?
3. Read the report. A phase that silently skipped or fired out of order is a skill bug — fix the
   instruction (usually a missing *why* or a pointer buried below the fold), not the symptom.
4. Re-run until phases fire reliably.

**Optional second mock:** spawn a *second* sub-agent that role-plays the user across a short
back-and-forth — answering the skill's interview questions, pushing back once — so you can see
the skill handle a real conversation, not just a one-shot prompt. Useful for skills that
interview or have human-in-the-loop checkpoints.

## Stage 2 — Hand off to skill-creator (rigorous)

Once phases fire, escalate. **Invoke the `skill-creator` skill** for the full loop:

- Test cases run **with-skill vs. baseline** so you can measure the skill's actual lift.
- Graded **assertions** (objective pass/fail checks) per test case.
- The **eval-viewer** browser UI: the user clicks through outputs, leaves feedback, sees the
  quantitative benchmark (pass rate, time, tokens) side by side.
- Iterate: improve the skill, rerun into a new iteration directory, review again.
- **Description optimization** to tune triggering accuracy.
- **Packaging** into an installable `.skill` file.

### What to carry into the handoff

Don't make skill-creator re-derive what you already learned. Bring:
- The drafted skill (path).
- The research findings — they tell you what "good output" means, which seeds the assertions.
- The realistic test prompts from Stage 1 (reuse them as eval prompts).
- The "what good looks like" and "what goes wrong" from the interview — these become assertions
  and qualitative review criteria.

skill-creator owns the test/benchmark/viewer mechanics from here. Your job was getting the
method right, the shape right, and the phases firing; its job is proving the quality at scale.
