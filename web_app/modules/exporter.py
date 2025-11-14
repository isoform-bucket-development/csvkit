"""
Data Export Module
Exports statistical results in multiple formats (CSV, Excel, JSON, PDF).
"""

from typing import Dict, Any
import pandas as pd
import json
import io
import streamlit as st


class DataExporter:
    """
    Exports statistical results in various formats.
    """

    def render_export_options(self, df: pd.DataFrame, statistics: Dict[str, Dict[str, Any]]):
        """
        Render export options and handle downloads.

        Args:
            df: The pandas DataFrame
            statistics: Dictionary of statistics for each column
        """
        st.header("💾 Export Results")

        col1, col2, col3, col4 = st.columns(4)

        with col1:
            self._export_csv(statistics)
        with col2:
            self._export_excel(statistics, df)
        with col3:
            self._export_json(statistics)
        with col4:
            st.info("PDF export (planned)")

    def _export_csv(self, statistics: Dict[str, Dict[str, Any]]):
        """
        Export statistics as CSV file.

        Args:
            statistics: Dictionary of statistics for each column
        """
        # Prepare data for CSV
        rows = []
        for col_name, stats in statistics.items():
            row = {
                'column_name': col_name,
                'data_type': stats.get('data_type', ''),
                'total_count': stats.get('total_count', 0),
                'non_null_count': stats.get('non_null_count', 0),
                'null_count': stats.get('null_count', 0),
                'null_percentage': stats.get('null_percentage', 0),
                'unique_count': stats.get('unique_count', 0),
            }

            # Add numeric stats
            for key in ['min', 'max', 'mean', 'median', 'std']:
                if key in stats:
                    row[key] = stats[key]

            # Add text stats
            for key in ['min_length', 'max_length', 'avg_length']:
                if key in stats:
                    row[key] = stats[key]

            # Add datetime stats
            for key in ['earliest', 'latest', 'range_days']:
                if key in stats:
                    row[key] = stats[key]

            rows.append(row)

        df_export = pd.DataFrame(rows)
        csv_data = df_export.to_csv(index=False)

        st.download_button(
            label="📥 Download CSV",
            data=csv_data,
            file_name="statistics.csv",
            mime="text/csv"
        )

    def _export_excel(self, statistics: Dict[str, Dict[str, Any]], df: pd.DataFrame):
        """
        Export statistics as Excel file with multiple sheets.

        Args:
            statistics: Dictionary of statistics for each column
            df: The original DataFrame
        """
        # Create Excel file in memory
        output = io.BytesIO()

        with pd.ExcelWriter(output, engine='openpyxl') as writer:
            # Statistics sheet
            rows = []
            for col_name, stats in statistics.items():
                row = {
                    'Column': col_name,
                    'Type': stats.get('data_type', ''),
                    'Total': stats.get('total_count', 0),
                    'Non-Null': stats.get('non_null_count', 0),
                    'Unique': stats.get('unique_count', 0),
                }
                rows.append(row)

            df_stats = pd.DataFrame(rows)
            df_stats.to_excel(writer, sheet_name='Statistics', index=False)

            # Data preview sheet (first 100 rows)
            df.head(100).to_excel(writer, sheet_name='Data Preview', index=False)

        excel_data = output.getvalue()

        st.download_button(
            label="📥 Download Excel",
            data=excel_data,
            file_name="statistics.xlsx",
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
        )

    def _export_json(self, statistics: Dict[str, Dict[str, Any]]):
        """
        Export statistics as JSON file.

        Args:
            statistics: Dictionary of statistics for each column
        """
        json_data = json.dumps(statistics, indent=2, default=str)

        st.download_button(
            label="📥 Download JSON",
            data=json_data,
            file_name="statistics.json",
            mime="application/json"
        )
