---
name: connect
description: >
  LinkedIn lead harvester that builds your outreach pipeline. ALWAYS invoke when the user says "build my
  outreach list", "harvest my connections", "pull my recent connections", "who should I follow up with",
  "add leads to outreach", "harvest the comments on this post", "who commented on this post", "pull the
  likers of this post", or "get people who engaged with <post> that fit my ICP". Drives Chrome to collect
  people worth reaching out to from two kinds of source — your own network (recent 1st-degree connections
  + pending sent invites) and specific posts (commenters + likers/reactors on a post URL you name) —
  captures a one-line context note per person, scores them against your ICP, assigns the configured
  bucket, and appends unique leads to outreach.csv. Does NOT write or send messages (that's outreach),
  scrape creator content (scout), or analyze your own posts (analyze).
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

## Step 2 — Harvest

Collect people in small batches (~5–10 at a time, pause between to dodge rate limits). Pick the mode
from what the user asked for — you can run both in one session:

### Mode A — Network harvest (default)

Runs when the user asks for their connections / follow-up list and names no post. Two sources:

1. **Pending sent invites you haven't messaged** — `https://www.linkedin.com/mynetwork/invitation-manager/sent/`.
   Read name + profile URL for each. `source = pending-invite`.
2. **Recent 1st-degree connections** — `https://www.linkedin.com/mynetwork/invite-connect/connections/`
   (sorted "Recently added"). Take the most recent (default ~last 2 weeks / top ~50 unless the user
   says otherwise). `source = recent-connection`.

### Mode B — Post harvest (commenters + likers)

Runs when the user names a post (their own or anyone's — a competitor's viral post is a great ICP
source) and asks for its commenters and/or likers. If they asked for post harvest but gave no URL, ask
which post(s) and whether they want commenters, likers, or both. Open each post URL, then:

3. **Commenters** — scroll the comment section, clicking "Load more comments" / "Load previous replies"
   until the count you want is loaded (default top ~50; more only if the user asks). For each commenter
   read name + profile URL + headline, **and the text of their comment** — that comment is the trigger.
   `source = post-commenter`.
4. **Likers / reactors** — click the reactions summary (the "👍 N" count above the comment box) to open
   the reactions modal, scroll it to load names (default top ~50). Read name + profile URL + headline
   for each. Reaction type (Like / Celebrate / etc.) optional. `source = post-liker`.

Record the post once — its author + a short topic phrase — so every lead from it can reference it as a
trigger, and so you don't re-scan. Dedupe within the session: if someone both commented and liked, keep
the commenter row (stronger trigger).

For each person capture: `name`, `profile_url` (canonical `/in/<handle>/`, no query string), `headline`
(the role/tagline shown in the list).

## Step 3 — Find the trigger, score, bucket

The trigger is the whole point — a specific observation is the single biggest lever on reply rate, and
`outreach` will DROP any lead whose step-1 draft has no real trigger. So find one at harvest time.

**`context_note`** — one concrete observation you can open a message with. Factual, no fluff.
- **Post harvest (Mode B):** the trigger comes for free from the engagement — no profile visit needed.
  - Commenter → quote/paraphrase their comment: `commented on <author>'s post on <topic>: "<excerpt>"`.
  - Liker → `reacted to <author>'s post on <topic>`.
- **Network harvest (Mode A):** open `https://www.linkedin.com/in/<handle>/recent-activity/all/` and
  scan their latest few posts/comments (last ~30–60 days) for a recent observation (e.g. "posted last
  week about permitting delays killing solar deals"). Prefer a recent post over the headline. If they
  have **no recent activity and nothing beyond a bare headline**, leave `context_note` empty — still add
  them (valid lead), but `outreach` will skip them at step 1 until a trigger is supplied. Count these.

**`icp_score`** — `hi` / `med` / `lo` against `config.icp`, from the headline (+ the post activity you
already scanned in Mode A). Blank if unclear.
- **Mode A:** a signal for you, not a filter — everyone still gets added.
- **Mode B:** a **filter** — a post can draw hundreds of off-target reactors, and the user wants only
  their ICP. Add `hi`/`med`; **skip `lo` and unclear** (report the skip count). If the user says "add
  everyone" / "don't filter", add all instead.

**`bucket`** — the single `config.outreach.bucket`.

Keep it light: for Mode B judge ICP from the list row (headline) — don't open every profile. Batch +
pause as in Step 2.

## Step 4 — Append via the script

Write the harvested leads to a temp JSON array (fields: profile_url, name, headline, source, bucket,
icp_score, context_note), then:

```
python3 "${CLAUDE_PLUGIN_ROOT}/skills/outreach/scripts/pipeline.py" add-leads --data-dir "<data_dir>" --file <tmp.json>
```

It dedupes by `profile_url` (never re-adds someone already in the pipeline) and sets `status=new,step=0`.

## Done

Report: how many leads added vs skipped (dupes + any dropped for ICP in Mode B), a breakdown by source
(`recent-connection` / `pending-invite` / `post-commenter` / `post-liker`), the bucket, an ICP-score
breakdown (hi/med/lo), and **how many have no trigger** (empty `context_note` — skipped at step 1 until
you add one). Tell the user to run `outreach` when ready to message. Note anything that blocked partial
harvest.

## Not in v1

1st/2nd/3rd-degree search harvest — same `outreach.csv`, added later.
