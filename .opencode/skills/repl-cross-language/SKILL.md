---
name: repl-cross-language
description: Use when switching between Python, MATLAB, and Julia REPL workflows or comparing language capabilities. Covers inline support differences, backspace key variations, line editing support, function reload patterns, and startup times.
---

# Cross-Language REPL Comparison

## Inline Code Support

| Code Type | Python | MATLAB | Julia |
|-----------|--------|--------|-------|
| Variable assignment | Yes | Yes | Yes |
| Simple function | Yes | No | Yes |
| if/elif/else in function | No (auto-indent breaks) | No (no inline) | Yes |
| Class/struct definition | No | No | Yes |
| For/while loop | Yes (simple) | Yes (with `...`) | Yes |
| try/except | No | No | Yes |

**Summary:** Julia has the most flexible inline support. Python supports inline for simple structures but fails for nested `:`. MATLAB has NO inline function support.

## Backspace Keys

| Language | Correct Key | Wrong Key | Effect of wrong key |
|----------|-------------|-----------|---------------------|
| Python | DEL | Ctrl+H | Works but non-standard |
| MATLAB | Ctrl+H | DEL | Prints literal character, does NOT delete |
| Julia | DEL | Ctrl+H | Usually works but non-standard |

## Line Editing Keys

| Key | Python | MATLAB | Julia |
|-----|--------|--------|-------|
| Backspace | Yes (DEL) | Yes (Ctrl+H) | Yes (DEL) |
| Clear line (Ctrl+U) | Yes | No | Yes |
| Kill to EOL (Ctrl+K) | No | No | Yes |
| Move to BOL (Ctrl+A) | Yes | No | Yes |
| Move to EOL (Ctrl+E) | Yes | No | Yes |
| Cancel (Ctrl+C) | Yes | Yes | Yes |

**MATLAB has minimal line editing** — only backspace and cancel work. Python and Julia have full ANSI terminal support.

## Function Redefinition

| Language | How to Reload | What Happens |
|----------|---------------|--------------|
| Python | Re-exec the file | Old definition fully replaced |
| MATLAB | Call function (no explicit reload) | Auto-reloads (timestamp check) |
| Julia | Re-include | Old definition fully replaced |

## Session Lifecycle

| Language | State Persists | Error Recovery | Kill + Spawn |
|----------|---------------|---------------|--------------|
| Python | Yes | Yes | Fresh session, all state lost |
| MATLAB | Yes | Yes | Fresh session, all state lost |
| Julia | Yes | Yes | Fresh session, all state lost |

## Startup Time

| Language | Time to First Prompt |
|----------|---------------------|
| Python | ~1-2 seconds |
| MATLAB | ~8-12 seconds |
| Julia | ~8 seconds (+ precompilation) |

## Key Differences Summary

| Aspect | Python | MATLAB | Julia |
|--------|--------|--------|-------|
| Inline functions | Simple only | NEVER | ALWAYS |
| Backspace | DEL | Ctrl+H | DEL |
| Line editing | Full | Minimal | Full |
| Reload | Re-exec file | Auto (timestamp) | Re-include |
| Prompt | `>>>` / `In [n]:` | `>> ` | `julia> ` |
| Startup | ~1-2s | ~8-12s | ~8s |

## When Switching Languages

**From Python to MATLAB:**
- Stop trying inline functions — write `.m` files
- Use Ctrl+H not DEL for backspace
- Add semicolons to suppress output
- Wait longer for startup

**From Python to Julia:**
- Most inline code works — be more flexible
- Use `include()` for files, not `exec()`
- Use `Pkg` mode (]) for packages

**From MATLAB to Python:**
- Simple functions can be sent inline
- Use DEL not Ctrl+H for backspace
- Semicolons optional for clean output

**From MATLAB to Julia:**
- Inline functions work
- Use DEL for backspace
- Use `Pkg` mode for packages

**From Julia to Python:**
- Complex functions need files
- Use `exec()` instead of `include()`

**From Julia to MATLAB:**
- Everything needs `.m` files
- Use Ctrl+H for backspace
- Add semicolons for output suppression
