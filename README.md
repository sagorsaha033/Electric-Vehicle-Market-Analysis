# ⚡ Electric Vehicle Market Analysis

An end-to-end data analytics project exploring pricing, range, charging performance, and brand positioning across 360 electric vehicle models — from raw data cleaning through statistical analysis to an interactive Streamlit dashboard.

![Python](https://img.shields.io/badge/Python-3.10-blue?logo=python)
![Pandas](https://img.shields.io/badge/Pandas-2.2-150458?logo=pandas)
![Streamlit](https://img.shields.io/badge/Streamlit-Dashboard-FF4B4B?logo=streamlit)
![Status](https://img.shields.io/badge/Status-Complete-success)

**🔗 [Live Dashboard](#)** ← *replace this with your Streamlit Community Cloud URL*

---

## 📌 Project Overview

This project analyzes specifications for 360 electric vehicle models to answer a core business question:
**what actually drives EV pricing, and which vehicles offer the best value to consumers?**

The analysis covers data cleaning, feature engineering, exploratory data analysis, correlation and statistical significance testing, a multiple regression with a multicollinearity check, and a 6-page interactive Streamlit dashboard — following the same workflow used in a real analyst role: raw data → cleaned data → insight → stakeholder-ready deliverable.

**📓 [View the Full Analysis Notebook](notebooks/EV_Market_Analysis.ipynb)**
**📄 [Read the Business Insights Summary](reports/Business_Insights_Summary.md)**

---

## 🗂️ Dataset

- **Source:** EV specifications scraped from [ev-database.org](https://ev-database.org), 360 vehicle records
- **Fields used:** Battery capacity (kWh), efficiency (Wh/km), fast-charge rate (km per 30 min), price (Germany, €), range (km), top speed (km/h), 0–100 km/h acceleration (sec), brand
- **Note:** This dataset does not include vehicle segment, body style, plug type, or seat count — these fields, common in some other EV datasets, are not present here. Comparisons that would normally group by "segment" instead use an engineered **Price Tier** (Budget / Mid-Range / Premium / Luxury), as documented below.

---

## 🎯 Business Questions Answered

| # | Question | Answer Location |
|---|----------|-----------------|
| 1 | Which EV brands dominate the market? | Notebook, Dashboard → Brand Analysis |
| 2 | Which EVs provide the highest range? | Notebook, Dashboard → Range Analysis |
| 3 | What factors affect EV prices? | Notebook, Dashboard → Key Insights |
| 4 | How does charging speed influence pricing? | Notebook, Dashboard → Charging Analysis |
| 5 | Which price tier offers the best value? | Notebook, Dashboard → Key Insights |
| 6 | Which vehicles offer the best price-to-range ratio? | Notebook, Dashboard → Key Insights |

---

## 🔑 Key Findings

- **Top speed is the strongest statistically significant price driver in this dataset** (r = 0.71, p < 0.001), ahead of range (r = 0.55, p < 0.001). Efficiency has a much weaker relationship with price (r = 0.17, p = 0.001).
- **Fast charging carries a substantial price premium.** Vehicles in the "Fast" charging tier average roughly €86,700, compared to roughly €51,000–53,000 for "Moderate" and "Slow" tiers — fast charging is concentrated in higher-priced vehicles, not spread evenly across the market.
- **Raw regression coefficients were initially misleading.** A first-pass linear regression on unstandardized features (Range, TopSpeed, Efficiency, AccelSec) produced coefficients that contradicted the simple correlation results. Standardizing the features and checking the correlation matrix between predictors revealed strong multicollinearity (e.g., TopSpeed and AccelSec correlated at r = -0.84) — three of the four predictors are largely measuring the same underlying "performance tier." Standardized coefficients, once corrected for this, aligned with the simple correlation findings.
- **The best price-to-range value in the dataset is the Citroën e-C3**, at approximately €93.20 per km of range — a budget-tier vehicle, not a premium one, challenging any assumption that higher price guarantees better range efficiency.
- Price is **not a reliable proxy for overall performance** — plotting a composite performance score against price shows meaningful scatter, with several mid-priced vehicles matching the performance of much more expensive ones.

*Full methodology, statistical tests, and caveats in [Business_Insights_Summary.md](reports/Business_Insights_Summary.md).*

---

## 🛠️ Tools & Methodology

| Stage | Tools / Techniques |
|---|---|
| Data Cleaning | Python, Pandas — missing value handling, duplicate detection, placeholder-value resolution, type correction |
| Outlier Analysis | IQR method, boxplots — outliers retained and justified, not blindly removed |
| Feature Engineering | Price-per-km-range, charging tiers, efficiency categories, composite performance score |
| Statistical Analysis | Pearson correlation with significance testing (SciPy), multiple linear regression, multicollinearity diagnosis via standardized coefficients and predictor correlation matrix |
| Visualization | Matplotlib, Seaborn — histograms, boxplots, scatter/bubble charts, correlation heatmaps |
| Dashboard | Streamlit — multi-page app, cached data loading, interactive filters and sliders |

---

## 📂 Repository Structure

```
electric-vehicle-market-analysis/
├── data/
│   ├── raw/                       # Original, untouched dataset
│   └── processed/
│       └── ElectricCarData_clean.csv
├── notebooks/
│   └── EV_Market_Analysis.ipynb
├── visuals/
│   └── eda/                       # Exported analysis charts
├── dashboard/                     # Streamlit app
│   ├── app.py
│   ├── utils.py
│   ├── requirements.txt
│   └── pages/
│       ├── 1_Brand_Analysis.py
│       ├── 2_Pricing_Analysis.py
│       ├── 3_Range_Analysis.py
│       ├── 4_Charging_Analysis.py
│       └── 5_Key_Insights.py
├── reports/
│   └── Business_Insights_Summary.md
├── requirements.txt
└── README.md
```

---

## 🚀 Running the Dashboard Locally

```bash
# Clone the repo
git clone https://github.com/<your-username>/electric-vehicle-market-analysis.git
cd electric-vehicle-market-analysis/dashboard

# Install dependencies
pip install -r requirements.txt

# Run the app
streamlit run app.py
```

The app opens automatically at `http://localhost:8501`, with sidebar navigation across all 6 pages.

---

## 📊 Dashboard Pages

| Page | Contents |
|---|---|
| **Executive Summary** | Market-wide KPIs, price tier breakdown, top brands by model count |
| **Brand Analysis** | Model count, average price/range by brand, brand comparison table, interactive brand filter |
| **Pricing Analysis** | Price distribution by tier, price-vs-range scatter, interactive price-range explorer |
| **Range Analysis** | Top vehicles by range, range distribution, range-vs-efficiency, range-per-kWh-of-battery |
| **Charging Analysis** | Charging tier distribution, price-by-charging-tier, fast-charge-speed-vs-price |
| **Key Insights** | Live-computed correlation findings, best-value vehicle, performance-vs-price, limitations |

---

## ⚠️ Limitations

- This dataset has no segment, body style, or seat-count fields — tier-based comparisons use an engineered Price Tier rather than a manufacturer-defined category.
- Sample reflects vehicle **specifications**, not sales volume or registrations — brand and tier findings describe catalog characteristics, not market share or consumer demand.
- "Best value" is defined narrowly as price-per-km-of-range; a multi-factor value index (incorporating efficiency, charging speed, and battery capacity) is a natural next step.
- The regression model (R² ≈ 0.59) explains roughly 59% of price variance using five specs — the remainder reflects factors outside this dataset (brand premium, trim level, market-specific pricing).

---

## 🚀 Future Improvements

- Build a multi-factor value index combining range, charging speed, efficiency, and battery capacity
- Layer in real-world sales/registration data to distinguish catalog breadth from actual market share
- Add a clustering analysis (e.g., KMeans) to discover natural EV market segments, since this dataset has no built-in segment labels
- Extend the regression with regularization (Ridge/Lasso) to handle the multicollinearity identified between range, top speed, and acceleration more formally

---

## 🧑‍💻 About This Project

Built as a portfolio project to demonstrate end-to-end data analyst skills: data cleaning, statistical reasoning, regression diagnostics, visualization, business communication, and interactive dashboard development.

**Author:** [Your Name] · [LinkedIn] · [Portfolio Site]
