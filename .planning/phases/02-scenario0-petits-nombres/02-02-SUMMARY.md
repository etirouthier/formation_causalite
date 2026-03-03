---
phase: 02-scenario0-petits-nombres
plan: "02"
subsystem: data-visualization
tags: [pandas, seaborn, matplotlib, jupyter, kdeplot, bar-chart, loi-grands-nombres, simulation]

# Dependency graph
requires:
  - phase: 02-scenario0-petits-nombres
    plan: "01"
    provides: agg_sc0 (200 magasins), colors_sc0 dict, tailles_ordre, generate_base_panel, compute_outcomes, SEED, PARAMS
provides:
  - figures/sc0_top10.png (Figure 3 — bar chart top 10 magasins par panier moyen, barres colorées par taille)
  - figures/sc0_loi_grands_nombres.png (Figure 4 — subplot 2 rangs KDE réelle + KDE simulées N=10..100000)
  - code-sc0-fig3 cellule dans notebook (top10 bar chart, nlargest, Patch legend)
  - code-sc0-fig4 cellule dans notebook (rng_fig4 local, simulation DGP par N, warn_singular=False)
affects:
  - Plans suivants (02-03+) réutilisent le pattern rng local pour les simulations

# Tech tracking
tech-stack:
  added: []
  patterns:
    - "rng local isolé pour simulations : rng_fig4 = np.random.default_rng(SEED + 4) — évite de polluer l'état du rng global"
    - "warn_singular=False dans sns.kdeplot — obligatoire pour distributions quasi-delta (std ≈ 0.018)"
    - "matplotlib.patches.Patch pour légende colorée dans bar chart sans artistes de barres nommés"
    - "sharex=True dans subplot 2 rangs — aligne l'axe X pour comparaison directe KDE réelle vs simulées"

key-files:
  created:
    - figures/sc0_top10.png
    - figures/sc0_loi_grands_nombres.png
  modified:
    - formation_causalite.ipynb

key-decisions:
  - "rng_fig4 = np.random.default_rng(SEED + 4) utilisé dans code-sc0-fig4 — isole les simulations Figure 4 du rng global pour garantir la reproductibilité des scénarios 1-3"
  - "warn_singular=False dans sns.kdeplot pour N=100000 — std ≈ 0.018, sans ce flag la courbe peut disparaître silencieusement"

patterns-established:
  - "Simulation DGP isolée : rng local avec SEED + offset — pattern à suivre pour toutes simulations hors du flux principal"

requirements-completed: [SC0-03]

# Metrics
duration: 8min
completed: 2026-03-03
---

# Phase 2 Plan 02: Scénario 0 — Figures 3+4 (top10 bar chart et loi des grands nombres) Summary

**Deux nouvelles cellules de visualisation insérées (code-sc0-fig3 et code-sc0-fig4) produisant sc0_top10.png (10/10 petits dans le top 10) et sc0_loi_grands_nombres.png (2 panneaux KDE réelle + 5 KDE simulées N=10..100000), rng_fig4 local isolé du rng global**

## Performance

- **Duration:** 8 min
- **Started:** 2026-03-03T18:12:46Z
- **Completed:** 2026-03-03T18:41:00Z
- **Tasks:** 2 auto + 1 checkpoint human-verify (APPROVED)
- **Files modified:** 1 notebook + 2 PNG exports + 1 titre fix commit

## Accomplishments
- code-sc0-fig3 : bar chart des 10 magasins avec `panier_moyen_moy` le plus élevé, barres colorées par taille via `colors_sc0`
- code-sc0-fig4 : subplot 2 rangs (sharex=True) — KDE réelle `agg_sc0` (rang 1) + KDE overlay N=10,100,1000,10000,100000 via DGP (rang 2)
- `rng_fig4 = np.random.default_rng(SEED + 4)` local — rng global non consommé, reproductibilité des scénarios suivants garantie
- `warn_singular=False` dans tous les appels `sns.kdeplot` du rang 2 — N=100000 visible (std ≈ 0.018)
- `savefig` avant `plt.show()` dans les deux cellules — PNG non blancs

## Résultats empiriques (SEED=42)

| Cellule | Résultat clé |
|---------|-------------|
| code-sc0-fig3 | Top 10 : 10/10 petits magasins (100%) — message pédagogique sur-représentation |
| code-sc0-fig4 | 5 courbes KDE simulées, rétrécissement visible de N=10 (large) à N=100000 (quasi-delta) |

## Notebook final

**16 cellules** (14 existantes + 2 nouvelles)

| ID | Position | Description |
|----|----------|-------------|
| md-sc0-section | index 8 | Séparateur section Scénario 0 (02-01) |
| code-sc0-aggregation | index 9 | groupby + export CSV (02-01) |
| code-sc0-fig1 | index 10 | 3 histogrammes distribution sharex=True (02-01) |
| code-sc0-fig2 | index 11 | Scatter variance vs affluence (02-01) |
| code-sc0-fig3 | index 12 | Top 10 bar chart (02-02) |
| code-sc0-fig4 | index 13 | Loi des grands nombres (02-02) |

## Task Commits

Each task was committed atomically:

1. **Task 1: Insérer Figure 3 (top 10 bar chart) et Figure 4 (loi des grands nombres)** - `f51419c` (feat)
2. **Task 2: Exécuter le notebook et vérifier les 4 exports** - `f0bcc3f` (feat)
3. **Task 3: Checkpoint humain — Validation visuelle des 4 figures** - APPROVED
   - Correctif post-checkpoint: `c90fc36` (fix) — titres figures sc0 rendus factuels (suppressions des commentaires interprétatifs), notebook ré-exécuté

**Plan metadata:** (docs commit — voir ci-dessous)

## Files Created/Modified
- `formation_causalite.ipynb` — 2 nouvelles cellules (code-sc0-fig3, code-sc0-fig4) insérées après code-sc0-fig2
- `figures/sc0_top10.png` — 50 KB, dpi=150, bar chart top 10, barres rouges (petits)
- `figures/sc0_loi_grands_nombres.png` — 106 KB, dpi=150, 2 panneaux KDE

## Confirmation nbconvert

**Exit code 0.** Commande : `jupyter nbconvert --to notebook --execute formation_causalite.ipynb --output /tmp/test_phase2_complete.ipynb --ExecutePreprocessor.timeout=300`
Sortie : `[NbConvertApp] Writing 333457 bytes to /tmp/test_phase2_complete.ipynb`

## Checkpoint Humain

**Statut : APPROUVE** — Le formateur a validé visuellement les 4 figures du scénario 0 (2026-03-03).

Suite à la validation, un correctif a été appliqué :
- Les titres des figures contenaient des commentaires interprétatifs — supprimés pour rendre les titres purement factuels
- Commit correctif : `c90fc36` — notebook ré-exécuté avec succès après modification

Points de contrôle visuels validés :
1. `sc0_distribution.png` : 3 panneaux empilés, axe X partagé, distribution "petit" plus large que "grand"
2. `sc0_scatter.png` : nuage avec tendance négative, points rouges (petits) en haut à gauche
3. `sc0_top10.png` : barres majoritairement rouges (petits), titre factuel, légende présente
4. `sc0_loi_grands_nombres.png` : rang 1 KDE grise réelle, rang 2 5 courbes dont N=100000 la plus étroite

## Decisions Made
- `rng_fig4 = np.random.default_rng(SEED + 4)` local dans code-sc0-fig4 — conforme au contrat anti-pattern du plan (pas de pollution du rng global)
- `warn_singular=False` dans `sns.kdeplot` — obligatoire pour N=100000 (std ≈ 0.018, sinon courbe absente silencieusement)

## Deviations from Plan

### Faux positif dans la vérification automatisée Task 1

**Note non bloquante — vérification sémantique OK**
- **Found during:** Task 1 (vérification automatisée)
- **Issue:** Le regex `\brng\b(?!_fig4)` du script de vérification du plan détecte le mot "rng" à la fin de `default_rng(...)` comme un faux positif pour un usage du rng global
- **Fix:** Vérification sémantique manuelle — le code ne contient aucune référence à la variable `rng` globale ; tous les usages sont `rng_fig4` ou `default_rng()`
- **Impact:** Zéro — le code est correct et conforme au plan

Hors ce faux positif : **None — plan executed exactly as written.**

## Issues Encountered

Faux positif du regex de vérification (voir Deviations). Résolu par inspection manuelle — la vérification réelle (nbconvert exit 0 + présence des PNG + top10 = 10/10 petits) est passée sans problème.

## User Setup Required

None — no external service configuration required.

## Next Phase Readiness
- Scénario 0 complet — 6 cellules sc0 insérées, 4 PNG et 1 CSV exportés, nbconvert exit 0
- Pattern `rng_fig4` local établi — réutilisable pour les simulations des scénarios suivants (SEED + offset unique par figure)
- Validation visuelle du formateur APPROUVEE (2026-03-03) — passage au scénario suivant possible

---
*Phase: 02-scenario0-petits-nombres*
*Completed: 2026-03-03*

## Self-Check: PASSED

- FOUND: figures/sc0_top10.png (41 KB)
- FOUND: figures/sc0_loi_grands_nombres.png (100 KB)
- FOUND: figures/sc0_distribution.png (81 KB)
- FOUND: figures/sc0_scatter.png (84 KB)
- FOUND: data/sc0_biais_petits_nombres.csv (13 KB, 200 magasins)
- FOUND: formation_causalite.ipynb (16 cellules, code-sc0-fig3 et code-sc0-fig4 présentes)
- FOUND: 02-02-SUMMARY.md
- FOUND: commit f51419c (Task 1 — insertion cellules)
- FOUND: commit f0bcc3f (Task 2 — exports PNG)
- FOUND: commit c90fc36 (fix post-checkpoint — titres factuels, notebook ré-exécuté)
- Checkpoint human-verify: APPROVED by formateur 2026-03-03
