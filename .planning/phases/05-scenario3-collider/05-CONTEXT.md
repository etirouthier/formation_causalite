# Phase 5: Scénario 3 — Surcontrôle sur un collider - Context

**Gathered:** 2026-03-04
**Status:** Ready for planning

<domain>
## Phase Boundary

Produire le scénario 3 : montrer que contrôler sur `posts_reseaux` (un collider) introduit un biais là où l'estimation naïve (`log_rev_int ~ pub`) était correcte. Le scénario utilise une assignation pub aléatoire (pas de confondant — même principe que Phase 4), et `posts_reseaux` est causé à la fois par `pub` et par `ventes`. Un DAG illustre la structure collider. Pas de médiateur, pas de sélection — uniquement la comparaison OLS sans vs avec contrôle sur le collider.

</domain>

<decisions>
## Implementation Decisions

### DGP du collider — posts_reseaux
- Variable **continue** calculée au **niveau magasin**
- Équation : `posts_reseaux = a * pub × ventes_agg + bruit` (terme d'interaction, pas additif)
  - `pub` : assignation magasin (0/1)
  - `ventes_agg` : ventes agrégées par magasin (somme sur les mois)
  - bruit : terme gaussien pour réalisme
- Structure collider : `pub → posts_reseaux ← ventes` — posts_reseaux est causé par les deux
- Narratif laissé au formateur (variable flexible, pas encore nommée définitivement)

### Paramètres exposés dans PARAMS
- `COLLIDER_PUB_VENTES_COEFF` (ou équivalent ALL_CAPS) dans la cellule Paramètres
- Permet de recalibrer si le biais observé est insuffisant (< 5%) ou trop fort
- Convention de seed : `rng_sc3 = np.random.default_rng(SEED + 50)` (convention +10×phase)

### Régressions OLS
- OLS naïf : `log_rev_int ~ pub` → effet total (proche de la vérité, pas de confondant)
- OLS sur-contrôlé : `log_rev_int ~ pub + posts_reseaux` → biaisé (direction déterminée empiriquement)
- Valeur vraie : ATT contrefactuel (même pattern que Phase 4)
- Biais requis : au moins 5% de différence visible (success criteria roadmap)

### Figures — 3 au total (même structure que Phase 4)
- `sc3_dag.png` — DAG networkx, même style que sc2 (pos dict fixe, nœuds colorés)
- `sc3_coeff.png` — coefficient plot vertical, 3 points avec IC 95%
- `sc3_bar.png` — bar chart 3 barres (naïf / sur-contrôlé / vrai) + ligne pointillée
- Naming cohérent avec la convention `sc{N}_*.png`

### DAG — structure
- Même pattern Phase 4 : `nx.DiGraph`, `pos` dict fixe, `draw_networkx`, nœuds colorés
- Nœuds : `Pub`, `Ventes`, `Posts réseaux` (collider), `Nb visites` (si utile)
- Structure en V inversé visible : `Pub → Posts réseaux ← Ventes`
- Couleur collider distincte des médiateurs (à décider par Claude)
- Labels verbeux en français pour les slides

### Claude's Discretion
- Direction effective du biais (vers le haut ou le bas — déterminée empiriquement par les coefficients)
- Couleur exacte du nœud collider dans le DAG
- Valeur initiale de COLLIDER_PUB_VENTES_COEFF (à calibrer pour ≥ 5% de biais)
- Nœuds DAG : inclure ou non `Nb visites` selon lisibilité
- Labels exacts des axes et titres

</decisions>

<code_context>
## Existing Code Insights

### Reusable Assets
- `generate_base_panel(params, rng)` et `compute_outcomes(df, params, rng)` — disponibles
- Pattern assignation pub aléatoire niveau magasin (sc2) — directement réutilisable
- Pattern DAG avec `pos` dict fixe, `draw_networkx` — sc1x et sc2
- Pattern coefficient plot vertical avec `ax.errorbar` — sc1x et sc2
- Pattern bar chart 3 barres + ligne pointillée — sc2
- `log_rev_int = np.log(df['ventes'] / df['n_potentiel'])` — pattern sc1x/sc2
- Pattern ATT contrefactuel avec rng dédié — sc2 (`rng_sc2 = np.random.default_rng(SEED + 41)`)

### Established Patterns
- Seed dédié par scénario : `rng_sc3 = np.random.default_rng(SEED + 50)`
- Export CSV : `data/sc3_collider.csv`
- Tous les paramètres numériques dans PARAMS (ALL_CAPS)
- Figures exportées en PNG dans `figures/`

### Integration Points
- Insérer après les cellules Phase 4 (scénario 2 — médiateur) dans le notebook
- `base_df` disponible en mémoire
- `PARAMS` dict disponible — ajouter `COLLIDER_PUB_VENTES_COEFF`

</code_context>

<specifics>
## Specific Ideas

- Le scénario 3 est la troisième variation sur l'assignation aléatoire : l'étudiant voit que même sans confondant et même en ne contrôlant pas "trop" naïvement, une variable post-traitement peut créer un biais si elle est un collider.
- Contraste pédagogique : Phase 3 (confondant → ajuster corrige), Phase 4 (médiateur → ajuster biaise), Phase 5 (collider → ajuster biaise aussi, mais différemment).
- Narratif de la variable flexible — le formateur décidera si c'est "nombre de posts Instagram", "score de visibilité réseaux", etc.

</specifics>

<deferred>
## Deferred Ideas

Aucune — discussion restée dans le périmètre de la phase.

</deferred>

---

*Phase: 05-scenario3-collider*
*Context gathered: 2026-03-04*
