def risk_color(level: str):
    colors = {
        "faible": "green",
        "modere": "orange",
        "eleve": "darkorange",
        "critique": "red"
    }
    return colors.get(level.lower(), "gray")