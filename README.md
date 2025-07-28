# UNICEF Health Services Coverage Analysis
**Learning and Skills Data Analyst Consultant - Req.#581598**

This repository contains a comprehensive analysis of health services coverage (ANC4 and SBA) for countries categorized by under-five mortality rate (U5MR) status, using births-weighted averages with projected births for 2022 as weights.

## Quick Start - Reproduce the Analysis

### 1. Clone the Repository
```bash
git clone <repository-url>
cd "UNICEF Test"
```

### 2. Set Up Environment
```bash
# Run the environment setup (installs dependencies and validates data)
python user_profile.py
```

### 3. Run the Analysis
```bash
# Execute the complete analysis workflow
python run_analysis.py
```

### 4. Launch Interactive Dashboard
```bash
# Launch the interactive Streamlit dashboard
streamlit run app.py
```

## Repository Structure

```
UNICEF Test/
├── README.md                           # This file - project documentation
├── requirements.txt                    # Python package dependencies
├── user_profile.py                    # Environment setup and configuration
├── run_analysis.py                    # Main analysis execution script
├── app.py                             # Interactive Streamlit dashboard
├── analysis_config.json               # Auto-generated configuration
├── data/
│   ├── raw/                          # Raw data files (included in repo)
│   │   ├── fusion_GLOBAL_DATAFLOW_UNICEF_1.0_.MNCH_ANC4+MNCH_SAB..csv
│   │   ├── WPP2022_GEN_F01_DEMOGRAPHIC_INDICATORS_COMPACT_REV1.xlsx
│   │   └── On-track and off-track countries.xlsx
│   ├── processed/                     # Intermediate cleaned data
│   └── output/                        # Final analysis outputs
│       ├── analysis_results.json      # Analysis results for dashboard
│       └── final_merged_dataset.csv   # Merged dataset for dashboard
├── src/
│   └── steps/                         # Analysis modules
│       ├── data_cleaner.py           # Data cleaning and merging
│       ├── coverage_calculator.py    # Births-weighted calculations
│       └── report_generator.py       # Static report generation
└── logs/                              # Analysis execution logs
    └── analysis.log                   # Detailed execution log
```

## Purpose of Each Folder and File

### Core Scripts
- **`user_profile.py`**: Environment setup script that ensures reproducible analysis across different machines. Checks Python version, installs dependencies, validates data files, and creates configuration.
- **`run_analysis.py`**: Main execution script that orchestrates the complete analysis workflow: data cleaning, births-weighted calculations, and data export for the interactive dashboard.
- **`app.py`**: Interactive Streamlit dashboard providing dynamic exploration of analysis results with filtering, visualization, and methodology explanation.

### Data Directory
- **`data/raw/`**: Contains manually downloaded raw data files from UNICEF Global Data Repository and UN World Population Prospects 2022.
- **`data/processed/`**: Stores intermediate cleaned datasets during the analysis pipeline.
- **`data/output/`**: Contains final analysis outputs used by the interactive dashboard.

### Source Code
- **`src/steps/`**: Modular analysis components following best practices for reproducible research.
  - `data_cleaner.py`: Handles complex Excel parsing, data standardization, and multi-dataset merging
  - `coverage_calculator.py`: Implements births-weighted statistical calculations
  - `report_generator.py`: Generates static HTML reports (optional)

### Configuration and Logs
- **`analysis_config.json`**: Auto-generated configuration containing project metadata, paths, and analysis settings.
- **`logs/analysis.log`**: Detailed execution log for debugging and reproducibility verification.

## How to Reproduce the Analysis

### Prerequisites
- Python 3.8 or higher
- Internet connection for package installation
- All raw data files are included in the repository

### Step 1: Environment Setup
```bash
# Run the environment setup
python user_profile.py
```

This will:
- Check Python version compatibility
- Install required packages (pandas, numpy, matplotlib, seaborn, openpyxl, xlrd, streamlit, plotly)
- Create necessary directories
- Validate data files
- Generate configuration file

### Step 2: Run Analysis
```bash
# Execute the complete analysis workflow
python run_analysis.py
```

This will:
1. **Data Cleaning**: Load and clean all datasets, handle complex Excel formatting, merge on consistent country identifiers
2. **Coverage Calculation**: Calculate births-weighted averages using projected births for 2022 as weights
3. **Data Export**: Save results for interactive dashboard
4. **Dashboard Launch**: Optionally launch the interactive Streamlit dashboard

### Step 3: Explore Results
```bash
# Launch the interactive dashboard (if not launched automatically)
streamlit run app.py
```

The dashboard provides:
- **Overview**: Key findings and metrics with coverage comparison
- **ANC4 & SBA Coverage**: Detailed analysis with expandable charts
- **Country Explorer**: Interactive filtering and visualization
- **Weighting Comparison**: Births-weighted vs simple averages
- **Methodology and Results**: Detailed explanation of analysis approach

## Data Sources

The analysis uses three key data sources, all included in the repository:

1. **UNICEF Global Data Repository**: ANC4 and SBA coverage indicators (2018-2022)
   - File: `data/raw/fusion_GLOBAL_DATAFLOW_UNICEF_1.0_.MNCH_ANC4+MNCH_SAB..csv`
   - Source: [UNICEF Data Explorer](https://data.unicef.org/resources/data_explorer/unicef_f/?ag=UNICEF&df=GLOBAL_DATAFLOW&ver=1.0&dq=.MNCH_ANC4+MNCH_SAB.&startPeriod=2018&endPeriod=2022)

2. **UN World Population Prospects 2022**: Projected births for 2022 (used as weights)
   - File: `data/raw/WPP2022_GEN_F01_DEMOGRAPHIC_INDICATORS_COMPACT_REV1.xlsx`
   - Source: [UN Population Division](https://population.un.org/wpp/Download/Standard/Excel/)

3. **U5MR Classification**: On-track vs off-track status for under-five mortality targets
   - File: `data/raw/On-track and off-track countries.xlsx`
   - Classification: On-track if Status.U5MR is "achieved" or "on-track", Off-track if "acceleration needed"


## Expected Outputs

### Analysis Results
- **Coverage by U5MR Status**: Births-weighted averages for on-track vs off-track countries
- **Indicator Comparison**: ANC4 vs SBA coverage patterns
- **Statistical Insights**: Weighted vs simple average comparisons

### Interactive Dashboard
- **Real-time Filtering**: By country, year, indicator, and U5MR status
- **Dynamic Visualizations**: Interactive charts and plots
- **Comprehensive Exploration**: Multiple analysis perspectives


---

*This analysis was completed as part of the UNICEF Data and Analytics technical evaluation for education. The code is designed to be reproducible, modular, and suitable for collaborative work environments.* 