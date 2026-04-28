#!/usr/bin/env python
"""Batch processing with argparse."""

import argparse
import json
import sys
from pathlib import Path

# Add package to path for script execution
sys.path.insert(0, str(Path(__file__).parent.parent / "package"))

from data_processor import Processor, filter_by, filter_range, sum_agg, mean_agg


def process(data, operation, column=None, value=None):
    """Process data with the specified operation.

    Args:
        data: List of dicts.
        operation: One of 'filter', 'aggregate', 'validate'.
        column: Column name for filter/aggregate.
        value: Value for filter operation.

    Returns:
        Processed result.
    """
    processor = Processor(data)

    if operation == "filter":
        if column and value is not None:
            return processor.filter_by(column, value, ">").data
        return processor.data

    elif operation == "aggregate":
        return {
            "sum": processor.sum_agg(column),
            "mean": processor.mean_agg(column),
            "count": processor.count_agg(column),
            "min": processor.min_agg(column),
            "max": processor.max_agg(column),
        }

    elif operation == "validate":
        return {
            "valid": all(isinstance(d, dict) for d in data),
            "row_count": len(data),
            "columns": list(data[0].keys()) if data else [],
        }

    else:
        raise ValueError(f"Unknown operation: {operation}")


def main():
    parser = argparse.ArgumentParser(description="Batch data processing")
    parser.add_argument("--input", required=True, help="Input JSON file")
    parser.add_argument("--output", required=True, help="Output JSON file")
    parser.add_argument(
        "--operation",
        choices=["filter", "aggregate", "validate"],
        required=True,
        help="Operation type",
    )
    parser.add_argument("--column", help="Column name")
    parser.add_argument("--value", type=float, help="Filter value")
    args = parser.parse_args()

    with open(args.input) as f:
        data = json.load(f)

    result = process(data, args.operation, args.column, args.value)

    with open(args.output, "w") as f:
        json.dump(result, f, indent=2)

    print(f"Processed {len(data)} records with '{args.operation}' -> {args.output}")


if __name__ == "__main__":
    main()
