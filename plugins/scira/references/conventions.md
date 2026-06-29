# SCIRA — shared conventions

Every skill reads this file first, then loads config. Config schema, data-file schemas, directory
resolution, and the last30days dependency live here and nowhere else. Don't redefine them in a skill.

## Config resolution (first hit wins)

1. `./scira.config.md` (current working directory)

If none found: copy `scira.config.example.md` to `./scira.config.md` in current dir,
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

## Data directory layout

All paths below are relative to `data_dir`

```
<data_dir>/
  swipe-file.csv        # scout appends; competitor signal
  analytics.csv         # analyze appends; own performance
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

## Browser pre-flight (scout + analyze download)

Both Chrome-driven skills share this gate. Load Chrome tools via ToolSearch:
`select:mcp__claude-in-chrome__tabs_context_mcp,mcp__claude-in-chrome__navigate,mcp__claude-in-chrome__read_page,mcp__claude-in-chrome__computer,mcp__claude-in-chrome__tabs_create_mcp`.
Confirm a browser is connected (`tabs_context_mcp`), navigate to `https://www.linkedin.com/feed/`, and
confirm a logged-in nav/avatar (not a login wall). If not connected or not logged in: STOP and tell the
user — "Chrome not connected / not logged into LinkedIn. Open Chrome with the extension + your LinkedIn
session, then re-run." Do not proceed.
