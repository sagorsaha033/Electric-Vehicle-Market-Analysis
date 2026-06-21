"""
Page: Brand Analysis
Uses 'Model' (which is Car_name, e.g. "Tesla Model Y Long Range Dual
Motor") since there's no separate Model column distinct from Brand
in this dataset.
"""

import streamlit as st
import matplotlib.pyplot as plt
from utils import load_data

st.set_page_config(page_title="Brand Analysis", page_icon="🏷️", layout="wide")

df = load_data()

st.title("🏷️ Brand Analysis")
st.markdown("Compare model count, pricing, and range across EV manufacturers.")

# ------------------------------------------------------------------
# SIDEBAR FILTER
# ------------------------------------------------------------------
st.sidebar.header("Filters")
all_brands = sorted(df['Brand'].unique())
selected_brands = st.sidebar.multiselect(
    "Select Brand(s)",
    options=all_brands,
    default=all_brands
)

filtered_df = df[df['Brand'].isin(selected_brands)]

if filtered_df.empty:
    st.warning("No brands selected. Please choose at least one brand from the sidebar.")
    st.stop()

st.divider()

# ------------------------------------------------------------------
# Top brands by model count
# With 360 rows across many brands, we show the top 20 for readability
# rather than every brand crammed onto one axis.
# ------------------------------------------------------------------
st.subheader("Models per Brand (Top 20)")
brand_counts = filtered_df['Brand'].value_counts().head(20).sort_values(ascending=True)

fig, ax = plt.subplots(figsize=(10, max(4, len(brand_counts) * 0.3)))
ax.barh(brand_counts.index, brand_counts.values, color='#2E86AB')
ax.set_xlabel("Number of Models")
st.pyplot(fig)

st.divider()

# ------------------------------------------------------------------
# Avg Price and Avg Range, restricted to brands with a minimum number
# of models — averaging a brand with only 1 listing is unstable and
# can mislead the chart (see Phase 7 notes on this exact issue).
# ------------------------------------------------------------------
min_models = st.slider("Minimum models per brand to include in averages", 1, 10, 3)
brand_model_counts = filtered_df['Brand'].value_counts()
qualifying_brands = brand_model_counts[brand_model_counts >= min_models].index
stable_df = filtered_df[filtered_df['Brand'].isin(qualifying_brands)]

col1, col2 = st.columns(2)

with col1:
    st.subheader("Average Price by Brand")
    avg_price = stable_df.groupby('Brand')['Price'].mean().sort_values(ascending=True).tail(20)
    fig, ax = plt.subplots(figsize=(7, max(4, len(avg_price) * 0.3)))
    ax.barh(avg_price.index, avg_price.values, color='#A23B72')
    ax.set_xlabel("Average Price (€)")
    st.pyplot(fig)

with col2:
    st.subheader("Average Range by Brand")
    avg_range = stable_df.groupby('Brand')['Range'].mean().sort_values(ascending=True).tail(20)
    fig, ax = plt.subplots(figsize=(7, max(4, len(avg_range) * 0.3)))
    ax.barh(avg_range.index, avg_range.values, color='#F18F01')
    ax.set_xlabel("Average Range (km)")
    st.pyplot(fig)

st.divider()

# ------------------------------------------------------------------
# Comparison table
# ------------------------------------------------------------------
st.subheader("Brand Comparison Table")

comparison = filtered_df.groupby('Brand').agg(
    Total_Models=('Model', 'count'),
    Avg_Price=('Price', 'mean'),
    Avg_Range=('Range', 'mean'),
    Avg_Efficiency=('Efficiency', 'mean')
).round(0).sort_values('Total_Models', ascending=False)

st.dataframe(comparison, use_container_width=True)
