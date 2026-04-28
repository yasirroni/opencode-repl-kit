"""Aggregation functions for data processing."""


def sum_agg(data, column=None):
    """Sum of values in a column.

    Args:
        data: List of dicts or list of numbers.
        column: Column name (for dict data) or None (for list data).

    Returns:
        Sum of values.
    """
    if not data:
        return 0

    total = 0
    for item in data:
        if isinstance(item, dict):
            val = item.get(column, 0)
        else:
            val = item
        if val is not None:
            total += val
    return total


def mean_agg(data, column=None):
    """Average of values in a column.

    Args:
        data: List of dicts or list of numbers.
        column: Column name (for dict data) or None (for list data).

    Returns:
        Mean of values, or 0 if empty.
    """
    if not data:
        return 0

    total = 0
    count = 0
    for item in data:
        if isinstance(item, dict):
            val = item.get(column)
        else:
            val = item
        if val is not None:
            total += val
            count += 1

    return total / count if count > 0 else 0


def count_agg(data, column=None):
    """Count of non-null values in a column.

    Args:
        data: List of dicts or list of values.
        column: Column name (for dict data) or None (for list data).

    Returns:
        Count of non-null values.
    """
    if not data:
        return 0

    count = 0
    for item in data:
        if isinstance(item, dict):
            val = item.get(column)
        else:
            val = item
        if val is not None:
            count += 1
    return count


def min_agg(data, column=None):
    """Minimum value in a column.

    Args:
        data: List of dicts or list of numbers.
        column: Column name (for dict data) or None (for list data).

    Returns:
        Minimum value, or None if empty.
    """
    if not data:
        return None

    values = []
    for item in data:
        if isinstance(item, dict):
            val = item.get(column)
        else:
            val = item
        if val is not None:
            values.append(val)

    return min(values) if values else None


def max_agg(data, column=None):
    """Maximum value in a column.

    Args:
        data: List of dicts or list of numbers.
        column: Column name (for dict data) or None (for list data).

    Returns:
        Maximum value, or None if empty.
    """
    if not data:
        return None

    values = []
    for item in data:
        if isinstance(item, dict):
            val = item.get(column)
        else:
            val = item
        if val is not None:
            values.append(val)

    return max(values) if values else None
