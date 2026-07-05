---
name: ideate
description: >
  Blue-ocean ideation engine over your existing drafts and ideas — the raw scan, not a weekly content
  plan. ALWAYS invoke when the user says "ideate", "find blue ocean ideas", "sharpen my drafts", or
  "find white space I can own". Crosses the swipe file (what's saturated/working out there), the
  latest research brief (trends + white-space), your own analytics (what works for YOU), and your
  drafts/ideas backlog to surface uncontested ideas that fit you — ranked, each layered on top of an
  existing draft or idea where possible. Do NOT use to scrape creators (scout), research a topic
  from scratch (research), or download analytics. If a personal planning/radar skill is installed,
  "what should I post this week" belongs to it — it consumes this skill's report. Reads local files only.
allowed-tools: Read, Write, Edit, Bash, Glob, Grep, AskUserQuestion
---

# Ideate (Blue Ocean)

Find the uncontested space you can own. Cross what the market does, what's trending, what works for you,
and what you've already started — to surface ideas that are high-interest, low-competition, and yours.
It ranks and sharpens; it does not draft finished posts or set voice.

> Blue ocean = high curiosity + thin coverage + fits a strength you've proven. Not "a topic nobody
> posts" (often nobody posts it because nobody cares) — it must have real signal *and* an open lane.

## Step 0 — Load conventions + config

Read `../../references/conventions.md` (config, data layout, CSV schemas) and
`../../references/hook-patterns.md`. Resolve config for `data_dir`, `ideas_file`, `drafts_dir`.

## Step 1 — Read the four inputs (local only, no network)

1. **Market** — `<data_dir>/swipe-file.csv` + newest `reports/creator-research-*.md`: what's saturated,
   what's working (hooks/formats/topics), where coverage is thin.
2. **Trends** — newest `reports/research-*.md`: emerging topics, white-space, open questions.
3. **My proven strengths** — `<data_dir>/analytics.csv` + newest `reports/analytics-*.md`: which
   hooks/formats/topics win for me (so blue-ocean ideas land on a strength, not a weakness).
4. **My raw material** — `ideas_file` (the running idea backlog) + `drafts_dir` (existing drafts).

Any input missing: proceed with what exists, note the gap. If both market and my-material are empty,
tell the user to run scout and add some ideas/drafts first, then stop. Do counting/grouping with
a short Bash/Python step, not by eye.

## Step 2 — The blue-ocean scan

For each candidate (drawn from drafts, ideas, research white-space, and swipe-file gaps), score:

| Check | Question | Kill / flag |
|---|---|---|
| **Interest** | Real signal it's wanted? (research engagement, recurring questions, swipe traction) | only `[speculative]` → low |
| **Openness** | Under-covered by the scouted creators? | saturated in swipe file → low (unless a sharp reframe) |
| **Fit-to-me** | Lands on a hook/format/topic that works for me (analytics) or a draft I've started? | off my proven strengths → flag |
| **Readiness** | Can it build on an existing draft/idea now? | needs fresh research → tag `→ needs research`, don't drop |

Rank by Interest × Openness, break ties by Fit-to-me. **Anchor each surviving idea to a specific draft
or idea-backlog line** where one exists (this is "on top of my drafts", not generic). Tag every claim
`[backed by source]` / `[reasonable inference]` / `[speculative]`.

## Step 3 — Write the output

Save `<data_dir>/reports/ideation-YYYY-MM-DD.md`:

```markdown
# Blue-Ocean Ideation — YYYY-MM-DD

## Headline
[the single boldest open lane this week]

## Ranked ideas
For each (5–10):
- **Idea** — one line
- **Why blue ocean** — interest signal (+source) × why it's open (swipe/trend evidence)
- **Fits me because** — the proven hook/format/topic or the draft it builds on
- **Anchor** — draft/idea-line it extends, or "new"
- **Suggested hook pattern** — from hook-patterns.md
- Flags: `→ needs research` if applicable

## Parked
[candidates that didn't make the cut + the one-line reason]
```

Then append any genuinely new ideas back into `ideas_file` (one line each, dated) so the backlog grows.
Don't rewrite the user's drafts — point at them.

## Done

Report path + the headline open lane + count of new backlog lines added.
