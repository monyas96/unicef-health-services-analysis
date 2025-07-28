#!/usr/bin/env python3
"""
UNICEF Health Services Coverage Analysis - Interactive Dashboard
================================================================

Streamlit dashboard for interactive exploration of:
- Health service coverage by U5MR status
- Births-weighted vs simple averages
- Country-level comparisons
- Time series analysis
- Interactive filtering and exploration

This provides an interactive complement to the static HTML report.
"""

import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import json
from pathlib import Path
import warnings
warnings.filterwarnings('ignore')

# Page configuration
st.set_page_config(
    page_title="UNICEF Health Services Analysis",
    page_icon="",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for better styling
st.markdown("""
<style>
    .main-header {
        font-size: 2.5rem;
        color: #1f77b4;
        text-align: center;
        margin-bottom: 2rem;
    }
    .metric-card {
        background-color: #f0f2f6;
        padding: 1rem;
        border-radius: 0.5rem;
        border-left: 4px solid #1f77b4;
    }
    .sidebar .sidebar-content {
        background-color: #f8f9fa;
    }
</style>
""", unsafe_allow_html=True)

@st.cache_data
def load_analysis_data():
    """Load the analysis results and data."""
    try:
        # Load analysis results
        with open('data/output/analysis_results.json', 'r') as f:
            results = json.load(f)
        
        # Load merged dataset
        df = pd.read_csv('data/output/final_merged_dataset.csv')
        
        # Exclude NaN values from U5MR status
        df = df.dropna(subset=['u5mr_status'])
        
        # Create indicator mapping for full names
        indicator_mapping = {
            'MNCH_ANC4': 'Antenatal Care (4+ visits)',
            'MNCH_SAB': 'Skilled Birth Attendance'
        }
        
        # Add full indicator names
        df['indicator_full_name'] = df['indicator'].map(indicator_mapping)
        
        return results, df
    except Exception as e:
        st.error(f"Error loading data: {e}")
        return None, None

def create_header():
    """Create the main header."""
    st.markdown('<h1 class="main-header">UNICEF Health Services Coverage Analysis</h1>', unsafe_allow_html=True)
    st.markdown("### Interactive Dashboard for Technical Evaluation")
    st.markdown("**Applicant for Learning and Skills Data Analyst Consultant - Req.#581598**")
    st.markdown("---")

def display_overview_metrics(results):
    """Display key metrics in cards."""
    
    # Navigation guide at the beginning
    st.markdown("### Dashboard Navigation Guide")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("""
        **Overview**
        - Key metrics and findings summary
        - Filter usage guide
        - Dashboard introduction
        
        **ANC4 & SBA Coverage (2018-2022)**
        - Detailed analysis of Antenatal Care and Skilled Birth Attendance
        - Coverage distribution by U5MR status
        - Year distribution of estimates
        - Coverage vs births relationship
        """)
    
    with col2:
        st.markdown("""
        **Country Explorer**
        - Interactive filtering by U5MR status, indicator, and year
        - Scatter plot: Coverage vs births by country
        - Real-time summary statistics
        - Country-level data exploration
        
        **Weighting Comparison**
        - Births-weighted vs simple averages
        - Statistical methodology comparison
        - Impact of weighting on global estimates
        
        **Methodology and Results**
        - Comprehensive methodology explanation
        - Detailed results and discussion
        - Policy implications and interpretation
        - Caveats and assumptions
        """)
    
    st.markdown("---")
    st.subheader("Key Findings Overview")
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric(
            label="Antenatal Care (4+ visits) Coverage",
            value=f"{results['overall_coverage']['MNCH_ANC4']['births_weighted_avg']:.1f}%",
            delta="vs Simple Average"
        )
    
    with col2:
        st.metric(
            label="Skilled Birth Attendance Coverage",
            value=f"{results['overall_coverage']['MNCH_SAB']['births_weighted_avg']:.1f}%",
            delta="vs Simple Average"
        )
    
    with col3:
        st.metric(
            label="Countries Analyzed",
            value=f"{results['summary']['unique_countries']}",
            delta="Total Countries"
        )
    
    with col4:
        st.metric(
            label="Total Births (2022)",
            value=f"{results['summary']['total_births']:,.0f}",
            delta="Covered"
        )

def create_coverage_comparison_chart(results, chart_key="coverage_comparison"):
    """Create interactive coverage comparison chart."""
    st.subheader("Coverage Comparison by U5MR Status")
    
    # Prepare data for plotting
    indicators = ['MNCH_ANC4', 'MNCH_SAB']
    statuses = ['on_track', 'off_track']
    
    # Create indicator mapping for full names
    indicator_mapping = {
        'MNCH_ANC4': 'Antenatal Care (4+ visits)',
        'MNCH_SAB': 'Skilled Birth Attendance'
    }
    
    data = []
    for indicator in indicators:
        for status in statuses:
            if status in results['by_status'] and indicator in results['by_status'][status]:
                data.append({
                    'Indicator': indicator_mapping[indicator],
                    'Status': status.replace('_', ' ').title(),
                    'Coverage': results['by_status'][status][indicator]['births_weighted_avg'],
                    'Countries': results['by_status'][status][indicator]['num_countries']
                })
    
    df_plot = pd.DataFrame(data)
    
    # Create interactive bar chart
    fig = px.bar(
        df_plot,
        x='Indicator',
        y='Coverage',
        color='Status',
        barmode='group',
        text='Coverage',
        title="Health Service Coverage by U5MR Status",
        color_discrete_map={
            'On Track': '#2E8B57',
            'Off Track': '#CD5C5C'
        }
    )
    
    fig.update_traces(texttemplate='%{text:.1f}%', textposition='outside')
    fig.update_layout(
        yaxis_title="Coverage (%)",
        yaxis_range=[0, 100],
        showlegend=True,
        height=500
    )
    
    st.plotly_chart(fig, use_container_width=True, key=chart_key)
    
    # Display detailed statistics
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("**Antenatal Care (4+ visits):**")
        anc4_data = df_plot[df_plot['Indicator'] == 'Antenatal Care (4+ visits)']
        for _, row in anc4_data.iterrows():
            st.write(f"- {row['Status']}: {row['Coverage']:.1f}% ({row['Countries']} countries)")
    
    with col2:
        st.markdown("**Skilled Birth Attendance:**")
        sba_data = df_plot[df_plot['Indicator'] == 'Skilled Birth Attendance']
        for _, row in sba_data.iterrows():
            st.write(f"- {row['Status']}: {row['Coverage']:.1f}% ({row['Countries']} countries)")

def create_weighted_vs_simple_chart(results):
    """Create comparison of births-weighted vs simple averages."""
    st.subheader("Births-Weighted vs Simple Averages")
    
    # Create indicator mapping for full names
    indicator_mapping = {
        'MNCH_ANC4': 'Antenatal Care (4+ visits)',
        'MNCH_SAB': 'Skilled Birth Attendance'
    }
    
    data = []
    for indicator, metrics in results['overall_coverage'].items():
        data.append({
            'Indicator': indicator_mapping[indicator],
            'Method': 'Births-Weighted',
            'Coverage': metrics['births_weighted_avg']
        })
        data.append({
            'Indicator': indicator_mapping[indicator],
            'Method': 'Simple Average',
            'Coverage': metrics['simple_avg']
        })
    
    df_plot = pd.DataFrame(data)
    
    fig = px.bar(
        df_plot,
        x='Indicator',
        y='Coverage',
        color='Method',
        barmode='group',
        text='Coverage',
        title="Comparison of Weighting Methods",
        color_discrete_map={
            'Births-Weighted': '#1f77b4',
            'Simple Average': '#ff7f0e'
        }
    )
    
    fig.update_traces(texttemplate='%{text:.1f}%', textposition='outside')
    fig.update_layout(
        yaxis_title="Coverage (%)",
        yaxis_range=[0, 100],
        height=500
    )
    
    st.plotly_chart(fig, use_container_width=True)
    
    # Calculate differences
    st.markdown("**Key Insights:**")
    for indicator in ['Antenatal Care (4+ visits)', 'Skilled Birth Attendance']:
        indicator_data = df_plot[df_plot['Indicator'] == indicator]
        if len(indicator_data) == 2:
            weighted = indicator_data[indicator_data['Method'] == 'Births-Weighted']['Coverage'].iloc[0]
            simple = indicator_data[indicator_data['Method'] == 'Simple Average']['Coverage'].iloc[0]
            diff = weighted - simple
            st.write(f"- **{indicator}:** Births-weighted ({weighted:.1f}%) vs Simple ({simple:.1f}%) = {diff:+.1f}% difference")

def create_country_explorer(df):
    """Create interactive country-level data explorer."""
    st.subheader("Country-Level Data Explorer")
    
    # Sidebar filters
    st.sidebar.markdown("### Filters")
    
    # U5MR Status filter
    status_filter = st.sidebar.multiselect(
        "U5MR Status:",
        options=df['u5mr_status'].unique(),
        default=df['u5mr_status'].unique()
    )
    
    # Indicator filter
    indicator_filter = st.sidebar.multiselect(
        "Indicator:",
        options=df['indicator_full_name'].unique(),
        default=df['indicator_full_name'].unique()
    )
    
    # Year filter
    min_year = int(df['year'].min())
    max_year = int(df['year'].max())
    year_filter = st.sidebar.slider(
        "Year Range:",
        min_value=min_year,
        max_value=max_year,
        value=(min_year, max_year)
    )
    
    # Apply filters
    filtered_df = df[
        (df['u5mr_status'].isin(status_filter)) &
        (df['indicator_full_name'].isin(indicator_filter)) &
        (df['year'] >= year_filter[0]) &
        (df['year'] <= year_filter[1])
    ]
    
    # Display filtered data
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.markdown(f"**Showing {len(filtered_df)} records**")
        
        # Create scatter plot
        fig = px.scatter(
            filtered_df,
            x='births_2022',
            y='coverage_value',
            color='indicator_full_name',
            size='coverage_value',
            hover_data=['country_name', 'u5mr_status', 'year'],
            title="Coverage vs Births by Country",
            labels={
                'births_2022': 'Births (2022)',
                'coverage_value': 'Coverage (%)',
                'indicator_full_name': 'Indicator'
            },
            color_discrete_map={
                'Antenatal Care (4+ visits)': '#1f77b4',
                'Skilled Birth Attendance': '#ff7f0e'
            }
        )
        
        fig.update_layout(height=500)
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        st.markdown("**Summary Statistics:**")
        
        # Coverage statistics
        st.metric("Average Coverage", f"{filtered_df['coverage_value'].mean():.1f}%")
        st.metric("Median Coverage", f"{filtered_df['coverage_value'].median():.1f}%")
        st.metric("Total Births", f"{filtered_df['births_2022'].sum():,.0f}")
        
        # Status distribution
        st.markdown("**Status Distribution:**")
        status_counts = filtered_df['u5mr_status'].value_counts()
        for status, count in status_counts.items():
            st.write(f"- {status}: {count} records")
        
        # Indicator distribution
        st.markdown("**Indicator Distribution:**")
        indicator_counts = filtered_df['indicator_full_name'].value_counts()
        for indicator, count in indicator_counts.items():
            st.write(f"- {indicator}: {count} records")

def create_anc4_sba_coverage_analysis(df):
    """Create detailed analysis of ANC4 and SBA coverage estimates from 2018-2022."""
    # Filter for ANC4 and SBA indicators
    anc4_sba_df = df[df['indicator_full_name'].isin(['Antenatal Care (4+ visits)', 'Skilled Birth Attendance'])].copy()
    
    # Coverage Distribution by U5MR Status
    with st.expander("Coverage Distribution by U5MR Status", expanded=True):
            st.markdown("""
            **What this graph shows us:**
            This box plot reveals the distribution of coverage values for each indicator across countries classified by their U5MR status. 
            It helps identify whether there are systematic differences in health service coverage between countries that are on-track 
            versus off-track for achieving child mortality targets. The median, quartiles, and outliers provide insights into 
            the equity gaps and variability in service delivery.
            """)
            
            fig = px.box(
                anc4_sba_df,
                x='indicator_full_name',
                y='coverage_value',
                color='u5mr_status',
                title="Coverage Distribution by U5MR Status",
                labels={
                    'coverage_value': 'Coverage (%)',
                    'indicator_full_name': 'Indicator',
                    'u5mr_status': 'U5MR Status'
                }
            )
            
            fig.update_layout(height=500)
            st.plotly_chart(fig, use_container_width=True)
    
    # Year Distribution of Estimates
    with st.expander("Year Distribution of Estimates", expanded=True):
            st.markdown("""
            **What this graph shows us:**
            This bar chart displays the number of countries reporting estimates for each indicator by year. 
            It helps identify trends in data availability and potential gaps in reporting, especially during 
            the COVID-19 pandemic period (2020-2022). Understanding data availability patterns is crucial 
            for assessing the reliability and completeness of global health monitoring.
            """)
            
            year_dist = anc4_sba_df.groupby(['year', 'indicator_full_name']).size().reset_index(name='count')
            
            fig = px.bar(
                year_dist,
                x='year',
                y='count',
                color='indicator_full_name',
                title="Number of Countries with Estimates by Year",
                labels={
                    'count': 'Number of Countries',
                    'year': 'Year',
                    'indicator_full_name': 'Indicator'
                }
            )
            
            fig.update_layout(height=400)
            st.plotly_chart(fig, use_container_width=True)
    
    # Coverage vs Births Relationship
    with st.expander("Coverage vs Births Relationship", expanded=True):
            st.markdown("""
            **What this graph shows us:**
            This scatter plot examines the relationship between health service coverage and birth volume (2022 projected births). 
            It reveals whether countries with higher birth volumes tend to have better or worse health service coverage, 
            which is critical for understanding global health equity. Countries in the bottom-right quadrant (high births, 
            low coverage) represent the greatest policy concern as they have the highest burden of need.
            """)
            
            fig = px.scatter(
                anc4_sba_df,
                x='births_2022',
                y='coverage_value',
                color='indicator_full_name',
                size='coverage_value',
                hover_data=['country_name', 'year', 'u5mr_status'],
                title="Coverage vs Births by Indicator",
                labels={
                    'births_2022': 'Births (2022)',
                    'coverage_value': 'Coverage (%)',
                    'indicator_full_name': 'Indicator'
                }
            )
            
            fig.update_layout(height=500)
            st.plotly_chart(fig, use_container_width=True)

def create_methodology_section():
    """Create methodology and results discussion section."""
    st.subheader("Methodology and Results Discussion")
    
    # Methodology Expander
    with st.expander("Methodology", expanded=True):
        st.markdown("""
        This analysis assessed global maternal health service coverage using a births-weighted approach to better reflect the distribution of need. Two core indicators were examined:
        
        **Antenatal Care (ANC4):** The percentage of women receiving at least four antenatal care visits.
        
        **Skilled Birth Attendance (SBA):** The percentage of births attended by skilled health personnel.
        
        **Data Sources** included the UNICEF Global Data Repository for service coverage estimates and the UN World Population Prospects 2022 for country-level projected births. For each country, the most recent estimate between 2018 and 2022 was used.
        
        To calculate more representative global averages, we applied the following weighting formula:
        
        ```
        Weighted Average = Σ (Coverage × Projected Births in 2022) / Σ (Projected Births in 2022)
        ```
        
        This method prioritizes countries with larger birth cohorts, aligning the analysis with where the greatest need for maternal health services exists. Countries were also grouped by Under-5 Mortality Rate (U5MR) status, classified as either "on-track" or "off-track" based on their likelihood of achieving child mortality targets. This enabled comparison of service coverage performance in relation to child survival outcomes.
        """)
    
    # Results Expander
    with st.expander("Results and Discussion", expanded=True):
        st.markdown("""
        ### 1. Births-Weighted vs Simple Average
        
        The births-weighted analysis reveals that global averages of maternal health coverage are significantly lower when accounting for where births are concentrated:
        
        **Antenatal Care (4+ visits):**
        - Births-weighted average: 67.7%
        - Simple average: 74.1%
        - → 6.5 percentage point gap
        
        **Skilled Birth Attendance:**
        - Births-weighted average: 82.3%
        - Simple average: 93.0%
        - → 10.7 percentage point gap
        
        This disparity indicates that countries with the highest number of births tend to have weaker service coverage, which highlights a critical equity concern in global health efforts.
        
        ### 2. Service Coverage by U5MR Status
        
        Coverage levels were substantially higher in countries classified as on-track to meet under-five mortality targets, compared to off-track countries:
        
        **ANC4 coverage:**
        - On-track: 89.7%
        - Off-track: 54.8%
        
        **SBA coverage:**
        - On-track: 96.7%
        - Off-track: 66.9%
        
        These findings reinforce the close relationship between maternal service coverage and child survival outcomes. Poor antenatal and delivery care coverage in off-track countries likely contributes to persistently high child mortality.
        
        ### 3. Distribution and Equity Gaps
        
        Boxplots illustrate the wide inequality in coverage across countries. Off-track countries show not only lower median coverage but also greater variation and outliers. Countries with high birth volumes and low coverage form a concerning cluster, as seen in the scatterplots, demonstrating that the greatest volume of births is often occurring in settings least equipped to provide adequate maternal care.
        
        ### 4. Data Availability and Indicator Behavior
        
        SBA coverage is generally higher and better reported (148 countries) than ANC4 (86 countries), possibly reflecting a system-level focus on delivery care over comprehensive antenatal care.
        
        Between 2018 and 2022, there was a decline in the number of countries reporting recent estimates, especially in 2021–2022, possibly due to disruptions in data collection during the COVID-19 pandemic.
        """)
    
    # Interpretation Expander
    with st.expander("Interpretation", expanded=True):
        st.markdown("""
        This analysis shows that traditional unweighted averages overestimate global progress by treating all countries equally, regardless of their birth burden. In contrast, births-weighted metrics highlight the service gaps in countries with the greatest need, offering a more policy-relevant picture.
        
        The strong alignment between low service coverage and off-track U5MR status suggests an urgent need for targeted investments in maternal health systems, particularly in high-fertility, low-coverage settings.
        
        **Key Policy Implications:**
        
        1. **Equity Focus:** Births-weighted analysis reveals critical gaps in countries with the highest birth volumes
        2. **Targeted Investment:** Off-track countries require urgent maternal health system strengthening
        3. **Data Gaps:** Improved reporting systems needed, especially for ANC4 coverage
        4. **Integrated Approach:** Maternal health and child survival programs should be coordinated
        
        **Caveats and Assumptions:**
        
        1. **Data Quality:** Analysis assumes UNICEF data represents the most recent available estimates per country-year. Missing data may affect coverage calculations for some countries.
        
        2. **Births Weighting:** Using projected births for 2022 as weights assumes birth rates are a reasonable proxy for maternal health service needs. This may not capture all relevant demographic factors.
        
        3. **U5MR Classification:** The on-track/off-track classification is based on 2022 status and may not reflect current progress or recent improvements in some countries.
        
        4. **Time Period:** Analysis covers 2018-2022 and uses the most recent estimate per country, which may not capture longer-term trends or recent policy changes affecting health service delivery.
        
        5. **Country Coverage:** Results depend on data availability from UNICEF and may not include all countries due to reporting gaps or data quality issues.
        
        6. **Indicator Definitions:** Coverage estimates are based on UNICEF's standardized definitions, which may vary slightly from national reporting standards in some countries.
        """)

def main():
    """Main Streamlit application."""
    create_header()
    
    # Load data
    results, df = load_analysis_data()
    
    if results is None or df is None:
        st.error("❌ Unable to load analysis data. Please ensure the analysis has been run.")
        return
    
    # Create tabs for different sections
    tab1, tab2, tab3, tab4, tab5 = st.tabs([
        "Overview", 
        "ANC4 & SBA Coverage (2018-2022)", 
        "Country Explorer", 
        "Weighting Comparison", 
        "Methodology and Results"
    ])
    
    with tab1:
        display_overview_metrics(results)
        st.markdown("---")
        
        # Coverage Comparison Chart in Dropdown
        chart_option = st.selectbox(
            "Select Chart to View:",
            ["Key Metrics", "Coverage Comparison by U5MR Status"],
            key="overview_chart_selector"
        )
        
        if chart_option == "Coverage Comparison by U5MR Status":
            st.markdown("""
            **What this graph shows us:**
            This bar chart compares health service coverage between countries classified as "On Track" versus "Off Track" 
            for achieving their under-five mortality targets. It reveals significant disparities in maternal health 
            service coverage, with on-track countries consistently showing higher coverage rates for both Antenatal Care 
            and Skilled Birth Attendance. This visualization highlights the critical relationship between health system 
            performance and child survival outcomes.
            """)
            create_coverage_comparison_chart(results, "overview_coverage_comparison")
        else:
            # Display key metrics (default view)
            st.markdown("### Key Metrics Summary")
            st.markdown("""
            The key metrics above show the births-weighted averages for maternal health service coverage globally.
            These metrics provide a more accurate representation of global health service coverage by weighting 
            countries based on their birth volumes rather than treating all countries equally.
            """)
        
        st.markdown("---")
        
        # Callout note on how to use filters
        st.markdown("""
        <div style="background-color: #f0f8ff; border-left: 4px solid #1f77b4; padding: 1rem; margin: 1rem 0; border-radius: 0.5rem;">
        <h4 style="margin-top: 0; color: #1f77b4;">How to Use the Filters</h4>
        <p><strong>U5MR Status Filter:</strong> Select "on_track" or "off_track" to compare coverage between countries achieving their under-five mortality targets versus those needing acceleration.</p>
        <p><strong>Indicator Filter:</strong> Choose "Antenatal Care (4+ visits)" or "Skilled Birth Attendance" to focus on specific health services.</p>
        <p><strong>Year Range Slider:</strong> Adjust to explore data from 2018-2022. Note: The analysis uses the most recent estimate per country within this range.</p>
        <p><strong>Tip:</strong> Use the Country Explorer tab with these filters to see how coverage varies by country size (births) and indicator type.</p>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("""
        **About this Dashboard:**
        
        This interactive dashboard provides an enhanced view of the UNICEF Health Services Coverage Analysis. 
        Use the sidebar filters to explore the data dynamically and gain deeper insights into health service 
        coverage patterns across different countries and time periods.
        """)
    
    with tab2:
        # Coverage Summary Table at the beginning
        st.markdown("### Coverage Summary by Indicator")
        
        # Filter for ANC4 and SBA indicators
        anc4_sba_df = df[df['indicator_full_name'].isin(['Antenatal Care (4+ visits)', 'Skilled Birth Attendance'])].copy()
        
        # Create summary table
        summary_data = []
        for indicator in anc4_sba_df['indicator_full_name'].unique():
            indicator_data = anc4_sba_df[anc4_sba_df['indicator_full_name'] == indicator]
            summary_data.append({
                'Indicator': indicator,
                'Average Coverage (%)': f"{indicator_data['coverage_value'].mean():.1f}",
                'Median Coverage (%)': f"{indicator_data['coverage_value'].median():.1f}",
                'Countries with Data': indicator_data['country_name'].nunique(),
                'Coverage Range (%)': f"{indicator_data['coverage_value'].min():.1f} - {indicator_data['coverage_value'].max():.1f}",
                'On-track Average (%)': f"{indicator_data[indicator_data['u5mr_status'] == 'on_track']['coverage_value'].mean():.1f}",
                'Off-track Average (%)': f"{indicator_data[indicator_data['u5mr_status'] == 'off_track']['coverage_value'].mean():.1f}"
            })
        
        summary_df = pd.DataFrame(summary_data)
        st.dataframe(summary_df, use_container_width=True)
        
        st.markdown("---")
        
        # Coverage Comparison Chart
        with st.expander("Coverage Comparison by U5MR Status", expanded=True):
            st.markdown("""
            **What this graph shows us:**
            This bar chart compares health service coverage between countries classified as "On Track" versus "Off Track" 
            for achieving their under-five mortality targets. It reveals significant disparities in maternal health 
            service coverage, with on-track countries consistently showing higher coverage rates for both Antenatal Care 
            and Skilled Birth Attendance. This visualization highlights the critical relationship between health system 
            performance and child survival outcomes.
            """)
            create_coverage_comparison_chart(results, "detailed_coverage_comparison")
        
        # Other analysis charts
        create_anc4_sba_coverage_analysis(df)
    
    with tab3:
        create_country_explorer(df)
    
    with tab4:
        create_weighted_vs_simple_chart(results)
    
    with tab5:
        create_methodology_section()

if __name__ == "__main__":
    main() 