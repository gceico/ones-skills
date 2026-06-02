# CLAUDE.md

This repo contains Agent Skills installable via `npx skills add gceico/ones-skills`.

Personal overrides go in `CLAUDE.local.md` (gitignored).

---

## Structure

```
skills/
  <skill-name>/
    SKILL.md        # skill definition with YAML frontmatter
```

## Adding a Skill

1. Create `skills/<name>/SKILL.md`
2. Add YAML frontmatter: `name`, `description`
3. Write skill instructions below the frontmatter
4. Push — installable immediately

## Testing a Skill Locally

```bash
npx skills add ./skills/<name>
```

## Installing from This Repo

```bash
npx skills add gceico/ones-skills --list   # browse all skills
npx skills add gceico/ones-skills/<name>   # install one skill
