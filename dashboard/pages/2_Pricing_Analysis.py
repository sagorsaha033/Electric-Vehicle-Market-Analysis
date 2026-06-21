"""
Page: Pricing Analysis
Note: 'Segment' doesn't exist in this dataset, so the boxplot-by-segment
and scatter-colored-by-segment from the original design are replaced
with PriceTier (which does exist and serves a similar grouping purpose).
"""

import streamlit as st
import matplotlib.pyplot as plt
import seaborn as sns
from utils import load_data

st.set_page_config(page_title="Pricing Analysis", page_icon="💶", layout="wide")

df = load_data()

st.title("💶 Pricing Analysis")
st.markdown("Explore how price varies by performance, range, and market tier.")
st.divider()

# ------------------------------------------------------------------
# Boxplot: Price by Price Tier (Segment substitute)
# ------------------------------------------------------------------
st.subheader("Price Distribution by Price Tier")

fig, ax = plt.subplots(figsize=(12, 5))
tier_order = ['Budget', 'Mid-Range', 'Premium', 'Luxury']
existing_tiers = [t for t in tier_order if t in df['PriceTier'].unique()]
sns.boxplot(data=df, x='PriceTier', y='Price', order=existing_tiers, ax=ax, palette='coolwarm')
ax.set_ylabel("Price (€)")
st.pyplot(fig)

st.divider()

# ------------------------------------------------------------------
# Scatter: Price vs Range, colored by PriceTier, sized by TopSpeed
# ------------------------------------------------------------------
st.subheader("Price vs. Range (bubble size = Top Speed)")

fig, ax = plt.subplots(figsize=(12, 6))
sns.scatterplot(
    data=df, x='Range', y='Price',
    hue='PriceTier', size='TopSpeed', sizes=(40, 300),
    alpha=0.75, palette='viridis', ax=ax
)
ax.set_xlabel("Range (km)")
ax.set_ylabel("Price (€)")
ax.legend(bbox_to_anchor=(1.02, 1), loc='upper left', fontsize=8)
st.pyplot(fig)

st.divider()

# ------------------------------------------------------------------
# Price Tier breakdown by Charging Tier (instead of by Segment)
# ------------------------------------------------------------------
col1, col2 = st.columns(2)

with col1:
    st.subheader("Price Tier vs. Charging Tier")
    fig, ax = plt.subplots(figsize=(7, 5))
    crosstab = df.groupby(['PriceTier', 'ChargingTier']).size().unstack(fill_value=0)
    crosstab = crosstab.reindex(existing_tiers)
    crosstab.plot(kind='bar', stacked=True, ax=ax, colormap='Set2')
    ax.set_ylabel("Number of Models")
    ax.legend(bbox_to_anchor=(1.02, 1), loc='upper left', fontsize=7)
    st.pyplot(fig)

with col2:
    st.subheader("Average Price by Tier")
    tier_price = df.groupby('PriceTier')['Price'].mean().reindex(existing_tiers)
    fig, ax = plt.subplots(figsize=(7, 5))
    sns.barplot(x=tier_price.index, y=tier_price.values, ax=ax, palette='magma')
    ax.set_ylabel("Average Price (€)")
    st.pyplot(fig)

st.divider()

# ------------------------------------------------------------------
# Interactive price range filter
# ------------------------------------------------------------------
st.subheader("Explore by Price Range")
price_range = st.slider(
    "Select a price range (€)",
    min_value=int(df['Price'].min()),
    max_value=int(df['Price'].max()),
    value=(int(df['Price'].min()), int(df['Price'].max()))
)

filtered = df[(df['Price'] >= price_range[0]) & (df['Price'] <= price_range[1])]
st.write(f"**{len(filtered)} models** fall within €{price_range[0]:,} – €{price_range[1]:,}")
st.dataframe(
    filtered[['Brand', 'Model', 'Price', 'Range', 'PriceTier']].sort_values('Price'),
    use_container_width=True
)
