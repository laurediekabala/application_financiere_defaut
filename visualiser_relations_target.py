def visualiser_relations_target(dataframe, 
    colonnes_a_ignorer=['annee', 'entreprise', 'secteur', 'distress_score', 'default_flag', 'target']):
    #                                                                                        ^^^^^^^^
    #                                                                              AJOUT DE 'target' ICI
    from scipy.stats import mannwhitneyu
    import pandas as pd
    import numpy as np
    import matplotlib.pyplot as plt
    import seaborn as sns
    
    print("="*80)
    print("📊 ANALYSE DES RELATIONS : VARIABLES CONTINUES vs TARGET")
    print("="*80 + "\n")
    
    colonnes_numeriques = dataframe.select_dtypes(include=['float64', 'int64']).columns
    colonnes_continues = [col for col in colonnes_numeriques if col not in colonnes_a_ignorer]
    
    print(f"📈 Nombre de variables continues analysées : {len(colonnes_continues)}\n")
    
    defaut_0 = dataframe[dataframe['target'] == 0]
    defaut_1 = dataframe[dataframe['target'] == 1]
    
    print(f"👥 Classe 0 (Non-Défaut) : {len(defaut_0)} observations")
    print(f"👥 Classe 1 (Défaut)     : {len(defaut_1)} observations\n")
    
    # BOX PLOTS
    n_cols = len(colonnes_continues)
    n_cols_plot = 3
    n_rows = (n_cols + n_cols_plot - 1) // n_cols_plot
    
    fig, axes = plt.subplots(n_rows, n_cols_plot, figsize=(16, 4*n_rows))
    axes = axes.flatten() if n_cols > 1 else [axes]
    
    for idx, col in enumerate(colonnes_continues):
        sns.boxplot(data=dataframe, x='target', y=col, ax=axes[idx],
                   palette=['#2ecc71', '#e74c3c'], width=0.6, linewidth=2)
        axes[idx].set_title(f"Box Plot : {col}", fontsize=11, fontweight='bold')
        axes[idx].set_xlabel('Target', fontsize=10)
        axes[idx].set_ylabel(col, fontsize=10)
        axes[idx].grid(True, alpha=0.3, axis='y')
    
    for idx in range(len(colonnes_continues), len(axes)):
        axes[idx].axis('off')
    
    plt.tight_layout()
    plt.suptitle('📊 Box Plots : Distribution des Variables par Target', 
                 fontsize=14, fontweight='bold', y=0.995)
    plt.show()
    
    # VIOLIN PLOTS
    fig, axes = plt.subplots(n_rows, n_cols_plot, figsize=(16, 4*n_rows))
    axes = axes.flatten() if n_cols > 1 else [axes]
    
    for idx, col in enumerate(colonnes_continues):
        sns.violinplot(data=dataframe, x='target', y=col, ax=axes[idx],
                      palette=['#2ecc71', '#e74c3c'], linewidth=2)
        axes[idx].set_title(f"Violin Plot : {col}", fontsize=11, fontweight='bold')
        axes[idx].set_xlabel('Target', fontsize=10)
        axes[idx].set_ylabel(col, fontsize=10)
        axes[idx].grid(True, alpha=0.3, axis='y')
    
    for idx in range(len(colonnes_continues), len(axes)):
        axes[idx].axis('off')
    
    plt.tight_layout()
    plt.suptitle('🎻 Violin Plots : Distribution Détaillée par Target', 
                 fontsize=14, fontweight='bold', y=0.995)
    plt.show()
    
    # DENSITY PLOTS
    fig, axes = plt.subplots(n_rows, n_cols_plot, figsize=(16, 4*n_rows))
    axes = axes.flatten() if n_cols > 1 else [axes]
    
    for idx, col in enumerate(colonnes_continues):
        var_0 = defaut_0[col].var()
        var_1 = defaut_1[col].var()
        
        if var_0 > 0:
            defaut_0[col].plot(kind='density', ax=axes[idx], linewidth=2.5, 
                              color='#2ecc71', label='Non-Défaut (0)', alpha=0.7)
        if var_1 > 0:
            defaut_1[col].plot(kind='density', ax=axes[idx], linewidth=2.5, 
                              color='#e74c3c', label='Défaut (1)', alpha=0.7)
        
        axes[idx].set_title(f"Distribution de {col}", fontsize=11, fontweight='bold')
        axes[idx].set_xlabel(col, fontsize=10)
        axes[idx].set_ylabel('Densité', fontsize=10)
        axes[idx].legend(loc='upper right', fontsize=9)
        axes[idx].grid(True, alpha=0.3)
    
    for idx in range(len(colonnes_continues), len(axes)):
        axes[idx].axis('off')
    
    plt.tight_layout()
    plt.suptitle('📈 Density Plots : Distributions Superposées', 
                 fontsize=14, fontweight='bold', y=0.995)
    plt.show()
    
    # STATISTIQUES
    print("\n" + "="*80)
    print("📋 STATISTIQUES DESCRIPTIVES PAR CLASSE")
    print("="*80 + "\n")
    
    resultats_stats = {}
    
    for col in colonnes_continues:
        print(f"\n🔹 VARIABLE : {col}")
        print("-" * 80)
        
        stats_0 = defaut_0[col].describe()
        stats_1 = defaut_1[col].describe()
        
        print(f"✅ Non-Défaut (target=0): Moy={stats_0['mean']:.4f}, "
              f"Méd={defaut_0[col].median():.4f}, Std={stats_0['std']:.4f}")
        print(f"⚠️  Défaut (target=1):     Moy={stats_1['mean']:.4f}, "
              f"Méd={defaut_1[col].median():.4f}, Std={stats_1['std']:.4f}")
        
        # ✅ Protection division par zéro
        if stats_0['mean'] != 0:
            diff_percent = abs(stats_1['mean'] - stats_0['mean']) / abs(stats_0['mean']) * 100
            print(f"📊 Différence de moyenne : {diff_percent:.2f}%")
        else:
            diff_percent = np.nan
            print(f"📊 Différence de moyenne : non calculable (moyenne classe 0 = 0)")
        
        stat, p_value = mannwhitneyu(defaut_0[col].dropna(), defaut_1[col].dropna())
        significance = ("***" if p_value < 0.001 else 
                        "**" if p_value < 0.01 else 
                        "*" if p_value < 0.05 else "NS")
        
        print(f"🔬 Test Mann-Whitney U : p-value = {p_value:.6f} {significance}")
        
        resultats_stats[col] = {
            'mean_0': stats_0['mean'],
            'mean_1': stats_1['mean'],
            'p_value': p_value,
            'difference_percent': diff_percent
        }
    
    # CORRÉLATION
    print("\n" + "="*80)
    print("🔥 CORRÉLATION : VARIABLES vs TARGET")
    print("="*80 + "\n")
    
    # ✅ Maintenant colonnes_continues ne contient plus 'target'
    #    donc pas de doublon → corr()['target'] retourne bien une Series
    correlations = dataframe[colonnes_continues + ['target']].corr()['target'][:-1]
    correlations = correlations.reindex(
        correlations.abs().sort_values(ascending=False).index
    )
    
    print("Corrélations avec la target :\n")
    for var, corr in correlations.items():
        emoji = "📈" if corr > 0 else "📉"
        print(f"{emoji} {var:30s} : {corr:7.4f}")
    
    fig, ax = plt.subplots(figsize=(10, 8))
    
    corr_matrix = dataframe[colonnes_continues + ['target']].corr()[['target']]
    corr_matrix = corr_matrix.reindex(
        corr_matrix['target'].abs().sort_values(ascending=False).index
    )
    
    sns.heatmap(corr_matrix, annot=True, fmt='.3f', cmap='RdBu_r', center=0,
                cbar_kws={"label": "Corrélation"}, ax=ax, vmin=-1, vmax=1,
                linewidths=1, linecolor='white', annot_kws={"size": 11, "weight": "bold"})
    
    ax.set_title('🔥 Corrélation des Variables avec la Target', 
                 fontsize=13, fontweight='bold', pad=15)
    plt.tight_layout()
    plt.show()
    
    return {'statistiques': resultats_stats, 'correlations': correlations}