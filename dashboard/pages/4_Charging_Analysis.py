"""
Page: Charging Analysis
'Charging Tier by Segment' replaced with 'Charging Tier by Price Tier'
since Segment doesn't exist in this dataset.
"""

import streamlit as st
import matplotlib.pyplot as plt
import seaborn as sns
from utils import load_data

st.set_page_config(page_title="Charging Analysis", page_icon="⚡", layout="wide")

df = load_data()

st.title("⚡ Charging Analysis")
st.markdown("How does charging speed relate to price and vehicle tier?")
st.divider()

col1, col2 = st.columns(2)

with col1:
    st.subheader("Charging Tier Distribution")
    tier_counts = df['ChargingTier'].value_counts()
    fig, ax = plt.subplots(figsize=(6, 6))
    ax.pie(tier_counts.values, labels=tier_counts.index, autopct='%1.0f%%',
           colors=sns.color_palette('Set2'))
    st.pyplot(fig)

with col2:
    st.subheader("Average Price by Charging Tier")
    tier_price = df.groupby('ChargingTier')['Price'].mean().sort_values(ascending=False)
    fig, ax = plt.subplots(figsize=(6, 6))
    sns.barplot(x=tier_price.index, y=tier_price.values, ax=ax, palette='flare')
    ax.set_ylabel("Average Price (€)")
    st.pyplot(fig)

st.divider()

# ------------------------------------------------------------------
# FastCharge speed vs Price scatter + trend line
# ------------------------------------------------------------------
st.subheader("Fast Charge Speed vs. Price")

fig, ax = plt.subplots(figsize=(12, 6))
sns.scatterplot(
    data=df, x='FastCharge', y='Price',
    hue='ChargingTier', palette='Set2', alpha=0.8, s=80, ax=ax
)
sns.regplot(
    data=df, x='FastCharge', y='Price',
    scatter=False, color='gray', line_kws={'linestyle': '--'}, ax=ax
)
ax.set_xlabel("Fast Charge (km range per 30 min)")
ax.set_ylabel("Price (€)")
st.pyplot(fig)

st.divider()

# ------------------------------------------------------------------
# Charging Tier composition by Price Tier
# ------------------------------------------------------------------
st.subheader("Charging Tier Composition by Price Tier")

tier_order = ['Budget', 'Mid-Range', 'Premium', 'Luxury']
existing_tiers = [t for t in tier_order if t in df['PriceTier'].unique()]

crosstab = df.groupby(['PriceTier', 'ChargingTier']).size().unstack(fill_value=0)
crosstab = crosstab.reindex(existing_tiers)
crosstab_pct = crosstab.div(crosstab.sum(axis=1), axis=0) * 100

fig, ax = plt.subplots(figsize=(12, 5))
crosstab_pct.plot(kind='bar', stacked=True, ax=ax, colormap='Set2')
ax.set_ylabel("% of Models")
ax.legend(bbox_to_anchor=(1.02, 1), loc='upper left')
st.pyplot(fig)
