"""
Budget Optimisation page. Answers: "If I have $X to spend, how should it
be split across markets and channels to get the most lifted users?"

Uses market_channel_analysis.csv (Market x Channel level CPLU) as the
efficiency signal. See utils/optimizer.py for the allocation method and
its assumptions -- this is a heuristic, not a guaranteed-optimal solution.
"""

import streamlit as st

from utils.formatting import format_currency, format_number, format_cplu
from utils.optimizer import optimize_allocation
from charts.market_channel_charts import plot_allocation_comparison, plot_lifted_users_comparison


def show_budget_optimisation(market_channel_df):
    st.title("Budget Optimisation")
    st.caption(
        "Recommended budget allocation across Market × Channel combinations, "
        "based on historical cost-per-lifted-user (CPLU)."
    )

    with st.expander("How this works, and its limitations", expanded=False):
        st.markdown(
            "- Each Market × Channel combination's historical **CPLU** (cost per lifted user) "
            "is used as its efficiency score. Cheaper CPLU = more lifted users per dollar.\n"
            "- The optimiser fills the cheapest combinations first, up to a **cap** on how much "
            "of the total budget any single combination can absorb — without a cap it would "
            "put 100% of spend into whichever combo happened to have the lowest historical CPLU, "
            "which isn't realistic.\n"
            "- **This assumes CPLU stays constant as spend increases.** In reality, pushing more "
            "budget into a channel usually raises its cost per result (diminishing returns) — "
            "we don't have the underlying spend-response curve to model that, so treat this as "
            "**directional guidance**, not a guaranteed outcome.\n"
            "- Combinations with no positive CPLU (no measurable lift in the data) are excluded "
            "from the optimisation."
        )

    # --- Controls -------------------------------------------------------------
    st.sidebar.markdown("### Budget Settings")

    current_total_spend = float(market_channel_df["Spend"].sum())
    total_budget = st.sidebar.number_input(
        "Total budget to allocate ($)",
        min_value=0.0,
        value=current_total_spend,
        step=1000.0,
        format="%.0f",
    )
    max_share_per_combo = st.sidebar.slider(
        "Max share of budget per Market/Channel combo",
        min_value=0.05,
        max_value=1.0,
        value=0.35,
        step=0.05,
        help="Caps how concentrated the recommendation can get. Lower = more diversified.",
    )

    markets = sorted(market_channel_df["Market"].unique().tolist())
    channels = sorted(market_channel_df["Channel"].unique().tolist())
    selected_markets = st.sidebar.multiselect("Include markets", markets, default=markets, key="budget_market")
    selected_channels = st.sidebar.multiselect("Include channels", channels, default=channels, key="budget_channel")

    candidates = market_channel_df[
        market_channel_df["Market"].isin(selected_markets)
        & market_channel_df["Channel"].isin(selected_channels)
    ]

    if candidates.empty:
        st.warning("No Market/Channel combinations match the current filters.")
        return

    if total_budget <= 0:
        st.info("Set a total budget above zero in the sidebar to see a recommended allocation.")
        return

    try:
        allocation_df, leftover_relaxed = optimize_allocation(
            candidates, total_budget=total_budget, max_share_per_combo=max_share_per_combo
        )
    except ValueError as e:
        st.error(str(e))
        return

    if leftover_relaxed:
        st.info(
            "The per-combo cap was too tight to spend the full budget across the included "
            "combinations, so the remainder was distributed efficiency-weighted, ignoring the cap. "
            "Raise the cap, include more combinations, or lower the budget to avoid this."
        )

    # --- KPI comparison ---------------------------------------------------------
    projected_lifted_users = allocation_df["Projected_Lifted_Users"].sum()
    projected_blended_cplu = total_budget / projected_lifted_users if projected_lifted_users > 0 else float("nan")

    current_lifted_users = (
        allocation_df["Current_Lifted_Users"].sum() if "Current_Lifted_Users" in allocation_df.columns else None
    )

    col1, col2, col3 = st.columns(3)
    col1.metric("Total Budget", format_currency(total_budget, 0))
    col2.metric("Projected Lifted Users", format_number(projected_lifted_users))
    col3.metric("Projected Blended CPLU", format_cplu(projected_blended_cplu))

    if current_lifted_users is not None and current_lifted_users > 0:
        uplift_pct = (projected_lifted_users - current_lifted_users) / current_lifted_users * 100
        st.metric(
            "Projected vs Current Lifted Users (same included combos)",
            format_number(projected_lifted_users),
            delta=f"{uplift_pct:+.1f}% vs current ({format_number(current_lifted_users)})",
        )

    st.divider()

    # --- Charts -------------------------------------------------------------
    tab1, tab2 = st.tabs(["Spend Allocation", "Lifted Users Impact"])
    with tab1:
        st.plotly_chart(plot_allocation_comparison(allocation_df), use_container_width=True)
    with tab2:
        st.plotly_chart(plot_lifted_users_comparison(allocation_df), use_container_width=True)

    st.divider()

    # --- Table -------------------------------------------------------------
    st.subheader("Recommended Allocation")
    display_df = allocation_df.copy().sort_values("Recommended_Spend", ascending=False)
    display_df["CPLU"] = display_df["CPLU"].apply(format_cplu)
    display_df["Recommended_Spend"] = display_df["Recommended_Spend"].apply(lambda v: format_currency(v, 0))
    display_df["Projected_Lifted_Users"] = display_df["Projected_Lifted_Users"].apply(format_number)
    if "Current_Spend" in display_df.columns:
        display_df["Current_Spend"] = display_df["Current_Spend"].apply(lambda v: format_currency(v, 0))
    if "Current_Lifted_Users" in display_df.columns:
        display_df["Current_Lifted_Users"] = display_df["Current_Lifted_Users"].apply(format_number)

    columns_to_show = [
        c for c in [
            "Market", "Channel", "CPLU", "Current_Spend", "Recommended_Spend",
            "Current_Lifted_Users", "Projected_Lifted_Users",
        ] if c in display_df.columns
    ]
    st.dataframe(
        display_df[columns_to_show].rename(columns={
            "Current_Spend": "Current Spend",
            "Recommended_Spend": "Recommended Spend",
            "Current_Lifted_Users": "Current Lifted Users",
            "Projected_Lifted_Users": "Projected Lifted Users",
        }),
        use_container_width=True,
        hide_index=True,
    )
