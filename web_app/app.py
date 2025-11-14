#!/usr/bin/env python3
"""
CSV Statistics Dashboard - Main Streamlit Application
Converts csvstat CLI tool to an interactive web application
"""

import streamlit as st
import pandas as pd
from modules.file_handler import FileUploadHandler
from modules.stats_analyzer import StatisticsAnalyzer
from modules.visualizer import DataVisualizer
from modules.exporter import DataExporter


def main():
    """Main application entry point"""
    st.set_page_config(
        page_title="CSV Statistics Dashboard",
        page_icon="📊",
        layout="wide"
    )

    st.title("📊 CSV Statistics Dashboard")
    st.markdown("**Convert CSV files into interactive statistical insights**")

    # Initialize session state
    if 'uploaded_file' not in st.session_state:
        st.session_state.uploaded_file = None
    if 'dataframe' not in st.session_state:
        st.session_state.dataframe = None
    if 'statistics' not in st.session_state:
        st.session_state.statistics = None

    # File upload section
    st.header("1. Upload CSV File")
    file_handler = FileUploadHandler()
    uploaded_file = file_handler.render_upload_widget()

    if uploaded_file is not None:
        # Validate and process file
        is_valid, message, dataframe = file_handler.validate_and_load(uploaded_file)

        if is_valid:
            st.success(message)
            st.session_state.uploaded_file = uploaded_file
            st.session_state.dataframe = dataframe

            # Data preview section
            st.header("2. Data Preview")
            file_handler.render_preview(dataframe)

            # Statistical analysis section
            st.header("3. Statistical Analysis")
            analyzer = StatisticsAnalyzer()
            statistics = analyzer.analyze(dataframe)
            st.session_state.statistics = statistics

            # Display statistics table
            analyzer.render_statistics_table(statistics)

            # Visualization section
            st.header("4. Interactive Visualizations")
            visualizer = DataVisualizer()
            visualizer.render_visualizations(dataframe, statistics)

            # Export section
            st.header("5. Export Results")
            exporter = DataExporter()
            exporter.render_export_options(dataframe, statistics)

        else:
            st.error(message)
    else:
        st.info("👆 Please upload a CSV file to begin analysis")


if __name__ == "__main__":
    main()
