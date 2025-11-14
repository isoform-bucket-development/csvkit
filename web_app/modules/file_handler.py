"""
File Handler Module
Handles CSV file upload, validation, encoding detection, and loading.
"""

import io
from typing import Tuple, Optional
import pandas as pd
import chardet


class FileHandler:
    """
    Handles CSV file upload, validation, and loading with automatic
    encoding and delimiter detection.
    """

    def __init__(self, max_file_size_mb: float = 10.0):
        """
        Initialize the FileHandler.

        Args:
            max_file_size_mb: Maximum file size in megabytes (default: 10.0)
        """
        self.max_file_size_mb = max_file_size_mb
        self.max_file_size_bytes = max_file_size_mb * 1024 * 1024

    def validate_file_size(self, file) -> Tuple[bool, str]:
        """
        Validate that the file size does not exceed the maximum limit.

        Args:
            file: The uploaded file object

        Returns:
            Tuple of (is_valid, message)
        """
        file.seek(0, 2)  # Seek to end
        file_size = file.tell()
        file.seek(0)  # Reset to beginning

        file_size_mb = file_size / (1024 * 1024)

        if file_size > self.max_file_size_bytes:
            return False, f"File size ({file_size_mb:.2f}MB) exceeds maximum allowed size ({self.max_file_size_mb}MB)"

        return True, f"File size: {file_size_mb:.2f}MB"

    def detect_encoding(self, file) -> str:
        """
        Detect the encoding of the file.

        Args:
            file: The uploaded file object

        Returns:
            Detected encoding string
        """
        file.seek(0)
        raw_data = file.read(10000)  # Read first 10KB for detection
        file.seek(0)

        result = chardet.detect(raw_data)
        encoding = result['encoding']

        # Map common encodings
        if encoding and encoding.lower() in ['ascii', 'utf-8', 'utf-16', 'iso-8859-1', 'windows-1252']:
            return encoding

        return 'utf-8'  # Default fallback

    def detect_delimiter(self, file, encoding: str) -> str:
        """
        Detect the CSV delimiter (comma, semicolon, tab, pipe).

        Args:
            file: The uploaded file object
            encoding: The file encoding

        Returns:
            Detected delimiter character
        """
        file.seek(0)
        sample = file.read(10000).decode(encoding, errors='ignore')
        file.seek(0)

        # Count occurrences of common delimiters
        delimiters = [',', ';', '\t', '|']
        delimiter_counts = {d: sample.count(d) for d in delimiters}

        return max(delimiter_counts, key=delimiter_counts.get)

    def validate_and_load(self, file) -> Tuple[bool, str, Optional[pd.DataFrame]]:
        """
        Validate and load a CSV file into a pandas DataFrame.

        Args:
            file: The uploaded file object

        Returns:
            Tuple of (success, message, dataframe)
        """
        # Validate file size
        is_valid, message = self.validate_file_size(file)
        if not is_valid:
            return False, message, None

        try:
            # Detect encoding
            encoding = self.detect_encoding(file)

            # Detect delimiter
            delimiter = self.detect_delimiter(file, encoding)

            # Load CSV into DataFrame
            file.seek(0)
            df = pd.read_csv(file, encoding=encoding, delimiter=delimiter)

            # Validate the loaded data
            if df.empty:
                return False, "Error: CSV file is empty (no data rows)", None

            if len(df.columns) == 0:
                return False, "Error: No columns detected in CSV file", None

            return True, f"File loaded successfully: {len(df)} rows, {len(df.columns)} columns", df

        except pd.errors.EmptyDataError:
            return False, "Error: CSV file is empty", None
        except pd.errors.ParserError as e:
            return False, f"Error: Unable to parse CSV file - {str(e)}", None
        except UnicodeDecodeError as e:
            return False, f"Error: Unable to decode file with detected encoding - {str(e)}", None
        except Exception as e:
            return False, f"Error loading file: {str(e)}", None
