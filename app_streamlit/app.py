import streamlit as st
import os

st.set_page_config(
    page_title="Credit Risk Monitoring",
    page_icon="📉",
    layout="wide",
    initial_sidebar_state="expanded"
)

def load_css():
    css_path = os.path.join(os.path.dirname(__file__), "assets", "style.css")
    with open(css_path, "r", encoding="utf-8") as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

load_css()

st.title("📉 Plateforme de prédiction du défaut d'entreprise")
st.markdown("""
Bienvenue dans la plateforme de scoring du risque de défaut.

Utilisez le menu latéral pour naviguer entre :
- l'accueil,
- la prédiction,
- l'explicabilité,
- le monitoring du modèle.
""")
st.markdown("""pour toute information complémentaire, contactez l'équipe de développement.:
- Gmail :laurediekabala@gmail.com,
- whattapp : +243814900752""")
          