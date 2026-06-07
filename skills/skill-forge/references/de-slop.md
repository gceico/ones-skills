# De-slop & friction pass

Reread the draft with fresh eyes, as a reviewer who didn't write it. Three lenses.

## 1. Engineering (DRY / KISS / YAGNI)

- **No repetition.** Every concept has one home. If the same instruction appears in two places,
  one is wrong the moment you edit the other. Move shared truth to a reference and point to it.
- **Nothing speculative.** Cut steps, options, and edge-case handling for situations that
  haven't come up. A skill earns complexity by needing it, not by anticipating it.
- **One job per piece.** Each section, each reference file, does one thing. If a file is a
  grab-bag, split it.
- **Earn every line.** Read each instruction and ask "what breaks if I delete this?" If nothing,
  delete it. Lean skills run better — less to skim, less to dilute attention.

## 2. Reasoning over rules

- Prefer explaining **why** over piling on `MUST`/`ALWAYS`/`NEVER`. A model that understands the
  goal handles cases you didn't enumerate; a model following bare commands breaks on the first
  case you missed.
- All-caps imperatives are a **yellow flag**. When you catch one, try reframing it as the reason
  behind it. Reserve hard `MUST`/`NEVER` for genuine lines: compliance, safety, data loss.
- Don't overfit to the test cases. You're iterating on a few examples; the skill runs on
  thousands of unseen prompts. Write the principle, not a patch.

## 3. UX & friction

- **Sensible defaults.** The skill should pick the obvious option and move, not stop to ask
  what it could reasonably infer. Ask only when the answer genuinely changes the outcome.
- **No dead ends.** Every branch leads somewhere. If a step can fail, say what to do next.
- **Minimal questions, batched.** One focused `AskUserQuestion` batch beats a drip of prompts.
- **The Friday test.** Would a tired, non-expert user get through this without confusion? If a
  step needs jargon, define it inline in half a sentence.

## 4. Prose (kill the slop)

Skill text should read like a sharp engineer wrote it, not a content mill.

- Cut filler: *just, really, basically, simply, actually, in order to, it's important to note.*
- Cut formulaic scaffolding: "In this section we will…", "Let's dive in", windup before the point.
- Prefer active voice and concrete verbs. "Read the file," not "the file should be read."
- Cut vague declaratives that assert without informing ("This is a powerful feature").
- One idea per sentence. If you need a comma-spliced clause to qualify a claim, split it.

After the pass, the draft should be shorter, clearer, and free of instructions that don't pull
their weight.
