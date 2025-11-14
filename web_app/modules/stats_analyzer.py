"""
Statistical Analysis Module
Analyzes CSV columns and computes comprehensive statistics
Adapted from csvkit's csvstat functionality
"""

import pandas as pd
import numpy as np
import streamlit as st
from typing import Dict, Any, List
from collections import Counter


class StatisticsAnalyzer:
    """Analyzes DataFrame columns and computes statistics"""

    def analyze(self, df: pd.DataFrame) -> Dict[str, Dict[str, Any]]:
        """
        Analyze all columns in the DataFrame

        Returns:
            Dictionary mapping column names to their statistics
        """
        statistics = {}

        for column in df.columns:
            statistics[column] = self.analyze_column(df, column)

        return statistics

    def analyze_column(self, df: pd.DataFrame, column: str) -> Dict[str, Any]:
        """Analyze a single column and return comprehensive statistics"""
        series = df[column]

        stats = {
            'column_name': column,
            'data_type': self._detect_data_type(series),
            'total_count': len(series),
            'non_null_count': series.notna().sum(),
            'null_count': series.isna().sum(),
            'null_percentage': (series.isna().sum() / len(series)) * 100,
            'unique_count': series.nunique(),
        }

        # Type-specific statistics
        if pd.api.types.is_numeric_dtype(series):
            stats.update(self._analyze_numeric(series))
        elif pd.api.types.is_datetime64_any_dtype(series):
            stats.update(self._analyze_datetime(series))
        else:
            stats.update(self._analyze_text(series))

        # Most frequent values
        stats['most_frequent'] = self._get_most_frequent(series, n=5)

        return stats

    def _detect_data_type(self, series: pd.Series) -> str:
        """Detect the data type of a series"""
        if pd.api.types.is_integer_dtype(series):
            return 'Integer'
        elif pd.api.types.is_float_dtype(series):
            return 'Float'
        elif pd.api.types.is_bool_dtype(series):
            return 'Boolean'
        elif pd.api.types.is_datetime64_any_dtype(series):
            return 'DateTime'
        elif pd.api.types.is_timedelta64_dtype(series):
            return 'TimeDelta'
        elif pd.api.types.is_categorical_dtype(series):
            return 'Categorical'
        else:
            return 'Text'

    def _analyze_numeric(self, series: pd.Series) -> Dict[str, Any]:
        """Analyze numeric column"""
        non_null_series = series.dropna()

        if len(non_null_series) == 0:
            return {
                'min': None,
                'max': None,
                'mean': None,
                'median': None,
                'std': None,
                'sum': None,
            }

        return {
            'min': float(non_null_series.min()),
            'max': float(non_null_series.max()),
            'mean': float(non_null_series.mean()),
            'median': float(non_null_series.median()),
            'std': float(non_null_series.std()),
            'sum': float(non_null_series.sum()),
        }

    def _analyze_datetime(self, series: pd.Series) -> Dict[str, Any]:
        """Analyze datetime column"""
        non_null_series = series.dropna()

        if len(non_null_series) == 0:
            return {
                'earliest': None,
                'latest': None,
                'range_days': None,
            }

        earliest = non_null_series.min()
        latest = non_null_series.max()

        return {
            'earliest': str(earliest),
            'latest': str(latest),
            'range_days': (latest - earliest).days if pd.notna(earliest) and pd.notna(latest) else None,
        }

    def _analyze_text(self, series: pd.Series) -> Dict[str, Any]:
        """Analyze text column"""
        non_null_series = series.dropna().astype(str)

        if len(non_null_series) == 0:
            return {
                'min_length': None,
                'max_length': None,
                'avg_length': None,
            }

        lengths = non_null_series.str.len()

        return {
            'min_length': int(lengths.min()),
            'max_length': int(lengths.max()),
            'avg_length': float(lengths.mean()),
        }

    def _get_most_frequent(self, series: pd.Series, n: int = 5) -> List[Dict[str, Any]]:
        """Get the most frequent values"""
        non_null_series = series.dropna()

        if len(non_null_series) == 0:
            return []

        value_counts = non_null_series.value_counts().head(n)

        return [
            {'value': str(val), 'count': int(count)}
            for val, count in value_counts.items()
        ]

    def render_statistics_table(self, statistics: Dict[str, Dict[str, Any]]):
        """Render statistics as an interactive table"""
        # Convert statistics to DataFrame for display
        rows = []

        for col_name, stats in statistics.items():
            row = {
                'Column': col_name,
                'Type': stats.get('data_type', ''),
                'Non-Null': stats.get('non_null_count', 0),
                'Null': stats.get('null_count', 0),
                'Null %': f"{stats.get('null_percentage', 0):.1f}%",
                'Unique': stats.get('unique_count', 0),
            }

            # Add type-specific columns
            if 'min' in stats and stats['min'] is not None:
                row['Min'] = f"{stats['min']:.2f}"
                row['Max'] = f"{stats['max']:.2f}"
                row['Mean'] = f"{stats['mean']:.2f}"
                row['Median'] = f"{stats['median']:.2f}"
                row['Std'] = f"{stats['std']:.2f}"
            elif 'min_length' in stats and stats['min_length'] is not None:
                row['Min Len'] = stats['min_length']
                row['Max Len'] = stats['max_length']
                row['Avg Len'] = f"{stats['avg_length']:.1f}"
            elif 'earliest' in stats and stats['earliest'] is not None:
                row['Earliest'] = stats['earliest']
                row['Latest'] = stats['latest']

            rows.append(row)

        stats_df = pd.DataFrame(rows)

        # Display with filtering options
        st.subheader("Column Statistics")

        # Filter by data type
        data_types = stats_df['Type'].unique().tolist()
        selected_types = st.multiselect(
            "Filter by Data Type",
            options=data_types,
            default=data_types
        )

        filtered_df = stats_df[stats_df['Type'].isin(selected_types)]

        st.dataframe(filtered_df, use_container_width=True, hide_index=True)

        # Display detailed statistics in expander
        with st.expander("📋 Detailed Statistics"):
            for col_name, stats in statistics.items():
                st.markdown(f"**{col_name}** ({stats['data_type']})")

                col1, col2 = st.columns(2)

                with col1:
                    st.write("Basic Statistics:")
                    st.json({
                        k: v for k, v in stats.items()
                        if k not in ['column_name', 'most_frequent']
                    })

                with col2:
                    if stats.get('most_frequent'):
                        st.write("Most Frequent Values:")
                        for item in stats['most_frequent']:
                            st.text(f"  {item['value']}: {item['count']}x")

                st.divider()
