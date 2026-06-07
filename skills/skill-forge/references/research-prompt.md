# Deep-research prompt template

The research step is the quality gate. A thin map of the method makes a thin skill, so the
goal here is to ground the skill in how the field's best practitioners actually do this work —
not the model's vague recollection.

## How it runs

The user runs deep research, not you. Fill the template below for their specific method, hand
it over in one copyable block, and tell them: **"Run this in your deep-research tool
(Perplexity, ChatGPT deep research, Gemini, etc.) and paste the whole result back. I'll build
the skill from it."** Then stop and wait.

If the user declines (method is trivial or they know it cold), offer a quick inline `WebSearch`
pass instead — but say plainly it'll be shallower.

## Template — fill the brackets, then hand it over

```
I'm building a reusable AI skill that performs: [THE TASK / METHOD, e.g. "a Jobs-to-be-Done
customer-interview analysis"]. It will be used repeatedly by [WHO RUNS IT] to produce
[THE DELIVERABLE]. Research how this is done at a gold-standard level and return:

1. CANONICAL METHOD. The accepted steps / framework, in order. Cite the originators or the
   authoritative sources. If there are competing schools, name them and their differences.

2. INPUTS & CONTEXT. What information must a practitioner gather before starting? What
   questions must be answered for the output to be any good?

3. WHAT GOOD LOOKS LIKE. The standard deliverable format and the quality bar. Show a strong
   example if one exists. What separates an expert result from an amateur one?

4. COMMON FAILURE MODES. Where do naive or first-time attempts go wrong? What do experts
   check for that beginners miss?

5. RULES & CONSTRAINTS. Any compliance, ethical, or domain rules that must never be broken.

6. TOOLS & ARTIFACTS. Templates, scoring matrices, checklists, or reference materials the
   pros rely on.

Be concrete and cite sources. Prefer primary/authoritative sources over blog summaries.
```

## What to extract when they paste it back

- **Canonical steps** → the skill's workflow / phase order.
- **Context questions** → what the skill should ask or gather before producing output.
- **What good looks like** → the output format and quality checks baked into the skill.
- **Failure modes** → the "watch out for / verify" guidance.
- **Rules** → the guardrails (and any CLAUDE.md contract rules if building a harness).
- **Templates/matrices** → bundle as `assets/` or `references/` so the skill doesn't reinvent them.

Tell the user which parts you're using and why, so the link from research to skill is visible.
