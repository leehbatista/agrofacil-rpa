
import csv
import logging

ARQUIVO_PRODUTORES = "data/produtores.csv"


def carregar_produtores():
    produtores_validos = []
    produtores_invalidos = []

    try:
        with open(ARQUIVO_PRODUTORES, "r", encoding="utf-8") as arquivo:
            leitor = csv.DictReader(arquivo)

            campos_obrigatorios = {
                "id", "nome", "cultura", "latitude", "longitude"
            }

            if not leitor.fieldnames or not campos_obrigatorios.issubset(leitor.fieldnames):
                raise ValueError("Cabeçalho do CSV inválido.")

            ids_processados = set()

            for linha in leitor:
                try:
                    produtor_id = (linha.get("id") or "").strip()
                    nome = (linha.get("nome") or "").strip()
                    cultura = (linha.get("cultura") or "").strip()

                    if not produtor_id or not nome or not cultura:
                        raise ValueError("Campo obrigatório vazio.")

                    latitude = float(linha.get("latitude") or "")
                    longitude = float(linha.get("longitude") or "")

                    if produtor_id in ids_processados:
                        raise ValueError("ID de produtor duplicado.")

                    if not -90 <= latitude <= 90:
                        raise ValueError("Latitude inválida.")

                    if not -180 <= longitude <= 180:
                        raise ValueError("Longitude inválida.")

                    ids_processados.add(produtor_id)

                    produtores_validos.append({
                        "id": produtor_id,
                        "nome": nome,
                        "cultura": cultura,
                        "latitude": latitude,
                        "longitude": longitude
                    })

                except (ValueError, TypeError, AttributeError) as erro:
                    produtores_invalidos.append({
                        "id": (linha.get("id") or "Não identificado"),
                        "erro": str(erro)
                    })

        logging.info(
            "Cadastro processado: %d válidos e %d inválidos.",
            len(produtores_validos),
            len(produtores_invalidos)
        )

        return produtores_validos, produtores_invalidos

    except FileNotFoundError:
        logging.error("Arquivo de produtores não encontrado.")
        raise

    except OSError:
        logging.exception("Erro ao acessar o arquivo de produtores.")
        raise
