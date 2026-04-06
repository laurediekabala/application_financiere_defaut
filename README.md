# 📊 Analyse Financière et Prédiction du Défaut de Paiement

## 🎯 Objectif du Projet

Ce projet vise à **diagnostiquer la santé financière** de 20 entreprises africaines (2000-2025) et à **prédire les risques de défaut de paiement** pour l'année suivante en utilisant des modèles de machine learning.

**Objectifs spécifiques :**
1. ✅ Identifier les **facteurs de risque** de défaut de paiement
2. ✅ Analyser la **solvabilité** des entreprises
3. ✅ Prédire le **défaut de paiement** via XGBoost et autres modèles

---

## 📈 Architecture du Projet

```
finance-RDC/
├── analyse.ipynb          # Notebook principal avec tout le pipeline
├── README.md              # Ce fichier
└── modèles_sauvegardés/
    ├── modele_logistique.joblib
    ├── explicabilite_logistique.joblib
    └── metadata_modele.pkl
```

---

## 📊 Dataset

### Composition
- **Observations** : 520 enregistrements (20 entreprises × 26 années)
- **Période** : 2000 à 2025
- **Secteurs** : 8 secteurs économiques
  - 🏦 Banque (4 entreprises)
  - ⛏️ Mines (4 entreprises)
  - 🚚 Transport (2 entreprises)
  - 🏭 Construction (1 entreprise)
  - 💊 Pharmaceutique (1 entreprise)
  - ⚡ Énergie (2 entreprises)
  - 🍺 Agroalimentaire (3 entreprises)
  - 📱 Télécom (2 entreprises)

### Variables Disponibles

#### Variables Financières Continues (15+)
| Variable | Description |
|----------|-------------|
| `CA` | Chiffre d'affaires |
| `resultat_net` | Résultat net |
| `actifs` | Total des actifs |
| `passifs` | Total des passifs |
| `capitaux_propres` | Capitaux propres |
| `flux_operationnel` | Flux de trésorerie opérationnel |
| `flux_investissement` | Flux de trésorerie d'investissement |
| `flux_financement` | Flux de trésorerie de financement |

#### Ratios Financiers
| Ratio | Description |
|-------|-------------|
| `ratio_marge` | Marge bénéficiaire (%) |
| `ratio endettement` | Taux d'endettement (%) |
| `ratio rentabilité` | Rentabilité nette (%) |
| `ratio de liquidité` | Ratio de liquidité |
| `ratio de solvabilité` | Ratio de solvabilité |
| `ratio_ci` | Ratio de couverture des intérêts |
| `ratio_cf` | Ratio de conversion de flux |

#### Variables Cibles
- `distress_score` : Score de détresse (0-5) basé sur :
  - Liquidité faible
  - Endettement élevé
  - Rentabilité faible
  - Dégradation de marge
  - Augmentation de dette
- `default_flag` : Flag défaut (distress_score ≥ 3)
- `target` : Défaut année suivante (0 ou 1)

---

## 🔄 Pipeline de Traitement

### 1️⃣ Récupération des Données
```python
# Données simulées réalistes avec trajectoires de dégradation
df = simuler_donnees_realistes(n_entreprises=20, n_annees=26)
```

### 2️⃣ Enrichissement & Nettoyage
- ✅ Mapping des entreprises vers secteurs officiels
- ✅ Vérification des données manquantes
- ✅ Détection des doublons
- ✅ Analyse des valeurs extrêmes (IQR)

### 3️⃣ Analyse Exploratoire (EDA)
- 📊 **Distributions** : Histogrammes + KDE pour variables continues
- 📈 **Corrélations** : Pearson/Spearman avec test Shapiro-Wilk
- ⏱️ **Séries temporelles** : Évolution des ratios (2000-2025)
- ⚠️ **Valeurs extrêmes** : Détection IQR

### 4️⃣ Feature Engineering
- Création des **variables de tendance** (delta_liquidite, delta_endettement, etc.)
- Création du **score de détresse** multidimensionnel
- Création du **target laggé** (shift -1)

### 5️⃣ Séparation Temporelle Train/Test
```
Train  : 70% (années 2000-2018)
Test   : 30% (années 2019-2025)
```

### 6️⃣ Modélisation
4 modèles entraînés :
1. **Régression Logistique** (pipeline + preprocessing + SelectKBest k=7)
2. **Random Forest** (100 arbres + SelectKBest)
3. **XGBoost** (avec poids de classe pour déséquilibre)
4. **SVM** (noyau RBF + SelectKBest)

### 7️⃣ Évaluation & Explicabilité
- 📊 Confusion matrix (absolue + normalisée)
- 📈 Courbes ROC + Precision-Recall
- 🔥 Feature importance (native + permutation)
- 💡 SHAP values pour logistique

### 8️⃣ Sauvegarde
- ✅ Modèles en `.joblib`
- ✅ Coefficients & explicabilité
- ✅ Métadonnées du projet

---

## 🛠️ Installation & Dépendances

### Python 3.11.5+

```bash
pip install -r requirements.txt
```

### Dépendances Principales
```
pandas==2.3.3
numpy==2.4.3
scikit-learn==1.8.0
xgboost==3.2.0
matplotlib==3.10.8
seaborn==0.13.2
plotly==6.6.0
scipy==1.15.2
statsmodels==0.14.6
imbalanced-learn==0.12.0
joblib==1.4.2
mysql-connector-python==9.6.0
sqlalchemy==2.0.48
```

---

## 📖 Utilisation

### 1. Lancer le Notebook Complet
```bash
jupyter notebook analyse.ipynb
```

### 2. Exécuter par Étapes
- **Cellule 1-6** : Imports et données
- **Cellule 7** : EDA (distributions)
- **Cellule 8-10** : Analyse de corrélation
- **Cellule 11-12** : Séries temporelles
- **Cellule 13** : Feature engineering
- **Cellule 14-18** : Modélisation
- **Cellule 19-20** : Explicabilité
- **Cellule 21-22** : Sauvegarde

### 3. Charger un Modèle Sauvegardé
```python
import joblib

# Charger le meilleur modèle
model = joblib.load('modele_logistique.joblib')

# Faire une prédiction
y_pred = model.predict(X_new)
y_proba = model.predict_proba(X_new)[:, 1]
```

---

## 📊 Résultats Attendus

### Métriques de Performance
| Modèle | Accuracy | ROC-AUC | F1-Score (Défaut) | Recall |
|--------|----------|---------|-------------------|--------|
| Logistique | À calculer | À calculer | À calculer | À calculer |
| Random Forest | À calculer | À calculer | À calculer | À calculer |
| XGBoost | À calculer | À calculer | À calculer | À calculer |
| SVM | À calculer | À calculer | À calculer | À calculer |

### Variables les Plus Prédictives
(À déterminer après feature selection)

Top 7 variables sélectionnées par SelectKBest (f_classif) :
1. TBD
2. TBD
3. TBD
...

---

## 🔬 Méthodologie

### Test de Normalité (Shapiro-Wilk)
- **Null hypothesis** : La variable suit une distribution normale
- **Seuil** : α = 0.05
- **Résultat** : Utilisation de corrélation Spearman si ≥1 variable non-normale

### Sélection de Variables (SelectKBest)
- **Score** : f_classif (ANOVA F-score)
- **k** : 7 variables sélectionnées
- **Raison** : Réduction de la dimensionalité + combat du surapprentissage

### Équilibrage des Classes
- **Technique** : `scale_pos_weight` (XGBoost) + `class_weight='balanced'` (Logistique, RF, SVM)
- **Raison** : Défauts sont minoritaires dans les données

### Validation Temporelle
- **Approche** : Time series split (pas de shuffle)
- **Raison** : Respecter l'ordre chronologique pour éviter la fuite d'information

---

## 🎯 Interprétation des Résultats

### Coefficients de Régression Logistique
- **Coefficient > 0** : ↑ variable → ↑ probabilité défaut
- **Coefficient < 0** : ↑ variable → ↓ probabilité défaut
- **Odds Ratio** : Multiplicateur du risque

### Feature Importance (XGBoost/Random Forest)
- Valeurs élevées = variables critiques pour la prédiction
- Ordonnée par impact sur les prédictions

### Permutation Importance
- Mesure la chute de performance quand on permute une variable
- Plus robuste pour données corrélées

---

## 📋 Structure du Notebook

```
1. RÉCUPÉRATION DES DONNÉES
   ├── Imports & configuration
   ├── Simulation de données réalistes
   └── Mapping entreprises → secteurs

2. ANALYSE EXPLORATOIRE
   ├── Information sur dataset
   ├── Visualisation distributions
   ├── Analyse de corrélation (Shapiro + Pearson/Spearman)
   ├── Séries temporelles
   └── Détection valeurs extrêmes

3. NETTOYAGE & FEATURE ENGINEERING
   ├── Création du score de détresse
   ├── Création du target laggé
   └── Visualisation distribution target

4. MODÉLISATION
   ├── Split train/test temporel
   ├── Preprocessing (StandardScaler)
   ├── Sélection variables (SelectKBest)
   ├── Entraînement 4 modèles
   └── Évaluation comparative

5. EXPLICABILITÉ & SAUVEGARDE
   ├── Analyse coefficients logistique
   ├── Contribution locale des variables
   ├── Sauvegarde modèles
   └── Sauvegarde explicabilité
```

---

## 🚀 Améliorations Futures

- [ ] Intégration SHAP values pour explicabilité avancée
- [ ] Hyperparameter tuning (GridSearchCV, RandomizedSearchCV)
- [ ] Cross-validation time series avancée
- [ ] Ensemble voting / stacking
- [ ] Prediction intervals
- [ ] Dashboard Streamlit
- [ ] API FastAPI pour prédictions en temps réel
- [ ] Monitoring du modèle (data drift, model drift)

---

## 👥 Auteur

**Projet** : Diagnostic de Solvabilité & Prédiction de Défaut  
**Objectif** : Analyser la santé financière de 20 entreprises africaines  
**Technologies** : Python, scikit-learn, XGBoost, Pandas, Jupyter

---

## 📞 Support

Pour toute question ou problème, consultez le notebook ou les logs d'exécution.

---

## 📄 License

Projet professionnel - 2026

---

**Dernière mise à jour** : Avril 2026  
**Status** : ✅ En production
