import streamlit as st
import pandas as pd
import plotly.express as px
from utils.nettoyer import clean_feature_names
import os 
def load_css():
    current_dir = os.path.dirname(os.path.abspath(__file__))      # .../app_streamlit/pages
    app_dir = os.path.dirname(current_dir)                       # .../app_streamlit
    css_path = os.path.join(app_dir, "assets", "style.css")

    with open(css_path, "r", encoding="utf-8") as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

load_css()
st.title("🧠 Explicabilité")

if "last_prediction" not in st.session_state:
    st.warning("Aucune prédiction disponible. Veuillez d'abord lancer une analyse depuis la page Prédiction.")
else:
    result = st.session_state["last_prediction"]

    st.subheader("Résumé")
    st.write(f"**Entreprise** : {result['entreprise']}")
    st.write(f"**Probabilité de défaut** : {result['probabilite_defaut_annee_prochaine']*100:.2f}%")
    st.write(f"**Niveau de risque** : {result['niveau_risque']}")

    col1, col2 = st.columns(2)

    with col1:
        st.markdown("### 🔺 Facteurs qui augmentent le risque")
        pos_df = pd.DataFrame(result["explicabilite"]["top_facteurs_hausse_risque"])
        pos_df["feature"] = clean_feature_names(pos_df["feature"])
        if not pos_df.empty:
            st.dataframe(pos_df, use_container_width=True)
            fig_pos = px.bar(
                pos_df.sort_values("contribution"),
                x="contribution",
                y="feature",
                orientation="h",
                color="contribution",
                color_continuous_scale="Reds"
            )
            st.plotly_chart(fig_pos, use_container_width=True)
        else:
            st.info("Pas de facteurs disponibles.")

    with col2:
        st.markdown("### 🔻 Facteurs qui réduisent le risque")
        neg_df = pd.DataFrame(result["explicabilite"]["top_facteurs_baisse_risque"])
        neg_df["feature"] = clean_feature_names(neg_df["feature"])
        if not neg_df.empty:
            st.dataframe(neg_df, use_container_width=True)
            fig_neg = px.bar(
                neg_df.sort_values("contribution"),
                x="contribution",
                y="feature",
                orientation="h",
                color="contribution",
                color_continuous_scale="Greens"
            )
            st.plotly_chart(fig_neg, use_container_width=True)
        else:
            st.info("Pas de facteurs disponibles.")