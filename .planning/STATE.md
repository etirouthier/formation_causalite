# Project State

## Project Reference

See: .planning/PROJECT.md (updated 2026-03-02)

**Core value:** Permettre au formateur d'illustrer quatre biais causaux classiques avec des données reproductibles, tous construits sur le même modèle cohérent
**Current focus:** Phase 2 — Scénario 0 — Biais de petits nombres

## Current Position

Phase: 2 of 6 (Scénario 0 — Biais de petits nombres)
Plan: 2 of TBD in current phase (02-02 complete — awaiting checkpoint human-verify)
Status: In progress — checkpoint human-verify pending
Last activity: 2026-03-03 — Plan 02-02 completed (code-sc0-fig3 + code-sc0-fig4 insérées, sc0_top10.png + sc0_loi_grands_nombres.png exportés, nbconvert exit 0)

Progress: [████░░░░░░] 25%

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

### Pending Todos

None yet.

### Blockers/Concerns

- [Phase 1 - RESOLVED]: Calibration validée empiriquement avec SEED=42 — P_BASE_VISITE=0.25, N_PETIT=30, N_MOYEN=150, N_GRAND=500 : 0 zéros, ratio_variance=4.4x
- [Phase 5]: alpha_collider pour `posts_reseaux` est non trivial — nécessite des essais pour garantir la visibilité du biais (≥5% de différence)

## Session Continuity

Last session: 2026-03-03
Stopped at: Plan 02-02 — checkpoint human-verify pending — code-sc0-fig3 + code-sc0-fig4 insérées, 4 PNG exportés (sc0_top10.png 10/10 petits), nbconvert exit 0
Resume file: None
