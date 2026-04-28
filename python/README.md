# Python Data Processing Demo

## Setup

Create a virtual environment and install dependencies:

```bash
cd python
uv venv env && source env/bin/activate
uv pip install pip ipython jupyter
```

## Usage

### REPL with opencode-pty

Use `/pty-open-background-spy` to start an interactive Python REPL:

```bash
/pty-open-background-spy --command "source env/bin/activate && python -i"
```

Then use `pty_write` to send commands and `pty_read` to see output.

### Manual REPL

Start an interactive Python REPL:

```bash
source env/bin/activate
python -i
```

Then import the package:

```python
from packagename import Processor
```

### Scripts

Run a script:

```bash
source env/bin/activate
python scripts/data_generator.py
```

It needs to be noted that the source command require relative path to the env.

## Project Structure

```
python/
├── env/                    # Virtual environment (created by uv)
├── scripts/
│   ├── data_generator.py
│   ├── process_batch.py
│   └── analysis_runner.py
└── packagename/
    ├── __init__.py
    ├── processor.py
    ├── filters.py
    └── aggregators.py
```

## Scripts

- **data_generator.py** - Generate sample datasets
- **process_batch.py** - Batch processing with argparse
- **analysis_runner.py** - Run full analysis pipeline

## Package

**packagename** package with:
- `Processor` class - Main processor
- `filter_by()`, `filter_range()` - Filter functions
- `sum_agg()`, `mean_agg()`, `count_agg()` - Aggregation functions
