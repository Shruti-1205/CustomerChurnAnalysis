"""
Train and save the customer churn model.

Replicates the pipeline from notebooks/05_churn_model.ipynb using the
best hyperparameters found via RandomizedSearchCV, fits on the full
dataset, then saves model artifacts for use by the Streamlit app.

Usage:
    python models/train_and_save.py
"""

import json
from pathlib import Path

import joblib
import pandas as pd
from sklearn.calibration import CalibratedClassifierCV
from sklearn.compose import ColumnTransformer
from sklearn.ensemble import HistGradientBoostingClassifier
from sklearn.impute import SimpleImputer
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder, StandardScaler

# ---------------------------------------------------------------------------
# Paths
# ---------------------------------------------------------------------------
PROJECT_ROOT = Path(__file__).parent.parent
PROCESSED_DIR = PROJECT_ROOT / "data" / "processed"
MODELS_DIR = Path(__file__).parent

DATA_PATH = PROCESSED_DIR / "analytics_ready_churn_data.csv"
MODEL_PATH = MODELS_DIR / "churn_model.pkl"
META_PATH = MODELS_DIR / "model_metadata.json"

# ---------------------------------------------------------------------------
# Load data (already cleaned + feature-engineered by notebooks 02 & 03)
# ---------------------------------------------------------------------------
print("Loading data...")
df = pd.read_csv(DATA_PATH)
print(f"  {df.shape[0]:,} rows, {df.shape[1]} columns")

drop_cols = [c for c in df.columns if c.lower() in ["customerid", "customer_id"]]
X = df.drop(columns=["Churn"] + drop_cols)
y = df["Churn"].astype(int)

print(f"  Features: {X.shape[1]} | Target churn rate: {y.mean():.2%}")

# ---------------------------------------------------------------------------
# Feature identification (mirrors notebook 05 logic exactly)
# ---------------------------------------------------------------------------
numeric_features = [c for c in X.columns if pd.api.types.is_numeric_dtype(X[c])]
categorical_features = [c for c in X.columns if c not in numeric_features]

print(f"  Numeric features ({len(numeric_features)}): {numeric_features}")
print(f"  Categorical features ({len(categorical_features)}): {categorical_features}")

# ---------------------------------------------------------------------------
# Preprocessing pipeline
# ---------------------------------------------------------------------------
numeric_transformer = Pipeline(steps=[
    ("imputer", SimpleImputer(strategy="median")),
    ("scaler", StandardScaler()),
])

categorical_transformer = Pipeline(steps=[
    ("imputer", SimpleImputer(strategy="most_frequent")),
    ("onehot", OneHotEncoder(handle_unknown="ignore")),
])

preprocess = ColumnTransformer(transformers=[
    ("num", numeric_transformer, numeric_features),
    ("cat", categorical_transformer, categorical_features),
], remainder="drop")

# ---------------------------------------------------------------------------
# Model — best hyperparameters from notebook 05 RandomizedSearchCV
# ---------------------------------------------------------------------------
hgb = HistGradientBoostingClassifier(
    random_state=42,
    learning_rate=0.03,
    max_depth=2,
    max_leaf_nodes=31,
    min_samples_leaf=10,
    l2_regularization=1.0,
    max_iter=400,
)

hgb_pipe = Pipeline(steps=[
    ("preprocess", preprocess),
    ("model", hgb),
])

calibrated_model = CalibratedClassifierCV(
    estimator=hgb_pipe,
    method="isotonic",
    cv=3,
)

# ---------------------------------------------------------------------------
# Fit on full dataset (same as final_model.fit(X, y) in notebook 05)
# ---------------------------------------------------------------------------
print("\nTraining calibrated HGB model on full dataset...")
calibrated_model.fit(X, y)
print("  Training complete.")

# ---------------------------------------------------------------------------
# Save model artifact
# ---------------------------------------------------------------------------
joblib.dump(calibrated_model, MODEL_PATH)
print(f"\nModel saved: {MODEL_PATH}")

# ---------------------------------------------------------------------------
# Save metadata
# ---------------------------------------------------------------------------
# Store TotalCharges quartile boundaries so the Streamlit predictor can
# replicate the customer_value_segment logic from notebook 03 (pd.qcut)
tc_quantiles = df["TotalCharges"].quantile([0.25, 0.5, 0.75]).tolist()

metadata = {
    "model_name": "HGB_tuned_calibrated",
    "threshold": 0.31434675005907337,
    "roc_auc": 0.8448,
    "avg_precision": 0.6532,
    "total_charges_quantiles": tc_quantiles,
    "numeric_features": numeric_features,
    "categorical_features": categorical_features,
    "feature_columns": list(X.columns),
}

with open(META_PATH, "w") as f:
    json.dump(metadata, f, indent=2)

print(f"Metadata saved: {META_PATH}")
print("\nDone. Artifacts created:")
print(f"  {MODEL_PATH.relative_to(PROJECT_ROOT)}")
print(f"  {META_PATH.relative_to(PROJECT_ROOT)}")
