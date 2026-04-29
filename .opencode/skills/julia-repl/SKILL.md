---
name: julia-repl
description: Use when spawning a Julia REPL via PTY, sending commands to Julia interactive interpreter, or managing Julia packages interactively. Covers --project activation, inline function and struct support, include() workflow, pkg> mode, and full ANSI line editing.
---

# Julia REPL

## Overview

Julia REPL fully supports inline function and struct definitions — unlike MATLAB. Most code can be sent directly without writing to files.

## Critical Rules

- **ALWAYS append `\n`** to every `pty_write` — `pty_write` sends raw keystrokes. Without `\n`, the text is typed but NEVER executed. The REPL waits forever for Enter. If you see no output after a write, this is the #1 cause.
- **ONE command per `pty_write`**
- Use `temp/` directory for `.jl` files (project root, gitignored)

## Spawn Commands — Julia Binary + Project Detection

### Julia Binary

1. Try `~/.juliaup/bin/julia` (juliaup installs)
2. Fall back to `julia` (in PATH)
3. If neither works → **ASK USER**: "Where is Julia installed? (common: `~/.juliaup/bin/julia` or `julia` on PATH)"

### Project Activation

Always activate a project-level `Project.toml` to avoid polluting `~/.julia/packages/`:

1. Glob for `**/Project.toml` (excluding `~/.julia/` system-level files)
2. If found → spawn with `--project=<parent-dir>` flag
3. If none found → spawn bare (fine for exploration)

Using `--project` ensures `] add` installs packages into the project's environment, not the global one.

```
# Bare Julia REPL
pty_spawn(command="julia", title="Julia REPL")

# With project activated (after detecting Project.toml in julia/PackageName/)
pty_spawn(command="julia", args=["--project=julia/PackageName"], title="Julia REPL")
```

**Wait ~8 seconds** for the `julia> ` prompt before sending commands.

## Sending Commands — Minimize PTY Writes

**Key insight:** PTY bridge latency accumulates per `pty_write` call. Each call has ~1-5ms overhead. For long-running Julia code (>1s), this is negligible. But for short operations, fewer writes = less overhead.

### Best: File + include(), single pty_write

```
1. Write exploration code to temp/eda_01.jl
2. Single pty_write: include("temp/eda_01.jl")\n
3. Read results
```

**Benchmark (fresh REPL, Pkg setup):**
- 4 separate pty_writes: ~1970ms (Julia) + 4×PTY = ~1980ms total
- Single multiline pty_write: ~1075ms (Julia) + 1×PTY = ~1080ms total
- File + include (1 pty_write): ~1253ms (Julia) + 1×PTY = ~1255ms total

**Winner for complex exploration: File + include()** — edit-friendly, fast enough, single PTY call.

### Good: Multiline single pty_write

```
pty_write(data="using Pkg; Pkg.activate(\"julia/PackageName\"); Pkg.instantiate(); using Revise\n")
```

Best for simple one-time setup where you don't need to iterate.

### Avoid: Multiple sequential pty_writes

Each `pty_write` adds latency. Unless you NEED to read output before sending the next command, don't do this:

```
# BAD — 4 PTY calls for 4 simple commands
pty_write(data="using Pkg\n")
pty_write(data="Pkg.activate(...)\n")
pty_write(data="Pkg.instantiate()\n")
pty_write(data="using Revise\n")
```

**Rule: One task = one pty_write. If you need to send multiple commands, combine them into one multiline write or use a file.**

### When to read after write

- Read when next command DEPENDS on previous output
- Don't read when commands are independent — batch them

## Inline Code — Works for Most Cases

Julia REPL handles multiline blocks correctly in a single write, including nested `if/elseif/else`:

```
pty_write(data="function classify(n)\n    if n > 10\n        return \"large\"\n    elseif n > 5\n        return \"medium\"\n    else\n        return \"small\"\n    end\nend\n")
```

**Verified:** Julia REPL supports inline function definitions, struct definitions, if/else blocks — everything works.

## File + include() — For Larger Code

For larger code blocks or iteration:

1. Write to `temp/` using write tool (File: `temp/my_code.jl`)
2. Execute: `pty_write(data="include(\"temp/my_code.jl\")\n")`
3. Use definitions interactively

## Function Redefinition

Re-including a `.jl` file with the same function names replaces old definitions. Verified: REPL namespace is updated.

## Package Mode (pkg>)

```
# Enter pkg mode
pty_write(data="]\n")

# Exit pkg mode — send backspace
pty_write(data="\x7f")
```

Backspace (`\x7f`) exits `pkg>` and returns to `julia>`.

## Backspace and Line Editing

| Key | Code | Effect |
|-----|------|--------|
| Backspace | `\x7f` | Deletes character before cursor (also exits `pkg>`) |
| Clear line | `\x15` (Ctrl+U) | Clears entire line |
| Kill to EOL | `\x0b` (Ctrl+K) | Kills from cursor to end |
| Move to BOL | `\x01` (Ctrl+A) | Moves cursor to beginning |
| Move to EOL | `\x05` (Ctrl+E) | Moves cursor to end |
| Cancel | `\x03` (Ctrl+C) | Cancels continuation, prints `^C`, returns to prompt |

Julia has **full ANSI terminal line-editing support**.

## Gotchas

| Gotcha | Solution |
|--------|----------|
| Missing `\n` in `pty_write` | **Most common bug.** Text typed but not executed. Fix: send `\n` to run pending text, then always include `\n` in future writes |
| `round(Float32, digits=N)` fails | Julia's `round` with `digits` keyword doesn't support Float32. Use `@printf` or `round(Float64(x), digits=N)` |
| First `using` | Precompilation delay (~1-3 seconds) — wait |
| Session killed | All state lost — re-include everything |
| Stuck in `pkg>` mode | Send backspace `\x7f` to exit |
| `using Printf` needed for `@printf` | Not auto-loaded — must import explicitly |

## When in Doubt

1. Try inline first — most things work
2. For large code, write to `.jl` file in `temp/`
3. Execute with `include("temp/file.jl")`

## References

- [Package mode](references/pkg-mode.md) — Pkg mode entry/exit, add commands
- [Line editing](references/line-editing.md) — Full ANSI support details

## After Tasks: Keep REPL Alive

**Do NOT kill the REPL after completing tasks.** Leave it running so the user can inspect state, run their own commands, or continue exploration.

**Always tell the user:**
> REPL session `pty_xxxxxxxx` is still running. You can open and interact with it via `/pty-open-background-spy`.

Only kill the REPL if the user explicitly asks you to.
