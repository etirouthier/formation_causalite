import json
import uuid

with open('formation_causalite.ipynb') as f:
    nb = json.load(f)

def make_markdown_cell(source_lines):
    return {
        "cell_type": "markdown",
        "id": str(uuid.uuid4())[:8],
        "metadata": {},
        "source": source_lines
    }

def make_code_cell(source_lines):
    return {
        "cell_type": "code",
        "execution_count": None,
        "id": str(uuid.uuid4())[:8],
        "metadata": {},
        "outputs": [],
        "source": source_lines
    }

# Cell 1 — Markdown section 1c
cell_md_1c = make_markdown_cell([
    "## Scénario 1c — Biais de sélection par saison\n",
    "\n",
    "Le confondant `saison` détermine à la fois la probabilité de recevoir la pub (haute saison = plus de pub) et le niveau des ventes. L'assignation pub varie par mois (niveau ligne). Le modèle naïf omet les dummies de mois, rendant le biais saisonnier visible."
])

# Cell 2 — code-sc1c-data
cell_data_1c = make_code_cell([
    "# ─────────────────────────────────────────────\n",
    "# Scénario 1c — Sélection par saison\n",
    "# Confondant : effet_saison_val (via mois)\n",
    "# Assignation pub : niveau LIGNE (varie par mois) — différent de 1a/1b\n",
    "# ─────────────────────────────────────────────\n",
    "\n",
    "rng_sc1c = np.random.default_rng(SEED + 30)\n",
    "\n",
    "# Assignation pub au niveau ligne (4800 lignes) — haute saison = pub plus probable\n",
    "df_sc1c = base_df.copy()\n",
    "haute_mask = df_sc1c['effet_saison_val'] > 0\n",
    "probs_1c = np.where(haute_mask, P_PUB_HAUTE_SAISON, P_PUB_BASSE_SAISON)\n",
    "df_sc1c['pub'] = rng_sc1c.binomial(1, probs_1c)\n",
    "df_sc1c = compute_outcomes(df_sc1c, PARAMS, rng_sc1c)\n",
    "\n",
    "# Calcul ATT contrefactuel — traités = lignes avec pub=1 (pas des magasins)\n",
    "df_treated_1c = df_sc1c[df_sc1c['pub'] == 1].copy()\n",
    "rng_cf_1c = np.random.default_rng(SEED + 31)\n",
    "df_cf_1c = df_treated_1c.copy()\n",
    "df_cf_1c['pub'] = 0\n",
    "df_cf_1c = compute_outcomes(df_cf_1c, PARAMS, rng_cf_1c)\n",
    "att_1c = (df_treated_1c['ventes'].values - df_cf_1c['ventes'].values).mean()\n",
    "\n",
    "# OLS naïf : SANS C(mois) — pour rendre le biais saisonnier visible\n",
    "model_naive_1c = smf.ols('ventes ~ pub', data=df_sc1c).fit()\n",
    "# OLS ajusté : AVEC C(mois) — contrôle la saison\n",
    "model_adj_1c   = smf.ols('ventes ~ pub + C(mois)', data=df_sc1c).fit()\n",
    "\n",
    "# Export CSV\n",
    "df_sc1c.to_csv('data/sc1c_selection_saison.csv', index=False)\n",
    "print(f\"Sc1c — Lignes pub=1 : {df_sc1c['pub'].sum()}/4800\")\n",
    "print(f\"Sc1c — ATT: {att_1c:.1f} €  |  OLS naïf (sans mois): {model_naive_1c.params['pub']:.1f} €  |  OLS ajusté (C(mois)): {model_adj_1c.params['pub']:.1f} €\")"
])

# Cell 3 — code-sc1c-dag
cell_dag_1c = make_code_cell([
    "# ─────────────────────────────────────────────\n",
    "# Figure DAG — Scénario 1c\n",
    "# ─────────────────────────────────────────────\n",
    "\n",
    "G_1c = nx.DiGraph()\n",
    "G_1c.add_edges_from([\n",
    "    ('Saison', 'Pub'),\n",
    "    ('Saison', 'Ventes'),\n",
    "    ('Pub', 'Ventes'),\n",
    "])\n",
    "pos_1c = {'Pub': (0, 0), 'Ventes': (2, 0), 'Saison': (1, 1)}\n",
    "\n",
    "color_map_1c = {'Pub': 'steelblue', 'Ventes': 'seagreen', 'Saison': 'darkorange'}\n",
    "node_colors_1c = [color_map_1c[n] for n in G_1c.nodes()]\n",
    "\n",
    "fig, ax = plt.subplots(figsize=(5, 3))\n",
    "nx.draw_networkx(G_1c, pos_1c, ax=ax,\n",
    "                 node_color=node_colors_1c,\n",
    "                 node_size=2000, font_size=9, font_color='white',\n",
    "                 arrows=True, arrowsize=20)\n",
    "ax.axis('off')\n",
    "ax.set_title('DAG — Scénario 1c : sélection par saison')\n",
    "fig.savefig('figures/sc1c_dag.png', dpi=150, bbox_inches='tight')\n",
    "plt.show()"
])

# Cell 4 — code-sc1c-coeff
cell_coeff_1c = make_code_cell([
    "# ─────────────────────────────────────────────\n",
    "# Figure coefficient plot — Scénario 1c\n",
    "# ─────────────────────────────────────────────\n",
    "\n",
    "coef_naive_1c = model_naive_1c.params['pub']\n",
    "ci_naive_1c   = model_naive_1c.conf_int()\n",
    "lower_naive_1c = ci_naive_1c.loc['pub', 0]\n",
    "upper_naive_1c = ci_naive_1c.loc['pub', 1]\n",
    "\n",
    "coef_adj_1c = model_adj_1c.params['pub']\n",
    "ci_adj_1c   = model_adj_1c.conf_int()\n",
    "lower_adj_1c = ci_adj_1c.loc['pub', 0]\n",
    "upper_adj_1c = ci_adj_1c.loc['pub', 1]\n",
    "\n",
    "xerr_naive_1c = [[coef_naive_1c - lower_naive_1c], [upper_naive_1c - coef_naive_1c]]\n",
    "xerr_adj_1c   = [[coef_adj_1c   - lower_adj_1c],   [upper_adj_1c   - coef_adj_1c]]\n",
    "\n",
    "estimators_1c = ['OLS naïf (sans mois)', 'OLS ajusté + C(mois)', 'Valeur vraie (ATT)']\n",
    "y_pos_1c = [2, 1, 0]\n",
    "\n",
    "fig, ax = plt.subplots(figsize=(8, 4))\n",
    "ax.errorbar(coef_naive_1c, 2, xerr=xerr_naive_1c, fmt='o', capsize=5,\n",
    "            color='#e74c3c', label='OLS naïf (sans mois)', markersize=8)\n",
    "ax.errorbar(coef_adj_1c, 1, xerr=xerr_adj_1c, fmt='o', capsize=5,\n",
    "            color='#3498db', label='OLS ajusté + C(mois)', markersize=8)\n",
    "ax.errorbar(att_1c, 0, fmt='D', color='#2ecc71', label='Valeur vraie (ATT)', markersize=10)\n",
    "ax.axvline(x=att_1c, color='gray', linestyle='--', alpha=0.5)\n",
    "ax.set_yticks(y_pos_1c)\n",
    "ax.set_yticklabels(estimators_1c)\n",
    "ax.set_xlabel('Effet estimé de la pub sur les ventes (€)')\n",
    "ax.set_title('Scénario 1c — Coefficients OLS naïf vs ajusté vs valeur vraie')\n",
    "ax.legend(loc='lower right')\n",
    "fig.savefig('figures/sc1c_coeff.png', dpi=150, bbox_inches='tight')\n",
    "plt.show()"
])

# Cell 5 — code-sc1c-bar
cell_bar_1c = make_code_cell([
    "# ─────────────────────────────────────────────\n",
    "# Figure bar chart — Scénario 1c\n",
    "# ─────────────────────────────────────────────\n",
    "\n",
    "fig, ax = plt.subplots(figsize=(7, 4))\n",
    "labels_1c = ['OLS naïf (sans mois)', 'OLS ajusté + C(mois)', 'Valeur vraie (ATT)']\n",
    "values_1c = [coef_naive_1c, coef_adj_1c, att_1c]\n",
    "colors_est_1c = ['#e74c3c', '#3498db', '#2ecc71']\n",
    "\n",
    "ax.bar(range(len(labels_1c)), values_1c, color=colors_est_1c, width=0.5)\n",
    "ax.set_xticks(range(len(labels_1c)))\n",
    "ax.set_xticklabels(labels_1c)\n",
    "ax.set_ylabel('Effet estimé de la pub sur les ventes (€)')\n",
    "ax.set_title('Scénario 1c — Comparaison des estimateurs')\n",
    "ax.axhline(y=att_1c, color='gray', linestyle='--', alpha=0.5)\n",
    "fig.savefig('figures/sc1c_bar.png', dpi=150, bbox_inches='tight')\n",
    "plt.show()"
])

# Append all 5 cells
nb['cells'].extend([cell_md_1c, cell_data_1c, cell_dag_1c, cell_coeff_1c, cell_bar_1c])

total = len(nb['cells'])
print(f'Total cells after insertion: {total}')

with open('formation_causalite.ipynb', 'w') as f:
    json.dump(nb, f, indent=1, ensure_ascii=False)

print('Notebook saved successfully.')
