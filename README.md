# Marketing Growth Analysis
### Ecommerce Channel Performance & Predictive Budget Optimization

A marketing performance analysis project combining **descriptive analytics** and **AI-powered predictive modeling** to answer a core business question:

> *What should marketing do next to improve growth efficiency — and what is the revenue impact?*

---

## Project Overview

This project analyzes ecommerce marketing performance across paid, owned, and organic channels. It goes beyond reporting what happened — it uses machine learning to **simulate the revenue impact of a proposed budget reallocation**, providing data-driven recommendations to marketing leadership.

The analysis is structured in two layers:

| Layer | Type | Goal |
|---|---|---|
| **Descriptive Analysis** | `marketinganalysis.py` | Understand current channel performance |
| **Clustering (ML)** | `marketinganalysis_clustering.py` | Group channels by performance profile |
| **Predictive Modeling** | `marketinganalysis_predictive.py` | Forecast revenue impact of reallocation |

---

## Dataset

`ecommerce_marketing_growth_2025.csv` — Daily ecommerce marketing performance across acquisition channels.

| Column | Description |
|---|---|
| `date` | Daily granularity |
| `channel` | Acquisition channel (Meta, Google, Email, Affiliate, Organic) |
| `spend` | Marketing spend (€) |
| `revenue` | Revenue generated (€) |
| `clicks` | Clicks |
| `sessions` | Sessions |
| `conversions` | Conversions |

---

## Layer 1 — Descriptive Analysis

**File:** `marketinganalysis.py`

Evaluates channel efficiency across 4 dimensions:

- **Spend** — Budget distribution and monthly trends
- **Revenue** — Revenue contribution and share by channel
- **Efficiency** — ROAS, CAC, CPC, CVR, Revenue per Session
- **Scaling** — Efficiency gap (revenue share vs spend share) and priority ranking

---

## Layer 2 — K-Means Clustering (ML)

**File:** `marketinganalysis_clustering.py`

Uses **K-Means** (unsupervised machine learning) to automatically group channels by performance similarity — without any predefined labels. The algorithm answers: *"Which channels behave alike, and what does that tell us strategically?"*

### How it works

1. Builds a feature matrix of 6 efficiency metrics per channel (ROAS, CAC, CPC, CVR, Revenue per Session, Efficiency Gap)
2. Standardizes all metrics so no single metric dominates
3. Groups the 5 channels into 3 clusters: High / Mid / Low Efficiency
4. Uses PCA to reduce 6 dimensions to 2D for visualization

### Cluster Results

| Cluster | Channels | Strategic Action |
|---|---|---|
| 🟢 High Efficiency | Email | Scale budget |
| 🟡 Mid Efficiency | Google Ads, Affiliate, Organic Search | Optimize |
| 🔴 Low Efficiency | Meta Ads | Reduce or restructure |

> The clustering objectively confirms the budget reallocation recommendations using an ML approach — Email is underfunded, Meta is inefficient.

### Outputs

- `clustering_results.csv` — Cluster assignments and metrics per channel, ready for Power BI
- `clustering_by_channel.png` — PCA scatter plot + ROAS vs CAC bubble chart

---

## Layer 3 — Predictive Modeling (AI-Powered)

**File:** `marketinganalysis_predictive.py`

Uses **Meta Prophet** (time series forecasting) to simulate the revenue impact of a proposed budget reallocation over the next 12 months.

### How it works

1. Trains a Prophet model per channel on historical daily revenue
2. Applies a spend multiplier based on the proposed budget change
3. Forecasts revenue, spend, and ROAS over 365 days
4. Compares baseline vs reallocated scenario to quantify the uplift

### Budget Reallocation Scenario

| Channel | Current Spend | Proposed Spend | Change |
|---|---|---|---|
| Meta Ads | €260.9k | €180k | -€80.9k |
| Google Ads | €204.9k | €190k | -€14.9k |
| Affiliate | €65.4k | €35k | -€30.4k |
| Email | €19.8k | €90k | +€70.2k |
| Organic Search | €0 | €50k | +€50k |

### Outputs

- `forecast_reallocation.csv` — Full daily forecast per channel, ready for Power BI
- `forecast_reallocation_by_channel.png` — Forecast charts per channel + global total with 95% confidence intervals

---

## Key Insights

**1. Paid growth is too dependent on Meta**
Meta drives volume but CAC is rising and efficiency is declining — it is the primary candidate for budget reallocation.

**2. Email is the most efficient channel and is heavily underfunded**
With the strongest ROAS and lowest CAC, Email should be the first channel scaled.

**3. Google shows stronger intent and better paid efficiency**
More efficient than Meta and worth protecting in any reallocation scenario.

**4. Organic Search is a scalable, low-cost acquisition lever**
SEO and content investment can grow non-paid acquisition with strong long-term compounding.

**5. Affiliate quality is uneven**
Exposure to low-value partners is diluting efficiency — selective pruning is recommended.

---

## Recommendations

1. **Rebalance paid budget** — Reduce Meta dependency, reallocate toward Google and owned channels
2. **Scale Email / CRM** — Invest in lifecycle automation and audience segmentation
3. **Increase organic leverage** — SEO and content on high-intent pages
4. **Set paid guardrails** — Introduce CAC and ROAS thresholds on Meta
5. **Reassess affiliate partnerships** — Retain only placements delivering efficient incremental revenue

---

## Tools & Libraries

| Tool | Usage |
|---|---|
| Python | Core language |
| Pandas | Data manipulation |
| Scikit-learn | K-Means clustering & PCA |
| Meta Prophet | Time series forecasting |
| Matplotlib | Data visualization |
| VS Code | Development environment |

---

## Project Structure

```
marketing-growth-analysis/
│
├── ecommerce_marketing_growth_2025.csv   # Raw dataset
├── marketinganalysis.py                  # Layer 1 — Descriptive analysis
├── marketinganalysis_clustering.py       # Layer 2 — K-Means clustering
├── marketinganalysis_predictive.py       # Layer 3 — Predictive modeling
└── README.md
```
