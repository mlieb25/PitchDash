
# Create Page 1: Overview (this completes the dashboard)
page_overview = '''"""
Overview Page - Executive summary and key highlights
"""
import streamlit as st
import pandas as pd
import sys
from pathlib import Path

sys.path.append(str(Path(__file__).parent.parent))

from utils.calculations import format_currency, format_percentage, format_multiple

st.set_page_config(page_title="Dashboard Overview", page_icon="📊", layout="wide")

# Load data
@st.cache_data
def load_data():
    data_path = Path(__file__).parent.parent / "data"
    roi_summary = pd.read_csv(data_path / "investor_roi_summary.csv")
    financials = pd.read_csv(data_path / "financial_projections_2015_2030.csv")
    operational = pd.read_csv(data_path / "operational_metrics.csv")
    return roi_summary, financials, operational

roi_summary, financials, operational = load_data()

# Header
st.title("📊 Dashboard Overview")
st.markdown("### AI Datacenter Vancouver - Series B Investment Opportunity")

st.markdown("---")

# Top-level metrics
st.header("Investment Opportunity at a Glance")

col1, col2, col3, col4, col5 = st.columns(5)

series_b = roi_summary[roi_summary['Round'] == 'Series B'].iloc[0]

with col1:
    st.metric(
        "Series B Round",
        format_currency(8000000),
        delta="Q2 2026"
    )

with col2:
    st.metric(
        "Valuation",
        format_currency(33000000),
        delta="Post-money"
    )

with col3:
    st.metric(
        "Projected MOIC",
        format_multiple(series_b['MOIC']),
        delta="at IPO (2030)"
    )

with col4:
    st.metric(
        "Projected IRR",
        format_percentage(series_b['IRR_%']),
        delta="4-year hold"
    )

with col5:
    st.metric(
        "Equity Offered",
        "24.24%",
        delta="of company"
    )

# Investment Thesis
st.markdown("---")
st.header("Investment Thesis")

col1, col2 = st.columns([2, 1])

with col1:
    st.markdown("""
    ### Why Invest in AI Datacenter Vancouver?
    
    **1. Proven Execution & Track Record**
    - 10 years of consistent growth (2015-2024)
    - 32.2% revenue CAGR with improving margins
    - Net margins expanded from 6.7% to 23.8%
    - World-class operational metrics (99.96% uptime, 1.26 PUE)
    
    **2. Superior Returns vs Later Rounds**
    - Series B: 4.85x MOIC vs Series C: 2.00x MOIC
    - 48.4% IRR significantly above VC benchmarks
    - 67% lower entry valuation than Series C
    - Early exit option at Series C for 2.42x in 2 years
    
    **3. Strong Market Tailwinds**
    - Explosive AI/ML compute demand
    - GPU shortage driving premium pricing
    - Enterprise customers with mission-critical workloads
    - Vancouver's clean energy advantage
    
    **4. Clear Path to Exit**
    - Series C planned for 2028 ($100M valuation)
    - IPO targeted for 2030 ($240M valuation)
    - Historical investor returns validate projections
    - Multiple strategic acquirers in market
    """)

with col2:
    st.markdown("""
    ### Key Risks
    
    **Market Risks:**
    - Competition from hyperscalers
    - Technology obsolescence
    - Regulatory changes
    
    **Operational Risks:**
    - Power cost volatility
    - Customer concentration
    - Talent retention
    
    **Financial Risks:**
    - CapEx requirements
    - Dilution in future rounds
    - Exit valuation uncertainty
    
    ---
    
    ### Mitigants
    
    ✅ Diversified customer base (29 clients)  
    ✅ Long-term contracts with uptime SLAs  
    ✅ Best-in-class operational efficiency  
    ✅ Strong balance sheet & cash flow  
    ✅ Experienced management team  
    """)

# Comparison: Series B vs Series C
st.markdown("---")
st.header("🎯 Why Invest Now vs Waiting for Series C?")

series_c = roi_summary[roi_summary['Round'] == 'Series C'].iloc[0]

comparison_metrics = pd.DataFrame({
    'Metric': [
        'Investment Timing',
        'Entry Valuation',
        'Minimum Check Size',
        'Ownership % (for $8M)',
        'MOIC at IPO',
        'IRR',
        'Holding Period',
        'Early Exit Option',
        'Entry Price Advantage'
    ],
    'Series B (Now)': [
        '2026',
        format_currency(series_b['Entry_Valuation']),
        format_currency(500000),
        f"{(8000000/33000000)*100:.2f}%",
        format_multiple(series_b['MOIC']),
        format_percentage(series_b['IRR_%']),
        '4 years to IPO',
        'Yes - 2.42x in 2 years',
        '67% lower valuation'
    ],
    'Series C (Later)': [
        '2028',
        format_currency(series_c['Entry_Valuation']),
        format_currency(1000000),
        f"{(8000000/100000000)*100:.2f}%",
        format_multiple(series_c['MOIC']),
        format_percentage(series_c['IRR_%']),
        '2 years to IPO',
        'No - must hold to IPO',
        'Baseline'
    ]
})

st.dataframe(comparison_metrics, use_container_width=True, hide_index=True)

st.success(f"""
**Bottom Line:** Investing in Series B delivers **{series_b['MOIC']:.2f}x returns** compared to 
{series_c['MOIC']:.2f}x for Series C — a **{((series_b['MOIC']/series_c['MOIC'] - 1)*100):.0f}% higher multiple** 
by entering 2 years earlier at a 67% lower valuation.
""")

# Historical Performance
st.markdown("---")
st.header("Historical Performance Validates Projections")

col1, col2, col3, col4 = st.columns(4)

latest_financial = financials[financials['Status'] == 'Historical'].iloc[-1]
first_financial = financials[financials['Status'] == 'Historical'].iloc[0]

with col1:
    revenue_growth = ((latest_financial['Revenue'] / first_financial['Revenue']) ** (1/9) - 1) * 100
    st.metric(
        "Revenue CAGR",
        format_percentage(revenue_growth),
        delta="2015-2024"
    )

with col2:
    st.metric(
        "2024 Revenue",
        format_currency(latest_financial['Revenue']),
        delta=f"{latest_financial['Revenue'] / first_financial['Revenue']:.1f}x growth"
    )

with col3:
    margin_improvement = latest_financial['Net_Margin_%'] - first_financial['Net_Margin_%']
    st.metric(
        "Net Margin Expansion",
        f"+{margin_improvement:.1f}pp",
        delta=f"{first_financial['Net_Margin_%']:.1f}% → {latest_financial['Net_Margin_%']:.1f}%"
    )

with col4:
    latest_ops = operational.iloc[-1]
    st.metric(
        "Customer Growth",
        f"{latest_ops['Number_of_Customers']} clients",
        delta=f"+{latest_ops['Number_of_Customers'] - operational.iloc[0]['Number_of_Customers']} from 2015"
    )

# Past Investor Success Stories
st.markdown("---")
st.header("💎 Past Investor Success Stories")

st.markdown("""
Our early investors have achieved exceptional returns, demonstrating the company's ability to create value:
""")

col1, col2, col3 = st.columns(3)

seed = roi_summary[roi_summary['Round'] == 'Seed'].iloc[0]
series_a = roi_summary[roi_summary['Round'] == 'Series A'].iloc[0]

with col1:
    st.markdown(f"""
    ### Seed Investors (2015)
    
    **Invested:** {format_currency(seed['Investment_Amount'])}  
    **Valuation:** {format_currency(seed['Entry_Valuation'])}  
    
    **Returns at IPO:**  
    🎯 **{format_multiple(seed['MOIC'])}** return multiple  
    📈 **{format_percentage(seed['IRR_%'])}** annualized IRR  
    💰 **{format_currency(seed['Exit_Value_at_IPO'])}** exit value  
    
    ⏱️ 15-year holding period
    """)

with col2:
    st.markdown(f"""
    ### Series A Investors (2017)
    
    **Invested:** {format_currency(series_a['Investment_Amount'])}  
    **Valuation:** {format_currency(series_a['Entry_Valuation'])}  
    
    **Returns at IPO:**  
    🎯 **{format_multiple(series_a['MOIC'])}** return multiple  
    📈 **{format_percentage(series_a['IRR_%'])}** annualized IRR  
    💰 **{format_currency(series_a['Exit_Value_at_IPO'])}** exit value  
    
    ⏱️ 13-year holding period
    """)

with col3:
    st.markdown(f"""
    ### Series B (You!)
    
    **Investment:** {format_currency(series_b['Investment_Amount'])}  
    **Valuation:** {format_currency(series_b['Entry_Valuation'])}  
    
    **Projected Returns:**  
    🎯 **{format_multiple(series_b['MOIC'])}** return multiple  
    📈 **{format_percentage(series_b['IRR_%'])}** annualized IRR  
    💰 **{format_currency(series_b['Exit_Value_at_IPO'])}** exit value  
    
    ⏱️ 4-year holding period
    """)

# Next Steps
st.markdown("---")
st.header("📋 Next Steps")

col1, col2 = st.columns(2)

with col1:
    st.markdown("""
    ### For Investors
    
    1. **Review** all sections of this interactive dashboard
    2. **Model** your investment using the Scenarios page
    3. **Analyze** financial projections and company details
    4. **Schedule** management presentation and Q&A
    5. **Conduct** due diligence review
    6. **Commit** to Series B participation
    
    **Key Dates:**
    - Series B Opening: Q2 2026
    - Series B Closing: Q3 2026
    - Series C (optional exit): Q1 2028
    - Target IPO: Q3 2030
    """)

with col2:
    st.markdown("""
    ### Contact Information
    
    **Company:**  
    AI Datacenter Vancouver  
    [Address]  
    Vancouver, BC, Canada  
    
    **Investor Relations:**  
    Email: investors@aidcvancouver.com  
    Phone: +1 (604) XXX-XXXX  
    
    **Lead Investor Contact:**  
    [Name], Managing Partner  
    [VC Firm]  
    
    **Data Room Access:**  
    [Secure Link]
    """)

st.info("""
💡 **Tip:** Use the sidebar to navigate between different sections of this dashboard. 
Try the Investment Scenarios page to model your custom investment amount and explore different return scenarios.
""")

# Footer
st.markdown("---")
st.caption("""
This dashboard contains forward-looking statements that are subject to risks and uncertainties. 
Actual results may differ materially. For complete disclaimers, see the Private Placement Memorandum.  
AI Datacenter Vancouver | Confidential Investor Materials | 2025
""")
'''

with open(f'{base_dir}/pages/1_📊_Overview.py', 'w') as f:
    f.write(page_overview)

print("✓ Created pages/1_📊_Overview.py")
