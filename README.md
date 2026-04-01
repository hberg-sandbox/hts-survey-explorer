# Hopper Survey Explorer

An interactive Streamlit web app for exploring cross-tabulated survey data from the Hopper Travel Flexibility Survey.

## Features

- **Interactive Question Selection**: Browse through 36 survey questions
- **Demographic Filtering**: Filter results by various demographic segments (Age, Gender, Income, etc.)
- **Comparison Mode**: Compare two demographic segments side-by-side
- **Multiple View Modes**: Toggle between percentage and raw count displays
- **Chart Export**: Download charts as PNG images
- **Data Table View**: See detailed data in tabular format
- **Branded Design**: Consistent Hopper brand colors and typography

## Installation

1. Install required dependencies:
```bash
pip install -r requirements.txt
```

## Running the App

```bash
streamlit run app.py
```

The app will open in your default browser at `http://localhost:8501`

## Usage

1. **Select a Question**: Use the dropdown in the sidebar to choose a survey question
2. **Choose Demographics**: Select a demographic group and segment to filter results
3. **Compare Segments** (optional): Enable comparison mode to view two segments side-by-side
4. **Toggle Display Mode**: Switch between percentage and raw count views
5. **Export Charts**: Click the download button to save charts as PNG files
6. **View Data**: Expand the data table to see detailed response data

## Data

The app uses `survey_data.json` which contains:
- 36 survey questions
- Response data across multiple demographic segments
- Base sizes (n) for each segment
- Both percentage and raw count data

Survey sample: n=1,030 US Adults who flew in the past 12 months