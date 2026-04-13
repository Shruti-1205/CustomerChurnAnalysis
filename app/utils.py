"""Data loading helpers for the Streamlit app.

All paths are resolved relative to this file's location so the app works
regardless of which directory `streamlit run` is invoked from.
"""

from pathlib import Path

import pandas as pd
import streamlit as st

# ---------------------------------------------------------------------------
# Base paths
# ---------------------------------------------------------------------------
APP_DIR      = Path(__file__).parent
PROJECT_ROOT = APP_DIR.parent
DATA_DIR     = PROJECT_ROOT / "data" / "processed" / "dashboard_tables"
MODELS_DIR   = PROJECT_ROOT / "models"


# ---------------------------------------------------------------------------
# Loaders  (all cached so re-renders don't re-read disk)
# ---------------------------------------------------------------------------

@st.cache_data
def load_kpis() -> dict:
    kpi = pd.read_csv(DATA_DIR / "kpi_summary.csv").iloc[0]
    rev = pd.read_csv(DATA_DIR / "revenue_summary.csv").iloc[0]
    pred = pd.read_csv(DATA_DIR / "pred_kpis.csv").iloc[0]
    return {
        "total_customers":      int(kpi["total_customers"]),
        "churn_rate_pct":       float(kpi["churn_rate_pct"]),
        "total_revenue":        float(kpi["total_revenue"]),
        "avg_monthly_charge":   float(kpi["avg_monthly_charge"]),
        "revenue_at_risk":      float(rev["revenue_at_risk"]),
        "pct_revenue_at_risk":  float(rev["percent_revenue_at_risk"]),
        "predicted_churn_rate": float(pred["predicted_churn_rate_pct"]),
        "model_name":           str(pred["model_name"]),
        "threshold":            float(pred["threshold"]),
    }


@st.cache_data
def load_churn_by_contract() -> pd.DataFrame:
    return pd.read_csv(DATA_DIR / "churn_by_contract.csv")


@st.cache_data
def load_churn_by_tenure() -> pd.DataFrame:
    df = pd.read_csv(DATA_DIR / "churn_by_tenure.csv")
    order = ["0-12", "12-24", "24-48", "48-60", "60-72"]
    df["tenure_group"] = pd.Categorical(df["tenure_group"], categories=order, ordered=True)
    return df.sort_values("tenure_group")


@st.cache_data
def load_churn_by_value() -> pd.DataFrame:
    df = pd.read_csv(DATA_DIR / "churn_by_value.csv")
    order = ["Low Value", "Mid Value", "High Value", "Very High Value"]
    df["customer_value_segment"] = pd.Categorical(
        df["customer_value_segment"], categories=order, ordered=True
    )
    return df.sort_values("customer_value_segment")


@st.cache_data
def load_churn_by_charge() -> pd.DataFrame:
    df = pd.read_csv(DATA_DIR / "churn_by_charge.csv")
    order = ["Low", "Medium", "High", "Very High"]
    df["monthly_charge_group"] = pd.Categorical(
        df["monthly_charge_group"], categories=order, ordered=True
    )
    return df.sort_values("monthly_charge_group")


@st.cache_data
def load_risk_bands() -> pd.DataFrame:
    df = pd.read_csv(DATA_DIR / "risk_band_summary.csv")
    order = ["Critical", "High", "Medium", "Low"]
    df["risk_band"] = pd.Categorical(df["risk_band"], categories=order, ordered=True)
    return df.sort_values("risk_band")


@st.cache_data
def load_top_risk_customers() -> pd.DataFrame:
    df = pd.read_csv(DATA_DIR / "top_50_high_risk_customers.csv")
    df["churn_probability_pct"] = (df["churn_probability"] * 100).round(1)
    return df


def model_path() -> Path:
    return MODELS_DIR / "churn_model.pkl"


def metadata_path() -> Path:
    return MODELS_DIR / "model_metadata.json"
