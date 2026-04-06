import os

BASE_DIR = os.path.abspath(os.path.dirname(__file__))

class Config:
    MODEL_PATH = os.path.join(BASE_DIR, "models", "modele_logistique.joblib")
    EXPLAIN_PATH = os.path.join(BASE_DIR, "models", "explicabilite_logistique.joblib")
    METADATA_PATH = os.path.join(BASE_DIR, "models", "metadata_modele.pkl")
    DEBUG = True