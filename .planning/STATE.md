---
gsd_state_version: 1.0
milestone: v1.0
milestone_name: milestone
status: in_progress
last_updated: "2026-03-04T13:15:00Z"
progress:
  total_phases: 6
  completed_phases: 3
  total_plans: 7
  completed_plans: 6
---

# Project State

## Project Reference

See: .planning/PROJECT.md (updated 2026-03-02)

**Core value:** Permettre au formateur d'illustrer quatre biais causaux classiques avec des données reproductibles, tous construits sur le même modèle cohérent
**Current focus:** Phase 4 — Scénario 2 — Surcontrôle sur un médiateur

## Current Position

Phase: 4 of 6 (Scénario 2 — Surcontrôle sur un médiateur)
Plan: 0 of TBD in current phase (Phase 3 COMPLETE — 1a/1b/1c DV log_rev_int, 9 PNG + 3 CSV, surestimation validée)
Status: Ready to start Phase 4
Last activity: 2026-03-04 — Plan 03-02 COMPLETE — scénario 1c validé, phase 3 complète (OLS naïf > ATT pour 1a/1b/1c)

Progress: [█████░░░░░] 50%

## Performance Metrics

**Velocity:**
- Total plans completed: 4
- Average duration: 5 min
- Total execution time: 20 min

**By Phase:**

| Phase | Plans | Total | Avg/Plan |
|-------|-------|-------|----------|
| 01-fondations | 2/2 | 10 min | 5 min |
| 02-scenario0-petits-nombres | 2/TBD | 10 min | 5 min |
| 03-sc-narios-1a-1b-1c-biais-de-s-lection | 1/TBD | 15 min | 15 min |

**Recent Trend:**
- Last 5 plans: 3 min, 7 min, 5 min
- Trend: stable

*Updated after each plan completion*

## Accumulated Context

### Decisions

Decisions are logged in PROJECT.md Key Decisions table.
Recent decisions affecting current work:

- [Pre-phase]: Modèle micro-fondé client par client — crée naturellement le biais de petits nombres via la variance binomiale
- [Pre-phase]: `panier_moyen` dépend uniquement de la pub — simplifie le Scénario 2 (médiateur pur)
- [Pre-phase]: Paramètres dans une cellule unique ALL_CAPS — formateur édite un seul endroit
- [01-01]: Commentaire de garde-fou retiré du code source car il déclenchait le check de validation — libellé équivalent sans la chaîne interdite utilisé à la place
- [01-02]: P_BASE_VISITE fixé à 0.25 (non 0.05) — p trop faible causait nb_visites=0 pour petits magasins (P(0)≈36% avec N_PETIT=30, p=0.05)
- [01-02]: Mapping effet_saison cyclique via ((mois-1)%12)+1 — T_MOIS=24 nécessite répétition du cycle annuel sur les 12 clés de EFFET_SAISON
- [02-01]: groupby(['magasin_id','taille']) avec les deux colonnes — 'taille' obligatoire pour survivre au reset_index()
- [02-01]: colors_sc0 dict défini une fois dans code-sc0-fig1, réutilisé dans fig2 et les figures du plan 02-02
- [02-02]: rng_fig4 = np.random.default_rng(SEED + 4) local dans code-sc0-fig4 — isole les simulations Figure 4 du rng global pour garantir la reproductibilité des scénarios 1-3
- [02-02]: warn_singular=False dans sns.kdeplot obligatoire pour N=100000 (std ≈ 0.018, courbe absente silencieusement sinon)
- [03-01]: colors_est redéfini dans code-sc1b-coeff (pas dépendant de code-sc1a-bar) — robustesse réexécution partielle
- [03-01]: Direction biais DGP inversée pour 1a et 1b (OLS naïf sous-estime ATT, non surestime) — EFFET_EQUIPE=0.02 et EFFET_URBAIN=0.03 trop faibles vs variance taille ; décision de recalibration à prendre par le formateur
- [03-01 REFACTORING]: DV = log(ventes/n_potentiel) — mesure intensive, supprime l'effet de taille, interprétation en log-points ≈ % uplift. EFFET_SAISON max 0.08 (vs 0.02). Surestimation validée: 1a +70%, 1b +55%, 1c +8.6pp (SEED=42)
- [03-02]: Checkpoint human-verify sc1c superseded par demande architecturale du formateur (PAUSE.md). Assignation niveau ligne (pas magasin) pour sc1c. OLS naïf sans C(mois) est l'exception structurelle voulue pour rendre le biais saisonnier visible.

### Pending Todos

None yet.

### Blockers/Concerns

- [Phase 1 - RESOLVED]: Calibration validée empiriquement avec SEED=42 — P_BASE_VISITE=0.25, N_PETIT=30, N_MOYEN=150, N_GRAND=500 : 0 zéros, ratio_variance=4.4x
- [Phase 5]: alpha_collider pour `posts_reseaux` est non trivial — nécessite des essais pour garantir la visibilité du biais (≥5% de différence)
- [Phase 3 - RESOLVED]: Direction du biais pédagogique corrigée via refactoring DV log_rev_int + EFFET_EQUIPE/URBAIN=0.20 + EFFET_SAISON max 0.08. OLS naïf > ATT_log confirmé pour 1a (+70%), 1b (+55%), 1c (+8.6pp). Blocker résolu.

## Session Continuity

Last session: 2026-03-04
Stopped at: Plan 03-02 COMPLETE — Phase 3 entière validée. Scénario 1c: OLS naïf 38.0% > ATT 29.4% (+8.6pp). 9 PNG + 3 CSV produits. nbconvert exit 0. Prochaine étape: Phase 4 — Scénario 2 médiateur.
Resume file: None
