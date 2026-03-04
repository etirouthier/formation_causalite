# Requirements: Générateur de données — Formation Causalité

**Defined:** 2026-03-02
**Core Value:** Permettre au formateur d'illustrer visuellement quatre biais causaux classiques avec des données reproductibles, tous construits sur le même modèle de données cohérent

---

## v1 Requirements

### Infrastructure

- [x] **INFRA-01**: Le formateur peut modifier tous les paramètres de simulation depuis une cellule unique en tête de notebook (constantes ALL_CAPS, aucun magic number ailleurs)
- [x] **INFRA-02**: Le notebook produit des résultats identiques à chaque exécution `Restart & Run All` via `numpy.random.default_rng(SEED)`
- [x] **INFRA-03**: Une cellule d'assertions valide que les paramètres sont cohérents (`p_visite ∈ [0,1]`, overlap suffisant dans les scénarios de sélection, effet vrai identique entre scénarios)
- [x] **INFRA-04**: Toutes les figures sont automatiquement exportées en PNG vers `figures/` et tous les datasets en CSV vers `data/` lors de l'exécution du notebook

### Générateur de données (DGP)

- [x] **DGP-01**: Un générateur de panel partagé `generate_base_panel(params, rng)` produit le DataFrame N_magasins × T_mois utilisé par tous les scénarios
- [x] **DGP-02**: Chaque magasin est caractérisé par : `taille` (petit/moyen/grand, détermine N_potentiel), `urbain` (binaire, effet additif sur p_visite), `qualite_equipe` (binaire, effet additif sur p_visite)
- [x] **DGP-03**: La variable mensuelle `saison` produit un effet additif paramétrable sur `p_visite`
- [x] **DGP-04**: Le traitement `pub` est binaire par magasin × mois, avec un mécanisme de sélection probabiliste paramétrable (`P(pub=1 | caractéristique)`)
- [x] **DGP-05**: L'effet vrai de la pub est : +10% sur `p_visite` (nombre de visiteurs) ET +10% sur `μ_panier` (panier moyen), toutes deux paramétrables ; effet homogène entre magasins
- [x] **DGP-06**: Les DAGs causaux sont dessinés programmatiquement via `networkx.DiGraph` avec un layout de nœuds fixe et déterministe (pas de spring_layout)

### Scénario 0 — Biais de petits nombres

- [x] **SC0-01**: Figure montrant la distribution du `panier_moyen` par taille de magasin (histogramme ou violin plot avec `hue=taille`)
- [x] **SC0-02**: Scatter plot montrant la relation entre `nb_visites` et la variance du `panier_moyen` par magasin (petits magasins = plus de variance)
- [x] **SC0-03**: Bar chart ou tableau des top 10 magasins par `panier_moyen` le plus élevé, avec la répartition par taille de magasin (illustre la sur-représentation des petits magasins)

### Scénario 1 — Biais de sélection

- [x] **SC1-01**: Scénario 1a (sélection par qualité d'équipe) : DAG causal + coefficient plot (OLS naïf vs OLS ajusté vs valeur vraie avec IC 95%) + bar chart comparant effet naïf/ajusté/vrai
- [x] **SC1-02**: Scénario 1b (sélection par localisation urbain/rural) : DAG causal + coefficient plot + bar chart comparant effet naïf/ajusté/vrai
- [x] **SC1-03**: Scénario 1c (sélection par saison) : DAG causal + coefficient plot + bar chart comparant effet naïf/ajusté/vrai

### Scénario 2 — Surcontrôle sur un médiateur

- [x] **SC2-01**: DAG causal illustrant les deux chemins (`pub → nb_visites → ventes` ET `pub → panier_moyen → ventes`)
- [x] **SC2-02**: Coefficient plot montrant comment le coefficient `pub` change quand on ajoute `panier_moyen` comme variable de contrôle (OLS sans médiateur vs OLS avec médiateur)
- [x] **SC2-03**: Bar chart comparant : effet estimé sans contrôle (correct) vs effet estimé avec contrôle sur médiateur (biaisé) vs valeur vraie

### Scénario 3 — Surcontrôle sur un collider

- [ ] **SC3-01**: DAG causal illustrant le collider (`pub → posts_reseaux ← ventes`) et le chemin non causal ouvert par le contrôle
- [ ] **SC3-02**: Coefficient plot montrant comment le coefficient `pub` change quand on ajoute `posts_reseaux` comme variable de contrôle (OLS sans collider vs OLS avec collider)
- [ ] **SC3-03**: Bar chart comparant : estimation naïve (sans contrôle) vs estimation sur-contrôlée (avec collider) vs valeur vraie

---

## v2 Requirements

*(Déféré — hors scope pédagogique v1)*

- Effets hétérogènes de la pub selon le magasin
- Widgets interactifs ipywidgets pour exploration temps réel
- Version R du notebook
- Interface web (Streamlit/Dash)

---

## Out of Scope

| Feature | Raison |
|---------|--------|
| Widgets interactifs | Complexité technique, le formateur édite directement les paramètres |
| Effets hétérogènes de la pub | Distrait du message sur les biais de sélection/contrôle |
| Données réelles | Simulation pure pour contrôle pédagogique total |
| Version R | Python uniquement pour v1 |
| Génération de slides automatique | Le formateur extrait les figures manuellement |
| Données individuelles clients non agrégées | Agrégation magasin×mois suffit |

---

## Traceability

| Requirement | Phase | Status |
|-------------|-------|--------|
| INFRA-01 | Phase 1 | Complete (01-01) |
| INFRA-02 | Phase 1 | Complete (01-01) |
| INFRA-03 | Phase 1 | Complete (01-02) |
| INFRA-04 | Phase 1 | Complete (01-01) |
| DGP-01 | Phase 1 | Complete (01-02) |
| DGP-02 | Phase 1 | Complete (01-02) |
| DGP-03 | Phase 1 | Complete (01-02) |
| DGP-04 | Phase 1 | Complete (01-02) |
| DGP-05 | Phase 1 | Complete (01-02) |
| DGP-06 | Phase 1 | Complete (01-02) |
| SC0-01 | Phase 2 | Complete (02-01) |
| SC0-02 | Phase 2 | Complete (02-01) |
| SC0-03 | Phase 2 | Complete (02-02) |
| SC1-01 | Phase 3 | Complete (03-01) |
| SC1-02 | Phase 3 | Complete (03-01) |
| SC1-03 | Phase 3 | Complete (03-02) |
| SC2-01 | Phase 4 | Complete (04-01) |
| SC2-02 | Phase 4 | Complete (04-01) |
| SC2-03 | Phase 4 | Complete (04-01) |
| SC3-01 | Phase 5 | Pending |
| SC3-02 | Phase 5 | Pending |
| SC3-03 | Phase 5 | Pending |

**Coverage:**
- v1 requirements: 22 total
- Mapped to phases: 22
- Unmapped: 0

---
*Requirements defined: 2026-03-02*
*Last updated: 2026-03-03 after plan 02-02 completion — SC0-03 marked complete*
