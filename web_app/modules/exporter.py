"""
Data Export Module
Exports statistical results in multiple formats
"""

import streamlit as st
import pandas as pd
import json
import io
from typing import Dict, Any


class DataExporter:
    """Handles exporting statistics and visualizations"""

    def render_export_options(self, df: pd.DataFrame, statistics: Dict[str, Dict[str, Any]]):
        """Render export options"""

        st.subheader("Export Statistical Results")

        col1, col2, col3, col4 = st.columns(4)

        with col1:
            if st.button("📄 Export CSV", use_container_width=True):
                self._export_csv(statistics)

        with col2:
            if st.button("📊 Export Excel", use_container_width=True):
                self._export_excel(statistics, df)

        with col3:
            if st.button("📋 Export JSON", use_container_width=True):
                self._export_json(statistics)

        with col4:
            st.info("PDF export (planned)")

    def _export_csv(self, statistics: Dict[str, Dict[str, Any]]):
        """Export statistics as CSV"""
        rows = []

        for col_name, stats in statistics.items():
            row = {
                'column_name': col_name,
                'data_type': stats.get('data_type', ''),
                'non_null_count': stats.get('non_null_count', 0),
                'null_count': stats.get('null_count', 0),
                'null_percentage': stats.get('null_percentage', 0),
                'unique_count': stats.get('unique_count', 0),
            }

            # Add numeric stats
            for key in ['min', 'max', 'mean', 'median', 'std', 'sum']:
                if key in stats:
                    row[key] = stats[key]

            # Add text stats
            for key in ['min_length', 'max_length', 'avg_length']:
                if key in stats:
                    row[key] = stats[key]

            rows.append(row)

        stats_df = pd.DataFrame(rows)

        csv_buffer = io.StringIO()
        stats_df.to_csv(csv_buffer, index=False)
        csv_data = csv_buffer.getvalue()

        st.download_button(
            label="Download CSV",
            data=csv_data,
            file_name="csv_statistics.csv",
            mime="text/csv"
        )

    def _export_excel(self, statistics: Dict[str, Dict[str, Any]], df: pd.DataFrame):
        """Export statistics as Excel"""
        rows = []

        for col_name, stats in statistics.items():
            row = {
                'column_name': col_name,
                'data_type': stats.get('data_type', ''),
                'non_null_count': stats.get('non_null_count', 0),
                'null_count': stats.get('null_count', 0),
                'null_percentage': stats.get('null_percentage', 0),
                'unique_count': stats.get('unique_count', 0),
            }

            # Add numeric stats
            for key in ['min', 'max', 'mean', 'median', 'std', 'sum']:
                if key in stats:
                    row[key] = stats[key]

            # Add text stats
            for key in ['min_length', 'max_length', 'avg_length']:
                if key in stats:
                    row[key] = stats[key]

            rows.append(row)

        stats_df = pd.DataFrame(rows)

        excel_buffer = io.BytesIO()

        with pd.ExcelWriter(excel_buffer, engine='openpyxl') as writer:
            stats_df.to_excel(writer, sheet_name='Statistics', index=False)
            df.head(100).to_excel(writer, sheet_name='Data Preview', index=False)

        excel_data = excel_buffer.getvalue()

        st.download_button(
            label="Download Excel",
            data=excel_data,
            file_name="csv_statistics.xlsx",
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
        )

    def _export_json(self, statistics: Dict[str, Dict[str, Any]]):
        """Export statistics as JSON"""
        json_data = json.dumps(statistics, indent=2, default=str)

        st.download_button(
            label="Download JSON",
            data=json_data,
            file_name="csv_statistics.json",
            mime="application/json"
        )
