# ones-skills

A Claude Code marketplace of agent plugins, built by [@gceico](https://github.com/gceico).

## Install

```
/plugin marketplace add gceico/ones-skills
/plugin install tool-box@ones-skills    # challenger + skill-forge
/plugin install linkedin-ops@ones-skills       # LinkedIn creator ops loop
```

## Plugins

| Plugin | Skills | What it does |
|---|---|---|
| [tool-box](plugins/tool-box/) | challenger, skill-forge | challenger stress-tests a technical decision before you commit; skill-forge turns workflows you keep redoing by hand into reusable, validated Agent Skills |
| [linkedin-ops](plugins/linkedin-ops/) | scout, ideate, research, analyze, connect, outreach | White-label LinkedIn creator ops loop on local `.md`/`.csv` files — scout creators into a swipe file, ideate blue-ocean angles, research trends, analyze your own stats, harvest leads into a pipeline, and run a pre-approved stop-on-reply outreach sequence |

## Layout

```
.claude-plugin/marketplace.json   # this marketplace
plugins/
  tool-box/                       # one plugin per folder
    .claude-plugin/plugin.json
    skills/<name>/SKILL.md
  linkedin-ops/
    .claude-plugin/plugin.json
    skills/<name>/SKILL.md
```

Add a plugin: drop a folder under `plugins/` with its own `.claude-plugin/plugin.json` and `skills/`, then add an entry to `marketplace.json`.

## Who's behind this

I'm Gabriel. I build these skills for my own work first — the LinkedIn loop runs my actual posting, the tool-box is what I reach for to pressure-test a decision or turn a task I keep redoing by hand into something reusable. When one gets good enough, I clean it up and ship it here.

Day job: I run [**Aibl**](https://aibl.to) with Nizar. We do hands-on workshops where teams take the work they already know and turn it into AI agents they use the next day — the same instinct as this repo, just in a room with your team. Most AI training stops at the login screen; we start where the actual work is.

If that sounds like your team, [come say hi](https://aibl.to). No pitch — just tell me what you're trying to automate and I'll tell you straight whether we can help.

— Gabriel

## License

MIT
