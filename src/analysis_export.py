from pathlib import Path

def salvar_metricas_analysis(
    vol_recebidos,
    vol_resolvidos,
    performance,
    capacidade,
    tempo_med
):

    raiz_projeto = Path(__file__).resolve().parent.parent
    pasta = raiz_projeto / "analysis"
    pasta.mkdir(exist_ok=True)

    vol_recebidos.to_csv(pasta / "volume_recebidos_diario.csv")
    vol_resolvidos.to_csv(pasta / "volume_resolvidos_diario.csv")
    performance.to_csv(pasta / "performance_analistas.csv")
    capacidade.to_csv(pasta / "capacidade_backlog_diaria.csv")

    texto = f"""
    Resumo Operacional
    
    ==================
    Tempo médio de resolução (horas): {tempo_med:.2f}
    """
    with open(pasta / "resumo_metricas.txt", "w", encoding="utf-8") as f:
        f.write(texto)

    print("Arquivos salvos em /analysis")
