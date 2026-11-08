import json
import logging
from pathlib import Path
from datetime import datetime

from src.processador import carregar_produtores
from src.clima import consultar_clima
from src.regras import analisar_condicoes
from src.logger_config import configurar_logging


def main():
    configurar_logging()

    logging.info("=== INÍCIO DA EXECUÇÃO DO AGROFÁCIL ===")

    produtores, invalidos = carregar_produtores()

    resultados = []
    falhas = []

    total_cadastrados = len(produtores) + len(invalidos)

    logging.info(
        "Cadastros carregados: %d válidos e %d inválidos.",
        len(produtores),
        len(invalidos)
    )

    for produtor_invalido in invalidos:
        logging.warning(
            "Cadastro inválido. ID: %s | Erro: %s",
            produtor_invalido["id"],
            produtor_invalido["erro"]
        )

    print("\n=== AGROFÁCIL RPA ===")
    print(f"\nTotal de cadastros: {total_cadastrados}")
    print(f"Produtores válidos: {len(produtores)}")
    print(f"Produtores inválidos: {len(invalidos)}")

    for produtor in produtores:
        print(f"\nProdutor: {produtor['nome']}")
        print(f"Cultura: {produtor['cultura']}")

        try:
            clima = consultar_clima(
                produtor["latitude"],
                produtor["longitude"]
            )

            resultado = analisar_condicoes(clima)

            resultados.append({
                "id": produtor["id"],
                "nome": produtor["nome"],
                "cultura": produtor["cultura"],
                "clima": clima,
                "analise": resultado
            })

            logging.info(
                "Produtor %s processado com sucesso.",
                produtor["id"]
            )

            print(
                f"Temperatura atual: "
                f"{clima['temperatura_atual']} °C"
            )

            print("\nAlertas:")
            for alerta in resultado["alertas"]:
                print(f"- {alerta}")

            print("\nRecomendações:")
            for recomendacao in resultado["recomendacoes"]:
                print(f"- {recomendacao}")

        except Exception as erro:
            logging.exception(
                "Falha ao processar produtor %s.",
                produtor["id"]
            )

            print(f"Falha no processamento: {erro}")

            falhas.append({
                "id": produtor["id"],
                "nome": produtor["nome"],
                "erro": str(erro)
            })

    dados_saida = {
        "data_execucao": datetime.now().astimezone().isoformat(
            timespec="seconds"
        ),
        "total_produtores": total_cadastrados,
        "total_validos": len(produtores),
        "total_processados": len(resultados),
        "total_invalidos": len(invalidos),
        "total_falhas": len(falhas),
        "produtores_invalidos": invalidos,
        "falhas": falhas,
        "resultados": resultados
    }

    pasta_saida = Path(__file__).resolve().parent.parent / "outputs"
    arquivo_saida = pasta_saida / "analise_climatica.json"

    try:
        pasta_saida.mkdir(parents=True, exist_ok=True)

        with open(arquivo_saida, "w", encoding="utf-8") as arquivo:
            json.dump(
                dados_saida,
                arquivo,
                ensure_ascii=False,
                indent=4
            )

        logging.info("Arquivo JSON salvo com sucesso.")

        print(f"\nResultados salvos em: {arquivo_saida}")

    except OSError:
        logging.exception("Erro ao criar pasta ou salvar o arquivo JSON.")
        raise

    logging.info(
        "Execução finalizada. "
        "Processados: %d | Inválidos: %d | Falhas: %d",
        len(resultados),
        len(invalidos),
        len(falhas)
    )

    print("\n=== RESUMO DA EXECUÇÃO ===")
    print(f"Processados com sucesso: {len(resultados)}")
    print(f"Cadastros inválidos: {len(invalidos)}")
    print(f"Falhas de processamento: {len(falhas)}")
    print("\nExecução finalizada!")


if __name__ == "__main__":
    main()
