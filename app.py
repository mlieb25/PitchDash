"""
AI Datacenter Vancouver - Investor Dashboard
Main entry point for the Streamlit application
"""
import streamlit as st
import pandas as pd
import sys
from pathlib import Path

# Add utils to path
current_dir = Path(__file__).parent
if str(current_dir) not in sys.path:
    sys.path.insert(0, str(current_dir))

from utils.calculations import format_currency, format_percentage, format_multiple
import plotly.graph_objects as go

# Page configuration
st.set_page_config(
    page_title="AI Datacenter Vancouver - Investor Dashboard",
    page_icon="🏢",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for better styling
st.markdown("""
<style>
    .main-header {
        font-size: 3rem;
        font-weight: bold;
        color: #0066CC;
        text-align: center;
        margin-bottom: 1rem;
    }
    .sub-header {
        font-size: 1.5rem;
        color: #666;
        text-align: center;
        margin-bottom: 2rem;
    }
    .metric-card {
        background-color: #F0F2F6;
        padding: 1.5rem;
        border-radius: 0.5rem;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
    }
    .highlight-box {
        background-color: #E6F2FF;
        padding: 1.5rem;
        border-left: 4px solid #0066CC;
        border-radius: 0.5rem;
        margin: 1rem 0;
    }
</style>
""", unsafe_allow_html=True)

# Load data
@st.cache_data
def load_data():
    data_path = Path(__file__).parent / "data"

    roi_summary = pd.read_csv(data_path / "investor_roi_summary.csv")
    financials = pd.read_csv(data_path / "financial_projections_2015_2030.csv")
    funding_rounds = pd.read_csv(data_path / "funding_rounds_overview.csv")

    return roi_summary, financials, funding_rounds

roi_summary, financials, funding_rounds = load_data()

# Header
st.markdown('<h1 class="main-header">🏢 AI Datacenter Vancouver</h1>', unsafe_allow_html=True)
st.markdown('<p class="sub-header">Interactive Investor Pitch Dashboard - Series B Opportunity</p>', unsafe_allow_html=True)

# Executive Summary
st.markdown("---")
st.header("Executive Summary")

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric(
        label="Series B Investment",
        value=format_currency(8000000),
        delta="Opening 2026"
    )

with col2:
    series_b_roi = roi_summary[roi_summary['Round'] == 'Series B'].iloc[0]
    st.metric(
        label="Projected MOIC",
        value=format_multiple(series_b_roi['MOIC']),
        delta=f"{series_b_roi['IRR_%']:.1f}% IRR"
    )

with col3:
    st.metric(
        label="Exit Valuation (IPO 2030)",
        value=format_currency(240000000),
        delta="4 year hold"
    )

with col4:
    st.metric(
        label="Historical Revenue CAGR",
        value="32.2%",
        delta="2015-2024"
    )

# Key Highlights
st.markdown("---")
st.header("Why Invest Now?")

col1, col2 = st.columns(2)

with col1:
    st.markdown("""
    <div class="highlight-box">
    <h3>🎯 Proven Track Record</h3>
    <ul>
        <li><strong>10 years</strong> of consistent growth</li>
        <li><strong>32.2% revenue CAGR</strong> (2015-2024)</li>
        <li><strong>Net margins improved</strong> from 6.7% to 23.8%</li>
        <li><strong>29 enterprise customers</strong> with high retention</li>
        <li><strong>World-class uptime:</strong> 99.96%</li>
    </ul>
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown("""
    <div class="highlight-box">
    <h3>💰 Superior Returns vs Later Rounds</h3>
    <ul>
        <li><strong>4.85x MOIC</strong> for Series B investors</li>
        <li><strong>48.4% IRR</strong> to IPO exit (4 years)</li>
        <li><strong>2.85x higher</strong> returns than Series C</li>
        <li><strong>Early exit option:</strong> 2.42x in just 2 years</li>
        <li><strong>$33M valuation</strong> vs $100M in Series C</li>
    </ul>
    </div>
    """, unsafe_allow_html=True)

# Company Overview
st.markdown("---")
st.header("Company Overview")

col1, col2, col3 = st.columns(3)

with col1:
    st.markdown("""
    **Founded:** 2015  
    **Location:** Vancouver, BC, Canada  
    **Industry:** AI Infrastructure / Datacenter Services  
    **Current Stage:** Preparing Series B (2026)
    """)

with col2:
    st.markdown("""
    **2024 Performance:**  
    - Revenue: $9.9M  
    - Net Income: $2.3M  
    - Gross Margin: 64%  
    - Operating Margin: 33%
    """)

with col3:
    st.markdown("""
    **Infrastructure:**  
    - 273 Servers  
    - 2,184 GPUs  
    - 20,753 sq ft  
    - 115 Employees
    """)

# Past Investor Success
st.markdown("---")
st.header("Past Investor Returns")

st.markdown("""
Our early investors have achieved exceptional returns, validating our business model and growth trajectory:
""")

col1, col2, col3 = st.columns(3)

seed_roi = roi_summary[roi_summary['Round'] == 'Seed'].iloc[0]
series_a_roi = roi_summary[roi_summary['Round'] == 'Series A'].iloc[0]

with col1:
    st.markdown(f"""
    <div class="metric-card">
    <h4>💎 Seed Investors (2015)</h4>
    <p style="font-size: 2rem; font-weight: bold; color: #0066CC;">{seed_roi['MOIC']:.1f}x</p>
    <p>Invested: {format_currency(seed_roi['Investment_Amount'])}</p>
    <p>Exit Value: {format_currency(seed_roi['Exit_Value_at_IPO'])}</p>
    <p>IRR: {seed_roi['IRR_%']:.1f}%</p>
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown(f"""
    <div class="metric-card">
    <h4>🚀 Series A Investors (2017)</h4>
    <p style="font-size: 2rem; font-weight: bold; color: #0066CC;">{series_a_roi['MOIC']:.1f}x</p>
    <p>Invested: {format_currency(series_a_roi['Investment_Amount'])}</p>
    <p>Exit Value: {format_currency(series_a_roi['Exit_Value_at_IPO'])}</p>
    <p>IRR: {series_a_roi['IRR_%']:.1f}%</p>
    </div>
    """, unsafe_allow_html=True)

with col3:
    st.markdown(f"""
    <div class="metric-card">
    <h4>⭐ Series B Opportunity (2026)</h4>
    <p style="font-size: 2rem; font-weight: bold; color: #CC0066;">{series_b_roi['MOIC']:.1f}x</p>
    <p>Investment: {format_currency(series_b_roi['Investment_Amount'])}</p>
    <p>Projected Exit: {format_currency(series_b_roi['Exit_Value_at_IPO'])}</p>
    <p>IRR: {series_b_roi['IRR_%']:.1f}%</p>
    </div>
    """, unsafe_allow_html=True)

# Navigation Guide
st.markdown("---")
st.header("📱 Navigate the Dashboard")

st.info("""
Use the sidebar to explore different sections:
- **📊 Overview**: Key metrics and company highlights (you are here)
- **💰 ROI Analysis**: Deep dive into investor returns by round
- **📈 Financial Projections**: Revenue, profitability, and growth forecasts
- **🎯 Investment Scenarios**: Interactive calculator to model your investment
- **📑 Company Details**: Operational metrics and business fundamentals
""")

# Footer
st.markdown("---")
st.caption("AI Datacenter Vancouver | Confidential Investor Materials | 2025")
