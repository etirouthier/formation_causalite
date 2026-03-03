# Phase 3: Scénarios 1a/1b/1c — Biais de sélection - Context

**Gathered:** 2026-03-03
**Status:** Ready for planning

<domain>
## Phase Boundary

Produire 3 sous-scénarios indépendants (1a, 1b, 1c) illustrant le biais de sélection : quand un confondant détermine l'assignation au traitement (pub), comparer naïvement traités et non-traités surestime l'effet. Chaque sous-scénario produit un DAG, un coefficient plot et un bar chart. Pas de matching, pas de méthodes causales avancées — uniquement OLS naïf vs OLS ajusté vs valeur vraie (ATT contrefactuel).

</domain>

<decisions>
## Implementation Decisions

### Structure des sous-scénarios
- Code commun pour la génération et l'assignation pub (une fonction par confondant ou paramètres mutualisés), mais 3 sections de cellules **indépendantes** dans le notebook (1a, 1b, 1c)
- Un seul confondant à la fois par sous-scénario — pas de modèle multi-confondants
- Confondants : 1a = `qualite_equipe`, 1b = `urbain`, 1c = `effet_saison_val` / `mois`

### Figures — 9 au total
- **Séparées par type ET par sous-scénario** : 3 scénarios × 3 types = 9 PNG dans `figures/`
- Naming : `sc1a_dag.png`, `sc1a_coeff.png`, `sc1a_bar.png` (et idem pour 1b, 1c)
- Pas de figure composite multi-scénarios

### Coefficient plot
- Style **vertical** : un point par estimateur (naïf, ajusté, vrai) sur l'axe Y, valeur sur l'axe X — ou l'inverse si plus lisible
- **Barres d'erreur** pour les IC 95% (errplot / errorbar matplotlib)
- 3 points par plot : OLS naïf, OLS ajusté, ATT contrefactuel (valeur vraie)

### Valeur vraie — ATT contrefactuel
- Pour chaque sous-scénario, l'**ATT** est calculé par comparaison contrefactuelle :
  1. Identifier les magasins traités (pub=1) dans le scénario
  2. Recalculer leurs outcomes avec pub=0 (contrefactuel, impossible en vrai)
  3. ATT = moyenne(Y_observé − Y_contrefactuel) pour les traités
- Cette valeur est utilisée comme référence "vrai effet" dans le coefficient plot et le bar chart

### Variable dépendante
- OLS sur **`ventes`** (chiffre d'affaires total), pas `panier_moyen`

### Niveau et spécification OLS
- **Panel complet** : 200 magasins × 24 mois = 4800 lignes
- **Scénarios 1a et 1b** (confondant non saisonnier) :
  - OLS naïf : `ventes ~ pub + C(mois)` — contrôle la saisonnalité mais PAS le confondant d'intérêt
  - OLS ajusté : `ventes ~ pub + confondant + C(mois)`
- **Scénario 1c** (confondant = saison) :
  - OLS naïf : `ventes ~ pub` — SANS mois, pour rendre le biais saisonnier visible
  - OLS ajusté : `ventes ~ pub + C(mois)` — contrôle la saison

### DAG — nœuds
- **Noms verbeux en français** pour les slides : `Qualité équipe`, `Localisation`, `Saison`
- Nœuds communs à tous les DAGs : `Pub` et `Ventes`
- Même pattern de layout fixe que `code-dag-pattern` (`pos` dict, pas de `spring_layout`)

### Claude's Discretion
- Couleurs des nœuds dans les DAGs (cohérentes avec le style du notebook)
- Palette des 3 estimateurs dans les coefficient plots et bar charts
- Labels exacts des axes et titres des figures (factuel, sans commentaire interprétatif)
- Gestion du rng pour le calcul ATT contrefactuel (rng local dédié par scénario)

</decisions>

<code_context>
## Existing Code Insights

### Reusable Assets
- `generate_base_panel(params, rng)` : génère le panel partagé — Phase 3 l'appelle avec PARAMS inchangés, puis assigne pub selon le confondant
- `compute_outcomes(df, params, rng)` : calcule ventes et panier_moyen à partir de `pub` — à appeler deux fois par scénario (pub assigné + pub=0 pour ATT)
- `code-dag-pattern` : pattern DAG établi (`nx.DiGraph`, `pos` dict fixe, `draw_networkx`, `fig.savefig` avant `plt.show()`)
- `smf.ols` importé depuis `statsmodels.formula.api` — disponible, pas encore utilisé

### Established Patterns
- `rng = np.random.default_rng(SEED)` passé en argument — chaque scénario doit utiliser un `rng` local dédié (ex : `rng_sc1a = np.random.default_rng(SEED + 10)`) pour ne pas perturber l'état global
- `fig.savefig(..., dpi=150, bbox_inches='tight')` avant `plt.show()` — obligatoire pour tous les exports
- `C(mois)` dans la formule statsmodels pour les dummies mois (traitement catégoriel)

### Integration Points
- Les 3 sections (1a, 1b, 1c) s'insèrent après les cellules du Scénario 0 dans le notebook
- `base_df` est disponible en mémoire — Phase 3 l'utilise comme point de départ pour assigner pub
- Les paramètres d'assignation pub existent déjà dans PARAMS : `P_PUB_BONNE_EQUIPE`, `P_PUB_MAUVAISE_EQUIPE`, `P_PUB_URBAIN`, `P_PUB_RURAL`, `P_PUB_HAUTE_SAISON`, `P_PUB_BASSE_SAISON`

</code_context>

<specifics>
## Specific Ideas

- La "valeur vraie" (ATT) est intentionnellement impossible à calculer en vrai — c'est un avantage pédagogique de la simulation : montrer ce que l'on cherche à estimer
- Le scénario 1c est structurellement différent des autres : le naïf N'inclut PAS `C(mois)` pour rendre le biais saisonnier visible ; l'ajusté l'inclut

</specifics>

<deferred>
## Deferred Ideas

Aucune — la discussion est restée dans le périmètre de la Phase 3.

</deferred>

---

*Phase: 03-sc-narios-1a-1b-1c-biais-de-s-lection*
*Context gathered: 2026-03-03*
