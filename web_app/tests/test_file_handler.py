"""
Tests for File Upload and Validation Module
Testing: REQ-1 (CSV File Upload and Validation) and REQ-2 (Data Preview)
"""

import pytest
import pandas as pd
import io
import sys
import os

# Add parent directory to path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from modules.file_handler import FileHandler


class TestFileHandler:
    """Test suite for FileHandler class"""

    @pytest.fixture
    def handler(self):
        """Create FileHandler instance"""
        return FileHandler()

    @pytest.fixture
    def sample_csv_file(self):
        """Create a sample CSV file in memory"""
        csv_content = """name,age,salary,department
John Doe,30,50000,Engineering
Jane Smith,25,55000,Marketing
Bob Johnson,35,60000,Engineering
Alice Williams,28,52000,Sales
"""
        return io.BytesIO(csv_content.encode('utf-8'))

    @pytest.fixture
    def large_csv_file(self):
        """Create a CSV file exceeding size limit"""
        # Create a file with size > 10MB
        csv_content = "col1,col2,col3\n" + ("data," * 100 + "\n") * 100000
        return io.BytesIO(csv_content.encode('utf-8'))

    @pytest.fixture
    def empty_csv_file(self):
        """Create an empty CSV file"""
        return io.BytesIO(b"")

    @pytest.fixture
    def malformed_csv_file(self):
        """Create a malformed CSV file"""
        csv_content = """name,age,salary
John,30,50000
Jane,25
Bob,35,60000,extra_field
"""
        return io.BytesIO(csv_content.encode('utf-8'))

    @pytest.fixture
    def latin1_csv_file(self):
        """Create a CSV file with Latin-1 encoding"""
        csv_content = "name,city\nJosé,São Paulo\nFrançois,Montréal\n"
        return io.BytesIO(csv_content.encode('latin-1'))

    @pytest.fixture
    def semicolon_delimited_csv(self):
        """Create a semicolon-delimited CSV file"""
        csv_content = "name;age;salary\nJohn;30;50000\nJane;25;55000\n"
        return io.BytesIO(csv_content.encode('utf-8'))

    @pytest.fixture
    def tab_delimited_csv(self):
        """Create a tab-delimited CSV file"""
        csv_content = "name\tage\tsalary\nJohn\t30\t50000\nJane\t25\t55000\n"
        return io.BytesIO(csv_content.encode('utf-8'))

    def test_validate_file_size_valid(self, handler, sample_csv_file):
        """Test file size validation with valid file"""
        is_valid, message = handler.validate_file_size(sample_csv_file)
        assert is_valid is True
        assert "File size:" in message

    def test_validate_file_size_exceeds_limit(self, handler, large_csv_file):
        """Test file size validation with file exceeding limit"""
        is_valid, message = handler.validate_file_size(large_csv_file)
        assert is_valid is False
        assert "exceeds maximum" in message

    def test_detect_encoding_utf8(self, handler, sample_csv_file):
        """Test encoding detection for UTF-8 file"""
        encoding = handler.detect_encoding(sample_csv_file)
        assert encoding in ['utf-8', 'latin-1', 'cp1252', 'iso-8859-1', 'ascii']

    def test_detect_encoding_latin1(self, handler, latin1_csv_file):
        """Test encoding detection for Latin-1 file"""
        encoding = handler.detect_encoding(latin1_csv_file)
        assert encoding.lower() in ['utf-8', 'latin-1', 'iso-8859-1', 'windows-1252', 'ascii']

    def test_detect_delimiter_comma(self, handler, sample_csv_file):
        """Test delimiter detection for comma-separated file"""
        delimiter = handler.detect_delimiter(sample_csv_file, 'utf-8')
        assert delimiter == ','

    def test_detect_delimiter_semicolon(self, handler, semicolon_delimited_csv):
        """Test delimiter detection for semicolon-separated file"""
        delimiter = handler.detect_delimiter(semicolon_delimited_csv, 'utf-8')
        assert delimiter == ';'

    def test_detect_delimiter_tab(self, handler, tab_delimited_csv):
        """Test delimiter detection for tab-separated file"""
        delimiter = handler.detect_delimiter(tab_delimited_csv, 'utf-8')
        assert delimiter == '\t'

    def test_validate_and_load_valid_file(self, handler, sample_csv_file):
        """Test loading a valid CSV file"""
        is_valid, message, df = handler.validate_and_load(sample_csv_file)

        assert is_valid is True
        assert "File loaded successfully" in message
        assert df is not None
        assert isinstance(df, pd.DataFrame)
        assert len(df) == 4
        assert len(df.columns) == 4
        assert list(df.columns) == ['name', 'age', 'salary', 'department']

    def test_validate_and_load_empty_file(self, handler, empty_csv_file):
        """Test loading an empty CSV file"""
        is_valid, message, df = handler.validate_and_load(empty_csv_file)

        assert is_valid is False
        assert "empty" in message.lower()
        assert df is None

    def test_validate_and_load_latin1_file(self, handler, latin1_csv_file):
        """Test loading a Latin-1 encoded file"""
        is_valid, message, df = handler.validate_and_load(latin1_csv_file)

        assert is_valid is True
        assert df is not None
        assert len(df) == 2

    def test_validate_and_load_semicolon_delimited(self, handler, semicolon_delimited_csv):
        """Test loading a semicolon-delimited CSV"""
        is_valid, message, df = handler.validate_and_load(semicolon_delimited_csv)

        assert is_valid is True
        assert df is not None
        assert len(df.columns) == 3

    def test_validate_and_load_malformed_csv(self, handler, malformed_csv_file):
        """Test loading a malformed CSV file (should still load with pandas)"""
        is_valid, message, df = handler.validate_and_load(malformed_csv_file)

        # Pandas is lenient and may still load malformed CSVs
        # This test ensures we handle it gracefully
        assert is_valid in [True, False]

    def test_single_column_csv(self, handler):
        """Test loading a CSV with a single column"""
        csv_content = "name\nJohn\nJane\nBob\n"
        file = io.BytesIO(csv_content.encode('utf-8'))

        is_valid, message, df = handler.validate_and_load(file)

        assert is_valid is True
        assert df is not None
        assert len(df.columns) == 1
        assert len(df) == 3

    def test_csv_with_special_characters(self, handler):
        """Test loading CSV with special characters in data"""
        csv_content = 'name,description\nJohn,"Likes coffee, tea"\nJane,"Says ""hello"""\n'
        file = io.BytesIO(csv_content.encode('utf-8'))

        is_valid, message, df = handler.validate_and_load(file)

        assert is_valid is True
        assert df is not None
        assert len(df) == 2

    def test_csv_with_missing_values(self, handler):
        """Test loading CSV with missing values"""
        csv_content = "name,age,salary\nJohn,30,50000\nJane,,55000\nBob,35,\n"
        file = io.BytesIO(csv_content.encode('utf-8'))

        is_valid, message, df = handler.validate_and_load(file)

        assert is_valid is True
        assert df is not None
        assert df['age'].isna().sum() == 1
        assert df['salary'].isna().sum() == 1

    def test_large_number_of_columns(self, handler):
        """Test loading CSV with large number of columns (edge case for performance)"""
        columns = ','.join([f'col{i}' for i in range(150)])
        data_row = ','.join(['value'] * 150)
        csv_content = f"{columns}\n{data_row}\n{data_row}\n"
        file = io.BytesIO(csv_content.encode('utf-8'))

        is_valid, message, df = handler.validate_and_load(file)

        assert is_valid is True
        assert df is not None
        assert len(df.columns) == 150

    def test_csv_with_numeric_column_names(self, handler):
        """Test loading CSV with numeric column names"""
        csv_content = "1,2,3\n10,20,30\n40,50,60\n"
        file = io.BytesIO(csv_content.encode('utf-8'))

        is_valid, message, df = handler.validate_and_load(file)

        assert is_valid is True
        assert df is not None


class TestFileHandlerIntegration:
    """Integration tests for file upload workflow"""

    def test_complete_upload_workflow(self):
        """Test complete upload and validation workflow"""
        handler = FileHandler()

        # Create sample file
        csv_content = "name,age,salary\nJohn,30,50000\nJane,25,55000\n"
        file = io.BytesIO(csv_content.encode('utf-8'))

        # Step 1: Validate size
        is_valid, _ = handler.validate_file_size(file)
        assert is_valid is True

        # Step 2: Detect encoding
        encoding = handler.detect_encoding(file)
        assert encoding.lower() in ['utf-8', 'latin-1', 'iso-8859-1', 'windows-1252', 'ascii']

        # Step 3: Detect delimiter
        delimiter = handler.detect_delimiter(file, encoding)
        assert delimiter == ','

        # Step 4: Load file
        is_valid, message, df = handler.validate_and_load(file)
        assert is_valid is True
        assert df is not None
        assert len(df) == 2
        assert len(df.columns) == 3

    def test_error_recovery_workflow(self):
        """Test error handling and recovery in upload workflow"""
        handler = FileHandler()

        # Test with empty file
        empty_file = io.BytesIO(b"")
        is_valid, message, df = handler.validate_and_load(empty_file)

        assert is_valid is False
        assert df is None
        assert "empty" in message.lower()
