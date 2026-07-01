---
name: research
description: >
  Cross-platform topic & trend research for content ops. ALWAYS invoke when the user says "research
  [topic]", "what's trending in my niche", "pull info on X", "what are people saying about Y", "refresh
  the niche radar", or wants source-backed background before writing about a heavy topic. Runs the
  last30days plugin on the topic (or the configured seed topics), supplements with web search, optionally
  cross-references the latest swipe file, and writes a sourced research brief — discourse map, ranked
  trends, open questions, weak signals, sources. Do NOT use to scrape LinkedIn creators (scout),
  to analyze own performance (analyze), or to draft/pick content.
allowed-tools: Read, Write, Bash, Glob, Grep, Skill, ToolSearch, WebSearch, WebFetch, AskUserQuestion
---

# Research

Research ops: find what's being discussed and trending on a topic, with sources. It informs — it does
not write posts, set voice, or pick ideas.

## Step 0 — Load conventions + config

Read `../../references/conventions.md` and resolve config. Read `../../references/research-method.md`
(the discourse-map + trends engine). From config you may use `seed_topics` and `niche`.

## Step 1 — Settle the topic

If the user named a topic, use it. Otherwise default to `config.seed_topics` (weekly niche radar). Don't
over-ask — one clarifying question only if the topic is genuinely ambiguous.

## Step 2 — Gather (delegate, don't hand-roll)

- **last30days** — `Skill("last30days")` on the topic. Use `--deep` for one heavy topic; default
  breadth for the weekly seed-topic radar. Keep the raw output: its engagement signal is how you rank
  trends by real interest. If last30days isn't installed, note it and fall back to web only.
- **Web** — `WebSearch` + `WebFetch` for editorial coverage, docs, and primary sources to corroborate.
- **Swipe file (optional)** — read the newest `<data_dir>/swipe-file.csv` to see what creators already
  cover (helps mark saturated vs white-space). Skip if absent.

## Step 3 — Run the method

Follow `research-method.md` stages 1–6 (disruption → discourse canvas → ranked trends → open questions
→ cross-domain angles → weak signals). Tag every material claim
`[backed by source]` / `[reasonable inference]` / `[speculative]` and cite inline.

## Step 4 — Write the brief

Save `<data_dir>/reports/research-<slug>-YYYY-MM-DD.md` (slug = kebab of the topic). Sections per
`research-method.md`: takeaway, discourse map, ranked trends (with sources + direction), open questions,
weak signals, flat source list. No "seeds in my voice", no pillars, no calendar.

## Done

Give the user the brief path and the one-line takeaway. Note any gap (last30days missing, thin sources).
