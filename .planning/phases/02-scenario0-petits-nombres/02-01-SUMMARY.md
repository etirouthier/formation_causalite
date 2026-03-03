---
phase: 02-scenario0-petits-nombres
plan: "01"
subsystem: data-visualization
tags: [pandas, seaborn, matplotlib, jupyter, groupby, histogram, scatter]

# Dependency graph
requires:
  - phase: 01-fondations
    provides: base_df (4800 lignes), generate_base_panel, compute_outcomes, PARAMS, rng, notebook structure
provides:
  - agg_sc0 DataFrame (200 lignes, une par magasin) avec colonnes taille, nb_visites_moy, panier_moyen_moy, panier_moyen_std
  - data/sc0_biais_petits_nombres.csv (export agrégé scénario 0)
  - figures/sc0_distribution.png (3 histogrammes sharex=True distribution panier_moyen par taille)
  - figures/sc0_scatter.png (scatter 200 points nb_visites_moy vs panier_moyen_std)
  - colors_sc0 dict (palette réutilisable pour plan 02-02 Figures 3 et 4)
affects:
  - 02-02 (Figure 3 top10 et Figure 4 loi des grands nombres réutilisent agg_sc0 et colors_sc0)

# Tech tracking
tech-stack:
  added: []
  patterns:
    - "groupby(['magasin_id','taille']) — inclure taille dans le groupby pour la conserver dans l'agrégat"
    - "colors_sc0 dict défini une fois dans fig1, réutilisé dans toutes les figures du scénario"
    - "subplots(3, 1, sharex=True) — axe X partagé pour comparaison directe des distributions"
    - "fig.savefig() avant plt.show() — pattern Phase 1 maintenu"

key-files:
  created:
    - data/sc0_biais_petits_nombres.csv
    - figures/sc0_distribution.png
    - figures/sc0_scatter.png
  modified:
    - formation_causalite.ipynb

key-decisions:
  - "colors_sc0 défini une seule fois dans code-sc0-fig1 et référencé dans code-sc0-fig2 — évite duplication et facilite réutilisation en 02-02"
  - "groupby(['magasin_id','taille']) avec les deux colonnes — 'taille' obligatoire pour survivre au reset_index()"

patterns-established:
  - "Agrégation scénario : groupby(['magasin_id','taille']).agg(...).reset_index() → 200 points un par magasin"
  - "Palette couleur scénario : colors_sc0 dict défini dans première cellule figure, réutilisé dans les suivantes"

requirements-completed: [SC0-01, SC0-02]

# Metrics
duration: 5min
completed: 2026-03-03
---

# Phase 2 Plan 01: Scénario 0 — Agrégation et Figures 1+2 Summary

**Section Scénario 0 insérée dans le notebook avec agg_sc0 (200 magasins, corrélation -0.758), CSV exporté, et deux figures pédagogiques (histogrammes distribution par taille et scatter variance vs affluence)**

## Performance

- **Duration:** 5 min
- **Started:** 2026-03-03T18:08:04Z
- **Completed:** 2026-03-03T18:09:00Z
- **Tasks:** 2
- **Files modified:** 1 notebook + 3 exports (CSV + 2 PNG)

## Accomplishments
- Agrégation agg_sc0 : 200 lignes (petit=79, moyen=86, grand=35) — résultats empiriques SEED=42 conformes aux specs
- Export data/sc0_biais_petits_nombres.csv (200 lignes, 6 colonnes)
- Figure 1 (sc0_distribution.png) : 3 histogrammes empilés verticalement avec sharex=True, une couleur par taille
- Figure 2 (sc0_scatter.png) : scatter 200 points, corrélation nb_visites_moy / panier_moyen_std = -0.758 visible
- colors_sc0 dict défini dans code-sc0-fig1, réutilisable par les figures du plan 02-02

## Résultats empiriques agg_sc0 (SEED=42)

| Taille | N magasins | panier_moyen_std moyen |
|--------|-----------|------------------------|
| petit  | 79        | 5.47                   |
| moyen  | 86        | 2.29                   |
| grand  | 35        | 1.24                   |

**Corrélation nb_visites_moy / panier_moyen_std : -0.758** (conforme aux specs : -0.758 attendu)

## Task Commits

Each task was committed atomically:

1. **Task 1: Insérer md-sc0-section et code-sc0-aggregation** - `51341bd` (feat)
2. **Task 2: Insérer code-sc0-fig1 et code-sc0-fig2** - `16c07ce` (feat)

**Plan metadata:** (docs commit — voir ci-dessous)

## Cellules ajoutées au notebook

| ID | Type | Position | Description |
|----|------|----------|-------------|
| md-sc0-section | markdown | après code-assertions (index 8) | Séparateur section Scénario 0 |
| code-sc0-aggregation | code | index 9 | groupby + export CSV |
| code-sc0-fig1 | code | index 10 | 3 histogrammes distribution sharex=True |
| code-sc0-fig2 | code | index 11 | Scatter variance vs affluence |

**Notebook final : 14 cellules** (10 existantes + 4 nouvelles)

## Files Created/Modified
- `formation_causalite.ipynb` - 4 nouvelles cellules insérées après code-assertions
- `data/sc0_biais_petits_nombres.csv` - 200 lignes, colonnes: magasin_id, taille, n_potentiel, nb_visites_moy, panier_moyen_moy, panier_moyen_std
- `figures/sc0_distribution.png` - 3 histogrammes empilés sharex=True (83 KB, dpi=150)
- `figures/sc0_scatter.png` - scatter 200 points colorés par taille (94 KB, dpi=150)

## Decisions Made
- colors_sc0 défini dans code-sc0-fig1 et réutilisé dans code-sc0-fig2 sans redéfinition — facilite la cohérence visuelle et évite drift de couleurs
- groupby(['magasin_id','taille']) avec les deux colonnes — 'taille' obligatoire pour que la colonne survive au reset_index()

## Deviations from Plan

None — plan executed exactly as written.

## Issues Encountered

None. Le notebook s'exécute sans erreur via `jupyter nbconvert --execute` (exit code 0). Les exports CSV et PNG sont créés correctement.

## Confirmation nbconvert

**Exit code 0.** Commande : `jupyter nbconvert --to notebook --execute formation_causalite.ipynb --output /tmp/test_02_01.ipynb`
Sortie : `[NbConvertApp] Writing 193681 bytes to /tmp/test_02_01.ipynb`

## User Setup Required

None — no external service configuration required.

## Next Phase Readiness
- agg_sc0 et colors_sc0 disponibles en mémoire pour plan 02-02 (Figures 3 et 4)
- Pattern groupby et palette couleur établis — 02-02 les réutilise directement
- CSV exporté pour inspection par le formateur

---
*Phase: 02-scenario0-petits-nombres*
*Completed: 2026-03-03*

## Self-Check: PASSED

- FOUND: formation_causalite.ipynb
- FOUND: data/sc0_biais_petits_nombres.csv
- FOUND: figures/sc0_distribution.png
- FOUND: figures/sc0_scatter.png
- FOUND: 02-01-SUMMARY.md
- FOUND: commit 51341bd (Task 1)
- FOUND: commit 16c07ce (Task 2)
