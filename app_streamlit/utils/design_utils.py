import streamlit as st
import pandas as pd
import os

def inject_css(css_file_name="style.css"):
    """
    Injecte le fichier CSS spécifié dans l'application Streamlit.
    Le fichier CSS doit se trouver dans le même répertoire que le script appelant,
    ou le chemin complet doit être fourni.
    """
    current_dir = os.path.dirname(os.path.abspath(__file__))
    css_file_path = os.path.join(current_dir, "..", css_file_name)
    if os.path.exists(css_file_path):
        with open(css_file_path) as f:
            st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)
    else:
        st.warning(f"Fichier CSS non trouvé : {css_file_path}")


def highlight_values_gradient(s, cmap='viridis', low_is_bad=True):
    """
    Applique un dégradé de couleur à une série numérique,
    mettant en évidence les valeurs faibles/fortes.
    'low_is_bad=True' utilise des couleurs chaudes pour les valeurs faibles (rouge)
    et froides pour les valeurs fortes (vert).
    """
    if s.dtype == 'object' or not pd.api.types.is_numeric_dtype(s):
        return [''] * len(s)
    
    norm_s = (s - s.min()) / (s.max() - s.min())
    
    if low_is_bad: # Rouge pour les faibles, vert pour les fortes (ex: risque)
        colors = st.get_option("color.sequential") # Utilise la palette de Streamlit
        if colors:
             # Inverser le dégradé si low_is_bad pour avoir les faibles en 'mauvais' couleur
            # Streamlit palettes are generally from light to dark.
            # To make low values "bad" (red-ish), we need a specific cmap like 'RdYlGn_r'
            # For generic low_is_bad, RdYlGn_r or similar is good.
            return [f'background-color: {st.get_option("theme.base") == "dark" and "hsl(0, 100%, 30%, " or "hsl(0, 100%, 80%, "}{x})' for x in norm_s] # Placeholder, will use actual cmap in styler
        return s.apply(lambda x: f'background-color: {st.get_option("theme.base") == "dark" and "hsl(0, 100%, 30%, " or "hsl(0, 100%, 80%, "}{x})') # Fallback if no sequential colors

    # Pour les valeurs fortes (vert) et faibles (bleu/jaune) - ex: contributions positives
    return s.apply(lambda x: f'background-color: {st.get_option("theme.base") == "dark" and "hsl(120, 100%, 30%, " or "hsl(120, 100%, 80%, "}{x})') # Placeholder


def apply_dataframe_styling(df, columns_to_style=None, color_map='RdYlGn', low_is_bad=False, subset=None):
    """
    Applique un style de dégradé à un DataFrame.
    :param df: Le DataFrame à styliser.
    :param columns_to_style: Liste des colonnes numériques à styliser. Si None, toutes les numériques.
    :param color_map: La colormap à utiliser (ex: 'viridis', 'Reds', 'Greens', 'RdYlGn').
    :param low_is_bad: Si True, les valeurs faibles sont colorées comme "mauvaises" (plus chaudes/rouges).
    :param subset: Un sous-ensemble de colonnes/lignes à appliquer le style.
    :return: Le DataFrame stylisé.
    """
    if not isinstance(df, pd.DataFrame):
        return df # Retourne le DataFrame original si ce n'est pas un DataFrame

    numeric_cols = df.select_dtypes(include=['number']).columns.tolist()
    if columns_to_style:
        numeric_cols = [col for col in columns_to_style if col in numeric_cols]

    if not numeric_cols:
        return df.style.set_properties(**{'border-color': 'var(--border-color)', 'border-width': '1px', 'border-style': 'solid'})

    if low_is_bad:
        # Utilise un dégradé qui va du vert (bon) au rouge (mauvais) pour les valeurs faibles
        # Pour low_is_bad = True, on veut que le min soit rouge et le max vert.
        # Une colormap comme 'RdYlGn' ou 'YlGn_r' (inversée) peut fonctionner.
        # Ou 'Reds' inversée pour les faibles (faible = moins de rouge)
        return df.style.background_gradient(cmap=color_map, subset=subset).set_properties(**{'border-color': 'var(--border-color)', 'border-width': '1px', 'border-style': 'solid'})
    else:
        # Pour low_is_bad = False, on veut que le min soit vert et le max rouge.
        return df.style.background_gradient(cmap=color_map, subset=subset).set_properties(**{'border-color': 'var(--border-color)', 'border-width': '1px', 'border-style': 'solid'})


def style_risk_dataframe(df, value_col='contribution'):
    """Style un DataFrame de facteurs de risque (plus la contribution est haute, plus c'est rouge)."""
    if df.empty:
        return df
    return df.style.background_gradient(subset=[value_col], cmap='Reds').set_properties(**{'border-color': 'var(--border-color)', 'border-width': '1px', 'border-style': 'solid'})

def style_mitigating_dataframe(df, value_col='contribution'):
    """Style un DataFrame de facteurs atténuants (plus la contribution est basse/négative, plus c'est vert)."""
    if df.empty:
        return df
    # Pour les facteurs qui réduisent le risque, une contribution plus négative est "meilleure" (verte).
    # Si 'contribution' est toujours positive ici (juste des facteurs qui réduisent), on peut inverser la logique ou le cmap.
    # Assuming 'contribution' here is positive values representing reduction 'amount'.
    # If 'contribution' are negative values, then 'Greens_r' would be better.
    # Let's assume positive values, so higher value means more reduction.
    return df.style.background_gradient(subset=[value_col], cmap='Greens').set_properties(**{'border-color': 'var(--border-color)', 'border-width': '1px', 'border-style': 'solid'})

def style_drift_dataframe(df):
    """
    Applique un style spécifique aux DataFrames de dérive,
    mettant en évidence 'drift_detected' en vert/rouge et 'drift_score' en dégradé.
    """
    if df.empty:
        return df

    styled_df = df.style \
        .applymap(lambda x: 'background-color: #ffe6e6' if x else 'background-color: #e6ffe6', subset=['drift_detected']) \
        .background_gradient(subset=['drift_score'], cmap='OrRd', vmin=0, vmax=1) \
        .set_properties(**{'border-color': 'var(--border-color)', 'border-width': '1px', 'border-style': 'solid'})
    return styled_df