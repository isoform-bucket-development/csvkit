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

from modules.visualizer import DataVisualizer
from modules.stats_analyzer import StatisticsAnalyzer


class TestDataVisualizer:
    """Test suite for DataVisualizer class"""

    @pytest.fixture
    def visualizer(self):
        """Create DataVisualizer instance"""
        return DataVisualizer()

    @pytest.fixture
    def analyzer(self):
        """Create StatisticsAnalyzer instance"""
        return StatisticsAnalyzer()

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

    def test_visualizer_instantiation(self, visualizer):
        """Test that DataVisualizer can be instantiated"""
        assert visualizer is not None
        assert isinstance(visualizer, DataVisualizer)

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

    def test_visualization_with_empty_dataframe(self, analyzer):
        """Test visualization handling with empty DataFrame"""
        df = pd.DataFrame()
        statistics = analyzer.analyze(df)

        assert len(statistics) == 0

    def test_visualization_with_single_column(self, analyzer):
        """Test visualization with single column DataFrame"""
        df = pd.DataFrame({'single_col': [1, 2, 3, 4, 5]})
        statistics = analyzer.analyze(df)

        assert len(statistics) == 1
        assert 'single_col' in statistics

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

    def test_visualization_with_all_text_columns(self, analyzer):
        """Test visualization with all text columns"""
        df = pd.DataFrame({
            'col1': ['A', 'B', 'C'],
            'col2': ['X', 'Y', 'Z'],
            'col3': ['P', 'Q', 'R']
        })
        statistics = analyzer.analyze(df)

        text_cols = [
            col for col, stats in statistics.items()
            if stats.get('data_type') == 'Text'
        ]

        assert len(text_cols) == 3

    def test_visualization_with_no_missing_values(self, sample_df):
        """Test visualization when there are no missing values"""
        null_counts = sample_df.isnull().sum()
        has_nulls = null_counts[null_counts > 0]

        assert len(has_nulls) == 0

    def test_visualization_with_large_dataset(self, analyzer):
        """Test visualization data preparation with large dataset"""
        df = pd.DataFrame({
            f'col{i}': np.random.randint(0, 100, 1000)
            for i in range(10)
        })

        statistics = analyzer.analyze(df)

        assert len(statistics) == 10

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


class TestDataVisualizerIntegration:
    """Integration tests for data visualization workflow"""

    def test_complete_visualization_workflow(self):
        """Test complete workflow from DataFrame to visualization data"""
        analyzer = StatisticsAnalyzer()
        visualizer = DataVisualizer()

        # Create test DataFrame
        df = pd.DataFrame({
            'integers': [1, 2, 3, 4, 5],
            'floats': [1.1, 2.2, 3.3, 4.4, 5.5],
            'text': ['A', 'B', 'C', 'D', 'E'],
            'with_nulls': [1, None, 3, None, 5]
        })

        # Analyze
        statistics = analyzer.analyze(df)

        # Prepare visualization data
        # 1. Data type distribution
        data_types = {}
        for stats in statistics.values():
            dtype = stats.get('data_type', 'Unknown')
            data_types[dtype] = data_types.get(dtype, 0) + 1

        assert len(data_types) > 0

        # 2. Missing values
        null_counts = df.isnull().sum()
        has_nulls = null_counts[null_counts > 0]

        assert len(has_nulls) == 1

        # 3. Numeric columns for histograms
        numeric_cols = [
            col for col, stats in statistics.items()
            if stats.get('data_type') in ['Integer', 'Float']
        ]

        assert len(numeric_cols) == 3  # integers, floats, with_nulls

        # 4. Unique values
        unique_data = {
            col_name: stats.get('unique_count', 0)
            for col_name, stats in statistics.items()
        }

        assert len(unique_data) == 4

    def test_visualization_data_accuracy(self):
        """Test accuracy of visualization data preparation"""
        analyzer = StatisticsAnalyzer()

        df = pd.DataFrame({
            'values': [1, 1, 2, 2, 2, 3, 3, 3, 3, 4]
        })

        statistics = analyzer.analyze(df)

        # Verify unique count for visualization
        assert statistics['values']['unique_count'] == 4

        # Verify most frequent values
        most_frequent = statistics['values']['most_frequent']
        assert len(most_frequent) > 0
        assert most_frequent[0]['value'] == '3'  # Most frequent (appears 4 times)
        assert most_frequent[0]['count'] == 4
