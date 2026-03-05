# Roadmap: Générateur de données — Formation Causalité

## Milestones

- ✅ **v1.0 Formation Causalité MVP** — Phases 1–6 (shipped 2026-03-05)
- [ ] **v1.1 Formation Causalité** — Phases 7–8 (in progress)

## Phases

<details>
<summary>✅ v1.0 Formation Causalité MVP (Phases 1–6) — SHIPPED 2026-03-05</summary>

- [x] Phase 1: Fondations (2/2 plans) — completed 2026-03-03
- [x] Phase 2: Scénario 0 — Biais de petits nombres (2/2 plans) — completed 2026-03-03
- [x] Phase 3: Scénarios 1a/1b/1c — Biais de sélection (2/2 plans) — completed 2026-03-04
- [x] Phase 4: Scénario 2 — Surcontrôle sur un médiateur (1/1 plan) — completed 2026-03-04
- [x] Phase 5: Scénario 3 — Surcontrôle sur un collider (1/1 plan) — completed 2026-03-04
- [x] Phase 6: Validation bout-en-bout (1/1 plan) — completed 2026-03-05

Full archive: `.planning/milestones/v1.0-ROADMAP.md`

</details>

### v1.1 Formation Causalité

- [x] **Phase 7: Scénario Randomisation** — Nouveau scénario illustrant la balance des groupes en grand vs petit échantillon (completed 2026-03-05)
- [ ] **Phase 8: Ventes par m2 et DAG uniforme** — Variable dérivée ventes_par_m2 avec visualisation + DAG en noir sur tous les scénarios

## Phase Details

### Phase 7: Scénario Randomisation
**Goal**: Le formateur peut montrer comment la randomisation équilibre les caractéristiques en grand échantillon, et produit des déséquilibres apparents en petit échantillon par le seul hasard
**Depends on**: Phase 6 (notebook v1.0 validé)
**Requirements**: RAND-01, RAND-02, RAND-03, RAND-04
**Success Criteria** (what must be TRUE):
  1. Le formateur peut voir un tableau de balance (% urbain, taille, qualité équipe) entre groupe traité et groupe témoin après tirage aléatoire
  2. Dans le cas grand échantillon, les distributions des caractéristiques sont visuellement équilibrées entre les deux groupes
  3. Dans le cas petit échantillon, des déséquilibres apparents sont visibles — sans confondant, par hasard seul
  4. Les données du scénario sont exportées en CSV dans `data/` et les figures en PNG dans `figures/`
**Plans**: 1 plan

Plans:
- [x] 07-01-PLAN.md — Scenario 4 Randomisation : donnees + figures balance grand vs petit echantillon (completed 2026-03-05)

### Phase 8: Ventes par m2 et DAG uniforme
**Goal**: Le notebook intègre la variable dérivée ventes_par_m2 avec au moins une figure illustrative, et tous les DAG utilisent exclusivement le noir
**Depends on**: Phase 7
**Requirements**: VM2-01, VM2-02, DAG-01
**Success Criteria** (what must be TRUE):
  1. La variable `ventes_par_m2 = ventes / N_potentiel` est calculée dans le notebook et présente dans le dataset exporté
  2. Au moins une figure représente `ventes_par_m2` par taille, localisation, ou traitement pub
  3. Tous les DAG du notebook (scénarios 1a, 1b, 1c, 2, 3) ont nœuds, arêtes et labels en noir — aucune couleur
  4. `Restart & Run All` produit toutes les figures et CSV sans erreur après ces modifications
**Plans**: 2 plans

Plans:
- [ ] 08-01-PLAN.md — ventes_par_m2 : calcul + figure par taille (sc0)
- [ ] 08-02-PLAN.md — DAG uniforme : tous les 6 DAG en noir

## Progress

| Phase | Milestone | Plans Complete | Status | Completed |
|-------|-----------|----------------|--------|-----------|
| 1. Fondations | v1.0 | 2/2 | Complete | 2026-03-03 |
| 2. Scénario 0 — Biais de petits nombres | v1.0 | 2/2 | Complete | 2026-03-03 |
| 3. Scénarios 1a/1b/1c — Biais de sélection | v1.0 | 2/2 | Complete | 2026-03-04 |
| 4. Scénario 2 — Surcontrôle sur un médiateur | v1.0 | 1/1 | Complete | 2026-03-04 |
| 5. Scénario 3 — Surcontrôle sur un collider | v1.0 | 1/1 | Complete | 2026-03-04 |
| 6. Validation bout-en-bout | v1.0 | 1/1 | Complete | 2026-03-05 |
| 7. Scénario Randomisation | v1.1 | 1/1 | Complete | 2026-03-05 |
| 8. Ventes par m2 et DAG uniforme | v1.1 | 0/2 | Not started | - |
