---
name: repl-session-management
description: Use when managing REPL session lifecycle — deciding when to kill vs keep alive, running multiple concurrent REPLs, monitoring background sessions, checkpointing state, or recovering from unexpected exits.
---

# REPL Session Management

## Default Behavior: Keep REPL Alive After Tasks

**After completing EDA or any REPL-driven task, DO NOT kill the REPL by default.** Leave it running so the user can inspect the session state, run their own commands, or continue exploration.

**Always tell the user** when a REPL session is left alive:
> REPL session `pty_xxxxxxxx` is still running. You can open and interact with it via `/pty-open-background-spy`.

**Only kill the REPL if:**
- The user explicitly asks you to kill it
- REPL is in a truly unrecoverable state (infinite loop, frozen, crashed)
- Memory is growing dangerously large from accumulated outputs

## When to Keep REPL Alive

- Data has been loaded and is expensive to reload (large datasets, network requests)
- Package precompilation just finished (Julia) — killing loses the cache
- Multiple sequential operations planned in the same language
- User explicitly says "keep session alive"
- **Default after EDA** — always leave REPL alive unless user says otherwise

## When to Kill and Respawn

- REPL is in a bad state (unrecoverable error, infinite loop, frozen)
- Wrong language/version selected and needs to change
- Memory is growing too large from accumulated outputs
- User explicitly asks you to kill it or start fresh

## Multiple Concurrent REPLs

- Each `pty_spawn` gets a unique ID (`pty_xxxxxxxx`)
- Use the `title` parameter to identify sessions
- Prefer single session per language unless task explicitly needs parallel REPLs
- Track which ID corresponds to which language/project

## Background Monitoring Pattern

```
# Start background session that runs indefinitely
# See python-repl skill for venv detection and binary discovery
pty_spawn(command="<venv>/bin/python", title="Background Monitor")

# Send a long-running or periodic task
pty_write(data="while True: print('alive'); time.sleep(10)\n")

# Periodically check output (use offset to get latest)
pty_read(id="pty_xxx", offset=(total_lines - 20), limit=20)

# DO NOT kill by default — leave alive for user inspection
# Only kill if user explicitly asks:
# pty_kill(id="pty_xxx", cleanup=true)
```

**After completing work:** Tell the user the session ID and that they can use `/pty-open-background-spy` to interact with it.

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

- **Read after** when you need the output to decide the next action
- **Don't read** when commands are independent — batch them into fewer `pty_write` calls
- **Batch write without reading** when running a sequence of independent commands
- **Read once after a batch** of writes to verify overall success
- If no output appears within ~5 seconds after your final `\n`, the command may be done or stuck

**Key insight: PTY bridge latency accumulates per `pty_write` call. Each call adds ~1-5ms overhead. For long-running Julia/MATLAB code (>1s), this is negligible. But for short operations, fewer writes = less overhead. One task = one pty_write.**

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

- **REPL stuck, no output after pty_write** → 99% chance you forgot `\n`. Send `pty_write(data="\n")` to execute the pending text, then check output.
- **REPL stuck in continuation** → Send `\x03` (Ctrl+C) to cancel and return to prompt.
- **REPL appears dead after error** → Send a simple command like `print('ok')` / `1+1` / `disp('ok')` to test.
- **MATLAB `>> ` prompt not appearing** → Wait the full 8-12 seconds before reading.
