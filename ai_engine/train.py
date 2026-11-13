"""
Train Isolation Forest on synthetic behavioural features derived from
access_logs patterns. Model is saved to ai_engine/model.pkl.
Run once:  python -m ai_engine.train
"""
import os
import numpy as np
import pandas as pd
import joblib
from sklearn.ensemble import IsolationForest

MODEL_PATH = os.path.join(os.path.dirname(__file__), "model.pkl")

FEATURES = [
    "hour_of_day",
    "day_of_week",
    "records_accessed_last_hour",
    "distinct_patients_last_day",
    "failed_logins_last_hour",
    "is_outside_business_hours",
    "action_frequency",
]


def _synthetic_training_set(n=2000, seed=42):
    rng = np.random.default_rng(seed)
    # 95% normal, 5% anomaly
    n_normal = int(n * 0.95)
    n_anom = n - n_normal

    normal = pd.DataFrame({
        "hour_of_day": rng.integers(8, 18, n_normal),
        "day_of_week": rng.integers(0, 5, n_normal),
        "records_accessed_last_hour": rng.integers(1, 10, n_normal),
        "distinct_patients_last_day": rng.integers(1, 15, n_normal),
        "failed_logins_last_hour": rng.integers(0, 2, n_normal),
        "is_outside_business_hours": rng.integers(0, 1, n_normal),
        "action_frequency": rng.integers(20, 200, n_normal),
    })

    anomalies = pd.DataFrame({
        "hour_of_day": rng.integers(0, 6, n_anom),
        "day_of_week": rng.integers(0, 7, n_anom),
        "records_accessed_last_hour": rng.integers(30, 200, n_anom),
        "distinct_patients_last_day": rng.integers(30, 300, n_anom),
        "failed_logins_last_hour": rng.integers(3, 20, n_anom),
        "is_outside_business_hours": np.ones(n_anom, dtype=int),
        "action_frequency": rng.integers(1, 10, n_anom),
    })

    return pd.concat([normal, anomalies], ignore_index=True)


def train():
    df = _synthetic_training_set()
    X = df[FEATURES].values
    model = IsolationForest(
        n_estimators=200,
        contamination=0.05,
        random_state=42,
    )
    model.fit(X)
    joblib.dump({"model": model, "features": FEATURES}, MODEL_PATH)
    print(f"[OK] Isolation Forest trained on {len(df)} samples -> {MODEL_PATH}")


if __name__ == "__main__":
    train()