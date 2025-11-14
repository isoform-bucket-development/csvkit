"""
Data Visualization Module
Creates interactive visualizations using Plotly
"""

import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from typing import Dict, Any


class DataVisualizer:
    """Creates interactive visualizations for statistical data"""

    def render_visualizations(self, df: pd.DataFrame, statistics: Dict[str, Dict[str, Any]]):
        """Render all visualizations"""

        # Data type distribution
        self._render_data_type_distribution(statistics)

        # Missing values heatmap
        self._render_missing_values_chart(df)

        # Numeric column distributions
        self._render_numeric_distributions(df, statistics)

        # Unique values chart
        self._render_unique_values_chart(statistics)

    def _render_data_type_distribution(self, statistics: Dict[str, Dict[str, Any]]):
        """Render pie chart of data type distribution"""
        st.subheader("Data Type Distribution")

        # Count data types
        data_types = {}
        for stats in statistics.values():
            dtype = stats.get('data_type', 'Unknown')
            data_types[dtype] = data_types.get(dtype, 0) + 1

        fig = px.pie(
            values=list(data_types.values()),
            names=list(data_types.keys()),
            title="Column Data Types"
        )

        st.plotly_chart(fig, use_container_width=True)

    def _render_missing_values_chart(self, df: pd.DataFrame):
        """Render bar chart of missing values per column"""
        st.subheader("Missing Values Analysis")

        null_counts = df.isnull().sum()
        null_percentages = (null_counts / len(df)) * 100

        # Filter columns with missing values
        has_nulls = null_counts[null_counts > 0]

        if len(has_nulls) == 0:
            st.success("✓ No missing values detected in any column")
            return

        fig = go.Figure()

        fig.add_trace(go.Bar(
            x=has_nulls.index,
            y=has_nulls.values,
            name='Missing Count',
            text=[f"{count} ({null_percentages[col]:.1f}%)"
                  for col, count in has_nulls.items()],
            textposition='auto'
        ))

        fig.update_layout(
            title="Missing Values by Column",
            xaxis_title="Column",
            yaxis_title="Missing Count",
            showlegend=False
        )

        st.plotly_chart(fig, use_container_width=True)

    def _render_numeric_distributions(self, df: pd.DataFrame, statistics: Dict[str, Dict[str, Any]]):
        """Render histograms for numeric columns"""
        st.subheader("Numeric Column Distributions")

        numeric_cols = [
            col for col, stats in statistics.items()
            if stats.get('data_type') in ['Integer', 'Float']
        ]

        if not numeric_cols:
            st.info("No numeric columns to visualize")
            return

        # Allow user to select columns
        selected_cols = st.multiselect(
            "Select columns to visualize",
            options=numeric_cols,
            default=numeric_cols[:min(3, len(numeric_cols))]
        )

        if not selected_cols:
            st.warning("Please select at least one column")
            return

        # Create histograms
        for col in selected_cols:
            fig = px.histogram(
                df,
                x=col,
                title=f"Distribution of {col}",
                nbins=30,
                marginal="box"
            )

            fig.update_layout(
                xaxis_title=col,
                yaxis_title="Frequency"
            )

            st.plotly_chart(fig, use_container_width=True)

    def _render_unique_values_chart(self, statistics: Dict[str, Dict[str, Any]]):
        """Render bar chart of unique value counts"""
        st.subheader("Unique Values per Column")

        columns = []
        unique_counts = []

        for col_name, stats in statistics.items():
            columns.append(col_name)
            unique_counts.append(stats.get('unique_count', 0))

        fig = go.Figure()

        fig.add_trace(go.Bar(
            x=columns,
            y=unique_counts,
            name='Unique Values',
            text=unique_counts,
            textposition='auto'
        ))

        fig.update_layout(
            title="Unique Value Counts by Column",
            xaxis_title="Column",
            yaxis_title="Unique Values",
            showlegend=False
        )

        st.plotly_chart(fig, use_container_width=True)
