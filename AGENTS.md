# AGENTS.md

This file, the skills in `.opencode/skills/`, and the agents in `.opencode/agents/` are the primary artifacts of this project. They are designed to be copied to other projects that require REPL interaction. The packages in `matlab/`, `python/`, and `julia/` exist only as test subjects — the real value is the verified PTY patterns, language-specific gotchas, and best practices documented here.

## Core Behavioral Guidelines

### Think Before Coding

Don't assume. Don't hide confusion. Surface tradeoffs.

Before implementing:
- State assumptions explicitly. If uncertain, ask.
- If multiple interpretations exist, present them - don't pick silently.
- If a simpler approach exists, say so. Push back when warranted.
- If something is unclear, stop. Name what's confusing. Ask.

### Simplicity First

Minimum code that solves the problem. Nothing speculative.

- No features beyond what was asked.
- No abstractions for single-use code.
- No "flexibility" or "configurability" that wasn't requested.
- No error handling for impossible scenarios.
- If you write 200 lines and it could be 50, rewrite it.

### Surgical Changes

Touch only what you must. Clean up only your own mess.

When editing existing code:
- Don't "improve" adjacent code, comments, or formatting.
- Don't refactor things that aren't broken.
- Match existing style, even if you'd do it differently.
- If you notice unrelated dead code, mention it - don't delete it.

When your changes create orphans:
- Remove imports/variables/functions that YOUR changes made unused.
- Don't remove pre-existing dead code unless asked.

### Goal-Driven Execution

Define success criteria. Loop until verified.

Transform tasks into verifiable goals:
- "Add validation" → "Write tests for invalid inputs, then make them pass"
- "Fix the bug" → "Write a test that reproduces it, then make them pass"
- "Refactor X" → "Ensure tests pass before and after"

For multi-step tasks, state a brief plan:
```
1. [Step] → verify: [check]
2. [Step] → verify: [check]
3. [Step] → verify: [check]
```

## Skills Overview

Before working with any REPL, check if a skill in `.opencode/skills/` applies. Skills use YAML frontmatter with `name` and `description` fields — the description tells you when to use the skill.

### Language REPL Skills

| Skill | When to Use |
|-------|-------------|
| `python-repl` | Spawning Python/IPython REPL, sending commands, multiline patterns |
| `matlab-repl` | Spawning MATLAB REPL, .m file workflow, MATPOWER |
| `julia-repl` | Spawning Julia REPL, inline functions, pkg> mode |

### EDA Skills

| Skill | When to Use |
|-------|-------------|
| `python-repl-eda` | EDA in Python REPL with NetCDF, Arrow, xarray, matplotlib |
| `matlab-repl-eda` | EDA in MATLAB REPL with Python bridge, built-in plotting |
| `julia-repl-eda` | EDA in Julia REPL with NCDatasets, Arrow, DataFrames, Plots |

### Reference Skills

| Skill | When to Use |
|-------|-------------|
| `repl-quick-reference` | One-page reference: spawn commands, write patterns, backspace keys |
| `repl-cross-language` | Comparing Python/MATLAB/Julia REPL capabilities |
| `repl-session-management` | Session lifecycle, pty_read best practices, checkpointing, recovery |

### Workflow & Test Skills

| Skill | When to Use |
|-------|-------------|
| `repl-eda-workflow` | Starting an EDA session in any language — phase-based workflow (A-G) |
| `repl-test-python` | Testing the Python packagename package via REPL |
| `repl-test-matlab` | Testing the MATLAB PackageName package via REPL |
| `repl-test-julia` | Testing the Julia PackageName package via REPL |
| `repl-pick-plan` | Selecting and executing a plan item from the project roadmap |
| `repl-review` | Reviewing a completed task against EXECUTED.md |

### Process Skills

| Skill | When to Use |
|-------|-------------|
| `writing-a-skill` | Creating a new skill in this repo — conventions and checklist |
| `updating-a-skill` | Modifying an existing skill — what can/cannot change, verification |

### Skill Structure

Each skill is a directory with `SKILL.md` (YAML frontmatter + instructions) and optional `references/`, `scripts/`, `assets/` subdirectories. Skills follow the [Agent Skills specification](https://agentskills.io/specification).

### Skill Separation Principle

**`*-repl` skills** cover general language mechanics (spawn, `\n` rules, multiline patterns, backspace). **`*-repl-eda` skills** cover task-specific patterns (data loading, exploration phases, visualization).

**Rule of thumb:** If the pattern exists in Python, MATLAB, and Julia REPL for the same reason, it belongs in the base `*-repl` skill. If it's unique to EDA workflows, it belongs in `*-repl-eda`.

## Agents

This project includes dispatchable subagents in `.opencode/agents/`. Agents are standalone entities with their own decision loop, tool access, and behavior rules — unlike skills which are reusable instruction sets loaded into another agent's context.

| Agent | When to Dispatch |
|-------|-----------------|
| `shelldon` | REPL-first debugging, data inspection, interactive exploration. Spins up the right REPL, checks runtime state before writing code, and leaves a trail of temp/ files. |

Agent files use YAML frontmatter with `description` and `mode: primary` fields (vs skills which use `name` and `description`).

## Investigation Order

1. README*, root manifests, workspace config, lockfiles
2. build, test, lint, formatter, typecheck config
3. CI workflows and pre-commit/task runner config
4. Existing instruction files (AGENTS.md, CLAUDE.md, .opencode/)
5. Repo-local OpenCode config (opencode.json)

## What to Extract

- Exact developer commands (especially non-obvious ones)
- How to run a single test, package, or focused verification
- Required command order (e.g., `lint -> typecheck -> test`)
- Monorepo boundaries, ownership, entrypoints
- Framework/toolchain quirks: codegen, migrations, env loading, dev servers
- Repo-specific style conventions that differ from defaults
- Testing quirks: fixtures, integration test prerequisites, snapshot workflows

## Writing Rules

Include only high-signal, repo-specific guidance:
- Exact commands the agent would otherwise guess wrong
- Architecture notes not obvious from filenames
- Setup requirements and operational gotchas

Exclude:
- Generic software advice
- Long tutorials or exhaustive file trees
- Obvious language conventions
- Speculative claims

## Questions

Only ask if the repo cannot answer something important. Use `question` tool for one short batch at most. Do not ask about anything the repo already makes clear.
