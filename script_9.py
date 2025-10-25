
# Create Page 5: Company Details
page_company = '''"""
Company Details Page - Operational metrics and business fundamentals
"""
import streamlit as st
import pandas as pd
import sys
from pathlib import Path

sys.path.append(str(Path(__file__).parent.parent))

from utils.calculations import format_currency, format_percentage
from utils.visualizations import create_ownership_chart
import plotly.graph_objects as go

st.set_page_config(page_title="Company Details", page_icon="📑", layout="wide")

# Load data
@st.cache_data
def load_data():
    data_path = Path(__file__).parent.parent / "data"
    operational = pd.read_csv(data_path / "operational_metrics.csv")
    ownership = pd.read_csv(data_path / "ownership_evolution.csv")
    balance_sheet = pd.read_csv(data_path / "balance_sheet.csv")
    income_stmt = pd.read_csv(data_path / "income_statement.csv")
    return operational, ownership, balance_sheet, income_stmt

operational, ownership, balance_sheet, income_stmt = load_data()

# Header
st.title("📑 Company Details")
st.markdown("Operational metrics, business fundamentals, and ownership structure")

st.markdown("---")

# Company Overview
st.header("Company Overview")

col1, col2 = st.columns(2)

with col1:
    st.subheader("Basic Information")
    st.markdown("""
    **Company Name:** AI Datacenter Vancouver  
    **Legal Structure:** Corporation  
    **Founded:** 2015  
    **Location:** Vancouver, British Columbia, Canada  
    **Industry:** AI Infrastructure / Datacenter Services  
    
    **Business Model:**  
    Providing high-performance GPU compute infrastructure for AI/ML workloads,
    serving enterprise customers with mission-critical AI applications.
    """)

with col2:
    st.subheader("2024 Snapshot")
    latest_ops = operational.iloc[-1]
    
    st.markdown(f"""
    **Infrastructure:**
    - Servers: {latest_ops['Server_Count']}
    - GPUs: {latest_ops['GPU_Count']}
    - Datacenter Space: {latest_ops['Datacenter_Space_SqFt']:,.0f} sq ft
    - Power Capacity: {latest_ops['Power_Capacity_kW']:,.0f} kW
    
    **Business Metrics:**
    - Customers: {latest_ops['Number_of_Customers']}
    - Employees: {latest_ops['Employee_Count']}
    - Uptime: {latest_ops['Uptime_%']}%
    - PUE: {latest_ops['Power_Usage_Effectiveness_PUE']}
    """)

# Operational Growth
st.markdown("---")
st.header("Operational Growth (2015-2024)")

# Create operational growth charts
fig_ops = go.Figure()

fig_ops.add_trace(go.Scatter(
    x=operational['Year'],
    y=operational['Server_Count'],
    name='Servers',
    line=dict(color='#0066CC', width=3),
    mode='lines+markers'
))

fig_ops.add_trace(go.Scatter(
    x=operational['Year'],
    y=operational['Number_of_Customers'],
    name='Customers',
    line=dict(color='#00CC66', width=3),
    mode='lines+markers',
    yaxis='y2'
))

fig_ops.update_layout(
    title="Server Count & Customer Growth",
    xaxis_title="Year",
    yaxis_title="Number of Servers",
    yaxis2=dict(
        title="Number of Customers",
        overlaying='y',
        side='right'
    ),
    height=400,
    hovermode='x unified',
    legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1)
)

st.plotly_chart(fig_ops, use_container_width=True)

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric(
        "Server Growth",
        f"{operational.iloc[-1]['Server_Count']} units",
        delta=f"{((operational.iloc[-1]['Server_Count'] / operational.iloc[0]['Server_Count']) - 1) * 100:.0f}% from 2015"
    )

with col2:
    st.metric(
        "Customer Growth",
        f"{operational.iloc[-1]['Number_of_Customers']} clients",
        delta=f"+{operational.iloc[-1]['Number_of_Customers'] - operational.iloc[0]['Number_of_Customers']} from 2015"
    )

with col3:
    st.metric(
        "GPU Capacity",
        f"{operational.iloc[-1]['GPU_Count']} GPUs",
        delta=f"{((operational.iloc[-1]['GPU_Count'] / operational.iloc[0]['GPU_Count']) - 1) * 100:.0f}% growth"
    )

with col4:
    st.metric(
        "Employee Count",
        f"{operational.iloc[-1]['Employee_Count']} people",
        delta=f"+{operational.iloc[-1]['Employee_Count'] - operational.iloc[0]['Employee_Count']} since 2015"
    )

# Key Performance Indicators
st.markdown("---")
st.header("Key Performance Indicators")

col1, col2 = st.columns(2)

with col1:
    st.subheader("Operational Excellence")
    
    # Uptime trend
    fig_uptime = go.Figure()
    fig_uptime.add_trace(go.Scatter(
        x=operational['Year'],
        y=operational['Uptime_%'],
        mode='lines+markers',
        line=dict(color='#00CC66', width=3),
        fill='tozeroy',
        fillcolor='rgba(0, 204, 102, 0.2)'
    ))
    
    fig_uptime.update_layout(
        title="Uptime Performance",
        xaxis_title="Year",
        yaxis_title="Uptime %",
        height=300,
        yaxis=dict(range=[99, 100])
    )
    
    st.plotly_chart(fig_uptime, use_container_width=True)
    
    st.success(f"✅ World-class uptime: {operational.iloc[-1]['Uptime_%']}% in 2024")

with col2:
    st.subheader("Energy Efficiency")
    
    # PUE trend
    fig_pue = go.Figure()
    fig_pue.add_trace(go.Scatter(
        x=operational['Year'],
        y=operational['Power_Usage_Effectiveness_PUE'],
        mode='lines+markers',
        line=dict(color='#0066CC', width=3),
        fill='tozeroy',
        fillcolor='rgba(0, 102, 204, 0.2)'
    ))
    
    fig_pue.update_layout(
        title="Power Usage Effectiveness (PUE)",
        xaxis_title="Year",
        yaxis_title="PUE (lower is better)",
        height=300
    )
    
    st.plotly_chart(fig_pue, use_container_width=True)
    
    st.success(f"✅ Industry-leading PUE: {operational.iloc[-1]['Power_Usage_Effectiveness_PUE']} in 2024")

# Unit Economics
st.markdown("---")
st.header("Unit Economics")

col1, col2 = st.columns(2)

with col1:
    st.subheader("Average Revenue Per Customer (ARPC)")
    
    fig_arpc = go.Figure()
    fig_arpc.add_trace(go.Bar(
        x=operational['Year'],
        y=operational['Avg_Revenue_Per_Customer'],
        marker_color='#0066CC',
        text=[format_currency(x, 0) for x in operational['Avg_Revenue_Per_Customer']],
        textposition='outside'
    ))
    
    fig_arpc.update_layout(
        title="ARPC Growth Over Time",
        xaxis_title="Year",
        yaxis_title="ARPC ($)",
        height=350
    )
    
    st.plotly_chart(fig_arpc, use_container_width=True)

with col2:
    st.subheader("Revenue Per Employee")
    
    fig_rpe = go.Figure()
    fig_rpe.add_trace(go.Bar(
        x=operational['Year'],
        y=operational['Revenue_Per_Employee'],
        marker_color='#00CC66',
        text=[format_currency(x, 0) for x in operational['Revenue_Per_Employee']],
        textposition='outside'
    ))
    
    fig_rpe.update_layout(
        title="Revenue Per Employee",
        xaxis_title="Year",
        yaxis_title="Revenue/Employee ($)",
        height=350
    )
    
    st.plotly_chart(fig_rpe, use_container_width=True)

# Ownership Structure
st.markdown("---")
st.header("Ownership Structure & Cap Table")

st.plotly_chart(create_ownership_chart(ownership), use_container_width=True)

# Current cap table
st.subheader("Current Ownership (Post-Series A)")
current_ownership = ownership[ownership['Milestone'] == '2017_Post_Series_A'].iloc[0]

col1, col2, col3 = st.columns(3)

with col1:
    st.metric("Founders", f"{current_ownership['Founders']:.2f}%")

with col2:
    st.metric("Seed Investors", f"{current_ownership['Seed_Investors']:.2f}%")

with col3:
    st.metric("Series A Investors", f"{current_ownership['Series_A_Investors']:.2f}%")

# Financial Health
st.markdown("---")
st.header("Financial Health Indicators")

latest_bs = balance_sheet.iloc[-1]
latest_is = income_stmt.iloc[-1]

col1, col2, col3, col4 = st.columns(4)

with col1:
    current_ratio = latest_bs['Total_Current_Assets'] / latest_bs['Total_Current_Liabilities']
    st.metric(
        "Current Ratio",
        f"{current_ratio:.2f}",
        delta="Strong liquidity" if current_ratio > 1.5 else "Adequate"
    )

with col2:
    debt_to_equity = latest_bs['Total_Liabilities'] / latest_bs['Total_Equity']
    st.metric(
        "Debt-to-Equity",
        f"{debt_to_equity:.2f}",
        delta="Healthy leverage" if debt_to_equity < 1 else "Moderate"
    )

with col3:
    st.metric(
        "Total Assets",
        format_currency(latest_bs['Total_Assets']),
        delta=f"+{((latest_bs['Total_Assets'] / balance_sheet.iloc[0]['Total_Assets']) - 1) * 100:.0f}% since 2015"
    )

with col4:
    st.metric(
        "Cash Position",
        format_currency(latest_bs['Cash_and_Equivalents']),
        delta=f"{(latest_bs['Cash_and_Equivalents'] / latest_bs['Total_Assets']) * 100:.1f}% of assets"
    )

# Competitive Advantages
st.markdown("---")
st.header("Competitive Advantages")

col1, col2 = st.columns(2)

with col1:
    st.markdown("""
    ### Technical Excellence
    - **99.96% uptime** - Industry-leading reliability
    - **1.26 PUE** - Among the most efficient datacenters globally
    - **2,184 GPUs** - Significant compute capacity for AI workloads
    - **10 years** of operational experience
    """)
    
    st.markdown("""
    ### Market Position
    - **Vancouver location** - Access to clean, affordable hydroelectric power
    - **29 enterprise customers** - Diverse, high-quality client base
    - **Strong unit economics** - $341K average revenue per customer
    - **Proven scalability** - 5x server growth over 10 years
    """)

with col2:
    st.markdown("""
    ### Financial Strength
    - **23.8% net margins** - Best-in-class profitability
    - **32.2% revenue CAGR** - Consistent historical growth
    - **Positive free cash flow** - Self-sustaining operations
    - **Low leverage** - 0.67 debt-to-equity ratio
    """)
    
    st.markdown("""
    ### Growth Runway
    - **AI market tailwinds** - Accelerating demand for GPU compute
    - **Customer retention** - Long-term enterprise relationships
    - **Scalable infrastructure** - Room for continued expansion
    - **Margin expansion** - Operating leverage driving profitability
    """)

# Footer
st.markdown("---")
st.caption("AI Datacenter Vancouver | Confidential Information | 2025")
'''

with open(f'{base_dir}/pages/5_📑_Company_Details.py', 'w') as f:
    f.write(page_company)

print("✓ Created pages/5_📑_Company_Details.py")
