from pathlib import Path
import matplotlib.pyplot as plt


def salvar_graficos_analysis(vol_recebidos, capacidade, performance):

    raiz_projeto = Path(__file__).resolve().parent.parent
    pasta = raiz_projeto / "analysis"
    pasta.mkdir(exist_ok=True)

    #Volume Recebidos
    plt.figure()
    vol_recebidos["recebidos"].plot()
    plt.title("Volume Diário de Tickets Recebidos")
    plt.xlabel("Data")
    plt.ylabel("Tickets")
    plt.tight_layout()
    plt.savefig(pasta / "grafico_volume_recebidos.png")
    plt.close()

    #Backlog
    plt.figure()
    capacidade["saldo"].plot()
    plt.title("Saldo Diário (Backlog Risk)")
    plt.xlabel("Data")
    plt.ylabel("Saldo")
    plt.tight_layout()
    plt.savefig(pasta / "grafico_backlog_saldo.png")
    plt.close()

    # Performance
    plt.figure()
    performance["tempo_medio_horas"].plot(kind="bar")
    plt.title("Tempo Médio de Resolução por Analista")
    plt.xlabel("Analista")
    plt.ylabel("Horas")
    plt.tight_layout()
    plt.savefig(pasta / "grafico_performance_analistas.png")
    plt.close()

    print(f"Gráficos salvos em: {pasta}")
