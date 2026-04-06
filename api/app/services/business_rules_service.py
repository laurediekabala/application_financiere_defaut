def compute_lgd(secteur: str, garantie_ratio: float = None):
    lgd_par_secteur = {
        "Banque": 0.35,
        "Télécom": 0.45,
        "Mines": 0.50,
        "Energie" :0.50,
        "Transport" :0.40,
        "Construction" :0.35,
        "Agroalimentaire":0.55,
        "Pharmaceutique" : 0.30 }

    lgd = lgd_par_secteur.get(secteur, 0.50)

    if garantie_ratio is not None:
        lgd = max(0.10, lgd - garantie_ratio)

    return round(lgd, 4)

def risk_level(prob_default: float):
    if prob_default < 0.20:
        return "faible"
    elif prob_default < 0.50:
        return "modéré"
    elif prob_default < 0.75:
        return "élevé"
    else:
        return "critique"

def business_decision(prob_default: float):
    if prob_default < 0.20:
        return "accordé"
    elif prob_default < 0.50:
        return "surveillance"
    elif prob_default < 0.75:
        return "analyse_approfondie"
    else:
        return "refus"

def expected_loss(prob_default: float, exposition: float, secteur: str, garantie_ratio: float = None):
    lgd = compute_lgd(secteur, garantie_ratio)
    ead = float(exposition) if exposition is not None else 0.0
    el = prob_default * lgd * ead

    return {
        "PD": round(prob_default, 4),
        "LGD": round(lgd, 4),
        "EAD": round(ead, 2),
        "expected_loss": round(el, 2)
    }