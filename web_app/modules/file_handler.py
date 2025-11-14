"""
File Upload and Validation Module
Handles CSV file uploads, validation, and data preview
"""

import streamlit as st
import pandas as pd
import io
from typing import Tuple, Optional


class FileUploadHandler:
    """Handles CSV file upload, validation, and preview"""

    MAX_FILE_SIZE_MB = 10
    SUPPORTED_ENCODINGS = ['utf-8', 'latin-1', 'cp1252', 'iso-8859-1']

    def render_upload_widget(self):
        """Render the file upload widget"""
        uploaded_file = st.file_uploader(
            "Choose a CSV file",
            type=['csv'],
            help=f"Maximum file size: {self.MAX_FILE_SIZE_MB}MB"
        )
        return uploaded_file

    def validate_file_size(self, file) -> Tuple[bool, str]:
        """Validate file size"""
        file_size_mb = len(file.getvalue()) / (1024 * 1024)
        if file_size_mb > self.MAX_FILE_SIZE_MB:
            return False, f"File size ({file_size_mb:.2f}MB) exceeds maximum allowed size ({self.MAX_FILE_SIZE_MB}MB)"
        return True, f"File size: {file_size_mb:.2f}MB"

    def detect_encoding(self, file) -> str:
        """Detect file encoding"""
        file_content = file.getvalue()

        for encoding in self.SUPPORTED_ENCODINGS:
            try:
                file_content.decode(encoding)
                return encoding
            except (UnicodeDecodeError, AttributeError):
                continue

        return 'utf-8'  # Default fallback

    def detect_delimiter(self, file, encoding: str) -> str:
        """Detect CSV delimiter"""
        file.seek(0)
        sample = file.read(1024).decode(encoding, errors='ignore')
        file.seek(0)

        delimiters = [',', ';', '\t', '|']
        delimiter_counts = {delim: sample.count(delim) for delim in delimiters}
        return max(delimiter_counts, key=delimiter_counts.get)

    def validate_and_load(self, file) -> Tuple[bool, str, Optional[pd.DataFrame]]:
        """
        Validate file and load into DataFrame

        Returns:
            Tuple of (is_valid, message, dataframe)
        """
        # Validate file size
        is_valid, size_msg = self.validate_file_size(file)
        if not is_valid:
            return False, size_msg, None

        # Detect encoding
        encoding = self.detect_encoding(file)

        # Detect delimiter
        delimiter = self.detect_delimiter(file, encoding)

        # Load CSV
        try:
            file.seek(0)
            df = pd.read_csv(
                file,
                encoding=encoding,
                delimiter=delimiter,
                low_memory=False
            )

            if df.empty:
                return False, "Error: CSV file is empty", None

            if len(df.columns) == 0:
                return False, "Error: No columns detected in CSV file", None

            success_msg = (
                f"✓ File loaded successfully | "
                f"Rows: {len(df):,} | "
                f"Columns: {len(df.columns)} | "
                f"Encoding: {encoding} | "
                f"Delimiter: '{delimiter}'"
            )

            return True, success_msg, df

        except pd.errors.EmptyDataError:
            return False, "Error: CSV file is empty or invalid", None
        except pd.errors.ParserError as e:
            return False, f"Error parsing CSV: {str(e)}", None
        except Exception as e:
            return False, f"Error loading file: {str(e)}", None

    def render_preview(self, df: pd.DataFrame, num_rows: int = 10):
        """Render data preview"""
        st.subheader("Data Preview")

        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("Total Rows", f"{len(df):,}")
        with col2:
            st.metric("Total Columns", len(df.columns))
        with col3:
            memory_mb = df.memory_usage(deep=True).sum() / (1024 * 1024)
            st.metric("Memory Usage", f"{memory_mb:.2f} MB")

        st.dataframe(df.head(num_rows), use_container_width=True)

        if len(df) > num_rows:
            st.caption(f"Showing first {num_rows} of {len(df):,} rows")
