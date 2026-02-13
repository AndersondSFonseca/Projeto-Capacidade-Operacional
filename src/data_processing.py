from src.data_loader import Dados

import pandas as pd

df = Dados.dado_bruto().copy()

print(df)

traducao_colunas = {
    "Status": "status_ticket",
    "Ticket ID": "id_ticket",
    "Priority": "prioridade",
    "Source": "origem_ticket",
    "Topic": "topico",
    "Agent Group": "grupo_atendimento",
    "Agent Name": "analista_responsavel",
    "Created time": "data_abertura",
    "Expected SLA to resolve": "sla_previsto_resolucao",
    "Expected SLA to first response": "sla_previsto_primeira_resposta",
    "First response time": "tempo_primeira_resposta",
    "SLA For first response": "cumpriu_sla_primeira_resposta",
    "Resolution time": "tempo_resolucao",
    "SLA For Resolution": "cumpriu_sla_resolucao",
    "Close time": "data_fechamento",
    "Agent interactions": "interacoes_analista",
    "Survey results": "resultado_pesquisa_satisfacao",
    "Product group": "grupo_produto",
    "Support Level": "nivel_suporte",
    "Country": "pais"
}

df.rename(columns=traducao_colunas, inplace=True)
# pd.set_option('display.max_columns', None)
retirar_coluna = ([
    'grupo_atendimento',
    'sla_previsto_primeira_resposta',
    'cumpriu_sla_primeira_resposta',
    'cumpriu_sla_resolucao',
    'interacoes_analista',
    'resultado_pesquisa_satisfacao',
    'grupo_produto',
    'nivel_suporte',
    'pais',
    'Latitude',
    'Longitude'])

df.drop(retirar_coluna, axis=1, inplace=True)
df.set_index('id_ticket', inplace=True)
df.columns
df
df['data_abertura'] = pd.to_datetime(df['data_abertura'])
df['data_fechamento'] = pd.to_datetime(df['data_fechamento'])

##criar tempo em minutos de resolução

df['tempo_resolucao_horas'] = (df['data_fechamento'] - df['data_abertura'])
df
df['tempo_resolucao_horas']

df.to_csv('teste.csv', index=False)