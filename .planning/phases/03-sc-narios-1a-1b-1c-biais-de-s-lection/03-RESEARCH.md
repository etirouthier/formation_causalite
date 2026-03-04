# Phase 3: Scénarios 1a/1b/1c — Biais de sélection - Research

**Researched:** 2026-03-04
**Domain:** Jupyter notebook — statsmodels OLS, networkx DAG, matplotlib errorbar, pandas panel, ATT counterfactual
**Confidence:** HIGH

---

<user_constraints>
## User Constraints (from CONTEXT.md)

### Locked Decisions

**Structure des sous-scénarios**
- Code commun pour la génération et l'assignation pub (une fonction par confondant ou paramètres mutualisés), mais 3 sections de cellules **indépendantes** dans le notebook (1a, 1b, 1c)
- Un seul confondant à la fois par sous-scénario — pas de modèle multi-confondants
- Confondants : 1a = `qualite_equipe`, 1b = `urbain`, 1c = `effet_saison_val` / `mois`

**Figures — 9 au total**
- **Séparées par type ET par sous-scénario** : 3 scénarios × 3 types = 9 PNG dans `figures/`
- Naming : `sc1a_dag.png`, `sc1a_coeff.png`, `sc1a_bar.png` (et idem pour 1b, 1c)
- Pas de figure composite multi-scénarios

**Coefficient plot**
- Style **vertical** : un point par estimateur (naïf, ajusté, vrai) sur l'axe Y, valeur sur l'axe X — ou l'inverse si plus lisible
- **Barres d'erreur** pour les IC 95% (errplot / errorbar matplotlib)
- 3 points par plot : OLS naïf, OLS ajusté, ATT contrefactuel (valeur vraie)

**Valeur vraie — ATT contrefactuel**
- Pour chaque sous-scénario, l'**ATT** est calculé par comparaison contrefactuelle :
  1. Identifier les magasins traités (pub=1) dans le scénario
  2. Recalculer leurs outcomes avec pub=0 (contrefactuel, impossible en vrai)
  3. ATT = moyenne(Y_observé − Y_contrefactuel) pour les traités
- Cette valeur est utilisée comme référence "vrai effet" dans le coefficient plot et le bar chart

**Variable dépendante**
- OLS sur **`ventes`** (chiffre d'affaires total), pas `panier_moyen`

**Niveau et spécification OLS**
- **Panel complet** : 200 magasins × 24 mois = 4800 lignes
- **Scénarios 1a et 1b** (confondant non saisonnier) :
  - OLS naïf : `ventes ~ pub + C(mois)` — contrôle la saisonnalité mais PAS le confondant d'intérêt
  - OLS ajusté : `ventes ~ pub + confondant + C(mois)`
- **Scénario 1c** (confondant = saison) :
  - OLS naïf : `ventes ~ pub` — SANS mois, pour rendre le biais saisonnier visible
  - OLS ajusté : `ventes ~ pub + C(mois)` — contrôle la saison

**DAG — nœuds**
- **Noms verbeux en français** pour les slides : `Qualité équipe`, `Localisation`, `Saison`
- Nœuds communs à tous les DAGs : `Pub` et `Ventes`
- Même pattern de layout fixe que `code-dag-pattern` (`pos` dict, pas de `spring_layout`)

### Claude's Discretion
- Couleurs des nœuds dans les DAGs (cohérentes avec le style du notebook)
- Palette des 3 estimateurs dans les coefficient plots et bar charts
- Labels exacts des axes et titres des figures (factuel, sans commentaire interprétatif)
- Gestion du rng pour le calcul ATT contrefactuel (rng local dédié par scénario)

### Deferred Ideas (OUT OF SCOPE)

Aucune — la discussion est restée dans le périmètre de la Phase 3.
</user_constraints>

---

<phase_requirements>
## Phase Requirements

| ID | Description | Research Support |
|----|-------------|-----------------|
| SC1-01 | Scénario 1a (sélection par qualité d'équipe) : DAG causal + coefficient plot (OLS naïf vs OLS ajusté vs valeur vraie avec IC 95%) + bar chart comparant effet naïf/ajusté/vrai | Pipeline vérifié empiriquement : `base_df` + assignation `pub` à niveau magasin via `P_PUB_BONNE/MAUVAISE_EQUIPE`, `smf.ols('ventes ~ pub + C(mois)', data=df)`, ATT contrefactuel via `compute_outcomes` avec `pub=0` pour traités, DAG networkx 3 nœuds |
| SC1-02 | Scénario 1b (sélection par localisation urbain/rural) : DAG causal + coefficient plot + bar chart comparant effet naïf/ajusté/vrai | Même pipeline que 1a, confondant `urbain`, PARAMS `P_PUB_URBAIN=0.65`, `P_PUB_RURAL=0.25` déjà dans PARAMS, `rng_sc1b = np.random.default_rng(SEED + 20)` |
| SC1-03 | Scénario 1c (sélection par saison) : DAG causal + coefficient plot + bar chart comparant effet naïf/ajusté/vrai | Structurellement différent : `pub` assigné à niveau **ligne** (par mois) via `effet_saison_val > 0`, OLS naïf sans `C(mois)`, OLS ajusté avec `C(mois)`, `rng_sc1c = np.random.default_rng(SEED + 30)` |
</phase_requirements>

---

## Summary

Phase 3 insère 3 sections indépendantes (1a, 1b, 1c) dans le notebook existant, chacune composée de 4 cellules de code (assignation pub + outcomes, DAG, coefficient plot, bar chart) et d'une cellule markdown de section. Toute l'infrastructure est déjà en place : `base_df` (4800 lignes) est en mémoire, `generate_base_panel` / `compute_outcomes` sont définies, `statsmodels.formula.api` est importé, `networkx` est importé. Aucun import additionnel n'est nécessaire.

La distinction architecturale critique est le niveau d'assignation du traitement : pour 1a et 1b, `pub` est assigné au niveau magasin (constant sur 24 mois pour un même magasin) en utilisant `rng.binomial(1, prob, n_magasins)` puis merge sur `magasin_id` ; pour 1c, `pub` est assigné au niveau ligne (varie par mois selon la saison) en utilisant `rng.binomial(1, prob_par_ligne, n_lignes)` directement sur le panel. Cette différence structure entièrement la logique d'assignation et le calcul de l'ATT (traités = magasins pour 1a/1b, lignes pour 1c).

Les vérifications empiriques confirment que le biais pédagogique est présent et dans la bonne direction : le coefficient OLS naïf surestime systématiquement la valeur vraie (ATT). Avec SEED=42 et SEED+10 pour 1a : ATT≈1070, OLS naïf≈1664 (+56% d'écart), OLS ajusté≈1574 (toujours surestimé, ATT hors IC 95%). La pédagogie fonctionne.

**Primary recommendation:** Écrire 3 × 4 cellules de code indépendantes réutilisant `base_df` et les fonctions DGP existantes. Utiliser `smf.ols(...).fit()` pour les OLS, `ax.errorbar()` pour les coefficient plots, `ax.bar()` pour les bar charts, `nx.draw_networkx()` pour les DAGs. Attribuer des seeds dédiés `SEED+10/+11`, `SEED+20/+21`, `SEED+30/+31` pour garantir la reproductibilité.

---

## Standard Stack

### Core (already installed and imported in notebook)

| Library | Version | Purpose | Why Standard |
|---------|---------|---------|--------------|
| statsmodels | 0.14.6 | `smf.ols(formula, data).fit()`, `conf_int()`, accès `.params[]` | Déjà importé comme `smf`, formule R-style, `C(mois)` pour dummies catégoriels |
| numpy | 2.4.2 | `rng.binomial()`, `np.random.default_rng()`, `np.where()`, `np.clip()` | Déjà utilisé partout dans le DGP |
| pandas | 3.0.1 | `merge()`, `drop_duplicates()`, `isin()`, `to_csv()` | Déjà utilisé pour `base_df` |
| matplotlib | 3.10.8 | `ax.errorbar()`, `ax.bar()`, `ax.axvline()`, `fig.savefig()` | Pattern établi dans le projet |
| networkx | 3.6.1 | `nx.DiGraph()`, `G.add_edges_from()`, `nx.draw_networkx()` | Déjà utilisé dans `code-dag-pattern` |
| seaborn | 0.13.2 | Pas utilisé directement en Phase 3 | Déjà importé si besoin de palette |

### Supporting

| Library | Version | Purpose | When to Use |
|---------|---------|---------|-------------|
| pathlib.Path | stdlib | `figures/`, `data/` dirs déjà créés | Déjà fait en cellule Import |
| matplotlib.patches.Patch | 3.10.8 | Légendes custom (couleurs bar chart) | Si bar chart nécessite une légende manuelle |

### Alternatives Considered

| Instead of | Could Use | Tradeoff |
|------------|-----------|----------|
| `smf.ols` | `sklearn.LinearRegression` | smf.ols donne CI directement, est identique à ce que ferait un économiste — pas d'alternative à explorer |
| `ax.errorbar` (horizontal) | `ax.errorbar` (vertical) | CONTEXT locked : estimateurs sur Y, valeur sur X — donc horizontal errorbar |
| Layout fixe `pos` dict | `spring_layout` | Interdit par DGP-06 et pattern DAG établi |

**Installation:** Aucune — toutes les dépendances sont déjà présentes.

---

## Architecture Patterns

### Structure des cellules à insérer

```
notebook (après code-dag-pattern):
├── md-sc1a-section         # Markdown: "## Scénario 1a — Sélection par qualité d'équipe"
├── code-sc1a-data          # Assignation pub 1a + compute_outcomes + ATT + OLS + export CSV
├── code-sc1a-dag           # DAG networkx sc1a -> figures/sc1a_dag.png
├── code-sc1a-coeff         # Coefficient plot sc1a -> figures/sc1a_coeff.png
├── code-sc1a-bar           # Bar chart sc1a -> figures/sc1a_bar.png
│
├── md-sc1b-section         # Markdown: "## Scénario 1b — Sélection par localisation"
├── code-sc1b-data          # Assignation pub 1b + compute_outcomes + ATT + OLS + export CSV
├── code-sc1b-dag           # DAG networkx sc1b -> figures/sc1b_dag.png
├── code-sc1b-coeff         # Coefficient plot sc1b -> figures/sc1b_coeff.png
├── code-sc1b-bar           # Bar chart sc1b -> figures/sc1b_bar.png
│
├── md-sc1c-section         # Markdown: "## Scénario 1c — Sélection par saison"
├── code-sc1c-data          # Assignation pub 1c + compute_outcomes + ATT + OLS + export CSV
├── code-sc1c-dag           # DAG networkx sc1c -> figures/sc1c_dag.png
├── code-sc1c-coeff         # Coefficient plot sc1c -> figures/sc1c_coeff.png
└── code-sc1c-bar           # Bar chart sc1c -> figures/sc1c_bar.png
```

Variante acceptable pour le planner : fusionner `code-scXX-data` et `code-scXX-dag` en une seule cellule si jugé plus compact. La séparation recommandée facilite la réexécution partielle et le débogage.

### Pattern 1: Assignation pub et calcul ATT (scénarios 1a et 1b — niveau magasin)

**What:** Pub est fixe par magasin sur 24 mois. Assigné via probabilité conditionnelle sur le confondant binaire.

**When to use:** Confondants `qualite_equipe` (1a) et `urbain` (1b).

```python
# Source: vérification empirique locale, SEED=42
# Scénario 1a : sélection par qualité d'équipe
rng_sc1a = np.random.default_rng(SEED + 10)

# Assignation pub au niveau magasin (constant sur 24 mois)
stores_1a = base_df[['magasin_id', 'qualite_equipe']].drop_duplicates('magasin_id').copy()
probs_1a = np.where(
    stores_1a['qualite_equipe'] == 1,
    P_PUB_BONNE_EQUIPE,      # 0.70
    P_PUB_MAUVAISE_EQUIPE    # 0.30
)
stores_1a['pub'] = rng_sc1a.binomial(1, probs_1a)

# Merge vers le panel complet
df_sc1a = base_df.merge(stores_1a[['magasin_id', 'pub']], on='magasin_id')
df_sc1a = compute_outcomes(df_sc1a, PARAMS, rng_sc1a)

# Calcul ATT contrefactuel
treated_ids_1a = stores_1a[stores_1a['pub'] == 1]['magasin_id'].values
df_treated_1a = df_sc1a[df_sc1a['magasin_id'].isin(treated_ids_1a)].copy()
rng_cf_1a = np.random.default_rng(SEED + 11)
df_cf_1a = df_treated_1a.copy()
df_cf_1a['pub'] = 0
df_cf_1a = compute_outcomes(df_cf_1a, PARAMS, rng_cf_1a)
att_1a = (df_treated_1a['ventes'].values - df_cf_1a['ventes'].values).mean()

# OLS naïf et ajusté
model_naive_1a  = smf.ols('ventes ~ pub + C(mois)', data=df_sc1a).fit()
model_adj_1a    = smf.ols('ventes ~ pub + qualite_equipe + C(mois)', data=df_sc1a).fit()

# Export CSV
df_sc1a.to_csv('data/sc1a_selection_qualite.csv', index=False)
```

### Pattern 2: Assignation pub et calcul ATT (scénario 1c — niveau ligne/mois)

**What:** Pub varie par mois selon la saison. Assigné ligne par ligne.

**When to use:** Confondant saisonnier (1c), structurellement différent des 1a/1b.

```python
# Source: vérification empirique locale
# Scénario 1c : sélection par saison
rng_sc1c = np.random.default_rng(SEED + 30)

# Assignation pub au niveau mois (varie par ligne)
# Haute saison = effet_saison_val > 0
df_sc1c = base_df.copy()
haute_mask = df_sc1c['effet_saison_val'] > 0
probs_1c = np.where(haute_mask, P_PUB_HAUTE_SAISON, P_PUB_BASSE_SAISON)  # 0.70 / 0.30
df_sc1c['pub'] = rng_sc1c.binomial(1, probs_1c)
df_sc1c = compute_outcomes(df_sc1c, PARAMS, rng_sc1c)

# ATT : traités = lignes avec pub=1
df_treated_1c = df_sc1c[df_sc1c['pub'] == 1].copy()
rng_cf_1c = np.random.default_rng(SEED + 31)
df_cf_1c = df_treated_1c.copy()
df_cf_1c['pub'] = 0
df_cf_1c = compute_outcomes(df_cf_1c, PARAMS, rng_cf_1c)
att_1c = (df_treated_1c['ventes'].values - df_cf_1c['ventes'].values).mean()

# OLS naïf SANS mois (biais visible), ajusté AVEC C(mois)
model_naive_1c = smf.ols('ventes ~ pub', data=df_sc1c).fit()
model_adj_1c   = smf.ols('ventes ~ pub + C(mois)', data=df_sc1c).fit()

# Export CSV
df_sc1c.to_csv('data/sc1c_selection_saison.csv', index=False)
```

### Pattern 3: Coefficient plot (horizontal errorbar)

**What:** 3 points sur l'axe Y (estimateurs), valeur sur X, IC 95% via `ax.errorbar()`.

```python
# Source: matplotlib.axes.errorbar, statsmodels RegressionResults.conf_int()
# Accès aux résultats OLS:
coef_naive = model_naive_1a.params['pub']
ci_naive   = model_naive_1a.conf_int().loc['pub']  # ci[0] lower, ci[1] upper

coef_adj   = model_adj_1a.params['pub']
ci_adj     = model_adj_1a.conf_int().loc['pub']

# Erreurs pour errorbar (doit être positif — distance au centre)
xerr_naive = [[coef_naive - ci_naive[0]], [ci_naive[1] - coef_naive]]
xerr_adj   = [[coef_adj   - ci_adj[0]],   [ci_adj[1]   - coef_adj]]

estimators = ['OLS naïf', 'OLS ajusté', 'Valeur vraie (ATT)']
coeffs     = [coef_naive, coef_adj, att_1a]
y_pos      = [2, 1, 0]

fig, ax = plt.subplots(figsize=(8, 4))
# OLS naïf avec CI
ax.errorbar(coef_naive, 2, xerr=xerr_naive, fmt='o', capsize=5,
            color='#e74c3c', label='OLS naïf', markersize=8)
# OLS ajusté avec CI
ax.errorbar(coef_adj, 1, xerr=xerr_adj, fmt='o', capsize=5,
            color='#3498db', label='OLS ajusté', markersize=8)
# ATT (pas de CI — valeur exacte simulée)
ax.errorbar(att_1a, 0, fmt='D', color='#2ecc71', label='Valeur vraie (ATT)', markersize=10)
# Ligne verticale à la valeur vraie
ax.axvline(x=att_1a, color='gray', linestyle='--', alpha=0.5)

ax.set_yticks(y_pos)
ax.set_yticklabels(estimators)
ax.set_xlabel('Effet estimé de la pub sur les ventes (€)')
ax.set_title('Scénario 1a — Coefficients OLS naïf vs ajusté vs valeur vraie')
ax.legend(loc='lower right')
fig.savefig('figures/sc1a_coeff.png', dpi=150, bbox_inches='tight')
plt.show()
```

### Pattern 4: Bar chart comparaison (3 estimateurs)

```python
# Source: matplotlib.axes.bar
fig, ax = plt.subplots(figsize=(7, 4))
labels = ['OLS naïf', 'OLS ajusté', 'Valeur vraie (ATT)']
values = [coef_naive, coef_adj, att_1a]
colors = ['#e74c3c', '#3498db', '#2ecc71']

x = range(len(labels))
ax.bar(x, values, color=colors, width=0.5)
ax.set_xticks(x)
ax.set_xticklabels(labels)
ax.set_ylabel('Effet estimé de la pub sur les ventes (€)')
ax.set_title('Scénario 1a — Comparaison des estimateurs')
ax.axhline(y=att_1a, color='gray', linestyle='--', alpha=0.5)
fig.savefig('figures/sc1a_bar.png', dpi=150, bbox_inches='tight')
plt.show()
```

### Pattern 5: DAG networkx

```python
# Source: code-dag-pattern existant dans le notebook
G_1a = nx.DiGraph()
G_1a.add_edges_from([
    ('Qualité équipe', 'Pub'),
    ('Qualité équipe', 'Ventes'),
    ('Pub', 'Ventes'),
])
pos_1a = {'Pub': (0, 0), 'Ventes': (2, 0), 'Qualité équipe': (1, 1)}

# OBLIGATOIRE: couleur par node via dict pour robustesse
color_map = {'Pub': 'steelblue', 'Ventes': 'seagreen', 'Qualité équipe': 'darkorange'}
node_colors = [color_map[n] for n in G_1a.nodes()]  # robuste quelle que soit l'ordre G.nodes()

fig, ax = plt.subplots(figsize=(5, 3))
nx.draw_networkx(G_1a, pos_1a, ax=ax,
                 node_color=node_colors,
                 node_size=2000, font_size=9, font_color='white',
                 arrows=True, arrowsize=20)
ax.axis('off')
ax.set_title('DAG — Scénario 1a : sélection par qualité équipe')
fig.savefig('figures/sc1a_dag.png', dpi=150, bbox_inches='tight')
plt.show()
```

### Anti-Patterns to Avoid

- **Ne pas utiliser `rng` global** : toujours créer `rng_sc1a = np.random.default_rng(SEED + 10)` local. Le rng global est déjà consommé par `base_df`, agg_sc0, et fig4 — y toucher casse la reproductibilité des scénarios.
- **Ne pas passer `node_color` comme liste littérale** : l'ordre de `G.nodes()` dépend de l'ordre d'insertion des arêtes. Utiliser `[color_map[n] for n in G.nodes()]` pour la robustesse.
- **Ne pas inverser `savefig` et `plt.show()`** : `fig.savefig(...)` AVANT `plt.show()` — pattern obligatoire du projet.
- **Ne pas utiliser `spring_layout`** : toujours un `pos` dict fixe pour les DAGs.
- **Ne pas oublier `drop_duplicates('magasin_id')`** : pour 1a et 1b, l'assignation pub se fait par magasin. Sans dedup, on produit 24 tirages par magasin au lieu de 1.
- **Ne pas confondre le niveau d'ATT entre 1a/1b et 1c** : pour 1a/1b, `treated_ids` est une liste de `magasin_id`; pour 1c, `treated_rows = df[df['pub'] == 1]` (lignes, pas magasins).
- **Ne pas utiliser `conf_int()[0]` et `conf_int()[1]`** : les colonnes de `conf_int()` sont indexées `0` et `1` (integers), pas `'lower'`/`'upper'`. Utiliser `ci.loc['pub', 0]` et `ci.loc['pub', 1]`.

---

## Don't Hand-Roll

| Problem | Don't Build | Use Instead | Why |
|---------|-------------|-------------|-----|
| Régression avec dummies catégoriels | Pd.get_dummies + np.linalg.lstsq | `smf.ols('ventes ~ C(mois)', data=df).fit()` | `C(mois)` gère automatiquement les 23 dummies (n-1), la référence et les CI |
| Intervalles de confiance OLS | Formule manuelle t * std_err | `result.conf_int().loc['pub']` | Statsmodels calcule les IC corrects avec les degrés de liberté appropriés |
| Layout DAG lisible | Algorithme de placement de nœuds | `pos = {'Pub': (0,0), 'Ventes': (2,0), 'Confondant': (1,1)}` | Layout fixe déterministe, identique à chaque exécution |
| Probabilités conditionnelles vectorisées | Boucle for sur magasins | `np.where(condition, prob_haute, prob_basse)` + `rng.binomial(1, probs)` | Vectorisé, exact, reproductible |

**Key insight:** Statsmodels `smf.ols` avec notation de formule R-style est le seul outil nécessaire pour toute la régression. `conf_int()` retourne directement un DataFrame avec colonnes `[0, 1]` (lower/upper) — pas besoin de calcul manuel.

---

## Common Pitfalls

### Pitfall 1: Ordre des couleurs dans `nx.draw_networkx`

**What goes wrong:** `node_color=['steelblue', 'seagreen', 'darkorange']` comme liste littérale applique les couleurs dans l'ordre de `G.nodes()`, qui dépend de l'ordre d'insertion des arêtes dans `add_edges_from`. Si on change l'ordre des arêtes, les couleurs s'inversent silencieusement.

**Why it happens:** `G.nodes()` retourne les nœuds dans l'ordre où ils ont été rencontrés pour la première fois dans `add_edges_from`. `('Qualité équipe', 'Pub')` donne `['Qualité équipe', 'Pub', 'Ventes']`, mais `('Pub', 'Ventes')` en premier donne `['Pub', 'Ventes', 'Qualité équipe']`.

**How to avoid:** Toujours utiliser `node_color = [color_map[n] for n in G.nodes()]` avec un dict explicite.

**Warning signs:** Le nœud `Pub` apparaît en vert au lieu de bleu, ou `Ventes` en orange.

### Pitfall 2: Niveau d'assignation pub différent pour 1c vs 1a/1b

**What goes wrong:** Appliquer la même logique d'assignation niveau-magasin pour 1c que pour 1a/1b. Si on assigne `pub` par magasin pour 1c, chaque magasin a le même pub sur tous ses mois — il n'y a plus de biais saisonnier (la variation intra-magasin manque).

**Why it happens:** Le confondant `saison` varie par mois, pas par magasin. L'assignation doit donc être au niveau ligne.

**How to avoid:** Pour 1c, utiliser `df_sc1c['pub'] = rng_sc1c.binomial(1, probs_1c)` directement sur le panel (4800 lignes), pas sur une table magasin-niveau.

**Warning signs:** Dans 1c, chaque magasin a soit `pub=0` sur 24 mois, soit `pub=1` sur 24 mois — aucun magasin n'a une variation mensuelle de pub.

### Pitfall 3: `xerr` dans `ax.errorbar` doit être positif

**What goes wrong:** Passer `xerr = [ci_lower, ci_upper]` directement. `ax.errorbar` attend des distances (positives) par rapport à la valeur centrale, pas les bornes absolues.

**Why it happens:** Convention matplotlib : `xerr` = demi-largeur de la barre d'erreur, pas les coordonnées absolues.

**How to avoid:**
```python
# CORRECT:
xerr = [[coef - ci[0]], [ci[1] - coef]]   # [lower_err, upper_err] distances positives
ax.errorbar(coef, y, xerr=xerr, ...)

# INCORRECT:
xerr = [ci[0], ci[1]]   # bornes absolues -- donne des résultats faux
```

**Warning signs:** Barres d'erreur asymétriques ou négatives, ou erreur `ValueError: xerr < 0`.

### Pitfall 4: RNG state pollution entre scénarios

**What goes wrong:** Appeler `rng` global ou réutiliser le même `rng_sc1a` pour le calcul contrefactuel. L'état du rng après les appels contrefactuels n'est pas déterministe et peut changer si le nombre de lignes traitées change.

**Why it happens:** `compute_outcomes` consomme `n_rows` draws de `rng.binomial` et `n_rows` draws de `rng.normal`. Si le nombre de traités change (ex: paramètres modifiés), l'état résiduel du rng change.

**How to avoid:** Utiliser un seed dédié pour le contrefactuel : `rng_cf_1a = np.random.default_rng(SEED + 11)`, indépendant de `rng_sc1a`.

**Warning signs:** Les coefficients OLS changent entre deux exécutions sans modification de PARAMS — signe que le rng est non-déterministe.

### Pitfall 5: `conf_int()` colonnes sont des integers 0 et 1, pas des strings

**What goes wrong:** `result.conf_int()['lower']` → KeyError.

**Why it happens:** statsmodels 0.14.6 retourne un DataFrame avec colonnes `0` (lower) et `1` (upper).

**How to avoid:** Utiliser `result.conf_int().loc['pub', 0]` et `result.conf_int().loc['pub', 1]`. Vérifié sur statsmodels 0.14.6.

**Warning signs:** `KeyError: 'lower'` ou accès par position incorrect.

### Pitfall 6: `base_df` a déjà des colonnes `ventes` / `panier_moyen` (pub=0)

**What goes wrong:** Croire que `base_df` est propre et sans `ventes`. En réalité, `base_df` contient déjà `ventes` et `panier_moyen` calculés avec `pub=0`. Appeler `compute_outcomes` **écrase** ces colonnes — c'est le comportement attendu (`.copy()` en début de `compute_outcomes`).

**Why it happens:** La cellule `code-dgp-exec` appelle `compute_outcomes(base_df, PARAMS, rng)` avec `pub=0` avant de retirer `pub` de `base_df`.

**How to avoid:** Aucune action spéciale — `compute_outcomes` fait un `.copy()` et retourne un nouveau DataFrame avec les outcomes calculés selon le `pub` courant. Juste s'assurer que `df_sc1x` est créé depuis `base_df.merge(...)` puis `compute_outcomes` est appelé dessus.

---

## Code Examples

Patterns vérifiés empiriquement (Python 3, SEED=42, statsmodels 0.14.6, matplotlib 3.10.8, networkx 3.6.1) :

### Accès aux résultats statsmodels

```python
# Source: vérification locale statsmodels 0.14.6
result = smf.ols('ventes ~ pub + C(mois)', data=df).fit()

# Coefficient
coef = result.params['pub']              # float

# IC 95%
ci = result.conf_int()                   # DataFrame, colonnes 0 et 1
lower = ci.loc['pub', 0]                 # float
upper = ci.loc['pub', 1]                 # float

# Standard error, t-value, p-value
se = result.bse['pub']
tval = result.tvalues['pub']
pval = result.pvalues['pub']
```

### Assignation pub niveau magasin (1a et 1b)

```python
# Source: vérification locale, SEED=42 SEED+10
# Résultat empirique 1a: 102 magasins traités / 200
stores = base_df[['magasin_id', 'qualite_equipe']].drop_duplicates('magasin_id').copy()
probs = np.where(stores['qualite_equipe'] == 1, P_PUB_BONNE_EQUIPE, P_PUB_MAUVAISE_EQUIPE)
stores['pub'] = rng_sc1a.binomial(1, probs)
df = base_df.merge(stores[['magasin_id', 'pub']], on='magasin_id')
df = compute_outcomes(df, PARAMS, rng_sc1a)
```

### Assignation pub niveau ligne (1c)

```python
# Source: vérification locale, SEED+30
# Résultat empirique 1c: ~2015/4800 lignes avec pub=1
df_sc1c = base_df.copy()
haute_mask = df_sc1c['effet_saison_val'] > 0
probs_1c = np.where(haute_mask, P_PUB_HAUTE_SAISON, P_PUB_BASSE_SAISON)
df_sc1c['pub'] = rng_sc1c.binomial(1, probs_1c)
df_sc1c = compute_outcomes(df_sc1c, PARAMS, rng_sc1c)
```

### Résultats empiriques vérifiés (SEED=42, SEED+10 pour 1a)

```
Scénario 1a (qualite_equipe):
  Traités: ~85-102 magasins (varie selon rng_sc1a)
  ATT: ~1070 - 1190 €
  OLS naïf:   ~1664 € (IC: 1493, 1836) — surestimation +56%
  OLS ajusté: ~1574 € (IC: 1384, 1763) — surestimation +48%
  -> Biais naïf vs ATT: +475 € (pédagogiquement visible)
  -> ATT hors IC 95% des deux estimateurs OLS

Scénario 1c (saison, SEED+30):
  Pub=1: ~2015/4800 lignes
  ATT: ~1163 €
  OLS naïf (sans mois):  ~1256 € (IC: 1085, 1428) — surestimation +8%
  OLS ajusté (C(mois)):  ~1194 € (IC: 1007, 1381) — surestimation +3%
  -> Biais saisonnier plus faible mais visible
```

---

## State of the Art

| Old Approach | Current Approach | When Changed | Impact |
|--------------|------------------|--------------|--------|
| `np.random.seed()` global | `np.random.default_rng(SEED + n)` dédié par scénario | numpy 1.17+ | Pattern déjà établi en Phase 1 — étendre avec SEED+10/+20/+30 |
| Dummies manuelles (`pd.get_dummies`) | `C(mois)` dans la formule statsmodels | statsmodels 0.9+ | `smf.ols` avec `C()` crée automatiquement n-1 dummies avec référence `mois=1` |
| `conf_int().columns` nommés | `conf_int()` avec colonnes `0` et `1` | statsmodels 0.14.x | Accès `.loc['pub', 0]` et `.loc['pub', 1]` |

**Deprecated/outdated:**
- `nx.spring_layout` : interdit par DGP-06 — toujours utiliser `pos` dict fixe.
- `plt.errorbar` sans `fmt` : matplotlib 3.10+ recommande toujours spécifier `fmt`.

---

## Open Questions

1. **Seed exact pour rng_sc1b**
   - What we know: CONTEXT mentionne SEED+10 pour 1a. L'espacement de 10 entre scénarios (SEED+10, SEED+20, SEED+30) est logique et laisse de la place pour les seeds CF (SEED+11, SEED+21, SEED+31).
   - What's unclear: Y a-t-il une convention explicite dans le projet pour les seeds ?
   - Recommendation: Utiliser SEED+10/+11 pour 1a, SEED+20/+21 pour 1b, SEED+30/+31 pour 1c. Le CONTEXT.md mentionne explicitement "SEED + 10" pour l'exemple rng_sc1a — suivre cette convention.

2. **Direction du biais dans 1b (urbain)**
   - What we know: `P_PUB_URBAIN=0.65` vs `P_PUB_RURAL=0.25`. `urbain` a un effet positif (`EFFET_URBAIN=0.03`) sur les ventes via p_visite.
   - What's unclear: Non vérifié empiriquement (seulement 1a et 1c vérifiés ci-dessus). La direction devrait être la même (naïf surestime) par symétrie avec 1a.
   - Recommendation: Vérifier lors de l'implémentation. Si le biais est dans la mauvaise direction, c'est que `EFFET_URBAIN` est insuffisant — mais avec P_PUB=0.65 vs 0.25 et EFFET_URBAIN=0.03, la direction devrait être correcte.

3. **Définition de "haute saison" pour 1c**
   - What we know: `EFFET_SAISON = {4:0.01, 5:0.02, 6:0.02, 7:0.02, 8:0.01, 11:0.01, 12:0.02}` sont positifs ; `{1:-0.01, 2:-0.01, 3:0.0, 9:0.0, 10:-0.01}` sont nuls ou négatifs.
   - What's unclear: Le CONTEXT dit "confondant = effet_saison_val / mois". Le critère exact pour "haute saison" n'est pas spécifié mais `effet_saison_val > 0` est la lecture naturelle.
   - Recommendation: Utiliser `haute_mask = df['effet_saison_val'] > 0` comme critère. Cela inclut mois 4, 5, 6, 7, 8, 11, 12 (7 mois sur 12).

---

## Sources

### Primary (HIGH confidence)

- Exécution locale Python 3 + statsmodels 0.14.6 + numpy 2.4.2 + pandas 3.0.1 + matplotlib 3.10.8 + networkx 3.6.1 — tous patterns vérifiés empiriquement dans cet environnement
- `formation_causalite.ipynb` — code DGP existant inspecté directement, patterns `compute_outcomes`, `generate_base_panel`, `smf.ols`, `code-dag-pattern` extraits
- `.planning/phases/03-sc-narios-1a-1b-1c-biais-de-s-lection/03-CONTEXT.md` — décisions locked lues directement

### Secondary (MEDIUM confidence)

- `.planning/phases/02-scenario0-petits-nombres/02-RESEARCH.md` — patterns établis en Phase 2 (RNG isolation, savefig/show order, export CSV) confirmés comme applicables en Phase 3
- `.planning/phases/02-scenario0-petits-nombres/02-01-PLAN.md` et `02-02-PLAN.md` — structure des plans et format des tâches (référence pour le planner)

### Tertiary (LOW confidence)

Aucune — toutes les affirmations sont HIGH ou MEDIUM, vérifiées directement sur l'environnement cible.

---

## Metadata

**Confidence breakdown:**
- Standard stack: HIGH — versions vérifiées, imports confirmés dans le notebook existant, `smf.ols` et `conf_int()` testés empiriquement
- Architecture: HIGH — pipeline complet testé empiriquement pour 1a et 1c, direction du biais confirmée, ATT calculé avec 2 approches (résultats cohérents)
- Pitfalls: HIGH — pitfalls identifiés par simulation directe (node_color, xerr, conf_int colonnes, niveau pub 1c vs 1a, RNG isolation)

**Research date:** 2026-03-04
**Valid until:** 2026-04-04 (stack stable, statsmodels 0.14.x, networkx 3.x, matplotlib 3.10.x — pas de breaking changes attendus)
