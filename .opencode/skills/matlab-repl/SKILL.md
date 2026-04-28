---
name: matlab-repl
description: Use when spawning a MATLAB REPL via PTY, sending commands to MATLAB interactive interpreter, or running MATLAB code interactively. Covers -nojvm -nodesktop flags, .m file workflow, addpath patterns, MATPOWER integration, and backspace behavior (use backspace Ctrl+H not DEL).
---

# MATLAB REPL

## Overview

MATLAB REPL does NOT support inline function definitions. All functions must be written to `.m` files and loaded via `addpath`.

## Critical Rules

- **ALWAYS append `\n`** to every `pty_write`
- **ONE command per `pty_write`**
- Use `temp/` directory for `.m` files (project root, gitignored)
- Use **semicolons** to suppress verbose output
- Use **backspace Ctrl+H** for backspace, NOT DEL character

## Spawn Command — MATLAB Binary Detection

MATLAB has no simple `matlab` command on macOS. Detect the binary before spawning:

1. **macOS**: Glob `/Applications/MATLAB_*.app/bin/matlab` to find installed versions
   - If exactly one found → use it
   - If multiple → pick the highest version (lexicographic sort on `R20*`)
   - If none found → **ASK USER**: "Where is MATLAB installed? (common: `/Applications/MATLAB_R2025b.app/bin/matlab`)"
2. **Windows**: `matlab` is typically on PATH — try `pty_spawn(command="matlab", args=["-nojvm", "-nodesktop"])`
3. **Linux**: Usually at `/usr/local/MATLAB/R20*b/bin/matlab` or added to PATH

**Always use** `-nojvm -nodesktop` flags to reduce startup time and resource usage.

```
# Example: after detecting binary at /Applications/MATLAB_R2025b.app/bin/matlab
pty_spawn(command="/Applications/MATLAB_R2025b.app/bin/matlab", args=["-nojvm", "-nodesktop"], title="MATLAB REPL")
```

**Wait ~8-12 seconds** for the `>> ` prompt before sending commands.

## Function Definitions — File Only

MATLAB REPL does NOT support inline functions. Always use `.m` files:

1. Write to `temp/` using write tool (File: `temp/my_function.m`)
2. Add to path: `pty_write(data="addpath('temp');\n")`
3. Call the function: `pty_write(data="result = my_function(15);\n")`

## Function Redefinition

MATLAB checks file timestamps automatically. Modifying a `.m` file and calling the function again uses the new definition. No explicit reload needed.

**Caveat:** If MATLAB has cached the function (MEX file, persistent variable), use `clear functionName` before the change takes effect.

## Backspace — Use Ctrl+H, NOT DEL

| Key | Code | Effect |
|-----|------|--------|
| Backspace | Ctrl+H | Deletes character before cursor |
| DEL | DEL character | Prints literal character, does NOT delete |

**Critical difference:** MATLAB requires Ctrl+H for backspace. Sending DEL produces a literal character, not deletion.

## Line Editing

| Key | Effect |
|-----|--------|
| Backspace (Ctrl+H) | Deletes character before cursor |
| Ctrl+C | Clears line and returns to `>> ` |

**Does NOT work:** Ctrl+U, Ctrl+K, Ctrl+A, Ctrl+E — these produce literal characters or nothing.

## Gotchas

| Gotcha | Solution |
|--------|----------|
| Missing `\n` | Always append `\n` |
| No semicolon | Verbose output printed — use `;` |
| Inline function definition | Error — use `.m` file + `addpath` |
| Using DEL for backspace | Prints literal character — use Ctrl+H |
| MATLAB startup time | Wait ~8-12 seconds for `>> ` prompt |
| Session killed | All state lost — re-add paths after spawn |
| Function not found | Directory not on path — use `addpath('temp')` |
| Stale function | Old version still used — use `clear functionName` |

## When in Doubt

1. Write code to `.m` file in `temp/`
2. Add to path with `addpath('temp')`
3. Call the function directly by name

## References

- [MATPOWER usage](references/matpower-usage.md) — MATPOWER setup, case files, power flow
- [Scripts via batch](references/scripts-via-batch.md) — Running scripts via `matlab -batch`
