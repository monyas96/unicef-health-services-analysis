#!/usr/bin/env python3
"""
User Profile Configuration for UNICEF Health Services Coverage Analysis
====================================================================

This script ensures the analysis can run on any machine by:
1. Setting up the Python environment
2. Checking and installing required dependencies
3. Configuring paths and directories
4. Validating data files
5. Setting up logging and error handling

This is a required component for the UNICEF technical evaluation.
"""

import sys
import os
import subprocess
import platform
from pathlib import Path
import logging
from datetime import datetime


class UserProfile:
    """Manages environment setup and configuration for reproducible analysis."""
    
    def __init__(self):
        """Initialize the user profile configuration."""
        self.project_root = Path.cwd()
        self.data_dir = self.project_root / 'data'
        self.src_dir = self.project_root / 'src'
        self.output_dir = self.data_dir / 'output'
        self.processed_dir = self.data_dir / 'processed'
        self.raw_dir = self.data_dir / 'raw'
        
        # Required packages for the analysis
        self.required_packages = [
            'pandas>=1.3.0',
            'numpy>=1.20.0',
            'matplotlib>=3.3.0',
            'seaborn>=0.11.0',
            'openpyxl>=3.0.0',
            'xlrd>=2.0.0',
            'streamlit>=1.28.0',
            'plotly>=5.15.0'
        ]
        
        # Required data files
        self.required_data_files = [
            'fusion_GLOBAL_DATAFLOW_UNICEF_1.0_.MNCH_ANC4+MNCH_SAB..csv',
            'WPP2022_GEN_F01_DEMOGRAPHIC_INDICATORS_COMPACT_REV1.xlsx',
            'On-track and off-track countries.xlsx'
        ]
        
        # Optional dashboard files
        self.dashboard_files = [
            'app.py',
            'requirements.txt',
            'README_Streamlit.md'
        ]
        
        # Setup logging
        self.setup_logging()
        
    def setup_logging(self):
        """Configure logging for the analysis."""
        log_dir = self.project_root / 'logs'
        log_dir.mkdir(exist_ok=True)
        
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(levelname)s - %(message)s',
            handlers=[
                logging.FileHandler(log_dir / 'analysis.log'),
                logging.StreamHandler(sys.stdout)
            ]
        )
        self.logger = logging.getLogger(__name__)
    
    def check_python_version(self):
        """Check if Python version is compatible."""
        print("="*80)
        print("PYTHON ENVIRONMENT CHECK")
        print("="*80)
        
        python_version = sys.version_info
        print(f"Python version: {python_version.major}.{python_version.minor}.{python_version.micro}")
        
        if python_version < (3, 8):
            raise SystemError(f"Python 3.8+ required. Current version: {python_version}")
        
        print(f"✓ Python version {python_version.major}.{python_version.minor} is compatible")
        return True
    
    def check_system_info(self):
        """Display system information for reproducibility."""
        print("\nSYSTEM INFORMATION:")
        print(f"  Operating System: {platform.system()} {platform.release()}")
        print(f"  Machine: {platform.machine()}")
        print(f"  Processor: {platform.processor()}")
        print(f"  Python Location: {sys.executable}")
        print(f"  Working Directory: {self.project_root}")
    
    def check_dependencies(self):
        """Check and install required dependencies."""
        print("\n" + "="*80)
        print("DEPENDENCY CHECK")
        print("="*80)
        
        missing_packages = []
        
        for package in self.required_packages:
            package_name = package.split('>=')[0]
            try:
                __import__(package_name)
                print(f"✓ {package_name} is installed")
            except ImportError:
                missing_packages.append(package)
                print(f"✗ {package_name} is missing")
        
        if missing_packages:
            print(f"\nInstalling missing packages: {', '.join(missing_packages)}")
            self.install_packages(missing_packages)
        else:
            print("\n✓ All required packages are installed")
        
        return True
    
    def install_packages(self, packages):
        """Install missing packages using pip."""
        try:
            for package in packages:
                print(f"  Installing {package}...")
                subprocess.check_call([sys.executable, '-m', 'pip', 'install', package])
                print(f"  ✓ {package} installed successfully")
        except subprocess.CalledProcessError as e:
            print(f"❌ Error installing packages: {e}")
            raise SystemError("Failed to install required packages")
    
    def setup_directories(self):
        """Create necessary directories for the analysis."""
        print("\n" + "="*80)
        print("DIRECTORY SETUP")
        print("="*80)
        
        directories = [
            self.data_dir,
            self.raw_dir,
            self.processed_dir,
            self.output_dir,
            self.src_dir / 'load',
            self.project_root / 'logs'
        ]
        
        for directory in directories:
            directory.mkdir(parents=True, exist_ok=True)
            print(f"✓ Created/verified directory: {directory}")
        
        return True
    
    def check_data_files(self):
        """Check if required data files are present."""
        print("\n" + "="*80)
        print("DATA FILES CHECK")
        print("="*80)
        
        missing_files = []
        
        for filename in self.required_data_files:
            file_path = self.raw_dir / filename
            if file_path.exists():
                file_size = file_path.stat().st_size / 1024  # KB
                print(f"✓ {filename} ({file_size:.1f} KB)")
            else:
                missing_files.append(filename)
                print(f"✗ {filename} - MISSING")
        
        if missing_files:
            print(f"\n⚠️  WARNING: Missing data files:")
            for file in missing_files:
                print(f"    - {file}")
            print("\nPlease ensure the following files are in data/raw/:")
            print("   1. fusion_GLOBAL_DATAFLOW_UNICEF_1.0_.MNCH_ANC4+MNCH_SAB..csv")
            print("   2. WPP2022_GEN_F01_DEMOGRAPHIC_INDICATORS_COMPACT_REV1.xlsx")
            print("   3. On-track and off-track countries.xlsx")
            print("\n   These files should be manually downloaded from:")
            print("   - UNICEF Global Data Repository")
            print("   - UN World Population Prospects 2022")
            print("   - Under-five mortality classification data")
            
            response = input("\nContinue without data files? (y/N): ")
            if response.lower() != 'y':
                raise SystemError("Analysis requires data files to be present")
        else:
            print("\n✓ All required data files are present")
        
        # Check for dashboard files
        print(f"\nChecking dashboard files...")
        dashboard_files_present = []
        for file in self.dashboard_files:
            file_path = self.project_root / file
            if file_path.exists():
                print(f"  ✓ {file}")
                dashboard_files_present.append(file)
            else:
                print(f"  ⚠️  {file} (optional)")
        
        if len(dashboard_files_present) > 0:
            print(f"✓ Dashboard files available: {len(dashboard_files_present)}/{len(self.dashboard_files)}")
            print(f"  Interactive dashboard can be launched with: streamlit run app.py")
        else:
            print(f"⚠️  No dashboard files found (optional feature)")
        
        return True
    
    def validate_environment(self):
        """Validate the complete environment setup."""
        print("\n" + "="*80)
        print("ENVIRONMENT VALIDATION")
        print("="*80)
        
        # Test imports
        try:
            import pandas as pd
            import numpy as np
            import matplotlib.pyplot as plt
            import seaborn as sns
            import openpyxl
            import xlrd
            print("✓ All required packages can be imported")
            
            # Test optional dashboard packages
            try:
                import streamlit
                import plotly
                print("✓ Dashboard packages available")
            except ImportError:
                print("⚠️  Dashboard packages not available (optional)")
        except ImportError as e:
            print(f"❌ Import error: {e}")
            return False
        
        # Test file operations
        try:
            test_file = self.output_dir / 'test.txt'
            test_file.write_text('test')
            test_file.unlink()
            print("✓ File operations work correctly")
        except Exception as e:
            print(f"❌ File operation error: {e}")
            return False
        
        # Test path configuration
        if not self.project_root.exists():
            print("❌ Project root directory not found")
            return False
        
        print("✓ Environment validation completed successfully")
        return True
    
    def create_config_file(self):
        """Create a configuration file for the analysis."""
        config = {
            'project_info': {
                'name': 'UNICEF Health Services Coverage Analysis',
                'version': '1.0.0',
                'description': 'Technical evaluation for Data and Analytics Education Team',
                'created': datetime.now().isoformat(),
                'python_version': f"{sys.version_info.major}.{sys.version_info.minor}.{sys.version_info.micro}",
                'platform': platform.platform()
            },
            'paths': {
                'project_root': str(self.project_root),
                'data_dir': str(self.data_dir),
                'raw_dir': str(self.raw_dir),
                'processed_dir': str(self.processed_dir),
                'output_dir': str(self.output_dir),
                'src_dir': str(self.src_dir)
            },
            'analysis_settings': {
                'min_year': 2018,
                'max_year': 2022,
                'indicators': ['MNCH_ANC4', 'MNCH_SAB'],
                'births_weighting': True
            },
            'dashboard': {
                'available': len([f for f in self.dashboard_files if (self.project_root / f).exists()]) > 0,
                'files': self.dashboard_files,
                'launch_command': 'streamlit run app.py'
            },
            'dependencies': {
                'required_packages': self.required_packages,
                'data_files': self.required_data_files
            }
        }
        
        import json
        config_file = self.project_root / 'analysis_config.json'
        with open(config_file, 'w') as f:
            json.dump(config, f, indent=2)
        
        print(f"✓ Configuration file created: {config_file}")
        return config_file
    
    def run_setup(self):
        """Run the complete environment setup."""
        print("="*80)
        print("UNICEF HEALTH SERVICES ANALYSIS - ENVIRONMENT SETUP")
        print("Technical Evaluation for Data and Analytics Education Team")
        print("="*80)
        
        try:
            # Check Python version
            self.check_python_version()
            
            # Display system information
            self.check_system_info()
            
            # Check and install dependencies
            self.check_dependencies()
            
            # Setup directories
            self.setup_directories()
            
            # Check data files
            self.check_data_files()
            
            # Validate environment
            self.validate_environment()
            
            # Create configuration file
            config_file = self.create_config_file()
            
            print("\n" + "="*80)
            print("ENVIRONMENT SETUP COMPLETED SUCCESSFULLY!")
            print("="*80)
            
            print("\nSETUP SUMMARY:")
            print(f"  • Python environment: ✓ Compatible")
            print(f"  • Dependencies: ✓ Installed")
            print(f"  • Directories: ✓ Created")
            print(f"  • Data files: ✓ Checked")
            print(f"  • Configuration: ✓ Created")
            
            # Check dashboard availability
            dashboard_available = len([f for f in self.dashboard_files if (self.project_root / f).exists()]) > 0
            if dashboard_available:
                print(f"  • Interactive dashboard: ✓ Available")
            else:
                print(f"  • Interactive dashboard: ⚠️  Not found (optional)")
            
            print("\nREADY FOR ANALYSIS:")
            print("  Run the analysis with: python run_analysis.py")
            if dashboard_available:
                print("  Launch dashboard with: streamlit run app.py")
            
            print("\nPROJECT STRUCTURE:")
            print(f"  • Project root: {self.project_root}")
            print(f"  • Data directory: {self.data_dir}")
            print(f"  • Source code: {self.src_dir}")
            print(f"  • Output files: {self.output_dir}")
            
            return True
            
        except Exception as e:
            print(f"\n❌ SETUP FAILED: {e}")
            self.logger.error(f"Setup failed: {e}")
            return False


def main():
    """Main function to run the user profile setup."""
    profile = UserProfile()
    success = profile.run_setup()
    
    if success:
        print("\nEnvironment is ready for UNICEF technical evaluation analysis!")
        return 0
    else:
        print("\nEnvironment setup failed. Please check the errors above.")
        return 1


if __name__ == "__main__":
    sys.exit(main()) 