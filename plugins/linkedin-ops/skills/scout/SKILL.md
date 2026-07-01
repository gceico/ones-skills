---
name: scout
description: >
  LinkedIn creator scout that builds your swipe file. ALWAYS invoke when the user says "run creator
  scout", "scrape creators", "refresh my swipe file", "what are top creators posting", or "scout
  LinkedIn". Drives Chrome to read each configured creator's recent activity, extracts hooks,
  media types and engagement, appends each unique post to the local swipe-file.csv, and writes a
  competitive report. Do NOT use for cross-platform or non-LinkedIn trend research (that's
  research) or for the user's own analytics (that's analyze).
allowed-tools: Read, Write, Edit, Bash, Glob, Grep, ToolSearch, AskUserQuestion
---

# Scout

Operational scouting: turn what top creators posted this week into rows in your swipe file plus one
competitive report. Browser-driven, hands-off. It collects and tags — it does not draft or opine.

## Step 0 — Load conventions + config

1. Read `../../references/conventions.md` (config resolution, data layout, swipe-file schema, browser
   pre-flight, operating style). Resolve config; if none, scaffold from the example and stop.
2. Read `../../references/hook-patterns.md` (hook patterns, media types).
3. From config you need: `creators` (handles), `data_dir`, `profile_url` (for the gap section).

## Step 1 — Browser pre-flight

Run the shared browser pre-flight from `conventions.md` (load Chrome tools, confirm connected + logged
into LinkedIn). STOP and notify if it fails — do not proceed.

## Step 2 — Scout each creator (batches of 5)

Process `config.creators` in **batches of 5** (1–5, 6–10, …). Pause briefly between batches to dodge
rate-limiting. If LinkedIn shows a "you're viewing too fast" interstitial, wait ~60s and continue; if it
persists, save what you have and note it at the end.

For each creator open `https://www.linkedin.com/in/<handle>/recent-activity/all/`. There is no "show
all" — posts lazy-load on scroll. Scroll down repeatedly until you reach posts **older than 7 days**,
then stop. Keep only posts from the last 7 days (today = run date).

Estimate the creator's follower count from their profile (open `/in/<handle>/` once) for `followers_est`.

### Per post (expand "…more" before reading)

Extract: creator name + `handle`; `age` (e.g. `3d`, `1w`, within 7 days); `hook` (the 1–2 lines before
"…more"); `body_excerpt` (full expanded text, trimmed to ~300 chars); `media_type`
(text/image-meme/infographic/screenshot/video/carousel/poll/repost); engagement (`likes`, `comments`,
`reposts`; impressions too if shown).

**De-dupe reposts:** a creator's own reshares show twice — keep each unique `post_url` once.

### Tag each post

- `theme_tags` — one or more, pipe-separated, e.g. `AI|Marketing|LinkedIn-tips`. Infer from the niche.
- `hook_pattern` — exactly one, from `hook-patterns.md`.
- `why_it_worked` — one short clause: the load-bearing reason (the hook), filled for the standouts.

## Step 3 — Append to the swipe file

Append every unique post as a row to `<data_dir>/swipe-file.csv` (create with the header from
`conventions.md` if absent). De-dupe against existing rows by `post_url` — never write a post already
in the file. RFC-4180 quote any field with a comma/newline. Use a short Bash/Python step to append
safely rather than hand-editing.

## Step 4 — Write the report

Save `<data_dir>/reports/creator-research-YYYY-MM-DD.md` (actual run date). One-paragraph **"this week's
biggest takeaway"** at the very top, then:

1. **Raw post table** — every unique post, all fields.
2. **Top hooks** — ranked by engagement, each labeled with its hook pattern.
3. **Content formats** — which media types win, per creator and overall.
4. **Best in the niche** — top 5 posts across all creators, and WHY each worked.
5. **Trends & resources** — recurring themes/formats/takes; surface any tools/resources creators
   explicitly recommend.
6. **Voice & cadence tips** — tone, structure, CTA patterns worth noting (observed, not prescriptive).
7. **Cross-creator leaderboard** — by total engagement and by reach-per-follower (using `followers_est`).
8. **Gap vs. my profile** — open `config.profile_url` recent activity; what these creators do that the
   user doesn't, ranked by ROI.

If anything blocked partial completion (rate limits, a feed wouldn't load), note it clearly at the end.

## Done

Tell the user the report path + how many new swipe-file rows were added.
