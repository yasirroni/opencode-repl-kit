---
name: repl-eda-workflow
description: Use when starting an exploratory data analysis session in any language REPL. Covers the phase-based workflow (A through G) that applies to Python, MATLAB, and Julia.
---

# EDA Workflow — Language-Agnostic REPL

## Core Principle

**State preservation is everything.** Load all data ONCE at the start. All data stays in memory across exploration phases. Each step builds on previous state.

### ⚠️ Critical: Always append `\n` to `pty_write`

Every `pty_write` call must end with `\n`. Without it, the text is typed but never executed, and the REPL waits forever. If you send a command and see no output, check for missing `\n` first. See `repl-session-management` for the full diagnostic checklist.

## Phase-Based Workflow

### Phase A: Data Loading & First Inspection

Load all datasets at once. Inspect shapes, dtypes, missing value counts, summary statistics.

### Phase B: Grid Data Exploration

1. **Vertical profiles** — mean of each variable at each altitude level
2. **Horizontal slices** — variable values at specific altitude levels
3. **Terrain elevation** — spatial pattern, min/max/mean
4. **Zonal mean** — variable vs latitude (mean across longitude)

### Phase C: Network Topology

1. **Degree distribution** — in-degree, out-degree, total degree per node
2. **Connected components** — how many? largest/smallest sizes?
3. **Isolated nodes** — count and identify
4. **Node type / region breakdown**

### Phase D: Node-Grid Integration

1. **Elevation lookup** — nearest grid cell for each node
2. **Elevation residual** — node vs grid elevation (RMSE, bias, outliers)
3. **Temperature residual** — measured vs grid model (RMSE, outliers)
4. **Spatial autocorrelation** — do nearby nodes have similar residuals?

### Phase E: Edge Analysis

1. **Weight vs distance** — correlation, scatter with regression
2. **Elevation change** — uphill vs downhill vs flat counts
3. **Terrain factor** — distribution, correlation with weight
4. **Bottleneck edges** — high-weight edges (>75th percentile)

### Phase F: Visualization

Generate all figures. Save to `data/figures/`. Always close/clear after saving.

Figures: `vertical_profiles.png`, `grid_temp_slices.png`, `grid_elevation.png`, `zonal_mean_temp.png`, `degree_distribution.png`, `residual_map.png`, `residual_histograms.png`, `edge_analysis.png`, `network_graph.png`, `summary_stats.png`

### Phase G: Consolidation

Assemble all exploration into a single executable script using language-appropriate cell markers or comment blocks.

## Iterative Refinement Pattern

The recommended workflow is **one temp file per phase**, executed and refined in the REPL:

```
1. Write exploratory code for ONE phase to temp file (e.g., temp/eda_01_load.jl)
2. Execute via language's include/exec pattern: include("temp/eda_01_load.jl")\n
3. pty_read() → inspect output, find errors or interesting results
4. Edit temp file to fix/refine
5. Re-include and verify
6. Move to next phase with new temp file
7. After all phases explored, consolidate into single pipeline script
```

**Rules:**
- Each temp file should be **short and focused** (one phase, one concern)
- **Never type complex code directly in `pty_write`** — always write to temp file first
- Data loaded in early temp files stays in REPL memory for later phases
- When consolidating, merge all working temp files into one script with clear phase markers

**Consolidation destination:** Default is `scripts/eda_spatial_network.jl` (or language equivalent). If the project has a different convention (e.g., `eda/`, `analysis/`), **ask the user** where to place the final pipeline.

## After EDA: Keep REPL Alive

**Do NOT kill the REPL after completing EDA.** Leave it running so the user can:
- Inspect loaded data and variables
- Run their own ad-hoc queries
- Continue exploration interactively

**Always tell the user:**
> REPL session `pty_xxxxxxxx` is still running with all data loaded. You can open and interact with it via `/pty-open-background-spy`.

Only kill the REPL if the user explicitly asks you to.

## Language-Specific Skills

| Language | REPL Skill | EDA Skill |
|----------|-----------|-----------|
| Python | `python-repl` | `python-repl-eda` |
| Julia | `julia-repl` | `julia-repl-eda` |
| MATLAB | `matlab-repl` | `matlab-repl-eda` |

## Data

- `data/grid_data.nc` — 50x50x10 atmospheric grid
- `data/nodes.arrow` — 200 network nodes
- `data/edges.arrow` — 500 directed edges
