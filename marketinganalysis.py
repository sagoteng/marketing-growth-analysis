import pandas as pd


# -----------------------------
# 1. LOAD DATA
# -----------------------------
df = pd.read_csv("ecommerce_marketing_growth_2025.csv")

print(df.head())

# -----------------------------
# PART 1 - Spending
# -----------------------------

# -----------------------------
# 2. TOTAL MARKETING SPEND
# -----------------------------
# Calculate total acquisition spend across all channels in 2025
total_spend = df["spend"].sum()

print("\nTotal Marketing Spend in 2025:")
print(total_spend)

# -----------------------------
# 3. SPEND BY CHANNEL
# -----------------------------
# Measure how much budget each acquisition channel consumed in 2025
spend_by_channel = df.groupby("channel")["spend"].sum()

print("\nSpend by Channel:")
print(spend_by_channel)

# -----------------------------
# 4. SPEND SHARE (%)
# -----------------------------
# Measure each channel's share of total acquisition spend
spend_share = (df.groupby("channel")["spend"].sum() / total_spend) * 100

print("\nSpend Share by Channel (%):")
print(spend_share)

# -----------------------------
# 5. MONTHLY SPEND TREND
# -----------------------------
# Track how budget allocation evolved month by month across channels
df["date"] = pd.to_datetime(df["date"])
df["month"] = df["date"].dt.to_period("M")

monthly_spend = df.groupby(["month", "channel"])["spend"].sum()

print("\nMonthly Spend Trend:")
print(monthly_spend)

# -----------------------------
# PART 2 - REVENUE CONTRIBUTION
# -----------------------------

# -----------------------------
# 6. TOTAL REVENUE
# -----------------------------
# Measure total revenue generated across all acquisition channels in 2025
total_revenue = df["revenue"].sum()

print("\nTotal Revenue in 2025:")
print(total_revenue)


# -----------------------------
# 7. REVENUE BY CHANNEL
# -----------------------------
# Measure how much revenue each acquisition channel generated in 2025
revenue_by_channel = df.groupby("channel")["revenue"].sum()

print("\nRevenue by Channel:")
print(revenue_by_channel)


# -----------------------------
# 8. REVENUE SHARE (%)
# -----------------------------
# Measure each channel's share of total revenue
revenue_share = (df.groupby("channel")["revenue"].sum() / total_revenue) * 100

print("\nRevenue Share by Channel (%):")
print(revenue_share)


# -----------------------------
# 9. SPEND VS REVENUE SHARE
# -----------------------------
# Compare budget allocation vs revenue contribution by channel
channel_efficiency = pd.DataFrame({
    "spend_share_pct": spend_share,
    "revenue_share_pct": revenue_share
})

print("\nSpend Share vs Revenue Share:")
print(channel_efficiency)

# -----------------------------
# PART 3 - EFFICIENCY & PROFITABILITY
# -----------------------------

# -----------------------------
# 10. ROAS BY CHANNEL
# -----------------------------
# Measure return on ad spend for each acquisition channel
roas_by_channel = df.groupby("channel")["revenue"].sum() / df.groupby("channel")["spend"].sum()

print("\nROAS by Channel:")
print(roas_by_channel)


# -----------------------------
# 11. CAC BY CHANNEL
# -----------------------------
# Measure customer acquisition cost by channel
cac_by_channel = df.groupby("channel")["spend"].sum() / df.groupby("channel")["conversions"].sum()

print("\nCAC by Channel:")
print(cac_by_channel)


# -----------------------------
# 12. CPC BY CHANNEL
# -----------------------------
# Measure cost per click by channel
cpc_by_channel = df.groupby("channel")["spend"].sum() / df.groupby("channel")["clicks"].sum()

print("\nCPC by Channel:")
print(cpc_by_channel)


# -----------------------------
# 13. CVR BY CHANNEL
# -----------------------------
# Measure conversion rate from sessions to conversions
cvr_by_channel = df.groupby("channel")["conversions"].sum() / df.groupby("channel")["sessions"].sum()

print("\nCVR by Channel:")
print(cvr_by_channel)


# -----------------------------
# 14. REVENUE PER SESSION
# -----------------------------
# Measure monetization efficiency per session
revenue_per_session = df.groupby("channel")["revenue"].sum() / df.groupby("channel")["sessions"].sum()

print("\nRevenue per Session:")
print(revenue_per_session)

# -----------------------------
# PART 4 - SCALING OPPORTUNITIES
# -----------------------------

# -----------------------------
# 15. CHANNEL PERFORMANCE SUMMARY
# -----------------------------
# Consolidate core efficiency metrics into one comparison table
channel_summary = pd.DataFrame({
    "spend": df.groupby("channel")["spend"].sum(),
    "revenue": df.groupby("channel")["revenue"].sum(),
    "spend_share_pct": spend_share,
    "revenue_share_pct": revenue_share,
    "roas": roas_by_channel,
    "cac": cac_by_channel,
    "cpc": cpc_by_channel,
    "cvr": cvr_by_channel,
    "revenue_per_session": revenue_per_session
})

print("\nChannel Performance Summary:")
print(channel_summary)


# -----------------------------
# 16. EFFICIENCY GAP
# -----------------------------
# Compare revenue share vs spend share to identify over- and under-funded channels
channel_summary["efficiency_gap"] = channel_summary["revenue_share_pct"] - channel_summary["spend_share_pct"]

print("\nEfficiency Gap (Revenue Share - Spend Share):")
print(channel_summary["efficiency_gap"])


# -----------------------------
# 17. SCALING PRIORITY RANKING
# -----------------------------
# Rank channels by scaling attractiveness based on efficiency gap
scaling_priority = channel_summary.sort_values("efficiency_gap", ascending=False)

print("\nScaling Priority Ranking:")
print(scaling_priority[["spend_share_pct", "revenue_share_pct", "efficiency_gap", "roas", "cac"]])
