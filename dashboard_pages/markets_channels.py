"""
Markets & Channels page. Answers: "Where should Gemini focus its marketing?"
"""

import streamlit as st

from utils.formatting import format_cplu, format_cpr
from charts.market_channel_charts import (
    plot_market_cplu,
    plot_channel_cplu,
    plot_market_channel_heatmap,
    plot_cpr_comparison,
    plot_relative_cost_index,
)


def show_markets_channels(market_channel_df):
    st.title("Markets & Channels")
    st.caption("Where is Gemini Pro's marketing spend working hardest, and where is it expensive?")

    st.sidebar.markdown("### Filters")
    markets = sorted(market_channel_df["Market"].unique().tolist())
    channels = sorted(market_channel_df["Channel"].unique().tolist())
    selected_markets = st.sidebar.multiselect("Market", markets, default=markets, key="mc_market")
    selected_channels = st.sidebar.multiselect("Channel", channels, default=channels, key="mc_channel")

    filtered_df = market_channel_df[
        market_channel_df["Market"].isin(selected_markets)
        & market_channel_df["Channel"].isin(selected_channels)
    ]

    if filtered_df.empty:
        st.warning("No market/channel combinations match the current filters.")
        return

    # --- Market performance ---
    st.subheader("Market Performance")
    st.plotly_chart(plot_market_cplu(filtered_df), use_container_width=True)

    st.divider()

    # --- Channel performance ---
    st.subheader("Channel Performance")
    st.plotly_chart(plot_channel_cplu(filtered_df), use_container_width=True)

    st.divider()

    # --- Heatmap: main visual ---
    st.subheader("Market × Channel Efficiency")
    metric = st.radio("Metric", ["CPLU", "CPR"], horizontal=True, key="mc_heatmap_metric")
    st.plotly_chart(plot_market_channel_heatmap(filtered_df, metric=metric), use_container_width=True)

    st.divider()

    # --- Cost analysis ---
    st.subheader("Cost Analysis")
    st.markdown(
        "**Relative Cost Index**: 100 = average cost to target across all Market × Channel "
        "combinations. Above 100 is more expensive than average, below 100 is cheaper."
    )
    c1, c2 = st.columns(2)
    with c1:
        st.plotly_chart(plot_cpr_comparison(filtered_df), use_container_width=True)
    with c2:
        st.plotly_chart(plot_relative_cost_index(filtered_df), use_container_width=True)

    with st.expander("Full data table"):
        table_df = filtered_df.copy()
        table_df["CPLU"] = table_df["CPLU"].apply(format_cplu)
        table_df["CPR"] = table_df["CPR"].apply(format_cpr)
        st.dataframe(table_df, use_container_width=True, hide_index=True)
