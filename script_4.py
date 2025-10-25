
# Create utils/visualizations.py - Plotly chart creation functions
visualizations_py = '''"""
Plotly visualization functions for the investor dashboard
"""
import plotly.graph_objects as go
import plotly.express as px
from plotly.subplots import make_subplots
import pandas as pd

def create_roi_comparison_chart(roi_data):
    """
    Create bar chart comparing MOIC across funding rounds
    
    Args:
        roi_data: DataFrame with columns ['Round', 'MOIC', 'IRR_%']
    
    Returns:
        Plotly figure
    """
    colors = ['#0066CC', '#0052A3', '#003D7A', '#002952']
    
    fig = go.Figure()
    
    fig.add_trace(go.Bar(
        x=roi_data['Round'],
        y=roi_data['MOIC'],
        text=[f"{x:.2f}x" for x in roi_data['MOIC']],
        textposition='outside',
        marker_color=colors[:len(roi_data)],
        name='MOIC'
    ))
    
    # Add benchmark line at 3x
    fig.add_hline(y=3.0, line_dash="dash", line_color="gray", 
                  annotation_text="VC Benchmark (3x)", 
                  annotation_position="right")
    
    fig.update_layout(
        title="Return Multiples by Funding Round (Exit at IPO)",
        xaxis_title="Funding Round",
        yaxis_title="Multiple on Invested Capital (MOIC)",
        height=400,
        showlegend=False,
        hovermode='x unified'
    )
    
    return fig

def create_valuation_revenue_chart(financials_df):
    """
    Create dual-axis chart with valuation and revenue
    
    Args:
        financials_df: DataFrame with columns ['Year', 'Revenue', 'Company_Valuation', 'Status']
    
    Returns:
        Plotly figure
    """
    fig = make_subplots(specs=[[{"secondary_y": True}]])
    
    # Split into historical and projected
    historical = financials_df[financials_df['Status'] == 'Historical']
    projected = financials_df[financials_df['Status'] == 'Projected']
    
    # Revenue line (historical)
    fig.add_trace(
        go.Scatter(
            x=historical['Year'],
            y=historical['Revenue'] / 1_000_000,
            name="Revenue (Historical)",
            line=dict(color='#00CC66', width=3),
            mode='lines+markers'
        ),
        secondary_y=False
    )
    
    # Revenue line (projected)
    fig.add_trace(
        go.Scatter(
            x=projected['Year'],
            y=projected['Revenue'] / 1_000_000,
            name="Revenue (Projected)",
            line=dict(color='#00CC66', width=3, dash='dash'),
            mode='lines+markers'
        ),
        secondary_y=False
    )
    
    # Valuation bars (historical)
    fig.add_trace(
        go.Bar(
            x=historical['Year'],
            y=historical['Company_Valuation'] / 1_000_000,
            name="Valuation (Historical)",
            marker_color='#0066CC',
            opacity=0.6
        ),
        secondary_y=True
    )
    
    # Valuation bars (projected)
    fig.add_trace(
        go.Bar(
            x=projected['Year'],
            y=projected['Company_Valuation'] / 1_000_000,
            name="Valuation (Projected)",
            marker_color='#99CCFF',
            opacity=0.6
        ),
        secondary_y=True
    )
    
    # Add funding round annotations
    funding_events = [
        (2015, 'Seed'),
        (2017, 'Series A'),
        (2026, 'Series B'),
        (2028, 'Series C'),
        (2030, 'IPO')
    ]
    
    for year, label in funding_events:
        fig.add_vline(
            x=year,
            line_dash="dot",
            line_color="gray",
            annotation_text=label,
            annotation_position="top"
        )
    
    fig.update_xaxes(title_text="Year")
    fig.update_yaxes(title_text="Revenue ($M CAD)", secondary_y=False)
    fig.update_yaxes(title_text="Valuation ($M CAD)", secondary_y=True)
    
    fig.update_layout(
        title="Company Valuation & Revenue Growth",
        height=500,
        hovermode='x unified',
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1)
    )
    
    return fig

def create_ownership_chart(ownership_df):
    """
    Create stacked bar chart showing ownership evolution
    
    Args:
        ownership_df: DataFrame with ownership percentages
    
    Returns:
        Plotly figure
    """
    fig = go.Figure()
    
    stakeholders = ['Founders', 'Seed_Investors', 'Series_A_Investors', 
                   'Series_B_Investors', 'Series_C_Investors', 'IPO_Public']
    
    colors = {
        'Founders': '#FFB800',
        'Seed_Investors': '#0066CC',
        'Series_A_Investors': '#00CC66',
        'Series_B_Investors': '#CC0066',
        'Series_C_Investors': '#6600CC',
        'IPO_Public': '#CCCCCC'
    }
    
    labels = {
        'Founders': 'Founders',
        'Seed_Investors': 'Seed',
        'Series_A_Investors': 'Series A',
        'Series_B_Investors': 'Series B',
        'Series_C_Investors': 'Series C',
        'IPO_Public': 'Public'
    }
    
    for stakeholder in stakeholders:
        if stakeholder in ownership_df.columns:
            fig.add_trace(go.Bar(
                name=labels[stakeholder],
                x=ownership_df['Milestone'],
                y=ownership_df[stakeholder],
                marker_color=colors[stakeholder],
                text=[f"{v:.1f}%" if v > 0 else "" for v in ownership_df[stakeholder]],
                textposition='inside'
            ))
    
    fig.update_layout(
        barmode='stack',
        title="Ownership Dilution Across Funding Rounds",
        xaxis_title="Funding Milestone",
        yaxis_title="Ownership %",
        height=400,
        yaxis=dict(range=[0, 100]),
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1)
    )
    
    return fig

def create_metric_card_figure(value, label, delta=None, prefix="", suffix=""):
    """
    Create a metric display figure
    
    Args:
        value: Main value to display
        label: Label for the metric
        delta: Optional change value
        prefix: Prefix for value (e.g., "$")
        suffix: Suffix for value (e.g., "%")
    
    Returns:
        Plotly figure
    """
    fig = go.Figure()
    
    display_text = f"{prefix}{value:,.2f}{suffix}"
    if delta:
        delta_text = f"Δ {prefix}{delta:,.2f}{suffix}"
        color = 'green' if delta > 0 else 'red'
    else:
        delta_text = ""
        color = 'gray'
    
    fig.add_annotation(
        text=display_text,
        xref="paper", yref="paper",
        x=0.5, y=0.6,
        showarrow=False,
        font=dict(size=32, color='#262730', family='Arial Black')
    )
    
    fig.add_annotation(
        text=label,
        xref="paper", yref="paper",
        x=0.5, y=0.3,
        showarrow=False,
        font=dict(size=14, color='#666666')
    )
    
    if delta_text:
        fig.add_annotation(
            text=delta_text,
            xref="paper", yref="paper",
            x=0.5, y=0.15,
            showarrow=False,
            font=dict(size=12, color=color)
        )
    
    fig.update_layout(
        height=150,
        margin=dict(l=10, r=10, t=10, b=10),
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        xaxis=dict(showgrid=False, showticklabels=False, zeroline=False),
        yaxis=dict(showgrid=False, showticklabels=False, zeroline=False)
    )
    
    return fig

def create_irr_comparison_chart(roi_data):
    """
    Create chart comparing IRR across rounds
    
    Args:
        roi_data: DataFrame with IRR data
    
    Returns:
        Plotly figure
    """
    colors = ['#0066CC', '#0052A3', '#003D7A', '#002952']
    
    fig = go.Figure()
    
    fig.add_trace(go.Bar(
        x=roi_data['Round'],
        y=roi_data['IRR_%'],
        text=[f"{x:.1f}%" for x in roi_data['IRR_%']],
        textposition='outside',
        marker_color=colors[:len(roi_data)],
        name='IRR'
    ))
    
    # Add benchmark line at 25% (good VC return)
    fig.add_hline(y=25.0, line_dash="dash", line_color="gray", 
                  annotation_text="VC Target (25%)", 
                  annotation_position="right")
    
    fig.update_layout(
        title="Internal Rate of Return (IRR) by Funding Round",
        xaxis_title="Funding Round",
        yaxis_title="IRR (%)",
        height=400,
        showlegend=False,
        hovermode='x unified'
    )
    
    return fig
'''

with open(f'{base_dir}/utils/visualizations.py', 'w') as f:
    f.write(visualizations_py)

print("✓ Created utils/visualizations.py")

# Create __init__.py
with open(f'{base_dir}/utils/__init__.py', 'w') as f:
    f.write('')

print("✓ Created utils/__init__.py")
