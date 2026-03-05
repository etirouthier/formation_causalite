# Project Retrospective

*A living document updated after each milestone. Lessons feed forward into future planning.*

## Milestone: v1.0 — Formation Causalité MVP

**Shipped:** 2026-03-05
**Phases:** 6 | **Plans:** 9 | **Timeline:** 3 jours (2026-03-02 → 2026-03-05)

### What Was Built
- Notebook Jupyter 42 cellules, ~993 lignes Python — DGP micro-fondé panel 4800 lignes (200 magasins × 24 mois)
- Scénario 0 : biais de petits nombres — 4 figures (distribution, scatter, top10, loi des grands nombres)
- Scénarios 1a/1b/1c : biais de sélection (qualité équipe, localisation, saison) — 9 figures DAG+coeff+bar
- Scénario 2 : surcontrôle médiateur — DAG diamond, OLS sans/avec médiateur
- Scénario 3 : collider V-structure — DAG V, biais introduit par contrôle sur collider
- Validation bout-en-bout : P_PUB_ALEATOIRE, cellule assertions finale, nbconvert exit 0

### What Worked
- **Cellule unique PARAMS** : ALL_CAPS + zéro magic number — très facile à modifier et à valider automatiquement
- **DGP micro-fondé** : la variance binomiale crée naturellement le biais de petits nombres sans code spécifique
- **Pattern DAG réutilisable** : le layout de nœuds fixe avec `pos dict` fonctionne pour tous les scénarios
- **GSD wave execution** : 6 phases avec agents autonomes — chaque phase livrait exactement ce que la suivante attendait

### What Was Inefficient
- **Calibration collider** (Phase 5) : 2–3 itérations pour trouver les bons coefficients COLLIDER_PUB_VENTES_COEFF (A=5, B=2) — un SNR cible explicite dans le plan aurait évité les allers-retours
- **DV inconsistant** (Phase 3) : la refactorisation vers log_rev_int a été faite pendant l'exécution plutôt que planifiée — coût réel d'une décision reportée
- **Coches SC3 dans REQUIREMENTS.md** : oubliées lors de l'exécution Phase 5, corrigées manuellement avant l'archivage milestone

### Patterns Established
- **DGP avec P_PUB_ALEATOIRE** : pour scénarios médiateur/collider, la sélection aléatoire isole proprement le biais de contrôle seul
- **Cellule validation finale nbconvert** : pattern robuste — asserte fichiers présents + cohérence effets vrais + exit 0
- **Figures en triplette (DAG + coeff + bar)** : convention pédagogique claire pour chaque scénario — DAG explique, coeff quantifie, bar compare

### Key Lessons
1. **Définir le SNR cible en amont** : pour les scénarios où le biais doit être "visible", spécifier l'amplitude minimale attendue dans le PLAN (ex. "biais ≥ 5pp") évite les iterations de calibration
2. **Valider la variable dépendante dès la Phase 1** : choisir log_rev_int vs ventes brutes avant de coder les scénarios — le changement en cours de route est coûteux
3. **Cocher les requirements au moment de l'exécution** : ne pas déléguer aux docs auto — si le plan dit "SC3-01 livré", cocher immédiatement dans REQUIREMENTS.md

### Cost Observations
- Model mix: ~100% sonnet (balanced profile)
- Sessions: ~6 sessions (une par phase + planning)
- Notable: les agents gsd-executor autonomes ont livré sans intervention humaine sur 5/6 phases — seule Phase 3 a nécessité une refactorisation DV non planifiée

---

## Cross-Milestone Trends

### Process Evolution

| Milestone | Timeline | Phases | Key Change |
|-----------|----------|--------|------------|
| v1.0 | 3 jours | 6 | Premier milestone — baseline établie |

### Cumulative Quality

| Milestone | nbconvert | Artefacts vérifiés | Magic numbers |
|-----------|-----------|-------------------|---------------|
| v1.0 | ✓ exit 0 | 20 PNG + 7 CSV | 0 hors PARAMS |

### Top Lessons (Verified Across Milestones)

1. *À confirmer sur v1.1+* — Définir SNR/amplitude cible dans le plan réduit les itérations de calibration
2. *À confirmer sur v1.1+* — Verrouiller la variable dépendante avant de coder les scénarios
