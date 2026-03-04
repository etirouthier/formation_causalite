# Phase 6: Validation bout-en-bout - Context

**Gathered:** 2026-03-04
**Status:** Ready for planning

<domain>
## Phase Boundary

Valider que le notebook est propre et prêt à distribuer : exécution complète sans erreur, zéro magic number hors cellule Paramètres, présence de tous les fichiers générés, cohérence des effets vrais entre scénarios. Aucun nouveau scénario ni nouvelle visualisation — validation et nettoyage uniquement.

</domain>

<decisions>
## Implementation Decisions

### Portée des magic numbers
- `p=0.5` dans `rng.binomial(1, 0.5, ...)` pour l'assignation pub aléatoire (sc2, sc3) EST un paramètre de simulation → ajouter `P_PUB_ALEATOIRE = 0.5` dans la cellule Paramètres et remplacer les deux occurrences
- Les offsets SEED (SEED+4, SEED+10, SEED+11, SEED+20, SEED+21, SEED+30, SEED+31, SEED+40, SEED+41, SEED+50, SEED+51) sont des détails d'implémentation RNG internes — acceptables tels quels, pas de migration dans PARAMS
- Les paramètres d'affichage (figsize, dpi, markersize, width) ne sont PAS des magic numbers dans ce contexte — laisser en place
- Les seuils d'assertion (ratio > 2.0, p_visite ∈ [0.01, 0.99]) sont des critères de validation pédagogique — acceptables tels quels

### Cellule de validation finale
- Ajouter une cellule en toute fin de notebook qui vérifie automatiquement :
  1. Présence de tous les fichiers PNG attendus (20 fichiers dans `figures/`)
  2. Présence de tous les CSV attendus (7 fichiers dans `data/`)
  3. Assertion que `EFFET_PUB_VISITES` et `EFFET_PUB_PANIER` dans PARAMS sont bien les valeurs utilisées partout (via `assert PARAMS['effet_pub_visites'] == EFFET_PUB_VISITES`)
- Format : assertions Python + message de succès "✓ Validation notebook : OK" si tout passe
- Si un fichier manque : `AssertionError` avec liste des fichiers absents

### Warnings
- L'exécution actuelle ne produit aucun warning bloquant — aucun `filterwarnings` supplémentaire nécessaire
- Ne pas supprimer les warnings statsmodels légitimes (convergence, degrés de liberté) — ils sont informatifs

### Vérification manuelle magic numbers
- Revue systématique du code : seul `p=0.5` (sc2 et sc3) est identifié comme magic number à corriger
- Aucun autre paramètre numérique de simulation hors PARAMS détecté

### Claude's Discretion
- Wording exact du message de succès final
- Ordre des assertions dans la cellule de validation
- Éventuels petits ajustements cosmétiques de commentaires si découverts pendant la revue

</decisions>

<specifics>
## Specific Ideas

- La cellule de validation doit lire la liste des fichiers attendus dynamiquement depuis les appels `savefig` du notebook, ou les hardcoder explicitement (liste des 20 PNG + 7 CSV) — approche explicite préférable pour la clarté pédagogique
- Le message final "Restart & Run All" dans le header du notebook est déjà présent et correct

</specifics>

<code_context>
## Existing Code Insights

### Reusable Assets
- Cellule d'assertions existante (après génération base_df) : pattern `assert condition, message` — réutiliser le même style pour la validation finale
- `Path('figures').mkdir(...)` et `Path('data').mkdir(...)` déjà en place

### Established Patterns
- PARAMS dict centralise tous les paramètres de simulation — ajouter `P_PUB_ALEATOIRE` suit ce pattern
- Variables ALL_CAPS au niveau module + injection dans PARAMS dict — suivre pour le nouveau paramètre
- RNG dédié par scénario (`rng_sc1a`, `rng_sc2`, etc.) — pattern établi, ne pas modifier

### Integration Points
- `p=0.5` à remplacer dans deux cellules : cellule sc2 (In[24]) et cellule sc3 (In[28])
- Cellule de validation finale : nouvelle cellule après In[31] (la dernière cellule sc3)
- 20 fichiers PNG attendus : sc0×4, dag_pattern_demo, sc1a×3, sc1b×3, sc1c×3, sc2×3, sc3×3
- 7 fichiers CSV attendus : base_panel, sc0, sc1a, sc1b, sc1c, sc2_mediateur, sc3_collider

</code_context>

<deferred>
## Deferred Ideas

None — discussion stayed within phase scope.

</deferred>

---

*Phase: 06-validation-bout-en-bout*
*Context gathered: 2026-03-04*
