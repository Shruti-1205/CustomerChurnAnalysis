"""
Generate and save 6 portfolio-quality charts from the project's CSV outputs.

Reads the processed dashboard tables and saves publication-ready PNGs to the
same directory as this script (reports/figures/).

Usage:
    python reports/figures/generate_charts.py
"""

from pathlib import Path

import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import numpy as np
import pandas as pd

# ---------------------------------------------------------------------------
# Paths
# ---------------------------------------------------------------------------
SCRIPT_DIR  = Path(__file__).parent                          # reports/figures/
REPORTS_DIR = SCRIPT_DIR.parent                              # reports/
DATA_DIR    = SCRIPT_DIR.parent.parent / "data" / "processed" / "dashboard_tables"

SCRIPT_DIR.mkdir(parents=True, exist_ok=True)

# ---------------------------------------------------------------------------
# Global style
# ---------------------------------------------------------------------------
COLORS = {
    "primary":  "#2563EB",
    "danger":   "#DC2626",
    "warning":  "#D97706",
    "success":  "#16A34A",
    "neutral":  "#6B7280",
    "light":    "#DBEAFE",
}

RISK_COLORS = {
    "Critical": COLORS["danger"],
    "High":     "#F97316",
    "Medium":   COLORS["warning"],
    "Low":      COLORS["success"],
}

plt.rcParams.update({
    "font.family":         "sans-serif",
    "font.size":           11,
    "axes.spines.top":     False,
    "axes.spines.right":   False,
    "axes.grid":           True,
    "axes.grid.axis":      "x",
    "grid.alpha":          0.3,
    "figure.dpi":          150,
    "savefig.bbox":        "tight",
    "savefig.facecolor":   "white",
    "savefig.dpi":         150,
})


def save(name: str) -> None:
    path = SCRIPT_DIR / name
    plt.savefig(path)
    plt.close()
    print(f"  Saved: {path.name}")


# ---------------------------------------------------------------------------
# Chart 1 — Churn Rate by Contract Type
# ---------------------------------------------------------------------------
def chart_churn_by_contract() -> None:
    df = pd.read_csv(DATA_DIR / "churn_by_contract.csv")
    df = df.sort_values("churn_rate", ascending=True)

    bar_colors = [
        COLORS["success"] if r < 10 else COLORS["warning"] if r < 25 else COLORS["danger"]
        for r in df["churn_rate"]
    ]

    fig, ax = plt.subplots(figsize=(8, 4))
    bars = ax.barh(df["Contract"], df["churn_rate"], color=bar_colors, height=0.5)

    for bar, val in zip(bars, df["churn_rate"]):
        ax.text(bar.get_width() + 0.5, bar.get_y() + bar.get_height() / 2,
                f"{val:.1f}%", va="center", fontweight="bold")

    ax.set_xlabel("Churn Rate (%)")
    ax.set_xlim(0, 55)
    ax.set_title("Churn Rate by Contract Type", fontsize=14, fontweight="bold", pad=12)
    ax.text(0, -0.12, "Month-to-month contracts churn at 15× the rate of two-year contracts",
            transform=ax.transAxes, color=COLORS["neutral"], fontsize=9)

    save("01_churn_by_contract.png")


# ---------------------------------------------------------------------------
# Chart 2 — Churn Rate by Tenure Cohort
# ---------------------------------------------------------------------------
def chart_churn_by_tenure() -> None:
    df = pd.read_csv(DATA_DIR / "churn_by_tenure.csv")
    df = df.sort_values("tenure_group")

    x = range(len(df))
    rates = df["churn_rate"].values

    fig, ax = plt.subplots(figsize=(8, 4))
    ax.fill_between(x, rates, alpha=0.15, color=COLORS["primary"])
    ax.plot(x, rates, color=COLORS["primary"], linewidth=2.5, marker="o", markersize=7)

    for i, (xi, r) in enumerate(zip(x, rates)):
        label = f"{r:.1f}%"
        if i == 0:
            ax.annotate("48.3%\nHighest risk window",
                        xy=(xi, r), xytext=(xi + 0.15, r - 4),
                        fontsize=8.5, color=COLORS["danger"], fontweight="bold")
        else:
            ax.text(xi, r + 1.2, label, ha="center", fontsize=9)

    ax.set_xticks(list(x))
    ax.set_xticklabels(df["tenure_group"])
    ax.set_xlabel("Tenure Group (months)")
    ax.set_ylabel("Churn Rate (%)")
    ax.set_ylim(0, 60)
    ax.set_title("Customer Churn Rate by Tenure Cohort", fontsize=14, fontweight="bold", pad=12)
    ax.text(0, -0.14, "Early-life churn is 6× higher than customers with 5+ years tenure",
            transform=ax.transAxes, color=COLORS["neutral"], fontsize=9)
    ax.grid(axis="y", alpha=0.3)
    ax.grid(axis="x", visible=False)

    save("02_churn_by_tenure.png")


# ---------------------------------------------------------------------------
# Chart 3 — Churn Rate by Customer Value Segment
# ---------------------------------------------------------------------------
def chart_churn_by_value() -> None:
    df = pd.read_csv(DATA_DIR / "churn_by_value.csv")
    df = df.sort_values("churn_rate", ascending=False)

    bar_colors = [
        COLORS["danger"] if r > 35 else COLORS["warning"] if r > 22 else COLORS["success"]
        for r in df["churn_rate"]
    ]

    fig, ax = plt.subplots(figsize=(8, 4))
    bars = ax.bar(df["customer_value_segment"], df["churn_rate"],
                  color=bar_colors, width=0.5)

    for bar, val, n in zip(bars, df["churn_rate"], df["customers"]):
        ax.text(bar.get_x() + bar.get_width() / 2, bar.get_height() + 0.5,
                f"{val:.1f}%", ha="center", fontweight="bold")
        ax.text(bar.get_x() + bar.get_width() / 2, bar.get_height() / 2,
                f"n={n:,}", ha="center", color="white", fontsize=8.5)

    ax.set_ylabel("Churn Rate (%)")
    ax.set_ylim(0, 52)
    ax.set_title("Churn Rate by Customer Value Segment", fontsize=14, fontweight="bold", pad=12)
    ax.text(0, -0.14, "Low-value customers churn at 3× the rate of very high-value customers",
            transform=ax.transAxes, color=COLORS["neutral"], fontsize=9)

    save("03_churn_by_value_segment.png")


# ---------------------------------------------------------------------------
# Chart 4 — Feature Importance (Permutation)
# ---------------------------------------------------------------------------
def chart_feature_importance() -> None:
    df = pd.read_csv(REPORTS_DIR / "05_perm_importance.csv")
    df = df.sort_values("importance_mean", ascending=True).tail(10)

    bar_colors = [
        COLORS["primary"] if i >= 7 else COLORS["neutral"]
        for i in range(len(df))
    ]

    fig, ax = plt.subplots(figsize=(8, 5))
    bars = ax.barh(df["feature"], df["importance_mean"],
                   xerr=df["importance_std"], color=bar_colors,
                   capsize=3, height=0.55, error_kw={"elinewidth": 1})

    ax.set_xlabel("Permutation Importance (ROC-AUC drop)")
    ax.set_title("Top 10 Churn Prediction Features", fontsize=14, fontweight="bold", pad=12)
    ax.text(0, -0.12,
            "HGB Calibrated Model | ROC-AUC: 0.8448 | Error bars = ±1 std across 10 permutations",
            transform=ax.transAxes, color=COLORS["neutral"], fontsize=8.5)

    blue_patch = mpatches.Patch(color=COLORS["primary"], label="Top 3 features")
    ax.legend(handles=[blue_patch], loc="lower right", fontsize=9)

    save("04_feature_importance.png")


# ---------------------------------------------------------------------------
# Chart 5 — Customer Risk Band Distribution (donut)
# ---------------------------------------------------------------------------
def chart_risk_distribution() -> None:
    df = pd.read_csv(DATA_DIR / "risk_band_summary.csv")
    order = ["Critical", "High", "Medium", "Low"]
    df["risk_band"] = pd.Categorical(df["risk_band"], categories=order, ordered=True)
    df = df.sort_values("risk_band")

    sizes  = df["customers"].values
    labels = df["risk_band"].values
    colors = [RISK_COLORS[b] for b in labels]
    actual = df["actual_churn_rate"].values

    legend_labels = [
        f"{b}  ({n:,} customers, {a:.0f}% actual churn)"
        for b, n, a in zip(labels, sizes, actual)
    ]

    fig, ax = plt.subplots(figsize=(8, 5))
    wedges, _ = ax.pie(
        sizes, colors=colors,
        wedgeprops={"width": 0.5, "edgecolor": "white", "linewidth": 2},
        startangle=90,
    )
    ax.text(0, 0, f"7,043\ntotal\ncustomers", ha="center", va="center",
            fontsize=11, fontweight="bold", color="#1F2937")

    ax.legend(wedges, legend_labels, loc="lower center",
              bbox_to_anchor=(0.5, -0.18), ncol=1, fontsize=9)
    ax.set_title("Customer Distribution by Predicted Risk Band",
                 fontsize=14, fontweight="bold", pad=12)

    save("05_risk_band_distribution.png")


# ---------------------------------------------------------------------------
# Chart 6 — Revenue at Risk
# ---------------------------------------------------------------------------
def chart_revenue_at_risk() -> None:
    rev = pd.read_csv(DATA_DIR / "revenue_summary.csv")
    total   = float(rev["total_revenue"].iloc[0])
    at_risk = float(rev["revenue_at_risk"].iloc[0])
    safe    = total - at_risk

    fig, ax = plt.subplots(figsize=(7, 4))
    bars = ax.barh(
        ["Monthly Revenue"],
        [safe],
        color=COLORS["success"], label=f"Safe  ${safe/1e6:.2f}M", height=0.4
    )
    ax.barh(
        ["Monthly Revenue"],
        [at_risk],
        left=[safe],
        color=COLORS["danger"], label=f"At Risk  ${at_risk/1e6:.2f}M", height=0.4
    )

    ax.text(safe / 2, 0, f"${safe/1e6:.2f}M\nRetained", ha="center", va="center",
            color="white", fontweight="bold", fontsize=10)
    ax.text(safe + at_risk / 2, 0, f"${at_risk/1e6:.2f}M\nAt Risk", ha="center", va="center",
            color="white", fontweight="bold", fontsize=10)

    ax.set_xlim(0, total * 1.02)
    ax.set_xlabel("Monthly Revenue ($)")
    ax.get_yaxis().set_visible(False)
    ax.legend(loc="upper right", fontsize=10)
    ax.set_title("Monthly Revenue at Risk from Predicted Churn",
                 fontsize=14, fontweight="bold", pad=12)
    ax.text(0, -0.18,
            f"${at_risk/1e6:.2f}M of ${total/1e6:.2f}M total monthly revenue "
            f"({at_risk/total*100:.1f}%) is at risk of loss",
            transform=ax.transAxes, color=COLORS["neutral"], fontsize=9)

    save("06_revenue_at_risk.png")


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------
if __name__ == "__main__":
    print("Generating charts...\n")
    chart_churn_by_contract()
    chart_churn_by_tenure()
    chart_churn_by_value()
    chart_feature_importance()
    chart_risk_distribution()
    chart_revenue_at_risk()
    print(f"\nAll 6 charts saved to: {SCRIPT_DIR}")
