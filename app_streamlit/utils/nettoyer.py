def clean_feature_names(feature_names):
    cleaned = []
    for name in feature_names:
        # Supprime tout avant "__"
        if "__" in name:
            name = name.split("__")[-1]
        cleaned.append(name)
    return cleaned