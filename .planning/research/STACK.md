# Stack Research

**Domain:** Python/Jupyter educational notebook — causal inference simulation
**Researched:** 2026-03-02
**Confidence:** MEDIUM (training knowledge to Aug 2025; versions should be verified before pinning)

---

## Recommended Stack

### Core Technologies

| Technology | Version | Purpose | Why Recommended |
|------------|---------|---------|-----------------|
| Python | 3.11+ | Runtime | LTS sweet spot: up to 25% faster than 3.10, mature wheel availability |
| JupyterLab | 4.x | Notebook environment | Current standard; classic `jupyter notebook` 6.x est en maintenance-only |
| numpy | 2.x (2.0+) | Array math, tirages aléatoires (Binomial, Normal) | `numpy.random.default_rng(seed)` est l'API correcte — reproductible, thread-safe |
| pandas | 2.x (2.1+) | Panel DataFrame, CSV export, groupby | pandas 2.2+ avec copy-on-write par défaut |

### Supporting Libraries

| Library | Version | Purpose |
|---------|---------|---------|
| scipy | 1.13+ | Objets de distributions statistiques (`scipy.stats`) |
| matplotlib | 3.8+ | Figures PNG publication-quality |
| seaborn | 0.13+ | Visualisations statistiques (histplot par groupe, scatterplot) |
| statsmodels | 0.14+ | OLS avec formula API, tables de résultats avec SE et p-values |
| linearmodels | 6.x | Panel OLS avec within-estimator pour FE |
| networkx | 3.x | Construction de DAGs (graphes orientés acycliques) |

---

## Installation

```bash
pip install "numpy>=2.0" "pandas>=2.1" "scipy>=1.13" "matplotlib>=3.8" "seaborn>=0.13"
pip install "statsmodels>=0.14" "linearmodels>=6.0"
pip install "networkx>=3.0"
pip install "jupyterlab>=4.0"
pip freeze > requirements.txt
```

---

## Patterns par usage

**DAG visualization (tous les scénarios) :**
- Utiliser `networkx.DiGraph` + `pos` dict manuel (layout déterministe — pas de spring_layout stochastique)
- Colorisation : traitement (bleu), outcome (vert), confondant (orange), collider (rouge)
- Rendu : `nx.draw_networkx(G, pos, ax=ax, ...)`

**Graphiques de comparaison des coefficients (Scénarios 2, 3) :**
- Barres d'erreur horizontales avec IC 95%
- OLS naïf vs OLS avec surcontrôle côte à côte
- `result.params['pub']` et `result.conf_int().loc['pub']`

**Distribution figures (Scénario 0) :**
- `seaborn.histplot(data=df, x='panier_moyen', hue='taille', kde=True, stat='density')`

**Export :**
- Figures → `figures/scenario_N_description.png` à `dpi=150`
- Données → `data/scenario_N_description.csv`
- Créer les dossiers au démarrage : `pathlib.Path('figures').mkdir(exist_ok=True)`

---

## À ne PAS utiliser

| Éviter | Pourquoi | Utiliser à la place |
|--------|----------|---------------------|
| `np.random.seed()` global | Thread-unsafe, déprécié | `rng = np.random.default_rng(SEED)` |
| `sklearn.linear_model.LinearRegression` | Pas d'erreurs standard, pas de p-values | `statsmodels.formula.api.ols` |
| `plotly` / `bokeh` pour PNG | Sortie HTML/JS, pas de PNG natif | `matplotlib` avec `fig.savefig(..., dpi=150)` |
| `causalgraphicalmodels` | Non maintenu depuis ~2020 | `networkx.DiGraph` |
| Spring layout (`nx.spring_layout`) | Stochastique entre exécutions | Layout `pos` dict fixé manuellement |

---

*Confidence: MEDIUM — basé sur connaissance du domaine (cutoff août 2025), web non disponible*
