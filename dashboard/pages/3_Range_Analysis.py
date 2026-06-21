"""
Page: Range Analysis
'Average Range by Segment' replaced with 'Average Range by Price Tier'
since Segment doesn't exist in this dataset.
"""

import streamlit as st
import matplotlib.pyplot as plt
import seaborn as sns
from utils import load_data

st.set_page_config(page_title="Range Analysis", page_icon="🔋", layout="wide")

df = load_data()

st.title("🔋 Range Analysis")
st.markdown("Which vehicles go the farthest, and what drives range?")
st.divider()

# ------------------------------------------------------------------
# Top EVs by Range
# ------------------------------------------------------------------
st.subheader("Top EVs by Range")

top_n = st.slider("Number of vehicles to show", min_value=5, max_value=20, value=10)
top_range = df.nlargest(top_n, 'Range')[['Brand', 'Model', 'Range', 'Price', 'PriceTier']]

fig, ax = plt.subplots(figsize=(10, max(4, top_n * 0.35)))
labels = top_range['Model']  # Model already includes the brand name in this dataset
ax.barh(labels[::-1], top_range['Range'][::-1], color='#2E86AB')
ax.set_xlabel("Range (km)")
st.pyplot(fig)

with st.expander("View underlying data"):
    st.dataframe(top_range, use_container_width=True)

st.divider()

# ------------------------------------------------------------------
# Range distribution + Average range by price tier
# ------------------------------------------------------------------
col1, col2 = st.columns(2)

with col1:
    st.subheader("Range Distribution")
    fig, ax = plt.subplots(figsize=(7, 5))
    sns.histplot(df['Range'], kde=True, bins=20, ax=ax, color='#2E86AB')
    ax.axvline(df['Range'].mean(), color='red', linestyle='--', label='Mean')
    ax.axvline(df['Range'].median(), color='green', linestyle='--', label='Median')
    ax.set_xlabel("Range (km)")
    ax.legend()
    st.pyplot(fig)

with col2:
    st.subheader("Average Range by Price Tier")
    tier_order = ['Budget', 'Mid-Range', 'Premium', 'Luxury']
    existing_tiers = [t for t in tier_order if t in df['PriceTier'].unique()]
    tier_range = df.groupby('PriceTier')['Range'].mean().reindex(existing_tiers)
    fig, ax = plt.subplots(figsize=(7, 5))
    sns.barplot(x=tier_range.index, y=tier_range.values, ax=ax, palette='crest')
    ax.set_ylabel("Average Range (km)")
    st.pyplot(fig)

st.divider()

# ------------------------------------------------------------------
# Range vs Efficiency scatter
# ------------------------------------------------------------------
st.subheader("Range vs. Efficiency")
fig, ax = plt.subplots(figsize=(12, 6))
sns.scatterplot(
    data=df, x='Efficiency', y='Range',
    hue='PriceTier', s=80, alpha=0.75, palette='viridis', ax=ax
)
ax.set_xlabel("Efficiency (Wh/km) — lower is more efficient")
ax.set_ylabel("Range (km)")
ax.legend(bbox_to_anchor=(1.02, 1), loc='upper left', fontsize=8)
st.pyplot(fig)

st.divider()

# ------------------------------------------------------------------
# BONUS: Range per kWh of battery — a metric the original design
# didn't have access to, since the classic dataset had no Battery
# column. This dataset does, so it's worth surfacing.
# ------------------------------------------------------------------
st.subheader("Range per kWh of Battery (efficiency by capacity)")
df_temp = df.copy()
df_temp['Range_per_kWh'] = df_temp['Range'] / df_temp['Battery']

fig, ax = plt.subplots(figsize=(12, 5))
sns.scatterplot(data=df_temp, x='Battery', y='Range_per_kWh', hue='PriceTier', s=60, alpha=0.75, ax=ax)
ax.set_xlabel("Battery Capacity (kWh)")
ax.set_ylabel("Range per kWh (km/kWh)")
st.pyplot(fig)
st.caption(
    "Higher values indicate a vehicle extracts more range per unit of battery "
    "capacity — a complementary efficiency lens to Wh/km."
)
