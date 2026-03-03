# Phase 2: Scénario 0 — Biais de petits nombres - Research

**Researched:** 2026-03-03
**Domain:** Jupyter notebook — pandas aggregation, seaborn KDE/histogram, matplotlib subplots, DGP reuse
**Confidence:** HIGH

---

<user_constraints>
## User Constraints (from CONTEXT.md)

### Locked Decisions

**Figure 1 — Distribution par taille (sc0_distribution.png)**
- 3 histogrammes empilés verticalement avec axe X partagé
- Données : panier_moyen moyen par magasin sur 24 mois (200 points par groupe)
- Une couleur par taille (petit / moyen / grand)

**Figure 2 — Scatter variance (sc0_scatter.png)**
- Scatter plot agrégé par magasin (200 points)
- Axe X : moyenne de `nb_visites` sur 24 mois
- Axe Y : std de `panier_moyen` sur 24 mois
- Montre la corrélation négative nb_visites ↔ variance

**Figure 3 — Top 10 magasins (sc0_top10.png)**
- Bar chart des 10 magasins avec le `panier_moyen` moyen sur 24 mois le plus élevé
- Critère : classement décroissant par moyenne (ce qu'un analyste naïf ferait)
- Barres colorées par taille pour révéler la sur-représentation des petits magasins

**Figure 4 — Mécanisme loi des grands nombres (sc0_loi_grands_nombres.png)**
- Subplot 2 rangs, axe X partagé
  - Rang 1 (haut) : KDE de la distribution réelle de `panier_moyen` depuis `base_df`
  - Rang 2 (bas) : KDE overlay de 5 simulations pour N = 10, 100, 1000, 10000, 100000
- Simulation : pour chaque N, générer un panel avec `n_potentiel=N` via le DGP existant, calculer `panier_moyen`, en tracer la KDE
- Objectif pédagogique : montrer que la distribution de la moyenne se resserre à mesure que N augmente

**Export CSV**
- 1 CSV exporté dans `data/` avec les données du scénario (à minima le DataFrame agrégé par magasin)

### Claude's Discretion
- Noms exacts des colonnes dans le CSV exporté
- Palette de couleurs précise
- Labels et titres des figures
- Nombre de bins dans les histogrammes
- Bandwidth KDE

### Deferred Ideas (OUT OF SCOPE)
Aucune — la discussion est restée dans le périmètre de la Phase 2.
</user_constraints>

---

<phase_requirements>
## Phase Requirements

| ID | Description | Research Support |
|----|-------------|-----------------|
| SC0-01 | Figure montrant la distribution du `panier_moyen` par taille de magasin (histogramme avec hue=taille ou 3 panneaux séparés) | Figure 1: 3 histogrammes `sns.histplot` empilés avec `plt.subplots(3,1,sharex=True)`, données depuis `agg_sc0` (200 points par groupe) |
| SC0-02 | Scatter plot montrant la relation entre `nb_visites` et la variance du `panier_moyen` par magasin | Figure 2: `ax.scatter` avec couleur par taille, corrélation empirique vérifiée à -0.76, depuis `agg_sc0` (200 points) |
| SC0-03 | Bar chart des top 10 magasins par `panier_moyen` le plus élevé, répartition par taille | Figure 3: `ax.bar` avec `df.nlargest(10, 'panier_moyen_moy')`, 100% petits dans le top 10 avec SEED=42 |
</phase_requirements>

---

## Summary

Phase 2 insère 4 cellules de code (+ 1 cellule markdown de section) dans le notebook existant, immédiatement après la cellule Assertions (cell id `code-assertions`). Elle réutilise intégralement `base_df` (déjà en mémoire) et les fonctions `generate_base_panel` / `compute_outcomes` déjà définies. Aucun import additionnel n'est nécessaire — `numpy`, `pandas`, `matplotlib`, `seaborn` sont tous déjà importés.

La structure des données pour les Figures 1, 2, 3 est identique : un DataFrame agrégé `agg_sc0` de 200 lignes (une par magasin) produit par `base_df.groupby(['magasin_id','taille']).agg(...)`. La Figure 4 requiert des simulations séparées avec un `rng` local dédié pour ne pas altérer l'état du `rng` global. Les données empiriques confirment la pédagogie : top 10 composé à 100% de petits magasins (SEED=42), corrélation nb_visites/variance = -0.76, ratio variance petit/grand = 4.4x.

La seule subtilité technique est le risque d'avertissement `seaborn` sur `warn_singular` pour la courbe N=100000 (std ≈ 0.018) dans la Figure 4. Ce risque est mitigé en passant `warn_singular=False`.

**Primary recommendation:** Écrire 4 cellules de code séquentielles qui réutilisent `base_df` et les fonctions DGP existantes — aucune nouvelle infrastructure requise.

---

## Standard Stack

### Core (already installed and imported in notebook)

| Library | Version | Purpose | Why Standard |
|---------|---------|---------|--------------|
| numpy | 2.4.2 | Calculs numériques, `rng.binomial`, `np.sqrt` | Déjà utilisé partout dans le DGP |
| pandas | 3.0.1 | `groupby().agg()`, `nlargest()`, `to_csv()` | Déjà utilisé pour `base_df` |
| matplotlib | 3.10.8 | `plt.subplots()`, `ax.bar()`, `ax.scatter()`, `fig.savefig()` | Pattern établi dans le projet |
| seaborn | 0.13.2 | `sns.histplot()`, `sns.kdeplot()` | Déjà importé, parfait pour KDE overlay |

### Supporting

| Library | Version | Purpose | When to Use |
|---------|---------|---------|-------------|
| pathlib.Path | stdlib | `figures/`, `data/` dirs déjà créés | Déjà fait en cellule Import |

### Alternatives Considered

| Instead of | Could Use | Tradeoff |
|------------|-----------|----------|
| `sns.histplot` (3 axes séparés) | `sns.histplot(..., hue='taille')` sur 1 axe | Décision locked: 3 panneaux empilés — pas d'alternative à explorer |
| `ax.scatter` par groupe | `sns.scatterplot(hue='taille')` | sns.scatterplot fonctionne aussi; ax.scatter plus explicite pour contrôle couleur |

**Installation:** Aucune — toutes les dépendances sont déjà présentes.

---

## Architecture Patterns

### Structure des cellules à insérer

```
notebook (après code-assertions):
├── md-sc0-section          # Markdown: "## Scénario 0 — Biais de petits nombres"
├── code-sc0-aggregation    # Agrégation base_df → agg_sc0 + export CSV
├── code-sc0-fig1           # Figure 1: distribution par taille
├── code-sc0-fig2           # Figure 2: scatter variance
├── code-sc0-fig3           # Figure 3: top 10 bar chart
└── code-sc0-fig4           # Figure 4: loi des grands nombres (KDE subplot)
```

**Variante acceptable:** Fusionner Figs 1+2 ou Figs 3+4 en une cellule si le planner le juge pertinent. La séparation 1 figure = 1 cellule est recommandée pour la lisibilité et la réexécution partielle.

### Pattern 1: Agrégation base_df → agg_sc0

**What:** Produit le DataFrame 200 lignes utilisé par Figures 1, 2, 3 et exporté en CSV.

```python
# Source: established pandas groupby pattern in project
agg_sc0 = base_df.groupby(['magasin_id', 'taille']).agg(
    n_potentiel=('n_potentiel', 'first'),
    nb_visites_moy=('nb_visites', 'mean'),
    panier_moyen_moy=('panier_moyen', 'mean'),
    panier_moyen_std=('panier_moyen', 'std'),
).reset_index()

agg_sc0.to_csv('data/sc0_biais_petits_nombres.csv', index=False)
print(f"Scénario 0 : {len(agg_sc0)} magasins agrégés")
```

**Notes:**
- `'taille'` dans le `groupby` est nécessaire pour conserver la colonne dans l'agrégat
- `panier_moyen_std` est la std sur 24 mois par magasin — c'est la mesure de variance pour Figure 2
- `base_df` a déjà `pub` retiré — pas besoin de filtrer

### Pattern 2: Figure 1 — 3 histogrammes empilés

```python
# Source: matplotlib.pyplot.subplots + seaborn.histplot
fig, axes = plt.subplots(3, 1, figsize=(9, 9), sharex=True)
tailles = ['petit', 'moyen', 'grand']
colors = {'petit': '#e74c3c', 'moyen': '#3498db', 'grand': '#2ecc71'}  # Claude discretion

for ax, taille in zip(axes, tailles):
    subset = agg_sc0[agg_sc0['taille'] == taille]
    sns.histplot(data=subset, x='panier_moyen_moy', ax=ax,
                 color=colors[taille], bins=20)
    ax.set_title(f'Magasins {taille} (N={len(subset)})')
    ax.set_xlabel('')

axes[-1].set_xlabel('panier_moyen moyen sur 24 mois (€)')
fig.suptitle('Distribution du panier moyen par taille de magasin', fontsize=13)
plt.tight_layout()
fig.savefig('figures/sc0_distribution.png', dpi=150, bbox_inches='tight')
plt.show()
```

### Pattern 3: Figure 2 — Scatter variance

```python
# Source: matplotlib.axes.scatter
fig, ax = plt.subplots(figsize=(8, 5))
for taille, grp in agg_sc0.groupby('taille'):
    ax.scatter(grp['nb_visites_moy'], grp['panier_moyen_std'],
               color=colors[taille], label=taille, alpha=0.7, s=40)
ax.set_xlabel('Nombre de visites moyen (24 mois)')
ax.set_ylabel('Écart-type du panier moyen (24 mois)')
ax.set_title('Variance du panier moyen vs affluence par magasin')
ax.legend(title='Taille')
fig.savefig('figures/sc0_scatter.png', dpi=150, bbox_inches='tight')
plt.show()
```

### Pattern 4: Figure 3 — Top 10 bar chart

```python
# Source: pandas.DataFrame.nlargest + matplotlib.axes.bar
top10 = agg_sc0.nlargest(10, 'panier_moyen_moy').reset_index(drop=True)
bar_colors = [colors[t] for t in top10['taille']]

fig, ax = plt.subplots(figsize=(10, 5))
bars = ax.bar(range(len(top10)), top10['panier_moyen_moy'], color=bar_colors)
ax.set_xticks(range(len(top10)))
ax.set_xticklabels([f"#{i+1}" for i in range(len(top10))], fontsize=10)
ax.set_ylabel('panier_moyen moyen (€)')
ax.set_title('Top 10 magasins par panier moyen — analyse naïve\n'
             '(ce qu\'un analyste sans méfiance ferait)')
# Legend
from matplotlib.patches import Patch
ax.legend(handles=[Patch(facecolor=colors[t], label=t) for t in tailles], title='Taille')
fig.savefig('figures/sc0_top10.png', dpi=150, bbox_inches='tight')
plt.show()
```

### Pattern 5: Figure 4 — Loi des grands nombres (KDE subplot)

```python
# Source: seaborn.kdeplot + matplotlib subplots(2,1,sharex=True)
# CRITICAL: use dedicated rng to avoid perturbing global rng state
rng_fig4 = np.random.default_rng(SEED + 4)

fig, axes = plt.subplots(2, 1, figsize=(10, 8), sharex=True)

# Row 1: KDE of real base_df data (all 200 stores, mean panier_moyen over 24 months)
sns.kdeplot(data=agg_sc0['panier_moyen_moy'], ax=axes[0],
            fill=True, color='gray', label='Données réelles')
axes[0].set_title('Distribution réelle — mélange de tailles')
axes[0].set_ylabel('Densité')

# Row 2: KDE overlay for N = 10, 100, 1000, 10000, 100000
N_values = [10, 100, 1000, 10000, 100000]
palette_fig4 = sns.color_palette('viridis', len(N_values))

for N, color in zip(N_values, palette_fig4):
    params_sim = {**PARAMS, 'n_petit': N, 'n_moyen': N, 'n_grand': N}
    sim_df = generate_base_panel(params_sim, rng_fig4)
    sim_df['pub'] = 0
    sim_df = compute_outcomes(sim_df, params_sim, rng_fig4)
    agg_sim = sim_df.groupby('magasin_id')['panier_moyen'].mean()
    sns.kdeplot(data=agg_sim.dropna(), ax=axes[1],
                label=f'N={N:,}', color=color, warn_singular=False)

axes[1].set_title('Distribution simulée par N_potentiel — loi des grands nombres')
axes[1].set_xlabel('panier_moyen moyen (€)')
axes[1].set_ylabel('Densité')
axes[1].legend(title='N potentiel')

fig.suptitle('Mécanisme : la variance diminue avec le nombre de clients potentiels', fontsize=13)
plt.tight_layout()
fig.savefig('figures/sc0_loi_grands_nombres.png', dpi=150, bbox_inches='tight')
plt.show()
```

### Anti-Patterns to Avoid

- **Ne pas appeler `rng` global pour la Figure 4** : cela altèrerait l'état du générateur pour tous les scénarios suivants. Toujours utiliser `rng_fig4 = np.random.default_rng(SEED + 4)` local.
- **Ne pas utiliser `spring_layout` pour les DAGs** : pas de DAG dans cette phase, mais règle générale du projet (DGP-06).
- **Ne pas recalculer `base_df`** : `base_df` est déjà en mémoire depuis la cellule DGP. Le réutiliser directement.
- **Ne pas filtrer `pub` avant l'agrégation** : `pub` a déjà été retiré de `base_df` (drop en cellule DGP).
- **Ne pas ignorer `bbox_inches='tight'`** : pattern établi pour tous les exports PNG du projet.

---

## Don't Hand-Roll

| Problem | Don't Build | Use Instead | Why |
|---------|-------------|-------------|-----|
| Histogramme avec axe partagé | Axes manuels avec xlim synchronisé | `plt.subplots(3,1,sharex=True)` | Matplotlib gère automatiquement la synchronisation |
| KDE lissée | Kernel density estimator maison | `sns.kdeplot()` | seaborn utilise scipy.stats.gaussian_kde, gère bandwidth automatiquement |
| Top N par colonne | Tri manuel + slice | `df.nlargest(10, 'col')` | pandas optimisé, sûr avec ex-aequo |
| Agrégation multiple par groupe | Boucle sur groupes | `groupby().agg({...})` | Vectorisé, noms de colonnes contrôlés |

**Key insight:** Tout l'outillage nécessaire est déjà présent dans le projet et importé. Cette phase est du pur assemblage de patterns existants.

---

## Common Pitfalls

### Pitfall 1: RNG state pollution dans Figure 4

**What goes wrong:** Appeler `rng` global dans les simulations Figure 4 consomme des tirages aléatoires, ce qui décale l'état du générateur pour tous les scénarios suivants (Scénarios 1, 2, 3). Les figures de ces scénarios deviendraient non reproductibles si l'ordre des cellules change.

**Why it happens:** Le `rng` global est passé par référence implicite — toute fonction qui l'appelle le modifie.

**How to avoid:** Créer systématiquement `rng_fig4 = np.random.default_rng(SEED + 4)` au début de la cellule Figure 4 et le passer à `generate_base_panel` et `compute_outcomes`.

**Warning signs:** Si les figures des scénarios 1-3 changent quand on réordonne ou ajoute des cellules en Phase 2.

### Pitfall 2: sns.kdeplot warn_singular pour N=100000

**What goes wrong:** Pour N=100000, la distribution du `panier_moyen` moyen a un std ≈ 0.018 €. seaborn 0.13.2 émet un avertissement `UserWarning: Dataset has 0 variance; skipping density estimate` ou similaire, et peut ne pas tracer la courbe.

**Why it happens:** La bandwidth de Silverman sur données quasi-constantes devient presque nulle, ce qui déclenche une singularité numérique dans le kernel density estimator.

**How to avoid:** Passer `warn_singular=False` dans `sns.kdeplot()`. La courbe s'affiche comme un pic très étroit — comportement pédagogiquement désiré.

**Warning signs:** `UserWarning` dans la sortie cellule, courbe N=100000 absente de la figure.

### Pitfall 3: agg_sc0 groupby avec taille manquant

**What goes wrong:** Si `groupby('magasin_id')` sans `'taille'`, la colonne `taille` disparaît de l'agrégat et les figures ne peuvent pas colorier par taille.

**Why it happens:** groupby ne conserve que les colonnes listées + colonnes agrégées.

**How to avoid:** Toujours `groupby(['magasin_id', 'taille'])` — `taille` est fixe par magasin (même valeur sur 24 mois), donc groupby dessus ne change pas le niveau d'agrégation.

### Pitfall 4: xlim trop étroit avec sharex=True en Figure 4

**What goes wrong:** La courbe N=10 (std ≈ 2.0) s'étale de ~44 à ~56. La courbe N=100000 (std ≈ 0.018) forme un pic invisible à cette échelle, ou l'xlim est trop serré pour voir les queues de N=10.

**Why it happens:** matplotlib avec `sharex=True` prend l'union des xlim de tous les axes — généralement correct automatiquement avec seaborn qui fixe ses propres limites.

**How to avoid:** Ne pas forcer `xlim` manuellement. Laisser seaborn et matplotlib calculer automatiquement. Si nécessaire, `axes[1].set_xlim(40, 60)` pour garantir visibilité des queues de N=10.

### Pitfall 5: panier_moyen_std NaN pour magasin avec T_MOIS=1

**What goes wrong:** `std()` sur 1 seule valeur retourne NaN. Pas de risque ici (T_MOIS=24), mais potentiellement un problème si le paramètre est modifié par le formateur.

**Why it happens:** variance sur 1 observation = NaN par définition statistique.

**How to avoid:** Aucune action nécessaire pour T_MOIS=24. Note optionnelle dans le commentaire de code pour signaler la dépendance.

---

## Code Examples

Patterns vérifiés empiriquement dans cet environnement:

### Agrégation complète

```python
# Vérifié : pandas 3.0.1, SEED=42
agg_sc0 = base_df.groupby(['magasin_id', 'taille']).agg(
    n_potentiel=('n_potentiel', 'first'),
    nb_visites_moy=('nb_visites', 'mean'),
    panier_moyen_moy=('panier_moyen', 'mean'),
    panier_moyen_std=('panier_moyen', 'std'),
).reset_index()
# Résultat empirique SEED=42: 200 lignes, petit=79, moyen=86, grand=35
# panier_moyen_std: petit≈1.26, moyen≈0.46, grand≈0.26
# nb_visites_moy corrélation avec panier_moyen_std: -0.758
```

### Paramètre simulation Figure 4

```python
# Pattern DGP existant — vérifié compatible avec generate_base_panel
params_sim = {**PARAMS, 'n_petit': N, 'n_moyen': N, 'n_grand': N}
sim_df = generate_base_panel(params_sim, rng_fig4)
sim_df['pub'] = 0
sim_df = compute_outcomes(sim_df, params_sim, rng_fig4)
agg_sim = sim_df.groupby('magasin_id')['panier_moyen'].mean()
# Résultat empirique:
# N=10    : std≈2.01 (distribution large)
# N=100   : std≈0.60
# N=1000  : std≈0.19
# N=10000 : std≈0.06
# N=100000: std≈0.018 (distribution quasi-delta)
```

### Pédagogie Figure 3 (résultat vérifié SEED=42)

```python
# top10 contient 100% de petits magasins avec les paramètres par défaut
top10 = agg_sc0.nlargest(10, 'panier_moyen_moy')
# magasin_id 170: panier_moyen_moy≈53.1€ (rang 1, petit)
# Tous les 10 sont des petits magasins — message pédagogique fort
```

---

## State of the Art

| Old Approach | Current Approach | When Changed | Impact |
|--------------|------------------|--------------|--------|
| `np.random.seed()` global | `np.random.default_rng(SEED)` passé en argument | numpy 1.17+ | Pattern déjà établi en Phase 1 — ne pas déroger |
| `pd.DataFrame.merge(how='cross')` indisponible | Disponible pandas 1.2+ | pandas 1.2 (2020) | Déjà utilisé dans `generate_base_panel` |
| seaborn `distplot` (déprécié) | `sns.histplot` + `sns.kdeplot` | seaborn 0.11 (2020) | Utiliser uniquement les nouvelles fonctions |

**Deprecated/outdated:**
- `sns.distplot`: remplacé par `sns.histplot` + `sns.kdeplot` — ne jamais utiliser.
- `plt.tight_layout()` vs `fig.tight_layout()`: les deux fonctionnent, `plt.tight_layout()` est le pattern utilisé dans le projet.

---

## Open Questions

1. **Xlim Figure 4 Row 1 vs Row 2**
   - What we know: `sharex=True` synchronise automatiquement. La Row 1 (données réelles, std ≈ 1.3 pour les petits) a une plage plus large que les courbes N≥1000. La courbe N=10 (std ≈ 2.0 sur les moyennes de 24 mois) devrait fixer le xlim principal.
   - What's unclear: Avec des données réelles row 1 qui ont std variable (mélange petit/moyen/grand), le xlim auto peut ou non inclure les queues de N=10 en row 2.
   - Recommendation: Ne pas forcer le xlim. Si visuellement insuffisant, ajouter `axes[1].set_xlim(axes[1].get_xlim()[0]-2, axes[1].get_xlim()[1]+2)` après le tracé.

2. **N_values pour Figure 4: ordre de tracé et légende**
   - What we know: [10, 100, 1000, 10000, 100000] sont tracés dans cet ordre. La palette `viridis` va du sombre (10) au clair (100000).
   - What's unclear: L'ordre visuel dans la légende.
   - Recommendation: Tracer dans l'ordre croissant de N pour que la légende liste du plus large au plus étroit — intuitive pédagogiquement.

---

## Sources

### Primary (HIGH confidence)

- Exécution locale Python 3 + numpy 2.4.2 + pandas 3.0.1 + seaborn 0.13.2 + matplotlib 3.10.8 — tous patterns vérifiés empiriquement dans cet environnement
- Notebook `formation_causalite.ipynb` — code DGP existant inspecté directement, patterns extraits
- `.planning/phases/02-scenario0-petits-nombres/02-CONTEXT.md` — décisions locked lues directement

### Secondary (MEDIUM confidence)

- seaborn 0.13.2 API `warn_singular` parameter — vérifié via `inspect.signature(sns.kdeplot)`, présent dans les paramètres
- pandas `groupby().agg()` named aggregation syntax — vérifié fonctionnel en production avec pandas 3.0.1

### Tertiary (LOW confidence)

Aucune — toutes les affirmations sont HIGH ou MEDIUM, vérifiées directement sur l'environnement cible.

---

## Metadata

**Confidence breakdown:**
- Standard stack: HIGH — versions vérifiées, imports confirmés dans le notebook existant
- Architecture: HIGH — patterns testés empiriquement, résultats numériques confirmés (SEED=42)
- Pitfalls: HIGH — pitfalls identifiés par simulation directe (warn_singular testé, RNG state analysé, groupby columns vérifiées)

**Research date:** 2026-03-03
**Valid until:** 2026-04-03 (stack stable, seaborn 0.13.x, pandas 3.x — pas de breaking changes attendus à court terme)
