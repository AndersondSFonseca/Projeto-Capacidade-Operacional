# Análise de Capacidade Operacional — Equipe de Suporte Técnico

## Contexto

Equipes de suporte técnico lidam diariamente com variações na demanda de tickets. Quando o volume recebido supera consistentemente o volume resolvido, ocorre acúmulo e risco de backlog, impactando SLA, eficiência operacional e satisfação do cliente.

Este projeto analisa a capacidade operacional de uma equipe de suporte técnico, identificando gargalos, riscos de backlog e oportunidades de melhoria de performance.

---

## Dashboard Interativo

O projeto inclui um dashboard web construído com **Streamlit + Plotly**, com 4 abas analíticas e filtros globais na sidebar.

### Pré-requisitos

- Python 3.10+

### Instalação

```bash
git clone https://github.com/AndersondSFonseca/Projeto-Capacidade-Operacional
cd Projeto-Capacidade-Operacional
pip install -r requirements.txt
```

### Executar o dashboard

```bash
py -3.13 -m streamlit run dashboard/app.py
```

O navegador abre automaticamente em `http://localhost:8501`.

### O que está no dashboard

| Aba | Conteúdo |
|-----|----------|
| **Visão Geral** | KPIs principais · Volume diário de tickets abertos vs encerrados · Distribuição por status, prioridade e tópico |
| **Análise de SLA** | Taxa global de cumprimento · Breakdown por prioridade, origem, analista e tópico · Evolução mensal com linha de meta |
| **Performance** | Tempo médio de resolução por analista · Volume encerrado · Scatter de eficiência (volume × velocidade × SLA) · Tabela detalhada |
| **Tendências & Backlog** | Backlog acumulado no tempo · Volume mensal recebidos vs encerrados · Distribuição do tempo de resolução por prioridade |

**Filtros na sidebar** (afetam todas as abas): período, prioridade, analista, origem do ticket e tópico.

---

## Objetivo

Responder às seguintes perguntas de negócio:

- Qual o volume diário de tickets recebidos?
- O volume resolvido acompanha a demanda?
- Existe risco de backlog estrutural?
- Qual o tempo médio de resolução e a taxa de cumprimento de SLA?
- Há diferença significativa de performance entre analistas?

---

## Tecnologias

- Python · Pandas · Streamlit · Plotly
- Jupyter Notebook (análises exploratórias)
- Power BI (modelo semântico e relatório complementar)

---

## Estrutura do Projeto

```
Projeto - Capacidade Operacional/
├── data/
│   ├── bruto/                  # Dados originais
│   └── tratado/                # Dados limpos e padronizados
├── notebooks/
│   ├── 01_entendimento_dados.ipynb
│   ├── 02_validar_dados.ipynb
│   ├── 03_visualizacao.ipynb
│   ├── 04_apresentacao_resultados.ipynb
│   ├── 05_analise_sla.ipynb
│   ├── 06_simulacao_demanda.ipynb
│   └── 07_dimensionamento_equipe.ipynb
├── src/
│   ├── data_processing.py      # Limpeza e transformação
│   ├── metrics.py              # Cálculo de métricas operacionais
│   ├── analysis_export.py      # Exportação de resultados
│   └── analysis_visuals.py     # Geração de gráficos
├── analysis/                   # CSVs e gráficos exportados
├── dashboard/
│   └── app.py                  # Dashboard Streamlit
├── powerbi/                    # Modelo semântico e relatório .pbip
├── requirements.txt
└── README.md
```

---

## Principais Insights

- O saldo diário (recebidos − resolvidos) permite identificar períodos de risco de backlog estrutural.
- A taxa de cumprimento de SLA global é de ~80%, com variação significativa por prioridade e analista.
- Existe diferença de até 12 horas no tempo médio de resolução entre analistas, indicando oportunidades de padronização.
- Pequenas variações na demanda impactam significativamente o acúmulo de backlog ao longo do tempo.

---

## Contato

Desenvolvido por **Anderson Santos**

- LinkedIn: [andersonsfonseca](https://www.linkedin.com/in/andersonsfonseca/)
- GitHub: [AndersondSFonseca](https://github.com/AndersondSFonseca)
