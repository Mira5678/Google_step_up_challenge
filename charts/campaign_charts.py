"""
Charts built from processed_campaign_analysis.csv (campaign-level:
one row per Campaign x Market x Channel).
"""

import pandas as pd
import plotly.express as px


def plot_campaign_lift(df: pd.DataFrame, top_n: int = 10):
    """Horizontal bar chart of the top N campaigns by Relative_Lift."""
    top = df.sort_values("Relative_Lift", ascending=False).head(top_n)
    top = top.sort_values("Relative_Lift", ascending=True)  # so #1 sits at the top of the chart

    fig = px.bar(
        top,
        x="Relative_Lift",
        y="Campaign_Name",
        color="is_significant",
        orientation="h",
        text=top["Relative_Lift"].round(1).astype(str) + "%",
        color_discrete_map={True: "#0F9D58", False: "#B0BEC5"},
        labels={"Relative_Lift": "Relative Lift (%)", "Campaign_Name": "", "is_significant": "Significant"},
        title=f"Top {top_n} Campaigns by Relative Lift",
        hover_data=["Market", "Channel"],
    )
    fig.update_traces(textposition="outside")
    fig.update_layout(showlegend=True)
    return fig


def plot_campaign_cplu(df: pd.DataFrame, top_n: int = 10):
    """Horizontal bar chart of the top N most cost-efficient campaigns (lowest CPLU)."""
    valid = df.dropna(subset=["CPLU"])
    top = valid.sort_values("CPLU", ascending=True).head(top_n)
    top = top.sort_values("CPLU", ascending=False)

    fig = px.bar(
        top,
        x="CPLU",
        y="Campaign_Name",
        orientation="h",
        text=top["CPLU"].apply(lambda v: f"${v:.2f}"),
        labels={"CPLU": "Cost per Lifted User ($)", "Campaign_Name": ""},
        title=f"Top {top_n} Most Efficient Campaigns (Lowest CPLU)",
        color_discrete_sequence=["#4285F4"],
        hover_data=["Market", "Channel"],
    )
    fig.update_traces(textposition="outside")
    return fig


def plot_lift_vs_cplu(df: pd.DataFrame):
    """
    Quadrant scatter: Relative Lift vs CPLU, split on medians.
    The single most useful chart on this page — flags best performers,
    effective-but-expensive, efficient-but-limited, and weak campaigns.
    """
    plot_df = df.dropna(subset=["CPLU", "Relative_Lift"]).copy()

    median_cplu = plot_df["CPLU"].median()
    median_lift = plot_df["Relative_Lift"].median()

    def classify(row):
        if row["Relative_Lift"] >= median_lift and row["CPLU"] <= median_cplu:
            return "Best performers"
        elif row["Relative_Lift"] >= median_lift and row["CPLU"] > median_cplu:
            return "Effective but expensive"
        elif row["Relative_Lift"] < median_lift and row["CPLU"] <= median_cplu:
            return "Efficient but limited impact"
        return "Weak performers"

    plot_df["Quadrant"] = plot_df.apply(classify, axis=1)

    fig = px.scatter(
        plot_df,
        x="CPLU",
        y="Relative_Lift",
        color="Quadrant",
        size="Reach" if "Reach" in plot_df.columns else None,
        hover_name="Campaign_Name",
        hover_data=["Market", "Channel", "is_significant"],
        labels={"CPLU": "Cost per Lifted User ($)", "Relative_Lift": "Relative Lift (%)"},
        title="Campaign Impact vs Efficiency",
        color_discrete_map={
            "Best performers": "#0F9D58",
            "Effective but expensive": "#F4B400",
            "Efficient but limited impact": "#4285F4",
            "Weak performers": "#DB4437",
        },
    )
    fig.add_vline(x=median_cplu, line_dash="dash", line_color="gray")
    fig.add_hline(y=median_lift, line_dash="dash", line_color="gray")
    return fig


def plot_campaign_spend(df: pd.DataFrame, top_n: int = 10):
    """Horizontal bar chart of total spend by campaign."""
    top = df.sort_values("Spend", ascending=False).head(top_n)
    top = top.sort_values("Spend", ascending=True)

    fig = px.bar(
        top,
        x="Spend",
        y="Campaign_Name",
        orientation="h",
        text=top["Spend"].apply(lambda v: f"${v:,.0f}"),
        labels={"Spend": "Total Spend ($)", "Campaign_Name": ""},
        title=f"Top {top_n} Campaigns by Spend",
        color_discrete_sequence=["#673AB7"],
        hover_data=["Market", "Channel"],
    )
    fig.update_traces(textposition="outside")
    return fig
