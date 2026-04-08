import requests

#"http://127.0.0.1:5000/api/v1/predict"
API_URL ="https://application-financiere-defaut.onrender.com/api/v1/predict"

def call_prediction_api(payload: dict):
    response = requests.post(API_URL, json=payload, timeout=30)

    if response.status_code != 200:
        try:
            error_detail = response.json()
        except:
            error_detail = response.text
        raise Exception(f"Erreur API ({response.status_code}) : {error_detail}")

    return response.json()