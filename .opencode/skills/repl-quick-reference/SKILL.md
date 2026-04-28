---
name: repl-quick-reference
description: Use when you need a one-page reference for REPL patterns across Python, MATLAB, and Julia — spawn commands, write patterns, backspace keys, temp conventions, and load patterns side-by-side.
---

# REPL Quick Reference

## Spawn Commands

| Language | Command |
|----------|---------|
| Python | `pty_spawn(command="python/env/bin/python", title="Python REPL")` |
| IPython | `pty_spawn(command="python/env/bin/ipython", title="IPython REPL")` |
| MATLAB | `pty_spawn(command="/Applications/MATLAB_R2025b.app/bin/matlab", args=["-nojvm", "-nodesktop"], title="MATLAB REPL")` |
| Julia | `pty_spawn(command="/Users/myasirroni/.juliaup/bin/julia", args=["--project=julia/PackageName"], title="Julia REPL")` |

## Critical Rules — Always Follow

1. **ALWAYS append `\n`** — without it, command is typed but NOT executed
2. **ONE command per `pty_write`** — multiple commands cause syntax errors
3. **Use correct backspace** — Python/Julia: DEL, MATLAB: Ctrl+H

## Write Patterns — Inline vs File

| Language | Simple Code | Complex Code |
|----------|------------|--------------|
| Python | Single write | File + `exec()` |
| MATLAB | Single write (expressions only) | File + `addpath` |
| Julia | Single write (everything works) | File + `include()` |

## Temp File Conventions

All languages use `temp/` at project root (gitignored):

| Language | File Pattern | Load Command |
|----------|-------------|--------------|
| Python | `temp/file.py` | `exec(open('temp/file.py').read())` |
| MATLAB | `temp/file.m` | `addpath('temp')` then call by name |
| Julia | `temp/file.jl` | `include("temp/file.jl")` |

## Backspace Keys

| Language | Key | Code |
|----------|-----|------|
| Python | DEL | DEL character |
| MATLAB | BS (Ctrl+H) | Ctrl+H |
| Julia | DEL | DEL character |

## Package Loading

| Language | How to Load |
|----------|-------------|
| Python | `sys.path.insert(0, 'python')` then `from packagename import ...` |
| MATLAB | `addpath('matlab/PackageName')` |
| Julia | Spawn with `--project=julia/PackageName`, then `using PackageName` |

## Function Redefinition

| Language | Reload Pattern |
|----------|---------------|
| Python | Re-exec the file — replaces old definition |
| MATLAB | Call the function — auto-reloads (timestamp check) |
| Julia | Re-include — replaces old definition |

## Prompt Formats

| Language | Prompt |
|----------|--------|
| Python | `>>>` |
| IPython | `In [3]:` |
| MATLAB | `>> ` |
| Julia | `julia> ` |

## Startup Time

| Language | Approximate Time |
|----------|-----------------|
| Python | ~1-2 seconds |
| MATLAB | ~8-12 seconds |
| Julia | ~8 seconds (+ precompilation on first `using`) |

## When in Doubt

- **Python**: Write to `.py` file, execute with `exec()`
- **MATLAB**: Write to `.m` file, add to path, call by name
- **Julia**: Try inline first, write to `.jl` file for large code, use `include()`
