---
name: writing-a-skill
description: Use when creating a new skill in this repo — covers naming conventions, frontmatter requirements, directory structure, category templates, required elements, cross-referencing, and length guidelines. Load before writing any new SKILL.md.
---

# Writing a Skill

## When to Use

- Creating a new skill in `.opencode/skills/`
- Before writing any new SKILL.md
- When you're unsure whether a task warrants a skill, an agent, or an AGENTS.md entry

## Skill vs Agent

| | Skill | Agent |
|---|---|---|
| **Location** | `.opencode/skills/<name>/SKILL.md` | `.opencode/agents/<name>.md` |
| **Frontmatter** | `name` + `description` | `description` + `mode: primary` |
| **Behavior** | Reusable instruction set loaded into any agent's context | Standalone entity with its own decision loop |
| **Has decision loop?** | No | Yes |
| **Has own tool access?** | No | Yes |

→ If the output is "instructions the main agent follows," it's a skill.
→ If the output is "a subagent you dispatch to do work autonomously," it's an agent.
→ If it's neither (behavioral guidelines for all agents), put it in **AGENTS.md**.

## Directory Structure

```
.opencode/skills/<kebab-case-name>/
├── SKILL.md              # required
├── references/           # optional: supplementary docs (100+ line references)
├── scripts/              # optional: helper scripts, templates
└── assets/               # optional: configs, static files
```

## Naming Conventions

- **`repl-*`** prefix: REPL-agnostic cross-cutting skills (`repl-session-management`, `repl-quick-reference`, `repl-eda-workflow`)
- **`*-repl`** suffix: language-specific mechanics (`python-repl`, `matlab-repl`, `julia-repl`)
- **`*-repl-eda`** suffix: language-specific EDA patterns
- **`repl-test-*`** prefix: per-language test workflows
- **Gerund verb-first** for process skills: `writing-a-skill`, `updating-a-skill` (not `skill-writing`)
- **kebab-case only.** One skill per directory. Directory name must match frontmatter `name`.

## Frontmatter (Required)

```yaml
---
name: <kebab-case>           # must match directory name exactly
description: <trigger only>  # starts with "Use when...", describe WHEN not WHAT
---
```

- `name`: letters, numbers, hyphens only. No parentheses or special chars.
- `description`: start with "Use when...". Describe triggering conditions only — **never** summarize the skill's workflow. Agents use the description to decide whether to load the skill; if the workflow is summarized there, they skip reading the body.
- Max ~500 characters for description.

## Category Templates

Each skill category has a set of expected sections. Follow the template for the category your skill belongs to.

| Category | Skills | Required Sections |
|----------|--------|-------------------|
| **Language REPL** | `python-repl`, `matlab-repl`, `julia-repl` | Overview → Critical Rules → Spawn Commands → Multiline Code → Backspace → Gotchas → When in Doubt → References → Keep Alive |
| **EDA Extension** | `python-repl-eda`, `matlab-repl-eda`, `julia-repl-eda` | Core Principle → Phase Workflow → Data Loading → Visualization → Iterative Refinement → Gotchas → References → Keep Alive |
| **Reference** | `repl-quick-reference`, `repl-cross-language`, `repl-session-management` | Free-form. Use tables, checklists, decision trees as needed. |
| **Workflow/Test** | `repl-test-*`, `repl-pick-plan`, `repl-review` | Numbered step list + Quick Start or Rules section. |
| **Process** | `writing-a-skill`, `updating-a-skill` | When to Use → Conventions → Checklist → Verification |

## Required Elements

These must appear in every skill of the indicated category:

| Element | Applies To |
|---------|------------|
| `⚠️ Critical: Always append \n to pty_write` | Any skill that uses `pty_write` |
| "After Tasks: Keep REPL Alive" footer | Any skill that spawns a REPL |
| Cross-reference to parent/related skills | All skills |
| Gotchas table (`| Gotcha | Solution |`) | Language REPL, EDA |

## Cross-Referencing

All cross-references are relative from the skill's SKILL.md location. Use paths relative to the `skills/` directory root:

```markdown
<!-- To another skill -->
Load [repl-eda-workflow](../repl-eda-workflow/SKILL.md) for the phase workflow.

<!-- To a reference file within the same skill -->
See [line-editing](references/line-editing.md) for ANSI escape handling.

<!-- To a script/asset within the same skill -->
Use the template at [exec-template.py](assets/exec-template.py).
```

Do **not** use absolute paths or `@` force-load syntax. Skills are intended to be copied to other projects — absolute paths break portability.

## Length Guidelines

| Category | Target Lines |
|----------|-------------|
| Language REPL | 100-170 |
| EDA Extension | 90-155 |
| Reference | 100-160 |
| Workflow/Test | 25-40 |
| Process | 60-120 |

Language REPL skills are the upper bound at ~170 lines. If a skill exceeds this, split it into a base skill + extension (like `*-repl` → `*-repl-eda`).

## After Writing

1. **Load test**: confirm the skill fires when its trigger description matches
2. **Link check**: verify every `../`, `references/`, `scripts/`, `assets/` link resolves to an existing file
3. **Line count**: `wc -l .opencode/skills/<name>/SKILL.md` — within category guidelines?
4. **AGENTS.md**: add the skill to the appropriate table in AGENTS.md (see Skills Overview section)
5. **Commit**: follow repo commit conventions — don't commit secrets, temp files, or node_modules

## Verification Commands

```bash
# Check all cross-references in the new skill resolve
grep -r '\.\./' .opencode/skills/<name>/SKILL.md

# Check line count
wc -l .opencode/skills/<name>/SKILL.md
```
