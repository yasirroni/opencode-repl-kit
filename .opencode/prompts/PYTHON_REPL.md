# Prompt Template: Python REPL Exploration

## How to Use

Copy this into your chat when you want an agent to spawn a Python REPL and exercise the packagename package.

---

Read `AGENTS.md` to understand general agent behavior.

Spawn a Python REPL using PTY. Load the `python-repl` skill for the correct spawn command and patterns.

Once the REPL is ready:
1. Import the `packagename` package (add `python` to sys.path first)
2. Create a `Processor` instance with sample data `[1, 2, 3, 4, 5]`
3. Test each method: `filter_by()`, `filter_range()`, `sum_agg()`, `mean_agg()`, `count_agg()`, `min_agg()`, `max_agg()`
4. Show me the output of each call

If you need to test complex code, write it to `temp/` first and use `exec(open('temp/file.py').read())` as documented in the skill.

Keep the REPL session alive — I may want to send additional commands.
