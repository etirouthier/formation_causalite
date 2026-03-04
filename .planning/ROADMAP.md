# Roadmap: Générateur de données — Formation Causalité

## Overview

Un notebook Jupyter Python standalone qui génère des données simulées illustrant quatre biais causaux classiques, tous construits sur le même modèle de données. Le projet part de zéro vers un outil complet que le formateur peut exécuter en `Restart & Run All` sans erreur. L'ordre des phases est dicté par les dépendances techniques : le générateur de base doit précéder tous les scénarios, et le scénario le plus simple (petits nombres) valide la calibration du DGP avant d'aborder les biais plus délicats.

## Phases

**Phase Numbering:**
- Integer phases (1, 2, 3): Planned milestone work
- Decimal phases (2.1, 2.2): Urgent insertions (marked with INSERTED)

Decimal phases appear between their surrounding integers in numeric order.

- [ ] **Phase 1: Fondations** - Notebook squelette avec cellule Paramètres, seed, assertions, dossiers d'export, et `generate_base_panel()` validé
- [ ] **Phase 2: Scénario 0 — Biais de petits nombres** - Figures de distribution du `panier_moyen` par taille de magasin + exports PNG/CSV
- [x] **Phase 3: Scénarios 1a/1b/1c — Biais de sélection** - DAGs networkx, comparaisons naïf vs ajusté avec IC 95%, exports
- [x] **Phase 4: Scénario 2 — Surcontrôle sur un médiateur** - Visualisation du changement de coefficient OLS lors de l'ajout du médiateur
- [ ] **Phase 5: Scénario 3 — Surcontrôle sur un collider** - Variable `posts_reseaux` comme collider, comparaison OLS avec vs sans collider
- [ ] **Phase 6: Validation bout-en-bout** - Notebook propre, `Restart & Run All` sans erreur, zero magic number hors cellule Paramètres

## Phase Details

### Phase 1: Fondations
**Goal**: Le formateur dispose d'un notebook fonctionnel avec un générateur de panel partagé, reproductible, et validé par des assertions automatiques
**Depends on**: Nothing (first phase)
**Requirements**: INFRA-01, INFRA-02, INFRA-03, INFRA-04, DGP-01, DGP-02, DGP-03, DGP-04, DGP-05, DGP-06
**Success Criteria** (what must be TRUE):
  1. `Restart & Run All` s'exécute sans erreur avec les paramètres par défaut
  2. Deux exécutions consécutives produisent exactement le même DataFrame (seed reproductible)
  3. La cellule d'assertions passe sans exception : `p_visite ∈ [0.01, 0.99]` pour toutes les lignes, overlap suffisant dans les scénarios de sélection
  4. Les dossiers `figures/` et `data/` sont créés automatiquement au démarrage
  5. Tous les paramètres numériques sont dans la cellule Paramètres sous forme de constantes ALL_CAPS — aucun magic number dans les cellules de génération
**Plans**: 2 plans

Plans:
- [x] 01-01-PLAN.md — Notebook skeleton : cellule Paramètres (ALL_CAPS) + cellule Imports (rng, mkdir)
- [x] 01-02-PLAN.md — DGP + validation : generate_base_panel, compute_outcomes, assertions, DAG pattern

### Phase 2: Scénario 0 — Biais de petits nombres
**Goal**: Le formateur peut illustrer visuellement que les petits magasins dominent les extrêmes de distribution du panier moyen en raison de la variance binomiale
**Depends on**: Phase 1
**Requirements**: SC0-01, SC0-02, SC0-03
**Success Criteria** (what must be TRUE):
  1. La figure de distribution montre des distributions clairement différentes par taille (petit, moyen, grand), exportée en PNG dans `figures/`
  2. Le scatter plot montre une corrélation négative visible entre `nb_visites` et la variance du `panier_moyen`
  3. Le bar chart des top 10 magasins révèle la sur-représentation des petits magasins (idéalement ≥ 50% du top 10)
  4. Le dataset du scénario est exporté en CSV dans `data/`
**Plans**: 2 plans (02-01 complete, 02-02 complete — checkpoint human-verify APPROVED)

Plans:
- [x] 02-01-PLAN.md — Agrégation agg_sc0 + export CSV + Figure 1 (distribution) + Figure 2 (scatter variance)
- [x] 02-02-PLAN.md — Figure 3 (top 10 magasins) + Figure 4 (mécanisme loi des grands nombres)

### Phase 3: Scénarios 1a/1b/1c — Biais de sélection
**Goal**: Le formateur peut montrer que comparer naïvement les groupes traités et non traités surestime l'effet de la pub quand un confondant détermine l'assignation au traitement
**Depends on**: Phase 2
**Requirements**: SC1-01, SC1-02, SC1-03
**Success Criteria** (what must be TRUE):
  1. Chaque sous-scénario (1a, 1b, 1c) affiche un DAG networkx avec layout fixe et déterministe
  2. Le coefficient naïf est systématiquement plus élevé que la valeur vraie ; l'estimateur ajusté converge vers la valeur vraie (dans l'IC 95%)
  3. Les trois comparaisons (naïf vs ajusté vs vrai) sont affichées sur un graphique lisible par taille pour slides
  4. Les trois datasets (un par sous-scénario) sont exportés en CSV dans `data/`
**Plans**: 2 plans

Plans:
- [x] 03-01-PLAN.md — Scénarios 1a (qualite_equipe) et 1b (urbain) : données + DAG + coefficient plot + bar chart
- [x] 03-02-PLAN.md — Scénario 1c (saison) : données + DAG + coefficient plot + bar chart + validation checkpoint

### Phase 4: Scénario 2 — Surcontrôle sur un médiateur
**Goal**: Le formateur peut montrer que contrôler sur `panier_moyen` dans la régression biaise le coefficient de `pub` vers zéro car `panier_moyen` est un médiateur
**Depends on**: Phase 3
**Requirements**: SC2-01, SC2-02, SC2-03
**Success Criteria** (what must be TRUE):
  1. Le DAG causal illustre clairement les deux chemins causaux (`pub → nb_visites → ventes` ET `pub → panier_moyen → ventes`)
  2. Le coefficient plot montre un coefficient `pub` significativement plus faible quand `panier_moyen` est inclus comme contrôle
  3. Le bar chart de comparaison révèle que l'estimation sans contrôle est proche de la valeur vraie, et l'estimation avec médiateur est biaisée vers le bas
**Plans**: 1 plan

Plans:
- [x] 04-01-PLAN.md — Données + ATT + OLS (sans/avec médiateur) + DAG + coefficient plot + bar chart + CSV export

### Phase 5: Scénario 3 — Surcontrôle sur un collider
**Goal**: Le formateur peut montrer que contrôler sur `posts_reseaux` introduit un biais là où l'estimation naïve était correcte, parce que `posts_reseaux` est un collider
**Depends on**: Phase 4
**Requirements**: SC3-01, SC3-02, SC3-03
**Success Criteria** (what must be TRUE):
  1. Le DAG causal illustre le collider (`pub → posts_reseaux ← ventes`) et rend visible le chemin non causal ouvert par le contrôle
  2. L'estimation sans contrôle sur `posts_reseaux` est proche de la valeur vraie ; l'estimation avec contrôle en diffère d'au moins 5% (biais visible)
  3. Le bar chart de comparaison (naïf / sur-contrôlé / vrai) rend le biais pédagogiquement lisible
**Plans**: 1 plan

Plans:
- [x] 05-01-PLAN.md — COLLIDER_PUB_VENTES_COEFF dans PARAMS + 5 cellules sc3 (DAG V-structure + coefficient plot + bar chart) + CSV export

### Phase 6: Validation bout-en-bout
**Goal**: Le notebook est propre, complet, et prêt à l'emploi — le formateur peut le distribuer ou l'exécuter sans modification
**Depends on**: Phase 5
**Requirements**: INFRA-01, INFRA-02, INFRA-03, INFRA-04 (cross-cutting — validation finale de toutes les phases)
**Success Criteria** (what must be TRUE):
  1. `Restart & Run All` s'exécute de bout en bout sans erreur ni warning bloquant
  2. Tous les fichiers PNG attendus sont présents dans `figures/` et tous les CSV dans `data/` après exécution
  3. Aucun magic number n'existe hors de la cellule Paramètres (revue manuelle du code)
  4. L'effet vrai est identique entre tous les scénarios (même valeur de `EFFET_PUB_VISITES` et `EFFET_PUB_PANIER` utilisée partout)
**Plans**: 1 plan

Plans:
- [ ] 06-01-PLAN.md — P_PUB_ALEATOIRE dans PARAMS + correction sc2/sc3 + cellule validation finale + nbconvert exit 0

## Progress

**Execution Order:**
Phases execute in numeric order: 1 → 2 → 3 → 4 → 5 → 6

| Phase | Plans Complete | Status | Completed |
|-------|----------------|--------|-----------|
| 1. Fondations | 2/2 | Complete (checkpoint) | 2026-03-03 |
| 2. Scénario 0 — Biais de petits nombres | 2/2 | Complete | 2026-03-03 |
| 3. Scénarios 1a/1b/1c — Biais de sélection | 2/2 | Complete | 2026-03-04 |
| 4. Scénario 2 — Surcontrôle sur un médiateur | 1/1 | Complete | 2026-03-04 |
| 5. Scénario 3 — Surcontrôle sur un collider | 1/1 | Complete | 2026-03-04 |
| 6. Validation bout-en-bout | 0/1 | Not started | - |
