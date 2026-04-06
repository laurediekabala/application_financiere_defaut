import numpy as np
import pandas as pd
from app.services.model_service import get_model

def explain_prediction_local(X_new: pd.DataFrame, top_n: int = 5):
    pipeline = get_model()
    steps = pipeline.named_steps
    final_model = list(steps.values())[-1]

    if not hasattr(final_model, "coef_"):
        return {
            "top_facteurs_hausse_risque": [],
            "top_facteurs_baisse_risque": [],
            "message": "Explicabilité locale détaillée disponible uniquement pour la régression logistique."
        }

    coefs = final_model.coef_[0]

    transformed = X_new.copy()
    for _, step_obj in list(steps.items())[:-1]:
        transformed = step_obj.transform(transformed)

    transformed = np.array(transformed).reshape(1, -1)

    feature_names = np.array(X_new.columns)

    first_step = list(steps.values())[0]
    try:
        feature_names = first_step.get_feature_names_out(X_new.columns)
    except:
        pass

    for step in steps.values():
        if hasattr(step, "get_support"):
            feature_names = np.array(feature_names)[step.get_support()]
            break

    contributions = transformed[0] * coefs

    contrib_df = pd.DataFrame({
        "feature": feature_names,
        "value_transformed": transformed[0],
        "coefficient": coefs,
        "contribution": contributions
    })

    positive = contrib_df.sort_values("contribution", ascending=False).head(top_n)
    negative = contrib_df.sort_values("contribution", ascending=True).head(top_n)

    return {
        "top_facteurs_hausse_risque": positive[["feature", "contribution"]].round(4).to_dict(orient="records"),
        "top_facteurs_baisse_risque": negative[["feature", "contribution"]].round(4).to_dict(orient="records")
    }