# -*- coding: utf-8 -*-
"""Monta um HTML auto-contido (imagens em base64) para impressao em PDF."""
import base64
from pathlib import Path

base = Path(__file__).resolve().parent
img = base / "img"

def b64(nome):
    return base64.b64encode((img / nome).read_bytes()).decode()

mer = b64("01_MER.png")
classe = b64("02_DIAGRAMA_CLASSE.png")
uso = b64("03_CASO_DE_USO.png")

html = f"""<!DOCTYPE html>
<html lang="pt-br">
<head>
<meta charset="utf-8">
<style>
  @page {{ size: A4; margin: 18mm 16mm; }}
  * {{ box-sizing: border-box; }}
  body {{ font-family: 'Segoe UI', Arial, sans-serif; color: #1f2430; font-size: 11pt; line-height: 1.5; }}
  h1 {{ color: #4b3fa7; font-size: 22pt; margin: 0 0 4px; }}
  h2 {{ color: #4b3fa7; font-size: 16pt; border-bottom: 2px solid #e3e0f5; padding-bottom: 4px; margin: 0 0 10px; }}
  h3 {{ color: #2d2a45; font-size: 12pt; margin: 14px 0 4px; }}
  .sub {{ color: #6a6a7a; font-size: 11pt; margin: 0 0 18px; }}
  .capa {{ text-align: center; padding-top: 60mm; page-break-after: always; }}
  .capa h1 {{ font-size: 28pt; }}
  .capa .meta {{ margin-top: 24px; color: #555; font-size: 12pt; }}
  .badge {{ display: inline-block; background: #efedfb; color: #4b3fa7; border-radius: 6px;
            padding: 2px 10px; font-size: 10pt; margin-top: 16px; }}
  section {{ page-break-before: always; }}
  .fig {{ text-align: center; margin: 14px 0; }}
  .fig img {{ max-width: 100%; max-height: 115mm; border: 1px solid #e3e0f5; border-radius: 6px; padding: 6px; }}
  .quote {{ background: #f6f5fc; border-left: 4px solid #6c5ce7; padding: 10px 14px;
            border-radius: 4px; font-style: italic; color: #33334d; margin: 10px 0; }}
  ul {{ margin: 6px 0 6px 0; padding-left: 20px; }}
  li {{ margin: 2px 0; }}
  .tag {{ font-weight: 600; color: #4b3fa7; }}
  table {{ border-collapse: collapse; width: 100%; font-size: 10pt; margin: 8px 0; }}
  th, td {{ border: 1px solid #d9d6ec; padding: 5px 8px; text-align: left; }}
  th {{ background: #efedfb; color: #2d2a45; }}
  .foot {{ color: #8a8a9a; font-size: 9pt; text-align: center; margin-top: 8px; }}
</style>
</head>
<body>

<div class="capa">
  <h1>Documentação de Modelagem</h1>
  <div class="sub">Projeto de BI — Análise de Capacidade Operacional<br>Equipe de Suporte Técnico</div>
  <div class="badge">MER &nbsp;•&nbsp; Diagrama de Classes &nbsp;•&nbsp; Diagrama de Casos de Uso</div>
  <div class="meta">
    Anderson Santos<br>
    github.com/AndersondSFonseca/Projeto-Capacidade-Operacional
  </div>
</div>

<section>
  <h2>1. Modelo de Dados (MER)</h2>
  <p class="sub">Modelo dimensional (esquema estrela) da base de tickets de suporte (~2.330 registros).</p>
  <div class="fig"><img src="data:image/png;base64,{mer}"></div>

  <h3>O que é</h3>
  <p>Modelo de dados desenhado como <b>esquema estrela</b>, padrão de Business Intelligence: no
  centro a tabela <b>Fato</b> (os tickets e suas métricas) e ao redor as <b>Dimensões</b> (atributos
  descritivos usados para filtrar e agrupar as análises).</p>

  <h3>Componentes</h3>
  <ul>
    <li><span class="tag">FATO_TICKET</span> — 1 linha = 1 ticket. Guarda as métricas (tempo de
    resolução, SLA, satisfação, interações) e as chaves para as dimensões.</li>
    <li><span class="tag">Dimensões</span> — Tempo (abertura/fechamento), Analista, Prioridade,
    Status, Origem, Tópico, Produto e Localização.</li>
  </ul>

  <h3>Cardinalidade</h3>
  <p>Todos os relacionamentos são <b>1:N (um-para-muitos)</b>: cada dimensão descreve muitos tickets;
  cada ticket aponta para uma única ocorrência de cada dimensão.</p>

  <h3>Como apresentar</h3>
  <div class="quote">"Este é o modelo de dados em esquema estrela. No centro a tabela Fato, com um
  registro por ticket e todas as métricas — tempo de resolução, SLA e satisfação. Ao redor, as
  dimensões, que são os filtros do dashboard: analista, prioridade, tempo, canal, tópico e
  localização. A relação é sempre um-para-muitos. É esse modelo que permite cruzar os dados."</div>
</section>

<section>
  <h2>2. Diagrama de Classes</h2>
  <p class="sub">Arquitetura do código-fonte em Python, organizada em camadas (pipeline de dados).</p>
  <div class="fig"><img src="data:image/png;base64,{classe}"></div>

  <h3>O que é</h3>
  <p>Representa os <b>módulos do código</b>, seus métodos e as <b>dependências</b> entre eles. Mostra
  que o projeto é uma solução organizada, com separação de responsabilidades.</p>

  <h3>O fluxo do dado (pipeline)</h3>
  <ul>
    <li><span class="tag">Dados (data_loader)</span> — lê o CSV bruto.</li>
    <li><span class="tag">DataProcessing</span> — ETL: traduz colunas, limpa, converte datas, calcula tempos.</li>
    <li><span class="tag">Metrics</span> — volume recebido/resolvido, tempo médio, performance, backlog.</li>
    <li><span class="tag">AnalysisExport / AnalysisVisuals</span> — exportam CSVs e gráficos.</li>
    <li><span class="tag">Dashboard (app.py)</span> — apresenta tudo no painel Streamlit.</li>
    <li><span class="tag">Main</span> — orquestra o pipeline de tratamento.</li>
  </ul>
  <p>As setas tracejadas significam "usa / depende de".</p>

  <h3>Como apresentar</h3>
  <div class="quote">"Aqui está a arquitetura do código em camadas. O dado entra pelo data_loader,
  passa pelo tratamento no data_processing, vira métrica no metrics e é apresentado no dashboard.
  Cada módulo tem uma responsabilidade única — isso deixa o projeto fácil de manter e testar."</div>
</section>

<section>
  <h2>3. Diagrama de Casos de Uso</h2>
  <p class="sub">Visão de negócio: quem usa o sistema e o que cada ator consegue fazer.</p>
  <div class="fig"><img src="data:image/png;base64,{uso}"></div>

  <h3>O que é</h3>
  <p>Mostra os <b>atores</b> e os <b>casos de uso</b> dentro da fronteira do sistema. Responde "para
  que serve e para quem", do ponto de vista do usuário.</p>

  <h3>Componentes</h3>
  <table>
    <tr><th>Ator</th><th>O que faz</th></tr>
    <tr><td>Gestor / Coordenador de Suporte</td><td>Visualiza KPIs, analisa SLA, avalia performance dos analistas, monitora backlog e identifica risco de gargalo.</td></tr>
    <tr><td>Analista de Dados</td><td>Executa o tratamento de dados (ETL) e exporta métricas e gráficos.</td></tr>
  </table>
  <p><b>«include»</b>: um caso sempre usa outro (monitorar backlog inclui avaliar o risco).<br>
  <b>«extend»</b>: um caso opcional estende outro (exportar estende o ETL).</p>

  <h3>Como apresentar</h3>
  <div class="quote">"Este diagrama mostra quem usa o sistema. O Gestor usa o dashboard para ver KPIs,
  acompanhar SLA, avaliar a performance e monitorar o backlog. O Analista de Dados cuida do pipeline:
  roda o ETL e exporta as métricas. É a visão de negócio do projeto."</div>
  <div class="foot">Projeto Capacidade Operacional — documentação gerada para a entrega acadêmica.</div>
</section>

</body>
</html>"""

saida = base / "Diagramas_Capacidade_Operacional.html"
saida.write_text(html, encoding="utf-8")
print(f"HTML gerado: {saida}")
