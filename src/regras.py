def analisar_condicoes(clima):
    previsao = clima.get("previsao", [])

    if not previsao:
        raise ValueError("Previsão climática não encontrada.")

    alertas = []
    recomendacoes = []

    chuva_acumulada = sum(
        dia["precipitacao"] for dia in previsao
    )

    maior_temperatura = max(
        dia["temperatura_maxima"] for dia in previsao
    )

    menor_temperatura = min(
        dia["temperatura_minima"] for dia in previsao
    )

    # Regra 1: risco de geada
    if menor_temperatura <= 2:
        alertas.append("Risco de geada")
        recomendacoes.append(
            "Proteger a plantação contra possíveis danos causados pelo frio."
        )

    # Regra 2: risco de chuva forte
    dias_chuva_forte = [
        dia for dia in previsao
        if dia["precipitacao"] >= 20
    ]

    if dias_chuva_forte:
        alertas.append("Previsão de chuva forte")
        recomendacoes.append(
            "Monitorar a plantação e verificar as condições de drenagem."
        )

    # Regra 3: possível seca
    if chuva_acumulada < 5 and maior_temperatura >= 30:
        alertas.append("Possível risco de seca")
        recomendacoes.append(
            "Monitorar a umidade do solo e avaliar a necessidade de irrigação."
        )

    # Regra 4: pouca chuva
    elif chuva_acumulada < 5:
        alertas.append("Baixa previsão de chuva")
        recomendacoes.append(
            "Avaliar a necessidade de irrigação da plantação."
        )

    if not alertas:
        alertas.append("Nenhum risco identificado")
        recomendacoes.append(
            "Manter o monitoramento das condições climáticas."
        )

    return {
        "alertas": alertas,
        "recomendacoes": recomendacoes,
        "chuva_acumulada_3_dias": round(chuva_acumulada, 2),
        "temperatura_minima_prevista": menor_temperatura,
        "temperatura_maxima_prevista": maior_temperatura
    }
