"""
Shared utilities for the EV Market Analysis Streamlit dashboard.
"""

import pandas as pd
import streamlit as st
import os


@st.cache_data
def load_data():
    """
    Load the cleaned EV dataset.

    Path note: app.py runs from inside the 'dashboard/' folder on
    Streamlit Cloud, but the cleaned CSV lives at the repo root under
    'data/processed/'. We build the path relative to THIS file's
    location (utils.py), rather than relative to wherever the app
    happens to be launched from -- this makes it work identically
    whether you run it locally from inside dashboard/, or it's run
    by Streamlit Cloud's own working directory setup.
    """
    current_dir = os.path.dirname(os.path.abspath(__file__))  # .../dashboard
    repo_root = os.path.dirname(current_dir)                   # one level up
    csv_path = os.path.join(repo_root, "data", "processed", "ElectricCarData_clean.csv")

    df = pd.read_csv(csv_path)

    df = df.rename(columns={
        "Price.DE.": "Price",
        "Top_speed": "TopSpeed",
        "acceleration..0.100.": "AccelSec",
        "Fast_charge": "FastCharge",
        "Car_name": "Model",
    })

    return df


def kpi_card(label, value, delta=None):
    """Small helper to keep KPI formatting consistent across pages."""
    st.metric(label=label, value=value, delta=delta)
