"""
Recommendations page. Turns the analysis into decisions.

Doesn't load a new CSV — draws on findings from all three processed
datasets, mixed with the narrative conclusions from the notebook
(some of which, like channel-level creative resonance, rely on figures
that aren't in the exported CSVs and are stated here as fixed findings).
"""

import streamlit as st

from utils.formatting import format_cplu, format_percentage


def show_recommendations(campaign_df, market_channel_df, creative_df):
    st.title("Recommendations")
    st.caption("Turning the analysis into decisions for Gemini Pro's next marketing push.")

    top_lift_row = campaign_df.loc[campaign_df["Relative_Lift"].idxmax()]
    top_cplu_row = campaign_df.dropna(subset=["CPLU"]).loc[campaign_df["CPLU"].idxmin()]
    top_creative = creative_df.groupby("Creative_Name")["Point_Est_Consideration"].mean().idxmax()
    cheapest_channel = market_channel_df.groupby("Channel")["CPR"].mean().idxmin()
    priciest_channel = market_channel_df.groupby("Channel")["CPR"].mean().idxmax()

    st.markdown("### 1. Prioritise campaigns that combine strong lift with cost efficiency")
    st.markdown(
        f"The highest statistically significant relative lift was **{top_lift_row['Campaign_Name']}** "
        f"in **{top_lift_row['Market']}** on **{top_lift_row['Channel']}** "
        f"({format_percentage(top_lift_row['Relative_Lift'])}). Separately, "
        f"**{top_cplu_row['Campaign_Name']}** in **{top_cplu_row['Market']}** on "
        f"**{top_cplu_row['Channel']}** was the most cost-efficient at {format_cplu(top_cplu_row['CPLU'])} "
        f"per lifted user. The campaign with the greatest impact isn't necessarily the cheapest one to "
        f"run — future budget should prioritise combinations that are both statistically significant "
        f"**and** cost-efficient, not just the highest-lift option in isolation."
    )

    st.divider()

    st.markdown("### 2. Prioritise high-consideration channels for brand-awareness objectives")
    st.markdown(
        f"Channel resonance and cost don't always move together. **{priciest_channel}** is the most "
        f"expensive channel to reach users on by cost-per-reach, while **{cheapest_channel}** is the "
        f"cheapest. Channels that combine strong creative consideration scores with reasonable cost "
        f"should be prioritised when the objective is increasing brand consideration; expensive "
        f"channels shouldn't be cut automatically, but their investment should be evaluated against "
        f"the specific objective they're meant to serve."
    )

    st.divider()

    st.markdown("### 3. Adapt creative strategy to individual markets")
    st.markdown(
        f"**{top_creative}** was the strongest-performing creative globally, but resonance varied by "
        f"market — the heatmap on the Creative Performance page shows which creative wins in each "
        f"market. A single global creative may not be optimal everywhere; consider testing the "
        f"top-performing local creative more heavily in markets where it outperforms the global winner."
    )

    st.divider()

    st.markdown("### 4. Evaluate channel investment using both cost and impact")
    st.markdown(
        f"There are substantial cost differences across channels — **{priciest_channel}** costs "
        f"considerably more per reached user than **{cheapest_channel}** in this analysis. Some "
        f"channel/market combinations didn't produce positive estimated lifted users at all. Channel "
        f"investment should be evaluated on both cost-to-reach and measurable brand impact, not reach "
        f"alone — see the Markets & Channels page for the full cost breakdown."
    )

    st.divider()

    with st.expander("Limitations"):
        st.markdown(
            "- Brand-lift measurements are available only for a subset of historical campaigns.\n"
            "- Brand-lift data is campaign-level, while historical performance data is weekly.\n"
            "- Lifted users are an estimated metric derived from reach and lift rate, not a direct "
            "measurement."
        )
