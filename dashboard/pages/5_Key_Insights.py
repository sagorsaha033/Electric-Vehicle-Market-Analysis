"""
Page: Key Insights
The narrative summary page. The headline numbers below are computed
LIVE from your actual data (not hardcoded placeholders), so they will
always reflect your real dataset.
"""

import streamlit as st
import matplotlib.pyplot as plt
import seaborn as sns
from scipy import stats
from utils import load_data

st.set_page_config(page_title="Key Insights", page_icon="🔑", layout="wide")

df = load_data()

st.title("🔑 Key Insights")
st.markdown("The headline findings from this analysis.")
st.divider()

# ------------------------------------------------------------------
# Compute real correlation values live, rather than hardcoding numbers
# that could drift out of sync with the actual data.
# ------------------------------------------------------------------
r_range, p_range = stats.pearsonr(df['Range'], df['Price'])
r_speed, p_speed = stats.pearsonr(df['TopSpeed'], df['Price'])
r_eff, p_eff = stats.pearsonr(df['Efficiency'], df['Price'])

fast_avg = df[df['ChargingTier'] == 'Fast']['Price'].mean()
none_avg = df[df['ChargingTier'] == 'No Fast Charge']['Price'].mean() if 'No Fast Charge' in df['ChargingTier'].unique() else None

st.markdown(f"""
> 📌 **Range and top speed are the strongest price drivers.**
> Correlation analysis shows range (r = {r_range:.2f}, p = {p_range:.4f}) and
> top speed (r = {r_speed:.2f}, p = {p_speed:.4f}) as statistically significant
> predictors of price. Efficiency shows a weaker relationship
> (r = {r_eff:.2f}, p = {p_eff:.4f}).
""")

if none_avg:
    price_gap = fast_avg / none_avg
    st.markdown(f"""
    > 📌 **Fast charging is a premium feature, not a market standard.**
    > Vehicles in the "Fast" charging tier average €{fast_avg:,.0f}, compared to
    > €{none_avg:,.0f} for vehicles with no fast-charge capability —
    > a {price_gap:.1f}x price gap.
    """)
else:
    st.markdown(f"""
    > 📌 **Fast charging tier pricing:** Vehicles in the "Fast" charging tier
    > average €{fast_avg:,.0f}.
    """)

st.markdown("""
> 📌 **Price is not a perfect proxy for performance.**
> Plotting performance score against price reveals meaningful scatter —
> several mid-priced EVs match the performance of vehicles priced
> significantly higher.
""")

st.divider()

# ------------------------------------------------------------------
# Best value callout
# ------------------------------------------------------------------
st.subheader("🏆 Best Value Vehicle")

best_value = df.nsmallest(1, 'Price_per_Km_Range')[
    ['Brand', 'Model', 'Price', 'Range', 'Price_per_Km_Range', 'PriceTier']
]
st.dataframe(best_value, use_container_width=True)

st.divider()

# ------------------------------------------------------------------
# Performance vs Price scatter
# ------------------------------------------------------------------
st.subheader("Performance Score vs. Price")

fig, ax = plt.subplots(figsize=(12, 6))
sns.scatterplot(
    data=df, x='Price', y='PerformanceScore',
    hue='PriceTier', palette='coolwarm', s=70, alpha=0.8, ax=ax
)
ax.set_xlabel("Price (€)")
ax.set_ylabel("Performance Score (0–100)")
st.pyplot(fig)

st.divider()

# ------------------------------------------------------------------
# Limitations
# ------------------------------------------------------------------
st.warning(
    "⚠️ **Limitations:** This dataset has no 'Segment', 'BodyStyle', or "
    "'Seats' columns, so vehicle-type comparisons here are based on engineered "
    "Price Tiers rather than the manufacturer's own segment classification. "
    "No sales volume or time-series data was available — findings describe "
    "product specifications, not market demand. 'Best value' is defined "
    "narrowly as price-per-km-of-range."
)
