# Phase 2: Scénario 0 — Biais de petits nombres - Context

**Gathered:** 2026-03-03
**Status:** Ready for planning

<domain>
## Phase Boundary

Produire 4 figures pédagogiques et 1 CSV illustrant pourquoi les petits magasins dominent les extrêmes de distribution du `panier_moyen` en raison de la variance binomiale. Les figures vont du concret (données réelles du DGP) vers le mécanisme (simulation CLT). Aucune régression, aucun test statistique — pure visualisation exploratoire.

</domain>

<decisions>
## Implementation Decisions

### Figure 1 — Distribution par taille (sc0_distribution.png)
- 3 histogrammes **empilés verticalement** avec axe X partagé
- Données : **panier_moyen moyen par magasin** sur 24 mois (200 points par groupe)
- Une couleur par taille (petit / moyen / grand)

### Figure 2 — Scatter variance (sc0_scatter.png)
- Scatter plot **agrégé par magasin** (200 points)
- Axe X : moyenne de `nb_visites` sur 24 mois
- Axe Y : std de `panier_moyen` sur 24 mois
- Montre la corrélation négative nb_visites ↔ variance

### Figure 3 — Top 10 magasins (sc0_top10.png)
- Bar chart des 10 magasins avec le `panier_moyen` **moyen sur 24 mois** le plus élevé
- Critère : ce qu'un analyste naïf ferait — classement décroissant par moyenne
- Barres colorées par taille pour révéler la sur-représentation des petits magasins

### Figure 4 — Mécanisme loi des grands nombres (sc0_loi_grands_nombres.png)
- **Subplot 2 rangs, axe X partagé :**
  - Rang 1 (haut) : KDE de la distribution réelle de `panier_moyen` depuis `base_df`
  - Rang 2 (bas) : KDE overlay de 5 simulations pour N = 10, 100, 1000, 10000, 100000
- Simulation : pour chaque N, générer un panel avec `n_potentiel=N` via le DGP existant, calculer `panier_moyen`, en tracer la KDE
- Objectif pédagogique : montrer que la distribution de la moyenne se resserre à mesure que N augmente

### Export CSV
- 1 CSV exporté dans `data/` avec les données du scénario (à minima le DataFrame agrégé par magasin utilisé pour les figures)

### Claude's Discretion
- Noms exacts des colonnes dans le CSV exporté
- Palette de couleurs précise
- Labels et titres des figures
- Nombre de bins dans les histogrammes
- Bandwidth KDE

</decisions>

<code_context>
## Existing Code Insights

### Reusable Assets
- `generate_base_panel(params, rng)` : disponible — Phase 2 l'appelle avec des `PARAMS` modifiés pour faire varier `n_petit/n_moyen/n_grand` dans la Figure 4
- `compute_outcomes(df, params, rng)` : disponible — à appeler avec `pub=0` pour les simulations Figure 4
- `base_df` : déjà calculé en mémoire (4800 lignes, pub=0 partout) — Figure 1, 2, 3 l'utilisent directement
- Pattern `fig.savefig(..., dpi=150, bbox_inches='tight')` avant `plt.show()` — à respecter pour tous les exports PNG

### Established Patterns
- `rng = np.random.default_rng(SEED)` passé en argument — pour la Figure 4, créer un `rng` local dédié pour les simulations afin de ne pas perturber l'état global
- Agrégation pandas : `base_df.groupby('magasin_id').agg(...)` pour produire les 200 points des Figures 1, 2, 3
- seaborn (`sns`) importé — disponible pour KDE (`sns.kdeplot`) et histogrammes (`sns.histplot`)

### Integration Points
- Les 4 cellules du scénario s'insèrent après la cellule Assertions dans le notebook
- Aucun paramètre nouveau requis dans la cellule Paramètres — `N_PETIT`, `N_MOYEN`, `N_GRAND` et `MU_PANIER_BASE`/`SIGMA_PANIER` existent déjà

</code_context>

<specifics>
## Specific Ideas

- Figure 3 (top 10) : le cadrage "ce qu'un analyste naïf ferait" est intentionnel — le titre ou la note de la figure peut le souligner pour le formateur
- Figure 4 : la progression N=10→100000 doit rendre visuellement évident le rétrécissement de la distribution — choisir une plage N qui maximise le contraste pédagogique

</specifics>

<deferred>
## Deferred Ideas

Aucune — la discussion est restée dans le périmètre de la Phase 2.

</deferred>

---

*Phase: 02-scenario0-petits-nombres*
*Context gathered: 2026-03-03*
