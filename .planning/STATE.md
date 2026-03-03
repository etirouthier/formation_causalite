# Project State

## Project Reference

See: .planning/PROJECT.md (updated 2026-03-02)

**Core value:** Permettre au formateur d'illustrer quatre biais causaux classiques avec des données reproductibles, tous construits sur le même modèle cohérent
**Current focus:** Phase 1 — Fondations

## Current Position

Phase: 1 of 6 (Fondations)
Plan: 1 of 2 in current phase (01-01 complete)
Status: In progress
Last activity: 2026-03-03 — Plan 01-01 completed

Progress: [█░░░░░░░░░] 8%

## Performance Metrics

**Velocity:**
- Total plans completed: 1
- Average duration: 3 min
- Total execution time: 3 min

**By Phase:**

| Phase | Plans | Total | Avg/Plan |
|-------|-------|-------|----------|
| 01-fondations | 1/2 | 3 min | 3 min |

**Recent Trend:**
- Last 5 plans: 3 min
- Trend: -

*Updated after each plan completion*

## Accumulated Context

### Decisions

Decisions are logged in PROJECT.md Key Decisions table.
Recent decisions affecting current work:

- [Pre-phase]: Modèle micro-fondé client par client — crée naturellement le biais de petits nombres via la variance binomiale
- [Pre-phase]: `panier_moyen` dépend uniquement de la pub — simplifie le Scénario 2 (médiateur pur)
- [Pre-phase]: Paramètres dans une cellule unique ALL_CAPS — formateur édite un seul endroit
- [01-01]: Commentaire de garde-fou retiré du code source car il déclenchait le check de validation — libellé équivalent sans la chaîne interdite utilisé à la place

### Pending Todos

None yet.

### Blockers/Concerns

- [Phase 1]: Calibration à valider empiriquement — les valeurs par défaut (N_petit=20, N_grand=400) sont recommandées mais non testées
- [Phase 5]: alpha_collider pour `posts_reseaux` est non trivial — nécessite des essais pour garantir la visibilité du biais (≥5% de différence)

## Session Continuity

Last session: 2026-03-03
Stopped at: Plan 01-01 complete — notebook squelette créé avec cellules Paramètres et Imports
Resume file: None
