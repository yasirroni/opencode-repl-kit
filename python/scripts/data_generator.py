#!/usr/bin/env python
"""Generate sample datasets for testing."""

import argparse
import json
import random
import sys
from pathlib import Path


def generate_data(size=10, output=None):
    """Generate sample data.

    Args:
        size: Number of records to generate.
        output: Optional output file path. If None, prints to stdout.
    """
    data = []
    for i in range(size):
        record = {
            "id": i + 1,
            "value": round(random.uniform(1, 100), 2),
            "category": random.choice(["A", "B", "C"]),
            "score": random.randint(0, 100),
        }
        data.append(record)

    if output:
        Path(output).write_text(json.dumps(data, indent=2))
        print(f"Generated {size} records to {output}")
    else:
        json.dump(data, sys.stdout, indent=2)
        print()

    return data


def main():
    parser = argparse.ArgumentParser(description="Generate sample datasets")
    parser.add_argument("--size", type=int, default=10, help="Number of records")
    parser.add_argument("--output", type=str, help="Output file path (JSON)")
    args = parser.parse_args()

    generate_data(size=args.size, output=args.output)


if __name__ == "__main__":
    main()
