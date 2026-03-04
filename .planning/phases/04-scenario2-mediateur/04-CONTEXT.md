# Phase 4: Scénario 2 — Surcontrôle sur un médiateur - Context

**Gathered:** 2026-03-04
**Status:** Ready for planning
**Source:** Héritée des décisions Phase 3 (formateur : "mêmes décisions")

<domain>
## Phase Boundary

Produire le scénario 2 : montrer que contrôler sur `panier_moyen` (un médiateur) dans la régression biaise le coefficient de `pub` vers zéro. Le scénario utilise un panel avec assignation pub aléatoire (pas de confondant) — le naïf `log_rev_int ~ pub` est correct, et `log_rev_int ~ pub + panier_moyen` est biaisé vers le bas. Un DAG illustre les deux chemins causaux. Pas de médiateur partiel, pas de décomposition directe/indirecte — juste la comparaison OLS avec vs sans contrôle sur le médiateur.

</domain>

<decisions>
## Implementation Decisions

### Variable dépendante
- DV = **`log_rev_int = log(ventes / n_potentiel)`** — log-points ≈ % uplift
- Même DV que Phase 3 (refactoring validé, décision formateur)
- Coefficients OLS en log-points (pas en €)

### Structure du scénario
- **Un seul scénario** (pas de sous-scénarios 2a/2b/2c)
- Assignation pub **aléatoire** au niveau magasin (pas de confondant — contraste avec Phase 3)
- Le biais vient du sur-contrôle, pas de la sélection
- `panier_moyen` est le médiateur : `pub → panier_moyen → ventes` ET `pub → nb_visites → ventes`

### Comparaison OLS
- OLS sans médiateur : `log_rev_int ~ pub` → effet total (proche de la vérité)
- OLS avec médiateur : `log_rev_int ~ pub + panier_moyen` → effet direct seulement (biaisé vers le bas)
- Valeur vraie : ATT contrefactuel (ou calculé via PARAMS si plus stable empiriquement)

### Figures — 3 au total
- **Une par type** : 1 DAG + 1 coefficient plot + 1 bar chart → 3 PNG dans `figures/`
- Naming : `sc2_dag.png`, `sc2_coeff.png`, `sc2_bar.png`
- Pas de figure composite

### DAG — nœuds
- Même pattern Phase 3 : `nx.DiGraph`, `pos` dict fixe, `draw_networkx`, nœuds colorés
- Labels verbeux en français pour les slides : `Pub`, `Ventes`, `Panier moyen`, `Nb visites`
- Deux chemins causaux visibles : `Pub → Nb visites → Ventes` ET `Pub → Panier moyen → Ventes`
- Nœuds couleurs cohérentes : Pub=steelblue, Ventes=seagreen, médiateurs=darkorange/mediumpurple

### Coefficient plot
- Style **vertical** : un point par estimateur sur l'axe Y, valeur sur l'axe X
- **Barres d'erreur IC 95%** pour les deux estimateurs OLS
- 3 points : OLS sans contrôle, OLS avec `panier_moyen`, Valeur vraie (ATT)
- xlabel : `"Uplift log des ventes (≈ %)"` — cohérent avec Phase 3

### Bar chart
- 3 barres : sans contrôle (rouge), avec médiateur (bleu), valeur vraie (vert)
- Ligne pointillée horizontale à la valeur vraie
- ylabel : `"Uplift log des ventes (≈ %)"`

### Claude's Discretion
- Seed dédié pour Phase 4 : `rng_sc2 = np.random.default_rng(SEED + 40)` (convention +10×phase)
- Niveau d'assignation pub (magasin ou ligne) — cohérent avec scénarios non-saisonniers → niveau magasin
- Couleurs exactes des nœuds DAG (cohérentes avec sc1x)
- Labels exacts des axes et titres (factuel, sans commentaire interprétatif)

</decisions>

<code_context>
## Existing Code Insights

### Reusable Assets
- `generate_base_panel(params, rng)` et `compute_outcomes(df, params, rng)` — disponibles
- Pattern assignation pub niveau magasin (drop_duplicates + merge) — sc1a/sc1b pattern
- Pattern DAG avec `pos` dict fixe — sc1x pattern
- Pattern coefficient plot avec `ax.errorbar` — sc1x pattern
- `log_rev_int = np.log(df['ventes'] / df['n_potentiel'])` — sc1x pattern
- ATT contrefactuel : rng dédié `np.random.default_rng(SEED + 41)` pour isolation

### DGP Mediator Structure
```python
# Dans compute_outcomes :
mu_panier = params['mu_panier_base'] * (1 + params['effet_pub_panier'] * df['pub'])
# → pub affecte panier_moyen (médiateur pur)
# → ventes = nb_visites * mu_panier + bruit
# → panier_moyen = ventes / nb_visites (ratio dérivé)
```
EFFET_PUB_PANIER = 0.10 et EFFET_PUB_VISITES = 0.10 (mêmes ordres de grandeur)

### Integration Points
- Insérer après les cellules Phase 3 (scénario 1c) dans le notebook
- `base_df` disponible en mémoire
- Export CSV : `data/sc2_mediateur.csv`

</code_context>

<specifics>
## Specific Ideas

- Le scénario 2 est pédagogiquement l'inverse du scénario 1 : pas de confondant mais un médiateur. L'étudiant voit que même une régression "naïve" peut être correcte si le DGP n'a pas de biais de sélection.
- `panier_moyen = ventes / nb_visites` est une variable dérivée dans le DGP — contrôler dessus bloque mécaniquement le chemin panier_moyen → ventes et crée un biais.

</specifics>

<deferred>
## Deferred Ideas

Aucune — Phase 4 est le seul scénario médiateur.

</deferred>

---

*Phase: 04-scenario2-mediateur*
*Context gathered: 2026-03-04 (héritée de Phase 3)*
