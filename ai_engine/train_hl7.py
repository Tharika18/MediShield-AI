
import os
import json
import joblib
import pandas as pd

from sklearn.model_selection import train_test_split
from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import OneHotEncoder, StandardScaler
from sklearn.pipeline import Pipeline
from sklearn.impute import SimpleImputer
from sklearn.ensemble import RandomForestClassifier, IsolationForest
from sklearn.metrics import (
    accuracy_score,
    precision_score,
    recall_score,
    f1_score,
    classification_report,
    confusion_matrix
)

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_DIR = os.path.join(BASE_DIR, "datasets", "emr")
MODEL_DIR = os.path.join(BASE_DIR, "ai_engine", "saved_models")

os.makedirs(MODEL_DIR, exist_ok=True)

def load_data():
    normal = pd.read_csv(
        os.path.join(DATA_DIR, "payload-normal.csv"),
        low_memory=False
    )

    anomaly = pd.read_csv(
        os.path.join(DATA_DIR, "payload-anomaly.csv"),
        low_memory=False
    )

    normal = normal.dropna(subset=["MSGTYPE", "PATIENTID"]).copy()
    anomaly = anomaly.dropna(subset=["MSGTYPE", "PATIENTID"]).copy()

    normal["label"] = 0
    anomaly["label"] = 1

    data = pd.concat([normal, anomaly], ignore_index=True)

    return data

def train():
    print("Loading healthcare message datasets...")
    data = load_data()

    # Use message-related features, not personal patient details.
    features = data[["MSGTYPE"]].copy()
    labels = data["label"]

    X_train, X_test, y_train, y_test = train_test_split(
        features,
        labels,
        test_size=0.25,
        random_state=42,
        stratify=labels
    )

    preprocessing = ColumnTransformer([
        (
            "message_type",
            OneHotEncoder(handle_unknown="ignore"),
            ["MSGTYPE"]
        )
    ])

    model = Pipeline([
        ("preprocessing", preprocessing),
        (
            "classifier",
            RandomForestClassifier(
                n_estimators=150,
                random_state=42,
                class_weight="balanced"
            )
        )
    ])

    print("Training Random Forest...")
    model.fit(X_train, y_train)

    predictions = model.predict(X_test)

    results = {
        "accuracy": round(float(accuracy_score(y_test, predictions)), 4),
        "precision": round(float(precision_score(
            y_test, predictions, zero_division=0
        )), 4),
        "recall": round(float(recall_score(
            y_test, predictions, zero_division=0
        )), 4),
        "f1_score": round(float(f1_score(
            y_test, predictions, zero_division=0
        )), 4),
        "confusion_matrix": confusion_matrix(
            y_test, predictions
        ).tolist(),
        "normal_records": int((labels == 0).sum()),
        "anomaly_records": int((labels == 1).sum()),
        "test_records": int(len(y_test)),
        "feature_used": ["MSGTYPE"],
        "purpose": "HL7 message anomaly classification"
    }

    model_path = os.path.join(MODEL_DIR, "hl7_anomaly_model.joblib")
    results_path = os.path.join(MODEL_DIR, "training_results.json")

    joblib.dump(model, model_path)

    with open(results_path, "w") as file:
        json.dump(results, file, indent=4)

    print("\nTRAINING COMPLETED")
    print(json.dumps(results, indent=4))
    print("\nModel saved:", model_path)
    print("Results saved:", results_path)

if __name__ == "__main__":
    train()
