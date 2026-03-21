import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from pathlib import Path

st.set_page_config(
    page_title="Capacidade Operacional",
    layout="wide",
    initial_sidebar_state="expanded",
)

#Paleta e estilo 
AZUL      = "#1B4F72"
AZUL_CLARO = "#2980B9"
VERDE     = "#1E8449"
LARANJA   = "#D35400"
VERMELHO  = "#922B21"
CINZA     = "#626567"
TEMPLATE  = "plotly_white"
CORES     = [AZUL_CLARO, "#27AE60", "#F39C12", "#E74C3C", "#8E44AD", "#16A085", "#D35400"]

st.markdown("""
<style>
  .block-container { padding-top: 1.2rem; padding-bottom: 0.5rem; }
  div[data-testid="metric-container"] {
    background: white;
    border: 1px solid #e8ecf0;
    border-radius: 10px;
    padding: 16px 20px;
    border-top: 3px solid #2980B9;
  }
  div[data-testid="stTabs"] button { font-size: 0.9rem; font-weight: 600; }
  h3 { color: #1B4F72; font-size: 1rem; margin: 1rem 0 0.3rem 0; }
</style>
""", unsafe_allow_html=True)

DATA_PATH = Path(__file__).parent.parent / "data" / "tratado" / "Technical Suport Dataset (tratado).csv"

@st.cache_data
def carregar_dados() -> pd.DataFrame:
    df = pd.read_csv(DATA_PATH, index_col=0)
    for col in ["data_abertura", "sla_previsto_resolucao", "data_fechamento",
                "tempo_primeira_resposta", "tempo_resolucao"]:
        if col in df.columns:
            df[col] = pd.to_datetime(df[col], errors="coerce")

    df["encerrado"] = df["status_ticket"].isin(["Closed", "Resolved"])

    # SLA mede o tempo de RESOLUÇÃO, não o fechamento administrativo
    df["cumpriu_sla"] = (
        df["encerrado"]
        & df["tempo_resolucao"].notna()
        & df["sla_previsto_resolucao"].notna()
        & (df["tempo_resolucao"] <= df["sla_previsto_resolucao"])
    )

    df["data_ref"]   = df["data_abertura"].dt.date
    df["fech_ref"]   = df["data_fechamento"].dt.date
    df["mes"]        = df["data_abertura"].dt.to_period("M").astype(str)
    df["prioridade"] = pd.Categorical(df["prioridade"], ["High", "Medium", "Low"], ordered=True)
    return df

df_full = carregar_dados()

with st.sidebar:
    st.markdown(f"## Filtros")
    st.markdown("---")

    dmin = df_full["data_abertura"].min().date()
    dmax = df_full["data_abertura"].max().date()
    periodo = st.date_input("Período de abertura", value=(dmin, dmax), min_value=dmin, max_value=dmax)

    pri_opts = ["High", "Medium", "Low"]
    prioridades = st.multiselect("Prioridade", pri_opts, default=pri_opts)

    analistas = st.multiselect(
        "Analista",
        sorted(df_full["analista_responsavel"].unique()),
        default=list(df_full["analista_responsavel"].unique()),
    )

    origens = st.multiselect(
        "Origem",
        sorted(df_full["origem_ticket"].unique()),
        default=list(df_full["origem_ticket"].unique()),
    )

    topicos = st.multiselect(
        "Tópico",
        sorted(df_full["topico"].unique()),
        default=list(df_full["topico"].unique()),
    )

    st.markdown("---")
    st.caption(f"Dados: {dmin} — {dmax}")

try:
    d_ini, d_fim = periodo
except (TypeError, ValueError):
    d_ini, d_fim = dmin, dmax

df = df_full[
    df_full["data_abertura"].dt.date.between(d_ini, d_fim)
    & df_full["prioridade"].isin(prioridades)
    & df_full["analista_responsavel"].isin(analistas)
    & df_full["origem_ticket"].isin(origens)
    & df_full["topico"].isin(topicos)
].copy()

st.markdown(f"# Capacidade Operacional — Suporte Técnico")
st.caption(
    f"{d_ini} a {d_fim}  ·  "
    f"**{len(df):,}** tickets filtrados de **{len(df_full):,}** total"
)

if len(df) == 0:
    st.warning("Nenhum ticket encontrado com os filtros selecionados.")
    st.stop()

total        = len(df)
encerrados   = int(df["encerrado"].sum())
em_andamento = total - encerrados
tempo_medio  = df.loc[df["encerrado"] & df["tempo_resolucao_horas"].notna(), "tempo_resolucao_horas"].mean()
df_sla_base  = df[df["encerrado"] & df["sla_previsto_resolucao"].notna()]
taxa_sla     = df_sla_base["cumpriu_sla"].mean() if len(df_sla_base) > 0 else 0.0

tab1, tab2, tab3, tab4 = st.tabs([
    "   Visao Geral   ",
    "   Analise de SLA   ",
    "   Performance   ",
    "   Tendencias e Backlog   ",
])

with tab1:
    c1, c2, c3, c4, c5 = st.columns(5)
    c1.metric("Total de Tickets",      f"{total:,}")
    c2.metric("Encerrados",            f"{encerrados:,}")
    c3.metric("Em Andamento",          f"{em_andamento:,}")
    c4.metric("Tempo Medio (h)",       f"{tempo_medio:.1f}h" if pd.notna(tempo_medio) else "—")
    c5.metric("Taxa de SLA",           f"{taxa_sla:.1%}",
              delta="acima da meta" if taxa_sla >= 0.80 else "abaixo da meta",
              delta_color="normal" if taxa_sla >= 0.80 else "inverse")

    st.markdown("### Volume Diario — Tickets Abertos vs Encerrados")

    rec = df.groupby("data_ref").size().reset_index(name="Recebidos")
    res = (df[df["encerrado"] & df["fech_ref"].notna()]
           .groupby("fech_ref").size().reset_index(name="Encerrados"))
    rec.columns = ["data", "Recebidos"]
    res.columns = ["data", "Encerrados"]
    vol = rec.merge(res, on="data", how="outer").fillna(0).sort_values("data")

    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=vol["data"], y=vol["Recebidos"], name="Recebidos",
        line=dict(color=AZUL_CLARO, width=2),
        fill="tozeroy", fillcolor="rgba(41,128,185,0.1)",
    ))
    fig.add_trace(go.Scatter(
        x=vol["data"], y=vol["Encerrados"], name="Encerrados",
        line=dict(color="#27AE60", width=2),
    ))
    fig.update_layout(
        template=TEMPLATE, height=260,
        margin=dict(t=10, b=10, l=0, r=0),
        legend=dict(orientation="h", y=1.12),
    )
    st.plotly_chart(fig, use_container_width=True)

    col_a, col_b, col_c = st.columns(3)

    with col_a:
        st.markdown("### Por Status")
        s = df["status_ticket"].value_counts().reset_index()
        s.columns = ["Status", "Tickets"]
        fig = px.bar(s, x="Tickets", y="Status", orientation="h",
                     color="Status", color_discrete_sequence=CORES,
                     template=TEMPLATE, height=220, text_auto=True)
        fig.update_layout(showlegend=False, margin=dict(t=5, b=5, l=0, r=0))
        st.plotly_chart(fig, use_container_width=True)

    with col_b:
        st.markdown("### Por Prioridade")
        p = df["prioridade"].value_counts().reset_index()
        p.columns = ["Prioridade", "Tickets"]
        fig = px.pie(p, names="Prioridade", values="Tickets", hole=0.52,
                     color="Prioridade",
                     color_discrete_map={"High": "#E74C3C", "Medium": "#F39C12", "Low": "#27AE60"},
                     template=TEMPLATE, height=220)
        fig.update_layout(margin=dict(t=5, b=5, l=0, r=0),
                          legend=dict(orientation="h", y=-0.1))
        fig.update_traces(textposition="inside", textinfo="percent+label")
        st.plotly_chart(fig, use_container_width=True)

    with col_c:
        st.markdown("### Por Topico")
        t = df["topico"].value_counts().reset_index()
        t.columns = ["Topico", "Tickets"]
        fig = px.bar(t.sort_values("Tickets"), x="Tickets", y="Topico",
                     orientation="h", color="Tickets",
                     color_continuous_scale=["#AED6F1", AZUL],
                     template=TEMPLATE, height=220, text_auto=True)
        fig.update_layout(showlegend=False, coloraxis_showscale=False,
                          margin=dict(t=5, b=5, l=0, r=0))
        st.plotly_chart(fig, use_container_width=True)

with tab2:
    df_sla = df_sla_base.copy()

    cor_sla = VERDE if taxa_sla >= 0.80 else VERMELHO
    c1, c2, c3 = st.columns(3)
    c1.metric("Taxa Global de SLA",  f"{taxa_sla:.1%}",
              delta="Meta: 80%",
              delta_color="normal" if taxa_sla >= 0.80 else "inverse")
    c2.metric("Tickets Cumpriram",   f"{int(df_sla['cumpriu_sla'].sum()):,}")
    c3.metric("Tickets Violaram",    f"{int((~df_sla['cumpriu_sla']).sum()):,}")

    col_a, col_b = st.columns(2)

    with col_a:
        st.markdown("### SLA por Prioridade")
        sla_p = (df_sla.groupby("prioridade", observed=True)["cumpriu_sla"]
                 .agg(taxa="mean", n="count").reset_index())
        sla_p["label"] = sla_p["taxa"].map("{:.1%}".format)
        fig = px.bar(
            sla_p.sort_values("taxa"), y="prioridade", x="taxa",
            orientation="h", text="label",
            color="taxa", color_continuous_scale=["#E74C3C", "#F39C12", "#27AE60"],
            range_color=[0, 1], template=TEMPLATE, height=220,
        )
        fig.add_vline(x=0.8, line_dash="dash", line_color=CINZA,
                      annotation_text="Meta 80%", annotation_position="top right")
        fig.update_layout(xaxis_tickformat=".0%", coloraxis_showscale=False,
                          margin=dict(t=10, b=10, l=0, r=0))
        st.plotly_chart(fig, use_container_width=True)

    with col_b:
        st.markdown("### SLA por Origem")
        sla_o = (df_sla.groupby("origem_ticket")["cumpriu_sla"]
                 .agg(taxa="mean", n="count").reset_index())
        sla_o["label"] = sla_o["taxa"].map("{:.1%}".format)
        fig = px.bar(
            sla_o.sort_values("taxa"), y="origem_ticket", x="taxa",
            orientation="h", text="label",
            color="taxa", color_continuous_scale=["#E74C3C", "#F39C12", "#27AE60"],
            range_color=[0, 1], template=TEMPLATE, height=220,
        )
        fig.add_vline(x=0.8, line_dash="dash", line_color=CINZA)
        fig.update_layout(xaxis_tickformat=".0%", coloraxis_showscale=False,
                          margin=dict(t=10, b=10, l=0, r=0))
        st.plotly_chart(fig, use_container_width=True)

    st.markdown("### SLA por Analista")
    sla_an = (df_sla.groupby("analista_responsavel")["cumpriu_sla"]
              .agg(taxa="mean", n="count").reset_index()
              .sort_values("taxa"))
    sla_an["nome"] = sla_an["analista_responsavel"].str.split().str[0]
    sla_an["label"] = sla_an["taxa"].map("{:.1%}".format)
    fig = px.bar(
        sla_an, y="nome", x="taxa", orientation="h", text="label",
        color="taxa", color_continuous_scale=["#E74C3C", "#F39C12", "#27AE60"],
        range_color=[0.5, 1.0], template=TEMPLATE, height=300,
    )
    fig.add_vline(x=0.8, line_dash="dash", line_color=CINZA,
                  annotation_text="Meta 80%", annotation_position="top right")
    fig.update_layout(xaxis_tickformat=".0%", coloraxis_showscale=False,
                      margin=dict(t=10, b=10, l=0, r=0))
    st.plotly_chart(fig, use_container_width=True)

    col_c, col_d = st.columns(2)

    with col_c:
        st.markdown("### SLA por Topico")
        sla_t = (df_sla.groupby("topico")["cumpriu_sla"]
                 .mean().reset_index().rename(columns={"cumpriu_sla": "taxa"}))
        sla_t["label"] = sla_t["taxa"].map("{:.1%}".format)
        fig = px.bar(
            sla_t.sort_values("taxa"), y="topico", x="taxa",
            orientation="h", text="label",
            color="taxa", color_continuous_scale=["#E74C3C", "#27AE60"],
            range_color=[0, 1], template=TEMPLATE, height=280,
        )
        fig.add_vline(x=0.8, line_dash="dash", line_color=CINZA)
        fig.update_layout(xaxis_tickformat=".0%", coloraxis_showscale=False,
                          margin=dict(t=5, b=5, l=0, r=0))
        st.plotly_chart(fig, use_container_width=True)

    with col_d:
        st.markdown("### Evolucao Mensal do SLA")
        sla_m = (df_sla.groupby("mes")["cumpriu_sla"]
                 .mean().reset_index().rename(columns={"cumpriu_sla": "taxa"}))
        fig = go.Figure()
        fig.add_trace(go.Scatter(
            x=sla_m["mes"], y=sla_m["taxa"],
            mode="lines+markers",
            line=dict(color=AZUL_CLARO, width=2.5),
            marker=dict(size=7, color=AZUL_CLARO),
            fill="tozeroy", fillcolor="rgba(41,128,185,0.08)",
        ))
        fig.add_hline(y=0.8, line_dash="dash", line_color=VERMELHO,
                      annotation_text="Meta 80%")
        fig.update_layout(
            template=TEMPLATE, height=280,
            yaxis_tickformat=".0%", yaxis_range=[0, 1.05],
            margin=dict(t=5, b=5, l=0, r=0),
        )
        st.plotly_chart(fig, use_container_width=True)

with tab3:
    df_enc = df[df["encerrado"] & df["tempo_resolucao_horas"].notna()].copy()

    if len(df_enc) == 0:
        st.info("Sem tickets encerrados no periodo filtrado.")
    else:
        perf = (df_enc.groupby("analista_responsavel")
                .agg(
                    tempo_medio=("tempo_resolucao_horas", "mean"),
                    tickets=("encerrado", "count"),
                    taxa_sla=("cumpriu_sla", "mean"),
                )
                .reset_index()
                .rename(columns={
                    "analista_responsavel": "Analista",
                    "tempo_medio": "Tempo Medio (h)",
                    "tickets": "Tickets",
                    "taxa_sla": "Taxa SLA",
                }))
        perf["nome"] = perf["Analista"].str.split().str[0]
        perf_tempo = perf.sort_values("Tempo Medio (h)")
        perf_vol   = perf.sort_values("Tickets")

        col_a, col_b = st.columns(2)

        with col_a:
            st.markdown("### Tempo Medio de Resolucao por Analista (h)")
            fig = px.bar(
                perf_tempo, y="nome", x="Tempo Medio (h)",
                orientation="h", text_auto=".1f",
                color="Tempo Medio (h)",
                color_continuous_scale=["#27AE60", "#F39C12", "#E74C3C"],
                template=TEMPLATE, height=320,
            )
            fig.update_layout(coloraxis_showscale=False,
                              margin=dict(t=5, b=5, l=0, r=0))
            st.plotly_chart(fig, use_container_width=True)

        with col_b:
            st.markdown("### Volume de Tickets Encerrados")
            fig = px.bar(
                perf_vol, y="nome", x="Tickets",
                orientation="h", text_auto=True,
                color="Tickets",
                color_continuous_scale=["#AED6F1", AZUL],
                template=TEMPLATE, height=320,
            )
            fig.update_layout(coloraxis_showscale=False,
                              margin=dict(t=5, b=5, l=0, r=0))
            st.plotly_chart(fig, use_container_width=True)

        st.markdown("### Eficiencia: Volume x Velocidade x SLA")
        st.caption("Tamanho da bolha = volume de tickets  ·  Cor = taxa de SLA")
        fig = px.scatter(
            perf,
            x="Tickets", y="Tempo Medio (h)",
            text="nome",
            size="Tickets", size_max=45,
            color="Taxa SLA",
            color_continuous_scale=["#E74C3C", "#F39C12", "#27AE60"],
            range_color=[0.5, 1.0],
            template=TEMPLATE, height=360,
            labels={"Tickets": "Volume de Tickets", "Tempo Medio (h)": "Tempo Medio (h)"},
        )
        fig.update_traces(textposition="top center", marker=dict(opacity=0.85))
        fig.update_layout(coloraxis_colorbar=dict(title="SLA", tickformat=".0%"),
                          margin=dict(t=10, b=10, l=0, r=0))
        st.plotly_chart(fig, use_container_width=True)

        st.markdown("### Tabela Detalhada")
        tabela = perf[["Analista", "Tickets", "Tempo Medio (h)", "Taxa SLA"]].copy()
        tabela["Tempo Medio (h)"] = tabela["Tempo Medio (h)"].round(1)
        tabela["Taxa SLA"] = (tabela["Taxa SLA"] * 100).round(1).astype(str) + "%"
        st.dataframe(
            tabela.sort_values("Tickets", ascending=False),
            use_container_width=True,
            hide_index=True,
            column_config={
                "Tickets":         st.column_config.NumberColumn(format="%d"),
                "Tempo Medio (h)": st.column_config.NumberColumn(format="%.1f h"),
            },
        )

with tab4:
    backlog_atual = int((~df["encerrado"]).sum())
    recebidos_p   = total
    encerrados_p  = encerrados

    c1, c2, c3 = st.columns(3)
    c1.metric("Backlog Atual",       f"{backlog_atual:,}",
              delta=f"{backlog_atual - encerrados_p:+,} vs encerrados",
              delta_color="inverse")
    c2.metric("Recebidos no Periodo", f"{recebidos_p:,}")
    c3.metric("Encerrados no Periodo", f"{encerrados_p:,}")

    st.markdown("### Backlog Acumulado ao Longo do Tempo")

    rec_d = df.groupby("data_ref").size().reset_index(name="rec")
    res_d = (df[df["encerrado"] & df["fech_ref"].notna()]
             .groupby("fech_ref").size().reset_index(name="res"))
    rec_d.columns = ["data", "rec"]
    res_d.columns = ["data", "res"]
    saldo = rec_d.merge(res_d, on="data", how="outer").fillna(0).sort_values("data")
    saldo["backlog"] = (saldo["rec"] - saldo["res"]).cumsum()

    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=saldo["data"], y=saldo["backlog"],
        fill="tozeroy",
        fillcolor="rgba(146,43,33,0.12)",
        line=dict(color=VERMELHO, width=2),
        name="Backlog Acumulado",
    ))
    fig.add_hline(y=0, line_color=CINZA, line_width=1)
    fig.update_layout(
        template=TEMPLATE, height=260,
        yaxis_title="Tickets em aberto (acumulado)",
        margin=dict(t=10, b=10, l=0, r=0),
    )
    st.plotly_chart(fig, use_container_width=True)

    col_a, col_b = st.columns(2)

    with col_a:
        st.markdown("### Volume Mensal — Recebidos vs Encerrados")
        mensal_rec = df.groupby("mes").size().reset_index(name="Recebidos")
        mensal_res = (df[df["encerrado"]]
                      .groupby("mes").size().reset_index(name="Encerrados"))
        mensal = mensal_rec.merge(mensal_res, on="mes", how="left").fillna(0)

        fig = go.Figure()
        fig.add_trace(go.Bar(x=mensal["mes"], y=mensal["Recebidos"],
                             name="Recebidos", marker_color=AZUL_CLARO))
        fig.add_trace(go.Bar(x=mensal["mes"], y=mensal["Encerrados"],
                             name="Encerrados", marker_color="#27AE60"))
        fig.update_layout(
            template=TEMPLATE, height=300, barmode="group",
            legend=dict(orientation="h", y=1.12),
            margin=dict(t=10, b=10, l=0, r=0),
        )
        fig.update_xaxes(tickangle=45)
        st.plotly_chart(fig, use_container_width=True)

    with col_b:
        st.markdown("### Volume por Origem e Topico")
        origem_topico = (df.groupby(["origem_ticket", "topico"])
                         .size().reset_index(name="Tickets"))
        fig = px.bar(
            origem_topico, x="origem_ticket", y="Tickets",
            color="topico", barmode="stack",
            color_discrete_sequence=CORES,
            template=TEMPLATE, height=300,
            labels={"origem_ticket": "Origem", "topico": "Topico"},
        )
        fig.update_layout(
            legend=dict(orientation="h", y=1.12, font=dict(size=10)),
            margin=dict(t=10, b=10, l=0, r=0),
        )
        st.plotly_chart(fig, use_container_width=True)

    st.markdown("### Distribuicao do Tempo de Resolucao por Prioridade")
    df_box = df[df["encerrado"] & df["tempo_resolucao_horas"].notna()].copy()
    df_box["prioridade"] = df_box["prioridade"].astype(str)
    fig = px.box(
        df_box, x="prioridade", y="tempo_resolucao_horas",
        color="prioridade",
        color_discrete_map={"High": "#E74C3C", "Medium": "#F39C12", "Low": "#27AE60"},
        template=TEMPLATE, height=300,
        labels={"prioridade": "Prioridade", "tempo_resolucao_horas": "Horas ate Encerramento"},
        category_orders={"prioridade": ["High", "Medium", "Low"]},
    )
    fig.update_layout(showlegend=False, margin=dict(t=10, b=10, l=0, r=0))
    st.plotly_chart(fig, use_container_width=True)
