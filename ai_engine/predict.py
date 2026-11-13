import os
import joblib
import numpy as np
from datetime import datetime, timedelta

MODEL_PATH = os.path.join(os.path.dirname(__file__), "model.pkl")
_cached = None


def _load():
    global _cached
    if _cached is None:
        if not os.path.exists(MODEL_PATH):
            from ai_engine.train import train
            train()
        _cached = joblib.load(MODEL_PATH)
    return _cached


def _compute_features(user_id, action, patient_id=None):
    """Compute behavioural features from the DB."""
    from models.models import AccessLog, db
    from sqlalchemy import func

    now = datetime.utcnow()
    one_hour_ago = now - timedelta(hours=1)
    one_day_ago = now - timedelta(days=1)

    last_hour_count = db.session.query(func.count(AccessLog.id)).filter(
        AccessLog.user_id == user_id,
        AccessLog.timestamp >= one_hour_ago,
    ).scalar() or 0

    distinct_patients = db.session.query(
        func.count(func.distinct(AccessLog.patient_id))
    ).filter(
        AccessLog.user_id == user_id,
        AccessLog.timestamp >= one_day_ago,
        AccessLog.patient_id.isnot(None),
    ).scalar() or 0

    failed_logins = db.session.query(func.count(AccessLog.id)).filter(
        AccessLog.user_id == user_id,
        AccessLog.timestamp >= one_hour_ago,
        AccessLog.status == "FAILED",
    ).scalar() or 0

    action_freq = db.session.query(func.count(AccessLog.id)).filter(
        AccessLog.user_id == user_id,
        AccessLog.action == action,
        AccessLog.timestamp >= one_day_ago,
    ).scalar() or 0

    is_outside = 1 if (now.hour < 8 or now.hour >= 18 or now.weekday() >= 5) else 0

    return {
        "hour_of_day": now.hour,
        "day_of_week": now.weekday(),
        "records_accessed_last_hour": int(last_hour_count),
        "distinct_patients_last_day": int(distinct_patients),
        "failed_logins_last_hour": int(failed_logins),
        "is_outside_business_hours": is_outside,
        "action_frequency": int(action_freq),
    }


def predict_risk(user_id, action, patient_id=None):
    """
    Returns (risk_score 0-100, is_anomaly bool, reasons list).
    Does NOT block access — only flags for Admin investigation.
    """
    bundle = _load()
    model = bundle["model"]
    features = bundle["features"]
    feats = _compute_features(user_id, action, patient_id)
    X = np.array([[feats[f] for f in features]])

    # decision_function returns higher = more normal
    raw = float(model.decision_function(X)[0])
    pred = int(model.predict(X)[0])  # -1 = anomaly, 1 = normal

    # Map raw score to 0-100 risk
    risk_score = max(0.0, min(100.0, (0.2 - raw) * 100.0))
    is_anomaly = pred == -1

    reasons = []
    if feats["is_outside_business_hours"]:
        reasons.append("Access outside business hours")
    if feats["failed_logins_last_hour"] >= 3:
        reasons.append(f"{feats['failed_logins_last_hour']} failed logins in last hour")
    if feats["records_accessed_last_hour"] >= 25:
        reasons.append(f"{feats['records_accessed_last_hour']} records accessed in last hour")
    if feats["distinct_patients_last_day"] >= 30:
        reasons.append(f"{feats['distinct_patients_last_day']} distinct patients accessed in last day")

    if not reasons:
        reasons.append("Isolation Forest flagged unusual feature combination")

    return risk_score, is_anomaly, reasons, feats