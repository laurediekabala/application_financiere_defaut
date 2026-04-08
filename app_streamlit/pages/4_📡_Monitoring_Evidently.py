import os
import streamlit as st
import pandas as pd
import streamlit.components.v1 as components
from evidently.report import Report
from evidently.metric_preset import DataDriftPreset, DataQualityPreset

st.set_page_config(page_title="Monitoring Evidently", layout="wide")
def load_css():
    current_dir = os.path.dirname(os.path.abspath(__file__))      # .../app_streamlit/pages
    app_dir = os.path.dirname(current_dir)                       # .../app_streamlit
    css_path = os.path.join(app_dir, "assets", "style.css")

    with open(css_path, "r", encoding="utf-8") as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

load_css()
st.title("📡 Monitoring du modèle avec Evidently")

st.markdown("""
Cette page permet de surveiller :
- la dérive des données,
- la qualité des données,
- les variables les plus instables,
- le niveau d’alerte global du modèle.
""")

# ============================================================
# 1. CHEMINS
# ============================================================
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
APP_DIR = os.path.dirname(BASE_DIR)
DATA_DIR = os.path.join(APP_DIR, "dataset")

reference_path = os.path.join(DATA_DIR, "train.csv")
current_path = os.path.join(DATA_DIR, "test.csv")

# ============================================================
# 2. VÉRIFICATION DES FICHIERS
# ============================================================
if not os.path.exists(reference_path):
    st.error(f"❌ Fichier de référence introuvable : {reference_path}")
    st.stop()

if not os.path.exists(current_path):
    st.error(f"❌ Fichier courant introuvable : {current_path}")
    st.stop()

# ============================================================
# 3. CHARGEMENT ET NETTOYAGE
# ============================================================
reference_data = pd.read_csv(reference_path)
current_data = pd.read_csv(current_path)

# Supprimer colonnes parasites
reference_data = reference_data.drop(columns=["Unnamed: 0"], errors="ignore")
current_data = current_data.drop(columns=["Unnamed: 0"], errors="ignore")
features_model = [
    "ratio rentabilité", "ratio de solvabilité", "ratio de liquidité",
    "ratio_ci","ratio_marge","ratio endettement","default_flag","distress_score"]

reference_data = reference_data[[c for c in features_model if c in reference_data.columns]]
current_data = current_data[[c for c in features_model if c in current_data.columns]]

# Garder uniquement les colonnes communes
common_cols = [col for col in reference_data.columns if col in current_data.columns]
reference_data = reference_data[common_cols]
current_data = current_data[common_cols]

st.subheader("📂 Aperçu des datasets")
col1, col2 = st.columns(2)

with col1:
    st.write("### Référence")
    st.write(f"**Lignes :** {reference_data.shape[0]} | **Colonnes :** {reference_data.shape[1]}")
    st.dataframe(reference_data.head(), use_container_width=True)

with col2:
    st.write("### Courant")
    st.write(f"**Lignes :** {current_data.shape[0]} | **Colonnes :** {current_data.shape[1]}")
    st.dataframe(current_data.head(), use_container_width=True)

# ============================================================
# 4. RAPPORT EVIDENTLY
# ============================================================
with st.spinner("⏳ Génération du rapport Evidently en cours..."):
    report = Report(metrics=[
        DataDriftPreset(),
        DataQualityPreset()
    ])

    report.run(
        reference_data=reference_data,
        current_data=current_data
    )

# Export dict pour lecture structurée
report_dict = report.as_dict()

# ============================================================
# 5. EXTRACTION DES INFOS CLÉS
# ============================================================
drift_data = None
for metric in report_dict["metrics"]:
    if metric["metric"] == "DataDriftTable":
        drift_data = metric["result"]
        break

if drift_data is None:
    st.error("Impossible d'extraire les résultats de drift depuis Evidently.")
    st.stop()

n_cols = drift_data["number_of_columns"]
n_drifted = drift_data["number_of_drifted_columns"]
share_drifted = n_drifted / n_cols if n_cols > 0 else 0

drift_by_columns = drift_data["drift_by_columns"]

# Convertir en DataFrame
drift_rows = []
for col_name, col_info in drift_by_columns.items():
    drift_rows.append({
        "feature": col_name,
        "column_type": col_info.get("column_type"),
        "drift_detected": col_info.get("drift_detected"),
        "stattest_name": col_info.get("stattest_name"),
        "drift_score": col_info.get("drift_score")
    })

drift_df = pd.DataFrame(drift_rows)

# Tri : drift d'abord, puis score croissant
drift_df = drift_df.sort_values(
    by=["drift_detected", "drift_score"],
    ascending=[False, True]
).reset_index(drop=True)

# ============================================================
# 6. NIVEAU D'ALERTE
# ============================================================
if share_drifted < 0.20:
    alert_level = "🟢 FAIBLE"
    alert_color = "green"
    alert_message = "Le dataset courant reste globalement proche du dataset de référence."
elif share_drifted < 0.50:
    alert_level = "🟠 MODÉRÉ"
    alert_color = "orange"
    alert_message = "Une dérive significative apparaît sur plusieurs variables. Le modèle doit être surveillé."
else:
    alert_level = "🔴 ÉLEVÉ"
    alert_color = "red"
    alert_message = "La dérive est importante. Le modèle peut être exposé à une baisse de fiabilité."

# ============================================================
# 7. KPI
# ============================================================
st.subheader("🚨 Indicateurs de monitoring")

k1, k2, k3, k4 = st.columns(4)
k1.metric("Variables totales", n_cols)
k2.metric("Variables en drift", n_drifted)
k3.metric("Part en drift", f"{share_drifted:.1%}")
k4.metric("Niveau d’alerte", alert_level)

st.markdown(f"### <span style='color:{alert_color}'>{alert_message}</span>", unsafe_allow_html=True)

# ============================================================
# 8. RÉSUMÉ AUTOMATIQUE
# ============================================================
st.subheader("📝 Synthèse automatique")

top_drift_features = drift_df[drift_df["drift_detected"] == True]["feature"].head(5).tolist()

if len(top_drift_features) == 0:
    st.success(
        "Aucune dérive significative n’a été détectée sur les variables analysées. "
        "Le modèle semble opérer dans un environnement de données stable."
    )
else:
    st.warning(
        f"""
        Une dérive a été détectée sur **{n_drifted} variables sur {n_cols}**, soit **{share_drifted:.1%}** des colonnes.
        
        Les variables les plus sensibles sont :
        **{', '.join(top_drift_features)}**.
        
        Cela signifie que les données courantes s’éloignent de la distribution du jeu de référence.
        Une surveillance renforcée du modèle est recommandée, et un recalibrage ou réentraînement
        peut devenir nécessaire si cette dérive persiste.
        """
    )

# ============================================================
# 9. TABLEAU DES VARIABLES EN DRIFT
# ============================================================
st.subheader("🔥 Variables les plus en drift")

only_drifted = drift_df[drift_df["drift_detected"] == True].copy()

if only_drifted.empty:
    st.info("Aucune variable en drift détectée.")
else:
    st.dataframe(only_drifted.head(15), use_container_width=True)

# ============================================================
# 10. TOP VARIABLES STABLES
# ============================================================
st.subheader("✅ Variables les plus stables")

stable_df = drift_df[drift_df["drift_detected"] == False].copy()

if stable_df.empty:
    st.info("Aucune variable stable détectée.")
else:
    st.dataframe(stable_df.head(10), use_container_width=True)

# ============================================================
# 11. RAPPORT HTML EVIDENTLY
# ============================================================
st.subheader("📊 Rapport détaillé Evidently")

html = report.get_html()
components.html(html, height=1200, scrolling=True)