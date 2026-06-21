"""
Electric Vehicle Market Analysis — Streamlit Dashboard
Home Page: Executive Summary

Rewritten to match the actual dataset schema (360 EVs, ev-database.org
style columns) rather than the original ~103-row ElectricCarData.csv schema.
"""

import streamlit as st
import matplotlib.pyplot as plt
import seaborn as sns
from utils import load_data

st.set_page_config(
    page_title="EV Market Analysis | Executive Summary",
    page_icon="⚡",
    layout="wide"
)

df = load_data()

# ------------------------------------------------------------------
# HEADER
# ------------------------------------------------------------------
st.title("⚡ Electric Vehicle Market Analysis")
st.markdown(
    "An interactive exploration of EV pricing, range, charging performance, "
    "and brand positioning across the current market."
)
st.divider()

# ------------------------------------------------------------------
# KPI ROW
# Note: no 'Fast Charge Adoption %' card removed — we kept it, since
# ChargingTier does exist in this dataset.
# ------------------------------------------------------------------
st.subheader("Market at a Glance")

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric("Total Models", f"{len(df)}")

with col2:
    st.metric("Average Price", f"€{df['Price'].mean():,.0f}")

with col3:
    st.metric("Average Range", f"{df['Range'].mean():.0f} km")

with col4:
    fast_charge_pct = (df['ChargingTier'] == 'Fast').mean() * 100
    st.metric("Fast Charge Adoption", f"{fast_charge_pct:.1f}%")

st.divider()

# ------------------------------------------------------------------
# CHARTS ROW
# Segment-based pie chart removed (no Segment column in this dataset).
# Replaced with Price Tier (which does exist) and Brand concentration,
# which is a more relevant "market structure" view for this data anyway.
# ------------------------------------------------------------------
left_col, right_col = st.columns(2)

with left_col:
    st.subheader("Models by Price Tier")
    fig, ax = plt.subplots(figsize=(6, 4))
    tier_counts = df['PriceTier'].value_counts()
    sns.barplot(x=tier_counts.index, y=tier_counts.values, ax=ax, palette='viridis')
    ax.set_ylabel("Number of Models")
    ax.set_xlabel("")
    st.pyplot(fig)

with right_col:
    st.subheader("Top 10 Brands by Model Count")
    fig, ax = plt.subplots(figsize=(6, 4))
    brand_counts = df['Brand'].value_counts().head(10).sort_values(ascending=True)
    ax.barh(brand_counts.index, brand_counts.values, color='#2E86AB')
    ax.set_xlabel("Number of Models")
    st.pyplot(fig)

st.divider()

# ------------------------------------------------------------------
# KEY TAKEAWAY
# ------------------------------------------------------------------
st.info(
    "💡 **Key takeaway:** The EV market is priced primarily on range and "
    "performance, with fast charging remaining a premium feature rather "
    "than a market standard. See the **Key Insights** page for full findings."
)

# ------------------------------------------------------------------
# SIDEBAR
# ------------------------------------------------------------------
st.sidebar.title("⚡ EV Market Analysis")
st.sidebar.markdown("Navigate using the pages above.")
st.sidebar.divider()
st.sidebar.markdown("**Dataset:** ElectricCarData_clean.csv")
st.sidebar.markdown(f"**Records:** {len(df)} EV models")
