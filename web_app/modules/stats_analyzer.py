"""
Statistical Analysis Module
Analyzes CSV data and computes comprehensive statistics for each column.
"""

from typing import Dict, Any, List
import pandas as pd
import numpy as np


class StatsAnalyzer:
    """
    Analyzes DataFrame columns and computes comprehensive statistics
    including data types, counts, and type-specific metrics.
    """

    def analyze(self, df: pd.DataFrame) -> Dict[str, Dict[str, Any]]:
        """
        Analyze all columns in a DataFrame and return comprehensive statistics.

        Args:
            df: The pandas DataFrame to analyze

        Returns:
            Dictionary mapping column names to their statistics
        """
        statistics = {}

        for column in df.columns:
            statistics[column] = self.analyze_column(df, column)

        return statistics

    def _detect_data_type(self, series: pd.Series) -> str:
        """
        Detect the data type of a pandas Series.

        Args:
            series: The pandas Series to analyze

        Returns:
            String representing the detected data type
        """
        # Remove null values for type detection
        non_null_series = series.dropna()

        if len(non_null_series) == 0:
            return 'Text'

        # Check for integer type
        if pd.api.types.is_integer_dtype(series):
            return 'Integer'

        # Check for float type
        if pd.api.types.is_float_dtype(series):
            return 'Float'

        # Check for datetime type
        if pd.api.types.is_datetime64_any_dtype(series):
            return 'DateTime'

        # Try to convert to datetime
        try:
            pd.to_datetime(non_null_series, errors='raise')
            return 'DateTime'
        except (ValueError, TypeError):
            pass

        # Check for boolean type
        if pd.api.types.is_bool_dtype(series):
            return 'Boolean'

        # Try to detect boolean from text
        unique_values = set(non_null_series.astype(str).str.lower().unique())
        if unique_values.issubset({'true', 'false', '1', '0', 'yes', 'no'}):
            return 'Boolean'

        # Default to text
        return 'Text'

    def analyze_column(self, df: pd.DataFrame, column: str) -> Dict[str, Any]:
        """
        Analyze a single column and return its statistics.

        Args:
            df: The pandas DataFrame
            column: The column name to analyze

        Returns:
            Dictionary of statistics for the column
        """
        series = df[column]
        data_type = self._detect_data_type(series)

        # Basic statistics for all types
        total_count = len(series)
        non_null_count = series.count()
        null_count = total_count - non_null_count
        null_percentage = (null_count / total_count * 100) if total_count > 0 else 0
        unique_count = series.nunique()

        stats = {
            'data_type': data_type,
            'total_count': total_count,
            'non_null_count': non_null_count,
            'null_count': null_count,
            'null_percentage': round(null_percentage, 2),
            'unique_count': unique_count,
        }

        # Add type-specific statistics
        if data_type in ['Integer', 'Float']:
            stats.update(self._analyze_numeric(series))
        elif data_type == 'Text':
            stats.update(self._analyze_text(series))
        elif data_type == 'DateTime':
            stats.update(self._analyze_datetime(series))

        # Add most frequent values
        stats['most_frequent'] = self._get_most_frequent(series)

        return stats

    def _analyze_numeric(self, series: pd.Series) -> Dict[str, Any]:
        """
        Analyze numeric column and compute statistics.

        Args:
            series: The pandas Series to analyze

        Returns:
            Dictionary of numeric statistics
        """
        non_null_series = series.dropna()

        if len(non_null_series) == 0:
            return {}

        return {
            'min': float(non_null_series.min()),
            'max': float(non_null_series.max()),
            'mean': float(non_null_series.mean()),
            'median': float(non_null_series.median()),
            'std': float(non_null_series.std()) if len(non_null_series) > 1 else 0.0,
            'sum': float(non_null_series.sum()),
        }

    def _analyze_datetime(self, series: pd.Series) -> Dict[str, Any]:
        """
        Analyze datetime column and compute statistics.

        Args:
            series: The pandas Series to analyze

        Returns:
            Dictionary of datetime statistics
        """
        # Convert to datetime if not already
        if not pd.api.types.is_datetime64_any_dtype(series):
            dt_series = pd.to_datetime(series, errors='coerce')
        else:
            dt_series = series

        non_null_series = dt_series.dropna()

        if len(non_null_series) == 0:
            return {}

        earliest = non_null_series.min()
        latest = non_null_series.max()
        range_days = (latest - earliest).days if pd.notna(earliest) and pd.notna(latest) else 0

        return {
            'earliest': str(earliest),
            'latest': str(latest),
            'range_days': range_days,
        }

    def _analyze_text(self, series: pd.Series) -> Dict[str, Any]:
        """
        Analyze text column and compute statistics.

        Args:
            series: The pandas Series to analyze

        Returns:
            Dictionary of text statistics
        """
        non_null_series = series.dropna()

        if len(non_null_series) == 0:
            return {}

        # Convert to string and calculate lengths
        str_series = non_null_series.astype(str)
        lengths = str_series.str.len()

        return {
            'min_length': int(lengths.min()),
            'max_length': int(lengths.max()),
            'avg_length': round(float(lengths.mean()), 2),
        }

    def _get_most_frequent(self, series: pd.Series, n: int = 5) -> List[Dict[str, Any]]:
        """
        Get the most frequent values in a column.

        Args:
            series: The pandas Series to analyze
            n: Number of top values to return (default: 5)

        Returns:
            List of dictionaries with value and count
        """
        value_counts = series.value_counts().head(n)

        return [
            {'value': str(value), 'count': int(count)}
            for value, count in value_counts.items()
        ]
