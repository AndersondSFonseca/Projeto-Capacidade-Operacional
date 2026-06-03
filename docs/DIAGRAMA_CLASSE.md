# Diagrama de Classes — Projeto Capacidade Operacional

Representa a arquitetura do código-fonte (`src/`, `main.py`, `dashboard/app.py`).
O projeto segue uma organização em **camadas / pipeline de dados**:
**Carga → Tratamento (ETL) → Métricas → Exportação/Visualização → Apresentação (Dashboard)**.

```mermaid
classDiagram
    direction LR

    class Dados {
        <<data_loader>>
        +dado_bruto() DataFrame$
    }

    class DataProcessing {
        <<data_processing>>
        +tratar_dados() DataFrame
        +salvar_dado_limpo(df) None
    }

    class Metrics {
        <<metrics>>
        +fechados(df) DataFrame
        +volume_diario_recebidos(df) DataFrame
        +volume_diario_resolvidos(df) DataFrame
        +tempo_medio_resolucao_horas(df) float
        +performance_media_por_analista(df) DataFrame
        +capacidade_backlog_diaria(df) DataFrame
    }

    class AnalysisExport {
        <<analysis_export>>
        +salvar_metricas_analysis(vol_rec, vol_res, perf, cap, tmr) None
    }

    class AnalysisVisuals {
        <<analysis_visuals>>
        +salvar_graficos_analysis(vol_rec, cap, perf) None
    }

    class Main {
        <<main.py>>
        +main() None
    }

    class Dashboard {
        <<dashboard/app.py>>
        +carregar_dados() DataFrame
        -render_visao_geral()
        -render_analise_sla()
        -render_performance()
        -render_tendencias_backlog()
    }

    Main ..> DataProcessing : orquestra
    DataProcessing ..> Dados : usa
    Metrics ..> DataProcessing : consome dados tratados
    AnalysisExport ..> Metrics : exporta resultados
    AnalysisVisuals ..> Metrics : plota resultados
    Dashboard ..> DataProcessing : carrega base tratada
    Dashboard ..> Metrics : calcula KPIs
```

## Descrição das classes/módulos

| Classe / Módulo | Responsabilidade | Arquivo |
|-----------------|------------------|---------|
| **Dados** | Camada de **carga**: lê o CSV bruto e devolve um DataFrame. | `src/data_loader.py` |
| **DataProcessing** | Camada de **ETL**: renomeia/traduz colunas, remove campos irrelevantes, converte datas e calcula `tempo_resolucao_horas`. | `src/data_processing.py` |
| **Metrics** | Camada de **cálculo**: volume recebido/resolvido, TMR, performance por analista e saldo de backlog. | `src/metrics.py` |
| **AnalysisExport** | **Exportação** das métricas para arquivos CSV/TXT em `/analysis`. | `src/analysis_export.py` |
| **AnalysisVisuals** | Geração de **gráficos estáticos** (matplotlib) em `/analysis`. | `src/analysis_visuals.py` |
| **Main** | **Orquestrador** do pipeline de tratamento. | `main.py` |
| **Dashboard** | **Apresentação**: app web Streamlit + Plotly com 4 abas e filtros globais. | `dashboard/app.py` |

> **Notas de notação:** `+` público, `-` privado, `$` método estático (`Dados.dado_bruto`).
> As setas tracejadas (`..>`) representam **dependência** (uma classe usa outra), padrão
> adequado a um projeto Python organizado por módulos funcionais.
