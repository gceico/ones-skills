# Interview: capture the workflow, find the best candidate

Use this when the user hasn't already described their workflow in enough detail to draft from.
Goal: extract one real, repeatable task worth turning into a skill — and capture *how the user
actually does it* and *what good looks like*, because that judgment is the skill's real value.

Ask **one question at a time** with `AskUserQuestion` (or plain prose if the user prefers to
just talk). After each answer, reflect a concrete artifact back — a draft rule, a filtered
list, a step — so the user sees the system forming. Don't drip a long quiz; stop as soon as you
have a clear candidate.

## Part 1 — Understand the work

1. **Role & domain.** What's your role, and what does your team actually do day to day?
   → Reflect back 2–3 candidate guardrail rules for their domain.
2. **A typical week, unfiltered.** List everything you do — the boring admin, meetings, reports,
   reviews, emails, all of it.
   → Reflect the list back, grouped by category.

## Part 2 — Filter to the best candidate

Run the list through four filters. Drop what fails each.

3. **Frequency.** Mark each task daily / weekly / monthly / rare. → Keep daily + weekly.
4. **Pattern.** Which survivors follow steps you could teach someone else? A task that's
   different every time is hard to capture. → Keep the ones with a describable pattern.
5. **Human checkpoints.** For each, where does human judgment have to stay in the loop —
   approve, decide, review? These become the "stop and confirm" points in the workflow.
6. **Tools & data.** What does each task touch — email, Slack, spreadsheets, a CRM, a database,
   files, an API? Known connections make a task easier to automate.

Then present the survivors as a ranked list: "These are your best candidates, easiest win
first." Pick #1 with the user (or let them override).

## Part 3 — Capture the expertise (the part that matters)

For the chosen candidate, go deep — this is what separates a real skill from a thin one:

- **Walk me through exactly how you do it, step by step.** What do you do first, then next?
- **Where do you make judgment calls?** What are you weighing? What's the rule of thumb?
- **What does "good" look like?** How do you know a finished one is right?
- **What goes wrong?** What mistakes does a junior make? What do you check for?
- **What's never allowed?** Compliance lines, quality bars, things that cause trouble if skipped.

These answers feed the research prompt (Phase 1) and the draft (Phase 3). The "judgment calls"
and "what good looks like" become the heart of the skill; the "never allowed" becomes its
guardrails.

## Reflecting artifacts as you go

The interview should feel like the skill building itself. Cheap, concrete reflections to show:
a draft trigger line, a 3-step workflow sketch, a guardrail rule, the file tree. Keep them
short — they're momentum, not deliverables.
