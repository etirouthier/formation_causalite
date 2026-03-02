# Architecture Research

**Domain:** Python/Jupyter educational notebook — causal inference simulation
**Researched:** 2026-03-02
**Confidence:** HIGH (patterns well-established pour notebooks scientifiques)

---

## Architecture recommandée : 5 couches

```
┌─────────────────────────────────────────────────────────┐
│  COUCHE 1 : PARAMÈTRES                                  │
│  Cellule unique en tête — ALL_CAPS constants            │
│  SEED, N_MAGASINS, T_MOIS, effets, probabilités         │
└─────────────────────┬───────────────────────────────────┘
                      │
┌─────────────────────▼───────────────────────────────────┐
│  COUCHE 2 : GÉNÉRATEUR DE BASE                          │
│  generate_base_panel(params, rng) → DataFrame           │
│  Panel N_MAGASINS × T_MOIS avec toutes les variables    │
│  (taille, urbain, equipe, mois, nb_visites, panier...)  │
└─────────────────────┬───────────────────────────────────┘
                      │
┌─────────────────────▼───────────────────────────────────┐
│  COUCHE 3 : SCÉNARIOS                                   │
│  Chaque scénario dérive du panel de base                │
│  generate_scenario_0(base_df, params) → df              │
│  generate_scenario_1a(base_df, params) → df             │
│  generate_scenario_1b(base_df, params) → df             │
│  generate_scenario_1c(base_df, params) → df             │
│  generate_scenario_2(base_df, params) → df              │
│  generate_scenario_3(base_df, params) → df              │
└─────────────────────┬───────────────────────────────────┘
                      │
┌─────────────────────▼───────────────────────────────────┐
│  COUCHE 4 : VISUALISATION                               │
│  Une fonction par figure                                │
│  plot_scenario_0_distribution(df, ax) → None            │
│  plot_dag_scenario_1a(ax) → None                        │
│  plot_coefficient_comparison(results, ax) → None        │
└─────────────────────┬───────────────────────────────────┘
                      │
┌─────────────────────▼───────────────────────────────────┐
│  COUCHE 5 : EXPORT                                      │
│  fig.savefig('figures/scenario_N.png', dpi=150)        │
│  df.to_csv('data/scenario_N.csv', index=False)         │
└─────────────────────────────────────────────────────────┘
```

---

## Structure du notebook

```
notebook.ipynb
├── [CELL 1] Paramètres globaux (ALL_CAPS)
├── [CELL 2] Imports + création dossiers figures/ et data/
├── [CELL 3] Fonctions utilitaires (générateur de base, helpers viz)
│
├── ── SCÉNARIO 0 : Biais de petits nombres ──────────────
├── [CELL 4] Markdown : DAG + explication
├── [CELL 5] Génération données scénario 0
├── [CELL 6] Figures scénario 0 + export PNG + CSV
│
├── ── SCÉNARIO 1 : Biais de sélection ──────────────────
├── [CELL 7] Markdown : introduction biais de sélection
├── [CELL 8] Scénario 1a (équipe) : données + figures + export
├── [CELL 9] Scénario 1b (localisation) : données + figures + export
├── [CELL 10] Scénario 1c (saison) : données + figures + export
│
├── ── SCÉNARIO 2 : Surcontrôle médiateur ───────────────
├── [CELL 11] Markdown : DAG médiateur
├── [CELL 12] Génération + régressions + figures + export
│
└── ── SCÉNARIO 3 : Surcontrôle collider ────────────────
    ├── [CELL 13] Markdown : DAG collider
    └── [CELL 14] Génération + régressions + figures + export
```

---

## Flux de données

```
rng = np.random.default_rng(SEED)
        │
        ▼
base_panel_df  ← generate_base_panel(params, rng)
  [N×T lignes : taille, urbain, equipe, mois, nb_visites_0, panier_0]
        │
        ├──▶ scenario_0_df  ← base_panel + variance par taille
        │
        ├──▶ scenario_1a_df ← base_panel + sélection P(pub|equipe)
        ├──▶ scenario_1b_df ← base_panel + sélection P(pub|urbain)
        ├──▶ scenario_1c_df ← base_panel + sélection P(pub|mois)
        │
        ├──▶ scenario_2_df  ← base_panel + pub uniforme + décomposition nb_visites × panier
        │
        └──▶ scenario_3_df  ← base_panel + pub uniforme + variable posts_reseaux
```

---

## 5 patterns architecturaux clés

### 1. Cellule paramètres unique (ALL_CAPS)
```python
# ═══════════════════════════════════════
# PARAMÈTRES — modifiez ici uniquement
# ═══════════════════════════════════════
SEED = 42
N_MAGASINS = 200
T_MOIS = 24

# Effets causaux vrais
EFFET_PUB_VISITES = 0.10   # +10% sur p_visite
EFFET_PUB_PANIER  = 0.10   # +10% sur μ_panier

# Taille des magasins (N_potentiel clients/mois)
N_PETIT  = 50
N_MOYEN  = 200
N_GRAND  = 1000

# Effets additifs sur p_visite (probabilité de base = P_BASE_VISITE)
P_BASE_VISITE  = 0.05
EFFET_URBAIN   = 0.03
EFFET_EQUIPE   = 0.02

# Scénarios de sélection (probabilité de traitement)
P_PUB_BONNE_EQUIPE   = 0.70
P_PUB_MAUVAISE_EQUIPE = 0.20
P_PUB_URBAIN  = 0.65
P_PUB_RURAL   = 0.25
```

### 2. RNG explicite (thread-safe, reproductible)
```python
rng = np.random.default_rng(SEED)
# Passer rng comme argument, jamais comme global
base_df = generate_base_panel(params, rng)
```

### 3. Une fonction = une figure = un export
```python
def plot_coefficient_comparison(results_naive, results_overcontrolled, true_effect, ax):
    """Toujours sauvegarde la figure. Retourne None."""
    # ... draw on ax ...
    ax.figure.savefig('figures/scenario2_coefficients.png', dpi=150, bbox_inches='tight')
```

### 4. DAG comme networkx.DiGraph avec layout fixe
```python
G = nx.DiGraph()
G.add_edges_from([('pub', 'ventes'), ('equipe', 'pub'), ('equipe', 'ventes')])
pos = {'pub': (0, 0), 'ventes': (2, 0), 'equipe': (1, 1)}  # layout FIXE
nx.draw_networkx(G, pos, ax=ax, node_color=['blue', 'green', 'orange'], ...)
```

### 5. Isolation des scénarios par DataFrames dérivés
```python
# Ne JAMAIS modifier base_df en place
scenario_1a_df = base_df.copy()
scenario_1a_df['pub'] = assign_treatment_by_team(scenario_1a_df, rng, params)
scenario_1a_df['ventes'] = compute_sales(scenario_1a_df, rng, params)
```

---

## Anti-patterns à éviter

| Anti-pattern | Risque | Solution |
|--------------|--------|---------|
| `np.random.seed()` global | Résultats changent si ordre des cellules change | `rng = np.random.default_rng(SEED)` |
| `plt.show()` inline sans `fig.savefig()` | Figures non exportées automatiquement | Créer `fig, ax` explicitement, toujours sauvegarder |
| Régénérer le DGP dans chaque scénario | Résultats incohérents entre scénarios | Générer `base_df` une seule fois, dériver |
| Paramètres éparpillés dans les cellules | Formateur doit chercher pour changer | Tout en cellule 1 |
| Dépendance à `graphviz` système | Friction d'installation sur machine formateur | `networkx` + `matplotlib` uniquement |

---

## Ordre de construction recommandé

1. Cellule paramètres (SEED, N, effets)
2. Imports + création `figures/` et `data/`
3. Générateur de base (`generate_base_panel`)
4. Scénario 0 (le plus simple — validation du DGP)
5. Scénarios 1a/1b/1c (mécanisme de sélection)
6. Scénario 2 (surcontrôle médiateur + OLS)
7. Scénario 3 (collider + OLS)
8. Vérification bout-en-bout (`Restart & Run All`)
9. Export README du notebook

---

*Confidence: HIGH — patterns standard pour notebooks scientifiques Python*
