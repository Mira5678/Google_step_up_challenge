"""
Loads the three processed CSVs produced by the analysis notebook
(notebooks/insights.ipynb -> data/processed/*.csv).

Expected schemas
-----------------
processed_campaign_analysis.csv  (one row per Campaign x Market x Channel)
    Campaign_Name, Market, Channel, Spend, Reach, Conversions,
    Relative_Lift, Exposed_Rate, Control_Rate, pval, is_significant,
    absolute_lift, lifted_users, CPLU, CPR

market_channel_analysis.csv  (one row per Market x Channel)
    Market, Channel, Spend, Reach, Lifted_Users, CPLU, CPR, Relative_Cost_Index

creative_market_performance.csv  (one row per Market x Creative)
    Market, Creative_Name, Point_Est_Consideration

"""

from pathlib import Path

import pandas as pd
import streamlit as st

DATA_DIR = Path(__file__).resolve().parent.parent / "data" / "processed"

CAMPAIGN_FILE = DATA_DIR / "processed_campaign_analysis.csv"
MARKET_CHANNEL_FILE = DATA_DIR / "market_channel_analysis.csv"
CREATIVE_FILE = DATA_DIR / "creative_market_performance.csv"


@st.cache_data
def load_campaign_data() -> pd.DataFrame:
    """Campaign-level performance: lift, significance, CPLU, CPR."""
    df = pd.read_csv(CAMPAIGN_FILE)
    df["is_significant"] = df["is_significant"].astype("boolean")
    return df


@st.cache_data
def load_market_channel_data() -> pd.DataFrame:
    """Market x Channel efficiency and targeting cost."""
    return pd.read_csv(MARKET_CHANNEL_FILE)


@st.cache_data
def load_creative_data() -> pd.DataFrame:
    """Creative resonance (consideration score) by market."""
    return pd.read_csv(CREATIVE_FILE)


@st.cache_data
def load_all_data() -> dict[str, pd.DataFrame]:
    return {
        "campaign": load_campaign_data(),
        "market_channel": load_market_channel_data(),
        "creative": load_creative_data(),
    }


def check_data_files_exist() -> list[str]:
    """Returns a list of missing file names, empty if everything is present."""
    missing = []
    for f in (CAMPAIGN_FILE, MARKET_CHANNEL_FILE, CREATIVE_FILE):
        if not f.exists():
            missing.append(f.name)
    return missing
