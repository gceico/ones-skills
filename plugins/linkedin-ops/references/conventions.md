# linkedin-ops — shared conventions

Every skill reads this file first, then loads config. Config schema, data-file schemas, directory
resolution, and the last30days dependency live here and nowhere else. Don't redefine them in a skill.

## Config resolution (first hit wins)

1. `./linkedin-ops.config.md` (current working directory)

If none found: copy `linkedin-ops.config.example.md` to `./linkedin-ops.config.md` in current dir,
tell the user to fill it, and stop. Don't invent niche/creators/profile.

The config is Markdown with a single fenced ```yaml block. Parse that block. Fields:

| Field | Required | Use |
|---|---|---|
| `data_dir` | yes | where tables + reports live. use current dir. |
| `profile_url` | scout, analyze | the user's own LinkedIn profile URL |
| `follower_count` | analyze | picks the benchmark bracket |
| `niche` | research, analyze | one-line niche, used for audience-alignment + default research framing |
| `seed_topics` | research | default topics for last30days when the user names none |
| `creators` | scout | list of LinkedIn handles (no `@`, no URL) to scout |
| `ideas_file` | ideate | path to the running idea backlog. Default `<data_dir>/ideas.md`. |
| `drafts_dir` | ideate | optional folder of existing drafts ideate reads + anchors to. Skip if unset. |
| `icp` | connect | one-line ideal-customer profile; scores harvested leads (hi/med/lo). |
| `voice_files` | optional (outreach) | list of paths to the user's own tone-of-voice / writing-style docs. Skills that write in the user's name read these before drafting so output sounds like the user, not a template engine. Paths resolve relative to the config file. Skip if unset. |
| `outreach` | connect, outreach | block: `bucket`, `max_steps`, `intervals_days`, `daily_cap`, `sender_context`. |
| `sequences` | outreach | per-bucket list of pre-approved message templates (`{name}`/`{context}`). |

## Data directory layout

All paths below are relative to `data_dir`

```
<data_dir>/
  swipe-file.csv        # scout appends; competitor signal
  analytics.csv         # analyze appends; own performance
  outreach.csv          # connect appends, outreach advances; the lead pipeline
  ideas.md              # ideate reads + grows; the running idea backlog
  reports/              # every skill writes dated markdown here
```

`ideas.md` is a free-form bullet list, one idea per line (date-prefixed when ideate appends). `drafts_dir`
(if set in config) is the user's own folder of in-progress drafts — ideate reads + anchors to them, never rewrites.

Create the dir and a CSV with its header row on first write. Never overwrite an existing CSV — append.

### swipe-file.csv

Header (exact, in order):

```
date_scouted,creator,handle,post_url,age,hook,hook_pattern,body_excerpt,media_type,theme_tags,likes,comments,reposts,followers_est,why_it_worked
```

- `date_scouted` ISO date of the scout run. `age` as shown on LinkedIn (e.g. `3d`, `1w`).
- `hook_pattern` from `hook-patterns.md`. `theme_tags` pipe-separated (e.g. `AI|Marketing`).
- Quote any field containing a comma/newline per RFC-4180. `body_excerpt` ≤ ~300 chars.
- De-dupe key: `post_url`. A creator's own reshares appear twice in the feed — keep one row.

### analytics.csv

Header (exact, in order):

```
period,post_url,publish_date,impressions,engagements,engagement_rate,topic,format,hook_type,tier
```

- `engagement_rate = engagements / impressions * 100`, one decimal.
- `tier` ∈ `top` / `mid` / `bottom` (assigned during distillation, may be blank on raw import).
- `topic`/`format`/`hook_type` filled by matching `post_url` against `swipe-file.csv` where possible, else blank.
- De-dupe key: `post_url`. Skip a row whose `post_url` already exists for the same `period`.

### outreach.csv (connect + outreach skills)

Header (exact, in order):

```
profile_url,name,headline,source,bucket,icp_score,context_note,status,step,last_sent_date,next_due_date,last_checked_date,notes
```

- **Never hand-edit this file.** All writes go through `skills/outreach/scripts/pipeline.py`
  (`add-leads` / `due` / `mark-sent` / `mark-replied` / `status`). It owns dedupe, interval math, and
  step advancement so skills spend tokens on the browser + messages, not bookkeeping.
- De-dupe key: `profile_url` (canonical `/in/<handle>/`, no query string).
- `status` ∈ `new` / `active` / `replied` / `done` / `stopped`. `replied`/`done`/`stopped` are
  terminal — never messaged again.
- `step` 0..`max_steps`. `icp_score` ∈ `hi`/`med`/`lo`/blank. `source` e.g. `pending-invite` /
  `recent-connection` / `post-commenter` / `post-liker`.

## LinkedIn analytics xlsx layout (for the `analyze` skill)

A LinkedIn "Content" analytics export contains these sheets:

- **TOP POSTS** — row 3 headers, row 4+ data. Cols A–C = Post URL, publish date, engagements (left table);
  cols E–G = Post URL, publish date, impressions (right table). Merge the two by Post URL.
- **FOLLOWERS** — row 1 total followers; row 3+ = date, new followers.
- **DEMOGRAPHICS** — job titles with percentages (for audience alignment).
- **DISCOVERY** — row 2 impressions total; row 3 members reached.
- **ENGAGEMENT** — daily: date, impressions, engagements.

## last30days dependency

Cross-platform research is delegated to the `last30days` plugin via `Skill("last30days")` — never a
hardcoded script path (keeps this white-label/portable). If the skill isn't installed, say so and
degrade to WebSearch/WebFetch only, noting the limitation in the report.

## Operating style (all skills)

Ops, not creative. Scout / research / download / distill — never draft posts, pick ideas, set voice,
or build a content calendar. Run hands-off: minimal questions, sensible defaults from config, prefer
reading the local dbs and the web over asking. Where a step is blocked (Chrome down, rate-limited,
last30days missing), save partial work and note the gap at the end of the report.

## Browser pre-flight (scout, analyze, connect, outreach)

Every Chrome-driven skill shares this gate. Load Chrome tools via ToolSearch:
`select:mcp__claude-in-chrome__tabs_context_mcp,mcp__claude-in-chrome__navigate,mcp__claude-in-chrome__read_page,mcp__claude-in-chrome__computer,mcp__claude-in-chrome__tabs_create_mcp`.
Confirm a browser is connected (`tabs_context_mcp`), navigate to `https://www.linkedin.com/feed/`, and
confirm a logged-in nav/avatar (not a login wall). If not connected or not logged in: STOP and tell the
user — "Chrome not connected / not logged into LinkedIn. Open Chrome with the extension + your LinkedIn
session, then re-run." Do not proceed.
