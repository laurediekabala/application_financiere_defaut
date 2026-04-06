import joblib
import pandas as pd
from flask import current_app

_model = None
_explain = None
_metadata = None

def load_artifacts():
    global _model, _explain, _metadata

    if _model is None:
        _model = joblib.load(current_app.config["MODEL_PATH"])
        _explain = joblib.load(current_app.config["EXPLAIN_PATH"])
        _metadata = joblib.load(current_app.config["METADATA_PATH"])

def get_model():
    load_artifacts()
    return _model

def get_explain():
    load_artifacts()
    return _explain

def get_metadata():
    load_artifacts()
    return _metadata

def predict_company(data: dict):
    model = get_model()
    metadata = get_metadata()

    df = pd.DataFrame([data])

    expected_features = metadata["features_entree"]
    missing_cols = [col for col in expected_features if col not in df.columns]
    if missing_cols:
        raise ValueError(f"Colonnes manquantes : {missing_cols}")

    df = df[expected_features]

    pred = int(model.predict(df)[0])
    proba = float(model.predict_proba(df)[0, 1])

    return pred, proba, df