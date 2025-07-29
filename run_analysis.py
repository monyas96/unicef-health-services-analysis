#!/usr/bin/env python3
"""
UNICEF Health Services Coverage Analysis - Main Execution Script
==============================================================

This script executes the complete analysis workflow:
1. Data cleaning and merging
2. Births-weighted coverage calculation
3. Data export for interactive dashboard

This is the main entry point for the UNICEF technical evaluation.
"""

import sys
from pathlib import Path
import pandas as pd
import subprocess
import webbrowser
import time

# Add src to path
sys.path.append('src')

from src.steps.data_cleaner import DataCleaner
from src.steps.coverage_calculator import CoverageCalculator


def launch_streamlit_dashboard():
    """Launch the Streamlit interactive dashboard."""
    print("\n" + "="*80)
    print("LAUNCHING INTERACTIVE DASHBOARD")
    print("="*80)
    
    try:
        # Check if streamlit is available
        import streamlit
        print("✓ Streamlit is available")
        
        # Check if the dashboard file exists
        dashboard_file = Path('app.py')
        if not dashboard_file.exists():
            print("❌ Dashboard file not found: app.py")
            return False
        
        print("Launching Streamlit dashboard...")
        print("   Dashboard will open in your default browser")
        print("   Local URL: http://localhost:8501")
        print("   Network URL: http://192.168.0.199:8501")
        print("\n   To stop the dashboard, press Ctrl+C in the terminal")
        
        # Launch Streamlit in background
        process = subprocess.Popen([
            'streamlit', 'run', 'app.py',
            '--server.headless', 'true',
            '--server.port', '8501'
        ])
        
        # Wait a moment for Streamlit to start
        time.sleep(3)
        
        # Open browser
        try:
            webbrowser.open('http://localhost:8501')
            print("✓ Browser opened automatically")
        except:
            print("⚠️  Please manually open: http://localhost:8501")
        
        print("\nDashboard Features:")
        print("   • Interactive visualizations")
        print("   • Real-time filtering")
        print("   • Country-level exploration")
        print("   • Time series analysis")
        print("   • Methodology explanation")
        
        return process
        
    except ImportError:
        print("❌ Streamlit not installed. Install with: pip install streamlit plotly")
        return False
    except Exception as e:
        print(f"❌ Error launching dashboard: {e}")
        return False


def main():
    """Execute the complete UNICEF health services coverage analysis."""
    print("="*80)
    print("UNICEF HEALTH SERVICES COVERAGE ANALYSIS")
    print("Technical Evaluation for Data and Analytics Education Team")
    print("="*80)
    
    # Applied positions
    print("\nAPPLIED POSITIONS:")
    print("  • Data and Analytics Education Team Consultant")
    print("  • UNICEF Technical Evaluation")
    
    # Set up paths
    data_paths = {
        'raw': Path('data/raw'),
        'processed': Path('data/processed'),
        'output': Path('data/output')
    }
    
    # Create output directories
    for path in data_paths.values():
        path.mkdir(parents=True, exist_ok=True)
    
    # Configuration
    config = {
        'processing': {
            'min_year': 2018,
            'max_year': 2022
        }
    }
    
    try:
        # Step 1: Data Cleaning and Merging
        print("\n" + "="*80)
        print("STEP 1: DATA CLEANING AND MERGING")
        print("="*80)
        
        cleaner = DataCleaner(config, data_paths)
        
        # Analyze data structure
        print("\nAnalyzing data structure...")
        analysis = cleaner.analyze_data_structure()
        
        # Clean and merge all datasets
        print("\nCleaning and merging datasets...")
        cleaned_data = cleaner.clean_all_datasets()
        
        merged_data = cleaned_data['merged']
        print(f"\n✓ Data cleaning completed successfully!")
        print(f"  Final merged dataset: {len(merged_data)} records")
        print(f"  Unique countries: {merged_data['country_name'].nunique()}")
        print(f"  Unique indicators: {merged_data['indicator'].unique()}")
        
        # Step 2: Births-Weighted Coverage Calculation
        print("\n" + "="*80)
        print("STEP 2: BIRTHS-WEIGHTED COVERAGE CALCULATION")
        print("="*80)
        
        calculator = CoverageCalculator(merged_data)
        results = calculator.get_results_for_reporting()
        
        print(f"\n✓ Coverage calculation completed successfully!")
        print(f"  Overall coverage calculated for {len(results['overall_coverage'])} indicators")
        print(f"  Status comparison completed for {len(results['by_status'])} U5MR statuses")
        
        # Step 3: Data Export for Dashboard
        print("\n" + "="*80)
        print("STEP 3: DATA EXPORT FOR INTERACTIVE DASHBOARD")
        print("="*80)
        
        # Save merged data for dashboard
        print("\nSaving data for interactive dashboard...")
        merged_data.to_csv(data_paths['output'] / 'final_merged_dataset.csv', index=False)
        
        # Save results as JSON for dashboard
        import json
        
        # Convert DataFrame to dict for JSON serialization
        results_for_json = results.copy()
        if 'data_for_visualization' in results_for_json:
            # Convert DataFrame to dict if it exists
            if isinstance(results_for_json['data_for_visualization'], pd.DataFrame):
                results_for_json['data_for_visualization'] = results_for_json['data_for_visualization'].to_dict('records')
        
        with open(data_paths['output'] / 'analysis_results.json', 'w') as f:
            json.dump(results_for_json, f, indent=2)
        
        print("✓ Data exported successfully for Streamlit dashboard")
        
        # Final summary
        print("\n" + "="*80)
        print("ANALYSIS COMPLETED SUCCESSFULLY!")
        print("="*80)
        
        print(f"\nOUTPUT FILES:")
        print(f"  • Analysis Results: data/output/analysis_results.json")
        print(f"  • Merged Dataset: data/output/final_merged_dataset.csv")
        print(f"  • Interactive Dashboard: app.py")
        
        print(f"\nKEY RESULTS:")
        for indicator, data in results['overall_coverage'].items():
            print(f"  • {indicator}: {data['births_weighted_avg']:.2f}% (births-weighted)")
        
        print(f"\nNEXT STEPS:")
        print(f"  1. Launch interactive dashboard: streamlit run app.py")
        print(f"  2. Explore the analysis results interactively")
        print(f"  3. Upload the complete repository to GitHub")
        print(f"  4. Share the GitHub repository link for evaluation")
        
        print(f"\nANALYSIS WORKFLOW COMPLETED!")
        print(f"   This analysis demonstrates:")
        print(f"   • Reproducible research practices")
        print(f"   • Modular code structure")
        print(f"   • Comprehensive data processing")
        print(f"   • Births-weighted statistical analysis")
        print(f"   • Interactive dashboard capabilities")
        
        # Ask user if they want to launch the dashboard
        print(f"\n" + "="*80)
        print("INTERACTIVE DASHBOARD OPTION")
        print("="*80)
        print("Would you like to launch the interactive Streamlit dashboard?")
        print("This will open a web browser with interactive visualizations.")
        
        try:
            response = input("Launch dashboard? (y/n): ").lower().strip()
            if response in ['y', 'yes', '']:
                dashboard_process = launch_streamlit_dashboard()
                if dashboard_process:
                    print("\nDashboard launched successfully!")
                    print("Press Ctrl+C to stop the dashboard when finished.")
                    try:
                        dashboard_process.wait()
                    except KeyboardInterrupt:
                        print("\nDashboard stopped by user.")
                        dashboard_process.terminate()
                else:
                    print("\n⚠️  Dashboard could not be launched.")
            else:
                print("\nTo launch the dashboard later, run:")
                print("   streamlit run app.py")
        except KeyboardInterrupt:
            print("\nTo launch the dashboard later, run:")
            print("   streamlit run app.py")
        
        return True
        
    except Exception as e:
        print(f"\n❌ ERROR: Analysis failed - {e}")
        import traceback
        traceback.print_exc()
        return False


if __name__ == "__main__":
    success = main()
    if success:
        print(f"\nUNICEF Technical Evaluation Analysis Completed Successfully!")
    else:
        print(f"\nAnalysis failed. Please check the error messages above.")
        sys.exit(1) 