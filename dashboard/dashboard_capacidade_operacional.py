# =============================================================================
#  Dashboard de Capacidade Operacional — Suporte Técnico
#  Autor: Anderson Santos | github.com/AndersondSFonseca
#
#  Como executar:
#    pip install dash plotly pandas
#    python dashboard_capacidade_operacional.py
#  Abra: http://127.0.0.1:8050
# =============================================================================

import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
from dash import Dash, dcc, html, Input, Output
import os

# ---------------------------------------------------------------------------
# 1. CARREGAMENTO E TRATAMENTO DOS DADOS
# ---------------------------------------------------------------------------
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
CSV_PATH  = os.path.join(BASE_DIR, "Technical_Suport_Dataset__tratado_.csv")

df = pd.read_csv(CSV_PATH)

# Datas
df["data_abertura"]    = pd.to_datetime(df["data_abertura"],    errors="coerce")
df["tempo_resolucao"]  = pd.to_datetime(df["tempo_resolucao"],  errors="coerce")
df["sla_previsto_resolucao"] = pd.to_datetime(df["sla_previsto_resolucao"], errors="coerce")
df["tempo_resolucao_horas"]  = pd.to_numeric(df["tempo_resolucao_horas"], errors="coerce")

df["mes"]        = df["data_abertura"].dt.to_period("M").astype(str)
df["mes_label"]  = df["data_abertura"].dt.strftime("%b/%y")
df["dia"]        = df["data_abertura"].dt.date

# Normaliza tópico
df["topico"] = df["topico"].replace({"Pricing and Licensing": "Pricing and licensing"})

# SLA
df["sla_ok"] = (
    df["tempo_resolucao"].notna() &
    df["sla_previsto_resolucao"].notna() &
    (df["tempo_resolucao"] <= df["sla_previsto_resolucao"])
)

# ---------------------------------------------------------------------------
# 2. MÉTRICAS AGREGADAS
# ---------------------------------------------------------------------------

# Volume mensal
monthly_rec = df.groupby("mes").size().rename("recebidos")
monthly_res = df[df["tempo_resolucao"].notna()].groupby(
    df["tempo_resolucao"].dt.to_period("M").astype(str)
).size().rename("resolvidos")
monthly = pd.DataFrame({"recebidos": monthly_rec, "resolvidos": monthly_res}).fillna(0)
monthly = monthly[monthly.index <= "2023-12"].sort_index()
monthly["saldo"] = monthly["resolvidos"] - monthly["recebidos"]
month_labels = pd.to_datetime(monthly.index + "-01").strftime("%b/%y").tolist()

# Backlog cumulativo diário
daily_rec = df.groupby("dia").size().rename("rec")
daily_res = df[df["tempo_resolucao"].notna()].groupby(
    df["tempo_resolucao"].dt.date
).size().rename("res")
daily = pd.DataFrame({"rec": daily_rec, "res": daily_res}).fillna(0).sort_index()
daily["saldo_dia"]   = daily["res"] - daily["rec"]
daily["backlog_cum"] = (daily["rec"] - daily["res"]).cumsum()

# Analistas
analyst = df.groupby("analista_responsavel").agg(
    recebidos=("id_ticket", "count"),
    resolvidos=("tempo_resolucao_horas", lambda x: x.notna().sum()),
    tempo_medio=("tempo_resolucao_horas", "mean")
).reset_index()
analyst["taxa"] = (analyst["resolvidos"] / analyst["recebidos"] * 100).round(1)
analyst = analyst.sort_values("tempo_medio")

# SLA totais
sla_ok_n    = df["sla_ok"].sum()
sla_nok_n   = (df["tempo_resolucao"].notna() & ~df["sla_ok"]).sum()

# Tópicos
topics = df["topico"].value_counts().reset_index()
topics.columns = ["topico", "count"]

# Status
status_counts = df["status_ticket"].value_counts()

# Canal e prioridade
canal  = df["origem_ticket"].value_counts()
prio   = df["prioridade"].value_counts()

# ---------------------------------------------------------------------------
# 3. PALETA E ESTILO
# ---------------------------------------------------------------------------
BLUE   = "#3274B5"
GREEN  = "#1D9E75"
AMBER  = "#C4820A"
RED    = "#D94F4F"
PURPLE = "#6C63B5"
GRAY   = "#888780"

BG        = "#F8F7F5"
CARD_BG   = "#FFFFFF"
TEXT_PRI  = "#2C2C2A"
TEXT_SEC  = "#73726C"
BORDER    = "rgba(0,0,0,0.08)"

FONT = "Inter, Segoe UI, Arial, sans-serif"

CHART_LAYOUT = dict(
    font_family=FONT,
    font_color=TEXT_PRI,
    paper_bgcolor="rgba(0,0,0,0)",
    plot_bgcolor="rgba(0,0,0,0)",
    margin=dict(l=8, r=8, t=8, b=8),
)

AXIS_STYLE = dict(
    showgrid=True, gridcolor="rgba(0,0,0,0.06)",
    zeroline=False, tickfont=dict(size=11, color=TEXT_SEC),
    linecolor=BORDER, showline=True
)

def card(children, style=None):
    s = {
        "background": CARD_BG,
        "borderRadius": "10px",
        "border": f"0.5px solid {BORDER}",
        "padding": "18px 20px",
        "boxShadow": "0 1px 4px rgba(0,0,0,0.05)",
    }
    if style:
        s.update(style)
    return html.Div(children, style=s)

def kpi(label, value, sub=None, color=TEXT_PRI):
    return card([
        html.P(label, style={"fontSize": "12px", "color": TEXT_SEC, "marginBottom": "6px"}),
        html.P(value, style={"fontSize": "26px", "fontWeight": "600", "color": color, "margin": "0"}),
        html.P(sub,   style={"fontSize": "11px", "color": TEXT_SEC, "marginTop": "4px"}) if sub else None
    ])

def section(title):
    return html.P(title, style={
        "fontSize": "11px", "fontWeight": "600", "color": TEXT_SEC,
        "textTransform": "uppercase", "letterSpacing": "0.06em",
        "marginTop": "28px", "marginBottom": "10px"
    })

# ---------------------------------------------------------------------------
# 4. FIGURAS
# ---------------------------------------------------------------------------

# 4.1 Volume mensal
fig_vol = go.Figure()
fig_vol.add_bar(x=month_labels, y=monthly["recebidos"].tolist(),
                name="Recebidos", marker_color=BLUE, marker_cornerradius=3)
fig_vol.add_bar(x=month_labels, y=monthly["resolvidos"].tolist(),
                name="Resolvidos", marker_color=GREEN, marker_cornerradius=3)
fig_vol.update_layout(
    **CHART_LAYOUT, barmode="group",
    xaxis=dict(AXIS_STYLE, tickangle=0),
    yaxis=dict(AXIS_STYLE),
    legend=dict(orientation="h", y=1.15, x=0,
                font=dict(size=11), bgcolor="rgba(0,0,0,0)"),
    showlegend=True
)

# 4.2 Saldo mensal
saldo_vals  = monthly["saldo"].tolist()
saldo_cores = [GREEN if v >= 0 else RED for v in saldo_vals]
fig_saldo = go.Figure(go.Bar(
    x=month_labels, y=saldo_vals,
    marker_color=saldo_cores, marker_cornerradius=3
))
fig_saldo.update_layout(**CHART_LAYOUT, showlegend=False,
    xaxis=dict(AXIS_STYLE, tickangle=0),
    yaxis=dict(AXIS_STYLE),
)
fig_saldo.add_hline(y=0, line_color=BORDER, line_width=1)

# 4.3 Backlog cumulativo
fig_back = go.Figure(go.Scatter(
    x=list(daily.index), y=daily["backlog_cum"].tolist(),
    fill="tozeroy", line_color=RED, fillcolor="rgba(217,79,79,0.12)",
    mode="lines"
))
fig_back.update_layout(**CHART_LAYOUT, showlegend=False,
    xaxis=dict(AXIS_STYLE),
    yaxis=dict(AXIS_STYLE),
)

# 4.4 Analistas — recebidos
fig_anal_rec = go.Figure(go.Bar(
    x=analyst["recebidos"].tolist(),
    y=analyst["analista_responsavel"].tolist(),
    orientation="h", marker_color=BLUE, marker_cornerradius=3
))
fig_anal_rec.update_layout(**CHART_LAYOUT, showlegend=False,
    xaxis=dict(AXIS_STYLE),
    yaxis=dict(AXIS_STYLE, tickfont=dict(size=11)),
)

# 4.5 Analistas — tempo médio
colors_tmr = [GREEN if v == analyst["tempo_medio"].min() else
              RED   if v == analyst["tempo_medio"].max() else
              AMBER for v in analyst["tempo_medio"]]
fig_anal_tmr = go.Figure(go.Bar(
    x=analyst["tempo_medio"].round(1).tolist(),
    y=analyst["analista_responsavel"].tolist(),
    orientation="h", marker_color=colors_tmr, marker_cornerradius=3,
    text=analyst["tempo_medio"].round(1).astype(str) + " h",
    textposition="outside", textfont=dict(size=11, color=TEXT_SEC)
))
fig_anal_tmr.update_layout(**CHART_LAYOUT, showlegend=False,
    xaxis=dict(AXIS_STYLE, range=[78, 102]),
    yaxis=dict(AXIS_STYLE, tickfont=dict(size=11)),
)

# 4.6 SLA donut
fig_sla = go.Figure(go.Pie(
    labels=["Dentro do SLA", "Violação"],
    values=[int(sla_ok_n), int(sla_nok_n)],
    hole=0.62,
    marker_colors=[GREEN, RED],
    textfont_size=12,
    hovertemplate="%{label}: %{value} (%{percent})<extra></extra>"
))
fig_sla.update_layout(**CHART_LAYOUT, showlegend=False,
    annotations=[dict(text=f"<b>{sla_ok_n/(sla_ok_n+sla_nok_n)*100:.1f}%</b><br><span style='font-size:10px'>SLA ok</span>",
                      x=0.5, y=0.5, showarrow=False, font_size=14)]
)

# 4.7 Tópicos
fig_top = go.Figure(go.Bar(
    x=topics["count"].tolist(),
    y=topics["topico"].tolist(),
    orientation="h", marker_color=PURPLE, marker_cornerradius=3,
    text=topics["count"].tolist(), textposition="outside",
    textfont=dict(size=11, color=TEXT_SEC)
))
fig_top.update_layout(**CHART_LAYOUT, showlegend=False,
    xaxis=dict(AXIS_STYLE, range=[0, 780]),
    yaxis=dict(AXIS_STYLE, tickfont=dict(size=11)),
)

# 4.8 Canal + Prioridade donuts
fig_canal = go.Figure(go.Pie(
    labels=canal.index.tolist(), values=canal.values.tolist(),
    hole=0.55, marker_colors=[BLUE, GREEN, AMBER],
    textfont_size=11,
))
fig_canal.update_layout(**CHART_LAYOUT, showlegend=True,
    legend=dict(orientation="h", y=-0.1, x=0.5, xanchor="center",
                font=dict(size=10), bgcolor="rgba(0,0,0,0)")
)

fig_prio = go.Figure(go.Pie(
    labels=prio.index.tolist(), values=prio.values.tolist(),
    hole=0.55, marker_colors=[GREEN, AMBER, RED],
    textfont_size=11,
))
fig_prio.update_layout(**CHART_LAYOUT, showlegend=True,
    legend=dict(orientation="h", y=-0.1, x=0.5, xanchor="center",
                font=dict(size=10), bgcolor="rgba(0,0,0,0)")
)

# ---------------------------------------------------------------------------
# 5. LAYOUT DO DASH
# ---------------------------------------------------------------------------
app = Dash(__name__, title="Capacidade Operacional | Anderson Santos")

GRAPH_CFG = {"displayModeBar": False, "responsive": True}

app.layout = html.Div(style={
    "fontFamily": FONT, "background": BG, "minHeight": "100vh",
    "padding": "28px 32px", "color": TEXT_PRI
}, children=[

    # ── CABEÇALHO
    html.Div([
        html.Div([
            html.H1("Capacidade Operacional — Suporte Técnico",
                    style={"fontSize": "22px", "fontWeight": "600", "margin": "0"}),
            html.P("Jan – Dez 2023  ·  2.330 tickets  ·  8 analistas  ·  Anderson Santos",
                   style={"fontSize": "13px", "color": TEXT_SEC, "marginTop": "4px"}),
        ]),
    ], style={"marginBottom": "24px"}),

    # ── KPIs
    section("KPIs PRINCIPAIS"),
    html.Div([
        kpi("Tickets recebidos",  "2.330",  "Jan – Dez 2023"),
        kpi("Tickets resolvidos", "1.173",  "Status Closed (50,3%)", RED),
        kpi("Backlog acumulado",  "418",    "Tickets em aberto", RED),
        kpi("Cumprimento SLA",    "80,9%",  "1.546 dentro do prazo", GREEN),
        kpi("Violações de SLA",   "366",    "19,1% dos resolvidos", AMBER),
        kpi("Tempo médio resolução","94,7 h","Média geral da equipe"),
    ], style={
        "display": "grid",
        "gridTemplateColumns": "repeat(6, minmax(0,1fr))",
        "gap": "12px"
    }),

    # ── VOLUME E BACKLOG
    section("VOLUME & BACKLOG"),
    html.Div([
        card([
            html.P("Tickets recebidos vs. resolvidos por mês",
                   style={"fontSize": "13px", "fontWeight": "500", "marginBottom": "12px"}),
            dcc.Graph(figure=fig_vol, config=GRAPH_CFG, style={"height": "260px"})
        ], {"flex": "2"}),
        card([
            html.P("Saldo mensal (resolvidos − recebidos)",
                   style={"fontSize": "13px", "fontWeight": "500", "marginBottom": "12px"}),
            dcc.Graph(figure=fig_saldo, config=GRAPH_CFG, style={"height": "260px"})
        ], {"flex": "1"}),
    ], style={"display": "flex", "gap": "14px"}),

    html.Div(style={"marginTop": "14px"}),
    card([
        html.P("Backlog cumulativo ao longo de 2023",
               style={"fontSize": "13px", "fontWeight": "500", "marginBottom": "12px"}),
        dcc.Graph(figure=fig_back, config=GRAPH_CFG, style={"height": "200px"})
    ]),

    html.Div([
        html.Span("⚠ Alerta: em todos os 12 meses o volume recebido superou o resolvido. "
                  "O backlog cresceu continuamente até atingir 418 tickets em aberto. "
                  "Maio foi o mês de maior déficit (−47 tickets).",
                  style={"fontSize": "12px", "color": "#8B5E10"})
    ], style={
        "background": "#FEF3C7", "border": "0.5px solid #F5C057",
        "borderRadius": "8px", "padding": "10px 16px", "marginTop": "12px"
    }),

    # ── ANALISTAS
    section("PERFORMANCE POR ANALISTA"),
    html.Div([
        card([
            html.P("Tickets recebidos",
                   style={"fontSize": "13px", "fontWeight": "500", "marginBottom": "12px"}),
            dcc.Graph(figure=fig_anal_rec, config=GRAPH_CFG, style={"height": "260px"})
        ]),
        card([
            html.P("Tempo médio de resolução (horas)",
                   style={"fontSize": "13px", "fontWeight": "500", "marginBottom": "12px"}),
            dcc.Graph(figure=fig_anal_tmr, config=GRAPH_CFG, style={"height": "260px"})
        ]),
    ], style={"display": "grid", "gridTemplateColumns": "1fr 1fr", "gap": "14px"}),

    # Tabela analistas
    html.Div(style={"marginTop": "14px"}),
    card([
        html.P("Tabela detalhada por analista",
               style={"fontSize": "13px", "fontWeight": "500", "marginBottom": "14px"}),
        html.Table([
            html.Thead(html.Tr([
                html.Th(c, style={"fontSize": "11px", "color": TEXT_SEC, "fontWeight": "600",
                                  "padding": "6px 10px", "borderBottom": f"0.5px solid {BORDER}",
                                  "textAlign": "left"})
                for c in ["Analista", "Recebidos", "Resolvidos", "Taxa resolução", "Tempo médio"]
            ])),
            html.Tbody([
                html.Tr([
                    html.Td(row["analista_responsavel"],
                            style={"padding": "7px 10px", "fontSize": "13px",
                                   "borderBottom": f"0.5px solid {BORDER}"}),
                    html.Td(str(row["recebidos"]),
                            style={"padding": "7px 10px", "fontSize": "13px",
                                   "borderBottom": f"0.5px solid {BORDER}"}),
                    html.Td(str(row["resolvidos"]),
                            style={"padding": "7px 10px", "fontSize": "13px",
                                   "borderBottom": f"0.5px solid {BORDER}"}),
                    html.Td(f"{row['taxa']}%",
                            style={"padding": "7px 10px", "fontSize": "13px",
                                   "borderBottom": f"0.5px solid {BORDER}",
                                   "color": GREEN if row["taxa"] >= 52 else AMBER}),
                    html.Td(f"{row['tempo_medio']:.1f} h",
                            style={"padding": "7px 10px", "fontSize": "13px",
                                   "borderBottom": f"0.5px solid {BORDER}",
                                   "color": GREEN if row["tempo_medio"] == analyst["tempo_medio"].min()
                                            else RED if row["tempo_medio"] == analyst["tempo_medio"].max()
                                            else TEXT_PRI}),
                ])
                for _, row in analyst.sort_values("tempo_medio").iterrows()
            ])
        ], style={"width": "100%", "borderCollapse": "collapse"})
    ]),

    # ── SLA & TÓPICOS
    section("SLA & DISTRIBUIÇÃO DE TÓPICOS"),
    html.Div([
        card([
            html.P("Cumprimento de SLA",
                   style={"fontSize": "13px", "fontWeight": "500", "marginBottom": "12px"}),
            dcc.Graph(figure=fig_sla, config=GRAPH_CFG, style={"height": "220px"})
        ]),
        card([
            html.P("Canal de abertura",
                   style={"fontSize": "13px", "fontWeight": "500", "marginBottom": "12px"}),
            dcc.Graph(figure=fig_canal, config=GRAPH_CFG, style={"height": "220px"})
        ]),
        card([
            html.P("Distribuição por prioridade",
                   style={"fontSize": "13px", "fontWeight": "500", "marginBottom": "12px"}),
            dcc.Graph(figure=fig_prio, config=GRAPH_CFG, style={"height": "220px"})
        ]),
    ], style={"display": "grid", "gridTemplateColumns": "1fr 1fr 1fr", "gap": "14px"}),

    html.Div(style={"marginTop": "14px"}),
    card([
        html.P("Volume por tópico",
               style={"fontSize": "13px", "fontWeight": "500", "marginBottom": "12px"}),
        dcc.Graph(figure=fig_top, config=GRAPH_CFG, style={"height": "240px"})
    ]),

    # ── INSIGHTS
    section("PRINCIPAIS INSIGHTS"),
    html.Div([
        card([
            html.P("Risco de backlog estrutural",
                   style={"fontSize": "13px", "fontWeight": "600", "marginBottom": "6px"}),
            html.P("Saldo negativo em todos os 12 meses de 2023. A capacidade de resolução "
                   "é sistematicamente inferior à demanda recebida, gerando acúmulo contínuo.",
                   style={"fontSize": "12px", "color": TEXT_SEC, "lineHeight": "1.6"})
        ]),
        card([
            html.P("Variação de performance entre analistas",
                   style={"fontSize": "13px", "fontWeight": "600", "marginBottom": "6px"}),
            html.P("Michele Whyatt tem o melhor tempo médio (85,1 h). Nicola Wane tem o maior "
                   "(97,4 h) — diferença de 14%, indicando oportunidade de padronização.",
                   style={"fontSize": "12px", "color": TEXT_SEC, "lineHeight": "1.6"})
        ]),
        card([
            html.P("Product Setup como principal driver",
                   style={"fontSize": "13px", "fontWeight": "600", "marginBottom": "6px"}),
            html.P("Product Setup representa 27% de todos os tickets. "
                   "Principal candidato para base de conhecimento ou automação de respostas.",
                   style={"fontSize": "12px", "color": TEXT_SEC, "lineHeight": "1.6"})
        ]),
        card([
            html.P("Próximos passos",
                   style={"fontSize": "13px", "fontWeight": "600", "marginBottom": "6px"}),
            html.Ul([
                html.Li("Simulação de aumento de demanda"),
                html.Li("Estimativa de necessidade de equipe"),
                html.Li("Modelo preditivo de demanda futura"),
            ], style={"fontSize": "12px", "color": TEXT_SEC, "lineHeight": "1.9", "paddingLeft": "16px"})
        ]),
    ], style={"display": "grid", "gridTemplateColumns": "1fr 1fr 1fr 1fr", "gap": "12px"}),

    # ── RODAPÉ
    html.P("Anderson Santos · github.com/AndersondSFonseca · linkedin.com/in/andersonsfonseca",
           style={"fontSize": "11px", "color": TEXT_SEC, "textAlign": "center",
                  "marginTop": "36px", "paddingTop": "16px",
                  "borderTop": f"0.5px solid {BORDER}"}),
])

# ---------------------------------------------------------------------------
# 6. EXECUÇÃO
# ---------------------------------------------------------------------------
if __name__ == "__main__":
    print("\n" + "="*60)
    print("  Dashboard de Capacidade Operacional")
    print("  Acesse: http://127.0.0.1:8050")
    print("="*60 + "\n")
    app.run(debug=False, port=8050)