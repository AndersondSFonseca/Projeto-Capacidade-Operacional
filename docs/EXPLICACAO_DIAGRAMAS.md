# Explicação dos Diagramas — Projeto Capacidade Operacional

Documento de apoio à apresentação. Para cada diagrama há: **o que é**, **por que existe no
projeto** e um **roteiro de fala** (o que dizer ao professor). As imagens em PNG estão na
pasta [`docs/img/`](img/).

> **Contexto do projeto:** análise de **Business Intelligence** sobre a base *Technical Support
> Dataset* (~2.330 tickets de uma equipe de suporte técnico). O objetivo é medir a **capacidade
> operacional** — se a equipe consegue resolver os chamados no ritmo em que eles chegam — e
> identificar risco de **backlog** (acúmulo) e desvios de **SLA**.

---

## 1. Modelo de Dados (MER) — `01_MER.png`

### O que é
É o **modelo de dados** do projeto, desenhado como **esquema estrela** (*star schema*), o
padrão usado em Business Intelligence. No centro fica a tabela **Fato** (os fatos mensuráveis:
os tickets e suas métricas) e ao redor as tabelas **Dimensão** (os atributos descritivos pelos
quais filtramos e agrupamos os dados).

### Por que existe
Como o projeto é de **análise de dados/BI**, o "modelo de dados" pedido é o modelo dimensional.
Ele mostra **como os dados estão organizados** para permitir as análises do dashboard (filtrar
por analista, prioridade, período, canal etc.).

### Componentes
- **FATO_TICKET** (tabela fato): 1 linha = 1 ticket. Guarda as **métricas** — tempo de resolução,
  cumprimento de SLA, satisfação, nº de interações — e as **chaves** que ligam às dimensões.
- **Dimensões** (as "pontas da estrela"):
  - **DIM_TEMPO** — calendário (dia, mês, ano); usada duas vezes: data de abertura e de fechamento.
  - **DIM_ANALISTA** — nome do analista, grupo (1ª/2ª linha) e nível (Tier 1/2).
  - **DIM_PRIORIDADE** — Low, Medium, High.
  - **DIM_STATUS** — Open, In progress, Resolved, Closed.
  - **DIM_ORIGEM** — canal de entrada: Chat, Email, Phone.
  - **DIM_TOPICO** — assunto do chamado (Bug report, Feature request...).
  - **DIM_PRODUTO** — grupo de produto.
  - **DIM_LOCALIZACAO** — país e coordenadas.

### Cardinalidade
Todos os relacionamentos são **1:N (um-para-muitos)**: cada dimensão descreve **muitos** tickets,
e cada ticket aponta para **uma** ocorrência de cada dimensão. Ex.: *um analista* atende *muitos
tickets*; *cada ticket* tem *um único analista*.

### Roteiro de fala (30s)
> "Este é o modelo de dados do projeto, em esquema estrela. No centro está a tabela Fato, com um
> registro por ticket e todas as métricas — tempo de resolução, SLA e satisfação. Ao redor estão
> as dimensões, que são os filtros do dashboard: analista, prioridade, tempo, canal, tópico e
> localização. A relação é sempre um-para-muitos: uma prioridade classifica vários tickets, mas
> cada ticket tem só uma prioridade. Esse modelo é o que permite cruzar os dados nas análises."

---

## 2. Diagrama de Classes — `02_DIAGRAMA_CLASSE.png`

### O que é
Representa a **arquitetura do código-fonte** em Python: os módulos (classes), seus métodos e como
**dependem uns dos outros**.

### Por que existe
Mostra que o projeto não é um script único, mas uma solução **organizada em camadas**, com
separação de responsabilidades — boa prática de engenharia de software.

### Componentes (o fluxo do dado)
A leitura é em **pipeline**, da esquerda para a direita:
1. **Dados** (`data_loader`) — lê o CSV bruto.
2. **DataProcessing** (`data_processing`) — faz o **ETL**: traduz colunas, limpa, converte datas e
   calcula o tempo de resolução.
3. **Metrics** (`metrics`) — calcula as métricas: volume recebido/resolvido, tempo médio,
   performance por analista e saldo de backlog.
4. **AnalysisExport / AnalysisVisuals** — exportam os resultados em CSV e gráficos.
5. **Dashboard** (`app.py`) — apresenta tudo no painel Streamlit.
6. **Main** (`main.py`) — orquestra o pipeline de tratamento.

As **setas tracejadas** significam "depende de / usa". Ex.: o Dashboard usa Metrics e
DataProcessing.

### Roteiro de fala (30s)
> "Aqui está a arquitetura do código, organizada em camadas. O dado entra pelo data_loader, passa
> pelo tratamento (ETL) no data_processing, vira métrica no metrics, e é apresentado no dashboard
> em Streamlit. Cada módulo tem uma responsabilidade única e as setas mostram as dependências.
> Essa separação deixa o projeto fácil de manter e de testar."

---

## 3. Diagrama de Casos de Uso — `03_CASO_DE_USO.png`

### O que é
Mostra **quem usa o sistema** (atores) e **o que cada um consegue fazer** (casos de uso),
delimitados pela **fronteira do sistema** (a caixa).

### Por que existe
Descreve o sistema do ponto de vista do **usuário/negócio**, e não do código — responde "para que
serve e para quem".

### Componentes
- **Atores:**
  - **Gestor / Coordenador de Suporte** — consome as análises para decidir.
  - **Analista de Dados** — mantém o pipeline e gera as bases.
- **Casos de uso principais:** visualizar KPIs, filtrar dados, analisar SLA, avaliar performance
  por analista, monitorar backlog, identificar risco de gargalo, executar o ETL e exportar
  métricas.
- **Relações:**
  - **«include»** — um caso de uso sempre usa outro (monitorar backlog **inclui** avaliar o risco).
  - **«extend»** — um caso de uso opcional estende outro (exportar **estende** o ETL).

### Roteiro de fala (30s)
> "Este diagrama mostra quem usa o sistema. O Gestor de Suporte usa o dashboard para ver KPIs,
> acompanhar SLA, avaliar a performance dos analistas e monitorar o backlog. O Analista de Dados
> cuida do pipeline: roda o ETL e exporta as métricas. As relações include e extend mostram as
> dependências entre as funcionalidades. É a visão de negócio do projeto."

---

## Como anexar na entrega (Classroom)

1. Anexe os três PNGs da pasta `docs/img/` (`01_MER.png`, `02_DIAGRAMA_CLASSE.png`,
   `03_CASO_DE_USO.png`).
2. Use este documento como **roteiro** para explicar cada um.
3. Os mesmos diagramas também ficam versionados e renderizados no GitHub (pasta `docs/`),
   junto com o código-fonte.
