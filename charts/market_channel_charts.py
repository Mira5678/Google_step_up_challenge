"""
Charts built from market_channel_analysis.csv
(one row per Market x Channel, with Spend, Reach, Lifted_Users, CPLU, CPR,
Relative_Cost_Index).
"""

import pandas as pd
import plotly.express as px


def plot_market_cplu(df: pd.DataFrame):
    """Average CPLU by market."""
    agg = df.groupby("Market", as_index=False)["CPLU"].mean().sort_values("CPLU")
    fig = px.bar(
        agg,
        x="Market",
        y="CPLU",
        text=agg["CPLU"].apply(lambda v: f"${v:.2f}"),
        labels={"CPLU": "Avg Cost per Lifted User ($)"},
        title="Average CPLU by Market",
        color_discrete_sequence=["#4285F4"],
    )
    fig.update_traces(textposition="outside")
    return fig


def plot_channel_cplu(df: pd.DataFrame):
    """Average CPLU by channel."""
    agg = df.groupby("Channel", as_index=False)["CPLU"].mean().sort_values("CPLU")
    fig = px.bar(
        agg,
        x="Channel",
        y="CPLU",
        text=agg["CPLU"].apply(lambda v: f"${v:.2f}"),
        labels={"CPLU": "Avg Cost per Lifted User ($)"},
        title="Average CPLU by Channel",
        color_discrete_sequence=["#0F9D58"],
    )
    fig.update_traces(textposition="outside")
    return fig


def plot_market_channel_heatmap(df: pd.DataFrame, metric: str = "CPLU"):
    """
    Market x Channel heatmap. Defaults to CPLU (lower = more efficient).
    This is the main chart for the page — mirrors the notebook's core analysis.
    """
    pivot = df.pivot(index="Market", columns="Channel", values=metric)

    fig = px.imshow(
        pivot,
        text_auto=".2f",
        color_continuous_scale="RdYlGn_r",  # red = expensive, green = cheap
        aspect="auto",
        labels=dict(color=metric),
        title=f"{metric} by Market and Channel",
    )
    fig.update_xaxes(side="top")
    return fig


def plot_cpr_comparison(df: pd.DataFrame):
    """Cost per Reach by channel — flags expensive channels like Search."""
    agg = df.groupby("Channel", as_index=False)["CPR"].mean().sort_values("CPR", ascending=False)
    fig = px.bar(
        agg,
        x="Channel",
        y="CPR",
        text=agg["CPR"].apply(lambda v: f"${v:.3f}"),
        labels={"CPR": "Avg Cost per Reach ($)"},
        title="Average Cost per Reach (CPR) by Channel",
        color_discrete_sequence=["#F4B400"],
    )
    fig.update_traces(textposition="outside")
    return fig

def plot_allocation_comparison(allocation_df: pd.DataFrame):
    """
    Grouped bar chart comparing current spend vs recommended spend per
    Market x Channel combo. Expects columns: Market, Channel,
    Current_Spend, Recommended_Spend.
    """
    df = allocation_df.copy()
    df["label"] = df["Market"] + " · " + df["Channel"]
    df = df.sort_values("Recommended_Spend", ascending=True)

    melted = df.melt(
        id_vars="label",
        value_vars=["Current_Spend", "Recommended_Spend"],
        var_name="Type",
        value_name="Spend",
    )
    melted["Type"] = melted["Type"].map(
        {"Current_Spend": "Current", "Recommended_Spend": "Recommended"}
    )

    fig = px.bar(
        melted,
        x="Spend",
        y="label",
        color="Type",
        orientation="h",
        barmode="group",
        labels={"Spend": "Spend ($)", "label": ""},
        title="Current vs Recommended Spend by Market/Channel",
        color_discrete_map={"Current": "#B0BEC5", "Recommended": "#0F9D58"},
    )
    return fig


def plot_lifted_users_comparison(allocation_df: pd.DataFrame):
    """
    Grouped bar chart comparing current vs projected lifted users per
    Market x Channel combo. Expects columns: Market, Channel,
    Current_Lifted_Users, Projected_Lifted_Users.
    """
    df = allocation_df.copy()
    df["label"] = df["Market"] + " · " + df["Channel"]
    df = df.sort_values("Projected_Lifted_Users", ascending=True)

    melted = df.melt(
        id_vars="label",
        value_vars=["Current_Lifted_Users", "Projected_Lifted_Users"],
        var_name="Type",
        value_name="Lifted_Users",
    )
    melted["Type"] = melted["Type"].map(
        {"Current_Lifted_Users": "Current", "Projected_Lifted_Users": "Projected"}
    )

    fig = px.bar(
        melted,
        x="Lifted_Users",
        y="label",
        color="Type",
        orientation="h",
        barmode="group",
        labels={"Lifted_Users": "Lifted Users", "label": ""},
        title="Current vs Projected Lifted Users by Market/Channel",
        color_discrete_map={"Current": "#B0BEC5", "Recommended": "#4285F4", "Projected": "#4285F4"},
    )
    return fig


def plot_relative_cost_index(df: pd.DataFrame, top_n: int = 10):
    """
    Relative Cost Index by Market x Channel. 100 = average cost to target,
    >100 = more expensive than average, <100 = cheaper than average.
    """
    combo = df.copy()
    combo["label"] = combo["Market"] + " · " + combo["Channel"]
    top = combo.sort_values("Relative_Cost_Index", ascending=False).head(top_n)
    top = top.sort_values("Relative_Cost_Index", ascending=True)

    fig = px.bar(
        top,
        x="Relative_Cost_Index",
        y="label",
        orientation="h",
        text=top["Relative_Cost_Index"].round(0).astype(int).astype(str),
        labels={"Relative_Cost_Index": "Relative Cost Index (100 = average)", "label": ""},
        title="Most Expensive Market/Channel Combinations to Target",
        color_discrete_sequence=["#DB4437"],
    )
    fig.add_vline(x=100, line_dash="dash", line_color="gray", annotation_text="Average")
    fig.update_traces(textposition="outside")
    return fig
