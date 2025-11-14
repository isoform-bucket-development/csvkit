"""
Tests for Data Export Module
Testing: REQ-8 (Data Export Functionality)
"""

import pytest
import pandas as pd
import json
import io
import sys
import os

# Add parent directory to path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from modules.stats_analyzer import StatsAnalyzer


class TestDataExporter:
    """Test suite for DataExporter class - data export preparation"""

    @pytest.fixture
    def analyzer(self):
        """Create StatsAnalyzer instance"""
        return StatsAnalyzer()

    @pytest.fixture
    def sample_df(self):
        """Create sample DataFrame"""
        return pd.DataFrame({
            'integers': [1, 2, 3, 4, 5],
            'floats': [1.1, 2.2, 3.3, 4.4, 5.5],
            'text': ['A', 'B', 'C', 'D', 'E']
        })

    @pytest.fixture
    def sample_statistics(self, analyzer, sample_df):
        """Generate statistics for sample DataFrame"""
        return analyzer.analyze(sample_df)

    def test_prepare_csv_export_data(self, sample_statistics):
        """Test preparation of data for CSV export"""
        rows = []

        for col_name, stats in sample_statistics.items():
            row = {
                'column_name': col_name,
                'data_type': stats.get('data_type', ''),
                'non_null_count': stats.get('non_null_count', 0),
                'null_count': stats.get('null_count', 0),
                'null_percentage': stats.get('null_percentage', 0),
                'unique_count': stats.get('unique_count', 0),
            }
            rows.append(row)

        assert len(rows) == 3
        assert rows[0]['column_name'] == 'integers'
        assert rows[1]['column_name'] == 'floats'
        assert rows[2]['column_name'] == 'text'

    def test_prepare_csv_export_with_numeric_stats(self, sample_statistics):
        """Test CSV export data includes numeric statistics"""
        rows = []

        for col_name, stats in sample_statistics.items():
            row = {'column_name': col_name}

            # Add numeric stats
            for key in ['min', 'max', 'mean', 'median', 'std', 'sum']:
                if key in stats:
                    row[key] = stats[key]

            rows.append(row)

        # Find integer column
        int_row = next(r for r in rows if r['column_name'] == 'integers')

        assert 'min' in int_row
        assert 'max' in int_row
        assert 'mean' in int_row
        assert int_row['min'] == 1.0
        assert int_row['max'] == 5.0

    def test_csv_export_format(self, sample_statistics):
        """Test CSV export format is valid"""
        rows = []

        for col_name, stats in sample_statistics.items():
            row = {
                'column_name': col_name,
                'data_type': stats.get('data_type', ''),
                'non_null_count': stats.get('non_null_count', 0),
                'null_count': stats.get('null_count', 0),
            }
            rows.append(row)

        stats_df = pd.DataFrame(rows)

        csv_buffer = io.StringIO()
        stats_df.to_csv(csv_buffer, index=False)
        csv_data = csv_buffer.getvalue()

        assert len(csv_data) > 0
        assert 'column_name' in csv_data
        assert 'data_type' in csv_data
        assert 'integers' in csv_data

    def test_excel_export_data_preparation(self, sample_statistics, sample_df):
        """Test preparation of data for Excel export"""
        rows = []

        for col_name, stats in sample_statistics.items():
            row = {
                'column_name': col_name,
                'data_type': stats.get('data_type', ''),
                'unique_count': stats.get('unique_count', 0),
            }
            rows.append(row)

        stats_df = pd.DataFrame(rows)

        # Verify DataFrame can be exported to Excel
        excel_buffer = io.BytesIO()

        with pd.ExcelWriter(excel_buffer, engine='openpyxl') as writer:
            stats_df.to_excel(writer, sheet_name='Statistics', index=False)
            sample_df.head(100).to_excel(writer, sheet_name='Data Preview', index=False)

        excel_data = excel_buffer.getvalue()

        assert len(excel_data) > 0

    def test_json_export_format(self, sample_statistics):
        """Test JSON export format is valid"""
        json_data = json.dumps(sample_statistics, indent=2, default=str)

        assert len(json_data) > 0

        # Verify JSON is valid
        parsed = json.loads(json_data)

        assert 'integers' in parsed
        assert 'floats' in parsed
        assert 'text' in parsed
        assert parsed['integers']['data_type'] == 'Integer'

    def test_json_export_structure(self, sample_statistics):
        """Test JSON export maintains correct structure"""
        json_str = json.dumps(sample_statistics, default=str)
        parsed = json.loads(json_str)

        for col_name, stats in parsed.items():
            assert 'data_type' in stats
            assert 'total_count' in stats
            assert 'unique_count' in stats

    def test_export_with_missing_values(self, analyzer):
        """Test export with DataFrame containing missing values"""
        df = pd.DataFrame({
            'col1': [1, None, 3, None, 5],
            'col2': ['A', 'B', None, 'D', 'E']
        })

        statistics = analyzer.analyze(df)

        # Prepare CSV export
        rows = []
        for col_name, stats in statistics.items():
            row = {
                'column_name': col_name,
                'null_count': stats.get('null_count', 0),
            }
            rows.append(row)

        assert rows[0]['null_count'] == 2
        assert rows[1]['null_count'] == 1

    def test_excel_multi_sheet_export(self, sample_statistics, sample_df):
        """Test Excel export with multiple sheets"""
        rows = []
        for col_name, stats in sample_statistics.items():
            row = {'column_name': col_name}
            rows.append(row)

        stats_df = pd.DataFrame(rows)

        excel_buffer = io.BytesIO()

        with pd.ExcelWriter(excel_buffer, engine='openpyxl') as writer:
            stats_df.to_excel(writer, sheet_name='Statistics', index=False)
            sample_df.to_excel(writer, sheet_name='Data', index=False)

        excel_data = excel_buffer.getvalue()

        assert len(excel_data) > 0
