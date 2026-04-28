# IPython Magic and Autoreload

## Magic Commands

```python
# Time execution
pty_write(data="%time sum(range(1000000))\n")

# Run a script
pty_write(data="%run python/scripts/data_generator.py\n")

# List files
pty_write(data="%ls\n")
```

## Autoreload

IPython can auto-reload modules when source files change:

```python
# Load autoreload extension
pty_write(data="%load_ext autoreload\n")

# Enable auto-reload (2 = reload all modules before every execution)
pty_write(data="%autoreload 2\n")

# Import module
pty_write(data="import sys; sys.path.insert(0, 'python')\n")
pty_write(data="from packagename import mean_agg\n")

# Now modify the source file
# Next call will use the updated code automatically
pty_write(data="print(mean_agg([1, 2, 3, 4, 5]))\n")
```

**Verified:** Changes to `.py` files are picked up without restarting the REPL.

## When to Use IPython vs Standard Python

**Use IPython when:**
- You need `%time` for performance measurement
- You want `%run` to execute scripts in REPL context
- You need autoreload for iterative development
- You want better error tracebacks

**Use standard Python when:**
- You need minimal startup time
- You're running automated scripts
- IPython is not installed
