"""
Shared utilities for the EV Market Analysis Streamlit dashboard.

NOTE: This version is written against the actual ev-database.org-style
schema (360 rows), NOT the original ~103-row ElectricCarData.csv schema.
Key differences from the original design:
  - No 'Segment', 'BodyStyle', 'PlugType', or 'Seats' columns exist in
    this dataset, so any visual relying on them has been removed or
    substituted with an available column.
  - 'Car_name' already contains Brand + Model combined as one string
    (there's no separate Model column).
  - Column names use the dataset's original naming (Price.DE., Top_speed,
    acceleration..0.100., etc.) rather than the Brand/Model/PriceEuro
    convention used in earlier phases of this project.
"""

import pandas as pd
import streamlit as st


@st.cache_data
def load_data():
    """
    Load the cleaned EV dataset and apply light renaming so the rest
    of the app can use clear, consistent names instead of the original
    dotted/abbreviated column headers (e.g. 'Price.DE.' -> 'Price').

    Renaming here, once, in a single place, means every page can refer
    to 'Price' instead of the awkward 'Price.DE.' syntax everywhere.
    """
    df = pd.read_csv("data/ElectricCarData_clean.csv")

    df = df.rename(columns={
        "Price.DE.": "Price",
        "Top_speed": "TopSpeed",
        "acceleration..0.100.": "AccelSec",
        "Fast_charge": "FastCharge",
        "Car_name": "Model",   # Car_name already includes brand, but we
                                 # keep it as the display name for a vehicle
    })

    return df


def kpi_card(label, value, delta=None):
    """Small helper to keep KPI formatting consistent across pages."""
    st.metric(label=label, value=value, delta=delta)
