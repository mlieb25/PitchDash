"""
ROI Analysis Page - Deep dive into investor returns
"""
import streamlit as st
import pandas as pd
import sys
from pathlib import Path

sys.path.append(str(Path(__file__).parent.parent))

from utils.calculations import format_currency, format_percentage, format_multiple
from utils.visualizations import create_roi_comparison_chart, create_irr_comparison_chart

st.set_page_config(page_title="ROI Analysis", page_icon="💰", layout="wide")

# Load data
@st.cache_data
def load_data():
    data_path = Path(__file__).parent.parent / "data"
    roi_summary = pd.read_csv(data_path / "investor_roi_summary.csv")
    series_b_scenarios = pd.read_csv(data_path / "series_b_exit_scenarios.csv")
    series_c_scenarios = pd.read_csv(data_path / "series_c_exit_scenarios.csv")
    return roi_summary, series_b_scenarios, series_c_scenarios

roi_summary, series_b_scenarios, series_c_scenarios = load_data()

# Header
st.title("💰 Investor ROI Analysis")
st.markdown("Comprehensive return analysis across all funding rounds")

st.markdown("---")

# Funding Round Selector in Sidebar
st.sidebar.header("Select Funding Round")
selected_round = st.sidebar.radio(
    "Choose a round to analyze:",
    options=['All Rounds', 'Seed', 'Series A', 'Series B', 'Series C'],
    index=3  # Default to Series B
)

# Show all rounds comparison
if selected_round == 'All Rounds':
    st.header("Returns Comparison Across All Rounds")

    # Filter to show only completed and current opportunity
    display_roi = roi_summary[roi_summary['Round'].isin(['Seed', 'Series A', 'Series B', 'Series C'])]

    col1, col2 = st.columns(2)

    with col1:
        st.plotly_chart(create_roi_comparison_chart(display_roi), use_container_width=True)

    with col2:
        st.plotly_chart(create_irr_comparison_chart(display_roi), use_container_width=True)

    # Data table
    st.subheader("Detailed Returns Data")

    display_df = display_roi[[
        'Round', 'Investment_Year', 'Status', 'Investment_Amount', 
        'Entry_Valuation', 'MOIC', 'IRR_%', 'Holding_Period_Years'
    ]].copy()

    # Format columns
    display_df['Investment_Amount'] = display_df['Investment_Amount'].apply(lambda x: format_currency(x))
    display_df['Entry_Valuation'] = display_df['Entry_Valuation'].apply(lambda x: format_currency(x))
    display_df['MOIC'] = display_df['MOIC'].apply(lambda x: format_multiple(x))
    display_df['IRR_%'] = display_df['IRR_%'].apply(lambda x: f"{x:.1f}%")

    st.dataframe(display_df, use_container_width=True, hide_index=True)

# Individual round analysis
else:
    round_data = roi_summary[roi_summary['Round'] == selected_round].iloc[0]

    st.header(f"{selected_round} Investment Analysis")

    # Key metrics
    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.metric(
            "Investment Amount",
            format_currency(round_data['Investment_Amount']),
            delta=f"{round_data['Investment_Year']}"
        )

    with col2:
        st.metric(
            "Return Multiple",
            format_multiple(round_data['MOIC']),
            delta="at IPO exit"
        )

    with col3:
        st.metric(
            "IRR",
            format_percentage(round_data['IRR_%']),
            delta=f"{round_data['Holding_Period_Years']} year hold"
        )

    with col4:
        st.metric(
            "Exit Value",
            format_currency(round_data['Exit_Value_at_IPO']),
            delta=format_currency(round_data['Absolute_Return']) + " profit"
        )

    st.markdown("---")

    # Detailed breakdown
    col1, col2 = st.columns(2)

    with col1:
        st.subheader("Investment Details")
        st.markdown(f"""
        - **Round:** {round_data['Round']}
        - **Year:** {round_data['Investment_Year']}
        - **Status:** {round_data['Status']}
        - **Entry Valuation:** {format_currency(round_data['Entry_Valuation'])}
        - **Initial Ownership:** {round_data['Initial_Ownership_%']:.2f}%
        - **Final Ownership (post-dilution):** {round_data['Final_Ownership_%_at_IPO']:.2f}%
        """)

    with col2:
        st.subheader("Return Metrics")
        st.markdown(f"""
        - **Exit Valuation:** {format_currency(240000000)} (IPO 2030)
        - **Exit Value:** {format_currency(round_data['Exit_Value_at_IPO'])}
        - **Absolute Return:** {format_currency(round_data['Absolute_Return'])}
        - **MOIC:** {format_multiple(round_data['MOIC'])}
        - **IRR:** {format_percentage(round_data['IRR_%'])}
        - **Holding Period:** {round_data['Holding_Period_Years']} years
        """)

    # Series B specific: show exit scenarios
    if selected_round == 'Series B':
        st.markdown("---")
        st.subheader("🎯 Multiple Exit Scenarios for Series B")

        st.info("""
        Series B investors have the flexibility to exit at Series C (2028) or hold until IPO (2030).
        This optionality provides downside protection with early exit while maintaining upside potential.
        """)

        col1, col2 = st.columns(2)

        with col1:
            st.markdown("### Option 1: Early Exit at Series C")
            early_exit = series_b_scenarios[series_b_scenarios['Exit_Scenario'].str.contains('Early')].iloc[0]

            st.metric("Holding Period", f"{early_exit['Holding_Period']} years")
            st.metric("MOIC", format_multiple(early_exit['MOIC']))
            st.metric("IRR", format_percentage(early_exit['IRR_%']))
            st.metric("Exit Value", format_currency(early_exit['Exit_Value']))

            st.success("✅ Lower risk: Earlier exit, less dilution, quick liquidity")

        with col2:
            st.markdown("### Option 2: Hold to IPO")
            ipo_exit = series_b_scenarios[series_b_scenarios['Exit_Scenario'].str.contains('IPO')].iloc[0]

            st.metric("Holding Period", f"{ipo_exit['Holding_Period']} years")
            st.metric("MOIC", format_multiple(ipo_exit['MOIC']))
            st.metric("IRR", format_percentage(ipo_exit['IRR_%']))
            st.metric("Exit Value", format_currency(ipo_exit['Exit_Value']))

            st.success("✅ Higher returns: 2x more value, full upside capture")

    # Series B vs Series C comparison
    if selected_round in ['Series B', 'Series C']:
        st.markdown("---")
        st.subheader("📊 Series B vs Series C Comparison")

        series_b = roi_summary[roi_summary['Round'] == 'Series B'].iloc[0]
        series_c = roi_summary[roi_summary['Round'] == 'Series C'].iloc[0]

        comparison_df = pd.DataFrame({
            'Metric': [
                'Investment Amount',
                'Entry Valuation',
                'Investment Year',
                'MOIC at IPO',
                'IRR',
                'Holding Period',
                'Entry Price Advantage'
            ],
            'Series B (2026)': [
                format_currency(series_b['Investment_Amount']),
                format_currency(series_b['Entry_Valuation']),
                '2026',
                format_multiple(series_b['MOIC']),
                format_percentage(series_b['IRR_%']),
                f"{series_b['Holding_Period_Years']} years",
                '-67% vs Series C'
            ],
            'Series C (2028)': [
                format_currency(series_c['Investment_Amount']),
                format_currency(series_c['Entry_Valuation']),
                '2028',
                format_multiple(series_c['MOIC']),
                format_percentage(series_c['IRR_%']),
                f"{series_c['Holding_Period_Years']} years",
                'Baseline'
            ]
        })

        st.dataframe(comparison_df, use_container_width=True, hide_index=True)

        st.warning(f"""
        **Key Insight:** Series B investors achieve {series_b['MOIC']:.2f}x returns compared to 
        {series_c['MOIC']:.2f}x for Series C - a **{((series_b['MOIC']/series_c['MOIC'] - 1)*100):.0f}% higher multiple** 
        by investing 2 years earlier at a 67% lower valuation.
        """)

# Footer
st.markdown("---")
st.caption("All projections based on IPO exit at $240M valuation in 2030")
