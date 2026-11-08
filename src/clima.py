import requests

URL_API = "https://api.open-meteo.com/v1/forecast"


def consultar_clima(latitude, longitude):
    parametros = {
        "latitude": latitude,
        "longitude": longitude,
        "current": "temperature_2m,precipitation",
        "daily": "temperature_2m_min,temperature_2m_max,precipitation_sum",
        "forecast_days": 3,
        "timezone": "auto"
    }

    try:
        resposta = requests.get(
            URL_API,
            params=parametros,
            timeout=15
        )

        resposta.raise_for_status()

        dados = resposta.json()

        if not isinstance(dados, dict):
            raise ValueError("Resposta da API inválida.")

        if "current" not in dados or "daily" not in dados:
            raise ValueError("Resposta da API incompleta.")

        atual = dados["current"]
        previsao = dados["daily"]

        campos_atual = [
            "temperature_2m",
            "precipitation"
        ]

        campos_diarios = [
            "time",
            "temperature_2m_min",
            "temperature_2m_max",
            "precipitation_sum"
        ]

        if not isinstance(atual, dict) or not isinstance(previsao, dict):
            raise ValueError("Estrutura dos dados meteorológicos inválida.")

        if not all(campo in atual for campo in campos_atual):
            raise ValueError("Dados climáticos atuais incompletos.")

        if not all(campo in previsao for campo in campos_diarios):
            raise ValueError("Dados da previsão incompletos.")

        datas = previsao["time"]

        if not isinstance(datas, list) or not datas:
            raise ValueError("Previsão meteorológica vazia.")

        if any(
            not isinstance(previsao[campo], list)
            or len(previsao[campo]) != len(datas)
            for campo in campos_diarios[1:]
        ):
            raise ValueError("Dados da previsão inconsistentes.")

        clima = {
            "temperatura_atual": float(atual["temperature_2m"]),
            "precipitacao_atual": float(atual["precipitation"]),
            "previsao": []
        }

        for i in range(len(datas)):
            dia = {
                "data": datas[i],
                "temperatura_minima": float(
                    previsao["temperature_2m_min"][i]
                ),
                "temperatura_maxima": float(
                    previsao["temperature_2m_max"][i]
                ),
                "precipitacao": float(
                    previsao["precipitation_sum"][i]
                )
            }

            clima["previsao"].append(dia)

        return clima

    except requests.exceptions.Timeout:
        raise Exception("Tempo limite da consulta climática excedido.")

    except requests.exceptions.RequestException as erro:
        raise Exception(f"Erro na consulta meteorológica: {erro}")

    except (KeyError, TypeError, ValueError) as erro:
        raise ValueError(
            f"Erro nos dados retornados pela API: {erro}"
        )
