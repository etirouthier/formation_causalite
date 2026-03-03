---
phase: 01-fondations
plan: "02"
subsystem: dgp
tags: [jupyter, numpy, pandas, networkx, matplotlib, dgp, assertions, dag]

# Dependency graph
requires:
  - "formation_causalite.ipynb squelette (01-01) : cellules Paramètres + Imports + rng"
provides:
  - "generate_base_panel(params, rng) : cross join vectorisé magasins × mois, mapping saison cyclique"
  - "compute_outcomes(df, params, rng) : np.clip [0.01, 0.99], CLT ventes, panier_moyen"
  - "Cellule exécution base_df : 4800 lignes, pub retiré, export data/base_panel.csv"
  - "Cellule Assertions INFRA-03 : 5 checks automatiques (max_p, p_visite, nb_visites, ratio, pub absent)"
  - "Cellule DAG pattern DGP-06 : nx.DiGraph pos dict fixe, figures/dag_pattern_demo.png"
affects: [01-03, 01-04, 01-05, 01-06]

# Tech tracking
tech-stack:
  added: []
  patterns:
    - "generate_base_panel retourne caractéristiques uniquement — pub assigné par chaque scénario"
    - "compute_outcomes prend df avec pub en entrée — modifie une copie df.copy()"
    - "np.clip(p_visite, 0.01, 0.99) OBLIGATOIRE avant rng.binomial() — pattern répété dans tous les scénarios"
    - "DAG avec pos dict fixe : pos = {'noeud': (x, y)} — jamais de layout automatique"
    - "mapping saison cyclique : mois_saison = ((mois - 1) % 12) + 1 — supporte T_MOIS > 12"
    - "fig.savefig(...) avant plt.show() — ordre obligatoire pour PNG non blanc"

key-files:
  created:
    - data/base_panel.csv
    - figures/dag_pattern_demo.png
  modified:
    - formation_causalite.ipynb

key-decisions:
  - "P_BASE_VISITE fixé à 0.25 (non 0.05) : p trop faible causait nb_visites=0 pour petits magasins avec N_PETIT=30"
  - "Mapping effet_saison cyclique via modulo 12 — T_MOIS=24 nécessite répétition du cycle annuel"
  - "nbformat_minor 4 -> 5 pour supporter les cell ids sans erreur de validation"

patterns-established:
  - "DGP pattern : generate_base_panel → base_df.copy() → assign pub → compute_outcomes → analyse"
  - "Assertions pattern : assertions paramétriques AVANT assertions sur données, print diagnostique à la fin"
  - "DAG pattern : G = nx.DiGraph(), pos dict fixe, node_color list par noeud, savefig avant show"

requirements-completed: [INFRA-03, DGP-01, DGP-02, DGP-03, DGP-04, DGP-05, DGP-06]

# Metrics
duration: 7min
completed: 2026-03-03
---

# Phase 01 Plan 02: Fonctions DGP Summary

**Fonctions generate_base_panel et compute_outcomes ajoutées au notebook — panel 4800 lignes reproductible, assertions INFRA-03 validées (max_p=0.420, ratio variance=4.4x), DAG pattern avec layout fixe exporté en PNG**

## Performance

- **Duration:** ~7 min
- **Started:** 2026-03-03T09:14:56Z
- **Completed:** 2026-03-03T09:22:39Z
- **Tasks:** 2 (+ 3 auto-fixes, + checkpoint reached)
- **Files modified:** 1 (formation_causalite.ipynb)
- **Files created:** 2 (data/base_panel.csv, figures/dag_pattern_demo.png)

## Accomplishments

- `generate_base_panel(params, rng)` : cross join vectorisé magasins × mois via `merge(how='cross')`, mapping saison cyclique pour supporter T_MOIS > 12, n_potentiel mappé depuis taille
- `compute_outcomes(df, params, rng)` : p_visite clippée [0.01, 0.99] avant `rng.binomial()`, approximation CLT pour ventes, `panier_moyen = np.where(nb > 0, ...)` pour gérer les zéros
- Cellule exécution : `base_df` généré sans colonne `pub` (ajoutée temporairement, retirée après calcul), 4800 lignes × 11 colonnes, export `data/base_panel.csv`
- Cellule Assertions : 5 checks INFRA-03 passent sans exception — max_p=0.420 < 0.99, p_visite ∈ [0.01, 0.99], nb_visites.min() > 0, ratio_variance=4.4x > 2.0, pub absent
- Cellule DAG pattern : `nx.DiGraph` avec 3 noeuds, `pos` dict fixe, export `figures/dag_pattern_demo.png` (859×411px, RGBA)
- Notebook exécutable de bout en bout via `nbconvert --execute` : exit code 0

## Task Commits

Each task was committed atomically:

1. **Task 1: Ajouter generate_base_panel et compute_outcomes** - `26188ad` (feat)
2. **Task 2: Ajouter cellule Assertions et cellule DAG pattern** - `6d7d17b` (feat)
3. **Auto-fixes calibration et mapping** - `8830a83` (fix)

**Plan metadata:** `(voir commit final docs)` (docs: complete plan)

## Files Created/Modified

- `formation_causalite.ipynb` — 10 cellules (3 initiales + 7 nouvelles : 3 markdown + 4 code)
- `data/base_panel.csv` — 4800 lignes, 11 colonnes (magasin_id, taille, urbain, qualite_equipe, n_potentiel, mois, effet_saison_val, p_visite, nb_visites, ventes, panier_moyen)
- `figures/dag_pattern_demo.png` — 859×411px, RGBA, DAG 3 noeuds avec layout fixe

## Valeurs diagnostiques des Assertions

```
Assertions OK — max p_visite cumulee: 0.420, variance ratio: 4.4x
```

- `max_p = 0.25 + 0.03 + 0.02 + 0.02 + 0.10 = 0.420` (< 0.99 ✓)
- `variance ratio petit/grand = 4.4x` (> 2.0 ✓)
- `nb_visites.min() > 0` ✓ (avec P_BASE_VISITE=0.25)
- `p_visite ∈ [0.01, 0.99]` ✓ (np.clip obligatoire)
- `'pub' not in base_df.columns` ✓

## Colonnes de base_df

```
['magasin_id', 'taille', 'urbain', 'qualite_equipe', 'n_potentiel', 'mois', 'effet_saison_val', 'p_visite', 'nb_visites', 'ventes', 'panier_moyen']
```

(11 colonnes — `pub` absent comme requis)

## Decisions Made

1. **P_BASE_VISITE = 0.25** (non 0.05 comme dans le notebook initial) : avec N_PETIT=30 et p_base=0.05, E[nb_visites] = 1.5 visites/mois pour les petits magasins, et P(nb=0) ≈ 36%. La valeur 0.25 garantit E[nb_visites] = 7.5 pour N_PETIT=30, éliminant les zéros (vérifié avec SEED=42).
2. **Mapping saison cyclique** : `mois_saison = ((mois - 1) % 12) + 1` — T_MOIS=24 représente 2 ans; EFFET_SAISON n'a que 12 clés (mois 1-12). Sans ce mapping, les mois 13-24 produisaient NaN, propageant à p_visite et causant l'erreur `p < 0, p > 1 or p contains NaNs` de numpy.
3. **nbformat_minor = 5** : les cellules créées avec un champ `id` sont valides en nbformat ≥ 4.5. Upgrade de 4.4 → 4.5 pour éviter les avertissements de validation futurs.

## Deviations from Plan

### Auto-fixed Issues

**1. [Rule 1 - Bug] Mapping effet_saison causait NaN pour mois 13-24**
- **Found during:** Task 1 (lors du premier nbconvert --execute)
- **Issue:** `base['effet_saison_val'] = base['mois'].map(params['effet_saison'])` — EFFET_SAISON a des clés 1-12, mais T_MOIS=24 génère des mois 1-24. Les mois 13-24 n'avaient pas de mapping → NaN → propagation à p_visite → ValueError dans rng.binomial()
- **Fix:** `mois_saison = ((base['mois'] - 1) % 12) + 1` suivi de `base['effet_saison_val'] = mois_saison.map(params['effet_saison'])`
- **Files modified:** formation_causalite.ipynb (cellule generate_base_panel)
- **Commit:** 8830a83

**2. [Rule 1 - Bug] P_BASE_VISITE=0.05 trop faible — assertion nb_visites.min() > 0 échouait**
- **Found during:** Task 1/Task 2 (lors des tests d'assertions)
- **Issue:** Avec N_PETIT=30 et p_base=0.05, E[nb_visites] = 1.5 pour les petits magasins. P(nb=0) ≈ 36% → l'assertion `base_df['nb_visites'].min() > 0` échouait systématiquement avec SEED=42 (174 zéros observés).
- **Fix:** `P_BASE_VISITE = 0.25` — E[nb_visites] = 7.5 pour petits magasins, probabilité de zéro < 0.1%. Vérifié : 0 zéros avec SEED=42. max_p = 0.42 < 0.99 (assertion 1 toujours satisfaite).
- **Files modified:** formation_causalite.ipynb (cellule Paramètres, ligne P_BASE_VISITE)
- **Commit:** 8830a83

**3. [Rule 1 - Bug] Commentaire `spring_layout` dans cellule code déclenchait faux positif**
- **Found during:** Task 2 (vérification automatique)
- **Issue:** Le commentaire `# FIXE — jamais spring_layout` contenait la chaîne `spring_layout` que le script de vérification interdisait dans les cellules code.
- **Fix:** Remplacement du commentaire par `# layout fixe via pos dict uniquement`
- **Files modified:** formation_causalite.ipynb (cellule DAG pattern, ligne de commentaire)
- **Commit:** 6d7d17b (inclus dans Task 2)

**4. [Rule 3 - Blocking] nbformat 4.4 n'accepte pas les cell ids**
- **Found during:** Task 1 (premier nbconvert --execute)
- **Issue:** `Additional properties are not allowed ('id' was unexpected)` — nbformat 4.4 ne supporte pas le champ `id` dans les cellules markdown.
- **Fix:** `nb['nbformat_minor'] = 5` — nbformat 4.5 supporte les cell ids.
- **Files modified:** formation_causalite.ipynb (métadonnées nbformat)
- **Commit:** 8830a83

---

**Total deviations:** 4 auto-fixes (3 Rule 1 bugs, 1 Rule 3 blocking)
**Impact:** Corrections critiques pour l'exécution du notebook. Aucun impact sur les interfaces ou les conventions établies.

## Checkpoint Status

**Task 3 (checkpoint:human-verify)** — Reached after Tasks 1 and 2 complete.

Pre-verification automation executed:
- `jupyter nbconvert --execute formation_causalite.ipynb` → **Exit code 0**
- `data/base_panel.csv` : 4800 lignes ✓
- `figures/dag_pattern_demo.png` : PNG 859×411px RGBA ✓
- Assertions affichent "Assertions OK — max p_visite cumulee: 0.420, variance ratio: 4.4x" ✓

## Issues Encountered

- Packages Python déjà disponibles (installés lors de plan 01-01).
- Le calibrage initial des paramètres (P_BASE_VISITE=0.05) était inadapté à N_PETIT=30 — corrigé automatiquement.

## User Setup Required

None — vérification automatique complète exécutée.

## Next Phase Readiness

- Toutes les fonctions DGP Phase 1 sont implémentées et testées
- base_df (4800 lignes, 11 colonnes) disponible pour les scénarios Phase 2
- Pattern DAG établi et documenté avec figures/dag_pattern_demo.png
- Prêt pour plan 01-03 (scénarios Phases 2-5)

---
*Phase: 01-fondations*
*Completed: 2026-03-03*
