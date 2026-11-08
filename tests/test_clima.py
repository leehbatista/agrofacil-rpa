
import unittest
from unittest.mock import patch, Mock

import requests

from src.clima import consultar_clima


class TestClima(unittest.TestCase):

    def test_consulta_clima_sucesso(self):
        resposta = Mock()

        resposta.json.return_value = {
            "current": {
                "temperature_2m": 25,
                "precipitation": 1
            },
            "daily": {
                "time": ["2026-11-06"],
                "temperature_2m_min": [18],
                "temperature_2m_max": [30],
                "precipitation_sum": [5]
            }
        }

        with patch(
            "src.clima.requests.get",
            return_value=resposta
        ):
            resultado = consultar_clima(-23.5, -46.6)

        self.assertEqual(resultado["temperatura_atual"], 25)
        self.assertEqual(len(resultado["previsao"]), 1)

    def test_tempo_limite_da_api(self):
        with patch(
            "src.clima.requests.get",
            side_effect=requests.exceptions.Timeout
        ):
            with self.assertRaises(Exception) as contexto:
                consultar_clima(-23.5, -46.6)

        self.assertIn(
            "Tempo limite",
            str(contexto.exception)
        )

    def test_falha_na_conexao_com_api(self):
        with patch(
            "src.clima.requests.get",
            side_effect=requests.exceptions.ConnectionError
        ):
            with self.assertRaises(Exception) as contexto:
                consultar_clima(-23.5, -46.6)

        self.assertIn(
            "Erro na consulta meteorológica",
            str(contexto.exception)
        )

    def test_resposta_api_incompleta(self):
        resposta = Mock()

        resposta.json.return_value = {
            "current": {
                "temperature_2m": 25,
                "precipitation": 1
            }
        }

        with patch(
            "src.clima.requests.get",
            return_value=resposta
        ):
            with self.assertRaises(ValueError):
                consultar_clima(-23.5, -46.6)

    def test_previsao_com_dados_inconsistentes(self):
        resposta = Mock()

        resposta.json.return_value = {
            "current": {
                "temperature_2m": 25,
                "precipitation": 1
            },
            "daily": {
                "time": ["2026-11-06", "2026-11-07"],
                "temperature_2m_min": [18],
                "temperature_2m_max": [30, 29],
                "precipitation_sum": [5, 8]
            }
        }

        with patch(
            "src.clima.requests.get",
            return_value=resposta
        ):
            with self.assertRaises(ValueError):
                consultar_clima(-23.5, -46.6)


if __name__ == "__main__":
    unittest.main()
