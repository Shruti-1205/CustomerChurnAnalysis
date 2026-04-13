"""
Build churn.db from the project's processed CSV files.

Creates a SQLite database with 10 tables that mirror every CSV exported
by the analysis notebooks.  Run this once before executing the SQL queries.

Usage:
    python sql/00_setup_database.py
"""

import sqlite3
from pathlib import Path

import pandas as pd

# ---------------------------------------------------------------------------
# Paths
# ---------------------------------------------------------------------------
PROJECT_ROOT = Path(__file__).parent.parent
PROCESSED_DIR = PROJECT_ROOT / "data" / "processed"
DASHBOARD_DIR = PROCESSED_DIR / "dashboard_tables"
REPORTS_DIR = PROJECT_ROOT / "reports"
DB_PATH = Path(__file__).parent / "churn.db"

# ---------------------------------------------------------------------------
# CSV → table mapping
# ---------------------------------------------------------------------------
TABLE_MAP = {
    "customers":            PROCESSED_DIR / "analytics_ready_churn_data.csv",
    "customer_predictions": DASHBOARD_DIR / "customer_predictions.csv",
    "kpi_summary":          DASHBOARD_DIR / "kpi_summary.csv",
    "churn_by_contract":    DASHBOARD_DIR / "churn_by_contract.csv",
    "churn_by_tenure":      DASHBOARD_DIR / "churn_by_tenure.csv",
    "churn_by_charge":      DASHBOARD_DIR / "churn_by_charge.csv",
    "churn_by_value":       DASHBOARD_DIR / "churn_by_value.csv",
    "risk_band_summary":    DASHBOARD_DIR / "risk_band_summary.csv",
    "revenue_summary":      DASHBOARD_DIR / "revenue_summary.csv",
    "top_high_risk":        DASHBOARD_DIR / "top_50_high_risk_customers.csv",
}

# ---------------------------------------------------------------------------
# Load CSVs into SQLite
# ---------------------------------------------------------------------------
print(f"Building database at: {DB_PATH}\n")

conn = sqlite3.connect(DB_PATH)

for table_name, csv_path in TABLE_MAP.items():
    df = pd.read_csv(csv_path)
    df.to_sql(table_name, conn, if_exists="replace", index=False)
    print(f"  {table_name:<25} {len(df):>6,} rows  ({csv_path.name})")

conn.close()

print(f"\nDatabase ready: {DB_PATH}")
print("\nRun queries with:")
print(f'  sqlite3 {DB_PATH.relative_to(PROJECT_ROOT)} < sql/queries/02_revenue_at_risk.sql')
