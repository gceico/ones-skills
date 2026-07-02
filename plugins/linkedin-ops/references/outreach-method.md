# outreach — message doctrine

Shared by `connect` (context notes) and `outreach` (drafting). Assisted, human-approved 1:1 messaging —
not mass automation. Every message is drafted, reviewed, and sent one at a time from your own session.
This is the lowest-risk architecture: LinkedIn's ToS §8.2 bans automated *sending*, not AI-assisted
*drafting*. Keep the human clicking send.

Grounded in practitioner data (Belkins/Expandi 42M-touch 2025 study, Morgan Ingram/Aaron Reeves 5k-DM
study, Lavender, Will Leatherman warm-vs-cold, LinkedIn User Agreement §8.2). See
`outreach-research-prompt.md` to refresh.

## The stance

- **Warm first.** These are people who already connected/accepted. Post-accept reply rates run 20–30%
  vs 3–8% cold — the win is in *who* you message, which `connect` already handles. Talk like they said
  yes once. No cold pitch.
- **Signal before sequence.** Reach out only with a real trigger: a post they wrote, a role change,
  headcount growth, something specific. Trigger-based outreach roughly doubles reply rate over "just
  connecting." The `context_note` is that trigger — if there's no real one, keep it honest and short
  rather than faking specificity.
- **One specific line beats name-only.** Name-only personalization is the weakest lever; a single
  observation sentence lifts replies ~28% even at 1:1 volume. Spend the 2 minutes to write it.
- **No pitch in step 1.** Step 1 opens a conversation with a question, never a calendar ask.
- **Single, easy CTA.** One question they can answer in a line. "How are you handling X right now?"
  beats "book a 30-min call." Multiple questions = decision fatigue = no reply.
- **Short.** 150–350 characters, steps 1–2. Under ~600 for the breakup. Fits a phone screen without
  scrolling. Messages >400 chars roughly halve reply rate.
- **Their name, your voice.** Personalize the name + one trigger detail; the rest stays in
  `sender_context` voice. Minimal, human — not a bespoke essay.

## Cadence

- **Max 3 touches** (config `max_steps`). Diminishing returns are sharp after 3; a 4th text DM reads as
  harassment in a persistent thread. After the last, the lead drops to `done` — no more nudges.
- **Space 4–7 days apart** (config `intervals_days`, default `[0, 4, 7]` = step1 now, +4d, +7d).
  Sub-4-day gaps read as automated. Don't instant-message someone the second they accept.
- **Later steps lighter, not louder.** Step 2 is a gentle bump. Step 3 is the breakup (below).
- **Timing:** Tue–Thu, mornings, recipient's local time lifts replies ~10–15%. Real but modest — never
  hold a message days to hit a "perfect" slot; proximity to the trigger matters more.

## The breakup (step 3)

The highest-reply message in the sequence, because it's final, polite, and hands over control.
Loss-aversion + an easy exit. Pattern (the one that works on us): *"reaching out one last time before I
disappear from your inbox — still think X could help, but I'll assume the timing's off. Just reply and
I'll close the loop."* No new pitch, no guilt.

## Stop-on-signal (the hard rule)

The moment a lead replies OR reacts to your message, the sequence ends for them (`mark-replied`,
terminal). A reply is the win — the goal was the conversation, not finishing the template. Even "not
now" moves them to human-handled. When a thread is ambiguous, assume they engaged and stop.

- **Reply / reaction / "remove me" → hard drop.** Never message again from the sequence.
- **Profile view after your DM → not a stop.** It's interest, not a reply. Continue as planned (maybe
  hold the next touch a day longer).
- **Re-engage a dropped lead only after 60–90 days**, with a fresh trigger, starting at step 1, never
  referencing the old thread.

## What kills it (the tells that flagged inbound spam as junk to us)

- The same line sent to everyone; no signal-specific observation.
- Pitching / calendar-asking before they've said a word back.
- "Just following up" with no new angle or value.
- Unfilled merge variables (`"targeting ."`, `{first_name}`) or double-spaces / `chat ?` spacing —
  the exact scars that read as a mail-merge tool. **Reject any draft with an unfilled `{placeholder}`.**
- Over 3 touches. Silence after 3 is an answer — respect it.
- Over-formal or buzzword-y ("I hope this finds you well", "leverage", "circle back").
- Stacking fake urgency ("2 spots left") or bribes (gift cards) — works for volume agencies, corrodes a
  personal brand built on trust. Skip it.
