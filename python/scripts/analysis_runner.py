#!/usr/bin/env python
"""Run full analysis pipeline."""

import argparse
import json
import sys
from pathlib import Path

# Add package to path for script execution
sys.path.insert(0, str(Path(__file__).parent.parent / "package"))

from data_processor import Processor


def run_analysis(data, output=None):
    """Run full analysis on data.

    Args:
        data: List of dicts.
        output: Optional output file path.

    Returns:
        Summary dict.
    """
    processor = Processor(data)

    summary = {
        "row_count": len(data),
        "overall": processor.summary(),
        "by_category": {},
    }

    # Group by category if present
    if data and "category" in data[0]:
        categories = set(d["category"] for d in data)
        for cat in sorted(categories):
            cat_data = [d for d in data if d["category"] == cat]
            cat_processor = Processor(cat_data)
            summary["by_category"][cat] = cat_processor.summary()

    if output:
        Path(output).write_text(json.dumps(summary, indent=2))
        print(f"Analysis summary written to {output}")

    return summary


def main():
    parser = argparse.ArgumentParser(description="Run full analysis pipeline")
    parser.add_argument("--input", required=True, help="Input JSON file")
    parser.add_argument("--output", help="Output JSON file")
    args = parser.parse_args()

    with open(args.input) as f:
        data = json.load(f)

    summary = run_analysis(data, args.output)
    print(json.dumps(summary, indent=2))


if __name__ == "__main__":
    main()
