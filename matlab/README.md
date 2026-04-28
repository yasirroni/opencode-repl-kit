# MATLAB Data Processing Demo

## Setup

MATLAB R2025b is installed at `/Applications/MATLAB_R2025b.app/bin/matlab`.

## MATPOWER

MATPOWER is available via the Python `matpower` pip package.

### Getting the MATPOWER Path

Use Python to dynamically resolve the path:

```bash
python/env/bin/python -c "from matpower import path_matpower; print(path_matpower)"
```

If `matpower` is not installed:

```bash
uv pip install matpower
```

### Adding MATPOWER to MATLAB Path

In the MATLAB REPL:

```matlab
addpath('python/env/lib/python3.14/site-packages/matpower')
addpath('python/env/lib/python3.14/site-packages/matpower/data')
```

## Usage

### REPL with opencode-pty

Use `/pty-open-background-spy` or `pty_spawn` to start an interactive MATLAB REPL:

```
pty_spawn(command="/Applications/MATLAB_R2025b.app/bin/matlab", args=["-nojvm", "-nodesktop"], title="MATLAB REPL")
```

Wait for the `>> ` prompt (~8-12 seconds), then add paths:

```matlab
addpath('python/env/lib/python3.14/site-packages/matpower')
addpath('python/env/lib/python3.14/site-packages/matpower/data')
addpath('PackageName')
```

Then use `pty_write` to send commands and `pty_read` to see output.

### Scripts

Run a script:

```bash
/Applications/MATLAB_R2025b.app/bin/matlab -nojvm -nodesktop -batch "run('scripts/data_generator.m')"
```

### Custom Functions

Write `.m` files to `temp/` (gitignored) and add to path:

```matlab
addpath('temp')
result = my_function(42);
```

## Project Structure

```
matlab/
├── PackageName/
│   ├── PackageName.m
│   ├── filterData.m
│   ├── aggregateData.m
│   └── validateData.m
└── scripts/
    ├── data_generator.m
    ├── process_batch.m
    └── analysis_runner.m
```

## Package

**PackageName** class with methods:
- `filterData` - Filter by condition
- `aggregateData` - Sum/mean/count operations
- `validateData` - Data validation helpers

## See Also

- `.opencode/skills/MATLAB_REPL.md` — Comprehensive REPL skill guide with workflows and gotchas
