# Hook taxonomy

Used by `scout` (tag every scouted post) and `ideate` (rank by pattern). One pattern per
post — pick the dominant one. The hook is the 1–2 lines shown before "…more".

| Pattern | What it looks like | Tell |
|---|---|---|
| `question` | Opens with a direct question to the reader | ends in `?`, "Ever notice…", "What if…" |
| `contrarian` | States the opposite of the consensus | "Unpopular opinion", "Everyone's wrong about…", "Stop doing X" |
| `stat` | Leads with a number/result | "92% of…", "I did X for 30 days", "$10k in 2 weeks" |
| `story` | First-person narrative open | "Last week a client…", "3 years ago I…" |
| `list` | Promises an enumerated payload | "7 ways to…", "5 mistakes…", "Here's my stack:" |
| `authority-quote` | Borrows a named authority | "Naval said…", "Per the OpenAI team…" |
| `before-after` | Transformation framing | "I went from X to Y", "Before: … After: …" |
| `news-jack` | Hooks onto a fresh event/release | "GPT-5 just dropped and…", reacting to a launch |
| `tease` | Withholds the payoff to force the click | "This changed everything 👇", "Nobody talks about this" |

## Media types (for `media_type`)

`text` / `image-meme` / `infographic` / `screenshot` / `video` / `carousel` / `poll` / `repost`.
