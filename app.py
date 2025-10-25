"""
AI Datacenter Vancouver - Investor Dashboard
Main entry point for the Streamlit application
"""
import streamlit as st
import pandas as pd
from pathlib import Path
import plotly.graph_objects as go

# Page configuration - MUST be first Streamlit command
st.set_page_config(
    page_title="AI Datacenter Vancouver - Investor Dashboard",
    page_icon="🏢",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ============================================================================
# HELPER FUNCTIONS
# ============================================================================

def format_currency(value, decimals=0):
    """Format value as currency"""
    if abs(value) >= 1_000_000:
        return f"${value/1_000_000:.{decimals}f}M"
    elif abs(value) >= 1_000:
        return f"${value/1_000:.{decimals}f}K"
    else:
        return f"${value:,.{decimals}f}"

def format_percentage(value, decimals=1):
    """Format value as percentage"""
    return f"{value:.{decimals}f}%"

def format_multiple(value, decimals=2):
    """Format value as multiple (e.g., 4.5x)"""
    return f"{value:.{decimals}f}x"

# ============================================================================
# CUSTOM CSS - COMPACT LAYOUT
# ============================================================================

st.markdown("""
<style>
    /* Reduce padding */
    .block-container {
        padding-top: 2rem;
        padding-bottom: 1rem;
        max-width: 100%;
    }

    /* Compact headers */
    h1 {
        margin-bottom: 0.5rem;
    }
    h2 {
        margin-top: 1rem;
        margin-bottom: 0.5rem;
        font-size: 1.5rem;
    }
    h3 {
        font-size: 1.2rem;
    }

    /* Header styling */
    .main-header {
        font-size: 2.5rem;
        font-weight: bold;
        color: #0066CC;
        text-align: center;
        margin-bottom: 0.5rem;
    }
    .sub-header {
        font-size: 1.2rem;
        color: #666;
        text-align: center;
        margin-bottom: 1rem;
    }

    /* Compact metric cards */
    .metric-card {
        background-color: #F0F2F6;
        padding: 1rem;
        border-radius: 0.5rem;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        height: 100%;
    }

    /* Compact highlight boxes */
    .highlight-box {
        background-color: #E6F2FF;
        padding: 1rem;
        border-left: 4px solid #0066CC;
        border-radius: 0.5rem;
        margin: 0.5rem 0;
    }
    .highlight-box h3 {
        margin-top: 0;
        margin-bottom: 0.5rem;
    }
    .highlight-box ul {
        margin-bottom: 0;
        padding-left: 1.5rem;
    }
    .highlight-box li {
        margin-bottom: 0.3rem;
    }

    /* Reduce spacing between sections */
    hr {
        margin: 1rem 0;
    }

    /* Make sidebar more prominent */
    [data-testid="stSidebar"] {
        background-color: #f8f9fa;
    }
</style>
""", unsafe_allow_html=True)

# ============================================================================
# DATA LOADING
# ============================================================================

@st.cache_data
def load_data():
    """Load all CSV data files"""
    try:
        data_path = Path(__file__).parent / "data"

        roi_summary = pd.read_csv(data_path / "investor_roi_summary.csv")
        financials = pd.read_csv(data_path / "financial_projections_2015_2030.csv")
        funding_rounds = pd.read_csv(data_path / "funding_rounds_overview.csv")

        return roi_summary, financials, funding_rounds
    except FileNotFoundError as e:
        st.error(f"⚠️ Data file not found: {e}")
        st.info("Please ensure all CSV files are in the 'data' directory.")
        st.stop()
    except Exception as e:
        st.error(f"⚠️ Error loading data: {e}")
        st.stop()

# Load data
roi_summary, financials, funding_rounds = load_data()

# ============================================================================
# SIDEBAR - NAVIGATION & FILTERS
# ============================================================================

with st.sidebar:
    st.markdown("## 🏢 AI DC Vancouver")

    st.markdown("### 📊 Dashboard")

    st.info("""
    **Quick Nav:**
    - Executive Summary
    - Investment Highlights
    - Historical Performance
    - ROI Comparison
    """)

    st.markdown("---")

    st.markdown("### 🎯 Key Metrics")
    st.metric("Series B MOIC", "4.85x")
    st.metric("Series B IRR", "48.4%")
    st.metric("Entry Valuation", "$33M")

    st.markdown("---")

    st.markdown("### 📞 Contact")
    st.markdown("""
    **Investor Relations**  
    investors@aidcvancouver.com  
    +1 (604) XXX-XXXX
    """)

    st.markdown("---")
    st.caption("© 2025 AI Datacenter Vancouver")

# ============================================================================
# HEADER
# ============================================================================

st.markdown('<h1 class="main-header">🏢 AI Datacenter Vancouver</h1>', unsafe_allow_html=True)
st.markdown('<p class="sub-header">Interactive Investor Pitch Dashboard - Series B Opportunity</p>', unsafe_allow_html=True)

# ============================================================================
# EXECUTIVE SUMMARY - COMPACT
# ============================================================================

st.header("Executive Summary")

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric("Series B Investment", format_currency(8000000), "Q2 2026")

with col2:
    series_b_roi = roi_summary[roi_summary['Round'] == 'Series B'].iloc[0]
    st.metric("Projected MOIC", format_multiple(series_b_roi['MOIC']), f"{series_b_roi['IRR_%']:.1f}% IRR")

with col3:
    st.metric("Exit Valuation", format_currency(240000000), "IPO 2030")

with col4:
    st.metric("Revenue CAGR", "32.2%", "2015-2024")

# ============================================================================
# KEY HIGHLIGHTS - SIDE BY SIDE
# ============================================================================

st.markdown("---")
st.subheader("Why Invest Now?")

col1, col2 = st.columns(2)

with col1:
    st.markdown("""
    <div class="highlight-box">
    <h3>🎯 Proven Track Record</h3>
    <ul>
        <li><strong>10 years</strong> consistent growth</li>
        <li><strong>32.2% CAGR</strong> (2015-2024)</li>
        <li><strong>Net margins:</strong> 6.7% → 23.8%</li>
        <li><strong>29 customers</strong>, 99.96% uptime</li>
    </ul>
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown("""
    <div class="highlight-box">
    <h3>💰 Superior Returns</h3>
    <ul>
        <li><strong>4.85x MOIC</strong> for Series B</li>
        <li><strong>48.4% IRR</strong> to IPO (4 years)</li>
        <li><strong>2.85x higher</strong> than Series C</li>
        <li><strong>Early exit:</strong> 2.42x in 2 years</li>
    </ul>
    </div>
    """, unsafe_allow_html=True)

# ============================================================================
# INVESTMENT COMPARISON - COMPACT TABLE
# ============================================================================

st.markdown("---")
st.subheader("Series B vs Series C Comparison")

comparison_df = pd.DataFrame({
    'Metric': ['Investment', 'Entry Valuation', 'MOIC', 'IRR', 'Hold Period'],
    'Series B (2026)': [
        format_currency(8000000),
        format_currency(33000000),
        '4.85x',
        '48.4%',
        '4 years'
    ],
    'Series C (2028)': [
        format_currency(20000000),
        format_currency(100000000),
        '2.00x',
        '41.4%',
        '2 years'
    ],
    'Series B Advantage': [
        '60% less capital',
        '67% lower',
        '2.85x higher',
        '+7.0%',
        'More time to exit'
    ]
})

st.dataframe(comparison_df, use_container_width=True, hide_index=True)

# ============================================================================
# PAST INVESTOR RETURNS - COMPACT
# ============================================================================

st.markdown("---")
st.subheader("Past Investor Returns")

col1, col2, col3 = st.columns(3)

seed_roi = roi_summary[roi_summary['Round'] == 'Seed'].iloc[0]
series_a_roi = roi_summary[roi_summary['Round'] == 'Series A'].iloc[0]

with col1:
    st.markdown(f"""
    <div class="metric-card">
    <h4>💎 Seed (2015)</h4>
    <p style="font-size: 1.8rem; font-weight: bold; color: #0066CC; margin: 0.5rem 0;">{seed_roi['MOIC']:.1f}x</p>
    <p style="margin: 0.2rem 0;"><small>Invested: {format_currency(seed_roi['Investment_Amount'])}</small></p>
    <p style="margin: 0.2rem 0;"><small>Exit: {format_currency(seed_roi['Exit_Value_at_IPO'])}</small></p>
    <p style="margin: 0.2rem 0;"><small>IRR: {seed_roi['IRR_%']:.1f}%</small></p>
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown(f"""
    <div class="metric-card">
    <h4>🚀 Series A (2017)</h4>
    <p style="font-size: 1.8rem; font-weight: bold; color: #0066CC; margin: 0.5rem 0;">{series_a_roi['MOIC']:.1f}x</p>
    <p style="margin: 0.2rem 0;"><small>Invested: {format_currency(series_a_roi['Investment_Amount'])}</small></p>
    <p style="margin: 0.2rem 0;"><small>Exit: {format_currency(series_a_roi['Exit_Value_at_IPO'])}</small></p>
    <p style="margin: 0.2rem 0;"><small>IRR: {series_a_roi['IRR_%']:.1f}%</small></p>
    </div>
    """, unsafe_allow_html=True)

with col3:
    st.markdown(f"""
    <div class="metric-card">
    <h4>⭐ Series B (You!)</h4>
    <p style="font-size: 1.8rem; font-weight: bold; color: #CC0066; margin: 0.5rem 0;">{series_b_roi['MOIC']:.1f}x</p>
    <p style="margin: 0.2rem 0;"><small>Investment: {format_currency(series_b_roi['Investment_Amount'])}</small></p>
    <p style="margin: 0.2rem 0;"><small>Projected Exit: {format_currency(series_b_roi['Exit_Value_at_IPO'])}</small></p>
    <p style="margin: 0.2rem 0;"><small>IRR: {series_b_roi['IRR_%']:.1f}%</small></p>
    </div>
    """, unsafe_allow_html=True)

# ============================================================================
# COMPANY SNAPSHOT - COMPACT
# ============================================================================

st.markdown("---")
st.subheader("Company Snapshot (2024)")

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric("Revenue", "$9.9M", "+24% YoY")
with col2:
    st.metric("Net Margin", "23.8%", "+2.3pp")
with col3:
    st.metric("Customers", "29", "+3 YoY")
with col4:
    st.metric("Servers", "273", "2,184 GPUs")

# ============================================================================
# CALL TO ACTION
# ============================================================================

st.markdown("---")

st.success("""
### 🎯 Ready to Invest?

**Series B Round Details:**
- **Amount:** $8M at $33M post-money valuation
- **Opening:** Q2 2026
- **Minimum Check:** $500K

**Next Steps:**
1. Review full financial projections (data room access)
2. Schedule management presentation
3. Conduct due diligence
4. Submit term sheet

**Contact:** investors@aidcvancouver.com
""")

# ============================================================================
# FOOTER
# ============================================================================

st.markdown("---")
st.caption("AI Datacenter Vancouver | Confidential Investor Materials | 2025 | This dashboard contains forward-looking statements subject to risks and uncertainties.")
