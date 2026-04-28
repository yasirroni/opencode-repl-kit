---
name: repl-test-matlab
description: Use when testing the MATLAB PackageName package via REPL — adding to path, creating instance, testing filter and aggregation methods.
---

# MATLAB REPL — Package Testing

## Instructions

1. Read `AGENTS.md` to understand general agent behavior
2. Use the `matlab-repl` skill for spawn command and patterns
3. Wait for the `>> ` prompt (~8-12 seconds), then:
   - Add `matlab/PackageName` to the path
   - Create a `PackageName` instance with sample data
   - Test each method: `filterData()`, `aggregateData()`, `validateData()`
   - Show the output of each call

## Quick Start

```
# Spawn — see matlab-repl skill for binary detection
# After detecting binary, use: pty_spawn(command="<matlab-path>", args=["-nojvm", "-nodesktop"], title="MATLAB REPL")

# Wait 8-12 seconds for >> prompt

# Add to path
pty_write(data="addpath('matlab/PackageName');\n")

# Create instance
pty_write(data="pkg = PackageName([1, 2, 3, 4, 5]);\n")

# Test methods
pty_write(data="disp(pkg.filterData('>', 3));\n")
pty_write(data="disp(pkg.meanAgg());\n")
```

For custom functions, write `.m` files to `temp/` first and use `addpath('temp')`.
