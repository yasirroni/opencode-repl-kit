---
name: julia-repl
description: Use when spawning a Julia REPL via PTY, sending commands to Julia interactive interpreter, or managing Julia packages interactively. Covers --project activation, inline function and struct support, include() workflow, pkg> mode, and full ANSI line editing.
---

# Julia REPL

## Overview

Julia REPL fully supports inline function and struct definitions — unlike MATLAB. Most code can be sent directly without writing to files.

## Critical Rules

- **ALWAYS append `\n`** to every `pty_write`
- **ONE command per `pty_write`**
- Use `temp/` directory for `.jl` files (project root, gitignored)

## Spawn Commands

```
# Standard Julia REPL
pty_spawn(command="/Users/myasirroni/.juliaup/bin/julia", title="Julia REPL")

# With project activated (for using PackageName)
pty_spawn(command="/Users/myasirroni/.juliaup/bin/julia", args=["--project=julia/PackageName"], title="Julia REPL")
```

**Wait ~8 seconds** for the `julia> ` prompt before sending commands.

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
| Missing `\n` | Always append `\n` |
| First `using` | Precompilation delay (~1-3 seconds) — wait |
| Session killed | All state lost — re-include everything |
| Stuck in `pkg>` mode | Send backspace `\x7f` to exit |

## When in Doubt

1. Try inline first — most things work
2. For large code, write to `.jl` file in `temp/`
3. Execute with `include("temp/file.jl")`

## References

- [Package mode](references/pkg-mode.md) — Pkg mode entry/exit, add commands
- [Line editing](references/line-editing.md) — Full ANSI support details
