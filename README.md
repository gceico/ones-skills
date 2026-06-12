# ones-skills

Agent Skills for Claude Code, built by [@gceico](https://github.com/gceico).

This repo supports **two install methods**:

- **skills.sh** — install a single skill on its own.
- **Claude Code marketplace plugin** — install the whole bundle at once.

### Install a single skill (skills.sh)

```bash
npx skills add gceico/ones-skills --list        # browse available skills
npx skills add gceico/ones-skills/<skill-name>  # install a specific skill
```

### Install as a plugin (Claude Code marketplace)

Install every skill in this repo as one plugin:

```
/plugin marketplace add gceico/ones-skills
/plugin install ones-skills@ones-skills
```

---

## Skills

| Skill | Description |
|---|---|
| [challenger](skills/challenger/) | Adversarial stress-tester for technical decisions, designs, specs, and rationale — forces a binary defend/revise verdict before you commit |
| [skill-forge](skills/skill-forge/) | Turns workflows you keep redoing by hand into real, reusable Agent Skills — and proves they fire before you trust them |

---

## Contributing / Forking

Each skill lives in `skills/<name>/SKILL.md`. Fork, add your own, and share via `npx skills add <your-handle>/<repo>`.

---

## License

MIT
