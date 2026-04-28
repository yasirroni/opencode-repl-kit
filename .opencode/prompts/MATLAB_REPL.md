# Prompt Template: MATLAB REPL Exploration

## How to Use

Copy this into your chat when you want an agent to spawn a MATLAB REPL and exercise the PackageName package.

---

Read `AGENTS.md` to understand general agent behavior.

Spawn a MATLAB REPL using PTY. Load the `matlab-repl` skill for the correct spawn command and patterns.

Wait for the `>> ` prompt (takes ~8-12 seconds). Then:
1. Add `matlab/PackageName` to the path
2. Create a `PackageName` instance with sample data
3. Test each method: `filterData()`, `aggregateData()`, `validateData()`
4. Show me the output of each call

If you need to test custom functions, write `.m` files to `temp/` first and use `addpath('temp')` as documented in the skill.

Keep the REPL session alive — I may want to send additional commands.
