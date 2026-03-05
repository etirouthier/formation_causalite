---
gsd_state_version: 1.0
milestone: v1.1
milestone_name: Formation Causalité
status: unknown
last_updated: "2026-03-05T12:32:22.593Z"
progress:
  total_phases: 2
  completed_phases: 2
  total_plans: 3
  completed_plans: 3
---

# Project State

## Project Reference

See: .planning/PROJECT.md (updated 2026-03-05)

**Core value:** Permettre au formateur d'illustrer quatre biais causaux classiques avec des données reproductibles, tous construits sur le même modèle cohérent
**Current focus:** Milestone v1.1 — Phase 8: Ventes par m2 et DAG uniforme

## Current Position

Phase: 8
Plan: 02 (completed)
Status: Phase 8 complete — DAG uniformes en noir, milestone v1.1 complete
Last activity: 2026-03-05 — 08-02 executed: 6 cellules DAG uniformisées en noir, notebook s'execute sans erreur

Progress: [##########] 100% (v1.1 — 2/2 phases completes, phase 8 2/2 plans)

## Performance Metrics

**Velocity (v1.0 reference):**
- Total plans completed: 9
- Average duration: ~5 min/plan
- Total execution time: ~45 min

**v1.1 Phases:**

| Phase | Plans | Status |
|-------|-------|--------|
| 07-scenario-randomisation | 1/1 | Complete |
| 08-vm2-dag-uniforme | 2/2 | Complete |

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
- [04-01]: OLS sans médiateur est le modèle CORRECT en sc2 — inversion pédagogique vs Phase 3 (naïf=correct ici). model_naive_sc2 = sans médiateur, model_med_sc2 = biaisé.
- [04-01]: Pas de C(mois) dans les formules OLS sc2 — assignation aléatoire, saison n'est pas un confondant.
- [04-01]: Seeds isolés SEED+40 (données sc2) et SEED+41 (contrefactuel sc2) — convention +10*phase maintenue.
- [05-01]: OLS naïf (sans collider) est le modèle CORRECT en sc3 — assignation aléatoire, même inversion pédagogique qu'en Phase 4.
- [05-01]: Couleur collider = crimson (rouge) pour distinction visuelle forte vs médiateur (bleu sc2). DAG inclut Pub→Ventes pour structure causale complète.
- [05-01]: Biais direction downward (naive 33.6% > avec-collider 30.5%) — 9.4% relatif. Proximité fortuite ATT (30.2%) ≈ avec-collider commentée explicitement.
- [06-01]: Notebook avait 41 cellules (pas 31 comme supposé dans le plan) — cellule validation ajoutée en 42e position. P_PUB_ALEATOIRE supprime les deux derniers magic numbers 0.5 dans sc2/sc3.
- [07-01]: SEED+70 pour rng_sc4 — convention +10*phase maintenue (phase=7), isole le rng sc4 du reste.
- [07-01]: Grand echantillon = tous les 200 magasins de base_df ; petit = 30 tires sans remise depuis le grand — meme population de base.
- [07-01]: Helpers locaux balance_table() et plot_balance() — evite repetition code pour les deux tailles d'echantillon.
- [07-01]: Couleurs steelblue (Temoin) / darkorange (Traite) coherentes avec palette existante des scenarios 1-3.
- [08-01]: ventes_par_m2 = ventes / n_potentiel calcule dans base_df avant export et dans agg_sc0 apres groupby — mesure intensive independante de la taille.
- [08-01]: ventes agregees via sum dans agg_sc0 groupby — necessite pour calculer ventes_par_m2 au niveau magasin (etait absent du groupby original).
- [08-02]: node_color='black' uniforme dans tous les DAG — suppression des color_map (steelblue/seagreen/darkorange/crimson/mediumpurple) dans les 6 cellules nx.draw_networkx().

### Pending Todos

None yet.

### Blockers/Concerns

None at start of v1.1.

## Session Continuity

Last session: 2026-03-05
Stopped at: Completed 08-02-PLAN.md — DAG uniformes en noir (6 cellules, 6 figures PNG)
Resume file: None
