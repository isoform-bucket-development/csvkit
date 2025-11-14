"""
CSV Statistics Dashboard - Main Application
A Streamlit web application for analyzing CSV files and displaying statistics.
"""

import streamlit as st
import pandas as pd
from modules.file_handler import FileHandler
from modules.stats_analyzer import StatsAnalyzer
from modules.visualizer import DataVisualizer
from modules.exporter import DataExporter


def main():
    """Main application entry point."""

    # Page configuration
    st.set_page_config(
        page_title="CSV Statistics Dashboard",
        page_icon="📊",
        layout="wide",
        initial_sidebar_state="expanded"
    )

    # Title and description
    st.title("📊 CSV Statistics Dashboard")
    st.markdown("""
    Upload a CSV file to automatically analyze its structure, data types, and statistics.
    This tool provides comprehensive statistical analysis and interactive visualizations.
    """)

    # Initialize modules
    file_handler = FileHandler(max_file_size_mb=10.0)
    stats_analyzer = StatsAnalyzer()
    visualizer = DataVisualizer()
    exporter = DataExporter()

    # Sidebar
    with st.sidebar:
        st.header("📁 File Upload")
        uploaded_file = st.file_uploader(
            "Choose a CSV file",
            type=['csv'],
            help="Upload a CSV file (max 10MB)"
        )

        if uploaded_file is not None:
            st.success(f"File uploaded: {uploaded_file.name}")

        st.markdown("---")
        st.markdown("""
        ### About
        This dashboard converts csvkit's `csvstat` functionality into an interactive web application.

        **Features:**
        - Automatic data type detection
        - Comprehensive statistics
        - Interactive visualizations
        - Multiple export formats
        """)

    # Main content area
    if uploaded_file is not None:
        # Validate and load file
        with st.spinner("Loading and validating file..."):
            success, message, df = file_handler.validate_and_load(uploaded_file)

        if not success:
            st.error(f"❌ {message}")
            return

        st.success(f"✅ {message}")

        # Display data preview
        with st.expander("📋 Data Preview (First 20 rows)", expanded=True):
            st.dataframe(df.head(20), use_container_width=True)

        st.markdown("---")

        # Perform statistical analysis
        with st.spinner("Analyzing data..."):
            statistics = stats_analyzer.analyze(df)

        # Display statistics table
        st.header("📈 Statistical Analysis")

        # Prepare statistics for display
        stats_rows = []
        for col_name, stats in statistics.items():
            row = {
                'Column': col_name,
                'Type': stats.get('data_type', ''),
                'Total': stats.get('total_count', 0),
                'Non-Null': stats.get('non_null_count', 0),
                'Null': stats.get('null_count', 0),
                'Null %': f"{stats.get('null_percentage', 0):.1f}%",
                'Unique': stats.get('unique_count', 0),
            }

            # Add type-specific stats
            if stats.get('data_type') in ['Integer', 'Float']:
                row['Min'] = f"{stats.get('min', ''):.2f}" if 'min' in stats else ''
                row['Max'] = f"{stats.get('max', ''):.2f}" if 'max' in stats else ''
                row['Mean'] = f"{stats.get('mean', ''):.2f}" if 'mean' in stats else ''
                row['Median'] = f"{stats.get('median', ''):.2f}" if 'median' in stats else ''
                row['Std Dev'] = f"{stats.get('std', ''):.2f}" if 'std' in stats else ''
            elif stats.get('data_type') == 'Text':
                row['Min Length'] = stats.get('min_length', '')
                row['Max Length'] = stats.get('max_length', '')
                row['Avg Length'] = f"{stats.get('avg_length', ''):.1f}" if 'avg_length' in stats else ''
            elif stats.get('data_type') == 'DateTime':
                row['Earliest'] = stats.get('earliest', '')
                row['Latest'] = stats.get('latest', '')
                row['Range (days)'] = stats.get('range_days', '')

            stats_rows.append(row)

        stats_df = pd.DataFrame(stats_rows)
        st.dataframe(stats_df, use_container_width=True, hide_index=True)

        # Display most frequent values
        with st.expander("🔍 Most Frequent Values per Column"):
            cols = st.columns(min(3, len(statistics)))
            for idx, (col_name, stats) in enumerate(statistics.items()):
                with cols[idx % 3]:
                    st.subheader(col_name)
                    freq_values = stats.get('most_frequent', [])
                    if freq_values:
                        for item in freq_values[:5]:
                            st.write(f"• {item['value']}: {item['count']}")
                    else:
                        st.write("No data")

        st.markdown("---")

        # Display visualizations
        visualizer.render_visualizations(df, statistics)

        st.markdown("---")

        # Export options
        exporter.render_export_options(df, statistics)

    else:
        # Welcome screen
        st.info("👆 Please upload a CSV file using the sidebar to get started.")

        st.markdown("""
        ### How to use:
        1. Click on "Browse files" in the sidebar
        2. Select a CSV file from your computer (max 10MB)
        3. The dashboard will automatically:
           - Validate and load your file
           - Detect data types and encoding
           - Calculate comprehensive statistics
           - Generate interactive visualizations
           - Provide export options

        ### Supported Features:
        - ✅ Multiple CSV formats (comma, semicolon, tab-delimited)
        - ✅ Various encodings (UTF-8, Latin-1, etc.)
        - ✅ Automatic data type detection
        - ✅ Missing value analysis
        - ✅ Interactive charts and graphs
        - ✅ Export to CSV, Excel, and JSON
        """)


if __name__ == "__main__":
    main()
