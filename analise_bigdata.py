# Análise de ações da B3 para a Invest+ Corretora
# Disciplina: Big Data | Estácio de Sá — São José
# Aluno: Fabricio Raddatz Ribeiro Araujo
# Professor: Robson Lorbieski
# Repositório: https://github.com/Fabricioordtz/investmais-b3

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import warnings
warnings.filterwarnings("ignore")

# lendo o arquivo de dados
df_raw = pd.read_csv("dados/dados_b3.csv")

# separando as colunas de mês das colunas de informação
meses = [col for col in df_raw.columns if col not in ["Ticker", "Setor"]]
setores = dict(zip(df_raw["Ticker"], df_raw["Setor"]))

# deixando o dataframe com meses nas linhas e tickers nas colunas
df = df_raw.set_index("Ticker")[meses].T

print(f"Ações carregadas: {len(df.columns)}")
print(f"Período: {meses[0]} a {meses[-1]}")
print(f"Total de registros: {df.shape[0] * df.shape[1]}\n")

# -------------------------------------------------------
# CÁLCULO DAS MÉTRICAS
# -------------------------------------------------------

# retorno mensal de cada ação
retornos = df.pct_change().dropna()

# rendimento total no período em %
rendimento = ((df.iloc[-1] / df.iloc[0]) - 1) * 100

# volatilidade = desvio padrão dos retornos (mede o risco)
volatilidade = retornos.std() * 100

# score: quanto maior o retorno e menor a volatilidade, melhor
# usei essa fórmula simples para equilibrar os dois fatores
score = rendimento / (1 + volatilidade)

# juntando tudo num dataframe só
metricas = pd.DataFrame({
    "Rendimento_%": rendimento,
    "Volatilidade_%": volatilidade,
    "Score": score,
    "Setor": pd.Series(setores)
}).sort_values("Score", ascending=False)

# top 10 e top 3 para a carteira
top10 = metricas.head(10)
top3 = metricas.head(3)
tickers_top3 = list(top3.index)

print("Top 10 ações por score:")
print(top10[["Rendimento_%", "Volatilidade_%", "Score", "Setor"]].round(2))

# -------------------------------------------------------
# SIMULAÇÃO DE APORTES MENSAIS
# -------------------------------------------------------

aporte = 1000.00
# distribuição da carteira entre as 3 melhores
distribuicao = {tickers_top3[0]: 0.40, tickers_top3[1]: 0.35, tickers_top3[2]: 0.25}

# taxa mensal da poupança (referência BCB mai/25 a abr/26)
taxa_poupanca = [0.0063] * 6 + [0.0058] * 6

meses_aporte = meses[:-1]  # 12 meses de compra, último mês só para avaliação
cotas = {t: 0.0 for t in tickers_top3}
historico = []

for i, mes in enumerate(meses_aporte):
    # comprando cotas ao preço do mês
    for ticker, pct in distribuicao.items():
        cotas[ticker] += (aporte * pct) / df.loc[mes, ticker]

    # avaliando patrimônio no mês seguinte
    mes_seguinte = meses[i + 1]
    patrimonio = sum(cotas[t] * df.loc[mes_seguinte, t] for t in tickers_top3)
    total_investido = aporte * (i + 1)

    historico.append({
        "Mês": mes,
        "Investido": total_investido,
        "Patrimônio": patrimonio,
        "Rendimento_%": (patrimonio / total_investido - 1) * 100
    })

df_sim = pd.DataFrame(historico)

# resultado final
patrimonio_final = sum(cotas[t] * df.loc[meses[-1], t] for t in tickers_top3)
total_final = aporte * 12

# simulação da poupança com os mesmos aportes
saldo_poupanca = 0.0
for taxa in taxa_poupanca:
    saldo_poupanca = (saldo_poupanca + aporte) * (1 + taxa)

print(f"\nResultado final:")
print(f"Top 3: {', '.join(tickers_top3)}")
print(f"Total investido:  R$ {total_final:,.2f}")
print(f"Patrimônio final: R$ {patrimonio_final:,.2f}")
print(f"Rendimento:       {(patrimonio_final/total_final - 1)*100:.1f}%")
print(f"Poupança teria:   R$ {saldo_poupanca:,.2f} ({(saldo_poupanca/total_final - 1)*100:.1f}%)")

# -------------------------------------------------------
# GRÁFICOS
# -------------------------------------------------------

plt.rcParams.update({
    "font.family": "DejaVu Sans",
    "axes.spines.top": False,
    "axes.spines.right": False,
    "axes.grid": True,
    "grid.alpha": 0.3
})

cores = ["#1F4E79","#2E86AB","#E8B84B","#A23B72","#57CC99",
         "#E76F51","#6A4C93","#2EC4B6","#FF9F1C","#CBFF8C"]

# gráfico 1 — ranking top 10
fig, ax = plt.subplots(figsize=(11, 7))
labels = top10.index.tolist()[::-1]
rends  = top10["Rendimento_%"].tolist()[::-1]
scores = top10["Score"].tolist()[::-1]

barras = ax.barh(labels, rends, color=cores[:10][::-1], height=0.65, edgecolor="white")

for bar, val, sc in zip(barras, rends, scores):
    ax.text(val + 1.5, bar.get_y() + bar.get_height()/2,
            f"{val:.1f}%  |  score {sc:.1f}",
            va="center", fontsize=10, fontweight="bold", color="#333")

# destaque nas top 3
for patch in barras[-3:]:
    patch.set_edgecolor("#E8B84B")
    patch.set_linewidth(2.5)

ax.set_xlabel("Rendimento acumulado 12 meses (%)")
ax.set_xlim(0, max(rends) * 1.28)
ax.set_title("Top 10 Ações da B3 — Melhor Score (Retorno/Risco)\nMai/2025 – Mai/2026",
             fontsize=13, fontweight="bold", color="#1F4E79", pad=15)
plt.tight_layout()
plt.savefig("graficos/grafico1_ranking_top10.png", dpi=150, bbox_inches="tight")
plt.close()
print("\ngráfico 1 salvo")

# gráfico 2 — risco vs retorno
cores_setor = {
    "Educação":"#E8B84B", "Construção":"#2E86AB", "Mobilidade":"#A23B72",
    "Energia":"#57CC99",  "Financeiro":"#1F4E79", "Petróleo":"#E76F51",
    "Mineração":"#6A4C93","Telecom":"#2EC4B6",    "Tecnologia":"#FF9F1C",
    "Varejo":"#CBFF8C",   "Alimentos":"#8338EC",  "Infraestrutura":"#FB5607",
    "Saúde":"#3A86FF",    "Vestuário":"#FF006E",  "Papel/Celulose":"#8AC926",
    "Saneamento":"#6EAF46"
}

fig, ax = plt.subplots(figsize=(12, 7))
setores_legenda = set()

for ticker, row in metricas.iterrows():
    cor = cores_setor.get(row["Setor"], "#AAA")
    top3_flag = ticker in tickers_top3
    ax.scatter(row["Volatilidade_%"], row["Rendimento_%"],
               color=cor, s=160 if top3_flag else 80,
               edgecolors="#333" if top3_flag else "white",
               linewidths=2 if top3_flag else 0.5,
               zorder=3 if top3_flag else 2,
               label=row["Setor"] if row["Setor"] not in setores_legenda else "")
    setores_legenda.add(row["Setor"])
    if top3_flag:
        ax.annotate(f" {ticker}", (row["Volatilidade_%"], row["Rendimento_%"]),
                    fontsize=9, fontweight="bold", color="#1F4E79")

ax.axvline(metricas["Volatilidade_%"].mean(), color="#E76F51",
           linewidth=1.2, linestyle="--", alpha=0.7, label="Volatilidade média")
ax.axhline(metricas["Rendimento_%"].mean(), color="#2E86AB",
           linewidth=1.2, linestyle="--", alpha=0.7, label="Retorno médio")

ax.set_xlabel("Volatilidade — Risco (%)")
ax.set_ylabel("Rendimento acumulado 12 meses (%)")
ax.set_title("Mapa Risco vs Retorno — 50 Ações da B3\n(ideal: canto superior esquerdo)",
             fontsize=13, fontweight="bold", color="#1F4E79", pad=15)
ax.legend(fontsize=8, loc="upper left", ncol=2, framealpha=0.9)
plt.tight_layout()
plt.savefig("graficos/grafico2_risco_retorno.png", dpi=150, bbox_inches="tight")
plt.close()
print("gráfico 2 salvo")

# gráfico 3 — pizza da carteira
fig, ax = plt.subplots(figsize=(7, 6))
valores = {t: cotas[t] * df.loc[meses[-1], t] for t in tickers_top3}

ax.pie(list(valores.values()), labels=list(valores.keys()),
       autopct="%1.1f%%", colors=cores[:3], startangle=140,
       pctdistance=0.78, explode=[0.04]*3,
       wedgeprops={"linewidth": 2, "edgecolor": "white"},
       textprops={"fontsize": 13, "fontweight": "bold"})

legenda = [f"{t}  —  R$ {v:,.2f}" for t, v in valores.items()]
ax.legend(legenda, loc="lower center", bbox_to_anchor=(0.5, -0.12),
          ncol=3, fontsize=11, frameon=False)
ax.set_title("Composição da Carteira em Mai/2026\n(% do Patrimônio por Ativo)",
             fontsize=14, fontweight="bold", pad=20, color="#1F4E79")
plt.tight_layout()
plt.savefig("graficos/grafico3_pizza_carteira.png", dpi=150, bbox_inches="tight")
plt.close()
print("gráfico 3 salvo")

# gráfico 4 — simulação mensal
import matplotlib.ticker as mticker

fig, ax = plt.subplots(figsize=(13, 6))
x = np.arange(len(meses_aporte))
larg = 0.38

ax.bar(x - larg/2, df_sim["Investido"],   width=larg, color="#B0C4DE",
       label="Total Investido (R$)", edgecolor="white")
barras_pat = ax.bar(x + larg/2, df_sim["Patrimônio"], width=larg, color="#1F4E79",
                    label="Patrimônio Real (R$)", edgecolor="white", alpha=0.92)

for bar in barras_pat:
    h = bar.get_height()
    ax.text(bar.get_x() + bar.get_width()/2, h + 60,
            f"R${h:,.0f}", ha="center", va="bottom",
            fontsize=8, color="#1F4E79", fontweight="bold")

# linha de rendimento % no eixo secundário
ax2 = ax.twinx()
ax2.plot(x, df_sim["Rendimento_%"], color="#E8B84B", linewidth=2.5,
         marker="D", markersize=6, label="Rendimento %")
ax2.set_ylabel("Rendimento (%)", color="#E8B84B")
ax2.tick_params(axis="y", colors="#E8B84B")
ax2.yaxis.set_major_formatter(mticker.FormatStrFormatter("%.1f%%"))
ax2.spines["right"].set_visible(True)
ax2.spines["right"].set_color("#E8B84B")

ax.set_xticks(x)
ax.set_xticklabels(meses_aporte, rotation=45, ha="right")
ax.yaxis.set_major_formatter(mticker.FuncFormatter(lambda v, _: f"R${v:,.0f}"))
ax.set_title(f"Simulação — {', '.join(tickers_top3)} | R$ 1.000/mês\n"
             f"Patrimônio Final: R$ {patrimonio_final:,.2f} "
             f"(+{(patrimonio_final/total_final-1)*100:.1f}% vs poupança +{(saldo_poupanca/total_final-1)*100:.1f}%)",
             fontsize=12, fontweight="bold", color="#1F4E79", pad=15)

l1, lb1 = ax.get_legend_handles_labels()
l2, lb2 = ax2.get_legend_handles_labels()
ax.legend(l1+l2, lb1+lb2, loc="upper left", fontsize=10)

plt.tight_layout()
plt.savefig("graficos/grafico4_simulacao_carteira.png", dpi=150, bbox_inches="tight")
plt.close()
print("gráfico 4 salvo")

print("\nAnálise concluída!")
