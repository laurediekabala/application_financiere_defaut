from flask import Blueprint, jsonify, request
from app.services.model_service import predict_company
from app.services.explain_service import explain_prediction_local
from app.services.business_rules_service import (
    risk_level,
    business_decision,
    expected_loss
)

prediction_bp = Blueprint("prediction_bp", __name__)

@prediction_bp.route("/health", methods=["GET"])
def health():
    return jsonify({
        "status": "ok",
        "message": "API de prédiction du défaut disponible"
    }), 200


@prediction_bp.route("/predict", methods=["POST"])
def predict():
    try:
        payload = request.get_json()

        if payload is None:
            return jsonify({
                "status": "error",
                "message": "Le body JSON est vide ou invalide."
            }), 400

        pred, proba, df_input = predict_company(payload)

        secteur = payload.get("secteur", "unknown")
        exposition = payload.get("exposition", 0)
        garantie_ratio = payload.get("garantie_ratio", None)

        explication = explain_prediction_local(df_input, top_n=5)

        risk_params = expected_loss(
            prob_default=proba,
            exposition=exposition,
            secteur=secteur,
            garantie_ratio=garantie_ratio
        )

        response = {
            "status": "success",
            "data": {
                "entreprise": payload.get("entreprise"),
                "prediction_label": "defaut" if pred == 1 else "sain",
                "probabilite_defaut_annee_prochaine": round(proba, 4),
                "score_risque_sur_100": round(proba * 100, 2),
                "niveau_risque": risk_level(proba),
                "decision_metier": business_decision(proba),
                "parametres_risque": risk_params,
                "explicabilite": explication
            }
        }

        return jsonify(response), 200

    except Exception as e:
        return jsonify({
            "status": "error",
            "message": str(e)
        }), 400