# CLAUDE.md — Kyndas Insights (Módulos de Dashboard e BI)

Este arquivo guia o assistente em todas as sessões de trabalho neste projeto.
Leia este arquivo completamente antes de qualquer ação de código.

---

## Identidade do Projeto

- **Nome:** Kyndas Insights
- **Tipo:** Módulos de Business Intelligence (BI) e Dashboards Data-Driven
- **Objetivo:** Fornecer as camadas de visualização e análise de dados para o ecossistema Kyndas. Historicamente focados em capacidade operacional, suporte técnico e saúde do negócio (Health Score).
- **Posicionamento:** Atua tanto como um submódulo integrante dos produtos SaaS Verticais (ex: GovTech, Food/Ops) quanto como serviços analíticos stand-alone para clientes B2B.

---

## Arquitetura e Stack Tecnológica (Python/BI)

- **Linguagem:** Python
- **Bibliotecas Principais:** Pandas (análise), Plotly & Dash (Visualização e Aplicações Web)
- **Estruturação:** Dashboards gerados via `Dash`, frequentemente estruturados em monolitos locais (ex: `dashboard_capacidade_operacional.py`) que interagem com datasets (`.csv` ou bancos SQL).

## Regras para Assistentes

1. Esta pasta engloba as ferramentas analíticas baseadas no valor de **Cultura Data-Driven** da matriz Kyndas.
2. Evite arquiteturas convolutas. Priorize views limpas integráveis em IFrames ou adaptáveis para React (caso migradas para o *Kyndas Hub* no futuro).
3. Respeite sempre a identidade visual da empresa (cores baseadas na paleta Kyndas: navy, mint green/yield, etc.).
