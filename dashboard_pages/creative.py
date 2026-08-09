"""
Creative Performance page. Answers: "What creative should Gemini use, and where?"
"""

import streamlit as st

from charts.creative_charts import plot_creative_ranking, plot_creative_market_heatmap


def show_creative(creative_df):
    st.title("Creative Performance")
    st.caption("Which creative resonates best, globally and market-by-market?")

    st.sidebar.markdown("### Filters")
    markets = sorted(creative_df["Market"].unique().tolist())
    selected_markets = st.sidebar.multiselect("Market", markets, default=markets, key="creative_market")

    filtered_df = creative_df[creative_df["Market"].isin(selected_markets)]

    if filtered_df.empty:
        st.warning("No creative data matches the current filters.")
        return

    st.subheader("Global Creative Ranking")
    st.plotly_chart(plot_creative_ranking(filtered_df), use_container_width=True)

    st.divider()

    st.subheader("Creative × Market Resonance")
    st.caption(
        "The strongest creative overall doesn't always win in every market — this heatmap "
        "shows where each creative performs best."
    )
    st.plotly_chart(plot_creative_market_heatmap(filtered_df), use_container_width=True)

    with st.expander("Full data table"):
        st.dataframe(
            filtered_df.sort_values("Point_Est_Consideration", ascending=False),
            use_container_width=True,
            hide_index=True,
        )
