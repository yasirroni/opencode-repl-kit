---
name: repl-test-python
description: Use when testing the Python packagename package via REPL — importing, creating Processor instance, testing filter and aggregation methods.
---

# Python REPL — Package Testing

## Instructions

1. Read `AGENTS.md` to understand general agent behavior
2. Use the `python-repl` skill for spawn command and patterns
3. Once REPL is ready:
   - Import the `packagename` package (add `python` to sys.path first)
   - Create a `Processor` instance with sample data `[1, 2, 3, 4, 5]`
   - Test each method: `filter_by()`, `filter_range()`, `sum_agg()`, `mean_agg()`, `count_agg()`, `min_agg()`, `max_agg()`
   - Show the output of each call

## Quick Start

```
# Spawn — see python-repl skill for venv detection and binary discovery
# After detecting venv, use: pty_spawn(command="<venv>/bin/python", title="Python REPL")

# Import
pty_write(data="import sys; sys.path.insert(0, 'python')\n")
pty_write(data="from packagename import Processor\n")

# Create instance
pty_write(data="p = Processor([1, 2, 3, 4, 5])\n")

# Test methods
pty_write(data="print(p.filter_by(3))\n")
pty_write(data="print(p.filter_range(2, 4))\n")
pty_write(data="print(p.sum_agg())\n")
pty_write(data="print(p.mean_agg())\n")
```

For complex code, write to `temp/` first and use `exec(open('temp/file.py').read())`.
