"""
Painel AgroFácil - componente que CONSOME o resultado da automação.

Lê o arquivo outputs/analise_climatica.json (gerado pelo src/main.py),
valida a estrutura e gera o painel outputs/painel.html com os alertas
e recomendações de cada produtor.
"""
import json
import logging
import webbrowser
from html import escape
from pathlib import Path

from src.logger_config import configurar_logging

RAIZ = Path(__file__).resolve().parent.parent
ARQUIVO_JSON = RAIZ / "outputs" / "analise_climatica.json"
ARQUIVO_HTML = RAIZ / "outputs" / "painel.html"


def carregar_resultados():
    """Lê e valida o JSON gerado pela automação."""
    try:
        with open(ARQUIVO_JSON, "r", encoding="utf-8") as arquivo:
            dados = json.load(arquivo)
    except FileNotFoundError:
        logging.error("Painel: arquivo JSON não encontrado. Execute src.main antes.")
        raise
    except json.JSONDecodeError:
        logging.exception("Painel: o arquivo JSON está corrompido.")
        raise

    if not isinstance(dados, dict) or "resultados" not in dados:
        raise ValueError("JSON fora do formato esperado (campo 'resultados' ausente).")

    return dados


def classe_do_alerta(alerta):
    """Define a cor do alerta conforme o tipo de risco."""
    texto = alerta.lower()
    if "nenhum" in texto:
        return "ok"
    if "geada" in texto or "chuva forte" in texto:
        return "critico"
    return "atencao"


def montar_card(item):
    analise = item["analise"]
    clima = item["clima"]

    alertas = "".join(
        f'<span class="alerta {classe_do_alerta(a)}">{escape(a)}</span>'
        for a in analise["alertas"]
    )
    recomendacoes = "".join(
        f"<li>{escape(r)}</li>" for r in analise["recomendacoes"]
    )
    linhas = "".join(
        f"<tr><td>{escape(dia['data'])}</td>"
        f"<td>{dia['temperatura_minima']} °C</td>"
        f"<td>{dia['temperatura_maxima']} °C</td>"
        f"<td>{dia['precipitacao']} mm</td></tr>"
        for dia in clima["previsao"]
    )

    return f"""
    <article class="card">
      <h2>{escape(item['nome'])}
        <small>{escape(item['id'])} · {escape(item['cultura'])}</small></h2>
      <p class="temp">Temperatura atual: <strong>{clima['temperatura_atual']} °C</strong></p>
      <div>{alertas}</div>
      <h3>Recomendações</h3>
      <ul>{recomendacoes}</ul>
      <table>
        <caption>Previsão dos próximos dias</caption>
        <thead><tr><th>Data</th><th>Mínima</th><th>Máxima</th><th>Chuva</th></tr></thead>
        <tbody>{linhas}</tbody>
      </table>
    </article>"""


def gerar_html(dados):
    cards = "".join(montar_card(item) for item in dados["resultados"])

    avisos = ""
    for falha in dados.get("falhas", []):
        avisos += (
            f"<p class='aviso'>Falha ao consultar {escape(str(falha.get('nome')))}: "
            f"{escape(str(falha.get('erro')))}</p>"
        )
    for inv in dados.get("produtores_invalidos", []):
        avisos += (
            f"<p class='aviso'>Cadastro inválido {escape(str(inv.get('id')))}: "
            f"{escape(str(inv.get('erro')))}</p>"
        )

    return f"""<!DOCTYPE html>
<html lang="pt-BR">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Painel AgroFácil</title>
<style>
  body {{ font-family: Arial, sans-serif; background:#f3f6f1; color:#1d2b1d; margin:0; }}
  header {{ background:#2e6b34; color:#fff; padding:20px 28px; }}
  header p {{ margin:4px 0 0; }}
  main {{ padding:24px; display:grid; gap:18px;
          grid-template-columns:repeat(auto-fit,minmax(320px,1fr)); }}
  .card {{ background:#fff; border-radius:10px; padding:18px;
           box-shadow:0 1px 4px rgba(0,0,0,.15); }}
  .card h2 {{ margin:0 0 6px; font-size:20px; }}
  .card small {{ display:block; color:#4a5a4a; font-size:13px; font-weight:normal; }}
  .alerta {{ display:inline-block; padding:5px 10px; border-radius:14px;
             margin:2px 4px 2px 0; font-weight:bold; font-size:14px; }}
  .ok {{ background:#d8f0d8; color:#14501a; }}
  .atencao {{ background:#ffe9b8; color:#6b4300; }}
  .critico {{ background:#ffd2d2; color:#7a0f0f; }}
  table {{ width:100%; border-collapse:collapse; margin-top:12px; font-size:14px; }}
  caption {{ text-align:left; font-weight:bold; padding-bottom:4px; }}
  th, td {{ border-bottom:1px solid #dde5dd; padding:5px; text-align:left; }}
  .aviso {{ background:#fff3cd; padding:10px 28px; margin:0; }}
</style>
</head>
<body>
<header>
  <h1>Painel AgroFácil</h1>
  <p>Dados gerados pela automação em {escape(str(dados.get('data_execucao', '-')))}
     · Processados: {dados.get('total_processados', 0)}
     · Inválidos: {dados.get('total_invalidos', 0)}
     · Falhas: {dados.get('total_falhas', 0)}</p>
</header>
{avisos}
<main>{cards}</main>
</body>
</html>"""


def main():
    configurar_logging()
    logging.info("=== PAINEL: início da leitura do JSON da automação ===")

    dados = carregar_resultados()
    html_final = gerar_html(dados)

    ARQUIVO_HTML.parent.mkdir(parents=True, exist_ok=True)
    with open(ARQUIVO_HTML, "w", encoding="utf-8") as arquivo:
        arquivo.write(html_final)

    logging.info(
        "Painel gerado com %d produtores a partir do JSON.",
        len(dados["resultados"])
    )
    print(f"Painel gerado com {len(dados['resultados'])} produtores: {ARQUIVO_HTML}")

    webbrowser.open(ARQUIVO_HTML.as_uri())


if __name__ == "__main__":
    main()