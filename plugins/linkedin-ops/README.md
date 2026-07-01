# linkedin-ops

**Sc**out · **I**deate · **R**esearch · **A**nalyze — a white-label LinkedIn creator **ops** loop on
local files. Scout creators, research topics, ideate blue-ocean angles over your drafts, and analyze your
own performance — no Notion, no creative drafting, no hardcoded niche. Config-driven, stored as `.md` + `.csv`.

## Skills (the loop, in order)

| # | Skill | Does | Runs on |
|---|---|---|---|
| 1 | `scout` | Weekly: scrape creators → swipe file + report of what's working out there | Chrome + LinkedIn |
| 2 | `research` | Weekly/on-demand: trend & topic research → sourced brief | last30days + web |
| 3 | `ideate` | Weekly: cross swipe × research × analytics × your drafts/ideas → ranked blue-ocean ideas | local files only |
| 4 | `analyze` | Monthly: download your LinkedIn export → insights; feeds back into step 3 | Chrome + Python/openpyxl |

Data lives under `data_dir` (set in config): `swipe-file.csv`, `analytics.csv`, `ideas.md`, `reports/`.

## Setup

1. Install: `/plugin install linkedin-ops@ones-skills`
2. Copy `linkedin-ops.config.example.md` → `linkedin-ops.config.md` and fill it.
3. Install the `last30days` plugin; connect the Claude-in-Chrome extension + log into LinkedIn;
   `python3 -m pip install --user openpyxl`.

Then just say things like *"run scout"*, *"research AI agents for business"*, *"ideate"*, *"download and
analyze my analytics"*.

## Depends on

- [`last30days`](https://github.com/mvanhorn/last30days-skill) — cross-platform research (invoked as a skill).
- Claude-in-Chrome — browser automation for scouting + the analytics export.

## Design notes

Distilled from a private Notion-coupled creator system, stripped to portable ops. It stops at *ranked
blue-ocean ideas anchored to your own drafts* — no finished-post drafting, no voice/brand layer, no
content calendar. linkedin-ops finds, measures, distills, and ideates; you decide what to write and write it.
See the shared `references/conventions.md` for the config + data schemas every skill reads.
