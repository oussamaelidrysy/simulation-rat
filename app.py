import streamlit as st
import matplotlib.pyplot as plt
import matplotlib.ticker as mticker
import pandas as pd
import numpy as np
import main

# ─────────────────────────────────────────────
#  CONFIG PAGE
# ─────────────────────────────────────────────
st.set_page_config(
    page_title="Simulation Retraites",
    page_icon="📊",
    layout="wide",
)

# ─────────────────────────────────────────────
#  CSS PERSONNALISÉ
# ─────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Outfit:wght@300;400;500;600;700&family=Inter:wght@300;400;500;600;700&family=JetBrains+Mono:wght@400;500&display=swap');

html, body, [class*="css"] {
    font-family: 'Inter', sans-serif;
}
h1, h2, h3, h4 {
    font-family: 'Outfit', sans-serif;
    font-weight: 700;
    letter-spacing: -0.5px;
    color: #0f172a;
}
code, .stDataFrame, pre {
    font-family: 'JetBrains Mono', monospace !important;
}

/* ── Layout global ── */
.block-container {
    padding-top: 1.5rem !important;
    padding-bottom: 2rem !important;
    max-width: 1350px !important;
}

/* ── Sidebar ── */
[data-testid="stSidebar"] {
    background-color: #f8fafc !important;
    border-right: 1px solid #e2e8f0;
}

/* ── Header ── */
.app-header {
    background: linear-gradient(135deg, #6366f1 0%, #4f46e5 100%);
    padding: 2.2rem 2.5rem;
    border-radius: 16px;
    margin-bottom: 2.5rem;
    color: #ffffff;
    box-shadow: 0 10px 15px -3px rgba(99, 102, 241, 0.1), 0 4px 6px -2px rgba(99, 102, 241, 0.05);
    position: relative;
    overflow: hidden;
}
.app-header::before {
    content: '';
    position: absolute;
    top: -50%;
    right: -20%;
    width: 350px;
    height: 350px;
    border-radius: 50%;
    background: radial-gradient(circle, rgba(255, 255, 255, 0.15) 0%, transparent 60%);
    pointer-events: none;
}
.app-header-icon {
    font-size: 2.5rem;
    background: rgba(255, 255, 255, 0.2);
    width: 55px;
    height: 55px;
    display: flex;
    align-items: center;
    justify-content: center;
    border-radius: 12px;
    backdrop-filter: blur(10px);
    margin-bottom: 0.75rem;
}
.app-header-text h1 {
    color: #ffffff !important;
    font-size: 1.85rem;
    margin: 0 0 0.3rem 0;
    font-weight: 700;
}
.app-header-text p {
    color: #e0e7ff;
    margin: 0;
    font-size: 0.95rem;
    opacity: 0.9;
}
.app-header-meta {
    margin-top: 1rem;
    display: flex;
    gap: 0.5rem;
}
.meta-chip {
    background: rgba(255, 255, 255, 0.15);
    color: #ffffff;
    border: 1px solid rgba(255, 255, 255, 0.2);
    border-radius: 8px;
    padding: 0.3rem 0.75rem;
    font-size: 0.78rem;
    font-weight: 500;
}

/* ── Étapes ── */
.step-header {
    display: flex;
    align-items: center;
    gap: 0.75rem;
    margin: 1.5rem 0 1rem 0;
}
.step-number {
    width: 30px;
    height: 30px;
    border-radius: 8px;
    background: #6366f1;
    color: #ffffff;
    font-size: 0.82rem;
    font-weight: 600;
    display: flex;
    align-items: center;
    justify-content: center;
    flex-shrink: 0;
    box-shadow: 0 4px 6px -1px rgba(99, 102, 241, 0.2);
}
.step-label {
    font-size: 1.05rem;
    font-weight: 600;
    color: #0f172a;
}

/* ── Paramètres ── */
.param-card {
    background: #ffffff;
    border: 1px solid #e2e8f0;
    border-radius: 12px;
    padding: 1.25rem 1.5rem;
    margin-bottom: 1.25rem;
    box-shadow: 0 1px 3px rgba(0,0,0,0.05);
}
.param-card-title {
    font-size: 0.78rem;
    font-weight: 600;
    text-transform: uppercase;
    letter-spacing: 0.05em;
    color: #4f46e5;
    margin-bottom: 0.75rem;
}

/* ── KPI Cards ── */
.kpi-card {
    background: #ffffff;
    border: 1px solid #e2e8f0;
    border-radius: 14px;
    padding: 1.5rem;
    box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.05), 0 2px 4px -1px rgba(0, 0, 0, 0.03);
    transition: transform 0.2s ease, box-shadow 0.2s ease;
    flex: 1;
    margin-bottom: 1rem;
}
.kpi-card:hover {
    transform: translateY(-2px);
    box-shadow: 0 10px 15px -3px rgba(0, 0, 0, 0.05), 0 4px 6px -2px rgba(0, 0, 0, 0.05);
    border-color: #cbd5e1;
}
.kpi-label {
    font-size: 0.75rem;
    font-weight: 600;
    text-transform: uppercase;
    letter-spacing: 0.05em;
    color: #64748b;
    margin-bottom: 0.5rem;
}
.kpi-value {
    font-size: 1.65rem;
    font-weight: 700;
    color: #0f172a;
    line-height: 1.1;
    margin-bottom: 0.5rem;
    font-family: 'Outfit', sans-serif;
}
.kpi-badge {
    display: inline-flex;
    align-items: center;
    gap: 0.25rem;
    padding: 0.2rem 0.5rem;
    border-radius: 6px;
    font-size: 0.75rem;
    font-weight: 600;
}
.kpi-badge-purple {
    background-color: #faf5ff;
    color: #7c3aed;
}
.kpi-badge-blue {
    background-color: #eff6ff;
    color: #2563eb;
}
.kpi-badge-red {
    background-color: #fef2f2;
    color: #dc2626;
}

/* ── Badges scénario ── */
.sc-badge {
    display: inline-flex;
    align-items: center;
    gap: 0.35rem;
    padding: 0.35rem 0.85rem;
    border-radius: 8px;
    font-size: 0.8rem;
    font-weight: 600;
}
.sc-badge-1 {
    background: #e0e7ff;
    color: #3730a3;
    border: 1px solid #c7d2fe;
}
.sc-badge-2 {
    background: #dcfce7;
    color: #166534;
    border: 1px solid #bbf7d0;
}
.sc-badge-sim {
    background: #fefce8;
    color: #854d0e;
    border: 1px solid #fef08a;
}

/* ── Séparateur ── */
.divider {
    height: 1px;
    background: #e2e8f0;
    margin: 2rem 0;
    border: none;
}

/* ── Info banner résultats ── */
.result-header {
    display: flex;
    align-items: center;
    gap: 0.75rem;
    padding: 1.25rem 1.5rem;
    background: #f8fafc;
    border: 1px solid #e2e8f0;
    border-radius: 12px;
    margin-bottom: 1.5rem;
}
.result-dot {
    width: 10px;
    height: 10px;
    border-radius: 50%;
    background: #10b981;
    box-shadow: 0 0 0 4px #dcfce7;
}
.result-title {
    font-size: 1.05rem;
    font-weight: 600;
    color: #0f172a;
    margin: 0;
}
.result-sub {
    font-size: 0.85rem;
    color: #64748b;
    margin: 0;
}

/* ── Tableau ── */
.stDataFrame {
    border-radius: 10px !important;
    border: 1px solid #e2e8f0 !important;
    box-shadow: 0 1px 3px rgba(0,0,0,0.02);
}

/* ── Bouton principal ── */
.stButton > button[kind="primary"] {
    background: linear-gradient(135deg, #6366f1 0%, #4f46e5 100%) !important;
    color: #ffffff !important;
    border: none !important;
    border-radius: 10px !important;
    padding: 0.6rem 1.8rem !important;
    font-weight: 600 !important;
    font-size: 0.9rem !important;
    box-shadow: 0 4px 6px -1px rgba(99, 102, 241, 0.25) !important;
    transition: all 0.2s ease !important;
}
.stButton > button[kind="primary"]:hover {
    transform: translateY(-1px) !important;
    box-shadow: 0 6px 12px -1px rgba(99, 102, 241, 0.35) !important;
}

/* ── Secondary Button styling ── */
.stButton > button {
    border-radius: 10px !important;
    transition: all 0.2s ease !important;
}

/* ── Tabs ── */
.stTabs [data-baseweb="tab-list"] {
    gap: 0.75rem;
    border-bottom: 2px solid #f1f5f9;
}
.stTabs [data-baseweb="tab"] {
    font-size: 0.9rem !important;
    font-weight: 600 !important;
    padding: 0.5rem 1.2rem !important;
    color: #64748b !important;
    border-bottom: 2px solid transparent !important;
}
.stTabs [aria-selected="true"] {
    color: #4f46e5 !important;
    border-bottom: 2px solid #4f46e5 !important;
}

/* ── Radio ── */
.stRadio label {
    font-size: 0.9rem !important;
    color: #334155 !important;
}

/* ── Number input ── */
.stNumberInput label {
    font-size: 0.82rem !important;
    font-weight: 500 !important;
    color: #475569 !important;
}
.stNumberInput input {
    font-family: 'JetBrains Mono', monospace !important;
    font-size: 0.9rem !important;
    border-radius: 7px !important;
    border: 1px solid #e2e8f0 !important;
}

/* ── Selectbox ── */
.stSelectbox label {
    font-size: 0.82rem !important;
    font-weight: 500 !important;
    color: #475569 !important;
}

/* ── Caption ── */
.stCaption {
    color: #94a3b8 !important;
    font-size: 0.78rem !important;
}

/* ── Spinner ── */
.stSpinner p {
    font-size: 0.85rem !important;
    color: #64748b !important;
}
</style>
""", unsafe_allow_html=True)


# ─────────────────────────────────────────────
#  HELPERS GRAPHIQUES
# ─────────────────────────────────────────────

COULEURS = {
    "s1_primary":   "#6366f1",
    "s1_secondary": "#a5b4fc",
    "s2_primary":   "#10b981",
    "s2_secondary": "#6ee7b7",
    "cotis":        "#f59e0b",
    "pens":         "#ef4444",
    "reserve":      "#8b5cf6",
}

def formatter_dh(x, _):
    if abs(x) >= 1_000_000:
        return f"{x/1_000_000:.1f}M"
    if abs(x) >= 1_000:
        return f"{x/1_000:.0f}K"
    return f"{x:.0f}"

def formatter_mdh(x, _):
    return f"{x:.2f}M"

def style_fig(fig):
    for ax in fig.get_axes():
        ax.spines["top"].set_visible(False)
        ax.spines["right"].set_visible(False)
        ax.spines["left"].set_color("#cbd5e1")
        ax.spines["bottom"].set_color("#cbd5e1")
        ax.tick_params(colors="#64748b", labelsize=9)
        ax.yaxis.label.set_color("#475569")
        ax.xaxis.label.set_color("#475569")
        ax.title.set_color("#0f172a")
        ax.title.set_fontsize(12)
        ax.title.set_fontweight("600")
        ax.set_facecolor("#f8fafc")
        ax.grid(axis="y", color="#e2e8f0", linewidth=0.8, linestyle=":")
    fig.patch.set_facecolor("white")
    return fig

def graphiques_simulation_unique(bilan: pd.DataFrame, scenario: int):
    annees = bilan["Année"].to_numpy()
    c  = COULEURS["s1_primary"]   if scenario == 1 else COULEURS["s2_primary"]
    c2 = COULEURS["s1_secondary"] if scenario == 1 else COULEURS["s2_secondary"]

    fig, axes = plt.subplots(2, 3, figsize=(18, 8))
    fig.suptitle(
        f"Évolution des indicateurs — Scénario {scenario}",
        fontsize=13, fontweight="600", color="#0f172a", y=1.01,
        fontfamily="DejaVu Sans",
    )

    # Graphique 1 — Effectifs totaux
    ax = axes[0, 0]
    ax.plot(annees, bilan["TotEmp"].to_numpy(), color=c, linewidth=2, marker="o", markersize=4, label="Employés")
    ax.plot(annees, bilan["TotRet"].to_numpy(), color=COULEURS["pens"], linewidth=2, marker="s", markersize=4, linestyle="--", label="Retraités")
    ax.set_title("Effectifs totaux")
    ax.legend(fontsize=8, framealpha=0.6, edgecolor="#e2e8f0")
    ax.set_xticks(annees)

    # Graphique 2 — Cotisations vs Pensions
    ax = axes[0, 1]
    width = 0.35
    x = np.arange(len(annees))
    ax.bar(x - width/2, bilan["TotCotis"].to_numpy(), width, color=COULEURS["cotis"], label="Cotisations", alpha=0.85, linewidth=0)
    ax.bar(x + width/2, bilan["TotPens"].to_numpy(),  width, color=COULEURS["pens"],  label="Pensions",   alpha=0.85, linewidth=0)
    ax.set_title("Cotisations vs Pensions (dh)")
    ax.set_xticks(x); ax.set_xticklabels(annees, rotation=45, ha="right")
    ax.yaxis.set_major_formatter(mticker.FuncFormatter(formatter_dh))
    ax.legend(fontsize=8, framealpha=0.6, edgecolor="#e2e8f0")

    # Graphique 3 — Réserve
    ax = axes[0, 2]
    ax.fill_between(annees, bilan["Reserve"].to_numpy(), alpha=0.12, color=COULEURS["reserve"])
    ax.plot(annees, bilan["Reserve"].to_numpy(), color=COULEURS["reserve"], linewidth=2, marker="D", markersize=4)
    ax.set_title("Évolution de la réserve (dh)")
    ax.yaxis.set_major_formatter(mticker.FuncFormatter(formatter_dh))
    ax.set_xticks(annees)

    # Graphique 4 — Flux annuels
    ax = axes[1, 0]
    ax.plot(annees, bilan["NouvRet"].to_numpy(), color=COULEURS["pens"], linewidth=2, marker="o", markersize=4, label="Nouveaux retraités")
    ax.plot(annees, bilan["NouvRec"].to_numpy(), color=c2,               linewidth=2, marker="s", markersize=4, linestyle="--", label="Recrutements")
    ax.set_title("Flux annuels")
    ax.legend(fontsize=8, framealpha=0.6, edgecolor="#e2e8f0")
    ax.set_xticks(annees)

    # Graphique 5 — Plus de 63 ans (scénario 2 uniquement)
    if scenario == 2:
        ax = axes[1, 1]
        ax.plot(annees, bilan["Plus63"].to_numpy(),  color=c,                    linewidth=2, marker="o", markersize=4, label="Total +63 ans")
        ax.plot(annees, bilan["Plus63H"].to_numpy(), color=COULEURS["s1_primary"], linewidth=2, marker="s", markersize=4, linestyle="--", label="Hommes +63 ans")
        ax.plot(annees, bilan["Plus63F"].to_numpy(), color=COULEURS["pens"],       linewidth=2, marker="^", markersize=4, linestyle=":",  label="Femmes +63 ans")
        ax.set_title("Salariés de plus de 63 ans")
        ax.legend(fontsize=8, framealpha=0.6, edgecolor="#e2e8f0")
        ax.set_xticks(annees)
        # Masquer la 6e case inutilisée
        axes[1, 2].set_visible(False)
    else:
        # Scénario 1 : masquer les deux cases inutilisées
        axes[1, 1].set_visible(False)
        axes[1, 2].set_visible(False)

    plt.tight_layout()
    return style_fig(fig)


def graphiques_40_simulations(bilan_2026, bilan_2030, bilan_2035, bilan_reserve, scenario: int):
    c = COULEURS["s1_primary"] if scenario == 1 else COULEURS["s2_primary"]
    annees = [int(col.split("_")[1]) for col in bilan_reserve.columns]
    sims = bilan_reserve.drop(index="Moyenne", errors="ignore")

    fig, axes = plt.subplots(2, 2, figsize=(13, 8))
    fig.suptitle(
        f"Résultats sur 40 simulations — Scénario {scenario}",
        fontsize=13, fontweight="600", color="#0f172a", y=1.01,
    )

    ax = axes[0, 0]
    for _, row in sims.iterrows():
        ax.plot(annees, row.values, color=c, alpha=0.15, linewidth=0.8)
    moy = bilan_reserve.loc["Moyenne"]
    ax.plot(annees, moy.values, color=COULEURS["reserve"], linewidth=2.5, label="Moyenne", zorder=5)
    ax.set_title("Trajectoires de la réserve")
    ax.yaxis.set_major_formatter(mticker.FuncFormatter(formatter_dh))
    ax.legend(fontsize=8, framealpha=0.6, edgecolor="#e2e8f0")
    ax.set_xticks(annees)

    ax = axes[0, 1]
    for df_ann, label, col in [(bilan_2026, "2026", "#93c5fd"), (bilan_2030, "2030", c), (bilan_2035, "2035", "#1e3a5f")]:
        vals = df_ann.drop(index="Moyenne", errors="ignore")["TotEmp"].dropna().astype(float)
        ax.hist(vals, bins=10, alpha=0.65, label=label, color=col, linewidth=0)
    ax.set_title("Distribution TotEmp (2026 / 2030 / 2035)")
    ax.legend(fontsize=8, framealpha=0.6, edgecolor="#e2e8f0")

    ax = axes[1, 0]
    data_box = [sims[col].dropna().astype(float).values for col in sims.columns]
    bp = ax.boxplot(data_box, patch_artist=True, medianprops=dict(color="white", linewidth=2),
                    whiskerprops=dict(color="#94a3b8"), capprops=dict(color="#94a3b8"),
                    flierprops=dict(marker="o", color=c, alpha=0.4, markersize=3))
    for patch in bp["boxes"]:
        patch.set_facecolor(c)
        patch.set_alpha(0.7)
        patch.set_linewidth(0)
    ax.set_xticklabels(annees, rotation=45, ha="right")
    ax.set_title("Distribution de la réserve par année")
    ax.yaxis.set_major_formatter(mticker.FuncFormatter(formatter_dh))

    ax = axes[1, 1]
    labels_ann = ["2026", "2030", "2035"]
    cotis_moy = [
        bilan_2026.drop(index="Moyenne", errors="ignore")["TotCotis"].astype(float).mean(),
        bilan_2030.drop(index="Moyenne", errors="ignore")["TotCotis"].astype(float).mean(),
        bilan_2035.drop(index="Moyenne", errors="ignore")["TotCotis"].astype(float).mean(),
    ]
    pens_moy = [
        bilan_2026.drop(index="Moyenne", errors="ignore")["TotPens"].astype(float).mean(),
        bilan_2030.drop(index="Moyenne", errors="ignore")["TotPens"].astype(float).mean(),
        bilan_2035.drop(index="Moyenne", errors="ignore")["TotPens"].astype(float).mean(),
    ]
    x = np.arange(3); w = 0.35
    ax.bar(x - w/2, cotis_moy, w, color=COULEURS["cotis"], label="Cotisations moy.", alpha=0.85, linewidth=0)
    ax.bar(x + w/2, pens_moy,  w, color=COULEURS["pens"],  label="Pensions moy.",   alpha=0.85, linewidth=0)
    ax.set_xticks(x); ax.set_xticklabels(labels_ann)
    ax.yaxis.set_major_formatter(mticker.FuncFormatter(formatter_dh))
    ax.set_title("Cotisations vs Pensions moyennes")
    ax.legend(fontsize=8, framealpha=0.6, edgecolor="#e2e8f0")

    plt.tight_layout()
    return style_fig(fig)


def graphiques_croises(res1, res2):
    bilan_2026_1, bilan_2030_1, bilan_2035_1, bres1 = res1
    bilan_2026_2, bilan_2030_2, bilan_2035_2, bres2 = res2

    annees = [int(col.split("_")[1]) for col in bres1.columns]
    sims1 = bres1.drop(index="Moyenne", errors="ignore")
    sims2 = bres2.drop(index="Moyenne", errors="ignore")

    fig, axes = plt.subplots(2, 3, figsize=(16, 9))
    fig.suptitle(
        "Comparaison Scénario 1 vs Scénario 2 — 40 simulations",
        fontsize=13, fontweight="600", color="#0f172a", y=1.01,
    )

    ax = axes[0, 0]
    for _, row in sims1.iterrows():
        ax.plot(annees, row.values, color=COULEURS["s1_primary"], alpha=0.12, linewidth=0.7)
    for _, row in sims2.iterrows():
        ax.plot(annees, row.values, color=COULEURS["s2_primary"], alpha=0.12, linewidth=0.7)
    ax.plot(annees, bres1.loc["Moyenne"].values, color=COULEURS["s1_primary"], linewidth=2.5, label="S1 moy.")
    ax.plot(annees, bres2.loc["Moyenne"].values, color=COULEURS["s2_primary"], linewidth=2.5, label="S2 moy.")
    ax.set_title("Trajectoires réserve")
    ax.yaxis.set_major_formatter(mticker.FuncFormatter(formatter_dh))
    ax.legend(fontsize=8, framealpha=0.6, edgecolor="#e2e8f0")
    ax.set_xticks(annees)

    ax = axes[0, 1]
    data1 = sims1["Reserve_2035"].dropna().astype(float).values
    data2 = sims2["Reserve_2035"].dropna().astype(float).values
    bp = ax.boxplot([data1, data2], patch_artist=True,
                    medianprops=dict(color="white", linewidth=2),
                    whiskerprops=dict(color="#94a3b8"), capprops=dict(color="#94a3b8"),
                    flierprops=dict(marker="o", alpha=0.4, markersize=3))
    colors = [COULEURS["s1_primary"], COULEURS["s2_primary"]]
    for patch, col in zip(bp["boxes"], colors):
        patch.set_facecolor(col); patch.set_alpha(0.75); patch.set_linewidth(0)
    ax.set_xticklabels(["Scénario 1", "Scénario 2"])
    ax.set_title("Distribution réserve 2035")
    ax.yaxis.set_major_formatter(mticker.FuncFormatter(formatter_dh))

    ax = axes[0, 2]
    ann_labels = ["2026", "2030", "2035"]
    emp_s1 = [b.drop(index="Moyenne", errors="ignore")["TotEmp"].astype(float).mean() for b in [bilan_2026_1, bilan_2030_1, bilan_2035_1]]
    emp_s2 = [b.drop(index="Moyenne", errors="ignore")["TotEmp"].astype(float).mean() for b in [bilan_2026_2, bilan_2030_2, bilan_2035_2]]
    x = np.arange(3); w = 0.35
    ax.bar(x - w/2, emp_s1, w, color=COULEURS["s1_primary"], label="S1", alpha=0.85, linewidth=0)
    ax.bar(x + w/2, emp_s2, w, color=COULEURS["s2_primary"], label="S2", alpha=0.85, linewidth=0)
    ax.set_xticks(x); ax.set_xticklabels(ann_labels)
    ax.set_title("Employés totaux moyens")
    ax.legend(fontsize=8, framealpha=0.6, edgecolor="#e2e8f0")

    ax = axes[1, 0]
    ret_s1 = [b.drop(index="Moyenne", errors="ignore")["TotRet"].astype(float).mean() for b in [bilan_2026_1, bilan_2030_1, bilan_2035_1]]
    ret_s2 = [b.drop(index="Moyenne", errors="ignore")["TotRet"].astype(float).mean() for b in [bilan_2026_2, bilan_2030_2, bilan_2035_2]]
    ax.plot(ann_labels, ret_s1, color=COULEURS["s1_primary"], marker="o", markersize=5, linewidth=2.5, label="S1")
    ax.plot(ann_labels, ret_s2, color=COULEURS["s2_primary"], marker="s", markersize=5, linewidth=2.5, label="S2")
    ax.set_title("Retraités totaux moyens")
    ax.legend(fontsize=8, framealpha=0.6, edgecolor="#e2e8f0")

    ax = axes[1, 1]
    cotis_s1 = [b.drop(index="Moyenne", errors="ignore")["TotCotis"].astype(float).mean() for b in [bilan_2026_1, bilan_2030_1, bilan_2035_1]]
    cotis_s2 = [b.drop(index="Moyenne", errors="ignore")["TotCotis"].astype(float).mean() for b in [bilan_2026_2, bilan_2030_2, bilan_2035_2]]
    ax.bar(x - w/2, cotis_s1, w, color=COULEURS["s1_primary"], label="S1", alpha=0.85, linewidth=0)
    ax.bar(x + w/2, cotis_s2, w, color=COULEURS["s2_primary"], label="S2", alpha=0.85, linewidth=0)
    ax.set_xticks(x); ax.set_xticklabels(ann_labels)
    ax.yaxis.set_major_formatter(mticker.FuncFormatter(formatter_dh))
    ax.set_title("Cotisations totales moyennes")
    ax.legend(fontsize=8, framealpha=0.6, edgecolor="#e2e8f0")

    ax = axes[1, 2]
    pens_s1 = [b.drop(index="Moyenne", errors="ignore")["TotPens"].astype(float).mean() for b in [bilan_2026_1, bilan_2030_1, bilan_2035_1]]
    pens_s2 = [b.drop(index="Moyenne", errors="ignore")["TotPens"].astype(float).mean() for b in [bilan_2026_2, bilan_2030_2, bilan_2035_2]]
    ax.bar(x - w/2, pens_s1, w, color=COULEURS["s1_primary"], label="S1", alpha=0.85, linewidth=0)
    ax.bar(x + w/2, pens_s2, w, color=COULEURS["s2_primary"], label="S2", alpha=0.85, linewidth=0)
    ax.set_xticks(x); ax.set_xticklabels(ann_labels)
    ax.yaxis.set_major_formatter(mticker.FuncFormatter(formatter_dh))
    ax.set_title("Pensions totales moyennes")
    ax.legend(fontsize=8, framealpha=0.6, edgecolor="#e2e8f0")

    plt.tight_layout()
    return style_fig(fig)


# ─────────────────────────────────────────────
#  HELPERS UI
# ─────────────────────────────────────────────

def step_header(n: int, label: str):
    st.markdown(
        f'<div class="step-header">'
        f'<div class="step-number">{n}</div>'
        f'<span class="step-label">{label}</span>'
        f'</div>',
        unsafe_allow_html=True,
    )

def sc_badge(scenario: int, text: str = None) -> str:
    label = text or f"Scénario {scenario}"
    return f'<span class="sc-badge sc-badge-{scenario}">{label}</span>'

def divider():
    st.markdown('<hr class="divider">', unsafe_allow_html=True)

def result_banner(title: str, sub: str = ""):
    sub_html = f'<p class="result-sub">{sub}</p>' if sub else ""
    st.markdown(
        f'<div class="result-header">'
        f'<div class="result-dot"></div>'
        f'<div><p class="result-title">{title}</p>{sub_html}</div>'
        f'</div>',
        unsafe_allow_html=True,
    )

def afficher_kpis_unique(bilan):
    final_row = bilan.iloc[-1]
    res_2035 = final_row["Reserve"]
    cotis_2035 = final_row["TotCotis"]
    pens_2035 = final_row["TotPens"]
    emp_2035 = final_row["TotEmp"]
    ret_2035 = final_row["TotRet"]
    
    ratio = (cotis_2035 / pens_2035 * 100) if pens_2035 > 0 else 0
    
    col1, col2, col3 = st.columns(3)
    with col1:
        st.markdown(f"""
        <div class="kpi-card">
            <div class="kpi-label">Réserve Finale (2035)</div>
            <div class="kpi-value">{res_2035:,.3f} Mdh</div>
            <div class="kpi-badge kpi-badge-purple">💰 Solde de réserve</div>
        </div>
        """, unsafe_allow_html=True)
    with col2:
        st.markdown(f"""
        <div class="kpi-card">
            <div class="kpi-label">Taux de Couverture (2035)</div>
            <div class="kpi-value">{ratio:.1f}%</div>
            <div class="kpi-badge kpi-badge-blue">📈 Cotisations / Pensions</div>
        </div>
        """, unsafe_allow_html=True)
    with col3:
        st.markdown(f"""
        <div class="kpi-card">
            <div class="kpi-label">Rapport Actifs / Inactifs</div>
            <div class="kpi-value">{int(emp_2035):,} / {int(ret_2035):,}</div>
            <div class="kpi-badge kpi-badge-red">👥 Employés / Retraités</div>
        </div>
        """, unsafe_allow_html=True)

def afficher_kpis_multi(bilan_2035):
    moyenne = bilan_2035.loc["Moyenne"]
    res_2035 = moyenne["Reserve"]
    cotis_2035 = moyenne["TotCotis"]
    pens_2035 = moyenne["TotPens"]
    emp_2035 = moyenne["TotEmp"]
    ret_2035 = moyenne["TotRet"]
    
    ratio = (cotis_2035 / pens_2035 * 100) if pens_2035 > 0 else 0
    
    col1, col2, col3 = st.columns(3)
    with col1:
        st.markdown(f"""
        <div class="kpi-card">
            <div class="kpi-label">Réserve Moyenne (2035)</div>
            <div class="kpi-value">{res_2035:,.3f} Mdh</div>
            <div class="kpi-badge kpi-badge-purple">💰 Moyenne des simulations</div>
        </div>
        """, unsafe_allow_html=True)
    with col2:
        st.markdown(f"""
        <div class="kpi-card">
            <div class="kpi-label">Taux de Couverture (2035)</div>
            <div class="kpi-value">{ratio:.1f}%</div>
            <div class="kpi-badge kpi-badge-blue">📈 Cotisations / Pensions</div>
        </div>
        """, unsafe_allow_html=True)
    with col3:
        st.markdown(f"""
        <div class="kpi-card">
            <div class="kpi-label">Effectifs Moyens (2035)</div>
            <div class="kpi-value">{int(emp_2035):,} / {int(ret_2035):,}</div>
            <div class="kpi-badge kpi-badge-red">👥 Employés / Retraités</div>
        </div>
        """, unsafe_allow_html=True)


# ─────────────────────────────────────────────
#  AFFICHAGE BILANS MULTI-SIMULATIONS
# ─────────────────────────────────────────────

def afficher_bilans_multi(bilan_2026, bilan_2030, bilan_2035, bilan_reserve, scenario: int):
    st.markdown(
        f'<p style="margin:0 0 0.9rem;font-size:0.85rem;color:#64748b;">'
        f'{sc_badge(scenario)} Résumé des indicateurs clés (Valeurs Moyennes en 2035)</p>',
        unsafe_allow_html=True,
    )
    
    # Rendre les cartes de KPIs
    afficher_kpis_multi(bilan_2035)
    st.markdown("")

    st.markdown(
        f'<p style="margin:0.5rem 0 0.9rem;font-size:0.85rem;color:#64748b;">'
        f'{sc_badge(scenario)} Bilans par année de référence</p>',
        unsafe_allow_html=True,
    )

    MONEY_COLS   = ["TotCotis", "TotPens", "Reserve"]
    RESERVE_COLS = [c for c in bilan_reserve.columns if c.startswith("Reserve_")]

    def prep(df):
        def fmt_index(val):
            try:
                i = float(val)
                return str(int(i)) if i == int(i) else str(val)
            except (ValueError, TypeError):
                return str(val)
        df = df.copy()
        df.index = [fmt_index(v) for v in df.index]
        return df

    def fmt(df, extra_money_cols=None):
        cols = MONEY_COLS + (extra_money_cols or [])
        return {c: "{:,.3f} Mdh" for c in cols if c in df.columns}

    tab1, tab2, tab3, tab4 = st.tabs(["2026", "2030", "2035", "Réserve 2026 → 2035"])
    with tab1:
        df = prep(bilan_2026)
        st.dataframe(df.style.format(fmt(df), na_rep="—"), use_container_width=True)
    with tab2:
        df = prep(bilan_2030)
        st.dataframe(df.style.format(fmt(df), na_rep="—"), use_container_width=True)
    with tab3:
        df = prep(bilan_2035)
        st.dataframe(df.style.format(fmt(df), na_rep="—"), use_container_width=True)
    with tab4:
        df = prep(bilan_reserve)
        st.dataframe(df.style.format(fmt(df, RESERVE_COLS), na_rep="—"), use_container_width=True)

    divider()
    st.markdown(
        f'<p style="margin:0 0 0.9rem;font-size:0.85rem;color:#64748b;">'
        f'{sc_badge(scenario)} Graphiques</p>',
        unsafe_allow_html=True,
    )
    fig = graphiques_40_simulations(bilan_2026, bilan_2030, bilan_2035, bilan_reserve, scenario)
    st.pyplot(fig, use_container_width=True)

    # ── Tableau des intervalles de confiance ──────────────────────────────
    st.markdown("**Intervalles de confiance de la réserve**")
    annees_ref = [2026, 2030, 2035]
    cols_ref   = ["Reserve_2026", "Reserve_2030", "Reserve_2035"]
    sims = bilan_reserve.drop(index="Moyenne", errors="ignore")

    ic_data = []
    for annee, col in zip(annees_ref, cols_ref):
        vals    = sims[col].dropna().astype(float).values
        moyenne = vals.mean()
        std     = vals.std()
        n       = len(vals)
        ic_95   = 1.96  * std / np.sqrt(n)
        ic_data.append({
            "Année":         annee,
            "Moyenne (Mdh)": round(moyenne, 3),
            "Borne inf. 95% (Mdh)": round(moyenne - ic_95, 3),
            "Borne sup. 95% (Mdh)": round(moyenne + ic_95, 3),
        })

    df_ic = pd.DataFrame(ic_data).set_index("Année")
    st.dataframe(df_ic.style.format("{:,.3f}"), use_container_width=True)
    
    # ── Tableau IC Plus63 (scénario 2 uniquement) ─────────────────────────
    if scenario == 2:
        st.markdown("**Intervalles de confiance des salariés de plus de 63 ans**")
        ic_plus63 = []
        for annee, b in zip([2026, 2030, 2035], [bilan_2026, bilan_2030, bilan_2035]):
            sims_b = b.drop(index="Moyenne", errors="ignore")
            row = {"Année": annee}
            for col, label in [("Plus63", "Total"), ("Plus63H", "Hommes"), ("Plus63F", "Femmes")]:
                vals    = sims_b[col].dropna().astype(float).values
                moyenne = vals.mean()
                std     = vals.std()
                n       = len(vals)
                ic_95   = 1.96  * std / np.sqrt(n)
                row[f"{label} — Moyenne"]       = round(moyenne, 1)
                row[f"{label} — Inf. 95%"]      = round(moyenne - ic_95, 1)
                row[f"{label} — Sup. 95%"]      = round(moyenne + ic_95, 1)
            ic_plus63.append(row)

        df_ic_plus63 = pd.DataFrame(ic_plus63).set_index("Année")
        st.dataframe(df_ic_plus63.style.format("{:,.1f}"), use_container_width=True)


# ─────────────────────────────────────────────
#  INTERFACE PRINCIPALE
# ─────────────────────────────────────────────

# ── SIDEBAR CONFIGURATION ──────────────────────────────────────────────────
with st.sidebar:
    st.markdown("### ⚙️ Configuration")
    
    mode = st.radio(
        "Nombre de simulations",
        ["1 simulation", "40 simulations"],
    )
    
    st.markdown("---")
    
    if mode == "1 simulation":
        st.markdown("#### Germes aléatoires")
        col_ix, col_iy, col_iz = st.columns(3)
        IX_val = col_ix.number_input("IX", min_value=1, max_value=30000, value=100, step=1)
        IY_val = col_iy.number_input("IY", min_value=1, max_value=30000, value=200, step=1)
        IZ_val = col_iz.number_input("IZ", min_value=1, max_value=30000, value=300, step=1)
        
        st.markdown("---")
        scenario = st.selectbox(
            "Scénario à simuler",
            [1, 2],
            format_func=lambda x: f"Scénario {x}",
        )
        
        st.markdown("")
        lancer = st.button("Lancer la simulation", type="primary", use_container_width=True)
        
        if lancer:
            with st.spinner("Simulation en cours…"):
                bilan = main.scenario_1(main.GenerateurAlea(IX_val, IY_val, IZ_val)) if scenario == 1 else main.scenario_2(main.GenerateurAlea(IX_val, IY_val, IZ_val))
            st.session_state["bilan_unique"] = bilan
            st.session_state["scenario_unique"] = scenario
            # clear other mode cache
            if "choix_sc_40" in st.session_state:
                del st.session_state["choix_sc_40"]
                
    else:
        choix_sc = st.radio(
            "Scénario(s) à simuler",
            ["Scénario 1 uniquement", "Scénario 2 uniquement", "Les deux scénarios"],
        )
        
        st.markdown("---")
        st.markdown("#### Germes de départ")
        st.caption("Les germes sont incrémentés de 5 à chaque simulation")
        col_ix, col_iy, col_iz = st.columns(3)
        IX_val = col_ix.number_input("IX", min_value=1, max_value=29600, value=10, step=1, key="ix_40")
        IY_val = col_iy.number_input("IY", min_value=1, max_value=29600, value=13, step=1, key="iy_40")
        IZ_val = col_iz.number_input("IZ", min_value=1, max_value=29600, value=16, step=1, key="iz_40")
        
        st.markdown("")
        lancer = st.button("Lancer les 40 simulations", type="primary", use_container_width=True)
        
        if lancer:
            if choix_sc in ["Scénario 1 uniquement", "Les deux scénarios"]:
                with st.spinner("Simulation scénario 1 × 40…"):
                    res1 = main.n_fois_scenario_1(40, int(IX_val), int(IY_val), int(IZ_val))
                st.session_state["res1"] = res1
            
            if choix_sc in ["Scénario 2 uniquement", "Les deux scénarios"]:
                with st.spinner("Simulation scénario 2 × 40…"):
                    res2 = main.n_fois_scenario_2(40, int(IX_val), int(IY_val), int(IZ_val))
                st.session_state["res2"] = res2
                
            st.session_state["choix_sc_40"] = choix_sc
            # clear other mode cache
            if "bilan_unique" in st.session_state:
                del st.session_state["bilan_unique"]

# ── MAIN SECTION ───────────────────────────────────────────────────────────
st.markdown("""
<div class="app-header">
  <div class="app-header-icon">📊</div>
  <div class="app-header-text">
    <h1>Simulation discrète de la caisse de retraite</h1>
    <p>Modèle d'analyse et de projection prospective de l'évolution des réserves (2026 – 2035)</p>
  </div>
  <div class="app-header-meta">
    <span class="meta-chip">Horizon 2026 – 2035</span>
    <span class="meta-chip">v3.0 Premium</span>
  </div>
</div>
""", unsafe_allow_html=True)

if mode == "1 simulation":
    if "bilan_unique" in st.session_state:
        bilan = st.session_state["bilan_unique"]
        sc    = st.session_state["scenario_unique"]
        
        result_banner(
            f"Résultats de la simulation — Scénario {sc}",
            "Visualisation des indicateurs clés et de l'évolution temporelle",
        )
        
        # Display KPI cards
        afficher_kpis_unique(bilan)
        st.markdown("")
        
        # Show data table
        st.markdown("##### 📝 Données Annuelles Détaillées")
        money_cols = ["TotCotis", "TotPens", "Reserve"]
        fmt = {c: "{:,.3f} Mdh" for c in money_cols if c in bilan.columns}
        st.dataframe(
            bilan.style.format(fmt),
            use_container_width=True,
            hide_index=True,
        )
        
        divider()
        st.markdown("##### 📈 Graphiques d'Évolution")
        fig = graphiques_simulation_unique(bilan, sc)
        st.pyplot(fig, use_container_width=True)
    else:
        st.markdown("""
        <div style="text-align: center; padding: 5rem 2rem; background: #ffffff; border: 2px dashed #e2e8f0; border-radius: 16px; margin-top: 2rem;">
            <div style="font-size: 3.5rem; margin-bottom: 1rem;">📊</div>
            <h3 style="color: #0f172a; margin-bottom: 0.5rem;">Prêt pour la simulation unique</h3>
            <p style="color: #64748b; max-width: 450px; margin: 0 auto 1.5rem;">Configurez les germes aléatoires et le scénario souhaité dans la barre latérale gauche, puis cliquez sur <strong>Lancer la simulation</strong>.</p>
        </div>
        """, unsafe_allow_html=True)
else:
    if "choix_sc_40" in st.session_state:
        choix = st.session_state["choix_sc_40"]
        
        if choix == "Scénario 1 uniquement" and "res1" in st.session_state:
            result_banner("Résultats cumulés — Scénario 1", "Analyse sur 40 simulations discrètes")
            bilan_2026, bilan_2030, bilan_2035, bres = st.session_state["res1"]
            afficher_bilans_multi(bilan_2026, bilan_2030, bilan_2035, bres, scenario=1)
            
        elif choix == "Scénario 2 uniquement" and "res2" in st.session_state:
            result_banner("Résultats cumulés — Scénario 2", "Analyse sur 40 simulations discrètes")
            bilan_2026, bilan_2030, bilan_2035, bres = st.session_state["res2"]
            afficher_bilans_multi(bilan_2026, bilan_2030, bilan_2035, bres, scenario=2)
            
        elif choix == "Les deux scénarios" and "res1" in st.session_state and "res2" in st.session_state:
            result_banner(
                "Résultats Comparatifs — Scénarios 1 & 2",
                "Comparaison croisée des trajectoires de réserves et des indicateurs (40 simulations)",
            )
            
            with st.expander("🔍 Détails Scénario 1 (Moyennes & distributions)", expanded=False):
                bilan_2026, bilan_2030, bilan_2035, bres = st.session_state["res1"]
                afficher_bilans_multi(bilan_2026, bilan_2030, bilan_2035, bres, scenario=1)
                
            with st.expander("🔍 Détails Scénario 2 (Moyennes & distributions)", expanded=False):
                bilan_2026, bilan_2030, bilan_2035, bres = st.session_state["res2"]
                afficher_bilans_multi(bilan_2026, bilan_2030, bilan_2035, bres, scenario=2)
                
            divider()
            st.markdown("##### ⚖️ Comparaison croisée des scénarios")
            fig = graphiques_croises(st.session_state["res1"], st.session_state["res2"])
            st.pyplot(fig, use_container_width=True)
    else:
        st.markdown("""
        <div style="text-align: center; padding: 5rem 2rem; background: #ffffff; border: 2px dashed #e2e8f0; border-radius: 16px; margin-top: 2rem;">
            <div style="font-size: 3.5rem; margin-bottom: 1rem;">📈</div>
            <h3 style="color: #0f172a; margin-bottom: 0.5rem;">Prêt pour la simulation multiple</h3>
            <p style="color: #64748b; max-width: 450px; margin: 0 auto 1.5rem;">Déterminez les scénarios et les germes initiaux dans la barre latérale de gauche, puis cliquez sur <strong>Lancer les 40 simulations</strong> pour débuter l'analyse prospective.</p>
        </div>
        """, unsafe_allow_html=True)