"""
Charts built from creative_market_performance.csv
(one row per Market x Creative_Name, with mean Point_Est_Consideration).

NOTE: this file is grouped by market, not a true unweighted global average.
plot_creative_ranking() approximates the global ranking by averaging each
creative's per-market means, which matches the notebook's global figures
closely as long as each market has a similar number of underlying
observations (true for this dataset).
"""

import pandas as pd
import plotly.express as px


def plot_creative_ranking(df: pd.DataFrame):
    """Global creative ranking by average consideration score."""
    agg = (
        df.groupby("Creative_Name", as_index=False)["Point_Est_Consideration"]
        .mean()
        .sort_values("Point_Est_Consideration", ascending=False)
    )
    agg_sorted = agg.sort_values("Point_Est_Consideration", ascending=True)

    fig = px.bar(
        agg_sorted,
        x="Point_Est_Consideration",
        y="Creative_Name",
        orientation="h",
        text=agg_sorted["Point_Est_Consideration"].round(2),
        labels={"Point_Est_Consideration": "Avg Consideration Score", "Creative_Name": ""},
        title="Global Creative Ranking",
        color_discrete_sequence=["#673AB7"],
    )
    fig.update_traces(textposition="outside")
    return fig


def plot_creative_market_heatmap(df: pd.DataFrame):
    """Creative x Market heatmap — shows where each creative resonates best."""
    pivot = df.pivot(index="Creative_Name", columns="Market", values="Point_Est_Consideration")

    fig = px.imshow(
        pivot,
        text_auto=".2f",
        color_continuous_scale="Greens",
        aspect="auto",
        labels=dict(color="Consideration"),
        title="Creative Resonance by Market",
    )
    fig.update_xaxes(side="top")
    return fig


def plot_creative_channel(df: pd.DataFrame):
    """
    Optional: Creative x Channel comparison. Only works if the processed
    CSV includes a Channel column (creative_channel_performance from the
    notebook, which currently is not exported by default).
    """
    if "Channel" not in df.columns:
        raise ValueError(
            "plot_creative_channel() needs a 'Channel' column. Export "
            "creative_channel_performance from the notebook to use this chart."
        )
    agg = df.groupby(["Channel", "Creative_Name"], as_index=False)["Point_Est_Consideration"].mean()
    fig = px.bar(
        agg,
        x="Channel",
        y="Point_Est_Consideration",
        color="Creative_Name",
        barmode="group",
        title="Creative Resonance by Channel",
        labels={"Point_Est_Consideration": "Avg Consideration Score"},
    )
    return fig
