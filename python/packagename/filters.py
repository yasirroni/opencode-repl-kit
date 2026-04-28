"""Filter functions for data processing."""


def filter_by(data, column, value, operator="=="):
    """Filter data by a condition on a column.

    Args:
        data: List of dicts or list of values.
        column: Column name (for dict data) or ignored (for list data).
        value: Value to compare against.
        operator: One of "==", "!=", ">", "<", ">=", "<=".

    Returns:
        Filtered list.
    """
    if not data:
        return []

    results = []
    for item in data:
        if isinstance(item, dict):
            item_value = item.get(column)
        else:
            item_value = item

        if operator == "==":
            if item_value == value:
                results.append(item)
        elif operator == "!=":
            if item_value != value:
                results.append(item)
        elif operator == ">":
            if item_value is not None and item_value > value:
                results.append(item)
        elif operator == "<":
            if item_value is not None and item_value < value:
                results.append(item)
        elif operator == ">=":
            if item_value is not None and item_value >= value:
                results.append(item)
        elif operator == "<=":
            if item_value is not None and item_value <= value:
                results.append(item)
        else:
            raise ValueError(f"Unknown operator: {operator}")

    return results


def filter_range(data, column, min_val, max_val):
    """Filter data by a range on a column.

    Args:
        data: List of dicts or list of values.
        column: Column name (for dict data) or ignored (for list data).
        min_val: Minimum value (inclusive).
        max_val: Maximum value (inclusive).

    Returns:
        Filtered list.
    """
    if not data:
        return []

    results = []
    for item in data:
        if isinstance(item, dict):
            item_value = item.get(column)
        else:
            item_value = item

        if item_value is not None and min_val <= item_value <= max_val:
            results.append(item)

    return results
