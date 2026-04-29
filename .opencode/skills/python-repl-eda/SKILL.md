---
name: python-repl-eda
description: Use when performing exploratory data analysis in a Python REPL with NetCDF, Arrow, or tabular data. Covers xarray lazy loading, pandas workflows, matplotlib Agg backend for PTY, phase-based exploration, and iterative refinement via temp files.
---

# Python REPL — EDA Patterns

## Core Principle

**State preservation is everything.** Load all data ONCE at the start. All data stays in memory across exploration phases. Each step builds on previous state.

### ⚠️ Critical: Always append `\n` to `pty_write`

When executing temp files: `pty_write(data="exec(open('temp/eda_01_load_data.py').read())\n")` — the `\n` is mandatory. Without it, the text is typed but never executed, and the REPL waits forever. If you see no output after a write, check for missing `\n` first.

## Phase Workflow

| Phase | Task |
|-------|------|
| A | Load all data (NetCDF, Arrow), inspect shapes/dtypes/NaN counts |
| B | Grid exploration — vertical profiles, horizontal slices, terrain |
| C | Network topology — degree distribution, connected components |
| D | Node-grid integration — nearest neighbor, residuals |
| E | Edge analysis — weight vs distance correlation |
| F | Visualization — save figures to `data/figures/` |
| G | Consolidation into `scripts/eda_spatial_network.py` |

See [repl-eda-workflow](../repl-eda-workflow/SKILL.md) for language-agnostic phase descriptions.

## Data Loading

### xarray NetCDF (lazy then load)

```python
import xarray as xr
ds = xr.open_dataset('data/grid_data.nc')  # lazy
ds.load()  # materialize all variables
```

### Arrow via pyarrow

```python
import pyarrow.feather as ff
nodes_df = ff.read_table('data/nodes.arrow').to_pandas()
edges_df = ff.read_table('data/edges.arrow').to_pandas()
```

**Execute via:** `pty_write(data="exec(open('temp/eda_01_load_data.py').read())\n")`

## Visualization — Critical for PTY

```python
import matplotlib
matplotlib.use('Agg')  # MUST be BEFORE importing pyplot
import matplotlib.pyplot as plt

# ... create plot ...

plt.savefig('data/figures/output.png', dpi=120)
plt.close()  # ALWAYS close to free memory
```

**NEVER call `plt.show()`** in PTY — it will hang.

## Iterative Refinement Pattern

```
1. Write exploratory code to temp file
2. Execute: exec(open('temp/explore.py').read())
3. pty_read() → inspect output
4. Edit temp file to refine
5. Repeat until satisfied
6. Move working code to consolidated script
```

**Never refine complex code via repeated pty_write — always write to file first.**

## Key Gotchas

| Pitfall | Solution |
|---------|----------|
| `plt.show()` in PTY | Use `plt.savefig()` only |
| `matplotlib.use('Agg')` after pyplot import | Set backend BEFORE importing pyplot |
| `ds.describe()` on xarray Dataset | Use `ds.to_dataframe().describe()` |
| `pcolormesh` shape mismatch | Use `shading='auto'` |
| `for _, row in df.iterrows()` on large data | Use vectorized numpy/pandas operations |

## References

- [xarray patterns](references/xarray-patterns.md) — lazy loading, slicing, NaN handling
- [matplotlib PTY](references/matplotlib-pty.md) — Agg backend, savefig patterns, figure management

## After EDA: Keep REPL Alive

**Do NOT kill the Python REPL after completing EDA.** Leave it running so the user can inspect loaded DataArrays, run ad-hoc queries, or continue exploration.

**Always tell the user:**
> REPL session `pty_xxxxxxxx` is still running with all data loaded. You can open and interact with it via `/pty-open-background-spy`.

Only kill the REPL if the user explicitly asks you to.
