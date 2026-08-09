"""
Overview / landing page. Answers: "What are the most important things I
need to know about Gemini's marketing performance?"

Uses all three processed datasets.
"""

import streamlit as st

from utils.formatting import format_currency, format_number, format_percentage, format_cplu
from charts.market_channel_charts import plot_market_channel_heatmap
from charts.creative_charts import plot_creative_ranking


def show_overview(campaign_df, market_channel_df, creative_df):
    st.title("Gemini Pro Marketing — Overview")
    st.caption(
        "A summary of campaign performance, market/channel efficiency, and creative "
        "resonance for Gemini Pro's marketing consideration campaigns."
    )

    # --- Section 1: KPI cards -------------------------------------------------
    total_spend = campaign_df["Spend"].sum()
    total_reach = campaign_df["Reach"].sum()
    total_lifted_users = campaign_df["lifted_users"].sum()
    significant_campaigns = int(campaign_df["is_significant"].sum())
    avg_cplu = campaign_df["CPLU"].mean()

    col1, col2, col3 = st.columns(3)
    col1.metric("Total Spend", format_currency(total_spend, 0))
    col2.metric("Total Reach", format_number(total_reach))
    col3.metric("Estimated Lifted Users", format_number(total_lifted_users))

    col4, col5 = st.columns(2)
    col4.metric("Statistically Significant Campaigns", f"{significant_campaigns}")
    col5.metric("Average CPLU", format_cplu(avg_cplu))

    st.divider()

    # --- Section 2: Top campaigns ----------------------------------------------
    st.subheader("Top Campaigns")
    top_lift_row = campaign_df.loc[campaign_df["Relative_Lift"].idxmax()]
    top_cplu_row = campaign_df.dropna(subset=["CPLU"]).loc[campaign_df["CPLU"].idxmin()]

    c1, c2 = st.columns(2)
    with c1:
        st.markdown("**Highest Relative Lift**")
        st.markdown(
            f"**{top_lift_row['Campaign_Name']}** — {top_lift_row['Market']} / {top_lift_row['Channel']}"
        )
        st.markdown(f"Relative Lift: {format_percentage(top_lift_row['Relative_Lift'])}")
    with c2:
        st.markdown("**Most Cost-Efficient**")
        st.markdown(
            f"**{top_cplu_row['Campaign_Name']}** — {top_cplu_row['Market']} / {top_cplu_row['Channel']}"
        )
        st.markdown(f"CPLU: {format_cplu(top_cplu_row['CPLU'])}")

    st.divider()

    # --- Section 3: Market / Channel --------------------------------------------
    st.subheader("Market & Channel Efficiency")
    best_combo = market_channel_df.dropna(subset=["CPLU"]).sort_values("CPLU").iloc[0]
    st.markdown(
        f"Most efficient combination: **{best_combo['Market']} + {best_combo['Channel']}** "
        f"at {format_cplu(best_combo['CPLU'])} CPLU."
    )
    st.plotly_chart(plot_market_channel_heatmap(market_channel_df), use_container_width=True)

    st.divider()

    # --- Section 4: Creative -----------------------------------------------------
    st.subheader("Creative Performance")
    st.plotly_chart(plot_creative_ranking(creative_df), use_container_width=True)

    st.divider()

    # --- Section 5: Key insight cards --------------------------------------------
    st.subheader("Key Insights")
    top_creative = (
        creative_df.groupby("Creative_Name")["Point_Est_Consideration"].mean().idxmax()
    )

    i1, i2, i3, i4 = st.columns(4)
    i1.info(f"**Highest Impact**\n\n{top_lift_row['Campaign_Name']} — {top_lift_row['Market']} — {top_lift_row['Channel']}")
    i2.info(f"**Most Efficient**\n\n{top_cplu_row['Campaign_Name']} — {top_cplu_row['Market']} — {top_cplu_row['Channel']}")
    i3.info(f"**Strongest Creative**\n\n{top_creative}")
    i4.info(f"**Most Efficient Market/Channel**\n\n{best_combo['Market']} — {best_combo['Channel']}")
