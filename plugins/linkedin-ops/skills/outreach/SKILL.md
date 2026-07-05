---
name: outreach
description: >
  LinkedIn outreach sequencer that runs your pre-approved message sequence. ALWAYS invoke when the user
  says "run my outreach", "send follow-ups", "message my leads", "who's due for a message", or "work my
  outreach pipeline". Reads outreach.csv, asks the script who is due, checks each LinkedIn thread for a
  reply or engagement (and drops anyone who answered — no one is messaged twice after they respond),
  drafts the next step from your pre-approved sequence, shows the whole batch for approval/edit, then
  drives Chrome to send and records state. Does NOT harvest leads (that's connect), scrape creators
  (scout), or analyze your posts (analyze).
allowed-tools: Read, Write, Bash, Glob, Grep, ToolSearch, AskUserQuestion
---

# Outreach

Run the sequence over the people `connect` harvested. On-demand and due-date driven: running it any day
only touches leads whose next step is due, so it's safe to re-run. Idempotent — the script owns all
state in `outreach.csv`. Tokens go to the browser + writing messages; the script does the bookkeeping.

**Hard rule:** if a lead has replied or engaged since your last message, they are done — never messaged
again. Enforced twice: the thread check in Step 3, and the terminal `replied` status in the script.

## Step 0 — Load conventions + method + config

1. Read `../../references/conventions.md` (config resolution, data layout, `outreach.csv` schema,
   browser pre-flight, operating style). Resolve config; if none, scaffold from the example and stop.
2. Read `../../references/outreach-method.md` (message doctrine).
3. From `config.outreach` you need: `bucket`, `max_steps`, `intervals_days`, `daily_cap`,
   `sender_context`, and `sequences`. If the block is missing, point the user at the example and stop.
4. If `config.voice_files` is set, Read each listed file (paths relative to the config) — these define
   how the user actually writes. They govern word choice and rhythm in Step 4; skip silently if unset.

Let `TODAY` = the run date (get it: `date +%F`). Let `INTERVALS` = `intervals_days` joined by commas
(e.g. `0,4,7`).

## Step 1 — Browser pre-flight

Run the shared browser pre-flight from `conventions.md`. STOP and notify if it fails.

## Step 2 — Who is due

```
python3 scripts/pipeline.py due --data-dir "<data_dir>" --today TODAY \
  --max-steps <max_steps> --intervals INTERVALS --daily-cap <daily_cap>
```

Returns the batch (each with `profile_url`, `name`, `context_note`, `step`, `next_step`,
`last_sent_date`). If empty: tell the user nobody's due and stop.

## Step 3 — Reply / engagement safety (the core rule)

For each due lead, open their conversation in Chrome (`https://www.linkedin.com/messaging/` → their
thread, or the message button on their profile). Determine: **is there any inbound message from them, or
any reaction to your last message, dated after `last_sent_date`?** (For a lead at step 0 there's usually
no thread yet — pass through.)

- If yes (they replied or engaged): `python3 scripts/pipeline.py mark-replied --data-dir "<data_dir>" --url <url> --today TODAY` and **drop them from the batch.**
- If no: they stay in the batch for a message.

When in doubt (ambiguous thread), treat as replied and drop — never risk double-messaging.

## Step 4 — Draft the batch

For each remaining lead, take the template at index `next_step - 1` from `config.sequences[bucket]`.
Fill `{name}` and weave `{context}` (the trigger/observation from `context_note`) into a natural line —
step 1 must carry one specific observation, not name-only. Voice from `config.outreach.sender_context`,
the `voice_files` loaded in Step 0 (word choice, rhythm, banned phrases — these win over generic
politeness), and the doctrine in `outreach-method.md`. Keep each 150–350 chars, one easy question,
no pitch in step 1.

**Lint before showing:** reject any draft that still contains an unfilled `{placeholder}`, a leftover
`<topic>`-style stub, or double-spaces — those are the exact tells that read as mail-merge spam. Rewrite
or, if there's no real trigger for step 1, drop that lead from this batch rather than send a generic line.

## Step 5 — Batch approval (nothing sends before this)

Present the whole batch as a table: `name | step | drafted message`. Ask the user to **approve all,
edit specific rows, or skip specific rows** (use AskUserQuestion or a plain prompt). Apply their edits.
Skipped rows are left untouched (still due next run).

## Step 6 — Send + record

For each approved message: drive Chrome to open the thread and send it, then immediately:

```
python3 scripts/pipeline.py mark-sent --data-dir "<data_dir>" --url <url> --date TODAY \
  --max-steps <max_steps> --intervals INTERVALS
```

This advances the step, sets `next_due_date`, and marks `done` when the last step is sent. If a send
fails, do NOT mark-sent — leave the lead due and note it.

## Done

Report: sent count, dropped-as-replied count, skipped count, then run
`python3 scripts/pipeline.py status --data-dir "<data_dir>"` and show the pipeline summary.
