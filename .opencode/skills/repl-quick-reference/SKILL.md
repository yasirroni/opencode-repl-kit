---
name: repl-quick-reference
description: Use when you need a one-page reference for REPL patterns across Python, MATLAB, and Julia — spawn commands, write patterns, backspace keys, temp conventions, and load patterns side-by-side.
---

# REPL Quick Reference

## Spawn Commands

| Language | Command |
|----------|---------|
| Python | See `python-repl` skill — detects venv, verifies isolation |
| IPython | See `python-repl` skill — same detection, use `ipython` binary |
| MATLAB | See `matlab-repl` skill — detects binary (macOS/Windows/Linux) |
| Julia | See `julia-repl` skill — detects binary, auto-activates Project.toml |

## Critical Rules — Always Follow

### ⚠️ Rule #1: ALWAYS append `\n` to every `pty_write`

**Without `\n`, the command is TYPED but NOT EXECUTED.** The REPL sits idle waiting for Enter.

```
# WRONG — text is typed, never runs, REPL waits forever:
pty_write(data="include(\"temp/foo.jl\")", id="pty_xxx")

# CORRECT — \n acts as pressing Enter:
pty_write(data="include(\"temp/foo.jl\")\n", id="pty_xxx")
```

**If you sent a command and see no output, assume you forgot `\n` until proven otherwise.**

### Rule #2: Minimize PTY writes — batch when possible

**One task = one pty_write.** Each PTY call adds ~1-5ms latency. For long-running code (>1s), negligible. For short ops, matters.

```
# BAD — 4 PTY calls for independent commands
pty_write(data="using Pkg\n")
pty_write(data="Pkg.activate(...)\n")
pty_write(data="Pkg.instantiate()\n")
pty_write(data="using Revise\n")

# GOOD — 1 PTY call, multiline string
pty_write(data="using Pkg; Pkg.activate(...); Pkg.instantiate(); using Revise\n")

# BEST for exploration — write file, single include
# temp/eda_01.jl
# Then: pty_write(data="include(\"temp/eda_01.jl\")\n")
```

**When to separate into multiple writes:** Only when next command depends on previous output.

### Rule #3: Use correct backspace
Python/Julia: DEL character, MATLAB: Ctrl+H

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

## Gotchas — Language-Specific

### Julia
| Issue | Fix |
|-------|-----|
| `round(Float32, digits=N)` fails | Convert to Float64 first: `round(Float64(x), digits=N)` or use `@printf` |
| No `skipnan` in Statistics | Use `mean(a[.!isnan.(a)])` — only `skipmissing` exists |
| GR "connect: Connection refused" | Harmless — figures still save. Ignore the warning |
| `using Printf` not auto-loaded | Must import explicitly for `@printf` |

### Python
| Issue | Fix |
|-------|-----|
| Auto-indent after `:` | Use file + `exec()` for nested code |
| `python3` has no packages | Use venv binary |

### MATLAB
| Issue | Fix |
|-------|-----|
| No inline functions | Write to `.m` file + `addpath` |
| DEL key prints literal | Use Ctrl+H for backspace |

## When in Doubt

- **Python**: Write to `.py` file, execute with `exec()`
- **MATLAB**: Write to `.m` file, add to path, call by name
- **Julia**: Try inline first, write to `.jl` file for large code, use `include()`

## After Tasks: Keep REPL Alive

**Do NOT kill the REPL after completing tasks.** Leave it running so the user can inspect state, run their own commands, or continue exploration.

**Always tell the user:**
> REPL session `pty_xxxxxxxx` is still running. You can open and interact with it via `/pty-open-background-spy`.

Only kill the REPL if the user explicitly asks you to.
