"""
Insert 5 Scénario 2 cells into formation_causalite.ipynb after cell index 30.
"""
import json

with open('formation_causalite.ipynb') as f:
    nb = json.load(f)

print(f"Before insertion: {len(nb['cells'])} cells")

# Cell 1 — Markdown section
cell_md = {
    "cell_type": "markdown",
    "metadata": {},
    "source": [
        "---\n",
        "## Scénario 2 — Surcontrôle sur un médiateur\n",
        "\n",
        "`panier_moyen` est un médiateur : `pub → panier_moyen → ventes`. Contrôler sur le médiateur dans la régression bloque mécaniquement ce chemin causal et biaise le coefficient de `pub` vers le bas — même si l'assignation est parfaitement aléatoire. Le modèle naïf (sans contrôle) capture l'effet total et est ici correct."
    ]
}

# Cell 2 — code-sc2-data
cell_data = {
    "cell_type": "code",
    "execution_count": None,
    "metadata": {},
    "outputs": [],
    "source": [
        "# ─────────────────────────────────────────────\n",
        "# Scénario 2 — Surcontrôle sur un médiateur\n",
        "# Assignation pub : aléatoire niveau magasin (pas de confondant)\n",
        "# Médiateur bloqué : panier_moyen\n",
        "# ─────────────────────────────────────────────\n",
        "\n",
        "rng_sc2 = np.random.default_rng(SEED + 40)\n",
        "\n",
        "# Assignation pub aléatoire au niveau magasin (p=0.5 — pas de confondant)\n",
        "stores_sc2 = base_df[['magasin_id']].drop_duplicates('magasin_id').copy()\n",
        "stores_sc2['pub'] = rng_sc2.binomial(1, 0.5, size=len(stores_sc2))\n",
        "\n",
        "# Panel complet + outcomes observés\n",
        "df_sc2 = base_df.merge(stores_sc2[['magasin_id', 'pub']], on='magasin_id')\n",
        "df_sc2 = compute_outcomes(df_sc2, PARAMS, rng_sc2)\n",
        "df_sc2['log_rev_int'] = np.log(df_sc2['ventes'] / df_sc2['n_potentiel'])\n",
        "\n",
        "# Calcul ATT contrefactuel (rng dédié pour isolation)\n",
        "treated_ids_sc2 = stores_sc2[stores_sc2['pub'] == 1]['magasin_id'].values\n",
        "df_treated_sc2 = df_sc2[df_sc2['magasin_id'].isin(treated_ids_sc2)].copy()\n",
        "rng_cf_sc2 = np.random.default_rng(SEED + 41)\n",
        "df_cf_sc2 = df_treated_sc2.copy()\n",
        "df_cf_sc2['pub'] = 0\n",
        "df_cf_sc2 = compute_outcomes(df_cf_sc2, PARAMS, rng_cf_sc2)\n",
        "df_cf_sc2['log_rev_int'] = np.log(df_cf_sc2['ventes'] / df_cf_sc2['n_potentiel'])\n",
        "log_Y1_sc2 = np.log(df_treated_sc2['ventes'] / df_treated_sc2['n_potentiel'])\n",
        "log_Y0_sc2 = np.log(df_cf_sc2['ventes'] / df_cf_sc2['n_potentiel'])\n",
        "att_sc2_log = (log_Y1_sc2 - log_Y0_sc2).mean()\n",
        "\n",
        "# OLS sans médiateur : effet total (correct car assignation aléatoire)\n",
        "model_naive_sc2 = smf.ols('log_rev_int ~ pub', data=df_sc2).fit()\n",
        "# OLS avec médiateur : effet direct seulement (biaisé vers le bas)\n",
        "model_med_sc2   = smf.ols('log_rev_int ~ pub + panier_moyen', data=df_sc2).fit()\n",
        "\n",
        "# Export CSV\n",
        "df_sc2.to_csv('data/sc2_mediateur.csv', index=False)\n",
        "print(f\"Sc2 — Traités: {len(treated_ids_sc2)}/200 magasins\")\n",
        "print(f\"Sc2 — ATT: {att_sc2_log*100:.1f}%  |  OLS sans médiateur: {model_naive_sc2.params['pub']*100:.1f}%  |  OLS avec panier_moyen: {model_med_sc2.params['pub']*100:.1f}%\")"
    ]
}

# Cell 3 — code-sc2-dag
cell_dag = {
    "cell_type": "code",
    "execution_count": None,
    "metadata": {},
    "outputs": [],
    "source": [
        "# ─────────────────────────────────────────────\n",
        "# Figure DAG — Scénario 2\n",
        "# Deux chemins causaux : Pub→Nb visites→Ventes ET Pub→Panier moyen→Ventes\n",
        "# PAS d'arête directe Pub→Ventes (le DGP n'en a pas)\n",
        "# ─────────────────────────────────────────────\n",
        "\n",
        "G_sc2 = nx.DiGraph()\n",
        "G_sc2.add_edges_from([\n",
        "    ('Pub', 'Nb visites'),\n",
        "    ('Pub', 'Panier moyen'),\n",
        "    ('Nb visites', 'Ventes'),\n",
        "    ('Panier moyen', 'Ventes'),\n",
        "])\n",
        "pos_sc2 = {\n",
        "    'Pub': (0, 0.5),\n",
        "    'Nb visites': (1, 1),\n",
        "    'Panier moyen': (1, 0),\n",
        "    'Ventes': (2, 0.5),\n",
        "}\n",
        "color_map_sc2 = {\n",
        "    'Pub': 'steelblue',\n",
        "    'Ventes': 'seagreen',\n",
        "    'Nb visites': 'darkorange',\n",
        "    'Panier moyen': 'mediumpurple',\n",
        "}\n",
        "node_colors_sc2 = [color_map_sc2[n] for n in G_sc2.nodes()]\n",
        "\n",
        "fig, ax = plt.subplots(figsize=(6, 3.5))\n",
        "nx.draw_networkx(G_sc2, pos_sc2, ax=ax,\n",
        "                 node_color=node_colors_sc2,\n",
        "                 node_size=2000, font_size=9, font_color='white',\n",
        "                 arrows=True, arrowsize=20)\n",
        "ax.axis('off')\n",
        "ax.set_title('DAG — Scénario 2 : deux chemins causaux via médiateurs')\n",
        "fig.savefig('figures/sc2_dag.png', dpi=150, bbox_inches='tight')\n",
        "plt.show()"
    ]
}

# Cell 4 — code-sc2-coeff
cell_coeff = {
    "cell_type": "code",
    "execution_count": None,
    "metadata": {},
    "outputs": [],
    "source": [
        "# ─────────────────────────────────────────────\n",
        "# Figure coefficient plot — Scénario 2\n",
        "# 3 points : OLS sans médiateur (correct), OLS avec panier_moyen (biaisé), ATT (vrai)\n",
        "# ─────────────────────────────────────────────\n",
        "\n",
        "coef_naive_sc2 = model_naive_sc2.params['pub']\n",
        "ci_naive_sc2   = model_naive_sc2.conf_int()\n",
        "xerr_naive_sc2 = [[coef_naive_sc2 - ci_naive_sc2.loc['pub', 0]],\n",
        "                   [ci_naive_sc2.loc['pub', 1] - coef_naive_sc2]]\n",
        "\n",
        "coef_med_sc2 = model_med_sc2.params['pub']\n",
        "ci_med_sc2   = model_med_sc2.conf_int()\n",
        "xerr_med_sc2 = [[coef_med_sc2 - ci_med_sc2.loc['pub', 0]],\n",
        "                 [ci_med_sc2.loc['pub', 1] - coef_med_sc2]]\n",
        "\n",
        "estimators_sc2 = ['OLS sans médiateur', 'OLS avec panier_moyen', 'Valeur vraie (ATT)']\n",
        "y_pos_sc2 = [2, 1, 0]\n",
        "\n",
        "fig, ax = plt.subplots(figsize=(8, 4))\n",
        "ax.errorbar(coef_naive_sc2, 2, xerr=xerr_naive_sc2, fmt='o', capsize=5,\n",
        "            color='#e74c3c', label='OLS sans médiateur', markersize=8)\n",
        "ax.errorbar(coef_med_sc2, 1, xerr=xerr_med_sc2, fmt='o', capsize=5,\n",
        "            color='#3498db', label='OLS avec panier_moyen', markersize=8)\n",
        "ax.errorbar(att_sc2_log, 0, fmt='D', color='#2ecc71',\n",
        "            label='Valeur vraie (ATT)', markersize=10)\n",
        "ax.axvline(x=att_sc2_log, color='gray', linestyle='--', alpha=0.5)\n",
        "ax.set_yticks(y_pos_sc2)\n",
        "ax.set_yticklabels(estimators_sc2)\n",
        "ax.set_xlabel('Uplift log des ventes (≈ %)')\n",
        "ax.set_title('Scénario 2 — Coefficients OLS sans vs avec médiateur vs valeur vraie')\n",
        "ax.legend(loc='lower right')\n",
        "fig.savefig('figures/sc2_coeff.png', dpi=150, bbox_inches='tight')\n",
        "plt.show()"
    ]
}

# Cell 5 — code-sc2-bar
cell_bar = {
    "cell_type": "code",
    "execution_count": None,
    "metadata": {},
    "outputs": [],
    "source": [
        "# ─────────────────────────────────────────────\n",
        "# Figure bar chart — Scénario 2\n",
        "# Sans médiateur (rouge, correct) vs Avec médiateur (bleu, biaisé) vs ATT (vert)\n",
        "# ─────────────────────────────────────────────\n",
        "\n",
        "fig, ax = plt.subplots(figsize=(7, 4))\n",
        "labels_sc2 = ['OLS sans médiateur', 'OLS avec panier_moyen', 'Valeur vraie (ATT)']\n",
        "values_sc2 = [coef_naive_sc2, coef_med_sc2, att_sc2_log]\n",
        "colors_sc2 = ['#e74c3c', '#3498db', '#2ecc71']\n",
        "\n",
        "ax.bar(range(len(labels_sc2)), values_sc2, color=colors_sc2, width=0.5)\n",
        "ax.set_xticks(range(len(labels_sc2)))\n",
        "ax.set_xticklabels(labels_sc2)\n",
        "ax.set_ylabel('Uplift log des ventes (≈ %)')\n",
        "ax.set_title('Scénario 2 — Comparaison des estimateurs')\n",
        "ax.axhline(y=att_sc2_log, color='gray', linestyle='--', alpha=0.5)\n",
        "fig.savefig('figures/sc2_bar.png', dpi=150, bbox_inches='tight')\n",
        "plt.show()"
    ]
}

# Insert the 5 cells after index 30 (append to end)
new_cells = [cell_md, cell_data, cell_dag, cell_coeff, cell_bar]
nb['cells'] = nb['cells'] + new_cells

print(f"After insertion: {len(nb['cells'])} cells")

with open('formation_causalite.ipynb', 'w') as f:
    json.dump(nb, f, indent=1, ensure_ascii=False)

print("Done — notebook saved.")
