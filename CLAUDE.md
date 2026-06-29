# CLAUDE.md

A Claude Code marketplace. Each plugin is a folder under `plugins/`.

Personal overrides go in `CLAUDE.local.md` (gitignored).

---

## Structure

```
.claude-plugin/marketplace.json   # lists every plugin
plugins/
  <plugin-name>/
    .claude-plugin/plugin.json    # name, description, author
    skills/<skill-name>/SKILL.md  # YAML frontmatter: name, description
    references/                   # optional shared docs
```

## Adding a skill to an existing plugin

1. Create `plugins/<plugin>/skills/<name>/SKILL.md` with `name` + `description` frontmatter.
2. Push — shipped on next install.

## Adding a new plugin

1. `plugins/<plugin>/.claude-plugin/plugin.json` (`name`, `description`, `author`).
2. Add its `skills/`.
3. Add an entry to `.claude-plugin/marketplace.json` with `source: "./plugins/<plugin>"`.

## Install

```
/plugin marketplace add gceico/ones-skills
/plugin install <plugin>@ones-skills
```
