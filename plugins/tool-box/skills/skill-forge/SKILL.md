---
name: skill-forge
description: >
  Turns the work you keep redoing by hand into a real, reusable Agent Skill — and proves it
  works before you trust it. ALWAYS invoke when the user wants to build, design, or scaffold
  a skill, agent, slash command, or CLAUDE.md harness; says "turn this workflow into a skill",
  "make a skill for X", "make a [named-method] skill" (Blue Ocean, JTBD, pre-mortem, devil's
  advocate, any methodology); pastes deep-research output and says "make this a skill"; or
  describes a process they repeat by hand and want captured. Runs an interview, gates on
  research, picks the right shape, drafts with progressive disclosure, role-plays a mock user
  to prove it fires, then hands off to skill-creator for the full eval loop. Do NOT use for
  authoring content with a skill that already exists, or for general coding unrelated to
  building agent configuration. Don't skip it because a request "sounds simple" — the
  interview and research are where the value is.
allowed-tools: Read, Write, Edit, Bash, Glob, Grep, Skill, Agent, AskUserQuestion, WebFetch, WebSearch
---

# Skill Forge

Build a skill the way you'd ship software: understand the job, research the gold standard,
draft for reuse, strip the slop, then prove it works. You orchestrate the build. The heavy
quantitative eval/viewer loop belongs to `skill-creator` — invoke it when the draft is ready.

## Why this exists

A skill captures something you do repeatedly so a general model becomes a domain expert on
demand. Two failure modes kill most skills: they're **thin** (the author never mapped how
the work is actually done, or what "good" looks like in the field), or they're **dead code**
(written once, reused never, because they overfit one example or buried the trigger). Every
phase below fights one of those.

## Read the room

This skill serves marketers and ops folks as often as engineers. **Adapt language to cues.**
Default to plain language: say "the trigger line that decides when this turns on," not "the
description field." Only use terms like *frontmatter*, *JSON*, *assertion*, *progressive
disclosure* once the user shows they know them. Explain a term in a half-sentence when in
doubt. Never make someone feel they need a CS degree to forge a skill.

## Operating principle

This is harness engineering: the win comes from curating the smallest set of high-signal
tokens that reach the model, not a bigger model. Two laws follow, and they shape every draft:

- **Progressive disclosure.** A skill loads in three tiers — `name`+`description` (always in
  context, ~100 tokens), the `SKILL.md` body (loads when the skill triggers), `references/`
  files (load only for the sub-task that needs them). Keep the body lean; push detail down a
  tier. Front-load what matters — content far below the fold gets skimmed.
- **Context as budget.** Every token competes for attention; quality rots as the window fills.
  Use sub-agents as context firewalls so noisy intermediate work never reaches the main thread.

---

## Phase 0 — Capture intent

Read the conversation first. If the user already described a workflow or pasted research,
extract what you can before asking. Then confirm the gaps with `AskUserQuestion` — one focused
batch, not a drip. You need four things:

- **The job.** What does the user keep doing by hand that this should capture? Who runs it?
- **The method.** A named methodology, or the user's own process? Either way there's a bar to
  hit — what does the field consider best practice for doing this well?
- **The shape.** Single skill, slash command, or a fuller harness? Don't default — decide in
  Phase 2.
- **Success.** What does a good run produce? What would make the user say "this nailed it"?

If the user hasn't described their workflow in enough detail to draft from, **interview them.**
Read `references/interview.md` — it has the workflow-capture question bank and the funnel that
filters a week of tasks down to the single best automation candidate.

---

## Phase 1 — Research (the quality gate)

A shallow method map yields a shallow skill, so don't research silently and move on. The flow:
**you craft a deep-research prompt, the user runs it in their external deep-research agent
(Perplexity, ChatGPT deep research, etc.), they paste the output back.**

1. Read `references/research-prompt.md` and fill the template for this specific method.
2. Hand the user the prompt in a copyable block: "Run this in your deep-research tool and paste
   the result back. I'll build from it."
3. **Stop and wait.** When they paste, extract: the canonical steps, the context questions any
   practitioner must answer, the standard deliverables, and where naive attempts go wrong.
4. If the user says skip it (method is simple or they know it cold), offer a quick inline
   `WebSearch` pass instead — but say plainly that a thin map makes a thin skill.

---

## Phase 2 — Pick the shape

Choose the smallest thing that fits the job. Read `references/authoring.md` for the decision
rules and the full anatomy.

- **Single skill** — one method, one workflow, bounded.
- **Skill + references** — the method has variants or large bodies of knowledge worth splitting
  so only the relevant slice loads.
- **Slash command** — a daily multi-step workflow wired to one trigger from pieces that exist.
- **Harness (CLAUDE.md + sub-agents)** — distinct roles running in sequence with shared method
  files. Only when the job genuinely spans roles.

Then design knowledge flow **before writing**: every concept gets ONE home. Shared truth lives
in a reference file that components point to — never duplicated, never copy-pasted across
workflows. Sketch the file tree and show the user.

---

## Phase 3 — Draft

Write the draft following `references/authoring.md` (anatomy, progressive disclosure, output
formats). The **description is the highest-leverage line** — it's the only thing read when
deciding whether to activate. Write it directive, not passive: "X expert. ALWAYS invoke when
the user <triggers>. Do NOT use for <exclusions>." Passive "Use when…" undertriggers; a
directive verb plus a negative clause triggers reliably.

---

## Phase 4 — De-slop & friction pass

Reread the draft with fresh eyes, as a reviewer. Run `references/de-slop.md`:
- **Engineering:** no repetition, nothing speculative, each piece one clear job. Prefer
  explaining *why* over piling on `MUST`/`ALWAYS`. All-caps imperatives are a yellow flag —
  reframe as reasoning the model can act on.
- **UX:** sensible defaults, minimal questions, no dead ends. Would a tired user on a Friday
  get through this without friction?
- **Prose:** kill filler, formulaic structure, passive voice, vague declaratives.

---

## Phase 5 — Prove it fires (role-play)

Before any heavy benchmark, prove the skill actually triggers and runs in order. Read
`references/roleplay-and-eval.md`. Fast version: spawn a sub-agent that **plays a realistic
end-user** hitting the new skill on 1–2 prompts the user would actually type, and reports which
phases fired, in order, with evidence. Where a phase silently skipped, that's a skill bug —
fix the instruction (usually a missing *why* or a buried pointer), not the symptom.

---

## Phase 6 — Hand off to the full eval loop

Once phases fire reliably, escalate to rigorous evaluation: **invoke the `skill-creator`
skill** for the quantitative test/benchmark/eval-viewer loop — test cases vs. baseline,
graded assertions, the browser review, description optimization, and packaging. You supplied
the researched method and the architecture; skill-creator supplies the scaffolding and the
rigorous harness. See `references/roleplay-and-eval.md` for how the handoff works and what to
carry over.

---

## Phase 7 — Deliver

Final read. Confirm the file tree matches the design, cross-references resolve, the trigger
line reads well. Tell the user what was built, where it lives, and how to invoke it. If it's
in this repo's `skills/`, remind them it's installable via `npx skills add`.
