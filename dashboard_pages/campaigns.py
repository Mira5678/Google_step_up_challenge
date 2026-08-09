"""
Campaign Performance page. Answers: "Which campaigns worked best?"
"""

import streamlit as st

from utils.filters import render_campaign_filters, apply_campaign_filters
from utils.formatting import format_currency, format_number, format_percentage, format_cplu, significance_badge
from charts.campaign_charts import (
    plot_campaign_lift,
    plot_campaign_cplu,
    plot_lift_vs_cplu,
    plot_campaign_spend,
)


def show_campaigns(campaign_df):
    st.title("Campaign Performance")
    st.caption("Which campaigns generated the strongest, most cost-efficient brand lift?")

    filters = render_campaign_filters(campaign_df, key_prefix="campaigns_page")
    filtered_df = apply_campaign_filters(campaign_df, filters)

    if filtered_df.empty:
        st.warning("No campaigns match the current filters.")
        return

    # --- KPI cards ---
    col1, col2, col3, col4 = st.columns(4)
    top_lift = filtered_df["Relative_Lift"].max()
    lowest_cplu = filtered_df["CPLU"].min()
    sig_count = int(filtered_df["is_significant"].sum())
    total_lifted = filtered_df["lifted_users"].sum()

    col1.metric("Highest Relative Lift", format_percentage(top_lift))
    col2.metric("Lowest CPLU", format_cplu(lowest_cplu))
    col3.metric("Significant Campaigns", sig_count)
    col4.metric("Total Lifted Users", format_number(total_lifted))

    st.divider()

    # --- Charts ---
    top_n = st.slider("Number of campaigns to show in charts", 5, 20, 10, key="campaigns_top_n")

    tab1, tab2, tab3 = st.tabs(["Impact vs Efficiency", "Top by Lift", "Top by CPLU"])
    with tab1:
        st.plotly_chart(plot_lift_vs_cplu(filtered_df), use_container_width=True)
    with tab2:
        st.plotly_chart(plot_campaign_lift(filtered_df, top_n=top_n), use_container_width=True)
    with tab3:
        st.plotly_chart(plot_campaign_cplu(filtered_df, top_n=top_n), use_container_width=True)

    with st.expander("Spend breakdown"):
        st.plotly_chart(plot_campaign_spend(filtered_df, top_n=top_n), use_container_width=True)

    st.divider()

    # --- Table ---
    st.subheader("Campaign Detail")
    display_df = filtered_df.copy()
    display_df["Significant?"] = display_df["is_significant"].apply(significance_badge)
    display_df["Relative Lift"] = display_df["Relative_Lift"].apply(format_percentage)
    display_df["CPLU"] = display_df["CPLU"].apply(format_cplu)
    display_df["Spend"] = display_df["Spend"].apply(lambda v: format_currency(v, 0))
    display_df["Reach"] = display_df["Reach"].apply(format_number)

    columns_to_show = [
        "Campaign_Name", "Market", "Channel", "Relative Lift", "absolute_lift",
        "pval", "Significant?", "lifted_users", "CPLU", "Spend", "Reach",
    ]
    columns_to_show = [c for c in columns_to_show if c in display_df.columns]
    st.dataframe(
        display_df[columns_to_show].rename(columns={
            "Campaign_Name": "Campaign",
            "absolute_lift": "Absolute Lift (pp)",
            "pval": "p-value",
            "lifted_users": "Lifted Users",
        }),
        use_container_width=True,
        hide_index=True,
    )
