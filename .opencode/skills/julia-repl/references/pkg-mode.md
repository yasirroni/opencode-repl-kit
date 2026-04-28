# Julia Package Mode (pkg>) — Detailed Reference

## Entering Package Mode

```
# From julia> prompt, send ] to enter pkg mode
pty_write(data="]\n")
# Now at pkg> prompt
```

## Common Pkg Commands

```
# Add packages
add NCDatasets Arrow DataFrames Plots Graphs

# Status
status

# Remove packages
rm PackageName

# Update packages
update

# Instantiate project (install deps from Project.toml)
instantiate
```

## Exiting Package Mode

**Backspace (`\x7f`) exits `pkg>` and returns to `julia>`:**

```
pty_write(data="\x7f")
```

This is necessary because `pty_write` with `]` may not reliably trigger pkg mode, but sending backspace always works to escape it.

## Project Activation via Spawn Flag

Instead of using pkg mode interactively, activate the project at spawn time:

```
# See julia-repl skill for binary detection and Project.toml discovery
pty_spawn(command="<julia-path>", args=["--project=<project-dir>"], title="Julia REPL")
```

Then `using PackageName` works immediately.

## First `using` Triggers Precompilation

The first time you `using` a package, Julia precompiles it. This takes a few seconds. Subsequent spawns use the precompiled cache.
