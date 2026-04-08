import streamlit as st

def show_alert(message, alert_type="info", title=None):
    """
    Affiche une alerte HTML/CSS custom.
    
    alert_type: info | success | warning | error
    """
    icons = {
        "info": "ℹ️",
        "success": "✅",
        "warning": "⚠️",
        "error": "❌"
    }

    default_titles = {
        "info": "Information",
        "success": "Succès",
        "warning": "Attention",
        "error": "Erreur"
    }

    if title is None:
        title = default_titles.get(alert_type, "Message")

    icon = icons.get(alert_type, "ℹ️")

    st.markdown(
        f"""
        <div class="custom-alert custom-alert-{alert_type}">
            <div class="custom-alert-title">{icon} {title}</div>
            <div class="custom-alert-text">{message}</div>
        </div>
        """,
        unsafe_allow_html=True
    )