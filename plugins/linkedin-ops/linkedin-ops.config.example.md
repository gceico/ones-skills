# linkedin-ops — config

Copy this file to `linkedin-ops.config.md` (in the folder you run Claude from, or `~/.config/linkedin-ops/`)
and fill the block below. That's the whole setup.

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
```

Loop + requirements: see `README.md`.
