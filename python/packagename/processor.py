"""Main Processor class for data processing."""

from .filters import filter_by, filter_range
from .aggregators import sum_agg, mean_agg, count_agg, min_agg, max_agg


class Processor:
    """Main data processor class.

    Wraps a dataset and provides methods for filtering and aggregation.
    """

    def __init__(self, data, column_names=None):
        """Initialize the processor with data.

        Args:
            data: List of dicts or list of values.
            column_names: Optional list of column names for metadata.
        """
        self.data = list(data) if data else []
        self.metadata = {
            "column_names": column_names or [],
            "row_count": len(self.data),
        }

    def filter_by(self, column, value, operator="=="):
        """Filter data by condition.

        Args:
            column: Column name or ignored for list data.
            value: Value to compare.
            operator: One of "==", "!=", ">", "<", ">=", "<=".

        Returns:
            New Processor with filtered data.
        """
        filtered = filter_by(self.data, column, value, operator)
        return Processor(filtered, self.metadata["column_names"])

    def filter_range(self, column, min_val, max_val):
        """Filter data by range.

        Args:
            column: Column name or ignored for list data.
            min_val: Minimum value (inclusive).
            max_val: Maximum value (inclusive).

        Returns:
            New Processor with filtered data.
        """
        filtered = filter_range(self.data, column, min_val, max_val)
        return Processor(filtered, self.metadata["column_names"])

    def sum_agg(self, column=None):
        """Sum of values."""
        return sum_agg(self.data, column)

    def mean_agg(self, column=None):
        """Average of values."""
        return mean_agg(self.data, column)

    def count_agg(self, column=None):
        """Count of non-null values."""
        return count_agg(self.data, column)

    def min_agg(self, column=None):
        """Minimum value."""
        return min_agg(self.data, column)

    def max_agg(self, column=None):
        """Maximum value."""
        return max_agg(self.data, column)

    def summary(self):
        """Get summary statistics.

        Returns:
            Dict with count, sum, mean, min, max.
        """
        return {
            "count": self.count_agg(),
            "sum": self.sum_agg(),
            "mean": self.mean_agg(),
            "min": self.min_agg(),
            "max": self.max_agg(),
        }

    def __repr__(self):
        return f"Processor(data={self.data[:5]}{'...' if len(self.data) > 5 else ''})"
