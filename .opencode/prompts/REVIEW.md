# Prompt Template: Review a Completed Task

## How to Use

Copy this into your chat when you want an agent to review a recently completed task. Replace the task name in the first line.

---

Review the most recently executed task for "[TASK_NAME]".

Read `AGENTS.md` to understand general agent behavior. Then read `.opencode/project/OVERVIEW.md` for project context and `.opencode/project/EXECUTED.md` to see what has been done.

Check:
1. Does the implementation match what was described in EXECUTED.md?
2. Is the code consistent with the project's patterns (same structure as other language implementations)?
3. Are there any bugs, edge cases, or improvements you notice?
4. Is the documentation (OVERVIEW.md, ARCHITECTURE.md, skill files) still accurate after the changes?

If you find problems or improvements:
- Describe what you found
- Propose how to fix it
- Wait for my approval before making changes

If everything looks good, confirm that the executed task is solid and nothing needs updating.
