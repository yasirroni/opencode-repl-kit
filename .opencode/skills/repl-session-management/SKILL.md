---
name: repl-session-management
description: Use when managing REPL session lifecycle — deciding when to kill vs keep alive, running multiple concurrent REPLs, monitoring background sessions, checkpointing state, or recovering from unexpected exits.
---

# REPL Session Management

## When to Keep REPL Alive

- Data has been loaded and is expensive to reload (large datasets, network requests)
- Package precompilation just finished (Julia) — killing loses the cache
- Multiple sequential operations planned in the same language
- User explicitly says "keep session alive"

## When to Kill and Respawn

- REPL is in a bad state (unrecoverable error, infinite loop, frozen)
- Wrong language/version selected and needs to change
- Memory is growing too large from accumulated outputs
- User explicitly asks for a fresh session

## Multiple Concurrent REPLs

- Each `pty_spawn` gets a unique ID (`pty_xxxxxxxx`)
- Use the `title` parameter to identify sessions
- Prefer single session per language unless task explicitly needs parallel REPLs
- Track which ID corresponds to which language/project

## Background Monitoring Pattern

```
# Start background session that runs indefinitely
pty_spawn(command="python/env/bin/python", title="Background Monitor")

# Send a long-running or periodic task
pty_write(data="while True: print('alive'); time.sleep(10)\n")

# Periodically check output (use offset to get latest)
pty_read(id="pty_xxx", offset=(total_lines - 20), limit=20)

# Kill when done
pty_kill(id="pty_xxx", cleanup=true)
```

## State Checkpointing

### Python

```python
import pickle
with open('temp/checkpoint.pkl', 'wb') as f:
    pickle.dump({'data': data, 'results': results}, f)

# On respawn, restore
with open('temp/checkpoint.pkl', 'rb') as f:
    state = pickle.load(f)
```

### MATLAB

```matlab
% Save variables
save('temp/checkpoint.mat')
% On respawn
load('temp/checkpoint.mat')
```

### Julia

```julia
using BSON
BSON.@save "temp/checkpoint.bson" data results
# On respawn
BSON.@load "temp/checkpoint.bson"
```

## Recovery After Unexpected Exit

1. Note which session ID was lost
2. Respawn with same command
3. Re-run initialization (addpath, using, sys.path.insert, etc.)
4. Reload any checkpointed state from temp files
5. Continue from last known good step

## pty_read Best Practices

### When to Read

- Always read after sending a command to verify it executed
- Check for errors before sending the next command
- If no output appears within ~5 seconds, the command may be done or stuck

### Prompt Detection

```
Python standard:    ">>> "
IPython:             "In [3]: "
MATLAB:              ">> "
Julia normal:        "julia> "
Julia package mode:  "pkg> "
```

### Output Volume Handling

- **Small output** (<100 lines): read all with default `pty_read()`
- **Large output** (>500 lines): use `offset` to paginate
- **Very large output**: use `pattern` parameter to filter for errors or key output

### Error Detection

```
Python:    "SyntaxError:", "NameError:", "Traceback (most recent call last)"
MATLAB:    "Error:", "Undefined function or variable", "Error using"
Julia:     "ERROR:", "UndefVarError:", "LoadError:", "MethodError:"
```

### Pattern Filtering Examples

```python
# Find only error lines
pty_read(id="pty_xxx", pattern="Error|Traceback|SyntaxError", ignoreCase=true)

# Check for specific prompt
pty_read(id="pty_xxx", pattern=">>> |In \\[\\d+\\]: |julia> |>> ")

# Read only last 50 lines of large output
pty_read(id="pty_xxx", offset=(total_lines - 50), limit=50)
```

### Recovery Patterns

- If REPL is stuck (no prompt, no output), try sending `\n` to wake it
- If REPL appears dead after error, send a simple command like `print('ok')` to test
- For MATLAB's `>> ` prompt, wait the full 8-12 seconds before reading
