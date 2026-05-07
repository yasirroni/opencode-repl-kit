---
name: updating-a-skill
description: Use when modifying an existing skill in this repo — covers what can and cannot change, how to check cross-references, when to split vs extend, and how to verify updates. Load before editing any existing SKILL.md.
---

# Updating a Skill

## When to Use

- Editing an existing SKILL.md in `.opencode/skills/`
- Adding or removing reference files, scripts, or assets
- Renaming or relocating a skill directory

## Principles

- **Match existing style** — copy the conventions of the file you're editing
- **Don't "improve" adjacent content** — touch only what the change requires
- **Surgical changes** — if you didn't break it, don't refactor it
- **Clean up orphans** — if your change removes a reference to a file, remove the link from the References section

## What Can Change

- Adding new sections that fit the skill's [category template](../writing-a-skill/SKILL.md)
- Adding reference files (update SKILL.md's References section with the link)
- Expanding gotchas with verified new findings from REPL testing
- Fixing broken links or outdated information
- Updating spawn commands for new runtime versions

## What Cannot Change (Without Strong Reason)

- **Frontmatter `name`** — must always match the directory name
- **Directory name** — renaming breaks every cross-reference that points at this skill
- **Category boundaries** — don't mix language REPL content into EDA skills (see skill separation principle in AGENTS.md)
- **"Keep Alive" footer** — don't remove it from REPL-spawning skills
- **`⚠️ Critical: \n` warning** — don't remove from any skill that uses `pty_write`

## When to Split vs Extend

| Situation | Action |
|-----------|--------|
| Skill exceeds 170 lines | Split into base skill + extension (like `*-repl` → `*-repl-eda`) |
| Content applies to multiple languages | Put in a shared reference skill (`repl-quick-reference`, etc.) |
| Content is specific to one language only | Put in that language's `*-repl` or `*-repl-eda` skill |
| Adding a task-specific workflow | Create a new workflow skill; cross-reference the base skill |

## Cross-Reference Checks After Any Update

```
1. Grep for the skill name across all SKILL.md files
   grep -r "skill-name" .opencode/skills/ --include='*.md'

2. If you renamed/moved the skill → update every SKILL.md that references it
   grep -r '\.\.\/skill-name' .opencode/skills/ --include='*.md'

3. If you added a reference file → add it to the skill's References section

4. Check AGENTS.md tables are still accurate
   grep -r "skill-name" AGENTS.md
```

## Verification After Update

1. **Load test**: skill still fires on its trigger description
2. **Link audit**: all `../` links in the edited skill resolve to existing files
3. **Line count**: skill still within its category's line-count guidelines
4. **AGENTS.md**: table description still accurately describes what the skill does
5. **Related skills**: any skill that cross-references this one still makes sense
