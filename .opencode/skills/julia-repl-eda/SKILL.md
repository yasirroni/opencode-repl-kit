---
name: julia-repl-eda
description: Use when performing exploratory data analysis in a Julia REPL with NetCDF, Arrow, or tabular data. Covers NCDatasets.jl, Arrow.jl, DataFrames.jl, Plots.jl (GR backend), phase-based exploration, and iterative refinement via temp .jl files.
---

# Julia REPL — EDA Patterns

## Core Principle

**State preservation is everything.** Load all data ONCE at the start. All data stays in memory across exploration phases. Each step builds on previous state.

### ⚠️ Critical: Always append `\n` to `pty_write`

When executing temp files: `pty_write(data="include(\"temp/eda_01_load_data.jl\")\n")` — the `\n` is mandatory. Without it, the text is typed but never executed, and the REPL waits forever. If you see no output after a write, check for missing `\n` first.

## Phase Workflow

| Phase | Task |
|-------|------|
| A | Load all data (NetCDF via NCDatasets, Arrow), inspect sizes/NaN counts |
| B | Grid exploration — vertical profiles, horizontal slices, terrain |
| C | Network topology — degree distribution, connected components |
| D | Node-grid integration — nearest neighbor, residuals |
| E | Edge analysis — weight vs distance correlation |
| F | Visualization — save figures to `data/figures/` |
| G | Consolidation into `scripts/eda_spatial_network.jl` |

## Data Loading

### NetCDF via NCDatasets.jl

```julia
using NCDatasets
ds = NCDataset("data/grid_data.nc")
temperature = ds["temperature"][:,:,:]
pressure = ds["pressure"][:,:,:]
elevation = ds["elevation"][:,:]
lat = ds["lat"][:]
lon = ds["lon"][:]
alt = ds["alt"][:]
close(ds)  # Close after reading
```

### Arrow via Arrow.jl

```julia
using Arrow, DataFrames
nodes_df = DataFrame(Arrow.Table("data/nodes.arrow"))
edges_df = DataFrame(Arrow.Table("data/edges.arrow"))
```

**Execute via:** `pty_write(data="include(\"temp/eda_01_load_data.jl\")\n")`

## Visualization — GR Backend (No Display Required)

```julia
using Plots
gr()  # GR backend — works without display in PTY

# Always use Plots.savefig() — never display()
plot(x, y)
savefig("data/figures/name.png")
clf()  # clear figure after save
```

## Missing Value Handling

```julia
# NCDatasets returns `missing` for fill values — convert to NaN:
temperature = coalesce.(ds["temperature"][:,:,:], Float32(NaN))

# Statistics with NaN — use array filtering, NOT skipna (doesn't exist in Julia)
using Statistics
nanmean(a) = mean(a[.!isnan.(a)])   # mean ignoring NaN
nanstd(a)  = std(a[.!isnan.(a)])    # std ignoring NaN

# For Arrow/DataFrames with Missing type:
mean(skipmissing(df.column))        # works for Missing, not NaN
```

**Critical:** Julia's `Statistics` module has `skipmissing` for `Missing` type but **no `skipnan`** for `NaN`. Always filter with `.!isnan.(a)` for NaN arrays.

## NetCDF Dimension Order (Critical)

**NCDatasets reads NetCDF in FILE dimension order**, NOT Python dimension order:
- File dimension order: `lon x lat x alt` = `(50, 50, 10)`
- Python (numpy) convention: `alt x lat x lon`

```julia
# WRONG (assumes Python dim order):
temp_grid_surf = temperature[1,:,:]

# CORRECT (NCDatasets uses file dimension order lon×lat×alt):
temp_grid_surf = temperature[:,:,10]
```

## Key Gotchas

| Pitfall | Solution |
|---------|----------|
| `display(pl)` in PTY | Tries to open GUI — use `savefig()` only |
| GR "connect: Connection refused" warnings | Harmless — GR tries to connect to display even with `savefig()`. Ignore these; figures still save correctly |
| 1-based indexing vs 0-based in data | Convert offsets when indexing |
| `mean(arr)` with NaN | Returns NaN — use `mean(a[.!isnan.(a)])` (no `skipnan` in Julia) |
| `round(Float32, digits=N)` | **Fails** — Julia's `round` with `digits` doesn't support Float32. Use `round(Float64(x), digits=N)` or `@printf` |
| `searchsortedfirst` edge case | Clamp index to [1, length(arr)] |
| `describe(df)` needs StatsBase | `using StatsBase` or use DataFrames built-in |
| Division by zero in ratios | Filter out zero-denominator values before computing ratios |
| `using Printf` needed for `@printf` | Not auto-loaded — must import explicitly |

## References

- [NCDatasets details](references/ncdatasets-julia.md) — dimension order, missing values, patterns

## After EDA: Keep REPL Alive

**Do NOT kill the Julia REPL after completing EDA.** Leave it running so the user can inspect loaded data, run ad-hoc queries, or continue exploration.

**Always tell the user:**
> REPL session `pty_xxxxxxxx` is still running with all data loaded. You can open and interact with it via `/pty-open-background-spy`.

Only kill the REPL if the user explicitly asks you to.
