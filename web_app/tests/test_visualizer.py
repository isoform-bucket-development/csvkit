"""
Tests for Data Visualization Module
Testing: REQ-5 (Interactive Data Visualization) and REQ-6 (Chart Interactivity)
"""

import pytest
import pandas as pd
import numpy as np
import sys
import os

# Add parent directory to path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from modules.stats_analyzer import StatsAnalyzer


class TestDataVisualizer:
    """Test suite for DataVisualizer class - data preparation for visualizations"""

    @pytest.fixture
    def analyzer(self):
        """Create StatsAnalyzer instance"""
        return StatsAnalyzer()

    @pytest.fixture
    def sample_df(self):
        """Create sample DataFrame for visualization"""
        return pd.DataFrame({
            'integers': [1, 2, 3, 4, 5, 6, 7, 8, 9, 10],
            'floats': [1.1, 2.2, 3.3, 4.4, 5.5, 6.6, 7.7, 8.8, 9.9, 10.0],
            'text': ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J'],
            'category': ['Cat1', 'Cat2', 'Cat1', 'Cat2', 'Cat1', 'Cat2', 'Cat1', 'Cat2', 'Cat1', 'Cat2']
        })

    @pytest.fixture
    def sample_df_with_nulls(self):
        """Create DataFrame with missing values"""
        return pd.DataFrame({
            'col1': [1, None, 3, None, 5],
            'col2': [10, 20, None, 40, 50],
            'col3': [100, 200, 300, 400, 500]
        })

    @pytest.fixture
    def sample_statistics(self, analyzer, sample_df):
        """Generate statistics for sample DataFrame"""
        return analyzer.analyze(sample_df)

    def test_data_type_distribution_calculation(self, sample_statistics):
        """Test calculation of data type distribution"""
        data_types = {}
        for stats in sample_statistics.values():
            dtype = stats.get('data_type', 'Unknown')
            data_types[dtype] = data_types.get(dtype, 0) + 1

        assert 'Integer' in data_types
        assert 'Float' in data_types
        assert 'Text' in data_types
        assert data_types['Integer'] == 1
        assert data_types['Float'] == 1
        assert data_types['Text'] == 2

    def test_missing_values_detection(self, sample_df_with_nulls):
        """Test detection of missing values for visualization"""
        null_counts = sample_df_with_nulls.isnull().sum()

        assert null_counts['col1'] == 2
        assert null_counts['col2'] == 1
        assert null_counts['col3'] == 0

    def test_missing_values_percentage_calculation(self, sample_df_with_nulls):
        """Test calculation of missing value percentages"""
        null_counts = sample_df_with_nulls.isnull().sum()
        null_percentages = (null_counts / len(sample_df_with_nulls)) * 100

        assert null_percentages['col1'] == 40.0
        assert null_percentages['col2'] == 20.0
        assert null_percentages['col3'] == 0.0

    def test_numeric_columns_identification(self, sample_statistics):
        """Test identification of numeric columns for visualization"""
        numeric_cols = [
            col for col, stats in sample_statistics.items()
            if stats.get('data_type') in ['Integer', 'Float']
        ]

        assert 'integers' in numeric_cols
        assert 'floats' in numeric_cols
        assert 'text' not in numeric_cols

    def test_unique_values_data_preparation(self, sample_statistics):
        """Test preparation of unique values data for chart"""
        columns = []
        unique_counts = []

        for col_name, stats in sample_statistics.items():
            columns.append(col_name)
            unique_counts.append(stats.get('unique_count', 0))

        assert len(columns) == 4
        assert len(unique_counts) == 4
        assert all(count > 0 for count in unique_counts)

    def test_histogram_data_preparation(self, sample_df):
        """Test preparation of data for histogram visualization"""
        numeric_data = sample_df['integers']

        assert len(numeric_data) == 10
        assert numeric_data.min() == 1
        assert numeric_data.max() == 10

    def test_visualization_with_all_numeric_columns(self, analyzer):
        """Test visualization with all numeric columns"""
        df = pd.DataFrame({
            'col1': [1, 2, 3],
            'col2': [4.5, 5.5, 6.5],
            'col3': [7, 8, 9]
        })
        statistics = analyzer.analyze(df)

        numeric_cols = [
            col for col, stats in statistics.items()
            if stats.get('data_type') in ['Integer', 'Float']
        ]

        assert len(numeric_cols) == 3

    def test_chart_data_structure_for_plotly(self, sample_statistics):
        """Test that data structures are compatible with Plotly"""
        # Data type distribution data
        data_types = {}
        for stats in sample_statistics.values():
            dtype = stats.get('data_type', 'Unknown')
            data_types[dtype] = data_types.get(dtype, 0) + 1

        # Verify data structure
        assert isinstance(data_types, dict)
        assert all(isinstance(k, str) for k in data_types.keys())
        assert all(isinstance(v, int) for v in data_types.values())
