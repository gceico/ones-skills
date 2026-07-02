---
name: connect
description: >
  LinkedIn lead harvester that builds your outreach pipeline. ALWAYS invoke when the user says "build my
  outreach list", "harvest my connections", "pull my recent connections", "who should I follow up with",
  or "add leads to outreach". Drives Chrome to collect people you haven't followed up with — recent
  1st-degree connections and pending sent invites — captures a one-line context note per person, scores
  them against your ICP, assigns the configured bucket, and appends unique leads to outreach.csv. Does
  NOT write or send messages (that's outreach), scrape creator content (scout), or analyze your own
  posts (analyze).
allowed-tools: Read, Write, Bash, Glob, Grep, ToolSearch, AskUserQuestion
---

# Connect

Turn the people already in your network into rows in `outreach.csv`. Browser-driven, hands-off. It
collects and buckets — it does not message anyone. The `outreach` skill does that later.

State is owned by `scripts/pipeline.py` (see the `outreach` skill) — this skill only harvests and hands
leads to `add-leads`. Never hand-edit `outreach.csv`.

## Step 0 — Load conventions + config

1. Read `../../references/conventions.md` (config resolution, data layout, `outreach.csv` schema,
   browser pre-flight, operating style). Resolve config; if none, scaffold from the example and stop.
2. From config you need: `data_dir`, `icp`, and `outreach.bucket`. If the `outreach` block is missing,
   tell the user to add it (point at the example) and stop.

## Step 1 — Browser pre-flight

Run the shared browser pre-flight from `conventions.md`. STOP and notify if it fails.

## Step 2 — Harvest (MVP sources)

Collect people in small batches (~5–10 at a time, pause between to dodge rate limits). Two sources:

1. **Pending sent invites you haven't messaged** — `https://www.linkedin.com/mynetwork/invitation-manager/sent/`.
   Read name + profile URL for each. `source = pending-invite`.
2. **Recent 1st-degree connections** — `https://www.linkedin.com/mynetwork/invite-connect/connections/`
   (sorted "Recently added"). Take the most recent (default ~last 2 weeks / top ~50 unless the user
   says otherwise). `source = recent-connection`.

For each person capture: `name`, `profile_url` (canonical `/in/<handle>/`, no query string), `headline`
(the role/tagline shown in the list).

## Step 3 — Find the trigger + bucket

The trigger is the whole point — a specific observation is the single biggest lever on reply rate, and
`outreach` will DROP any lead whose step-1 draft has no real trigger. So find one at harvest time.

Per person, open `https://www.linkedin.com/in/<handle>/recent-activity/all/` and scan their latest few
posts/comments (last ~30–60 days). Capture:
- `context_note` — **one concrete, recent observation** you can open a message with: what they posted,
  built, launched, or care about (e.g. "posted last week about permitting delays killing solar deals").
  Prefer a recent post over the headline. Factual, no fluff.
  - If they have **no recent activity and nothing beyond a bare headline**, leave `context_note` empty.
    Still add them (they're a valid lead) — but a later `outreach` run will skip them at step 1 unless
    you supply a trigger. Note the count of these at the end.
- `icp_score` — `hi` / `med` / `lo` against `config.icp`. Blank if unclear. A signal for you, not a
  filter — everyone still gets added.
- `bucket` — the single `config.outreach.bucket`.

Keep it light: a quick scan per profile, not a deep read. Batch + pause as in Step 2.

## Step 4 — Append via the script

Write the harvested leads to a temp JSON array (fields: profile_url, name, headline, source, bucket,
icp_score, context_note), then:

```
python3 ../outreach/scripts/pipeline.py add-leads --data-dir "<data_dir>" --file <tmp.json>
```

It dedupes by `profile_url` (never re-adds someone already in the pipeline) and sets `status=new,step=0`.

## Done

Report: how many leads added vs skipped (dupes), the bucket, an ICP-score breakdown (hi/med/lo), and
**how many have no trigger** (empty `context_note` — these get skipped at step 1 until you add one).
Tell the user to run `outreach` when ready to message. Note anything that blocked partial harvest.

## Not in v1

Likers/commenters on posts, and 1st/2nd/3rd-degree search harvest — same `outreach.csv`, added later.
