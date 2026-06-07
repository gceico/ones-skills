# Authoring: shape, anatomy, and writing the draft

## Pick the shape

Choose the smallest thing that does the job. Bigger structures cost more tokens at rest and
more maintenance later.

| Shape | When | Looks like |
|-------|------|-----------|
| **Single skill** | One method, one bounded workflow | `skills/<name>/SKILL.md` |
| **Skill + references** | Method has variants or large knowledge worth splitting so only the relevant slice loads | `SKILL.md` + `references/*.md` |
| **Slash command** | A daily multi-step workflow wired to one trigger, built from pieces that already exist | `.claude/commands/<name>.md` |
| **Harness** | Distinct roles run in sequence with shared method files | `CLAUDE.md` + sub-agents + shared `references/` |

When variants exist (frameworks, clouds, regions), organize by variant so Claude reads only the
relevant file:
```
cloud-deploy/
├── SKILL.md          (workflow + which-variant selection)
└── references/
    ├── aws.md
    ├── gcp.md
    └── azure.md
```

## Anatomy of a skill

```
skill-name/
├── SKILL.md (required)
│   ├── YAML frontmatter (name, description required)
│   └── Markdown body — the workflow / expertise
└── Optional bundled resources
    ├── scripts/     executable code for deterministic, repeated steps
    ├── references/  docs loaded into context only as needed
    └── assets/      files used in the output (templates, fonts, icons)
```

## Progressive disclosure (the load model)

1. **Metadata** (`name` + `description`) — always in context, ~100 tokens. The trigger.
2. **SKILL.md body** — loads when the skill triggers. Keep under ~500 lines. Front-load the
   critical instructions; content far below the fold gets skimmed during reasoning.
3. **references/** — load per sub-task. Unlimited in total because only the needed file loads.
   For any reference over ~300 lines, add a table of contents at the top.

If the body is creeping past 500 lines, that's the signal to push a section into `references/`
with a clear pointer from the body ("Read `references/x.md` when …").

## The description — highest-leverage line

It's the only thing read when deciding whether to activate, and skills tend to **under**trigger,
so make it directive and a little pushy:

- Lead with a directive verb + role: "Invoice-reconciliation expert."
- "**ALWAYS invoke when** the user <concrete triggers, phrasings, contexts>" — list real phrases
  a user would type, including ones where they don't name the skill or file type.
- "**Do NOT use for** <exclusions>" — a negative clause sharpens the boundary and prevents
  overtriggering on near-misses.
- Include *what it does* AND *when to use it*. Put all "when to use" info here, not in the body.

Passive "Use when you need to format data" undertriggers. "Data-cleaning expert. ALWAYS invoke
when the user mentions messy spreadsheets, deduping, or fixing a CSV — even if they don't say
'clean.' Do NOT use for building charts." triggers reliably.

## Writing the body

- **Imperative voice.** "Read the intake file," not "You should read the intake file."
- **Explain why.** Today's models have good theory of mind; a reason they can reason about beats
  a bare command. Reserve `MUST`/`NEVER` for genuine hard lines (compliance, safety).
- **Define output formats explicitly** when the output has a fixed shape:
  ```
  ## Report structure — always use this template:
  # [Title]
  ## Summary
  ## Findings
  ## Recommendations
  ```
- **Show examples** for anything with a learnable pattern (input → output pairs).
- **Don't overfit.** You're iterating on a few examples but the skill runs on thousands of
  unseen prompts. Write the general principle, not a patch for one test case.

## Frontmatter fields

- `name` (required) — lowercase-hyphen, matches the directory.
- `description` (required) — see above.
- `allowed-tools` (optional) — register only the tools the skill actually uses.
- `model` / `effort` / `context: fork` (optional, rare) — for skills that should run isolated or
  on a cheaper model.
