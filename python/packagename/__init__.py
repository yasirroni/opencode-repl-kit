"""packagename - Data processing package.

Provides Processor class and utility functions for filtering and aggregation.
"""

from .processor import Processor
from .filters import filter_by, filter_range
from .aggregators import sum_agg, mean_agg, count_agg, min_agg, max_agg

__all__ = [
    "Processor",
    "filter_by",
    "filter_range",
    "sum_agg",
    "mean_agg",
    "count_agg",
    "min_agg",
    "max_agg",
]
