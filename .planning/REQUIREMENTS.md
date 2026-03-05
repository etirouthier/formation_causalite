# Requirements: Générateur de données — Formation Causalité

**Defined:** 2026-03-05
**Core Value:** Permettre au formateur d'illustrer visuellement quatre biais causaux classiques avec des données reproductibles, tous construits sur le même modèle de données cohérent

---

## v1.1 Requirements

### Scénario Randomisation — Balance des groupes

- [ ] **RAND-01**: Le formateur peut illustrer la balance des caractéristiques (`% urbain`, `taille`, `qualité équipe`) entre groupe traité et groupe témoin après tirage aléatoire
- [ ] **RAND-02**: Le scénario montre le cas grand échantillon — les distributions des caractéristiques sont équilibrées entre les deux groupes
- [ ] **RAND-03**: Le scénario montre le cas petit échantillon — des déséquilibres apparents surgissent par le seul hasard (lien pédagogique avec Sc0)
- [ ] **RAND-04**: Le dataset du scénario est exporté en CSV dans `data/` et les figures en PNG dans `figures/`

### Ventes par m²

- [ ] **VM2-01**: La variable dérivée `ventes_par_m2 = ventes / N_potentiel` est calculée dans le notebook (proxy surface, interprétation en euros/m²)
- [ ] **VM2-02**: Au moins une visualisation représente `ventes_par_m2` par caractéristique pertinente (taille, urbain, ou pub)

### DAG

- [ ] **DAG-01**: Tous les DAG du notebook utilisent uniquement le noir pour les nœuds, arêtes et labels — suppression de toute couleur

---

## v2 Requirements

*(Déféré — hors scope pédagogique v1.1)*

- Effets hétérogènes de la pub selon le magasin
- Widgets interactifs ipywidgets pour exploration temps réel
- Version R du notebook
- Interface web (Streamlit/Dash)
- Autres méthodes d'estimation causale (DiD, RDD, IV)

---

## Out of Scope

| Feature | Raison |
|---------|--------|
| Widgets interactifs | Complexité technique, le formateur édite directement les paramètres |
| Effets hétérogènes de la pub | Distrait du message sur les biais de sélection/contrôle |
| Données réelles | Simulation pure pour contrôle pédagogique total |
| Version R | Python uniquement pour v1.x |
| Génération de slides automatique | Le formateur extrait les figures manuellement |

---

## Traceability

| Requirement | Phase | Status |
|-------------|-------|--------|
| RAND-01 | Phase 7 | Pending |
| RAND-02 | Phase 7 | Pending |
| RAND-03 | Phase 7 | Pending |
| RAND-04 | Phase 7 | Pending |
| VM2-01 | Phase 8 | Pending |
| VM2-02 | Phase 8 | Pending |
| DAG-01 | Phase 8 | Pending |

**Coverage:**
- v1.1 requirements: 7 total
- Mapped to phases: 7
- Unmapped: 0

---
*Requirements defined: 2026-03-05*
