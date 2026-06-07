# Invest+ Corretora — Análise de Carteira B3 com Big Data em Python

> Projeto de extensão desenvolvido para a disciplina de **Big Data**  
> Estácio de Sá — Campus São José | Professor: Robson Lorbieski

---

## Sobre o Projeto

Sistema em Python que aplica conceitos de Big Data para varrer **50 ações da B3**, calcular métricas de risco e retorno para cada uma, ranquear as melhores oportunidades e simular o resultado real de uma carteira com aportes mensais de R$ 1.000.

O projeto foi desenvolvido em parceria com a **Invest+ Corretora**, empresa de assessoria financeira de São José/SC, que precisava de uma ferramenta visual para demonstrar aos seus clientes o desempenho comparativo de ações frente à poupança.

---

## Resultados

| Indicador | Valor |
|---|---|
| Ações analisadas | 50 |
| Registros processados | 650 |
| Período analisado | Mai/2025 – Mai/2026 |
| Top 3 selecionadas | CURY3, MRVE3, DIRR3 |
| Patrimônio final (R$ 1.000/mês) | R$ 16.388,61 |
| Rendimento da carteira | +36,6% |
| Rendimento da poupança | +3,9% |
| Ganho extra vs poupança | R$ 3.915,36 |

---

## Gráficos Gerados

| Gráfico | Descrição |
|---|---|
| `grafico1_ranking_top10.png` | Top 10 ações por score combinado (retorno/risco) |
| `grafico2_risco_retorno.png` | Mapa scatter: risco vs retorno das 50 ações |
| `grafico3_pizza_carteira.png` | Composição percentual da carteira final |
| `grafico4_simulacao_carteira.png` | Simulação mensal: valor investido vs patrimônio real |

---

## Como Usar

### 1. Instalar dependências

```bash
pip install pandas numpy matplotlib
```

### 2. Clonar o repositório

```bash
git clone https://github.com/Fabricioordtz/investmais-b3.git
cd investmais-b3
```

### 3. Executar a análise

```bash
python analise_bigdata.py
```

Os 4 gráficos serão salvos automaticamente na pasta onde o script for executado.

---

## Estrutura do Projeto

```
investmais-b3/
│
├── analise_bigdata.py        # Script principal — análise e geração dos gráficos
│
├── dados/
│   └── dados_b3.csv          # Base de dados: 50 ações × 13 meses de preços
│
├── graficos/
│   ├── grafico1_ranking_top10.png
│   ├── grafico2_risco_retorno.png
│   ├── grafico3_pizza_carteira.png
│   └── grafico4_simulacao_carteira.png
│
└── docs/
    ├── Relatorio_InvestMais.docx
    ├── Documento_Extensao_InvestMais.docx
    └── Slides_InvestMais.pptx
```

---

## Como o Score é Calculado

O score é a métrica central do projeto. Ele combina retorno e risco numa única nota:

```
Score = Rendimento (%) / (1 + Volatilidade (%))
```

**Não basta uma ação render muito — ela precisa oscilar pouco.** O score premia ativos com alta rentabilidade e baixa volatilidade, identificando as melhores oportunidades para o perfil conservador a moderado dos clientes da Invest+.

| Score | Classificação |
|---|---|
| Acima de 25 | Excelente relação risco/retorno |
| Entre 15 e 25 | Bom — vale atenção |
| Abaixo de 15 | Retorno não justifica o risco |

---

## Tecnologias Utilizadas

- **Python 3** — linguagem principal
- **Pandas** — manipulação e análise dos dados
- **NumPy** — cálculos numéricos
- **Matplotlib** — geração dos gráficos

---

## Parâmetros Configuráveis

No início do arquivo `analise_bigdata.py` você pode ajustar:

```python
APORTE_MENSAL  = 1000.00           # valor aportado por mês (R$)
DISTRIB_TOP3   = [0.40, 0.35, 0.25] # distribuição entre as top 3
TAXA_POUPANCA  = [0.0063] * 6 + [0.0058] * 6  # taxas mensais BCB
```

---

## Documentação

- [Relatório Técnico](docs/Relatorio_InvestMais.docx)
- [Documento de Extensão](docs/Documento_Extensao_InvestMais.docx)
- [Slides de Apresentação](docs/Slides_InvestMais.pptx)

---

## Autor

**Fabricio Raddatz Ribeiro Araujo**  
Curso Técnico em Informática — Estácio de Sá, Campus São José  
Professor orientador: Robson Lorbieski  

---

*Projeto acadêmico com fins educativos. Os dados utilizados têm caráter ilustrativo e não constituem recomendação de investimento.*
