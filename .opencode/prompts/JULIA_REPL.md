# Prompt Template: Julia REPL Exploration

## How to Use

Copy this into your chat when you want an agent to spawn a Julia REPL and exercise the PackageName package.

---

Read `AGENTS.md` to understand general agent behavior.

Spawn a Julia REPL using PTY. Load the `julia-repl` skill for the correct spawn command and patterns.

Spawn with `--project=julia/PackageName` to activate the project. Wait for the `julia> ` prompt (~8 seconds). Then:
1. Run `using PackageName` to load the package
2. Test the `greet()` function or any other exported functions
3. If the package has a `Processor` struct or similar, instantiate it and test its methods

If you need to test custom code, write `.jl` files to `temp/` first and use `include("temp/file.jl")` as documented in the skill.

Keep the REPL session alive — I may want to send additional commands.
