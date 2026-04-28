# OpenCode REPL Kit

A collection of agents and skills for interacting with REPL sessions via the [opencode-pty](https://github.com/shekohex/opencode-pty) plugin. Copy these files to any project that requires REPL interaction — they encode patterns, language-specific gotchas, and best practices that make agents smarter when working with interactive environments.

The agents and skills here were created by agents themselves playing with REPLs — spawning sessions, testing patterns, documenting what works and what fails. The interaction trails live in `temp/`.

## What You Get

### agents/ — Dispatchable Agents

Agents live in `.opencode/agents/` and can be invoked via `@` mention or tab-cycle in OpenCode.

| Agent | Purpose |
|-------|---------|
| `shelldon` | REPL-first agent for debugging, data inspection, and interactive exploration |

More agents may be added later.

### AGENTS.md — Core Agent Behavior

Copy to your project's root as `AGENTS.md`. Contains:

- Behavioral guidelines (think before coding, simplicity, surgical changes, goal-driven execution)
- Universal PTY rules (always append `\n`, one command per write, session lifecycle)
- Pointers to language-specific skills

### skills/ — Language-Specific REPL Guides

Copy the ones you need to your project's `.opencode/skills/`. Each contains:

- **Environment detection** — how to find the right binary, venv, or project before spawning
- **Multiline code patterns** — what works inline vs what needs a file
- **Temp file conventions** — where to write code, how to load it
- **Function redefinition behavior** — what happens when you modify and re-run
- **Session lifecycle** — state persistence, error recovery, kill + respawn
- **Gotchas table** — verified pitfalls and their solutions

| Skill | Languages | Key Patterns |
|-------|-----------|--------------|
| `python-repl` | Python | venv detection, auto-indent trap, `exec()` workflow, IPython magic, autoreload |
| `matlab-repl` | MATLAB | binary detection, no inline functions, `.m` file + `addpath`, MATPOWER |
| `julia-repl` | Julia | binary + Project.toml detection, inline functions, `include()`, pkg> mode |
| `python-repl-eda` | Python | xarray lazy loading, pandas workflows, matplotlib Agg backend |
| `matlab-repl-eda` | MATLAB | Python bridge for data loading, built-in plotting |
| `julia-repl-eda` | Julia | NCDatasets, Arrow, DataFrames, Plots (GR backend) |

Reference skills: `repl-quick-reference`, `repl-cross-language`, `repl-session-management`, `repl-eda-workflow`, `repl-test-python`, `repl-test-matlab`, `repl-test-julia`, `repl-pick-plan`, `repl-review`.

## Quick Start

1. Install the plugin:

```bash
opencode plugin install opencode-pty
```

2. Add the plugin to your opencode config at `~/.opencode/config.json`:

```json
{
  "$schema": "https://opencode.ai/config.json",
  "plugin": ["opencode-pty"]
}
```

3. Copy `AGENTS.md` to your project root
4. Copy the skill files you need to `.opencode/skills/`
5. Copy `.opencode/agents/shelldon.md` to your project's `.opencode/agents/` (optional)
6. Restart OpenCode — the agent loads on startup
7. Customize paths and package names to match your project

## Subagents

### shelldon — REPL-First Agent

**Location**: `.opencode/agents/shelldon.md`

A dispatchable subagent that can be invoked by typing `@shelldon` in your OpenCode chat. It appears in the `@` autocomplete menu after OpenCode restarts.

**What it does**: Before writing code or proposing a fix, shelldon spins up the appropriate REPL (Python, MATLAB, or Julia) and inspects the runtime state — data shapes, types, NaN counts, value ranges, dimensions. Its core thesis: "Everything can be seen in a REPL — and you should look before you leap."

**When to use it**:
- Debugging something and don't know the root cause yet
- Inspecting data before writing processing code
- Verifying behavior interactively before committing to files
- Exploring a library's API without reading documentation

**How to invoke**:
```
@shelldon check the shape and dtype of data/grid_data.nc
@shelldon test the packagename Processor with [1, 2, 3, 4, 5]
@shelldon verify that filter_by works correctly in MATLAB REPL
```

**After restarting OpenCode**, type `@` and `shelldon` should appear in the autocomplete. If it doesn't, verify the file exists at `.opencode/agents/shelldon.md` and restart again.

## Why These Exist

Agents working with REPLs via PTY make the same mistakes:

- Forgetting `\n` at the end of commands (typed but not executed)
- Sending multiple commands in one write (syntax errors)
- Trying to define functions inline in MATLAB (not supported)
- Fighting Python's auto-indent on nested structures
- Not knowing how to reload modified code
- Using hardcoded binary paths that break on different machines

These files encode the answers so agents don't have to learn them from scratch.

## How They Were Built

Every agent and skill in this repo was created by agents themselves through REPL experimentation. The process:

1. Spawn a REPL via PTY
2. Try something — load data, define a function, test a pattern
3. Document what worked, what failed, and why
4. Save the exploration trail to `temp/`
5. Extract the verified patterns into skill files

The test subjects were three parallel data processing packages (MATLAB, Python, Julia) with identical functionality, allowing cross-language comparison.

## Demo Project

This repo also contains the demo project that served as the test subject:

- `matlab/` — MATLAB PackageName package (classdef with filter/aggregate/validate)
- `python/` — Python packagename package (Processor class with filter/aggregate)
- `julia/` — Julia PackageName package (standard Project.toml layout)
- `temp/` — Scratch files from REPL experiments

These packages exist to prove the REPL workflows work. The real deliverable is the instruction files.

## Requirements

- MATLAB R2025b (or compatible version)
- Python 3.10+ with uv
- Julia 1.12+ with juliaup
- opencode with opencode-pty plugin
