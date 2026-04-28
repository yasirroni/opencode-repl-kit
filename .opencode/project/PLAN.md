# Plan: OpenCode CLI & REPL Demo

## How to Use This File

**PLAN.md** is the forward-looking roadmap — what needs to be done next. It contains pending tasks that agents can pick up and execute.

**Relationship to EXECUTED.md**: When a task from this file is completed, move its description (not just a checkmark) to `.opencode/project/EXECUTED.md` with notes on what was done, decisions made, and why. Do not leave `[x]` markers here — the task either stays as pending or gets moved to EXECUTED.md entirely.

**Workflow**:
1. Pick a pending task from the Roadmap below
2. Write a detailed execution plan in `temp/PLAN_<TASK_NAME>.md` — include files to touch, approach, verification steps
3. Get approval on the plan
4. Execute, verify, then move the task description to EXECUTED.md
5. Update this file to remove the completed task

**Why temp/ for plans?** Detailed plans live in `temp/` so they persist as artifacts. When reviewing why something was designed a certain way, check `temp/` first — it contains the decision trail, failed experiments, and reasoning that led to the final implementation. Don't delete temp/ files by default; they are the audit trail.

## Objective

Build a tri-language (MATLAB + Python + Julia) demo project that proves opencode can interact with CLI scripts and persistent REPL sessions through the opencode-pty plugin. The project mirrors the same data processing logic across all three languages so agents can demonstrate equivalent workflows across different language environments.

## Roadmap

### Implement MATLAB Scripts

The `matlab/scripts/` directory is empty. Create three scripts:

- `data_generator.m` — generates sample datasets, accepts optional size and output file arguments, outputs JSON
- `process_batch.m` — batch processing CLI that accepts input file, output file, and operation type (filter/aggregate/validate)
- `analysis_runner.m` — runs the full analysis pipeline: load data, apply filters, compute aggregates, output summary

These scripts should mirror the behavior of their Python counterparts in `python/scripts/`. An agent should study the Python scripts for the expected CLI interface and output format, then implement the MATLAB versions using MATLAB's `inputname`, `nargin`, and argument parsing patterns.

### Verify Python REPL Integration

The Python side is implemented but needs verified REPL workflows. An agent should spawn a Python REPL via PTY, import the `packagename` package, and exercise all major operations:

- Create a `Processor` instance and call each filter method
- Run each aggregation function
- Test edge cases (empty data, invalid filters)
- Verify the `exec(open('temp/...').read())` pattern works for complex code
- Test IPython REPL if available (magic commands, autoreload)

Document any discrepancies between expected and actual behavior in `EXECUTED.md`. Update `PYTHON_REPL.md` if new gotchas are discovered.

### Verify MATLAB REPL Integration

Once the MATLAB code is implemented (PackageName package and scripts), an agent should spawn a MATLAB REPL via PTY and verify:

- MATLAB starts within the expected 8-12 second window
- `addpath` correctly loads the `PackageName` package
- Class instantiation and method calls work as expected
- Writing `.m` files to `temp/` and calling them via `addpath('temp')` works
- Function redefinition (modifying a `.m` file and re-calling) picks up changes
- MATPOWER integration works (if applicable): load case, run power flow, inspect results

Document findings in `EXECUTED.md`. Update `MATLAB_REPL.md` if new gotchas are discovered.

### Implement Julia PackageName Package

The `julia/PackageName/` package was initialized with a skeleton module. Expand it to mirror the Python and MATLAB implementations:

- Add `Processor` struct with `data` field
- Implement filter methods: `filter_by()`, `filter_range()`
- Implement aggregation methods: `sum_agg()`, `mean_agg()`, `count_agg()`, `min_agg()`, `max_agg()`
- Implement validation methods

The Julia implementation should produce equivalent results to the Python `Processor` class when given the same input data. Use Julia's multiple dispatch and type system idiomatically. An agent should read `python/packagename/` and `matlab/PackageName/` for reference on the expected behavior.

### Cross-Language Output Validation

Run equivalent operations in all three languages and compare outputs to confirm parity:

- Generate the same sample dataset in MATLAB, Python, and Julia
- Apply the same filter operations and compare results
- Compute the same aggregations and verify numerical equivalence
- Ensure JSON output format is compatible between languages

This step validates that the demo accurately shows equivalent workflows. An agent should write a small comparison script or manually verify outputs side by side. Any discrepancies should be documented and resolved.

### Improve REPL Skills Through Systematic Testing

The skill files (`PYTHON_REPL.md`, `MATLAB_REPL.md`, `JULIA_REPL.md`) are the primary reusable artifacts of this project. They need to be comprehensive and battle-tested. Test and document the following gaps:

**Python REPL:**
- `importlib.reload()` behavior via PTY — does it pick up file changes?
- `import` vs `from ... import` — which picks up changes after file modification?
- `KeyboardInterrupt` / Ctrl+C behavior — what happens on long-running commands?
- `sys.modules` cleanup after `exec()`
- `pip install` from within the REPL session

**MATLAB REPL:**
- `classdef` instantiation via PTY — any quirks with handle classes?
- `clear all` / `clear classes` behavior — needed to reload class definitions?
- Struct array creation inline via PTY
- `run()` vs `addpath` + direct call — which is more reliable?

**Julia REPL:**
- Pkg mode (`]`) via PTY — can you add packages interactively?
- `Revise.jl` — Julia's autoreload equivalent, does it work via PTY?
- `mutable struct` vs immutable `struct` — both work inline?
- Help mode (`?`) and shell mode (`;`) — do they work via PTY?
- `LOAD_PATH` manipulation for loading modules outside the active project
- `include()` with struct redefinition — Julia rejects this, what's the error and recovery?

**Cross-cutting:**
- Add a comparison table: which language supports what inline vs needs file
- Document prompt detection patterns (`>>>` vs `>> ` vs `julia> `)
- Document how to handle ANSI escape codes in PTY output

Update each skill file with verified findings. Add a cross-language reference section to each skill.

### Build Demo Scenarios and Examples

Create concrete, reproducible demo sequences that showcase each capability. Each scenario should be a step-by-step sequence an agent can follow:

- **Scenario A**: Start REPL, load package, interactive exploration
- **Scenario B**: Run a script with CLI arguments, inspect output
- **Scenario C**: Write custom code to `temp/`, execute in REPL, iterate on changes
- **Scenario D**: Full pipeline — generate data, process it, produce summary

These scenarios should be documented with exact commands and expected outputs so they can serve as both demos and informal integration tests. Add them to `PLAN.md` under a Demo Scenarios section or as separate example files.

### Final Documentation Review

Once all code is implemented and verified, review all documentation files for accuracy:

- `README.md` — does it match the actual project state?
- `OVERVIEW.md` — are component descriptions accurate?
- `ARCHITECTURE.md` — does the file tree match reality?
- `AGENTS.md` — are the behavioral guidelines still relevant?
- Skill files — are all documented patterns still valid?

Update any stale information. Move completed tasks to `EXECUTED.md` with notes on decisions made. Clear the `PLAN.md` roadmap of completed items.

## Improvements Roadmap

The following items have been completed and moved to `EXECUTED.md`:

- ~~Fix Inconsistencies & Gaps~~ — moved to EXECUTED.md
- ~~Add Quick-Reference Card~~ — moved to EXECUTED.md (`repl-quick-reference` skill)
- ~~Add Cross-Language Comparison Table~~ — moved to EXECUTED.md (`repl-cross-language` skill)
- ~~Add pty_read Best Practices~~ — moved to EXECUTED.md (`repl-session-management` skill)
- ~~Update Project Docs~~ — moved to EXECUTED.md
- ~~Create MATLAB_REPL_EDA.md~~ — moved to EXECUTED.md (`matlab-repl-eda` skill)
- ~~Add Session Management Guide~~ — moved to EXECUTED.md (`repl-session-management` skill)