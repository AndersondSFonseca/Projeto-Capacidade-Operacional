# 📊 Análise de Capacidade Operacional - Equipe de Suporte Técnico

## 📌 Contexto

Equipes de suporte técnico lidam diariamente com variações na demanda de
tickets. Quando o volume recebido supera consistentemente o volume
resolvido, ocorre acúmulo e risco de backlog, impactando SLA, eficiência
operacional e satisfação do cliente.

Este projeto foi desenvolvido com o objetivo de analisar a capacidade
operacional de uma equipe de suporte técnico, identificando gargalos e
riscos de acúmulo estrutural.

------------------------------------------------------------------------

## 🎯 Objetivo do Projeto

Responder às seguintes perguntas de negócio:

-   Qual o volume diário de tickets recebidos?
-   O volume resolvido acompanha a demanda?
-   Existe risco de backlog?
-   Qual o tempo médio de resolução?
-   Há diferença significativa de performance entre analistas?

------------------------------------------------------------------------

## 🛠 Tecnologias Utilizadas

-   Python
-   Pandas
-   Matplotlib
-   Jupyter Notebook
-   Estrutura modular em arquivos `.py`
-   Power BI (etapa complementar de visualização executiva)

------------------------------------------------------------------------

## 🏗 Estrutura do Projeto

Projeto - Capacidade Operacional │ ├── data/ │ ├── raw/ │ ├── processed/
│ ├── notebooks/ │ ├── 01_exploracao.ipynb │ ├──
02_validar_metricas.ipynb │ ├── 03_visualizacao.ipynb │ ├── src/ │ ├──
data_processing.py │ ├── metrics.py │ ├── analysis_export.py │ ├──
analysis_visuals.py │ ├── analysis/ │ ├── arquivos CSV gerados │ ├──
gráficos exportados │

O projeto foi estruturado separando responsabilidades: - Processamento e
limpeza de dados - Cálculo de métricas operacionais - Exportação de
resultados - Visualização e análise

------------------------------------------------------------------------

## 📊 Principais Métricas Analisadas

-   Volume diário de tickets recebidos
-   Volume diário de tickets resolvidos
-   Saldo diário (indicador de backlog)
-   Tempo médio de resolução (em horas)
-   Performance média por analista

------------------------------------------------------------------------

## 🔎 Principais Insights

-   O saldo diário permite identificar períodos de risco de backlog
    estrutural.
-   Pequenas variações na demanda impactam significativamente o acúmulo
    ao longo do tempo.
-   Existe variação na performance média entre analistas, indicando
    oportunidades de otimização e padronização.
-   O tempo médio de resolução é um indicador crítico para monitoramento
    de eficiência operacional.

------------------------------------------------------------------------

## 🚀 Próximos Passos

-   Simulação de aumento de demanda para avaliar resiliência operacional
-   Estimativa de necessidade de ampliação da equipe
-   Construção de dashboard executivo em Power BI
-   Evolução para modelo preditivo de demanda futura

------------------------------------------------------------------------

## ▶️ Como Executar o Projeto

``` bash
# Clonar repositório
git clone <https://github.com/AndersondSFonseca/Projeto-Capacidade-Operacional>

# Instalar dependências
pip install -r requirements.txt

------------------------------------------------------------------------

## 📬 Contato

Projeto desenvolvido por Anderson Santos.

LinkedIn: `<https://www.linkedin.com/in/andersonsfonseca/>`{=html} GitHub: `<https://github.com/AndersondSFonseca>`{=html}
