#!/usr/bin/env python3
"""
Report Generator for UNICEF Health Services Coverage Analysis
==========================================================

This module generates comprehensive reports including:
- Visualizations comparing coverage for on-track vs off-track countries
- Statistical analysis and interpretation
- PDF and HTML report generation

Key Functions:
- create_visualizations(): Generate charts and graphs
- generate_report(): Create comprehensive report
- save_results(): Save analysis results to files
"""

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
from pathlib import Path
from typing import Dict, Any
import json
from datetime import datetime


class ReportGenerator:
    """Generates reports and visualizations for the coverage analysis."""
    
    def __init__(self, results: Dict[str, Any], output_path: Path):
        """Initialize with analysis results and output path."""
        self.results = results
        self.output_path = output_path
        self.output_path.mkdir(parents=True, exist_ok=True)
        
        # Set up plotting style
        plt.style.use('default')
        sns.set_palette("husl")
    
    def create_visualizations(self) -> Dict[str, str]:
        """Create all visualizations for the report."""
        print("="*80)
        print("CREATING VISUALIZATIONS")
        print("="*80)
        
        viz_files = {}
        
        # 1. Coverage comparison by U5MR status
        viz_files['coverage_comparison'] = self._create_coverage_comparison_chart()
        
        # 2. Population-weighted vs simple averages
        viz_files['averages_comparison'] = self._create_averages_comparison_chart()
        
        # 3. Coverage distribution by indicator
        viz_files['coverage_distribution'] = self._create_coverage_distribution_chart()
        
        # 4. Summary statistics chart
        viz_files['summary_chart'] = self._create_summary_chart()
        
        print("✓ All visualizations created successfully")
        return viz_files
    
    def _create_coverage_comparison_chart(self) -> str:
        """Create chart comparing coverage for on-track vs off-track countries."""
        print("  Creating coverage comparison chart...")
        
        viz_data = self.results['data_for_visualization']
        
        # Create the plot
        fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(15, 6))
        
        # ANC4 comparison
        anc4_data = viz_data[viz_data['indicator'] == 'MNCH_ANC4']
        if not anc4_data.empty:
            status_order = ['on_track', 'off_track']
            colors = ['#2E8B57', '#CD5C5C']
            
            bars1 = ax1.bar(
                [status.replace('_', ' ').title() for status in status_order],
                [anc4_data[anc4_data['u5mr_status'] == status]['coverage_value'].iloc[0] 
                 if len(anc4_data[anc4_data['u5mr_status'] == status]) > 0 else 0 
                 for status in status_order],
                color=colors,
                alpha=0.8
            )
            
            # Add value labels on bars
            for bar in bars1:
                height = bar.get_height()
                ax1.text(bar.get_x() + bar.get_width()/2., height + 0.5,
                        f'{height:.1f}%', ha='center', va='bottom', fontweight='bold')
            
            ax1.set_title('ANC4 Coverage by U5MR Status', fontsize=14, fontweight='bold')
            ax1.set_ylabel('Coverage (%)', fontsize=12)
            ax1.set_ylim(0, 100)
            ax1.grid(axis='y', alpha=0.3)
        
        # SBA comparison
        sba_data = viz_data[viz_data['indicator'] == 'MNCH_SAB']
        if not sba_data.empty:
            bars2 = ax2.bar(
                [status.replace('_', ' ').title() for status in status_order],
                [sba_data[sba_data['u5mr_status'] == status]['coverage_value'].iloc[0] 
                 if len(sba_data[sba_data['u5mr_status'] == status]) > 0 else 0 
                 for status in status_order],
                color=colors,
                alpha=0.8
            )
            
            # Add value labels on bars
            for bar in bars2:
                height = bar.get_height()
                ax2.text(bar.get_x() + bar.get_width()/2., height + 0.5,
                        f'{height:.1f}%', ha='center', va='bottom', fontweight='bold')
            
            ax2.set_title('SBA Coverage by U5MR Status', fontsize=14, fontweight='bold')
            ax2.set_ylabel('Coverage (%)', fontsize=12)
            ax2.set_ylim(0, 100)
            ax2.grid(axis='y', alpha=0.3)
        
        plt.tight_layout()
        
        # Save the plot
        filename = 'coverage_comparison.png'
        filepath = self.output_path / filename
        plt.savefig(filepath, dpi=300, bbox_inches='tight')
        plt.close()
        
        print(f"    Saved: {filepath}")
        return filename
    
    def _create_averages_comparison_chart(self) -> str:
        """Create chart comparing population-weighted vs simple averages."""
        print("  Creating averages comparison chart...")
        
        # Prepare data
        comparison_data = []
        for indicator in self.results['overall_coverage'].keys():
            overall = self.results['overall_coverage'][indicator]
            comparison_data.append({
                'indicator': indicator,
                'type': 'Population-weighted',
                'value': overall['births_weighted_avg']
            })
            comparison_data.append({
                'indicator': indicator,
                'type': 'Simple average',
                'value': overall['simple_avg']
            })
        
        comp_df = pd.DataFrame(comparison_data)
        
        # Create the plot
        fig, ax = plt.subplots(figsize=(10, 6))
        
        # Create grouped bar chart
        indicators = comp_df['indicator'].unique()
        x = np.arange(len(indicators))
        width = 0.35
        
        weighted_vals = [comp_df[(comp_df['indicator'] == ind) & (comp_df['type'] == 'Population-weighted')]['value'].iloc[0] 
                        for ind in indicators]
        simple_vals = [comp_df[(comp_df['indicator'] == ind) & (comp_df['type'] == 'Simple average')]['value'].iloc[0] 
                      for ind in indicators]
        
        bars1 = ax.bar(x - width/2, weighted_vals, width, label='Population-weighted', color='#2E8B57', alpha=0.8)
        bars2 = ax.bar(x + width/2, simple_vals, width, label='Simple average', color='#4682B4', alpha=0.8)
        
        # Add value labels
        for bars in [bars1, bars2]:
            for bar in bars:
                height = bar.get_height()
                ax.text(bar.get_x() + bar.get_width()/2., height + 0.5,
                       f'{height:.1f}%', ha='center', va='bottom', fontsize=10)
        
        ax.set_xlabel('Health Service Indicator', fontsize=12)
        ax.set_ylabel('Coverage (%)', fontsize=12)
        ax.set_title('Population-weighted vs Simple Averages', fontsize=14, fontweight='bold')
        ax.set_xticks(x)
        ax.set_xticklabels(indicators)
        ax.legend()
        ax.grid(axis='y', alpha=0.3)
        
        plt.tight_layout()
        
        # Save the plot
        filename = 'averages_comparison.png'
        filepath = self.output_path / filename
        plt.savefig(filepath, dpi=300, bbox_inches='tight')
        plt.close()
        
        print(f"    Saved: {filepath}")
        return filename
    
    def _create_coverage_distribution_chart(self) -> str:
        """Create chart showing coverage distribution by indicator."""
        print("  Creating coverage distribution chart...")
        
        # This would require the original data for distribution analysis
        # For now, create a summary chart
        fig, ax = plt.subplots(figsize=(12, 6))
        
        # Create summary table
        summary_data = []
        for indicator in self.results['overall_coverage'].keys():
            overall = self.results['overall_coverage'][indicator]
            summary_data.append({
                'indicator': indicator,
                'weighted_avg': overall['births_weighted_avg'],
                'simple_avg': overall['simple_avg'],
                'min_coverage': overall['min_coverage'],
                'max_coverage': overall['max_coverage'],
                'num_countries': overall['num_countries']
            })
        
        summary_df = pd.DataFrame(summary_data)
        
        # Create a comprehensive summary chart
        x = np.arange(len(summary_df))
        width = 0.2
        
        bars1 = ax.bar(x - width*1.5, summary_df['weighted_avg'], width, label='Population-weighted', color='#2E8B57')
        bars2 = ax.bar(x - width*0.5, summary_df['simple_avg'], width, label='Simple average', color='#4682B4')
        bars3 = ax.bar(x + width*0.5, summary_df['min_coverage'], width, label='Minimum', color='#CD5C5C')
        bars4 = ax.bar(x + width*1.5, summary_df['max_coverage'], width, label='Maximum', color='#FFD700')
        
        ax.set_xlabel('Health Service Indicator', fontsize=12)
        ax.set_ylabel('Coverage (%)', fontsize=12)
        ax.set_title('Coverage Statistics by Indicator', fontsize=14, fontweight='bold')
        ax.set_xticks(x)
        ax.set_xticklabels(summary_df['indicator'])
        ax.legend()
        ax.grid(axis='y', alpha=0.3)
        
        plt.tight_layout()
        
        # Save the plot
        filename = 'coverage_distribution.png'
        filepath = self.output_path / filename
        plt.savefig(filepath, dpi=300, bbox_inches='tight')
        plt.close()
        
        print(f"    Saved: {filepath}")
        return filename
    
    def _create_summary_chart(self) -> str:
        """Create summary chart with key statistics."""
        print("  Creating summary chart...")
        
        fig, ((ax1, ax2), (ax3, ax4)) = plt.subplots(2, 2, figsize=(15, 10))
        
        # 1. Total countries by status
        status_dist = self.results['summary']['u5mr_status_distribution']
        status_labels = [k.replace('_', ' ').title() for k in status_dist.keys()]
        status_values = list(status_dist.values())
        
        ax1.pie(status_values, labels=status_labels, autopct='%1.1f%%', startangle=90)
        ax1.set_title('Distribution of Countries by U5MR Status', fontweight='bold')
        
        # 2. Coverage range by indicator
        indicators = list(self.results['overall_coverage'].keys())
        weighted_avgs = [self.results['overall_coverage'][ind]['births_weighted_avg'] for ind in indicators]
        
        bars = ax2.bar(indicators, weighted_avgs, color=['#2E8B57', '#4682B4'])
        ax2.set_title('Population-weighted Coverage by Indicator', fontweight='bold')
        ax2.set_ylabel('Coverage (%)')
        ax2.grid(axis='y', alpha=0.3)
        
        # Add value labels
        for bar in bars:
            height = bar.get_height()
            ax2.text(bar.get_x() + bar.get_width()/2., height + 0.5,
                    f'{height:.1f}%', ha='center', va='bottom', fontweight='bold')
        
        # 3. Year range
        year_range = self.results['summary']['year_range']
        ax3.bar(['Min Year', 'Max Year'], [year_range['min'], year_range['max']], color=['#CD5C5C', '#FFD700'])
        ax3.set_title('Data Year Range', fontweight='bold')
        ax3.set_ylabel('Year')
        ax3.grid(axis='y', alpha=0.3)
        
        # 4. Total population
        total_births = self.results['summary']['total_births'] / 1e6  # Convert to millions
        ax4.bar(['Total Births'], [total_births], color='#9370DB')
        ax4.set_title('Total Births (Millions)', fontweight='bold')
        ax4.set_ylabel('Births (Millions)')
        ax4.grid(axis='y', alpha=0.3)
        
        # Add value label
        ax4.text(0, total_births + total_births*0.05, f'{total_births:.1f}M', ha='center', va='bottom', fontweight='bold')
        
        plt.tight_layout()
        
        # Save the plot
        filename = 'summary_chart.png'
        filepath = self.output_path / filename
        plt.savefig(filepath, dpi=300, bbox_inches='tight')
        plt.close()
        
        print(f"    Saved: {filepath}")
        return filename
    
    def generate_report(self, viz_files: Dict[str, str]) -> str:
        """Generate comprehensive HTML report."""
        print("\n" + "="*80)
        print("GENERATING COMPREHENSIVE REPORT")
        print("="*80)
        
        # Create HTML report
        html_content = self._create_html_report(viz_files)
        
        # Save HTML report
        html_filename = 'UNICEF_Health_Services_Analysis.html'
        html_filepath = self.output_path / html_filename
        with open(html_filepath, 'w', encoding='utf-8') as f:
            f.write(html_content)
        
        print(f"✓ HTML report saved: {html_filepath}")
        
        # Save results as JSON
        json_filename = 'analysis_results.json'
        json_filepath = self.output_path / json_filename
        with open(json_filepath, 'w', encoding='utf-8') as f:
            json.dump(self.results, f, indent=2, default=str)
        
        print(f"✓ Results saved as JSON: {json_filepath}")
        
        return html_filename
    
    def _create_html_report(self, viz_files: Dict[str, str]) -> str:
        """Create comprehensive HTML report."""
        
        # Get key statistics
        summary = self.results['summary']
        overall_coverage = self.results['overall_coverage']
        status_comparison = self.results['by_status']
        
        # Create interpretation text
        interpretation = self._create_interpretation_text()
        
        html = f"""
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>UNICEF Health Services Coverage Analysis</title>
    <style>
        body {{
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            line-height: 1.6;
            margin: 0;
            padding: 20px;
            background-color: #f5f5f5;
        }}
        .container {{
            max-width: 1200px;
            margin: 0 auto;
            background-color: white;
            padding: 30px;
            border-radius: 10px;
            box-shadow: 0 0 20px rgba(0,0,0,0.1);
        }}
        h1 {{
            color: #2c3e50;
            text-align: center;
            border-bottom: 3px solid #3498db;
            padding-bottom: 10px;
        }}
        h2 {{
            color: #34495e;
            border-left: 4px solid #3498db;
            padding-left: 15px;
        }}
        h3 {{
            color: #2c3e50;
        }}
        .stats-grid {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
            gap: 20px;
            margin: 20px 0;
        }}
        .stat-card {{
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            padding: 20px;
            border-radius: 10px;
            text-align: center;
        }}
        .stat-value {{
            font-size: 2em;
            font-weight: bold;
            margin: 10px 0;
        }}
        .visualization {{
            text-align: center;
            margin: 30px 0;
        }}
        .visualization img {{
            max-width: 100%;
            height: auto;
            border-radius: 10px;
            box-shadow: 0 5px 15px rgba(0,0,0,0.2);
        }}
        .interpretation {{
            background-color: #ecf0f1;
            padding: 20px;
            border-radius: 10px;
            margin: 20px 0;
        }}
        .caveats {{
            background-color: #fff3cd;
            border: 1px solid #ffeaa7;
            padding: 15px;
            border-radius: 5px;
            margin: 20px 0;
        }}
        table {{
            width: 100%;
            border-collapse: collapse;
            margin: 20px 0;
        }}
        th, td {{
            padding: 12px;
            text-align: left;
            border-bottom: 1px solid #ddd;
        }}
        th {{
            background-color: #3498db;
            color: white;
        }}
        tr:nth-child(even) {{
            background-color: #f2f2f2;
        }}
    </style>
</head>
<body>
    <div class="container">
        <h1>UNICEF Health Services Coverage Analysis</h1>
        <p><strong>Generated on:</strong> {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}</p>
        
        <h2>Executive Summary</h2>
        <div class="stats-grid">
            <div class="stat-card">
                <h3>Total Countries</h3>
                <div class="stat-value">{summary['unique_countries']}</div>
                <p>analyzed</p>
            </div>
            <div class="stat-card">
                <h3>Total Births (2022)</h3>
                <div class="stat-value">{summary['total_births']:,.0f}</div>
                <p>covered</p>
            </div>
            <div class="stat-card">
                <h3>Data Period</h3>
                <div class="stat-value">{summary['year_range']['min']}-{summary['year_range']['max']}</div>
                <p>years</p>
            </div>
            <div class="stat-card">
                <h3>Indicators</h3>
                <div class="stat-value">{len(summary['indicators'])}</div>
                <p>analyzed</p>
            </div>
        </div>
        
        <h2>Population-Weighted Coverage Results</h2>
        <table>
            <thead>
                <tr>
                    <th>Indicator</th>
                    <th>Population-Weighted Average (%)</th>
                    <th>Simple Average (%)</th>
                    <th>Countries</th>
                    <th>Coverage Range (%)</th>
                </tr>
            </thead>
            <tbody>
        """
        
        for indicator, data in overall_coverage.items():
            html += f"""
                <tr>
                    <td><strong>{indicator}</strong></td>
                    <td>{data['births_weighted_avg']:.2f}%</td>
                    <td>{data['simple_avg']:.2f}%</td>
                    <td>{data['num_countries']}</td>
                    <td>{data['min_coverage']:.1f}% - {data['max_coverage']:.1f}%</td>
                </tr>
            """
        
        html += """
            </tbody>
        </table>
        
        <h2>Coverage by U5MR Status</h2>
        <table>
            <thead>
                <tr>
                    <th>Status</th>
                    <th>Indicator</th>
                    <th>Population-Weighted Average (%)</th>
                    <th>Countries</th>
                    <th>Total Population</th>
                </tr>
            </thead>
            <tbody>
        """
        
        for status, indicators in status_comparison.items():
            for indicator, data in indicators.items():
                html += f"""
                    <tr>
                        <td><strong>{status.replace('_', ' ').title()}</strong></td>
                        <td>{indicator}</td>
                        <td>{data['births_weighted_avg']:.2f}%</td>
                        <td>{data['num_countries']}</td>
                        <td>{data['total_births']:,.0f}</td>
                    </tr>
                """
        
        html += f"""
            </tbody>
        </table>
        
        <h2>Visualizations</h2>
        
        <div class="visualization">
            <h3>Coverage Comparison by U5MR Status</h3>
            <img src="{viz_files['coverage_comparison']}" alt="Coverage Comparison">
        </div>
        
        <div class="visualization">
            <h3>Population-weighted vs Simple Averages</h3>
            <img src="{viz_files['averages_comparison']}" alt="Averages Comparison">
        </div>
        
        <div class="visualization">
            <h3>Coverage Distribution by Indicator</h3>
            <img src="{viz_files['coverage_distribution']}" alt="Coverage Distribution">
        </div>
        
        <div class="visualization">
            <h3>Summary Statistics</h3>
            <img src="{viz_files['summary_chart']}" alt="Summary Chart">
        </div>
        
        <h2>Interpretation and Analysis</h2>
        <div class="interpretation">
            {interpretation}
        </div>
        
        <h2>Caveats and Assumptions</h2>
        <div class="caveats">
            <ul>
                <li><strong>Data Quality:</strong> The analysis assumes UNICEF data represents the most recent available estimate per country-year.</li>
                <li><strong>Population Data:</strong> Uses UN World Population Prospects 2022 for weighting calculations.</li>
                <li><strong>Country Matching:</strong> Relies on consistent country identifiers across datasets.</li>
                <li><strong>Missing Data:</strong> Countries with missing data are excluded from analysis.</li>
                <li><strong>Time Period:</strong> Focuses on 2018-2022 as specified in requirements.</li>
                <li><strong>U5MR Classification:</strong> Based on 2022 status classifications.</li>
            </ul>
        </div>
        
        <h2>Technical Details</h2>
        <p><strong>Analysis Method:</strong> Population-weighted averages were calculated using the formula:</p>
        <p style="text-align: center; font-family: monospace; background-color: #f8f9fa; padding: 10px; border-radius: 5px;">
            Weighted Average = Σ(coverage_value × population) / Σ(population)
        </p>
        
        <p><strong>Data Sources:</strong></p>
        <ul>
            <li>UNICEF Global Data Repository (ANC4 and SBA indicators)</li>
            <li>UN World Population Prospects 2022 (population data)</li>
            <li>Under-five Mortality Classification (U5MR status)</li>
        </ul>
        
        <footer style="text-align: center; margin-top: 50px; padding-top: 20px; border-top: 1px solid #ddd; color: #666;">
            <p>UNICEF Health Services Coverage Analysis | Generated for Technical Evaluation</p>
        </footer>
    </div>
</body>
</html>
        """
        
        return html
    
    def _create_interpretation_text(self) -> str:
        """Create interpretation text based on the results."""
        
        overall_coverage = self.results['overall_coverage']
        status_comparison = self.results['by_status']
        
        # Get key statistics
        anc4_overall = overall_coverage.get('MNCH_ANC4', {})
        sba_overall = overall_coverage.get('MNCH_SAB', {})
        
        anc4_on_track = status_comparison.get('on_track', {}).get('MNCH_ANC4', {})
        anc4_off_track = status_comparison.get('off_track', {}).get('MNCH_ANC4', {})
        sba_on_track = status_comparison.get('on_track', {}).get('MNCH_SAB', {})
        sba_off_track = status_comparison.get('off_track', {}).get('MNCH_SAB', {})
        
        interpretation = f"""
        <h3>Key Findings</h3>
        
        <p><strong>Overall Coverage:</strong> The analysis reveals significant variations in health service coverage across countries. 
        For ANC4 (antenatal care with 4+ visits), the births-weighted average coverage is {anc4_overall.get('births_weighted_avg', 0):.1f}%, 
        while for SBA (skilled birth attendance), it stands at {sba_overall.get('births_weighted_avg', 0):.1f}%.</p>
        
        <p><strong>U5MR Status Comparison:</strong> Countries classified as "on-track" for under-five mortality reduction show 
        {anc4_on_track.get('births_weighted_avg', 0):.1f}% ANC4 coverage and {sba_on_track.get('births_weighted_avg', 0):.1f}% SBA coverage, 
        compared to {anc4_off_track.get('births_weighted_avg', 0):.1f}% and {sba_off_track.get('births_weighted_avg', 0):.1f}% respectively 
        for "off-track" countries.</p>
        
        <p><strong>Population Weighting Impact:</strong> The difference between population-weighted and simple averages indicates 
        that larger countries may have different coverage patterns than smaller ones, highlighting the importance of 
        population-weighted analysis for global health assessments.</p>
        
        <h3>Policy Implications</h3>
        
        <p>The results suggest that countries making progress on under-five mortality targets also tend to have 
        better maternal health service coverage. This correlation underscores the interconnected nature of maternal 
        and child health outcomes and the importance of integrated health system strengthening.</p>
        
        <p>Countries classified as "off-track" for U5MR reduction may require targeted interventions to improve 
        maternal health service coverage, particularly in antenatal care and skilled birth attendance.</p>
        """
        
        return interpretation 