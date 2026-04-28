# Project Architecture

## File Tree

```
opencode-cli-repl-demo/
├── README.md                    # Project readme
├── .gitignore                   # Git ignore rules
├── AGENTS.md                    # Agent behavioral guidelines, skill discovery
├── .opencode/
│   ├── agents/
│   │   └── shelldon.md          # REPL-first dispatchable agent
│   ├── project/
│   │   ├── PLAN.md              # Active planning and roadmap
│   │   ├── EXECUTED.md          # Completed tasks with decisions and rationale
│   │   ├── OVERVIEW.md          # Project overview and component descriptions
│   │   └── ARCHITECTURE.md      # This file
│   ├── skills/
│   │   ├── python-repl/
│   │   │   ├── SKILL.md         # Python REPL: spawn, multiline, exec(), backspace
│   │   │   ├── references/
│   │   │   │   ├── multiline-patterns.md
│   │   │   │   ├── ipython-magic.md
│   │   │   │   └── line-editing.md
│   │   │   └── assets/
│   │   │       └── exec-template.py
│   │   ├── python-repl-eda/
│   │   │   ├── SKILL.md         # Python EDA: xarray, pandas, matplotlib Agg
│   │   │   ├── references/
│   │   │   │   ├── xarray-patterns.md
│   │   │   │   └── matplotlib-pty.md
│   │   │   └── scripts/
│   │   │       └── eda-checkpoint.py
│   │   ├── matlab-repl/
│   │   │   ├── SKILL.md         # MATLAB REPL: .m files, addpath, MATPOWER
│   │   │   ├── references/
│   │   │   │   ├── matpower-usage.md
│   │   │   │   └── scripts-via-batch.md
│   │   │   └── scripts/
│   │   │       └── addpath-template.m
│   │   ├── matlab-repl-eda/
│   │   │   ├── SKILL.md         # MATLAB EDA: Python bridge, built-in plotting
│   │   │   └── references/
│   │   │       └── python-bridge.md
│   │   ├── julia-repl/
│   │   │   ├── SKILL.md         # Julia REPL: inline functions, include(), pkg>
│   │   │   ├── references/
│   │   │   │   ├── pkg-mode.md
│   │   │   │   └── line-editing.md
│   │   │   └── scripts/
│   │   │       └── include-template.jl
│   │   ├── julia-repl-eda/
│   │   │   ├── SKILL.md         # Julia EDA: NCDatasets, Arrow, DataFrames, Plots
│   │   │   └── references/
│   │   │       └── ncdatasets-julia.md
│   │   ├── repl-quick-reference/
│   │   │   └── SKILL.md         # One-page cheatsheet: all 3 languages
│   │   ├── repl-cross-language/
│   │   │   └── SKILL.md         # Detailed cross-language comparison
│   │   ├── repl-session-management/
│   │   │   └── SKILL.md         # Session lifecycle, pty_read, checkpointing
│   │   ├── repl-eda-workflow/
│   │   │   └── SKILL.md         # Language-agnostic EDA phases (A-G)
│   │   ├── repl-test-python/
│   │   │   └── SKILL.md         # Test Python packagename via REPL
│   │   ├── repl-test-matlab/
│   │   │   └── SKILL.md         # Test MATLAB PackageName via REPL
│   │   ├── repl-test-julia/
│   │   │   └── SKILL.md         # Test Julia PackageName via REPL
│   │   ├── repl-pick-plan/
│   │   │   └── SKILL.md         # Select and execute a plan item
│   │   └── repl-review/
│   │       └── SKILL.md         # Review a completed task
│   └── prompts/
│       ├── EXPLORATORY_DATA_ANALYSIS.md  # EDA workflow prompt (legacy)
│       ├── PICK_PLAN.md          # Plan selection prompt (legacy)
│       ├── REVIEW.md             # Review prompt (legacy)
│       ├── PYTHON_REPL.md       # Python REPL prompt (legacy)
│       ├── MATLAB_REPL.md       # MATLAB REPL prompt (legacy)
│       └── JULIA_REPL.md        # Julia REPL prompt (legacy)
├── data/
│   ├── grid_data.nc             # 50x50x10 atmospheric grid
│   ├── nodes.arrow              # 200 network nodes
│   ├── edges.arrow              # 500 directed edges
│   └── figures/                 # EDA output figures
├── scripts/
│   ├── generate_data.py         # Generate all data files
│   ├── eda_spatial_network.py   # Python EDA script
│   └── eda_spatial_network.jl   # Julia EDA script
├── matlab/
│   ├── README.md                # MATLAB setup and usage
│   ├── scripts/                 # (empty — not yet implemented)
│   └── PackageName/
│       ├── PackageName.m        # Main class definition
│       ├── filterData.m         # Filter operations
│       ├── filterRange.m        # Range filtering
│       ├── sum_agg.m            # Sum aggregation
│       ├── mean_agg.m            # Mean aggregation
│       ├── count_agg.m          # Count aggregation
│       ├── min_agg.m            # Min aggregation
│       ├── max_agg.m            # Max aggregation
│       ├── has_nulls.m          # Null checking
│       ├── validate_types.m     # Type validation
│       ├── check_ranges.m       # Range validation
│       └── summary.m            # Summary statistics
├── python/
│   ├── README.md                # Python setup and usage
│   ├── env/                     # Virtual environment (gitignored)
│   ├── scripts/
│   │   ├── data_generator.py    # Generate sample datasets
│   │   ├── process_batch.py     # Batch processing with argparse
│   │   └── analysis_runner.py   # Full analysis pipeline
│   └── packagename/
│       ├── __init__.py          # Package exports
│       ├── processor.py         # Main Processor class
│       ├── filters.py           # Filter functions
│       └── aggregators.py       # Aggregation functions
├── julia/
│   └── PackageName/
│       ├── Project.toml         # Package metadata
│       └── src/
│           └── PackageName.jl   # Main module definition
└── temp/                        # Temporary files for REPL code execution (gitignored)
```

## Key Directories and Files

### `.opencode/`

OpenCode configuration and instruction files. Skills follow the [Agent Skills specification](https://agentskills.io/specification) — each skill is a directory with `SKILL.md` (YAML frontmatter + instructions) and optional `references/`, `scripts/`, `assets/` subdirectories.

### `AGENTS.md`

Core behavioral guidelines (think before coding, simplicity, surgical changes, goal-driven execution) and skill discovery instructions. Language-specific REPL details are delegated to skills.

#### `project/`

Project documentation split into four focused files:
- `PLAN.md` - Forward-looking: roadmap tasks and demo scenarios
- `EXECUTED.md` - Historical: completed tasks, decisions made, and why
- `OVERVIEW.md` - Contextual: what the project does, component descriptions
- `ARCHITECTURE.md` - Structural: file tree and folder/file explanations

#### `skills/`

Skills are organized as directories with `SKILL.md` files containing YAML frontmatter (`name`, `description`) and instructions. This follows the Anthropic Agent Skills format for progressive disclosure.

**Language REPL skills** (`*-repl/`): General language mechanics — spawn commands, `\n` rules, multiline patterns, backspace behavior, gotchas.

**EDA skills** (`*-repl-eda/`): Task-specific patterns — data loading, exploration phases, domain analysis, visualization, verified findings.

**Reference skills**: `repl-quick-reference/` (single-page cheatsheet), `repl-cross-language/` (detailed comparison tables), `repl-session-management/` (session lifecycle, pty_read best practices).

**Workflow skills**: `repl-eda-workflow/` (language-agnostic EDA phases), `repl-test-python/`, `repl-test-matlab/`, `repl-test-julia/` (package testing), `repl-pick-plan/` (plan selection), `repl-review/` (task review).

#### `prompts/`

Legacy prompt templates. Most have been migrated to workflow skills in `skills/`. Kept for backward compatibility.

### `data/`

Generated datasets used for EDA demonstrations across all three languages:

- `grid_data.nc` — 50x50x10 atmospheric grid with elevation, temperature, pressure, humidity variables (~5% NaN)
- `nodes.arrow` — 200 network nodes with location, elevation, and measured sensor values (~3% NaN)
- `edges.arrow` — 500 directed edges with distance, weight, terrain factor, elevation change
- `figures/` — output directory for EDA visualization scripts (created at runtime)

### `scripts/`

Python and Julia EDA scripts that consume data from `data/`:

- `generate_data.py` — generates all three data files using Python packages (netCDF4, pyarrow, numpy, scipy)
- `eda_spatial_network.py` — Python EDA script with `# %%` jupytext cell blocks, produces 10+ figures
- `eda_spatial_network.jl` — Julia equivalent EDA script using NCDatasets, Arrow, DataFrames, Plots

### `matlab/`

MATLAB subproject containing scripts and the PackageName package.

#### `matlab/scripts/`

**Note**: The `matlab/scripts/` directory is currently empty. Scripts (`data_generator.m`, `process_batch.m`, `analysis_runner.m`) are planned but not yet implemented.

#### `matlab/PackageName/`

MATLAB class-based package. Uses MATLAB's classdef syntax with separate `.m` files for each method. The package is loaded via `addpath('matlab/PackageName')` in the REPL.

### `python/`

Python subproject containing scripts and the packagename package.

#### `python/env/`

Virtual environment created by `uv venv`. Contains the Python interpreter and installed packages (ipython, jupyter, etc.). Excluded from version control.

#### `python/scripts/`

Standalone Python scripts with argparse-based CLI interfaces. Run directly via `python scripts/script_name.py [args]`.

#### `python/packagename/`

Standard Python package with `__init__.py` exports. The Processor class and utility functions are organized into separate modules (processor.py, filters.py, aggregators.py) for clarity.

### `julia/`

Julia subproject containing the PackageName package.

#### `julia/PackageName/`

Standard Julia package with `Project.toml` and `src/` layout. Activated via `--project=julia/PackageName` flag when spawning the REPL, then loaded with `using PackageName`.

### `temp/`

Temporary directory for REPL code execution. All languages use this same directory:

- **Python**: write `.py` files, execute with `exec(open('temp/file.py').read())`
- **MATLAB**: write `.m` files, load with `addpath('temp')`
- **Julia**: write `.jl` files, load with `include("temp/file.jl")`

The directory is gitignored. Do NOT delete temp files by default — users may want to inspect them.
