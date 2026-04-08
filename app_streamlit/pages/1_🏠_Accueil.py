import streamlit as st
import os

st.title("🏠 Accueil")
def load_css():
    current_dir = os.path.dirname(os.path.abspath(__file__))      # .../app_streamlit/pages
    app_dir = os.path.dirname(current_dir)                       # .../app_streamlit
    css_path = os.path.join(app_dir, "assets", "style.css")

    with open(css_path, "r", encoding="utf-8") as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

load_css()

st.markdown("""
## Objectif de la plateforme

Cette application permet de :

- prédire la **probabilité de défaut à 12 mois** d'une entreprise,
- expliquer la prédiction du modèle,
- appliquer des **règles métier** de décision,
- calculer la **perte attendue**,
- surveiller le comportement du modèle avec **Evidently**.

## Modules disponibles

### 📉 Prédiction
Formulaire de saisie des données financières d'une entreprise.

### 🧠 Explicabilité
Visualisation des facteurs qui augmentent ou réduisent le risque.

### 📡 Monitoring
Suivi de la dérive des données et de la stabilité du modèle.
""")