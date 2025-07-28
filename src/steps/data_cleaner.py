#!/usr/bin/env python3
"""
Data Cleaner for LOAD Phase
============================

This module handles the LOAD phase of the ELT process:
- Show data structure and column names
- Identify needed cleaning steps
- Create clean data tables with unified column names
- Prepare data for merging

Key Functions:
- analyze_data_structure(): Show structure and identify cleaning needs
- clean_unicef_data(): Clean UNICEF indicators data
- clean_population_data(): Clean population data
- clean_u5mr_data(): Clean U5MR classification data
- merge_datasets(): Merge all cleaned datasets
"""

import pandas as pd
import logging
from pathlib import Path
from typing import Dict, Any, Optional, List
import numpy as np


class DataCleaner:
    """Handles data cleaning and structuring """
    
    def __init__(self, config: Dict[str, Any], data_paths: Dict[str, Path]):
        """Initialize the data cleaner with configuration and paths."""
        self.config = config
        self.data_paths = data_paths
        self.logger = logging.getLogger(__name__)
        
        # Get processing parameters from config
        self.min_year = config.get('processing', {}).get('min_year', 2018)
        self.max_year = config.get('processing', {}).get('max_year', 2022)
    
    def analyze_data_structure(self) -> Dict[str, Any]:
        """Step 1: Analyze data structure and identify cleaning needs."""
        print("="*80)
        print("STEP 1: DATA STRUCTURE ANALYSIS")
        print("="*80)
        
        analysis = {}
        
        try:
            # Load raw data
            unicef_raw = self._load_unicef_data()
            population_raw = self._load_population_data()
            u5mr_raw = self._load_u5mr_data()
            
            # Analyze each dataset
            analysis['unicef'] = self._analyze_unicef_structure(unicef_raw)
            analysis['population'] = self._analyze_population_structure(population_raw)
            analysis['u5mr'] = self._analyze_u5mr_structure(u5mr_raw)
            
            # Print summary
            self._print_analysis_summary(analysis)
            
            return analysis
            
        except Exception as e:
            self.logger.error(f"Error in data structure analysis: {e}")
            raise
    
    def _analyze_unicef_structure(self, df: pd.DataFrame) -> Dict[str, Any]:
        """Analyze UNICEF data structure."""
        print("\n📊 UNICEF DATA STRUCTURE:")
        print("-" * 50)
        print(f"Shape: {df.shape}")
        print(f"Columns: {list(df.columns)}")
        print(f"Data types: {df.dtypes.to_dict()}")
        print(f"Missing values: {df.isnull().sum().to_dict()}")
        
        # Sample data
        print("\nSample data (first 2 rows):")
        print(df.head(2).to_string())
        
        # Identify key columns
        key_columns = {
            'country': 'REF_AREA:Geographic area',
            'indicator': 'INDICATOR:Indicator',
            'year': 'TIME_PERIOD:Time period',
            'value': 'OBS_VALUE:Observation Value'
        }
        
        # Identify cleaning needs
        cleaning_needs = [
            "Extract country names from 'CODE: Country Name' format",
            "Extract indicator names from 'INDICATOR: Indicator Name' format",
            "Filter for years 2018-2022",
            "Convert values to numeric",
            "Filter valid percentage values (0-100)",
            "Handle missing values"
        ]
        
        return {
            'shape': df.shape,
            'columns': list(df.columns),
            'dtypes': df.dtypes.to_dict(),
            'missing_values': df.isnull().sum().to_dict(),
            'key_columns': key_columns,
            'cleaning_needs': cleaning_needs,
            'sample_data': df.head(2).to_dict('records')
        }
    
    def _analyze_population_structure(self, df: pd.DataFrame) -> Dict[str, Any]:
        """Analyze population data structure."""
        print("\n📊 POPULATION DATA STRUCTURE:")
        print("-" * 50)
        print(f"Shape: {df.shape}")
        print(f"Columns: {list(df.columns)}")
        print(f"Data types: {df.dtypes.to_dict()}")
        print(f"Missing values: {df.isnull().sum().to_dict()}")
        
        # Sample data
        print("\nSample data (first 2 rows):")
        print(df.head(2).to_string())
        
        # Get key columns from attributes
        key_columns = df.attrs.get('key_columns', {})
        print(f"\nIdentified key columns: {key_columns}")
        
        # Identify cleaning needs
        cleaning_needs = [
            "Filter for years 2018-2022",
            "Extract country names and ISO codes",
            "Convert population to numeric",
            "Handle missing values",
            "Standardize country identifiers"
        ]
        
        return {
            'shape': df.shape,
            'columns': list(df.columns),
            'dtypes': df.dtypes.to_dict(),
            'missing_values': df.isnull().sum().to_dict(),
            'key_columns': key_columns,
            'cleaning_needs': cleaning_needs,
            'sample_data': df.head(2).to_dict('records')
        }
    
    def _analyze_u5mr_structure(self, df: pd.DataFrame) -> Dict[str, Any]:
        """Analyze U5MR data structure."""
        print("\n📊 U5MR DATA STRUCTURE:")
        print("-" * 50)
        print(f"Shape: {df.shape}")
        print(f"Columns: {list(df.columns)}")
        print(f"Data types: {df.dtypes.to_dict()}")
        print(f"Missing values: {df.isnull().sum().to_dict()}")
        
        # Sample data
        print("\nSample data (first 5 rows):")
        print(df.head(5).to_string())
        
        # Identify key columns
        key_columns = {
            'iso3': 'ISO3Code',
            'country': 'OfficialName',
            'status': 'Status.U5MR'
        }
        
        # Show unique status values
        print(f"\nUnique U5MR status values: {df['Status.U5MR'].unique().tolist()}")
        
        # Identify cleaning needs
        cleaning_needs = [
            "Standardize country names",
            "Create binary on-track/off-track classification",
            "Handle missing values",
            "Ensure consistent ISO3 codes"
        ]
        
        return {
            'shape': df.shape,
            'columns': list(df.columns),
            'dtypes': df.dtypes.to_dict(),
            'missing_values': df.isnull().sum().to_dict(),
            'key_columns': key_columns,
            'cleaning_needs': cleaning_needs,
            'unique_status': df['Status.U5MR'].unique().tolist(),
            'sample_data': df.head(5).to_dict('records')
        }
    
    def _print_analysis_summary(self, analysis: Dict[str, Any]):
        """Print summary of data structure analysis."""
        print("\n" + "="*80)
        print("CLEANING NEEDS SUMMARY:")
        print("="*80)
        
        for dataset_name, dataset_analysis in analysis.items():
            print(f"\n📋 {dataset_name.upper()} CLEANING NEEDS:")
            for need in dataset_analysis['cleaning_needs']:
                print(f"  • {need}")
    
    def clean_all_datasets(self) -> Dict[str, pd.DataFrame]:
        """Step 2-4: Clean all datasets and prepare for merging."""
        print("\n" + "="*80)
        print("STEP 2-4: DATA CLEANING AND MERGING PREPARATION")
        print("="*80)
        
        try:
            # Load raw data
            unicef_raw = self._load_unicef_data()
            population_raw = self._load_population_data()
            u5mr_raw = self._load_u5mr_data()
            
            # Clean each dataset
            print("\n🧹 CLEANING UNICEF DATA...")
            unicef_clean = self.clean_unicef_data(unicef_raw)
            
            print("\n🧹 CLEANING POPULATION DATA...")
            population_clean = self.clean_population_data(population_raw)
            
            print("\n🧹 CLEANING U5MR DATA...")
            u5mr_clean = self.clean_u5mr_data(u5mr_raw)
            
            # Show cleaned data structure
            print("\n" + "="*80)
            print("CLEANED DATA STRUCTURE:")
            print("="*80)
            
            self._show_cleaned_structure('UNICEF', unicef_clean)
            self._show_cleaned_structure('Population', population_clean)
            self._show_cleaned_structure('U5MR', u5mr_clean)
            
            # Save cleaned datasets
            self._save_cleaned_datasets({
                'unicef': unicef_clean,
                'population': population_clean,
                'u5mr': u5mr_clean
            })
            
            # Test merging
            print("\n🔗 TESTING DATA MERGING...")
            merged_data = self.merge_datasets({
                'unicef': unicef_clean,
                'population': population_clean,
                'u5mr': u5mr_clean
            })
            
            print(f"✓ Merged dataset shape: {merged_data.shape}")
            print(f"✓ Merged dataset columns: {list(merged_data.columns)}")
            
            self.logger.info("✓ All datasets cleaned and merged successfully")
            
            return {
                'unicef': unicef_clean,
                'population': population_clean,
                'u5mr': u5mr_clean,
                'merged': merged_data
            }
            
        except Exception as e:
            self.logger.error(f"Error in data cleaning: {e}")
            raise
    
    def _show_cleaned_structure(self, dataset_name: str, df: pd.DataFrame):
        """Show structure of cleaned dataset."""
        print(f"\n📊 {dataset_name} CLEANED DATA:")
        print(f"  Shape: {df.shape}")
        print(f"  Columns: {list(df.columns)}")
        print(f"  Sample data:")
        print(df.head(3).to_string())
    
    def _load_unicef_data(self) -> pd.DataFrame:
        """Load UNICEF data from CSV file."""
        file_path = self.data_paths['raw'] / "fusion_GLOBAL_DATAFLOW_UNICEF_1.0_.MNCH_ANC4+MNCH_SAB..csv"
        if not file_path.exists():
            raise FileNotFoundError(f"UNICEF data file not found: {file_path}")
        
        df = pd.read_csv(file_path)
        self.logger.info(f"✓ UNICEF data loaded: {len(df)} records")
        return df
    
    def _load_population_data(self) -> pd.DataFrame:
        """Load population data from highly formatted Excel file."""
        file_path = self.data_paths['raw'] / "WPP2022_GEN_F01_DEMOGRAPHIC_INDICATORS_COMPACT_REV1.xlsx"
        if not file_path.exists():
            raise FileNotFoundError(f"Population data file not found: {file_path}")
        
        # Handle highly formatted Excel file structure:
        # - Rows 1-15: Metadata and title information
        # - Row 16: Category headers (merged cells like "Population")
        # - Row 17: Actual column headers (this is where data starts)
        # - Row 18+: Actual data rows
        
        # Read the Excel file without headers first to understand the structure
        df_raw = pd.read_excel(file_path, header=None)
        
        # Find the row with actual column headers (around row 17)
        # Look for the row that contains "Region, subregion, country or area"
        header_row = None
        for i in range(15, 20):  # Check rows 15-19
            if i < len(df_raw):
                row_values = df_raw.iloc[i].astype(str)
                if any('region, subregion, country or area' in str(val).lower() for val in row_values):
                    header_row = i
                    break
        
        if header_row is None:
            # Fallback: use row 16 as header
            header_row = 16
        
        # Read the Excel file with the correct header row
        df = pd.read_excel(file_path, header=header_row)
        

        
        # Store key column mapping for later use
        key_columns = {}
        for col in df.columns:
            col_str = str(col).lower().strip()
            if 'region, subregion, country or area' in col_str:
                key_columns['country'] = col
            elif 'iso3 alpha-code' in col_str:
                key_columns['iso3'] = col
            elif col_str == 'year':  # Exact match for 'Year'
                key_columns['year'] = col
            elif 'births' in col_str and 'thousands' in col_str:
                key_columns['births_2022'] = col  # Use births as weights for 2022
            elif 'total population, as of 1 july (thousands)' in col_str:
                key_columns['population'] = col  # Keep for reference
        
        # Handle the specific case where 'Year ' (with trailing space) exists
        if 'Year ' in df.columns:
            key_columns['year'] = 'Year '
        
        # If we couldn't identify columns automatically, use fallback positions
        if not key_columns:
            print("    Warning: Could not identify columns automatically, using fallback positions")
            if len(df.columns) >= 12:
                key_columns = {
                    'country': df.columns[2],  # Usually country name
                    'year': df.columns[10],    # Usually year
                    'births_2022': df.columns[11]  # Use births as weights
                }
        
        print(f"    Identified key columns: {key_columns}")
        
        df.attrs['key_columns'] = key_columns
        self.logger.info(f"✓ Population data loaded: {len(df)} records")
        return df
    
    def _load_u5mr_data(self) -> pd.DataFrame:
        """Load U5MR classification data from Excel file."""
        file_path = self.data_paths['raw'] / "On-track and off-track countries.xlsx"
        if not file_path.exists():
            raise FileNotFoundError(f"U5MR data file not found: {file_path}")
        
        df = pd.read_excel(file_path)
        self.logger.info(f"✓ U5MR data loaded: {len(df)} records")
        return df
    
    def clean_unicef_data(self, df: pd.DataFrame) -> pd.DataFrame:
        """Clean UNICEF indicators data with unified column names for merging."""
        print("  Processing UNICEF data...")
        
        # Create a copy to avoid modifying original
        clean_df = df.copy()
        
        # Filter for relevant years (2018-2022)
        clean_df = clean_df[
            (clean_df['TIME_PERIOD:Time period'] >= self.min_year) &
            (clean_df['TIME_PERIOD:Time period'] <= self.max_year)
        ]
        print(f"    Filtered to {len(clean_df)} records for years {self.min_year}-{self.max_year}")
        
        # Clean country names - extract actual country names from the format "CODE: Country Name"
        clean_df['country_name'] = clean_df['REF_AREA:Geographic area'].str.extract(r':\s*(.+)')
        clean_df['country_code'] = clean_df['REF_AREA:Geographic area'].str.extract(r'^([^:]+):')
        
        # Handle cases where extraction didn't work
        clean_df['country_name'] = clean_df['country_name'].fillna(clean_df['REF_AREA:Geographic area'])
        clean_df['country_code'] = clean_df['country_code'].fillna('UNKNOWN')
        
        # Clean indicator names - extract the actual indicator name
        clean_df['indicator_clean'] = clean_df['INDICATOR:Indicator'].str.extract(r'^([^:]+):')
        clean_df['indicator_clean'] = clean_df['indicator_clean'].fillna(clean_df['INDICATOR:Indicator'])
        
        # Convert value to numeric and handle missing values
        clean_df['value_clean'] = pd.to_numeric(clean_df['OBS_VALUE:Observation Value'], errors='coerce')
        
        # Filter out invalid values (negative or > 100 for percentages)
        clean_df = clean_df[
            (clean_df['value_clean'] >= 0) & 
            (clean_df['value_clean'] <= 100) &
            (clean_df['value_clean'].notna())
        ]
        print(f"    Filtered to {len(clean_df)} valid percentage records")
        
        # Create unified column names for merging
        result_df = clean_df[[
            'country_name', 'country_code', 'indicator_clean', 
            'TIME_PERIOD:Time period', 'value_clean'
        ]].rename(columns={
            'country_name': 'country_name',
            'country_code': 'iso3_code',
            'indicator_clean': 'indicator',
            'TIME_PERIOD:Time period': 'year',
            'value_clean': 'coverage_value'
        })
        
        # Remove duplicates
        result_df = result_df.drop_duplicates()
        
        # Standardize country names for merging
        result_df['country_name'] = result_df['country_name'].str.strip()
        result_df['iso3_code'] = result_df['iso3_code'].str.strip()
        
        # Filter for most recent estimate per country-indicator combination within 2018-2022
        print(f"    Before filtering for most recent estimates: {len(result_df)} records")
        
        # Group by country and indicator, then get the most recent year for each
        result_df = result_df.sort_values(['country_name', 'indicator', 'year'], ascending=[True, True, False])
        result_df = result_df.groupby(['country_name', 'indicator']).first().reset_index()
        
        print(f"    After filtering for most recent estimates: {len(result_df)} records")
        print(f"    Unique countries: {result_df['country_name'].nunique()}")
        print(f"    Unique indicators: {result_df['indicator'].unique()}")
        
        # Show year distribution for verification
        year_counts = result_df['year'].value_counts().sort_index()
        print(f"    Year distribution of most recent estimates:")
        for year, count in year_counts.items():
            print(f"      {year}: {count} estimates")
        
        return result_df
    
    def clean_population_data(self, df: pd.DataFrame) -> pd.DataFrame:
        """Clean population data with unified column names for merging."""
        print("  Processing population data...")
        
        clean_df = df.copy()
        
        key_columns = clean_df.attrs.get('key_columns', {})
        
        if not key_columns:
            print("    Warning: No key column mapping found, attempting to identify columns...")
            for col in clean_df.columns:
                col_str = str(col).lower().strip()
                if 'country' in col_str or 'area' in col_str:
                    key_columns['country'] = col
                elif 'iso3 alpha-code' in col_str:
                    key_columns['iso3'] = col
                elif 'year' in col_str:
                    key_columns['year'] = col
                elif 'births' in col_str and 'thousands' in col_str:
                    key_columns['births_2022'] = col  # Use births as weights
                elif 'population' in col_str and 'july' in col_str and 'thousands' in col_str:
                    key_columns['population'] = col  # Keep for reference
            # Handle the specific case where 'Year ' (with trailing space) exists
            if 'Year ' in clean_df.columns:
                key_columns['year'] = 'Year '
            
            # If still no key columns, use fallback positions
            if not key_columns and len(clean_df.columns) >= 12:
                print("    Using fallback column positions")
                key_columns = {
                    'country': clean_df.columns[2],  # Usually country name
                    'year': clean_df.columns[10],    # Usually year
                    'population': clean_df.columns[11]  # Usually population
                }
        
        print(f"    Using key columns: {key_columns}")
        
        # Validate that we have the required columns
        required_cols = ['country', 'year', 'births_2022']
        missing_cols = [col for col in required_cols if col not in key_columns]
        if missing_cols:
            print(f"    Error: Missing required columns: {missing_cols}")
            print(f"    Available columns: {list(clean_df.columns)}")
            raise ValueError(f"Cannot proceed without required columns: {missing_cols}")
        
        year_col = key_columns['year']
        country_col = key_columns['country']
        births_col = key_columns['births_2022']
        
        # Filter for relevant years
        clean_df = clean_df[
            (clean_df[year_col] >= self.min_year) &
            (clean_df[year_col] <= self.max_year)
        ]
        print(f"    Filtered to {len(clean_df)} records for years {self.min_year}-{self.max_year}")
        
        # Extract country names and ISO codes
        clean_df['country_name'] = clean_df[country_col].str.strip()
        
        # Handle ISO3 codes if available
        if 'iso3' in key_columns:
            iso3_col = key_columns['iso3']
            clean_df['iso3_code'] = clean_df[iso3_col].str.strip()
        else:
            clean_df['iso3_code'] = 'UNKNOWN'
        
        # Convert births to numeric and filter for 2022 only
        clean_df['births_2022'] = pd.to_numeric(clean_df[births_col], errors='coerce')
        
        # Filter for 2022 births only (as specified in test requirements)
        births_2022_data = clean_df[clean_df[year_col] == 2022].copy()
        
        if len(births_2022_data) == 0:
            print(f"    Warning: No 2022 births data found. Using all years for births data.")
            births_2022_data = clean_df.copy()
        
        # Create unified column names for merging
        result_df = births_2022_data[[
            'country_name', 'iso3_code', 'births_2022'
        ]].copy()
        
        # Remove duplicates and invalid data
        result_df = result_df.drop_duplicates()
        result_df = result_df[result_df['births_2022'].notna()]
        result_df = result_df[result_df['births_2022'] > 0]
        
        # Standardize country names for merging
        result_df['country_name'] = result_df['country_name'].str.strip()
        result_df['iso3_code'] = result_df['iso3_code'].str.strip()
        
        print(f"    Final cleaned data: {len(result_df)} records")
        print(f"    Unique countries: {result_df['country_name'].nunique()}")
        print(f"    Using 2022 projected births as weights")
        
        return result_df
    
    def clean_u5mr_data(self, df: pd.DataFrame) -> pd.DataFrame:
        """Clean U5MR classification data with unified column names for merging."""
        print("  Processing U5MR data...")
        
        clean_df = df.copy()
        
        # Standardize country names
        clean_df['country_name'] = clean_df['OfficialName'].str.strip()
        clean_df['iso3_code'] = clean_df['ISO3Code'].str.strip()
        
        # Create binary classification for on-track vs off-track
        def classify_status(status):
            if pd.isna(status):
                return 'unknown'
            status_lower = str(status).lower()
            if 'achieved' in status_lower or 'on-track' in status_lower:
                return 'on_track'
            elif 'acceleration' in status_lower or 'off-track' in status_lower:
                return 'off_track'
            else:
                return 'unknown'
        
        clean_df['u5mr_status'] = clean_df['Status.U5MR'].apply(classify_status)
        
        # Create unified column names for merging
        result_df = clean_df[[
            'country_name', 'iso3_code', 'u5mr_status'
        ]].copy()
        
        # Remove duplicates
        result_df = result_df.drop_duplicates()
        
        # Show status distribution
        status_counts = result_df['u5mr_status'].value_counts()
        print(f"    Status distribution: {status_counts.to_dict()}")
        
        print(f"    Final cleaned data: {len(result_df)} records")
        print(f"    Unique countries: {result_df['country_name'].nunique()}")
        
        return result_df
    
    def merge_datasets(self, cleaned_data: Dict[str, pd.DataFrame]) -> pd.DataFrame:
        """Merge all cleaned datasets using unified column names."""
        print("  Merging datasets...")
        
        unicef_df = cleaned_data['unicef']
        population_df = cleaned_data['population']
        u5mr_df = cleaned_data['u5mr']
        
        print(f"    UNICEF data: {len(unicef_df)} records")
        print(f"    Population data: {len(population_df)} records")
        print(f"    U5MR data: {len(u5mr_df)} records")
        
        # Step 1: Merge UNICEF and Population data on country only (births data is for 2022)
        print("    Step 1: Merging UNICEF and Population data...")
        merged_df = pd.merge(
            unicef_df, 
            population_df, 
            on=['country_name'], 
            how='inner'
        )
        print(f"    UNICEF + Population merge: {len(merged_df)} records")
        
        # Step 2: Merge with U5MR data on country
        print("    Step 2: Merging with U5MR classification...")
        final_df = pd.merge(
            merged_df,
            u5mr_df[['country_name', 'u5mr_status']],
            on='country_name',
            how='left'
        )
        print(f"    Final merged dataset: {len(final_df)} records")
        
        # Show merge statistics
        print(f"    Final columns: {list(final_df.columns)}")
        print(f"    Unique countries in final dataset: {final_df['country_name'].nunique()}")
        print(f"    Unique indicators: {final_df['indicator'].unique()}")
        print(f"    Year range: {final_df['year'].min()} - {final_df['year'].max()}")
        
        # Show status distribution in final dataset
        status_dist = final_df['u5mr_status'].value_counts()
        print(f"    U5MR status distribution: {status_dist.to_dict()}")
        
        return final_df
    
    def _save_cleaned_datasets(self, cleaned_data: Dict[str, pd.DataFrame]):
        """Save cleaned datasets to processed folder."""
        processed_path = self.data_paths['processed']
        processed_path.mkdir(parents=True, exist_ok=True)
        
        for name, df in cleaned_data.items():
            if name != 'merged':  # Don't save merged data yet
                file_path = processed_path / f"{name}_cleaned.csv"
                df.to_csv(file_path, index=False)
                print(f"    Saved {name} cleaned data to {file_path}")
    
    def get_cleaning_summary(self, cleaned_data: Dict[str, pd.DataFrame]) -> Dict[str, Any]:
        """Get summary of cleaning results."""
        summary = {}
        
        for name, df in cleaned_data.items():
            summary[name] = {
                'records': len(df),
                'columns': list(df.columns),
                'unique_countries': df['country_name'].nunique() if 'country_name' in df.columns else 0
            }
        
        return summary 