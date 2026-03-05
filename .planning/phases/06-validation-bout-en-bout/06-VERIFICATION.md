---
phase: 06-validation-bout-en-bout
verified: 2026-03-05T11:00:00Z
status: passed
score: 4/4 must-haves verified
re_verification: false
---

# Phase 6: Validation Bout-en-Bout — Verification Report

**Phase Goal:** Le notebook est propre, complet, et prêt à l'emploi — le formateur peut le distribuer ou l'exécuter sans modification
**Verified:** 2026-03-05T11:00:00Z
**Status:** passed
**Re-verification:** No — initial verification

---

## Goal Achievement

### Observable Truths

| # | Truth | Status | Evidence |
|---|-------|--------|----------|
| 1 | Le notebook s'exécute de bout en bout (Restart & Run All) sans erreur — nbconvert exit 0 | VERIFIED | `/tmp/formation_causalite_validated.ipynb` — 42 cellules exécutées, 0 erreur, dernière cellule imprime "Validation notebook : OK" |
| 2 | Aucun magic number de simulation hors cellule Paramètres — seul P_PUB_ALEATOIRE remplace 0.5 dans sc2 et sc3 | VERIFIED | `P_PUB_ALEATOIRE = 0.5` dans cellule 1 (PARAMS). Aucune occurrence de `binomial(1, 0.5` dans les cellules sc2 (cell 32) et sc3 (cell 37). Zéro anti-pattern binomial 0.5 détecté. |
| 3 | Les 20 PNG et 7 CSV sont confirmés présents par une cellule de validation en fin de notebook | VERIFIED | Cell 41 (dernière) contient `PNG_ATTENDUS` (20 fichiers), `CSV_ATTENDUS` (7 fichiers), assertions `png_manquants`/`csv_manquants`. Artefacts physiques confirmés : 20 PNG dans `figures/`, 7 CSV dans `data/`. Output exécuté : "20 PNG présents dans figures / 7 CSV présents dans data/" |
| 4 | La cohérence de EFFET_PUB_VISITES et EFFET_PUB_PANIER entre scénarios est assertée explicitement | VERIFIED | Cell 41 contient `assert PARAMS['effet_pub_visites'] == EFFET_PUB_VISITES` et `assert PARAMS['effet_pub_panier'] == EFFET_PUB_PANIER`. Output exécuté : "Effet pub visites : 10% (cohérent) / Effet pub panier : 10% (cohérent)" |

**Score:** 4/4 truths verified

---

### Required Artifacts

| Artifact | Expected | Status | Details |
|----------|----------|--------|---------|
| `formation_causalite.ipynb` | Notebook 42 cellules avec P_PUB_ALEATOIRE + cellule validation | VERIFIED | 42 cellules confirmées. Commits `f9342ac` et `f1d6615` documentent les modifications. |

**Artifact level checks:**

- Level 1 (Exists): `formation_causalite.ipynb` present — YES
- Level 2 (Substantive): 42 cellules de code et markdown, P_PUB_ALEATOIRE dans PARAMS (cell 1), validation cell en position 41 — YES
- Level 3 (Wired): P_PUB_ALEATOIRE fluye depuis cell 1 vers cells 32 (sc2) et 37 (sc3) ; cell 41 référence PARAMS, EFFET_PUB_VISITES, EFFET_PUB_PANIER définis dans les cellules précédentes — YES

---

### Key Link Verification

| From | To | Via | Status | Details |
|------|----|-----|--------|---------|
| Cell 1 — PARAMS (P_PUB_ALEATOIRE) | Cell 32 (sc2) et Cell 37 (sc3) | Variable `P_PUB_ALEATOIRE` | WIRED | `rng_sc2.binomial(1, P_PUB_ALEATOIRE, ...)` en cell 32 ; `rng_sc3.binomial(1, P_PUB_ALEATOIRE, ...)` en cell 37. Aucun littéral 0.5 résiduel. |
| Cell 41 — validation finale | `figures/` et `data/` | `Path(f).exists()` assertions via `png_manquants`/`csv_manquants` | WIRED | Les listes `PNG_ATTENDUS` et `CSV_ATTENDUS` sont assertées via `Path(f).exists()`. Exécution confirme 20+7 fichiers présents. |

---

### Requirements Coverage

| Requirement | Source Plan | Description | Status | Evidence |
|-------------|-------------|-------------|--------|----------|
| INFRA-01 | 06-01-PLAN.md | Le formateur peut modifier tous les paramètres depuis une cellule unique — aucun magic number ailleurs | SATISFIED | `P_PUB_ALEATOIRE = 0.5` dans cellule PARAMS. Zéro occurrence de `binomial(1, 0.5` dans sc2/sc3. Revue complète des cellules binomial : aucun literal 0.5 résiduel. |
| INFRA-02 | 06-01-PLAN.md | Résultats identiques à chaque `Restart & Run All` via `numpy.random.default_rng(SEED)` | SATISFIED | `SEED = 42` dans PARAMS, `default_rng(SEED)` utilisé. Notebook exécuté via nbconvert exit 0 avec résultats reproductibles. |
| INFRA-03 | 06-01-PLAN.md | Cellule d'assertions validant cohérence des paramètres et effets vrais entre scénarios | SATISFIED | Cell 41 asserte `PARAMS['effet_pub_visites'] == EFFET_PUB_VISITES` et `PARAMS['effet_pub_panier'] == EFFET_PUB_PANIER`. Output exécuté confirme 10% pour les deux. |
| INFRA-04 | 06-01-PLAN.md | Toutes les figures exportées en PNG vers `figures/` et datasets en CSV vers `data/` | SATISFIED | 20 PNG dans `figures/`, 7 CSV dans `data/` confirmés physiquement et par la cellule de validation exécutée. `savefig` et `to_csv` présents dans le notebook. |

**Note sur la traçabilité REQUIREMENTS.md :** La table de traçabilité dans REQUIREMENTS.md assigne INFRA-01 à INFRA-04 à la Phase 1. ROADMAP.md les réassigne explicitement à la Phase 6 comme "cross-cutting — validation finale de toutes les phases". Cette double attribution est cohérente : les exigences ont été implémentées en Phase 1, et leur satisfaction finale est validée en Phase 6. Aucun ORPHANED requirement détecté pour la Phase 6.

**Success Criteria ROADMAP cross-check :**

| SC | Description | Status |
|----|-------------|--------|
| SC1 | `Restart & Run All` sans erreur ni warning bloquant | VERIFIED — nbconvert exit 0, 0 erreur dans 42 cellules |
| SC2 | Tous les PNG dans `figures/` et CSV dans `data/` | VERIFIED — 20 PNG + 7 CSV confirmés physiquement et via cellule validation |
| SC3 | Aucun magic number hors cellule Paramètres (revue manuelle) | VERIFIED — Zéro `binomial(1, 0.5` résiduel, P_PUB_ALEATOIRE est le seul paramètre qui remplaçait un 0.5 |
| SC4 | Effet vrai identique entre scénarios (`EFFET_PUB_VISITES` et `EFFET_PUB_PANIER`) asserté | VERIFIED — Assertions explicites en cell 41, output exécuté 10%/10% |

---

### Anti-Patterns Found

| File | Line | Pattern | Severity | Impact |
|------|------|---------|----------|--------|
| — | — | — | — | Aucun anti-pattern détecté (TODO/FIXME/PLACEHOLDER/stub) |

---

### Human Verification Required

**1. Lisibilité pédagogique du notebook**

**Test:** Ouvrir `formation_causalite.ipynb` dans Jupyter. Parcourir les cellules markdown pour vérifier que les explications des scénarios sont claires pour un public praticien data/analytics.
**Expected:** Chaque scénario a une introduction textuelle qui explique le biais illustré avant la génération de données.
**Why human:** La qualité rédactionnelle et la pertinence pédagogique ne sont pas vérifiables programmatiquement.

**2. Qualité visuelle des figures exportées**

**Test:** Ouvrir les 20 PNG dans `figures/` et vérifier que les graphiques sont lisibles, correctement légendés et adaptés à une présentation de formation.
**Expected:** Légendes lisibles, titres présents, axes correctement libellés, DAGs clairs.
**Why human:** La qualité visuelle ne peut pas être assertée par code.

---

### Gaps Summary

Aucun gap détecté. Tous les must-haves sont vérifiés.

---

## Summary

La Phase 6 atteint son objectif : le notebook `formation_causalite.ipynb` est prêt à distribuer. Les quatre truths sont vérifiés :

1. Le notebook s'exécute sans erreur (`nbconvert exit 0`, 42 cellules, 0 erreur) et la cellule de validation imprime "Validation notebook : OK".
2. Le seul magic number résiduel `0.5` (probabilité de pub dans sc2 et sc3) est éliminé par la constante nommée `P_PUB_ALEATOIRE` dans la cellule PARAMS.
3. Les 20 PNG et 7 CSV sont présents physiquement et assertés par la cellule de validation.
4. La cohérence des effets vrais est assertée explicitement (10%/10% confirmé à l'exécution).

Les exigences INFRA-01 à INFRA-04 sont toutes satisfaites dans leur périmètre de validation finale. Deux commits documentés (`f9342ac`, `f1d6615`) tracent les modifications. Aucun anti-pattern détecté.

---

_Verified: 2026-03-05T11:00:00Z_
_Verifier: Claude (gsd-verifier)_
