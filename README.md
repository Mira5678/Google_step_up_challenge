# Gemini Marketing Intelligence Platform

An interactive marketing analytics platform for evaluating Gemini Pro campaigns and identifying opportunities to improve campaign efficiency, brand lift, and creative performance.

> **Note:** This is part of the Google Step Up Career Challenge — *Power Google's Gemini Pro Breakthrough!* — with further improvement and expansion of the project through additional data analysis in a Jupyter notebook and an interactive dashboard built with Streamlit.

## What it does

Three source datasets — a historic campaign performance log, a brand lift study, and a creative performance report — are cleaned, merged, and analysed in `insights.ipynb`. The notebook exports three processed CSVs, which the Streamlit app turns into an interactive dashboard for exploring what's working, where, and why, and for planning where budget should go next.

```
RAW CSVs  →  JUPYTER NOTEBOOK (analysis)  →  3 PROCESSED CSVs  →  STREAMLIT DASHBOARD
```

## User journey

**Overview → Campaigns → Markets & Channels → Creatives → Recommendations → Budget Optimisation**

| Page | Answers |
|---|---|
| **Overview** | What are the most important things to know about Gemini Pro's marketing performance, at a glance? |
| **Campaign Performance** | Which campaigns drove the strongest, most cost-efficient brand lift? |
| **Markets & Channels** | Where is spend working hardest, and where is it expensive? |
| **Creative Performance** | Which creative resonates best — globally, and market by market? |
| **Recommendations** | What should change, based on everything above? |
| **Budget Optimisation** | If I have $X to spend, how should it be split across markets and channels to maximise lifted users? |

## Data

| File | Grain | Key columns |
|---|---|---|
| `processed_campaign_analysis.csv` | Campaign × Market × Channel | `Relative_Lift`, `CPLU`, `CPR`, `is_significant`, `lifted_users` |
| `market_channel_analysis.csv` | Market × Channel | `Spend`, `Reach`, `Lifted_Users`, `CPLU`, `CPR`, `Relative_Cost_Index` |
| `creative_market_performance.csv` | Market × Creative | `Point_Est_Consideration` |

These live in `data/processed/`. The three raw source CSVs live in `data/raw/` for reference only — the dashboard never reads them directly.

## Project structure

```
gemini-marketing-dashboard/
│
├── app.py                     # entry point, sidebar navigation
│
├── data/
│   ├── raw/                   # original source CSVs (reference only)
│   └── processed/             # the 3 CSVs above — place your files here
│
├── pages/                     # one file per dashboard page
│   ├── overview.py
│   ├── campaigns.py
│   ├── markets_channels.py
│   ├── creative.py
│   ├── recommendations.py
│   └── budget_optimisation.py
│
├── charts/                    # Plotly chart builders, grouped by dataset
│   ├── campaign_charts.py
│   ├── market_channel_charts.py
│   └── creative_charts.py
│
├── utils/
│   ├── data_loader.py         # cached CSV loading
│   ├── filters.py             # sidebar filter widgets
│   ├── formatting.py          # currency / percentage / number formatting
│   └── optimizer.py           # budget allocation heuristic
│
├── assets/
├── requirements.txt
└── README.md
```

## Setup

```bash
pip install -r requirements.txt
```

## Run

```bash
streamlit run app.py
```

## Limitations to keep in mind

- **Budget Optimisation** assumes each Market × Channel combination's CPLU stays constant regardless of spend (no diminishing-returns curve is fitted, since the underlying spend-response data isn't available). Treat its output as directional guidance, not a guaranteed result — see the "How this works" expander on the page itself.
- **Creative Performance**'s global ranking is approximated by averaging `creative_market_performance.csv` across markets, since the notebook's true unweighted global average isn't currently exported separately.
- **Recommendations** blends figures computed from the processed CSVs with a couple of narrative findings from the notebook's exploratory analysis (e.g. channel-level creative resonance) that aren't in the exported CSVs yet — flagged in the page's own "Limitations" expander.