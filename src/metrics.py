import pandas as pd

# Volume diário de tickets

#Tempo médio de resolução (só fechados)

#Performance por analista

#Risco de backlog (recebidos vs resolvidos)

def fechados(df: pd.DataFrame) -> pd.DataFrame:
    return df[df['status_ticket'] == 'Closed'].copy()

def volume_diario_recebidos(df: pd.DataFrame) -> pd.DataFrame:
    saida = (df.groupby(df['data_abertura'].dt.date)
             .size()
             .rename('recebidos')
             .to_frame()
             )
    return saida

def volume_diario_resolvidos(df: pd.DataFrame) -> pd.DataFrame:
    df_f = fechados(df)
    saida = (df_f.groupby(df_f['data_fechamento'].dt.date)
             .size()
             .rename('resolvidos')
             .to_frame())
    return saida

def tempo_medio_resolucao_horas(df: pd.DataFrame) -> pd.DataFrame:
    df_f = fechados(df)
    return float(df_f['tempo_resolucao_horas'].mean())

def performance_media_por_analista(df: pd.DataFrame) -> pd.DataFrame:
    df_f = fechados(df)
    saida = (df_f.groupby('analista_responsavel')['tempo_resolucao_horas']
             .mean()
             .sort_values()
             .rename('tempo_medio_horas')
             .to_frame())
    return saida

def capacidade_backlog_diaria(df: pd.DataFrame) -> pd.DataFrame:
    """
    Junta recebidos vs resolvidos por dia e calcula saldo.
    saldo > 0 → risco backlog
    saldo = 0 → equilibrado
    saldo < 0 → folga
    """

    recebido = volume_diario_recebidos(df)
    resolvido = volume_diario_resolvidos(df)

    capacidade = recebido.join(resolvido, how='outer').fillna(0)
    capacidade['saldo'] = capacidade['recebidos'] - capacidade['resolvidos']
    return capacidade.sort_index()
