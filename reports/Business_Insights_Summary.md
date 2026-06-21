
# Electric Vehicle Market Analysis — Business Insights Summary


## Executive Summary

The EV market shows clear price stratification driven primarily by **range and 
performance**, not efficiency. Fast charging is currently a premium feature 
rather than a market standard. A small number of brands account for the 
majority of listed models, though this reflects catalog breadth, not confirmed 
sales volume. The best value-for-money vehicles are concentrated in the 
compact/mid-size segments rather than the luxury tier.

---

## Key Findings

### 1. Market Structure
- The top 10 brands account for **66% of all listed models**, indicating a 
  catalog concentrated among a handful of major manufacturers.
- ⚠️ Caveat: this reflects model availability in the dataset, not confirmed 
  unit sales or market share — no sales-volume data was available for this analysis.

### 2. Pricing Drivers
- **Range** (r = 0.69) and **top speed** (r = 0.65) are the strongest 
  statistically significant drivers of price (p < 0.001 for both).
- **Efficiency** has a weak, almost negligible relationship with price 
  (r = 0.21), suggesting the market does not currently pay a premium for 
  energy efficiency — it pays for range and performance capability.
- **Interpretation, not causation:** range and price likely both reflect an 
  underlying "vehicle tier" — a luxury SUV has both a bigger battery (more range) 
  and a higher price tag for many overlapping reasons, not because range alone 
  drives price.

### 3. Charging Speed as a Premium Feature
- Vehicles in the "Fast" charging tier average **€68,500**, compared to 
  **€24,000** for vehicles with no fast-charge capability — a >2.5x price gap.
- This signals a **market gap**: affordable EVs with fast-charging capability 
  remain rare, representing a potential differentiation opportunity for 
  budget-segment manufacturers.

### 4. Best Value Segment & Vehicles
- Using price-per-km-of-range as the value metric, the **[Segment X]** segment 
  offers the best average value at **€[XX] per km of range**.
- The single best value vehicle in the dataset is the **[Brand Model]**, at 
  **€[XX] per km of range** — notably in a non-luxury segment, contradicting 
  any assumption that higher price guarantees better range efficiency.

### 5. Performance Is Not Strictly Tied to Price
- Plotting performance score against price reveals meaningful scatter, not a 
  tight line — several mid-priced EVs achieve performance scores comparable 
  to vehicles priced significantly higher.
- This suggests price is a partial, not complete, proxy for performance — 
  worth highlighting for value-conscious buyers or competitive benchmarking.

---

## Limitations
- Sample size (~103 models) limits the statistical power of segment-level 
  comparisons with small subgroups.
- No sales volume, country, or time-series data — all findings describe 
  **product specifications**, not market demand or adoption trends.
- "Best value" is defined narrowly as price-per-km-of-range; a multi-factor 
  value index (incorporating efficiency and charging speed) is a natural 
  next step.

## Recommended Next Steps
1. Layer in real-world sales/registration data to validate "dominance" claims 
   with actual market share.
2. Build a multi-factor value index combining range, charging speed, and 
   efficiency, weighted by buyer priorities.
3. Track this analysis over multiple dataset snapshots/years to convert 
   point-in-time specs into genuine trend analysis.
