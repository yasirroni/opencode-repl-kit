# Prompt Template: Pick and Execute a Plan Item

## How to Use

Copy this into your chat when you want an agent to pick a task from the roadmap and execute it.

---

Read `AGENTS.md` to understand general agent behavior. Then read `.opencode/project/OVERVIEW.md` for project context and `.opencode/project/PLAN.md` for the roadmap.

Pick **one** plan item that is not yet completed. Tell me which one you picked and why.

Create a concise execution plan — what files you'll touch, what you'll build, how you'll verify it. Use deep thinking and maximum effort on planning. Make it as exhaustive as possible.

Store your plan in `.opencode/temp/PLAN_<PLAN_NAME>.md`.

Wait for my approval before implementing.

Once approved:
1. Build the solution
2. Verify it works (test via REPL, run scripts, or whatever is appropriate)
3. Update `.opencode/project/PLAN.md` — remove the completed task
4. Add an entry to `.opencode/project/EXECUTED.md` describing what you did, the decisions you made, and why

If you discover something that changes the scope of the task, tell me before proceeding.

Note: both `PLAN.md` and `EXECUTED.md` should not be numbered.
