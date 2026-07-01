---
name: analyze
description: >
  LinkedIn own-analytics download and distillation. ALWAYS invoke when the user says "download my
  analytics", "analyze my LinkedIn analytics", "distill my post performance", "monthly analytics report",
  or hands over a LinkedIn analytics xlsx. Drives Chrome to export the raw analytics from LinkedIn (or
  takes a provided xlsx), parses it, appends to the local analytics.csv, and writes an insights report —
  performance tiers, trends, growth projection, what's working vs not, audience alignment. Do NOT use for
  competitor scraping (scout) or topic/trend research (research).
allowed-tools: Read, Write, Bash, Glob, Grep, Skill, ToolSearch, AskUserQuestion
---

# Analyze

Operational analytics: get the raw LinkedIn export (ideally hands-off via Chrome), turn it into rows in
`analytics.csv`, and distill it into an insights report. Numbers and patterns — no creative output.

## Step 0 — Load conventions + config

Read `../../references/conventions.md` (config, data layout, the xlsx sheet layout, browser pre-flight).
Read `../../references/benchmarks.md` (engagement brackets, format multipliers, cadence). From config:
`data_dir`, `follower_count`, `niche`, `profile_url`.

## Step 1 — Get the raw export

**Preferred — Chrome auto-download:**
1. Run the shared browser pre-flight from `conventions.md`.
2. Navigate to the LinkedIn analytics export flow (creator/post analytics, e.g.
   `https://www.linkedin.com/analytics/` or the profile's post-analytics page) and trigger **Export**
   to xlsx. LinkedIn lets you pick a date range — use the range the user asks for (default: last full month).
3. Find the downloaded file (newest `*.xlsx` in the OS Downloads dir — `~/Downloads` on macOS).

**Fallback:** if the export UI can't be driven, ask the user to export manually and supply the xlsx path.

## Step 2 — Parse + append

Run the parser (it computes engagement rate, de-dupes by `post_url`, and appends to `analytics.csv`):

```bash
# run from this skill's dir, or prefix the script with its absolute path
python3 scripts/parse_xlsx.py <path-to.xlsx> --data-dir "<data_dir>" --period "<label>"
```

`--period` defaults to the date range in the filename (e.g. `2026-05`). The script:
- merges TOP POSTS left/right tables by Post URL, computes `engagement_rate = engagements/impressions*100`,
- skips any `post_url` already present for that `period`,
- enriches `topic`/`format`/`hook_type` by matching `post_url` against `swipe-file.csv` when present,
- appends rows to `<data_dir>/analytics.csv` and prints a JSON summary (followers, demographics,
  daily engagement, per-post rows) to stdout for you to read.

If `openpyxl` is missing: `pip install openpyxl` (or `python3 -m pip install --user openpyxl`).

## Step 3 — Distill

From the parsed data + `analytics.csv` history, produce:
- **Performance tiers** — top 10% / mid 60% / bottom 30% by engagement_rate (and flag low-impression
  outliers). Write the tier back into `analytics.csv` (`tier` column).
- **Trends** — month-over-month impressions/engagements/ER; posting cadence (posts/week, gaps).
- **Growth projection** — current followers + avg new/week → rough trajectory; flag long silences.
- **Thematic** — group by `format`, `hook_type`, posting-day; identify breakouts (2×+ avg) and the pattern.
- **Audience alignment** — top job titles from DEMOGRAPHICS vs `config.niche`: matches / adjacent / off.
- **Benchmark** — place the user's avg ER in their `follower_count` bracket (`benchmarks.md`).

## Step 4 — Write the report

Save `<data_dir>/reports/analytics-YYYY-MM.md`:

```markdown
# LinkedIn Analytics — <period>

## Summary
[3–5 one-sentence findings]

## Scorecard
| Metric | Current | Benchmark / Target | Status |
| Avg impressions/post | … | … | … |
| Avg engagement rate | …% | bracket median | above/below |
| Posts/week | … | 3–5 | … |
| Followers | … | — | (+X this period) |
| Audience match to niche | …% | — | … |

## What's working (top 5)
[Post, impressions, engagements, ER, format, hook_type]

## What's not (bottom 5)
[same columns — what to learn]

## Audience alignment
[demographics vs niche]

## Growth projection
[trajectory + what would change it]

## Prioritized actions
1. … 2. … 3. …
```

## Done

Report path + headline finding + count of new `analytics.csv` rows. Note which import path was used and
any blocked step.
