"""
Shared filter widgets for the Campaign Performance page (and anywhere else
that needs to slice the campaign-level dataframe). Centralised here so no
page has to re-implement the same selectboxes.
"""

import streamlit as st
import pandas as pd


def get_filter_options(df: pd.DataFrame) -> dict:
    """Collects the distinct values available for each filterable column."""
    return {
        "markets": sorted(df["Market"].dropna().unique().tolist()),
        "channels": sorted(df["Channel"].dropna().unique().tolist()),
        "campaigns": sorted(df["Campaign_Name"].dropna().unique().tolist()),
    }


def render_campaign_filters(df: pd.DataFrame, key_prefix: str = "campaign") -> dict:
    """
    Renders the filter widgets in the sidebar and returns the selections.
    Call this once per page that needs it, with a unique key_prefix.
    """
    options = get_filter_options(df)

    st.sidebar.markdown("### Filters")

    selected_market = st.sidebar.multiselect(
        "Market", options["markets"], default=options["markets"], key=f"{key_prefix}_market"
    )
    selected_channel = st.sidebar.multiselect(
        "Channel", options["channels"], default=options["channels"], key=f"{key_prefix}_channel"
    )
    selected_campaign = st.sidebar.multiselect(
        "Campaign", options["campaigns"], default=options["campaigns"], key=f"{key_prefix}_campaign"
    )
    significance_only = st.sidebar.checkbox(
        "Statistically significant only", value=False, key=f"{key_prefix}_sig"
    )

    return {
        "market": selected_market,
        "channel": selected_channel,
        "campaign": selected_campaign,
        "significance_only": significance_only,
    }


def apply_campaign_filters(df: pd.DataFrame, filters: dict) -> pd.DataFrame:
    """Applies the dict of selections returned by render_campaign_filters."""
    filtered = df[
        df["Market"].isin(filters["market"])
        & df["Channel"].isin(filters["channel"])
        & df["Campaign_Name"].isin(filters["campaign"])
    ]

    if filters["significance_only"]:
        filtered = filtered[filtered["is_significant"] == True]  # noqa: E712

    return filtered
