# Running Scripts via matlab -batch

Use `matlab -batch` to run standalone scripts without the full interactive REPL:

```bash
matlab -nojvm -nodesktop -batch "run('scripts/data_generator.m')"
```

The `-batch` flag runs MATLAB non-interactively — it accepts a single command string, executes, and exits.

## Common Patterns

```bash
# Run with exit
matlab -nojvm -nodesktop -batch "data_generator; exit"

# Run analysis runner
matlab -nojvm -nodesktop -batch "analysis_runner; exit"
```

## Difference from Interactive REPL

| Feature | `-batch` mode | Interactive REPL |
|---------|--------------|-----------------|
| Session | Single command, then exits | Persistent, stateful |
| State | Lost after each run | Persists between commands |
| Use case | Script execution | Exploration, debugging |
| Output | Printed to stdout | Printed to REPL |

## When to Use Each

- **Use `-batch`** for running complete scripts, CI/CD, automation
- **Use interactive REPL** for exploration, debugging, iterative development
