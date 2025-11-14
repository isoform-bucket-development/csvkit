# CSV Statistics Dashboard

A Streamlit web application that converts csvkit's `csvstat` command-line tool into an interactive web interface for analyzing CSV files.

## Features

- **File Upload & Validation**: Upload CSV files up to 10MB with automatic format detection
- **Automatic Analysis**: Detect data types, compute statistics, identify missing values
- **Interactive Visualizations**: Plotly charts for data type distribution, missing values, and more
- **Multiple Export Formats**: Export results as CSV, Excel, or JSON
- **Responsive Design**: Works on desktop, tablet, and mobile devices

## Installation

1. Install Python 3.8 or higher

2. Install dependencies:
```bash
pip install -r requirements.txt
```

## Usage

1. Start the application:
```bash
streamlit run app.py
```

2. Open your browser to `http://localhost:8501`

3. Upload a CSV file and explore the statistics!

## Project Structure

```
web_app/
├── app.py                  # Main Streamlit application
├── modules/
│   ├── __init__.py
│   ├── file_handler.py     # CSV file upload and validation
│   ├── stats_analyzer.py   # Statistical analysis
│   ├── visualizer.py       # Data visualizations
│   └── exporter.py         # Export functionality
├── tests/
│   ├── __init__.py
│   ├── test_file_handler.py
│   ├── test_stats_analyzer.py
│   ├── test_visualizer.py
│   └── test_exporter.py
├── requirements.txt
└── README.md
```

## Features Implemented

### File Upload and Validation
- File size validation (max 10MB)
- Automatic encoding detection (UTF-8, Latin-1, etc.)
- Automatic delimiter detection (comma, semicolon, tab, pipe)
- Error handling for malformed files

### Statistical Analysis
- Data type detection (Integer, Float, Text, DateTime, Boolean)
- Basic statistics (count, null count, unique count)
- Numeric statistics (min, max, mean, median, std deviation)
- Text statistics (min/max/average length)
- DateTime statistics (earliest, latest, range)
- Most frequent values (top 5)

### Visualizations
- Data type distribution pie chart
- Missing values bar chart
- Numeric distributions histograms
- Unique values count bar chart

### Export Options
- CSV export of statistics table
- Excel export with multiple sheets (statistics + data preview)
- JSON export of all statistical data
- PDF export (planned for future release)

## Development

### Running Tests

```bash
# Run all tests
pytest web_app/tests/

# Run with coverage
pytest web_app/tests/ --cov=web_app/modules --cov-report=html

# Run specific test file
pytest web_app/tests/test_file_handler.py -v
```

### Code Quality

The code follows:
- Python PEP 8 standards
- Comprehensive docstrings
- Type hints for better code clarity
- Modular architecture for maintainability

## Requirements

- Python 3.8+
- streamlit >= 1.28.0
- pandas >= 2.0.0
- numpy >= 1.24.0
- plotly >= 5.17.0
- chardet >= 5.2.0
- openpyxl >= 3.1.0

## License

This project is part of the csvkit ecosystem and follows the same license.

## Acknowledgments

- Based on csvkit's `csvstat` utility
- Built with Streamlit for rapid development
- Uses Plotly for interactive visualizations
