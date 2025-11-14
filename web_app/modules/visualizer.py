"""
Data Visualization Module
Creates interactive visualizations using Plotly and Streamlit.
"""

from typing import Dict, Any
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import streamlit as st


class DataVisualizer:
    """
    Creates interactive data visualizations for statistical analysis.
    """

    def render_visualizations(self, df: pd.DataFrame, statistics: Dict[str, Dict[str, Any]]):
        """
        Render all visualizations for the analyzed data.

        Args:
            df: The pandas DataFrame
            statistics: Dictionary of statistics for each column
        """
        st.header("📊 Data Visualizations")

        self._render_data_type_distribution(statistics)
        self._render_missing_values_chart(df)
        self._render_numeric_distributions(df, statistics)
        self._render_unique_values_chart(statistics)

    def _render_data_type_distribution(self, statistics: Dict[str, Dict[str, Any]]):
        """
        Render a pie chart showing data type distribution.

        Args:
            statistics: Dictionary of statistics for each column
        """
        st.subheader("Data Type Distribution")

        # Count data types
        data_types = {}
        for col_stats in statistics.values():
            dtype = col_stats.get('data_type', 'Unknown')
            data_types[dtype] = data_types.get(dtype, 0) + 1

        # Create pie chart
        fig = go.Figure(data=[go.Pie(
            labels=list(data_types.keys()),
            values=list(data_types.values()),
            hole=0.3
        )])

        fig.update_layout(title="Column Data Types")
        st.plotly_chart(fig, use_container_width=True)

    def _render_missing_values_chart(self, df: pd.DataFrame):
        """
        Render a bar chart showing missing values per column.

        Args:
            df: The pandas DataFrame
        """
        st.subheader("Missing Values Analysis")

        # Calculate missing values
        missing_data = df.isnull().sum()
        missing_pct = (missing_data / len(df) * 100).round(2)

        # Filter columns with missing values
        missing_cols = missing_data[missing_data > 0]

        if len(missing_cols) == 0:
            st.info("No missing values found in the dataset.")
            return

        # Create bar chart
        fig = go.Figure(data=[
            go.Bar(
                x=missing_cols.index,
                y=missing_cols.values,
                text=[f"{missing_pct[col]:.1f}%" for col in missing_cols.index],
                textposition='outside',
                marker_color='indianred'
            )
        ])

        fig.update_layout(
            title="Missing Values by Column",
            xaxis_title="Column Name",
            yaxis_title="Number of Missing Values",
            showlegend=False
        )

        st.plotly_chart(fig, use_container_width=True)

    def _render_numeric_distributions(self, df: pd.DataFrame, statistics: Dict[str, Dict[str, Any]]):
        """
        Render histograms for numeric columns.

        Args:
            df: The pandas DataFrame
            statistics: Dictionary of statistics for each column
        """
        st.subheader("Numeric Distributions")

        # Find numeric columns
        numeric_cols = [
            col for col, stats in statistics.items()
            if stats.get('data_type') in ['Integer', 'Float']
        ]

        if not numeric_cols:
            st.info("No numeric columns found in the dataset.")
            return

        # Create histograms
        num_cols = min(2, len(numeric_cols))
        cols = st.columns(num_cols)

        for idx, col in enumerate(numeric_cols[:6]):  # Limit to 6 charts
            with cols[idx % num_cols]:
                fig = px.histogram(
                    df,
                    x=col,
                    title=f"Distribution of {col}",
                    nbins=30
                )
                fig.update_layout(showlegend=False)
                st.plotly_chart(fig, use_container_width=True)

    def _render_unique_values_chart(self, statistics: Dict[str, Dict[str, Any]]):
        """
        Render a bar chart showing unique value counts.

        Args:
            statistics: Dictionary of statistics for each column
        """
        st.subheader("Unique Values Count")

        # Extract unique counts
        columns = list(statistics.keys())
        unique_counts = [stats.get('unique_count', 0) for stats in statistics.values()]

        # Create bar chart
        fig = go.Figure(data=[
            go.Bar(
                x=columns,
                y=unique_counts,
                marker_color='lightblue'
            )
        ])

        fig.update_layout(
            title="Unique Values per Column",
            xaxis_title="Column Name",
            yaxis_title="Number of Unique Values",
            showlegend=False
        )

        st.plotly_chart(fig, use_container_width=True)
