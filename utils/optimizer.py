"""
Budget allocation heuristic: given a total budget, recommend how to split
spend across Market x Channel combinations to maximise projected lifted
users, using each combination's historical CPLU as its efficiency score.

IMPORTANT ASSUMPTION: this treats CPLU as constant regardless of how much
is spent on a combination (i.e. no diminishing returns curve). We don't
have the underlying spend-response data to fit a real marginal-cost curve,
so a pure "put everything into the cheapest CPLU" allocation would be
unrealistic. To keep the recommendation sane, `max_share_per_combo` caps
how much of the total budget any single combination can receive. Treat the
output as directional guidance, not a guaranteed result.
"""

import pandas as pd


def optimize_allocation(
    df: pd.DataFrame,
    total_budget: float,
    max_share_per_combo: float = 0.35,
) -> tuple[pd.DataFrame, bool]:
    """
    df: market_channel_analysis dataframe, filtered to the combos to
        consider, with at least Market, Channel, CPLU columns (Spend and
        Lifted_Users are used for the "current" comparison if present).
    total_budget: total $ to allocate across all combos.
    max_share_per_combo: max fraction (0-1) of total_budget any single
        combo can receive in the first pass.

    Returns (allocation_df, leftover_was_relaxed).
    leftover_was_relaxed is True if the cap was too restrictive to spend
    the full budget and the remainder had to be distributed without the
    cap (still efficiency-weighted).
    """
    work = df.copy()
    work = work[work["CPLU"].notna() & (work["CPLU"] > 0)].reset_index(drop=True)

    if work.empty:
        raise ValueError(
            "No Market/Channel combinations have a usable (positive) CPLU to optimise on."
        )

    work = work.sort_values("CPLU", ascending=True).reset_index(drop=True)
    cap = total_budget * max_share_per_combo

    allocation = pd.Series(0.0, index=work.index)
    remaining = total_budget

    # Waterfall pass: cheapest CPLU first, capped per combo
    for i in work.index:
        if remaining <= 1e-9:
            break
        take = min(cap, remaining)
        allocation[i] = take
        remaining -= take

    leftover_relaxed = remaining > 1e-6
    if leftover_relaxed:
        # Cap was too tight to spend the full budget -- distribute the
        # remainder efficiency-weighted (inverse CPLU), ignoring the cap.
        weights = 1 / work["CPLU"]
        weights = weights / weights.sum()
        allocation = allocation + weights * remaining

    work["Recommended_Spend"] = allocation
    work["Projected_Lifted_Users"] = work["Recommended_Spend"] / work["CPLU"]

    rename_map = {}
    if "Spend" in work.columns:
        rename_map["Spend"] = "Current_Spend"
    if "Lifted_Users" in work.columns:
        rename_map["Lifted_Users"] = "Current_Lifted_Users"
    work = work.rename(columns=rename_map)

    return work, leftover_relaxed
