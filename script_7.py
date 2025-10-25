
# Create Page 3: Financial Projections
page_financials = '''"""
Financial Projections Page - Revenue, profitability, and growth forecasts
"""
import streamlit as st
import pandas as pd
import sys
from pathlib import Path

sys.path.append(str(Path(__file__).parent.parent))

from utils.calculations import format_currency, format_percentage
from utils.visualizations import create_valuation_revenue_chart

st.set_page_config(page_title="Financial Projections", page_icon="📈", layout="wide")

# Load data
@st.cache_data
def load_data():
    data_path = Path(__file__).parent.parent / "data"
    financials = pd.read_csv(data_path / "financial_projections_2015_2030.csv")
    income_stmt = pd.read_csv(data_path / "income_statement.csv")
    key_metrics = pd.read_csv(data_path / "key_metrics.csv")
    return financials, income_stmt, key_metrics

financials, income_stmt, key_metrics = load_data()

# Header
st.title("📈 Financial Projections")
st.markdown("Historical performance and forward-looking forecasts through IPO")

st.markdown("---")

# Time period selector
st.sidebar.header("Filters")
view_mode = st.sidebar.radio(
    "Select View:",
    options=['Historical & Projected', 'Historical Only', 'Projected Only']
)

# Filter data based on selection
if view_mode == 'Historical Only':
    display_financials = financials[financials['Status'] == 'Historical']
elif view_mode == 'Projected Only':
    display_financials = financials[financials['Status'] == 'Projected']
else:
    display_financials = financials

# Key Financial Metrics Summary
st.header("Key Financial Metrics")

col1, col2, col3, col4 = st.columns(4)

latest_historical = financials[financials['Status'] == 'Historical'].iloc[-1]
latest_projected = financials[financials['Status'] == 'Projected'].iloc[-1]

with col1:
    st.metric(
        "2024 Revenue",
        format_currency(latest_historical['Revenue']),
        delta=format_percentage(
            ((latest_historical['Revenue'] / financials.iloc[0]['Revenue']) ** (1/9) - 1) * 100
        ) + " CAGR"
    )

with col2:
    st.metric(
        "2030 Revenue (Projected)",
        format_currency(latest_projected['Revenue']),
        delta=format_currency(latest_projected['Revenue'] - latest_historical['Revenue'])
    )

with col3:
    st.metric(
        "2024 Net Margin",
        format_percentage(latest_historical['Net_Margin_%']),
        delta=f"+{latest_historical['Net_Margin_%'] - financials.iloc[0]['Net_Margin_%']:.1f}pp since 2015"
    )

with col4:
    st.metric(
        "2030 Valuation",
        format_currency(latest_projected['Company_Valuation']),
        delta=format_multiple(latest_projected['Revenue_Multiple']) + " revenue multiple"
    )

# Valuation & Revenue Chart
st.markdown("---")
st.header("Valuation & Revenue Growth Trajectory")

st.plotly_chart(create_valuation_revenue_chart(financials), use_container_width=True)

# Growth Analysis
st.markdown("---")
st.header("Growth Analysis")

col1, col2 = st.columns(2)

with col1:
    st.subheader("Historical Performance (2015-2024)")
    
    historical_cagr = ((latest_historical['Revenue'] / financials.iloc[0]['Revenue']) ** (1/9) - 1) * 100
    
    st.markdown(f"""
    - **Revenue CAGR:** {historical_cagr:.1f}%
    - **Starting Revenue (2015):** {format_currency(financials.iloc[0]['Revenue'])}
    - **Ending Revenue (2024):** {format_currency(latest_historical['Revenue'])}
    - **Growth Factor:** {latest_historical['Revenue'] / financials.iloc[0]['Revenue']:.1f}x
    - **Net Margin Expansion:** {financials.iloc[0]['Net_Margin_%']:.1f}% → {latest_historical['Net_Margin_%']:.1f}%
    """)
    
    st.success("✅ Consistent 32%+ annual growth over 10 years")

with col2:
    st.subheader("Projected Performance (2024-2030)")
    
    projected_cagr = ((latest_projected['Revenue'] / latest_historical['Revenue']) ** (1/6) - 1) * 100
    
    st.markdown(f"""
    - **Revenue CAGR:** {projected_cagr:.1f}%
    - **Starting Revenue (2024):** {format_currency(latest_historical['Revenue'])}
    - **Ending Revenue (2030):** {format_currency(latest_projected['Revenue'])}
    - **Growth Factor:** {latest_projected['Revenue'] / latest_historical['Revenue']:.1f}x
    - **Net Margin Target:** {latest_projected['Net_Margin_%']:.1f}%
    """)
    
    st.info("📊 Conservative projections with continued margin expansion")

# Detailed Financial Table
st.markdown("---")
st.header("Detailed Financial Projections")

# Create displayable table
display_df = display_financials[['Year', 'Revenue', 'Net_Income', 'Net_Margin_%', 
                                  'Company_Valuation', 'Revenue_Multiple', 'Status']].copy()

display_df['Revenue'] = display_df['Revenue'].apply(lambda x: format_currency(x))
display_df['Net_Income'] = display_df['Net_Income'].apply(lambda x: format_currency(x))
display_df['Net_Margin_%'] = display_df['Net_Margin_%'].apply(lambda x: f"{x:.1f}%")
display_df['Company_Valuation'] = display_df['Company_Valuation'].apply(lambda x: format_currency(x))
display_df['Revenue_Multiple'] = display_df['Revenue_Multiple'].apply(lambda x: f"{x:.1f}x")

st.dataframe(display_df, use_container_width=True, hide_index=True)

# Margin Analysis
st.markdown("---")
st.header("Profitability Margins Evolution")

# Create margin chart
import plotly.graph_objects as go

margin_fig = go.Figure()

historical_income = income_stmt.copy()
historical_income['Year'] = range(2015, 2015 + len(historical_income))

margin_fig.add_trace(go.Scatter(
    x=historical_income['Year'],
    y=historical_income['Gross_Margin_%'],
    name='Gross Margin',
    line=dict(color='#00CC66', width=3),
    mode='lines+markers'
))

margin_fig.add_trace(go.Scatter(
    x=historical_income['Year'],
    y=historical_income['Operating_Margin_%'],
    name='Operating Margin',
    line=dict(color='#0066CC', width=3),
    mode='lines+markers'
))

margin_fig.add_trace(go.Scatter(
    x=historical_income['Year'],
    y=historical_income['Net_Margin_%'],
    name='Net Margin',
    line=dict(color='#CC0066', width=3),
    mode='lines+markers'
))

margin_fig.update_layout(
    title="Profitability Margins (2015-2024)",
    xaxis_title="Year",
    yaxis_title="Margin %",
    height=400,
    hovermode='x unified',
    legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1)
)

st.plotly_chart(margin_fig, use_container_width=True)

col1, col2, col3 = st.columns(3)

with col1:
    st.metric(
        "Gross Margin Improvement",
        f"+{historical_income.iloc[-1]['Gross_Margin_%'] - historical_income.iloc[0]['Gross_Margin_%']:.0f}pp",
        delta=f"{historical_income.iloc[0]['Gross_Margin_%']:.0f}% → {historical_income.iloc[-1]['Gross_Margin_%']:.0f}%"
    )

with col2:
    st.metric(
        "Operating Margin Improvement",
        f"+{historical_income.iloc[-1]['Operating_Margin_%'] - historical_income.iloc[0]['Operating_Margin_%']:.0f}pp",
        delta=f"{historical_income.iloc[0]['Operating_Margin_%']:.0f}% → {historical_income.iloc[-1]['Operating_Margin_%']:.0f}%"
    )

with col3:
    st.metric(
        "Net Margin Improvement",
        f"+{historical_income.iloc[-1]['Net_Margin_%'] - historical_income.iloc[0]['Net_Margin_%']:.1f}pp",
        delta=f"{historical_income.iloc[0]['Net_Margin_%']:.1f}% → {historical_income.iloc[-1]['Net_Margin_%']:.1f}%"
    )

st.success("""
**Key Insight:** Consistent margin expansion demonstrates operational leverage and economies of scale. 
As the datacenter scales, fixed infrastructure costs are spread across growing revenue, driving profitability.
""")

# Helper for multiple formatting
def format_multiple(value):
    return f"{value:.1f}x"

# Footer
st.markdown("---")
st.caption("All financial projections are forward-looking statements subject to risks and uncertainties")
'''

with open(f'{base_dir}/pages/3_📈_Financial_Projections.py', 'w') as f:
    f.write(page_financials)

print("✓ Created pages/3_📈_Financial_Projections.py")
