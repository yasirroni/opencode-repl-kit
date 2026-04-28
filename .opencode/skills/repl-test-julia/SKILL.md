---
name: repl-test-julia
description: Use when testing the Julia PackageName package via REPL — activating project, loading package, testing exported functions.
---

# Julia REPL — Package Testing

## Instructions

1. Read `AGENTS.md` to understand general agent behavior
2. Use the `julia-repl` skill for spawn command and patterns
3. Spawn with `--project=julia/PackageName` to activate the project
4. Wait for the `julia> ` prompt (~8 seconds), then:
   - Run `using PackageName` to load the package
   - Test the `greet()` function or any other exported functions
   - If the package has a `Processor` struct or similar, instantiate and test its methods

## Quick Start

```
# Spawn — see julia-repl skill for binary detection and Project.toml activation
# After detecting binary and project, use: pty_spawn(command="<julia-path>", args=["--project=<project-dir>"], title="Julia REPL")

# Wait ~8 seconds for julia> prompt

# Load package
pty_write(data="using PackageName\n")

# Test functions
pty_write(data="PackageName.greet()\n")
```

For custom code, write `.jl` files to `temp/` first and use `include("temp/file.jl")`.
