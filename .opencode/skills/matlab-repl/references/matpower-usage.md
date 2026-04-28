# MATPOWER Usage in MATLAB REPL

## Getting the Path

```bash
# Use Python to dynamically resolve the path
python/env/bin/python -c "from matpower import path_matpower; print(path_matpower)"
```

If `matpower` is not installed:
```bash
uv pip install matpower
```

## Adding MATPOWER to MATLAB Path

```matlab
% Add matpower main directory
addpath('python/env/lib/python3.14/site-packages/matpower')

% Add data directory for case files
addpath('python/env/lib/python3.14/site-packages/matpower/data')

% Verify
which case9
which runpf
```

## Basic Power Flow

```matlab
% Load a case
mpc = case9;

% Run AC power flow
results = runpf(mpc);

% Inspect results
disp(results.bus);
disp(results.gen);
```

## Available Case Files

Located in `python/env/lib/python3.14/site-packages/matpower/data/`:
- `case9.m`, `case14.m`, `case30.m`, `case57.m`, `case118.m`, `case300.m`
- `case_ACTIVSg200.m`, `case_ACTIVSg500.m`, `case_ACTIVSg2000.m`, etc.

## Common Functions

| Function | Purpose |
|----------|---------|
| `case9`, `case14`, etc. | Load test case data |
| `runpf(mpc)` | Run AC power flow |
| `runopf(mpc)` | Run optimal power flow |
| `rundcpf(mpc)` | Run DC power flow |
| `rundcopf(mpc)` | Run DC optimal power flow |
