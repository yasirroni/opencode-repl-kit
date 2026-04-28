# Project Overview: OpenCode CLI & REPL Demo

## Objective

Demonstrate opencode's capability of using CLI and REPL with MATLAB, Python, and Julia projects. The primary output of this project is not the packages themselves, but the **AGENTS.md and skills/*.md files** — reusable, battle-tested instruction sets that can be copied to other projects requiring REPL interaction. These documents encode verified PTY patterns, language-specific gotchas, and best practices that make agents smarter when working with interactive environments.

## What is Being Demonstrated

This project showcases three key capabilities:

- **Interactive REPL** - Starting persistent REPL sessions for MATLAB, Python, and Julia where we can test code snippets and explore packages interactively
- **Script execution** - Running standalone scripts with CLI arguments (input file, output file, operation type)
- **Package testing** - Importing and testing package functions in REPL to verify behavior

## Project Structure

Three separate projects (MATLAB, Python, Julia) that process data using filter and aggregate operations. Each project includes:

- **Scripts**: Standalone executables with CLI arguments
- **Package**: Reusable data processing library

## MATLAB Project

**Location**: `matlab/`

### Scripts

- `data_generator.m` - Generate sample datasets
  - Creates sample data arrays (e.g., temperatures, sales figures)
  - Accepts optional arguments for data size and output file
  - Outputs JSON or CSV for cross-language interoperability

- `process_batch.m` - Batch processing with CLI args
  - Input file (path to data file)
  - Output file (path for results)
  - Operation type (filter, aggregate, validate)
  - Demonstrates MATLAB CLI argument passing

- `analysis_runner.m` - Run full analysis pipeline
  - Loads data from file
  - Applies multiple filters
  - Computes aggregates
  - Outputs summary statistics

### Package: PackageName

**Location**: `matlab/PackageName/`

A MATLAB class that provides data processing operations:

- `PackageName.m` - Main class constructor and properties
  - `data` property: stores the input array
  - `metadata` property: stores column names and types

- `filterData.m` - Filter by condition
  - Filter by value equality
  - Filter by range (min/max)
  - Filter by pattern (string matching)

- `aggregateData.m` - Sum/mean/count operations
  - `sum_agg()` - Sum of values
  - `mean_agg()` - Average of values
  - `count_agg()` - Count of non-null values
  - `min_agg()`, `max_agg()` - Min/max values

- `validateData.m` - Data validation helpers
  - Check for null values
  - Validate data types
  - Check value ranges

## Python Project

**Location**: `python/`

### Scripts

- `data_generator.py` - Generate sample datasets
  - Creates sample data using Python lists or dictionaries
  - argparse for CLI argument parsing
  - Outputs JSON for cross-language compatibility

- `process_batch.py` - Batch processing with argparse
  - Arguments: `--input`, `--output`, `--operation`
  - Operations: filter, aggregate, validate
  - Demonstrates Python argparse patterns

- `analysis_runner.py` - Run full analysis pipeline
  - Load data from JSON file
  - Apply multiple filters using packagename functions
  - Compute aggregates
  - Output summary statistics

### Package: packagename

**Location**: `python/packagename/`

A Python package providing data processing operations:

- `__init__.py` - Package exports
  - Exports `Processor` class and utility functions

- `processor.py` - Main Processor class
  - `Processor` class with `data` attribute
  - Methods: `filter_by()`, `filter_range()`, `sum_agg()`, `mean_agg()`, `count_agg()`

- `filters.py` - Filter functions
  - `filter_by(data, column, value, operator)` - Filter by condition
  - `filter_range(data, column, min_val, max_val)` - Filter by range

- `aggregators.py` - Aggregation functions
  - `sum_agg(data, column)` - Sum of values
  - `mean_agg(data, column)` - Average of values
  - `count_agg(data, column)` - Count of non-null values

## Julia Project

**Location**: `julia/`

### Package: PackageName

**Location**: `julia/PackageName/`

A standard Julia package with `Project.toml` and `src/` layout:

- `Project.toml` - Package metadata and dependencies
- `src/PackageName.jl` - Main module definition

The package is activated via `--project=julia/PackageName` flag when spawning the REPL, then loaded with `using PackageName`.

## Skills

The `.opencode/skills/` directory contains reusable instruction files for REPL interaction:

### Base REPL Skills (`*_REPL.md`)

General language mechanics applicable to any REPL task:
- **PYTHON_REPL.md** — spawn command, multiline patterns, IPython magic, package imports, gotchas
- **MATLAB_REPL.md** — spawn command, `.m` file workflow, MATPOWER usage, gotchas
- **JULIA_REPL.md** — spawn command, inline function/struct support, `include()` workflow, package activation, gotchas

### EDA Skills (`*_REPL_EDA.md`)

Task-specific patterns for exploratory data analysis:
- **PYTHON_REPL_EDA.md** — xarray/NetCDF loading, pandas workflows, matplotlib Agg backend, Phase A-G patterns
- **JULIA_REPL_EDA.md** — NCDatasets.jl, Arrow.jl, DataFrames.jl, Plots.jl (GR backend), same Phase A-G workflow

### Reference Skills

- **QUICK_REFERENCE.md** — single-page cheatsheet: spawn commands, write patterns, backspace keys, temp conventions for all 3 languages
- **CROSS_LANGUAGE.md** — detailed comparison tables: inline support, line editing keys, function reload, startup time, prompts

## Prompts

The `.opencode/prompts/` directory contains agent prompt templates for specific tasks:

| Prompt | Purpose |
|--------|---------|
| `EXPLORATORY_DATA_ANALYSIS.md` | Phase-based EDA workflow (language-agnostic) |
| `PICK_PLAN.md` | Select and execute a plan item |
| `REVIEW.md` | Review a completed task for accuracy |
| `PYTHON_REPL.md` | Spawn and test Python REPL |
| `MATLAB_REPL.md` | Spawn and test MATLAB REPL |
| `JULIA_REPL.md` | Spawn and test Julia REPL |

## Demo Scenarios

Step-by-step sequences that demonstrate opencode's REPL capabilities:

| Scenario | Description |
|----------|-------------|
| **A** | Start REPL, load package, interactive exploration |
| **B** | Run a script with CLI arguments, inspect output |
| **C** | Write custom code to `temp/`, execute in REPL, iterate on changes |
| **D** | Full pipeline — generate data, process it, produce summary |

Each scenario produces verifiable output and serves as an informal integration test.
