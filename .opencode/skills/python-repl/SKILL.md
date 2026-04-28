---
name: python-repl
description: Use when spawning a Python or IPython REPL session via PTY, sending commands to Python interactive interpreter, or debugging Python code interactively. Covers venv paths, multiline patterns, auto-indent traps, exec() workflow, IPython magic, autoreload, and backspace behavior.
---

# Python REPL

## Overview

Python REPL auto-indents after `:`, breaking nested structures sent inline. Use file + `exec()` for anything beyond simple functions.

## Critical Rules

- **ALWAYS append `\n`** to every `pty_write` — without it, command is typed but NOT executed
- **ONE command per `pty_write`** — multiple commands cause syntax errors
- Use `temp/` directory for files (project root, gitignored) — NOT `/tmp/`

## Spawn Commands

```
# Standard Python REPL
pty_spawn(command="python/env/bin/python", title="Python REPL")

# IPython REPL (magic commands, better tracebacks)
pty_spawn(command="python/env/bin/ipython", title="IPython REPL")
```

**Do NOT use `python3`** — it spawns the system Python with no project packages.

## Multiline Code

| Code Type | Approach |
|-----------|----------|
| Variable assignment | Single write: `pty_write(data="x = 42\n")` |
| Simple function (no nested `:`) | Single write with double trailing `\n` |
| if/elif/else in function | **File + exec()** |
| Class with multiple methods | **File + exec()** |
| try/except blocks | **File + exec()** |

**Why inline fails:** REPL auto-indents after each `:`, compounding indentation for nested structures.

## File + exec() Pattern (Recommended)

```
# 1. Write to temp/ using write tool
# File: temp/my_code.py

# 2. Execute in REPL
pty_write(data="exec(open('temp/my_code.py').read())\n")

# 3. Use definitions interactively
pty_write(data="result = my_function(42)\n")
```

Functions defined via `exec()` are available in REPL namespace. Re-executing replaces old definitions.

## Backspace and Cancel

| Key | Code | Effect |
|-----|------|--------|
| Backspace | `\x7f` | Deletes character before cursor |
| Clear line | `\x15` (Ctrl+U) | Clears entire line |
| Move to BOL | `\x01` (Ctrl+A) | Moves cursor to beginning |
| Cancel continuation | `\x03` (Ctrl+C) | Clean exit to `>>>` |

**Use Ctrl+C (`\x03`) to cancel continuation** — better than backspace which can damage the original line.

## IPython Magic

```
%time sum(range(1000000))
%run python/scripts/data_generator.py
%load_ext autoreload
%autoreload 2
```

## Gotchas

| Gotcha | Solution |
|--------|----------|
| Missing `\n` | Always append `\n` |
| Multiple commands in one write | One command per write |
| Nested if/elif/else inline | Use file + exec() |
| Using `python3` instead of venv | Use `python/env/bin/python` |
| Session killed | All state lost — re-import everything |
| Using backspace to cancel continuation | Use Ctrl+C (`\x03`) instead |

## When in Doubt

1. Write complex code to `.py` file in `temp/`
2. Execute with `exec(open('temp/file.py').read())`
3. Use definitions interactively

## References

- [Multiline patterns](references/multiline-patterns.md) — detailed auto-indent analysis, all approaches
- [IPython magic](references/ipython-magic.md) — magic commands, autoreload patterns
- [Line editing](references/line-editing.md) — Ctrl+U/K/A/E, backspace details
