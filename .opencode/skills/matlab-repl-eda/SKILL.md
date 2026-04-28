---
name: matlab-repl-eda
description: Use when performing exploratory data analysis in a MATLAB REPL with NetCDF, Arrow, or tabular data. Covers Python bridge for file loading, phase-based exploration, built-in visualization, and iterative refinement via temp .m files.
---

# MATLAB REPL — EDA Patterns

## Core Principle

**State preservation is everything.** Load all data ONCE at the start. All data stays in memory across exploration phases. Each step builds on previous state.

## Phase Workflow

| Phase | Task |
|-------|------|
| A | Load all data (NetCDF via Python bridge, Arrow), inspect sizes/NaN counts |
| B | Grid exploration — vertical profiles, horizontal slices, terrain |
| C | Network topology — degree distribution, connected components |
| D | Node-grid integration — nearest neighbor, residuals |
| E | Edge analysis — weight vs distance correlation |
| F | Visualization — save figures to `data/figures/` |
| G | Consolidation into `scripts/eda_spatial_network.m` |

## Data Loading — Python Bridge (Recommended)

MATLAB's native NetCDF support requires additional toolboxes. Use Python from within MATLAB:

```matlab
% Add Python path
py.sys.path.insert(0, 'python');

% Read NetCDF via xarray
ds = py.xarray.open_dataset('data/grid_data.nc');
ds.load();

% Extract variables as MATLAB arrays
temperature = double(ds{"temperature"}.values);
```

**Alternative:** Generate `.mat` files from Python, load in MATLAB with `load('data/grid.mat')`.

## Visualization — No Backend Selection Needed

MATLAB's built-in plotting works in REPL — no special backend needed:

```matlab
figure;
plot(x, y);
xlabel('X'); ylabel('Y');
saveas(gcf, 'data/figures/output.png');
close;  % IMPORTANT — free memory
```

**Always call `close` after `saveas`** to free memory.

## Iterative Refinement Pattern

```
1. Write exploratory code to temp/my_analysis.m
2. Execute: addpath('temp'); my_analysis();
3. pty_read() → inspect output
4. Edit temp file to refine
5. Repeat until satisfied
6. Move working code to consolidated script
```

## Key Gotchas

| Pitfall | Solution |
|---------|----------|
| No inline function support | Write `.m` file to `temp/` + `addpath` |
| 3D array dimension order | Verify with `size()` after loading |
| Memory from figures | Always `close` after each `saveas` |
| Missing values in mean | Use `'omitnan'` flag: `mean(arr, 'omitnan')` |
| figure not saved before close | Always `saveas` BEFORE `close` |

## References

- [Python bridge](references/python-bridge.md) — Using Python from MATLAB for NetCDF/Arrow loading
