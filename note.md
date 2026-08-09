print(f"{'Campaign_Name'} | {'Market':<10} | {'Channel':<10} | {'P-Value':<12} | {'Significant?'}")
print("-" * 55)

# 2. Iterate through each row of the CSV
for index, row in df.iterrows():
    # Pull values for the current row
    counts = [row['Exposed_Consideration'], row['Control_Consideration']]
    nobs = [row['Exposed_Responses'], row['Control_Responses']]

    # 3. Calculate p-value for this specific row
    stat, pval = proportions_ztest(counts, nobs)

    # 4. Determine if it's significant (using 0.05 threshold)
    is_significant = "YES" if pval < 0.05 else "No"

    # 5. Print the result for this row
    campaign_name = row['Campaign_Name']
    market = row['Market']
    channel = row['Channel']
    print(f"{campaign_name} | {market:<10} | {channel:<10} | {pval:<12.4e} | {is_significant}")
    
### Dashboard

An interactive marketing intelligence tool that lets users explore campaign effectiveness, market/channel efficiency, creative performance, and statistically significant brand lift, then translates those findings into actionable recommendations for Gemini's marketing strategy.

The basic purpose would be:

Help a marketing team understand which campaigns, markets, channels, and creatives are driving the strongest brand impact, how efficiently that impact is being generated, and where marketing strategy could be improved.

The dashboard structure

I'd probably have 5 main pages:

1. 🏠 Executive Overview

This is the "tell me what is happening" page.

It would show KPI cards such as:

Total campaign spend
Total reach
Number of campaigns with brand-lift measurements
Significant campaigns
Estimated lifted users
Average/median CPLU

Then a few high-level visuals:

Top-performing campaigns
Most efficient campaigns
Spend vs estimated impact
Overall channel performance

And most importantly, a small Key Insights / Recommendations section.

For example:

🟢 YouTube generated strong lift at relatively low cost in several markets.
🔴 Search had high targeting costs but limited measured brand lift.
🟢 Life Hack was the strongest-performing creative concept overall.

So someone could open the dashboard and understand the main story in ~30 seconds.

2. 📊 Campaign Performance

This page focuses specifically on:

Which campaigns worked?

Features:

Campaign ranking table
Relative lift
Absolute lift
p-value
Statistical significance
Estimated lifted users
CPLU
Spend
Reach

And interactive filters:

Market:      All / UK / DE / SA / EG
Channel:     All / YouTube / Social / Display / Search
Significant: All / Significant only

I'd also have a Lift vs CPLU scatter plot.

This would be one of the most useful visuals because it separates:

High lift + Low CPLU       → ⭐ Best performers
High lift + High CPLU      → Effective but expensive
Low lift + Low CPLU        → Efficient but limited
Low lift + High CPLU       → ⚠️ Poor performers
3. 🌍 Market & Channel

This page answers:

Where should Gemini focus its marketing efforts?

You could show:

Performance by market
Performance by channel
Market × channel heatmap
CPLU by market/channel
CPR / relative targeting cost
Spend distribution
Reach distribution

For example, a user could select:

Market: UK

and immediately see how:

YouTube
Social
Display
Search

compare within the UK.

Or select:

Channel: YouTube

and compare UK vs Germany vs Saudi Arabia vs Egypt.

This makes the dashboard interactive rather than just a report.

4. 🎨 Creative Intelligence

This would be one of the more distinctive pages.

It answers:

What type of creative should Gemini use, and where?

You already have the data for:

Global creative performance
Creative × market
Creative × channel

So I'd have:

Creative leaderboard

Creative       Avg Consideration Lift
Life Hack              5.51
Coding Help            3.08
Study Buddy            ...
Grade Calculator       ...
Free Trial             1.07

Then a Creative × Market heatmap.

And potentially:

Creative × Channel

This lets someone discover something more useful than simply:

"Life Hack is the best creative."

Instead:

"Life Hack performs particularly well in these markets/channels, while another creative may be more suitable elsewhere."

That leads directly into your recommendations.

5. 💡 Recommendations / Strategy

This is the page that makes the project feel more like a real business intelligence product.

Instead of making the marketing team interpret all the charts themselves, your analysis produces evidence-backed recommendations.

For example:

Campaign Strategy

Prioritise campaigns demonstrating both statistically significant lift and strong CPLU efficiency.

Channel Strategy

Investigate channels with high targeting costs but limited measured brand impact.

Creative Strategy

Life Hack demonstrates the strongest overall consideration performance, but creative selection should be adapted according to market-level performance.

Market Strategy

Allocate greater attention to market/channel combinations demonstrating consistently strong lift and efficiency.

And each recommendation could have a little:

"Why?"

button/section showing the underlying evidence.



1. Final project structure

I recommend this:

gemini-marketing-dashboard/
│
├── app.py
│
├── data/
│   ├── raw/
│   │   ├── Brand Lift Study Results - Sheet1.csv
│   │   ├── Historic Campaign Data - Sheet1.csv
│   │   └── Creative Performance Report - Sheet1.csv
│   │
│   └── processed/
│       ├── processed_campaign_analysis.csv
│       ├── market_channel_analysis.csv
│       └── creative_market_performance.csv
│
├── pages/
│   ├── overview.py
│   ├── campaigns.py
│   ├── markets_channels.py
│   ├── creative.py
│   └── recommendations.py
│
├── utils/
│   ├── data_loader.py
│   ├── filters.py
│   └── formatting.py
│
├── charts/
│   ├── campaign_charts.py
│   ├── market_channel_charts.py
│   └── creative_charts.py
│
├── assets/
│
├── requirements.txt
└── README.md

2. Which CSV goes where?

This is the key mapping.

CSV	Main purpose	Dashboard pages
processed_campaign_analysis.csv	Campaign performance, lift, significance, efficiency	Overview + Campaigns
market_channel_analysis.csv	Market/channel efficiency and targeting cost	Overview + Markets & Channels
creative_market_performance.csv	Creative performance by market	Overview + Creative
Raw 3 CSVs	Original data / reproducibility	Not directly used by dashboard

So:

processed_campaign_analysis.csv
             │
             ├── Overview
             └── Campaign Performance


market_channel_analysis.csv
             │
             ├── Overview
             └── Markets & Channels


creative_market_performance.csv
             │
             ├── Overview
             └── Creative Performance

The raw CSVs are kept because they document where your analysis came from, but the dashboard doesn't need to load them.

3. app.py
Purpose

This is the main entry point.

Run:

streamlit run app.py
Functions/logic

I'd have:

main()

and it should:

Configure Streamlit
Load the three processed datasets
Create the sidebar/global navigation
Display the selected page

Conceptually:

app.py
│
├── Load data
│
├── Sidebar
│
└── Navigation
     ├── Overview
     ├── Campaigns
     ├── Markets & Channels
     ├── Creative
     └── Recommendations

Keep app.py relatively small.

4. utils/data_loader.py

This handles only loading the CSVs.

CSVs used

All three processed CSVs.

Functions
load_campaign_data()
load_market_channel_data()
load_creative_data()

I'd also add:

load_all_data()

which returns all three.

For example:

def load_campaign_data():
    return pd.read_csv(
        "data/processed/processed_campaign_analysis.csv"
    )

And ideally use Streamlit's caching:

@st.cache_data

so the CSV isn't repeatedly loaded every time the user changes a filter.

5. utils/filters.py

This handles the dashboard's interactive filtering.

Mainly uses

processed_campaign_analysis.csv

because that's your main detailed dataset.

Functions
get_filter_options()
apply_campaign_filters()

You could have global filters for:

Market
Channel
Campaign
Statistical significance

Potentially date as well, if the dashboard needs time analysis.

For example:

filtered_df = apply_campaign_filters(
    campaign_df,
    selected_market,
    selected_channel,
    selected_campaign,
    selected_significance
)

The important thing is that you don't copy filtering code into every page.

6. utils/formatting.py

This is purely for making numbers look professional.

Functions
format_currency()
format_percentage()
format_number()
format_cplu()
format_cpr()

For example:

0.153423

becomes:

$0.15

and:

103.9321

becomes:

103.93%

This is a small file, but it makes the dashboard much cleaner.

7. charts/campaign_charts.py
CSV
processed_campaign_analysis.csv
Functions

I'd implement:

plot_campaign_lift()
plot_campaign_cplu()
plot_lift_vs_cplu()
plot_campaign_spend()
Most important:
plot_lift_vs_cplu()

This should be one of your main dashboard charts.

Conceptually:

                    HIGH LIFT
                       ↑
                       │
              ●        │      ●
                       │
                       │
 LOW CPLU ─────────────┼──────────── HIGH CPLU
                       │
                ●      │
                       │
                       ↓
                    LOW LIFT

This allows the user to identify campaigns that are:

highly effective
highly efficient
effective but expensive
weak and expensive

That's much more useful than simply showing a bar chart of campaign lift.

8. charts/market_channel_charts.py
CSV
market_channel_analysis.csv

Your notebook already groups by:

Market
Channel

and calculates:

Spend
Lifted Users
CPLU
Reach
CPR
Relative Cost Index
Functions
plot_market_cplu()
plot_channel_cplu()
plot_market_channel_heatmap()
plot_cpr_comparison()
plot_relative_cost_index()
Main chart

I'd make:

Market × Channel heatmap

               YouTube   Social   Display   Search
UK               ●        ●         ●        ●
DE               ●        ●         ●        ●
SA               ●        ●         ●        ●
EG               ●        ●         ●        ●

The metric could be CPLU.

Lower CPLU = more efficient.

This directly represents one of the major analyses you've already performed. Your original analysis identified SA + YouTube as the most efficient combination with a CPLU of about $0.45.

9. charts/creative_charts.py
CSV
creative_market_performance.csv
Functions
plot_creative_ranking()
plot_creative_market_heatmap()

Potentially:

plot_creative_channel()

only if your processed CSV contains the required channel-level information.

Your analysis already evaluates creative performance globally and by market, and your source analysis found Life Hack to be the strongest global creative.

10. pages/overview.py

This is the main landing page.

CSVs

All three:

processed_campaign_analysis.csv
market_channel_analysis.csv
creative_market_performance.csv
Purpose

Answer:

"What are the most important things I need to know about Gemini's marketing performance?"

Section 1 — KPI cards

Something like:

┌────────────────┐ ┌────────────────┐ ┌────────────────┐
│ Total Spend    │ │ Total Reach    │ │ Lifted Users   │
│    $XXX,XXX    │ │    XXX,XXX     │ │    XXX,XXX     │
└────────────────┘ └────────────────┘ └────────────────┘

┌────────────────┐ ┌────────────────┐
│ Significant    │ │ Average CPLU   │
│ Campaigns      │ │     $X.XX      │
└────────────────┘ └────────────────┘
Section 2 — Top campaigns

Use:

processed_campaign_analysis.csv

Show:

Highest relative lift
Most efficient campaign
Significant campaigns

Your analysis identifies BackToSchool_24 / SA / YouTube as the highest-lift significant campaign and ExamPrep_23 / SA / YouTube as the most efficient campaign.

Section 3 — Market/channel

Use:

market_channel_analysis.csv

Show the strongest market/channel combination.

Section 4 — Creative

Use:

creative_market_performance.csv

Show the strongest creative.

Section 5 — Key insights

This could contain 3–4 cards:

Highest Impact
BackToSchool_24 — SA — YouTube

Most Efficient
ExamPrep_23 — SA — YouTube

Strongest Creative
Life Hack

Strongest Creative Channel
YouTube

Your analysis supports these findings.

11. pages/campaigns.py
CSV
processed_campaign_analysis.csv
Purpose

Answer:

Which campaigns worked best?

Sections
KPI cards
Highest Relative Lift
Lowest CPLU
Number of Significant Campaigns
Total Estimated Lifted Users
Charts
plot_campaign_lift()
plot_campaign_cplu()
plot_lift_vs_cplu()
Campaign table

Columns could be:

Campaign
Market
Channel
Relative Lift
Absolute Lift
p-value
Significant?
Lifted Users
CPLU
Spend
Reach

This is where users can really investigate individual campaigns.

12. pages/markets_channels.py
CSV
market_channel_analysis.csv
Purpose

Answer:

Where should Gemini focus its marketing?

Sections
Market performance

Compare:

UK
DE
SA
EG
Channel performance

Compare:

YouTube
Social
Display
Search
Market × Channel heatmap

Main visual.

Cost analysis

Show:

CPLU
CPR
Relative Cost Index

Your notebook defines Relative Cost Index as:

100 = average
>100 = more expensive
<100 = cheaper

You can actually put that explanation directly underneath the chart.

13. pages/creative.py
CSV
creative_market_performance.csv
Purpose

Answer:

What creative should Gemini use, and where?

Sections
Global creative ranking
Life Hack
Coding Help
Study Buddy
Grade Calculator
Free Trial
Creative × Market heatmap

This is probably the most interesting chart on this page.

Your analysis found that Life Hack performs particularly well in DE and UK, while Coding Help performs relatively well in EG and SA.

So the dashboard could make that immediately visible.

14. pages/recommendations.py

This page doesn't really need a new CSV.

It uses the findings from all three processed datasets.

Its purpose is:

Turn the analysis into decisions.

I'd divide it into four recommendation cards.

Campaign strategy

Prioritise campaigns that combine strong statistically significant lift with strong CPLU efficiency.

Channel strategy

YouTube and Social showed the strongest creative consideration performance, with YouTube at 4.53 and Social at 4.49.

Creative strategy

Adapt creatives by market rather than using one creative globally.

Cost strategy

Investigate expensive channels such as Search before increasing investment. Your analysis found Search CPR around $0.09 versus Display around $0.019.

15. What about the raw CSVs?

Keep them:

data/raw/
├── Brand Lift Study Results - Sheet1.csv
├── Historic Campaign Data - Sheet1.csv
└── Creative Performance Report - Sheet1.csv

But none of the dashboard files need to load them.

Their purpose is documentation/reproducibility.

Your workflow is:

RAW CSVs
   ↓
JUPYTER NOTEBOOK
   ↓
ANALYSIS
   ↓
3 PROCESSED CSVs
   ↓
STREAMLIT DASHBOARD

That's a perfectly reasonable data-science project architecture.

16. Complete file/function map

Here's the version I'd actually use while building:

| File                              | Main CSV       | Functions                                                                                                                           |
| --------------------------------- | -------------- | ----------------------------------------------------------------------------------------------------------------------------------- |
| `app.py`                          | All processed  | `main()` / navigation                                                                                                               |
| `utils/data_loader.py`            | All 3          | `load_campaign_data()`, `load_market_channel_data()`, `load_creative_data()`                                                        |
| `utils/filters.py`                | Campaign       | `get_filter_options()`, `apply_campaign_filters()`                                                                                  |
| `utils/formatting.py`             | None           | `format_currency()`, `format_percentage()`, `format_number()`, `format_cplu()`                                                      |
| `charts/campaign_charts.py`       | Campaign       | `plot_campaign_lift()`, `plot_campaign_cplu()`, `plot_lift_vs_cplu()`, `plot_campaign_spend()`                                      |
| `charts/market_channel_charts.py` | Market/channel | `plot_market_cplu()`, `plot_channel_cplu()`, `plot_market_channel_heatmap()`, `plot_cpr_comparison()`, `plot_relative_cost_index()` |
| `charts/creative_charts.py`       | Creative       | `plot_creative_ranking()`, `plot_creative_market_heatmap()`                                                                         |
| `pages/overview.py`               | **All 3**      | `show_overview()`                                                                                                                   |
| `pages/campaigns.py`              | Campaign       | `show_campaigns()`                                                                                                                  |
| `pages/markets_channels.py`       | Market/channel | `show_markets_channels()`                                                                                                           |
| `pages/creative.py`               | Creative       | `show_creative()`                                                                                                                   |
| `pages/recommendations.py`        | **All 3**      | `show_recommendations()`                                                                                                            |
┌──────────────────────────────────────────────────────────┐
│             GEMINI MARKETING INTELLIGENCE                │
├──────────────────────────────────────────────────────────┤
│                                                          │
│  Overview                                             │
│  Campaign Performance                                 │
│  Markets & Channels                                   │
│  Creative Intelligence                                │
│  Recommendations                                      │
│                                                          │
└──────────────────────────────────────────────────────────┘

With filters in the sidebar, particularly on the Campaign and Market/Channel pages.