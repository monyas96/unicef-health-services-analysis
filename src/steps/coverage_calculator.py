#!/usr/bin/env python3
"""
Coverage Calculator for Population-Weighted Analysis
===================================================

This module calculates population-weighted coverage of health services:
- ANC4: % of women (aged 15–49) with at least 4 antenatal care visits
- SBA: % of deliveries attended by skilled health personnel

For countries categorized as on-track or off-track in achieving under-five mortality targets.

Key Functions:
- calculate_population_weighted_coverage(): Main calculation function
- analyze_by_u5mr_status(): Separate analysis for on-track vs off-track
- generate_summary_statistics(): Statistical summary of results
"""

import pandas as pd
import numpy as np
from typing import Dict, Any, Tuple
import logging


class CoverageCalculator:
    """Calculates population-weighted coverage for health services."""
    
    def __init__(self, merged_data: pd.DataFrame):
        """Initialize with merged dataset."""
        self.data = merged_data
        self.logger = logging.getLogger(__name__)
        
        # Validate required columns
        required_cols = ['country_name', 'indicator', 'year', 'coverage_value', 'births_2022', 'u5mr_status']
        missing_cols = [col for col in required_cols if col not in self.data.columns]
        if missing_cols:
            raise ValueError(f"Missing required columns: {missing_cols}")
    
    def calculate_population_weighted_coverage(self) -> Dict[str, Any]:
        """Calculate population-weighted coverage for ANC4 and SBA by U5MR status."""
        print("="*80)
        print("POPULATION-WEIGHTED COVERAGE CALCULATION")
        print("="*80)
        
        results = {}
        
                # Filter for valid data
        valid_data = self.data[
            (self.data['coverage_value'].notna()) &
            (self.data['births_2022'].notna()) &
            (self.data['coverage_value'] >= 0) &
            (self.data['coverage_value'] <= 100) &
            (self.data['births_2022'] > 0)
        ].copy()
        
        print(f"Valid data records: {len(valid_data)}")
        print(f"Unique countries: {valid_data['country_name'].nunique()}")
        print(f"Year range: {valid_data['year'].min()} - {valid_data['year'].max()}")
        
        # Calculate overall population-weighted averages
        results['overall'] = self._calculate_overall_coverage(valid_data)
        
        # Calculate by U5MR status
        results['by_status'] = self._calculate_by_u5mr_status(valid_data)
        
        # Calculate by indicator
        results['by_indicator'] = self._calculate_by_indicator(valid_data)
        
        # Generate summary statistics
        results['summary'] = self._generate_summary_statistics(valid_data)
        
        print("\n" + "="*80)
        print("CALCULATION COMPLETED")
        print("="*80)
        
        return results
    
    def _calculate_overall_coverage(self, data: pd.DataFrame) -> Dict[str, float]:
        """Calculate overall population-weighted coverage for each indicator."""
        print("\n OVERALL POPULATION-WEIGHTED COVERAGE:")
        print("-" * 50)
        
        overall_results = {}
        
        for indicator in data['indicator'].unique():
            indicator_data = data[data['indicator'] == indicator]
            
            # Calculate births-weighted average (using 2022 projected births as weights)
            weighted_avg = np.average(
                indicator_data['coverage_value'],
                weights=indicator_data['births_2022']
            )
            
            # Calculate simple average for comparison
            simple_avg = indicator_data['coverage_value'].mean()
            
            # Calculate statistics
            total_births = indicator_data['births_2022'].sum()
            num_countries = indicator_data['country_name'].nunique()
            
            overall_results[indicator] = {
                'births_weighted_avg': weighted_avg,
                'simple_avg': simple_avg,
                'total_births': total_births,
                'num_countries': num_countries,
                'min_coverage': indicator_data['coverage_value'].min(),
                'max_coverage': indicator_data['coverage_value'].max()
            }
            
            print(f"  {indicator}:")
            print(f"    Births-weighted average: {weighted_avg:.2f}%")
            print(f"    Simple average: {simple_avg:.2f}%")
            print(f"    Total births (2022): {total_births:,.0f}")
            print(f"    Number of countries: {num_countries}")
            print(f"    Coverage range: {indicator_data['coverage_value'].min():.1f}% - {indicator_data['coverage_value'].max():.1f}%")
        
        return overall_results
    
    def _calculate_by_u5mr_status(self, data: pd.DataFrame) -> Dict[str, Dict[str, Any]]:
        """Calculate population-weighted coverage by U5MR status (on-track vs off-track)."""
        print("\n📊 COVERAGE BY U5MR STATUS:")
        print("-" * 50)
        
        status_results = {}
        
        for status in data['u5mr_status'].unique():
            if pd.isna(status) or status == 'unknown':
                continue
                
            status_data = data[data['u5mr_status'] == status]
            
            print(f"\n  {status.upper().replace('_', ' ')} COUNTRIES:")
            print(f"    Number of countries: {status_data['country_name'].nunique()}")
            print(f"    Total births (2022): {status_data['births_2022'].sum():,.0f}")
            
            status_results[status] = {}
            
            for indicator in status_data['indicator'].unique():
                indicator_data = status_data[status_data['indicator'] == indicator]
                
                if len(indicator_data) == 0:
                    continue
                
                # Calculate births-weighted average (using 2022 projected births as weights)
                weighted_avg = np.average(
                    indicator_data['coverage_value'],
                    weights=indicator_data['births_2022']
                )
                
                # Calculate simple average
                simple_avg = indicator_data['coverage_value'].mean()
                
                # Calculate statistics
                total_births = indicator_data['births_2022'].sum()
                num_countries = indicator_data['country_name'].nunique()
                
                status_results[status][indicator] = {
                    'births_weighted_avg': weighted_avg,
                    'simple_avg': simple_avg,
                    'total_births': total_births,
                    'num_countries': num_countries,
                    'min_coverage': indicator_data['coverage_value'].min(),
                    'max_coverage': indicator_data['coverage_value'].max()
                }
                
                print(f"      {indicator}:")
                print(f"        Births-weighted average: {weighted_avg:.2f}%")
                print(f"        Simple average: {simple_avg:.2f}%")
                print(f"        Countries: {num_countries}")
                print(f"        Coverage range: {indicator_data['coverage_value'].min():.1f}% - {indicator_data['coverage_value'].max():.1f}%")
        
        return status_results
    
    def _calculate_by_indicator(self, data: pd.DataFrame) -> Dict[str, Dict[str, Any]]:
        """Calculate detailed statistics by indicator."""
        print("\n📊 DETAILED INDICATOR ANALYSIS:")
        print("-" * 50)
        
        indicator_results = {}
        
        for indicator in data['indicator'].unique():
            indicator_data = data[data['indicator'] == indicator]
            
            print(f"\n  {indicator}:")
            
            # Overall statistics
            overall_weighted = np.average(
                indicator_data['coverage_value'],
                weights=indicator_data['births_2022']
            )
            overall_simple = indicator_data['coverage_value'].mean()
            
            print(f"    Overall births-weighted average: {overall_weighted:.2f}%")
            print(f"    Overall simple average: {overall_simple:.2f}%")
            
            # By U5MR status
            status_comparison = {}
            for status in indicator_data['u5mr_status'].unique():
                if pd.isna(status) or status == 'unknown':
                    continue
                    
                status_data = indicator_data[indicator_data['u5mr_status'] == status]
                
                if len(status_data) > 0:
                    status_weighted = np.average(
                        status_data['coverage_value'],
                        weights=status_data['births_2022']
                    )
                    status_simple = status_data['coverage_value'].mean()
                    
                    status_comparison[status] = {
                        'births_weighted_avg': status_weighted,
                        'simple_avg': status_simple,
                        'num_countries': status_data['country_name'].nunique(),
                        'total_births': status_data['births_2022'].sum()
                    }
                    
                    print(f"      {status.replace('_', ' ').title()}: {status_weighted:.2f}% (weighted), {status_simple:.2f}% (simple)")
            
            indicator_results[indicator] = {
                'overall_weighted': overall_weighted,
                'overall_simple': overall_simple,
                'status_comparison': status_comparison,
                'total_countries': indicator_data['country_name'].nunique(),
                'total_births': indicator_data['births_2022'].sum()
            }
        
        return indicator_results
    
    def _generate_summary_statistics(self, data: pd.DataFrame) -> Dict[str, Any]:
        """Generate comprehensive summary statistics."""
        print("\n📊 SUMMARY STATISTICS:")
        print("-" * 50)
        
        summary = {
            'total_records': len(data),
            'unique_countries': data['country_name'].nunique(),
            'year_range': {
                'min': int(data['year'].min()),
                'max': int(data['year'].max())
            },
            'indicators': data['indicator'].unique().tolist(),
            'u5mr_status_distribution': data['u5mr_status'].value_counts().to_dict(),
            'total_births': data['births_2022'].sum(),
            'coverage_statistics': {
                'mean': data['coverage_value'].mean(),
                'median': data['coverage_value'].median(),
                'std': data['coverage_value'].std(),
                'min': data['coverage_value'].min(),
                'max': data['coverage_value'].max()
            }
        }
        
        print(f"  Total records: {summary['total_records']:,}")
        print(f"  Unique countries: {summary['unique_countries']}")
        print(f"  Year range: {summary['year_range']['min']} - {summary['year_range']['max']}")
        print(f"  Indicators: {summary['indicators']}")
        print(f"  Total births (2022): {summary['total_births']:,.0f}")
        print(f"  Coverage statistics:")
        print(f"    Mean: {summary['coverage_statistics']['mean']:.2f}%")
        print(f"    Median: {summary['coverage_statistics']['median']:.2f}%")
        print(f"    Standard deviation: {summary['coverage_statistics']['std']:.2f}%")
        print(f"    Range: {summary['coverage_statistics']['min']:.1f}% - {summary['coverage_statistics']['max']:.1f}%")
        
        return summary
    
    def get_results_for_reporting(self) -> Dict[str, Any]:
        """Get formatted results for reporting and visualization."""
        results = self.calculate_population_weighted_coverage()
        
        # Format results for easy reporting
        reporting_data = {
            'overall_coverage': results['overall'],
            'by_status': results['by_status'],
            'summary': results['summary'],
            'data_for_visualization': self._prepare_data_for_visualization()
        }
        
        return reporting_data
    
    def _prepare_data_for_visualization(self) -> pd.DataFrame:
        """Prepare data specifically for visualization."""
        # Create a summary dataframe for plotting
        viz_data = []
        
        for indicator in self.data['indicator'].unique():
            for status in self.data['u5mr_status'].unique():
                if pd.isna(status) or status == 'unknown':
                    continue
                    
                subset = self.data[
                    (self.data['indicator'] == indicator) &
                    (self.data['u5mr_status'] == status)
                ]
                
                if len(subset) > 0:
                                    weighted_avg = np.average(
                    subset['coverage_value'],
                    weights=subset['births_2022']
                )
                
                viz_data.append({
                    'indicator': indicator,
                    'u5mr_status': status,
                    'coverage_value': weighted_avg,
                    'num_countries': subset['country_name'].nunique(),
                    'total_births': subset['births_2022'].sum()
                })
        
        return pd.DataFrame(viz_data) 