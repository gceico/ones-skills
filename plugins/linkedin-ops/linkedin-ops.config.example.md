# linkedin-ops — config

Copy this file to `linkedin-ops.config.md` in the folder you run Claude from, and fill the block below.
That's the whole setup.

```yaml
# Where your tables + reports live. ~ expands; "." means the current folder.
data_dir: ./data/

# Your own LinkedIn profile (for the scout gap section + analyze).
profile_url: https://www.linkedin.com/in/your-handle/

# Your current follower count — picks the analyze benchmark bracket.
follower_count: 1000

# One-line niche — used for audience alignment + default research framing.
niche: "applied AI for builders"

# Default topics fed to last30days when you don't name one.
seed_topics:
  - AI agents for business
  - how teams actually work with AI

# Creators to scout — LinkedIn handles only (no @, no URL).
creators:
  - donnellychris
  - ruben-hassid
  - stevenbartlett-123
  - alexhormozi
  - lexfridman
  - alicjasmin
  - garyvaynerchuk

# Idea backlog ideate reads + grows. Default <data_dir>/ideas.md.
ideas_file: ./data/ideas.md

# Optional: folder of your in-progress drafts ideate anchors ideas to. Omit if none.
# drafts_dir: ./data/drafts/

# --- outreach (connect + outreach skills) ---
# One-line ICP: who you target + qualifying signals + disqualifiers. Free text; scores harvested leads.
icp: >
  Target: <roles/titles>. Signals: <what makes them a fit>. Skip: <disqualifiers>.

# Optional: your own tone-of-voice / writing-style docs. Outreach reads these before drafting
# so messages sound like you, not a template engine. Paths relative to this config file. Omit if none.
# voice_files:
#   - knowledge/brand/tone-of-voice.md
#   - knowledge/writing/my-voice.md

outreach:
  bucket: warm-connections      # v1: a single bucket
  max_steps: 3
  intervals_days: [0, 4, 7]     # days to next step: step1 now, step2 +4d, step3 +7d
  daily_cap: 15                 # max messages queued per outreach run
  sender_context: >
    Who you are in one line + the outcome you help with. Human, no pitch.

# Pre-approved sequence for the bucket. {name} + {context} placeholders (context = the trigger/
# observation from the lead's context_note). 3 short (150-350 char) human messages. No pitch in
# step 1 — one easy question. Later steps lighter. Step 3 is the breakup. See references/outreach-method.md.
sequences:
  warm-connections:
    - "Hey {name}, thanks for connecting! {context} — curious, how are you handling that right now?"
    - "Hey {name}, no worries if you're busy — just bumping this in case it got buried."
    - "Hey {name}, reaching out one last time before I disappear from your inbox. I'll assume the timing's off for now — just reply if that changes and I'll pick it back up."
```

Loop + requirements: see `README.md`.
