"""
Telecom Customer Churn Intelligence — Streamlit App

5 pages:
  1. Executive Overview   — KPI cards + business narrative
  2. Segment Analysis     — Churn by contract / tenure / value / charge tier
  3. Risk Intelligence    — Risk band table + donut chart
  4. Customer Lookup      — Searchable top-50 high-risk customer table
  5. Churn Predictor      — Live single-customer prediction form

Usage:
    streamlit run app/app.py
"""

import json
import sys
from pathlib import Path

import altair as alt
import joblib
import numpy as np
import pandas as pd
import streamlit as st

# Make sure local utils.py is importable when invoked from project root
sys.path.insert(0, str(Path(__file__).parent))
from utils import (
    load_churn_by_charge,
    load_churn_by_contract,
    load_churn_by_tenure,
    load_churn_by_value,
    load_kpis,
    load_risk_bands,
    load_top_risk_customers,
    metadata_path,
    model_path,
)

# ---------------------------------------------------------------------------
# Page config
# ---------------------------------------------------------------------------
st.set_page_config(
    page_title="Churn Intelligence Dashboard",
    page_icon="📡",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ---------------------------------------------------------------------------
# Minimal CSS — card borders + table highlight
# ---------------------------------------------------------------------------
st.markdown("""
<style>
[data-testid="metric-container"] {
    background: #F8FAFC;
    border-left: 4px solid #2563EB;
    border-radius: 6px;
    padding: 14px 18px;
}
</style>
""", unsafe_allow_html=True)

# ---------------------------------------------------------------------------
# Sidebar
# ---------------------------------------------------------------------------
st.sidebar.title("📡 Churn Intelligence")
page = st.sidebar.radio(
    "Navigate",
    ["Executive Overview", "Segment Analysis", "Risk Intelligence",
     "Customer Lookup", "Churn Predictor"],
)
st.sidebar.divider()
st.sidebar.caption("Model: HGB Calibrated | ROC-AUC: 0.8448 | Threshold: 0.3143")

# ---------------------------------------------------------------------------
# Shared data
# ---------------------------------------------------------------------------
kpis = load_kpis()

RISK_COLORS = {
    "Critical": "#DC2626",
    "High":     "#F97316",
    "Medium":   "#D97706",
    "Low":      "#16A34A",
}

# ===========================================================================
# Page 1 — Executive Overview
# ===========================================================================
if page == "Executive Overview":
    st.title("Customer Churn & Revenue Overview")
    st.caption("IBM Telco Dataset | 7,043 customers | Model: HGB Calibrated (ROC-AUC 0.8448)")

    c1, c2, c3, c4 = st.columns(4)
    with c1:
        st.metric(
            "Total Customers",
            f"{kpis['total_customers']:,}",
        )
    with c2:
        st.metric(
            "Churn Rate",
            f"{kpis['churn_rate_pct']:.2f}%",
            delta="↑ vs 2-yr contract: 2.83%",
            delta_color="inverse",
        )
    with c3:
        st.metric(
            "Revenue at Risk",
            f"${kpis['revenue_at_risk']:,.0f}",
        )
    with c4:
        st.metric(
            "% Revenue at Risk",
            f"{kpis['pct_revenue_at_risk']:.2f}%",
            delta_color="inverse",
        )

    st.divider()
    st.info(
        "**Key Insight:** 26.54% of customers are actively churning, putting **$2.86M in "
        "monthly revenue** at risk (17.83% of total). Month-to-month contract holders churn "
        "at 42.71% — nearly 15× the rate of two-year customers — and 48% of new customers "
        "leave within their first year. The 384 Critical-risk customers carry an **88% actual "
        "churn rate** and require immediate retention outreach."
    )

    st.subheader("Model Performance")
    mc1, mc2, mc3, mc4 = st.columns(4)
    mc1.metric("ROC-AUC", "0.8448")
    mc2.metric("Avg Precision", "0.6532")
    mc3.metric("Optimised Threshold", "0.3143")
    mc4.metric("Recall @ Threshold", "77.0%")

# ===========================================================================
# Page 2 — Segment Analysis
# ===========================================================================
elif page == "Segment Analysis":
    st.title("Churn by Customer Segment")
    st.caption("Explore how churn rate varies across contract type, tenure, value, and pricing tier")

    # Row 1
    col1, col2 = st.columns(2)

    with col1:
        st.subheader("By Contract Type")
        df_c = load_churn_by_contract().sort_values("churn_rate", ascending=False)
        chart = (
            alt.Chart(df_c)
            .mark_bar()
            .encode(
                x=alt.X("churn_rate:Q", title="Churn Rate (%)", scale=alt.Scale(domain=[0, 50])),
                y=alt.Y("Contract:N", sort="-x", title=""),
                color=alt.Color(
                    "churn_rate:Q",
                    scale=alt.Scale(scheme="redyellowgreen", reverse=True),
                    legend=None,
                ),
                tooltip=["Contract", alt.Tooltip("churn_rate:Q", title="Churn Rate (%)"),
                         alt.Tooltip("customers:Q", title="Customers", format=",")],
            )
            .properties(height=180)
        )
        st.altair_chart(chart, use_container_width=True)

    with col2:
        st.subheader("By Tenure Cohort")
        df_t = load_churn_by_tenure()
        chart = (
            alt.Chart(df_t)
            .mark_line(point=True, color="#2563EB", strokeWidth=2.5)
            .encode(
                x=alt.X("tenure_group:O", title="Tenure Group (months)", sort=None),
                y=alt.Y("churn_rate:Q", title="Churn Rate (%)", scale=alt.Scale(domain=[0, 55])),
                tooltip=["tenure_group", alt.Tooltip("churn_rate:Q", title="Churn Rate (%)"),
                         alt.Tooltip("customers:Q", title="Customers", format=",")],
            )
            .properties(height=180)
        )
        area = (
            alt.Chart(df_t)
            .mark_area(opacity=0.15, color="#2563EB")
            .encode(
                x=alt.X("tenure_group:O", sort=None),
                y="churn_rate:Q",
            )
        )
        st.altair_chart(area + chart, use_container_width=True)

    st.divider()

    # Row 2
    col3, col4 = st.columns(2)

    with col3:
        st.subheader("By Customer Value Segment")
        df_v = load_churn_by_value()
        chart = (
            alt.Chart(df_v)
            .mark_bar()
            .encode(
                x=alt.X("customer_value_segment:O", title="", sort=None),
                y=alt.Y("churn_rate:Q", title="Churn Rate (%)"),
                color=alt.Color(
                    "churn_rate:Q",
                    scale=alt.Scale(scheme="redyellowgreen", reverse=True),
                    legend=None,
                ),
                tooltip=["customer_value_segment",
                         alt.Tooltip("churn_rate:Q", title="Churn Rate (%)"),
                         alt.Tooltip("customers:Q", title="Customers", format=",")],
            )
            .properties(height=200)
        )
        st.altair_chart(chart, use_container_width=True)

    with col4:
        st.subheader("By Monthly Charge Tier")
        df_ch = load_churn_by_charge()
        chart = (
            alt.Chart(df_ch)
            .mark_bar()
            .encode(
                x=alt.X("monthly_charge_group:O", title="", sort=None),
                y=alt.Y("churn_rate:Q", title="Churn Rate (%)"),
                color=alt.Color(
                    "churn_rate:Q",
                    scale=alt.Scale(scheme="redyellowgreen", reverse=True),
                    legend=None,
                ),
                tooltip=["monthly_charge_group",
                         alt.Tooltip("churn_rate:Q", title="Churn Rate (%)"),
                         alt.Tooltip("customers:Q", title="Customers", format=",")],
            )
            .properties(height=200)
        )
        st.altair_chart(chart, use_container_width=True)

# ===========================================================================
# Page 3 — Risk Intelligence
# ===========================================================================
elif page == "Risk Intelligence":
    st.title("Predictive Risk Intelligence")
    st.caption("Model: HGB Calibrated | Threshold: 0.3143 | ROC-AUC: 0.8448")

    df_risk = load_risk_bands()

    # KPI row
    r1, r2, r3, r4 = st.columns(4)
    for col, band in zip([r1, r2, r3, r4], ["Critical", "High", "Medium", "Low"]):
        row = df_risk[df_risk["risk_band"] == band].iloc[0]
        col.metric(
            f"{band} Risk",
            f"{int(row['customers']):,}",
            delta=f"{row['actual_churn_rate']:.1f}% actual churn",
            delta_color="inverse" if band in ("Critical", "High") else "normal",
        )

    st.divider()

    left, right = st.columns([3, 2])

    with left:
        st.subheader("Risk Band Summary")

        display = df_risk.copy()
        display["avg_churn_probability"] = display["avg_churn_probability"].map("{:.1f}%".format)
        display["actual_churn_rate"]     = display["actual_churn_rate"].map("{:.1f}%".format)
        display["predicted_churn_rate"]  = display["predicted_churn_rate"].map("{:.1f}%".format)
        display["expected_revenue_at_risk"] = display["expected_revenue_at_risk"].map("${:,.0f}".format)

        display = display.rename(columns={
            "risk_band":               "Risk Band",
            "customers":               "Customers",
            "avg_churn_probability":   "Avg Churn Prob",
            "actual_churn_rate":       "Actual Churn Rate",
            "predicted_churn_rate":    "Predicted Churn Rate",
            "expected_revenue_at_risk":"Revenue at Risk",
        })

        def highlight_risk(row):
            band = row["Risk Band"]
            styles = {
                "Critical": "background-color: #7F1D1D; color: white",
                "High":     "background-color: #78350F; color: white",
            }
            style = styles.get(band, "")
            return [style for _ in row]

        st.dataframe(
            display.style.apply(highlight_risk, axis=1),
            use_container_width=True,
            hide_index=True,
        )

        st.error(
            "**384 Critical-risk customers carry an 88.28% actual churn rate — "
            "immediate retention outreach recommended.**"
        )

    with right:
        st.subheader("Customer Distribution")
        order = ["Critical", "High", "Medium", "Low"]
        df_plot = df_risk.copy()
        df_plot["risk_band"] = pd.Categorical(df_plot["risk_band"], categories=order, ordered=True)
        df_plot = df_plot.sort_values("risk_band")

        chart = (
            alt.Chart(df_plot)
            .mark_arc(innerRadius=60, outerRadius=110)
            .encode(
                theta=alt.Theta("customers:Q"),
                color=alt.Color(
                    "risk_band:N",
                    scale=alt.Scale(
                        domain=order,
                        range=[RISK_COLORS[b] for b in order],
                    ),
                    legend=alt.Legend(title="Risk Band"),
                ),
                tooltip=["risk_band",
                         alt.Tooltip("customers:Q", title="Customers", format=","),
                         alt.Tooltip("actual_churn_rate:Q", title="Actual Churn Rate (%)")],
            )
            .properties(height=280)
        )
        st.altair_chart(chart, use_container_width=True)

# ===========================================================================
# Page 4 — Customer Lookup
# ===========================================================================
elif page == "Customer Lookup":
    st.title("High-Risk Customer Lookup")
    st.caption("Top 50 customers ranked by predicted churn probability")

    df_top = load_top_risk_customers()

    # Filters
    fc1, fc2 = st.columns([2, 1])
    with fc1:
        search = st.text_input("Search by Customer ID", placeholder="e.g. 9497-QCMMS")
    with fc2:
        band_filter = st.selectbox("Filter by Risk Band", ["All", "Critical", "High", "Medium", "Low"])

    # Apply filters
    filtered = df_top.copy()
    if search:
        filtered = filtered[filtered["customerID"].str.contains(search, case=False, na=False)]
    if band_filter != "All":
        filtered = filtered[filtered["risk_band"] == band_filter]

    # Display columns
    show_cols = {
        "customerID":           "Customer ID",
        "Contract":             "Contract",
        "tenure":               "Tenure (mo)",
        "InternetService":      "Internet",
        "MonthlyCharges":       "Monthly $",
        "risk_band":            "Risk Band",
        "churn_probability_pct":"Churn Prob %",
        "expected_revenue_at_risk": "Revenue at Risk",
    }
    display = filtered[list(show_cols.keys())].rename(columns=show_cols)
    display["Monthly $"]       = display["Monthly $"].map("${:.2f}".format)
    display["Revenue at Risk"] = display["Revenue at Risk"].map("${:.2f}".format)
    display["Churn Prob %"]    = display["Churn Prob %"].map("{:.1f}%".format)

    def color_band(row):
        styles = {
            "Critical": "background-color: #7F1D1D; color: white",
            "High":     "background-color: #78350F; color: white",
        }
        style = styles.get(row["Risk Band"], "")
        return [style for _ in row]

    st.dataframe(
        display.style.apply(color_band, axis=1),
        use_container_width=True,
        hide_index=True,
    )
    st.caption(f"Showing {len(filtered)} of {len(df_top)} high-risk customers")

# ===========================================================================
# Page 5 — Churn Predictor
# ===========================================================================
elif page == "Churn Predictor":
    st.title("Live Churn Risk Predictor")
    st.caption(
        "Enter a customer's details to get an instant churn probability from the "
        "trained HGB Calibrated model (ROC-AUC: 0.8448)"
    )

    # Auto-train if model artifacts are missing (e.g. first run on Streamlit Cloud)
    if not model_path().exists():
        with st.spinner("Training model for the first time — this takes about 30 seconds..."):
            sys.path.insert(0, str(Path(__file__).parent.parent / "models"))
            from train_and_save import run as _train
            _train(verbose=False)
        st.success("Model trained and saved. Ready to predict!")

    # Load model + metadata (cached so re-renders don't reload from disk)
    @st.cache_resource
    def load_model():
        return joblib.load(model_path())

    @st.cache_data
    def load_meta():
        with open(metadata_path()) as f:
            return json.load(f)

    model = load_model()
    meta  = load_meta()
    threshold = meta["threshold"]
    q25, q50, q75 = meta["total_charges_quantiles"]

    # -----------------------------------------------------------------------
    # Helper functions (mirror notebook 03 feature engineering exactly)
    # -----------------------------------------------------------------------
    def get_tenure_group(t: int) -> str:
        if t < 12:  return "0-12"
        if t < 24:  return "12-24"
        if t < 48:  return "24-48"
        if t < 60:  return "48-60"
        return "60-72"

    def get_monthly_charge_group(mc: float) -> str:
        if mc <= 35:   return "Low"
        if mc <= 70:   return "Medium"
        if mc <= 100:  return "High"
        return "Very High"

    def get_value_segment(tc: float) -> str:
        if tc <= q25:  return "Low Value"
        if tc <= q50:  return "Mid Value"
        if tc <= q75:  return "High Value"
        return "Very High Value"

    SERVICE_COLS = [
        "MultipleLines", "InternetService", "OnlineSecurity",
        "OnlineBackup", "DeviceProtection", "TechSupport",
        "StreamingTV", "StreamingMovies",
    ]

    def count_services(row: dict) -> int:
        return sum(1 for col in SERVICE_COLS if row.get(col) == "Yes")

    # -----------------------------------------------------------------------
    # Input form
    # -----------------------------------------------------------------------
    with st.form("predict_form"):
        st.subheader("Account & Contract")
        a1, a2, a3 = st.columns(3)
        contract  = a1.selectbox("Contract Type", ["Month-to-month", "One year", "Two year"])
        tenure    = a2.slider("Tenure (months)", 0, 72, 6)
        payment   = a3.selectbox("Payment Method", [
            "Electronic check", "Mailed check",
            "Bank transfer (automatic)", "Credit card (automatic)",
        ])

        st.subheader("Demographics")
        d1, d2, d3, d4, d5 = st.columns(5)
        gender      = d1.selectbox("Gender", ["Male", "Female"])
        senior      = d2.checkbox("Senior Citizen")
        partner_val = d3.selectbox("Partner", ["Yes", "No"])
        dependents  = d4.selectbox("Dependents", ["Yes", "No"])
        paperless   = d5.selectbox("Paperless Billing", ["Yes", "No"])

        st.subheader("Services")
        s1, s2, s3, s4 = st.columns(4)
        phone       = s1.selectbox("Phone Service", ["Yes", "No"])
        multi_lines = s2.selectbox("Multiple Lines", ["Yes", "No"])
        internet    = s3.selectbox("Internet Service", ["DSL", "Fiber optic", "No"])
        online_sec  = s4.selectbox("Online Security", ["Yes", "No"])

        s5, s6, s7, s8, s9 = st.columns(5)
        online_bkp  = s5.selectbox("Online Backup", ["Yes", "No"])
        device_prot = s6.selectbox("Device Protection", ["Yes", "No"])
        tech_sup    = s7.selectbox("Tech Support", ["Yes", "No"])
        streaming_tv  = s8.selectbox("Streaming TV", ["Yes", "No"])
        streaming_mov = s9.selectbox("Streaming Movies", ["Yes", "No"])

        st.subheader("Charges")
        ch1, ch2 = st.columns(2)
        monthly_charges = ch1.number_input("Monthly Charges ($)", 0.0, 150.0, 65.0, step=0.5)
        total_charges   = ch2.number_input("Total Charges ($)", 0.0, 9000.0, 500.0, step=10.0)

        submitted = st.form_submit_button("Predict Churn Risk", type="primary", use_container_width=True)

    # -----------------------------------------------------------------------
    # Prediction
    # -----------------------------------------------------------------------
    if submitted:
        raw = {
            "gender":          gender,
            "SeniorCitizen":   1 if senior else 0,
            "Partner":         1 if partner_val == "Yes" else 0,
            "Dependents":      1 if dependents == "Yes" else 0,
            "tenure":          tenure,
            "PhoneService":    1 if phone == "Yes" else 0,
            "MultipleLines":   multi_lines,
            "InternetService": internet,
            "OnlineSecurity":  online_sec,
            "OnlineBackup":    online_bkp,
            "DeviceProtection":device_prot,
            "TechSupport":     tech_sup,
            "StreamingTV":     streaming_tv,
            "StreamingMovies": streaming_mov,
            "Contract":        contract,
            "PaperlessBilling":1 if paperless == "Yes" else 0,
            "PaymentMethod":   payment,
            "MonthlyCharges":  monthly_charges,
            "TotalCharges":    total_charges,
        }

        # Engineered features (mirror notebook 03)
        raw["tenure_group"]            = get_tenure_group(tenure)
        raw["num_services"]            = count_services(raw)
        raw["monthly_charge_group"]    = get_monthly_charge_group(monthly_charges)
        raw["customer_value_segment"]  = get_value_segment(total_charges)
        raw["is_month_to_month"]       = 1 if contract == "Month-to-month" else 0
        raw["is_new_customer"]         = 1 if tenure < 12 else 0
        raw["paperless_billing_flag"]  = 1 if paperless == "Yes" else 0

        # Assemble DataFrame in the exact column order the model was trained on
        input_df = pd.DataFrame([raw])[meta["feature_columns"]]

        prob = float(model.predict_proba(input_df)[0, 1])
        pct  = prob * 100

        # Risk band
        if prob >= 0.75:   band, band_color = "CRITICAL",  "#DC2626"
        elif prob >= 0.50: band, band_color = "HIGH",      "#F97316"
        elif prob >= 0.25: band, band_color = "MEDIUM",    "#D97706"
        else:              band, band_color = "LOW",        "#16A34A"

        predicted_churn = prob >= threshold

        # Key risk factors (rule-based explanation from top model features)
        risk_flags = []
        if internet == "Fiber optic":
            risk_flags.append("Fiber optic internet — top churn driver (importance: 0.0363)")
        if contract == "Month-to-month":
            risk_flags.append("Month-to-month contract — 42.7% churn vs 2.8% for two-year")
        if tenure < 12:
            risk_flags.append("New customer (<12 months) — 48% of new customers churn")
        if payment == "Electronic check":
            risk_flags.append("Electronic check payment — associated with higher churn rates")
        if raw["customer_value_segment"] == "Low Value":
            risk_flags.append("Low value segment — 43% churn rate")
        if not risk_flags:
            risk_flags.append("No major risk flags detected for this customer profile")

        # Display result
        st.divider()
        res1, res2 = st.columns([1, 2])

        with res1:
            st.markdown(
                f"""
                <div style="
                    background:{band_color}22;
                    border: 2px solid {band_color};
                    border-radius: 10px;
                    padding: 24px;
                    text-align: center;
                ">
                    <div style="font-size:42px; font-weight:bold; color:{band_color}">
                        {pct:.1f}%
                    </div>
                    <div style="font-size:18px; color:{band_color}; font-weight:600">
                        {band} RISK
                    </div>
                    <div style="font-size:13px; color:#4B5563; margin-top:8px">
                        {'⚠️ Predicted to churn' if predicted_churn else '✅ Predicted to retain'}
                    </div>
                </div>
                """,
                unsafe_allow_html=True,
            )

        with res2:
            st.subheader("Key Risk Factors")
            for flag in risk_flags:
                st.markdown(f"• {flag}")

            st.subheader("What This Means")
            if band in ("CRITICAL", "HIGH"):
                st.error(
                    f"This customer has a **{pct:.1f}% predicted churn probability** "
                    f"(threshold: {threshold:.4f}). Immediate retention outreach is recommended: "
                    "consider a contract upgrade offer or personalised discount."
                )
            elif band == "MEDIUM":
                st.warning(
                    f"This customer has a **{pct:.1f}% predicted churn probability**. "
                    "Monitor closely and consider proactive check-in or service review."
                )
            else:
                st.success(
                    f"This customer has a **{pct:.1f}% predicted churn probability**. "
                    "Low risk — standard engagement is sufficient."
                )

# ---------------------------------------------------------------------------
# Footer
# ---------------------------------------------------------------------------
st.divider()
st.caption(
    "Data: IBM Telco Customer Churn Dataset | 7,043 customers | "
    "Model: HistGradientBoosting Calibrated | ROC-AUC: 0.8448 | "
    "Built with Streamlit · Python · scikit-learn"
)
