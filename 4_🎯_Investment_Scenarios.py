"""
Investment Scenarios Page - Interactive calculator for custom investment amounts
"""
import streamlit as st
import pandas as pd
import sys
from pathlib import Path

sys.path.append(str(Path(__file__).parent.parent))

from utils.calculations import (
    calculate_custom_investment_roi, 
    format_currency, 
    format_percentage, 
    format_multiple
)
import plotly.graph_objects as go

st.set_page_config(page_title="Investment Scenarios", page_icon="🎯", layout="wide")

# Load data
@st.cache_data
def load_data():
    data_path = Path(__file__).parent.parent / "data"
    funding_rounds = pd.read_csv(data_path / "funding_rounds_overview.csv")
    return funding_rounds

funding_rounds = load_data()

# Header
st.title("🎯 Investment Scenario Calculator")
st.markdown("Model custom investment amounts and compare returns across funding rounds")

st.markdown("---")

# Sidebar controls
st.sidebar.header("Investment Parameters")

# Round selector
selected_round = st.sidebar.selectbox(
    "Select Funding Round:",
    options=['Series B', 'Series C'],
    index=0
)

# Get round details
if selected_round == 'Series B':
    round_info = funding_rounds[funding_rounds['Round'] == 'Series_B'].iloc[0]
    min_investment = 500000
    max_investment = 8000000
    default_investment = 2000000
else:
    round_info = funding_rounds[funding_rounds['Round'] == 'Series_C'].iloc[0]
    min_investment = 1000000
    max_investment = 20000000
    default_investment = 5000000

# Investment amount slider
investment_amount = st.sidebar.slider(
    "Investment Amount ($)",
    min_value=min_investment,
    max_value=max_investment,
    value=default_investment,
    step=100000,
    format="$%d"
)

# Exit scenario
exit_scenario = st.sidebar.radio(
    "Exit Scenario:",
    options=['IPO (2030)', 'Conservative (80% of IPO)', 'Optimistic (120% of IPO)']
)

if exit_scenario == 'IPO (2030)':
    exit_valuation = 240000000
elif exit_scenario == 'Conservative (80% of IPO)':
    exit_valuation = 192000000
else:
    exit_valuation = 288000000

# Calculate ROI
roi = calculate_custom_investment_roi(
    investment_amount=investment_amount,
    round_name=selected_round.replace(' ', '_'),
    round_year=round_info['Year'],
    round_post_money_val=round_info['Post_Money_Valuation'],
    exit_year=2030,
    exit_valuation=exit_valuation
)

# Display Results
st.header(f"Your {selected_round} Investment Analysis")

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric(
        "Investment Amount",
        format_currency(investment_amount),
        delta=f"{round_info['Year']}"
    )

with col2:
    st.metric(
        "Exit Value",
        format_currency(roi['exit_value']),
        delta=format_currency(roi['absolute_return']) + " profit"
    )

with col3:
    st.metric(
        "Return Multiple",
        format_multiple(roi['moic']),
        delta="MOIC"
    )

with col4:
    st.metric(
        "Annualized Return",
        format_percentage(roi['irr']),
        delta=f"{roi['years_held']} year hold"
    )

# Detailed breakdown
st.markdown("---")

col1, col2 = st.columns(2)

with col1:
    st.subheader("Investment Details")

    ownership_pct = (investment_amount / round_info['Post_Money_Valuation']) * 100

    st.markdown(f"""
    **Funding Round:** {selected_round}  
    **Investment Year:** {round_info['Year']}  
    **Your Investment:** {format_currency(investment_amount)}  

    **Entry Valuation:**  
    - Pre-money: {format_currency(round_info['Pre_Money_Valuation'])}  
    - Post-money: {format_currency(round_info['Post_Money_Valuation'])}  

    **Ownership:**  
    - Initial: {ownership_pct:.3f}%  
    - At Exit (post-dilution): {roi['ownership_at_exit']:.3f}%  
    """)

with col2:
    st.subheader("Return Analysis")

    st.markdown(f"""
    **Exit Scenario:** {exit_scenario}  
    **Exit Year:** 2030  
    **Exit Valuation:** {format_currency(exit_valuation)}  

    **Your Returns:**  
    - Exit Value: {format_currency(roi['exit_value'])}  
    - Absolute Return: {format_currency(roi['absolute_return'])}  
    - Multiple (MOIC): {format_multiple(roi['moic'])}  
    - IRR: {format_percentage(roi['irr'])}  
    - Holding Period: {roi['years_held']} years  
    """)

# Comparison with other rounds
st.markdown("---")
st.header("Compare with Other Funding Rounds")

# Calculate ROI for same investment amount in different rounds
comparison_data = []

for round_name in ['Series B', 'Series C']:
    round_key = round_name.replace(' ', '_')
    round_data = funding_rounds[funding_rounds['Round'] == round_key].iloc[0]

    # Use smaller of investment amount or round size
    compare_investment = min(investment_amount, round_data['Amount_Raised'])

    compare_roi = calculate_custom_investment_roi(
        investment_amount=compare_investment,
        round_name=round_key,
        round_year=round_data['Year'],
        round_post_money_val=round_data['Post_Money_Valuation'],
        exit_year=2030,
        exit_valuation=exit_valuation
    )

    comparison_data.append({
        'Round': round_name,
        'Investment': compare_investment,
        'Entry_Valuation': round_data['Post_Money_Valuation'],
        'Exit_Value': compare_roi['exit_value'],
        'MOIC': compare_roi['moic'],
        'IRR_%': compare_roi['irr'],
        'Years': compare_roi['years_held']
    })

comparison_df = pd.DataFrame(comparison_data)

# Visualization
fig = go.Figure()

fig.add_trace(go.Bar(
    name='Exit Value',
    x=comparison_df['Round'],
    y=comparison_df['Exit_Value'],
    text=[format_currency(x) for x in comparison_df['Exit_Value']],
    textposition='outside',
    marker_color=['#0066CC', '#CC0066']
))

fig.update_layout(
    title=f"Exit Value Comparison for {format_currency(min(investment_amount, comparison_df['Investment'].min()))} Investment",
    xaxis_title="Funding Round",
    yaxis_title="Exit Value ($)",
    height=400,
    showlegend=False
)

st.plotly_chart(fig, use_container_width=True)

# Comparison table
st.subheader("Detailed Comparison")

display_comparison = comparison_df.copy()
display_comparison['Investment'] = display_comparison['Investment'].apply(format_currency)
display_comparison['Entry_Valuation'] = display_comparison['Entry_Valuation'].apply(format_currency)
display_comparison['Exit_Value'] = display_comparison['Exit_Value'].apply(format_currency)
display_comparison['MOIC'] = display_comparison['MOIC'].apply(format_multiple)
display_comparison['IRR_%'] = display_comparison['IRR_%'].apply(lambda x: f"{x:.1f}%")

st.dataframe(display_comparison, use_container_width=True, hide_index=True)

# Key insights
best_round = comparison_df.loc[comparison_df['MOIC'].idxmax(), 'Round']
best_moic = comparison_df.loc[comparison_df['MOIC'].idxmax(), 'MOIC']
best_irr = comparison_df.loc[comparison_df['MOIC'].idxmax(), 'IRR_%']

st.success(f"""
**Best Return:** {best_round} offers the highest returns with {format_multiple(best_moic)} MOIC 
and {format_percentage(best_irr)} IRR under the {exit_scenario} scenario.
""")

# Sensitivity Analysis
st.markdown("---")
st.header("Sensitivity Analysis")

st.markdown("How do returns change with different exit valuations?")

# Generate sensitivity data
exit_valuations = [160000000, 200000000, 240000000, 280000000, 320000000]
exit_labels = ['$160M', '$200M', '$240M (Base)', '$280M', '$320M']

sensitivity_data = []

for exit_val in exit_valuations:
    roi_sens = calculate_custom_investment_roi(
        investment_amount=investment_amount,
        round_name=selected_round.replace(' ', '_'),
        round_year=round_info['Year'],
        round_post_money_val=round_info['Post_Money_Valuation'],
        exit_year=2030,
        exit_valuation=exit_val
    )

    sensitivity_data.append({
        'Exit_Valuation': exit_val,
        'MOIC': roi_sens['moic'],
        'IRR_%': roi_sens['irr']
    })

sensitivity_df = pd.DataFrame(sensitivity_data)

# Create sensitivity chart
fig_sens = go.Figure()

fig_sens.add_trace(go.Scatter(
    x=exit_labels,
    y=sensitivity_df['MOIC'],
    mode='lines+markers',
    name='MOIC',
    line=dict(color='#0066CC', width=3),
    marker=dict(size=10)
))

fig_sens.update_layout(
    title=f"Return Sensitivity to Exit Valuation ({selected_round})",
    xaxis_title="Exit Valuation",
    yaxis_title="Multiple on Invested Capital (MOIC)",
    height=400,
    showlegend=False
)

st.plotly_chart(fig_sens, use_container_width=True)

col1, col2, col3 = st.columns(3)

with col1:
    st.metric(
        "Conservative Case ($160M)",
        format_multiple(sensitivity_df.iloc[0]['MOIC']),
        delta=format_percentage(sensitivity_df.iloc[0]['IRR_%'])
    )

with col2:
    st.metric(
        "Base Case ($240M)",
        format_multiple(sensitivity_df.iloc[2]['MOIC']),
        delta=format_percentage(sensitivity_df.iloc[2]['IRR_%'])
    )

with col3:
    st.metric(
        "Optimistic Case ($320M)",
        format_multiple(sensitivity_df.iloc[4]['MOIC']),
        delta=format_percentage(sensitivity_df.iloc[4]['IRR_%'])
    )

# Footer
st.markdown("---")
st.caption("All calculations assume proportional ownership based on investment amount and standard dilution patterns")
