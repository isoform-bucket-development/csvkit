"""
Tests for Statistical Analysis Module
Testing: REQ-3 (Automatic Statistical Analysis) and REQ-4 (Statistical Results Display)
"""

import pytest
import pandas as pd
import numpy as np
import sys
import os
from datetime import datetime, timedelta

# Add parent directory to path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from modules.stats_analyzer import StatisticsAnalyzer


class TestStatisticsAnalyzer:
    """Test suite for StatisticsAnalyzer class"""

    @pytest.fixture
    def analyzer(self):
        """Create StatisticsAnalyzer instance"""
        return StatisticsAnalyzer()

    @pytest.fixture
    def sample_numeric_df(self):
        """Create DataFrame with numeric columns"""
        return pd.DataFrame({
            'integers': [1, 2, 3, 4, 5, 6, 7, 8, 9, 10],
            'floats': [1.1, 2.2, 3.3, 4.4, 5.5, 6.6, 7.7, 8.8, 9.9, 10.0],
            'mixed': [10, 20, 30, 40, 50, 60, 70, 80, 90, 100]
        })

    @pytest.fixture
    def sample_text_df(self):
        """Create DataFrame with text columns"""
        return pd.DataFrame({
            'names': ['Alice', 'Bob', 'Charlie', 'David', 'Eve', 'Frank', 'Grace', 'Henry', 'Ivy', 'Jack'],
            'cities': ['New York', 'Los Angeles', 'Chicago', 'Houston', 'Phoenix', 'Philadelphia', 'San Antonio', 'San Diego', 'Dallas', 'San Jose'],
            'codes': ['A1', 'B2', 'C3', 'D4', 'E5', 'F6', 'G7', 'H8', 'I9', 'J10']
        })

    @pytest.fixture
    def sample_datetime_df(self):
        """Create DataFrame with datetime columns"""
        start_date = datetime(2020, 1, 1)
        return pd.DataFrame({
            'dates': [start_date + timedelta(days=i) for i in range(10)],
            'timestamps': pd.date_range('2020-01-01', periods=10, freq='D')
        })

    @pytest.fixture
    def sample_missing_values_df(self):
        """Create DataFrame with missing values"""
        return pd.DataFrame({
            'col_with_nulls': [1, None, 3, None, 5, None, 7, None, 9, None],
            'col_all_nulls': [None] * 10,
            'col_no_nulls': list(range(10))
        })

    @pytest.fixture
    def sample_mixed_types_df(self):
        """Create DataFrame with mixed data types"""
        return pd.DataFrame({
            'integers': [1, 2, 3, 4, 5],
            'floats': [1.1, 2.2, 3.3, 4.4, 5.5],
            'strings': ['a', 'b', 'c', 'd', 'e'],
            'booleans': [True, False, True, False, True],
            'dates': pd.date_range('2020-01-01', periods=5)
        })

    def test_detect_data_type_integer(self, analyzer, sample_numeric_df):
        """Test detection of integer data type"""
        dtype = analyzer._detect_data_type(sample_numeric_df['integers'])
        assert dtype == 'Integer'

    def test_detect_data_type_float(self, analyzer, sample_numeric_df):
        """Test detection of float data type"""
        dtype = analyzer._detect_data_type(sample_numeric_df['floats'])
        assert dtype == 'Float'

    def test_detect_data_type_text(self, analyzer, sample_text_df):
        """Test detection of text data type"""
        dtype = analyzer._detect_data_type(sample_text_df['names'])
        assert dtype == 'Text'

    def test_detect_data_type_datetime(self, analyzer, sample_datetime_df):
        """Test detection of datetime data type"""
        dtype = analyzer._detect_data_type(sample_datetime_df['dates'])
        assert dtype == 'DateTime'

    def test_detect_data_type_boolean(self, analyzer, sample_mixed_types_df):
        """Test detection of boolean data type"""
        dtype = analyzer._detect_data_type(sample_mixed_types_df['booleans'])
        assert dtype == 'Boolean'

    def test_analyze_numeric_column(self, analyzer, sample_numeric_df):
        """Test analysis of numeric column"""
        stats = analyzer._analyze_numeric(sample_numeric_df['integers'])

        assert stats['min'] == 1.0
        assert stats['max'] == 10.0
        assert stats['mean'] == 5.5
        assert stats['median'] == 5.5
        assert stats['sum'] == 55.0
        assert 'std' in stats
        assert stats['std'] > 0

    def test_analyze_numeric_column_with_nulls(self, analyzer, sample_missing_values_df):
        """Test analysis of numeric column with null values"""
        stats = analyzer._analyze_numeric(sample_missing_values_df['col_with_nulls'])

        assert stats['min'] == 1.0
        assert stats['max'] == 9.0
        assert stats['mean'] == 5.0
        assert stats['median'] == 5.0
        assert 'std' in stats

    def test_analyze_numeric_column_all_nulls(self, analyzer, sample_missing_values_df):
        """Test analysis of numeric column with all null values"""
        stats = analyzer._analyze_numeric(sample_missing_values_df['col_all_nulls'])

        assert stats['min'] is None
        assert stats['max'] is None
        assert stats['mean'] is None
        assert stats['median'] is None
        assert stats['std'] is None

    def test_analyze_text_column(self, analyzer, sample_text_df):
        """Test analysis of text column"""
        stats = analyzer._analyze_text(sample_text_df['names'])

        assert stats['min_length'] >= 3  # 'Bob', 'Eve'
        assert stats['max_length'] >= 7  # 'Charlie'
        assert stats['avg_length'] > 0

    def test_analyze_text_column_with_nulls(self, analyzer):
        """Test analysis of text column with null values"""
        df = pd.DataFrame({'text_col': ['Alice', None, 'Bob', None, 'Charlie']})
        stats = analyzer._analyze_text(df['text_col'])

        assert stats['min_length'] == 3  # 'Bob'
        assert stats['max_length'] == 7  # 'Charlie'
        assert stats['avg_length'] > 0

    def test_analyze_datetime_column(self, analyzer, sample_datetime_df):
        """Test analysis of datetime column"""
        stats = analyzer._analyze_datetime(sample_datetime_df['dates'])

        assert stats['earliest'] is not None
        assert stats['latest'] is not None
        assert stats['range_days'] == 9  # 10 days, difference is 9

    def test_get_most_frequent_values(self, analyzer):
        """Test extraction of most frequent values"""
        series = pd.Series(['A', 'A', 'A', 'B', 'B', 'C', 'D', 'D', 'D', 'D'])
        freq = analyzer._get_most_frequent(series, n=3)

        assert len(freq) == 3
        assert freq[0]['value'] == 'D'
        assert freq[0]['count'] == 4
        assert freq[1]['value'] == 'A'
        assert freq[1]['count'] == 3

    def test_get_most_frequent_with_nulls(self, analyzer):
        """Test most frequent values with null values present"""
        series = pd.Series(['A', None, 'A', 'B', None, 'C'])
        freq = analyzer._get_most_frequent(series, n=5)

        assert len(freq) <= 3  # Should exclude nulls
        assert freq[0]['value'] == 'A'
        assert freq[0]['count'] == 2

    def test_analyze_column_complete(self, analyzer, sample_numeric_df):
        """Test complete column analysis"""
        stats = analyzer.analyze_column(sample_numeric_df, 'integers')

        assert stats['column_name'] == 'integers'
        assert stats['data_type'] == 'Integer'
        assert stats['total_count'] == 10
        assert stats['non_null_count'] == 10
        assert stats['null_count'] == 0
        assert stats['null_percentage'] == 0.0
        assert stats['unique_count'] == 10
        assert 'min' in stats
        assert 'max' in stats
        assert 'mean' in stats
        assert 'median' in stats
        assert 'std' in stats
        assert 'most_frequent' in stats

    def test_analyze_column_with_missing_values(self, analyzer, sample_missing_values_df):
        """Test column analysis with missing values"""
        stats = analyzer.analyze_column(sample_missing_values_df, 'col_with_nulls')

        assert stats['total_count'] == 10
        assert stats['non_null_count'] == 5
        assert stats['null_count'] == 5
        assert stats['null_percentage'] == 50.0

    def test_analyze_complete_dataframe(self, analyzer, sample_mixed_types_df):
        """Test analysis of complete DataFrame"""
        statistics = analyzer.analyze(sample_mixed_types_df)

        assert len(statistics) == 5
        assert 'integers' in statistics
        assert 'floats' in statistics
        assert 'strings' in statistics
        assert 'booleans' in statistics
        assert 'dates' in statistics

        # Verify each column has required fields
        for col_name, stats in statistics.items():
            assert 'column_name' in stats
            assert 'data_type' in stats
            assert 'total_count' in stats
            assert 'non_null_count' in stats
            assert 'null_count' in stats
            assert 'unique_count' in stats

    def test_analyze_empty_dataframe(self, analyzer):
        """Test analysis of empty DataFrame"""
        df = pd.DataFrame()
        statistics = analyzer.analyze(df)

        assert len(statistics) == 0

    def test_analyze_single_column_dataframe(self, analyzer):
        """Test analysis of DataFrame with single column"""
        df = pd.DataFrame({'single_col': [1, 2, 3, 4, 5]})
        statistics = analyzer.analyze(df)

        assert len(statistics) == 1
        assert 'single_col' in statistics

    def test_unique_count_all_unique(self, analyzer):
        """Test unique count when all values are unique"""
        df = pd.DataFrame({'unique_col': list(range(100))})
        stats = analyzer.analyze_column(df, 'unique_col')

        assert stats['unique_count'] == 100

    def test_unique_count_all_same(self, analyzer):
        """Test unique count when all values are the same"""
        df = pd.DataFrame({'same_col': ['A'] * 100})
        stats = analyzer.analyze_column(df, 'same_col')

        assert stats['unique_count'] == 1

    def test_numeric_statistics_precision(self, analyzer):
        """Test precision of numeric statistics"""
        df = pd.DataFrame({'precise_col': [1.123456789, 2.987654321, 3.456789012]})
        stats = analyzer.analyze_column(df, 'precise_col')

        assert isinstance(stats['mean'], float)
        assert isinstance(stats['std'], float)
        assert stats['mean'] > 0

    def test_large_dataset_performance(self, analyzer):
        """Test analysis performance with large dataset"""
        # Create large DataFrame (10000 rows, 10 columns)
        df = pd.DataFrame({
            f'col{i}': np.random.randint(0, 100, 10000)
            for i in range(10)
        })

        statistics = analyzer.analyze(df)

        assert len(statistics) == 10
        for stats in statistics.values():
            assert stats['total_count'] == 10000

    def test_special_values_handling(self, analyzer):
        """Test handling of special values (inf, -inf)"""
        df = pd.DataFrame({
            'special_col': [1.0, 2.0, float('inf'), 3.0, float('-inf')]
        })

        stats = analyzer.analyze_column(df, 'special_col')

        # Should handle inf values gracefully
        assert 'mean' in stats
        assert 'std' in stats


class TestStatisticsAnalyzerIntegration:
    """Integration tests for statistical analysis workflow"""

    def test_complete_analysis_workflow(self):
        """Test complete analysis workflow from DataFrame to statistics"""
        analyzer = StatisticsAnalyzer()

        # Create comprehensive test DataFrame
        df = pd.DataFrame({
            'employee_id': range(1, 11),
            'name': ['Alice', 'Bob', 'Charlie', 'David', 'Eve', 'Frank', 'Grace', 'Henry', 'Ivy', 'Jack'],
            'age': [25, 30, 35, None, 45, 50, 55, 60, 65, 70],
            'salary': [50000.0, 55000.0, 60000.0, 65000.0, 70000.0, 75000.0, 80000.0, 85000.0, 90000.0, 95000.0],
            'department': ['Eng', 'Sales', 'Eng', 'HR', 'Sales', 'Eng', 'HR', 'Sales', 'Eng', 'HR'],
            'hire_date': pd.date_range('2020-01-01', periods=10, freq='M')
        })

        # Analyze
        statistics = analyzer.analyze(df)

        # Verify all columns analyzed
        assert len(statistics) == 6

        # Verify employee_id (integer)
        assert statistics['employee_id']['data_type'] == 'Integer'
        assert statistics['employee_id']['min'] == 1.0
        assert statistics['employee_id']['max'] == 10.0

        # Verify name (text)
        assert statistics['name']['data_type'] == 'Text'
        assert statistics['name']['unique_count'] == 10

        # Verify age (with nulls)
        assert statistics['age']['null_count'] == 1
        assert statistics['age']['non_null_count'] == 9

        # Verify salary (float)
        assert statistics['salary']['data_type'] == 'Float'
        assert statistics['salary']['mean'] > 0

        # Verify department (text with duplicates)
        assert statistics['department']['unique_count'] < 10

        # Verify hire_date (datetime)
        assert statistics['hire_date']['data_type'] == 'DateTime'
        assert 'earliest' in statistics['hire_date']

    def test_accuracy_comparison_with_pandas(self):
        """Test that statistics match pandas built-in functions"""
        analyzer = StatisticsAnalyzer()

        df = pd.DataFrame({
            'values': [10, 20, 30, 40, 50]
        })

        stats = analyzer.analyze_column(df, 'values')

        # Compare with pandas
        assert stats['mean'] == df['values'].mean()
        assert stats['median'] == df['values'].median()
        assert stats['min'] == df['values'].min()
        assert stats['max'] == df['values'].max()
        assert abs(stats['std'] - df['values'].std()) < 0.0001  # Allow small floating point difference
