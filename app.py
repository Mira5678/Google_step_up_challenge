"""
Gemini Pro Marketing Intelligence Dashboard
Run with: streamlit run app.py
"""

import streamlit as st

from utils.data_loader import load_all_data, check_data_files_exist
from dashboard_pages.overview import show_overview
from dashboard_pages.campaigns import show_campaigns
from dashboard_pages.markets_channels import show_markets_channels
from dashboard_pages.creative import show_creative
from dashboard_pages.recommendations import show_recommendations


def main():
    st.set_page_config(
        page_title="Gemini Pro Marketing Intelligence",
        layout="wide",
    )

    missing_files = check_data_files_exist()
    if missing_files:
        st.error(
            "Missing processed data file(s): " + ", ".join(missing_files) + ".\n\n"
            "Run the analysis notebook first and confirm it exports to `data/processed/`:\n"
            "- processed_campaign_analysis.csv (the aggregated `campaign_analysis` dataframe, "
            "not the raw weekly `result_df`)\n"
            "- market_channel_analysis.csv\n"
            "- creative_market_performance.csv"
        )
        st.stop()

    data = load_all_data()
    campaign_df = data["campaign"]
    market_channel_df = data["market_channel"]
    creative_df = data["creative"]

    st.sidebar.title("Gemini Pro Marketing")
    page = st.sidebar.radio(
        "Navigate",
        [
            "Overview",
            "Campaign Performance",
            "Markets & Channels",
            "Creative Performance",
            "Recommendations",
        ],
    )
    st.sidebar.divider()

    if page == "Overview":
        show_overview(campaign_df, market_channel_df, creative_df)
    elif page == "Campaign Performance":
        show_campaigns(campaign_df)
    elif page == "Markets & Channels":
        show_markets_channels(market_channel_df)
    elif page == "Creative Performance":
        show_creative(creative_df)
    elif page == "Recommendations":
        show_recommendations(campaign_df, market_channel_df, creative_df)


if __name__ == "__main__":
    main()
