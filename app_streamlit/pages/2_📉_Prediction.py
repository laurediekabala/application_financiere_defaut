import streamlit as st
import pandas as pd
import plotly.graph_objects as go
from utils.api_client import call_prediction_api
from utils.helpers import risk_color
from utils.alerte import show_alert
import os 
def load_css():
    current_dir = os.path.dirname(os.path.abspath(__file__))      # .../app_streamlit/pages
    app_dir = os.path.dirname(current_dir)                       # .../app_streamlit
    css_path = os.path.join(app_dir, "assets", "style.css")

    with open(css_path, "r", encoding="utf-8") as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

load_css()

st.title("📉 Prédiction du défaut")

st.markdown("Saisissez les informations de l'entreprise puis lancez l'analyse.")

col1, col2, col3 = st.columns(3)

with col1:
    entreprise = st.text_input("Entreprise", value="AgroBiz")
    secteur = st.selectbox("Secteur", ["Agroalimentaire", "Télécom", "Banque", "Mines","Transport","Pharmaceutique","Construction","Energie"])
    annee = st.number_input("Année", min_value=2000, max_value=2030, value=2025)

with col2:
    exposition = st.number_input("Exposition (EAD)", min_value=0.0, value=1000000.0)
    garantie_ratio = st.number_input("Garantie ratio", min_value=0.0, max_value=1.0, value=0.10)
    CA = st.number_input("CA", min_value=0.0, value=4979437.91)
with col3: 
    ratio_marge = st.number_input("Ratio marge", value=26.05)
    ratio_endettement = st.number_input("Ratio endettement", value=32.50)
    ratio_rentabilite = st.number_input("Ratio rentabilité", value=13.87)   

st.subheader("Ratios")

r1, r2= st.columns(2) 
with r1:
      distress_score = st.selectbox("détresse financière",[0,1,2,3,4,5])
      default_flag = st.selectbox("risque", [0,1])
with r2:
    ratio_solvabilite = st.number_input("Ratio solvabilité", value=207.73)
    ratio_liquidite = st.number_input("Ratio liquidité", value=307.73)
    ratio_ci = st.number_input("Ratio CI", value=35.23)

   

payload = {
    "annee": annee,
    "entreprise": entreprise,
    "secteur": secteur,
    "CA": CA,
    "charges": 600000.1,
    "resultat_net": 600000.2,
    "actifs": 600000.3,
    "passifs": 600000.4,
    "capitaux_propres": 600000.1,
    "flux_operationnel": 600000.2,
    "flux_investissement": 561547.02,
    "flux_financement": 150000.00,
    "ratio_marge": ratio_marge,
    "ratio endettement": ratio_endettement,
    "ratio rentabilité": ratio_rentabilite,
    "ratio de solvabilité": ratio_solvabilite,
    "ratio de liquidité": ratio_liquidite,
    "ratio_ci": ratio_ci,
    "ratio_cf": 600000.3,
    "ratio_cf_invest": 600000.4,
    "delta_liquidite": 600000.5,
    "delta_endettement": 600000.6,
    "delta_rentabilite": 600000.7,
    "delta_marge": 600000.8,
     "distress_score":distress_score,
    "default_flag" :default_flag,
    "exposition": exposition,
    "garantie_ratio": garantie_ratio
}

if st.button("🚀 Lancer la prédiction", use_container_width=True):
    try:
        result = call_prediction_api(payload)["data"]
        st.session_state["last_prediction"] = result

        st.success("Analyse réalisée avec succès.")

        c1, c2, c3, c4 = st.columns([2.5, 2.5, 2.5, 4])
        c1.metric("Probabilité défaut", f"{result['probabilite_defaut_annee_prochaine']*100:.2f}%")
        c2.metric("Niveau risque", result["niveau_risque"].capitalize())
        
        c3.metric("Décision", result["decision_metier"])
        c4.metric("Expected Loss", f"{result['parametres_risque']['expected_loss']:,.2f}")

        fig = go.Figure(go.Indicator(
            mode="gauge+number",
            value=result["probabilite_defaut_annee_prochaine"] * 100,
            title={'text': "Score de risque"},
            gauge={
                'axis': {'range': [0, 100]},
                'steps': [
                    {'range': [0, 20], 'color': "#2ecc71"},
                    {'range': [20, 50], 'color': "#f1c40f"},
                    {'range': [50, 75], 'color': "#e67e22"},
                    {'range': [75, 100], 'color': "#e74c3c"}
                ],
                'bar': {'color': "black"}
            }
        ))
        st.plotly_chart(fig, use_container_width=True)

    except Exception as e:
        show_alert(f"Erreur : {e}", alert_type="error")