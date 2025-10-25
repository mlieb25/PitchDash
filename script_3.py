
# Create utils/calculations.py - helper functions for ROI calculations
calculations_py = '''"""
Utility functions for investor ROI calculations and financial analysis
"""
import pandas as pd
import numpy as np

def calculate_roi(investment_amount, entry_valuation, exit_valuation, 
                  initial_ownership_pct, final_ownership_pct, years_held):
    """
    Calculate comprehensive ROI metrics for an investment
    
    Args:
        investment_amount: Amount invested in CAD
        entry_valuation: Post-money valuation at entry
        exit_valuation: Valuation at exit
        initial_ownership_pct: Ownership % at entry
        final_ownership_pct: Ownership % at exit (after dilution)
        years_held: Number of years until exit
    
    Returns:
        Dictionary with ROI metrics
    """
    exit_value = exit_valuation * (final_ownership_pct / 100)
    absolute_return = exit_value - investment_amount
    moic = exit_value / investment_amount if investment_amount > 0 else 0
    
    if years_held > 0 and moic > 0:
        irr = (moic ** (1/years_held) - 1) * 100
    else:
        irr = 0
    
    return {
        'investment': investment_amount,
        'exit_value': exit_value,
        'absolute_return': absolute_return,
        'moic': moic,
        'irr': irr,
        'years_held': years_held,
        'ownership_at_exit': final_ownership_pct
    }

def calculate_custom_investment_roi(investment_amount, round_name, round_year, 
                                     round_post_money_val, exit_year=2030, 
                                     exit_valuation=240000000):
    """
    Calculate ROI for a custom investment amount in a specific round
    
    Args:
        investment_amount: Custom investment amount
        round_name: Name of funding round
        round_year: Year of investment
        round_post_money_val: Post-money valuation of the round
        exit_year: Year of exit (default 2030)
        exit_valuation: Exit valuation (default $240M)
    
    Returns:
        Dictionary with ROI metrics
    """
    # Calculate ownership percentage based on investment amount
    ownership_pct = (investment_amount / round_post_money_val) * 100
    
    # Estimate dilution based on future rounds
    dilution_factors = {
        'Seed': 0.0902 / 25.0,  # Dilutes to 9.02% from 25%
        'Series_A': 0.1443 / 28.57,  # Dilutes to 14.43% from 28.57%
        'Series_B': 0.1616 / 24.24,  # Dilutes to 16.16% from 24.24%
        'Series_C': 0.1667 / 20.0,  # Dilutes to 16.67% from 20%
    }
    
    dilution_factor = dilution_factors.get(round_name, 1.0)
    final_ownership = ownership_pct * dilution_factor
    
    years_held = exit_year - round_year
    
    return calculate_roi(
        investment_amount=investment_amount,
        entry_valuation=round_post_money_val,
        exit_valuation=exit_valuation,
        initial_ownership_pct=ownership_pct,
        final_ownership_pct=final_ownership,
        years_held=years_held
    )

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
'''

with open(f'{base_dir}/utils/calculations.py', 'w') as f:
    f.write(calculations_py)

print("✓ Created utils/calculations.py")
