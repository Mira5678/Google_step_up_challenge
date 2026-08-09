"""
Small formatting helpers so numbers look consistent everywhere in the dashboard.
Nothing in here touches data — pure presentation.
"""

import pandas as pd


def format_currency(value, decimals: int = 2) -> str:
    """0.153423 -> '$0.15'"""
    if value is None or pd.isna(value):
        return "N/A"
    return f"${value:,.{decimals}f}"


def format_percentage(value, decimals: int = 1) -> str:
    """103.9321 -> '103.9%'  (expects the value already in percentage units, e.g. Relative_Lift)"""
    if value is None or pd.isna(value):
        return "N/A"
    return f"{value:,.{decimals}f}%"


def format_number(value, decimals: int = 0) -> str:
    """123456.7 -> '123,457'"""
    if value is None or pd.isna(value):
        return "N/A"
    return f"{value:,.{decimals}f}"


def format_cplu(value) -> str:
    """Cost Per Lifted User -> currency, 2 decimals."""
    return format_currency(value, decimals=2)


def format_cpr(value) -> str:
    """Cost Per Reach -> currency, 3 decimals (values are typically < $0.10)."""
    return format_currency(value, decimals=3)


def significance_badge(is_significant) -> str:
    """Small text badge for statistical significance, used in tables/cards."""
    if pd.isna(is_significant):
        return "No data"
    return "✅ Significant" if bool(is_significant) else "⚪ Not significant"
