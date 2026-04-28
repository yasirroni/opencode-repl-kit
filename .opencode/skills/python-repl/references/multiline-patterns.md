# Python Multiline Patterns — Detailed Reference

## The Auto-Indent Trap

Python REPL automatically indents after any line ending with `:`. This compounds for nested structures.

## Approach 1: Single Write — Works for Simple Cases

Send the **ENTIRE block** in ONE `pty_write` with embedded `\n` and **TWO trailing `\n`** (one ends the last line, one blank line ends the block).

```python
# Simple function — WORKS
pty_write(data="def greet(name):\n    return f'Hello, {name}'\n\n")

# Simple class — WORKS
pty_write(data="class Counter:\n    def __init__(self):\n        self.value = 0\n\n")

# Simple loop — WORKS
pty_write(data="for i in range(3):\n    print(i)\n\n")
```

**Fails for:** functions with `if/elif/else`, nested loops, classes with multiple methods, any structure with multiple `:` at different indentation levels.

**Why it fails:**
```python
>>> def classify(n):
...             if n > 10:
...                                 return "large"
...                                     elif n > 5:    # WRONG INDENT!
IndentationError: unexpected indent
```

## Approach 2: Line-by-Line — Works for Simple, Fails for Nested

```python
# Simple function — WORKS
pty_write(data="def greet(name):\n")
pty_write(data="    return f'Hello, {name}'\n")
pty_write(data="\n")  # Blank line to end block
```

**Fails for `if/elif/else`:** After the `if` body executes, REPL is still in continuation mode with compounded indent. Sending `else:` puts it at the wrong level.

## Approach 3: File + exec() — Most Reliable (RECOMMENDED)

For **any complex code**, write to a `.py` file first, then execute:

```python
# Step 1: Write the file (using write tool, NOT pty_write)
# File: temp/my_code.py
def classify(n):
    if n > 10:
        return "large"
    elif n > 5:
        return "medium"
    else:
        return "small"

# Step 2: Execute in REPL
pty_write(data="exec(open('temp/my_code.py').read())\n")

# Step 3: Use the definitions
pty_write(data="print(classify(15))\n")
```

## Function Redefinition

Re-executing a `.py` file with the **same function/class names** **replaces** the old definitions.

**Caveat:** If you had created instances of a class before redefining it, those instances retain the old class behavior. New instances use the new definition.

## Import vs exec()

- `exec(open('temp/file.py').read())` — definitions go into REPL namespace directly
- `import module` — requires `sys.path` setup, module namespace
- `from module import *` — picks up changes only if module was not previously imported
