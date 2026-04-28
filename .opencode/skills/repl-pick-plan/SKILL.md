---
name: repl-pick-plan
description: Use when selecting and executing a plan item from the project roadmap. Guides the agent through reading project docs, picking a task, creating an execution plan, and waiting for approval.
---

# Pick and Execute a Plan Item

## Instructions

1. Read `AGENTS.md` to understand general agent behavior
2. Read `.opencode/project/OVERVIEW.md` to understand the project
3. Read `.opencode/project/PLAN.md` to see the roadmap
4. Pick **one** plan item that is not yet completed. Tell which one and why
5. Create a concise execution plan — what files you'll touch, what you'll build, how you'll verify it
6. Store your plan in `.opencode/temp/PLAN_<PLAN_NAME>.md`
7. **Wait for approval before implementing**

## Once Approved

1. Build the solution
2. Verify it works (test via REPL, run scripts, or whatever is appropriate)
3. Update `.opencode/project/PLAN.md` — mark the task as done or remove it
4. Add an entry to `.opencode/project/EXECUTED.md` describing what you did, decisions made, and why

## Rules

- If you discover something that changes the scope of the task, tell the user before proceeding
- Both `PLAN.md` and `EXECUTED.md` should not be numbered
- Use deep thinking and maximum effort on planning — make it as exhaustive as possible
