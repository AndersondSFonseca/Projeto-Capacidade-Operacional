# Projeto de BI: Análise de Capacidade Operacional — Equipe de Suporte Técnico

## 📋 Visão Geral do Projeto

Equipes de suporte técnico lidam diariamente com variações na demanda de tickets. Quando o volume recebido supera consistentemente o volume resolvido, ocorre acúmulo e risco de backlog, impactando acordos de nível de serviço (SLA), eficiência operacional e, principalmente, a satisfação do cliente.

Este projeto foca em aplicar conceitos de **Business Intelligence (BI)** e **Análise de Dados** para avaliar a capacidade operacional de uma equipe de suporte. O objetivo principal é identificar gargalos, prever riscos de formação de backlog e descobrir oportunidades para otimização de performance.

---

## 📊 Business Intelligence & Visualização de Dados

Como parte fundamental da estratégia de BI deste projeto, desenvolvemos soluções interativas para a apresentação e exploração dos dados. A ferramenta de visualização primária foi construída utilizando **Streamlit**, permitindo uma interface de usuário dinâmica e rica em insights operacionais.

### Dashboard Interativo (Streamlit)

O projeto inclui um dashboard web interativo, construído com **Streamlit + Plotly**. Ele atua como o ponto focal para o monitoramento operacional, oferecendo 4 abas analíticas principais e filtros globais na barra lateral (sidebar) para exploração detalhada.

| Aba Analítica | Descrição do Conteúdo |
|---------------|-----------------------|
| **Visão Geral** | KPIs principais de operação. Volume diário de tickets abertos vs encerrados. Distribuição interativa por status, prioridade e tópico. |
| **Análise de SLA** | Taxa global de cumprimento de prazos. Desdobramento (breakdown) detalhado por prioridade, origem, analista e tópico. Evolução mensal acompanhada de linha de meta. |
| **Performance** | Análise de tempo médio de resolução por analista. Volume total encerrado. Gráficos de dispersão (scatter) avaliando eficiência (volume × velocidade × SLA) e tabelas detalhadas de performance. |
| **Tendências & Backlog** | Acompanhamento do backlog acumulado no tempo. Comparativo mensal de volume recebido vs encerrado. Distribuição do tempo de resolução agrupado por prioridade. |

> **Filtros Globais:** O dashboard permite filtrar os dados por período de tempo, prioridade do ticket, analista responsável, origem da solicitação e tópico relacionado, refletindo instantaneamente em todas as visualizações.

### Estrutura de Solução de BI

O projeto não se resume apenas a uma tela de visualização, mas contempla o ciclo completo de inteligência de negócios:
1. **Extração e Tratamento (ETL/ELT):** Scripts estruturados para limpeza e padronização dos dados brutos.
2. **Modelagem:** Estruturação de dados limpos para consumo fluido pelas ferramentas de visualização.
3. **Apresentação:** Dashboard Streamlit (e suporte complementar em Power BI) para entrega de valor ao usuário final.

---

## 🎯 Objetivos de Negócio

Este projeto foi desenhado para responder de forma clara às seguintes perguntas estratégicas:

- Qual é o volume diário e a sazonalidade dos tickets recebidos?
- A capacidade de resolução atual (volume resolvido) consegue acompanhar a demanda de entrada?
- Existe um risco iminente ou estrutural de aumento de backlog?
- Qual é o tempo médio de resolução (TMR) e a taxa de cumprimento de SLA da operação?
- Como está distribuída a performance entre os diferentes analistas da equipe? Existem oportunidades de nivelamento?

---

## 🛠️ Tecnologias Utilizadas

A stack tecnológica do projeto baseia-se fortemente no ecossistema de dados em Python:

- **Linguagem Principal:** Python 3.10+
- **Manipulação de Dados:** Pandas
- **Dashboard e Web App:** Streamlit
- **Visualização Gráfica:** Plotly
- **Ambiente de Exploração:** Jupyter Notebook
- **Ferramentas Complementares de BI:** Power BI (para modelagem semântica e relatórios estáticos complementares)

---

## 🚀 Como Executar o Projeto

### Pré-requisitos
- Python 3.10 ou superior instalado no sistema.
- Git para versionamento e clonagem.

### Instalação
1. Clone o repositório:
```bash
git clone https://github.com/AndersondSFonseca/Projeto-Capacidade-Operacional
cd Projeto-Capacidade-Operacional
```

2. Instale as dependências listadas:
```bash
pip install -r requirements.txt
```

### Inicializando o Dashboard de BI
Para executar o dashboard Streamlit localmente, utilize o comando abaixo:
```bash
python -m streamlit run dashboard/app.py
```
> O navegador padrão abrirá automaticamente o aplicativo no endereço local: `http://localhost:8501`.

---

## 📂 Estrutura de Diretórios

A arquitetura do projeto foi estruturada visando clareza e separação de responsabilidades (pipeline de dados vs apresentação):

```text
Projeto - Capacidade Operacional/
├── data/
│   ├── bruto/                  # Dados originais e não processados
│   └── tratado/                # Base de dados limpa, padronizada e pronta para o BI
├── notebooks/                  # Notebooks Jupyter (Exploração, Simulações, Dimensionamento)
├── src/
│   ├── data_processing.py      # Lógicas de ETL (Limpeza e transformação)
│   ├── metrics.py              # Cálculos padronizados de métricas operacionais
│   ├── analysis_export.py      # Exportação de tabelas e resultados
│   └── analysis_visuals.py     # Geração programática de gráficos estáticos
├── analysis/                   # Repositório de arquivos CSV exportados e imagens geradas
├── dashboard/
│   └── app.py                  # Código fonte principal do Dashboard Streamlit
├── powerbi/                    # Arquivos relacionados ao modelo semântico do Power BI
├── requirements.txt            # Dependências do projeto Python
└── README.md                   # Documentação oficial
```

---

## 💡 Principais Insights Operacionais

Através das análises e do monitoramento pelo dashboard, destacam-se as seguintes descobertas:
- **Indicador de Alerta:** O saldo diário (recebidos − resolvidos) provou ser a métrica mais confiável para identificar antecipadamente períodos críticos com risco de backlog estrutural.
- **Conformidade de Prazos:** A taxa de cumprimento global de SLA orbita na casa dos 80%, porém apresenta flutuações severas dependendo da prioridade do chamado e do analista alocado.
- **Disparidade de Performance:** Identificou-se uma variação de até 12 horas no tempo médio de resolução entre diferentes membros da equipe, sinalizando uma forte necessidade e oportunidade de criação de base de conhecimento e padronização de procedimentos.
- **Sensibilidade a Oscilações:** A estrutura atual mostra-se inelástica; variações de curto prazo na demanda geram impactos que perduram a longo prazo no acúmulo de backlog.

---

## ✉️ Contato do Desenvolvedor

Desenvolvido por **Anderson Santos**

- **LinkedIn:** [andersonsfonseca](https://www.linkedin.com/in/andersonsfonseca/)
- **GitHub:** [AndersondSFonseca](https://github.com/AndersondSFonseca)
