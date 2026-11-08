import unittest

from src.regras import analisar_condicoes


class TestRegrasAgroFacil(unittest.TestCase):

    def criar_clima(self, previsao):
        return {"previsao": previsao}

    def test_risco_de_geada(self):
        clima = self.criar_clima([
            {
                "temperatura_minima": 1,
                "temperatura_maxima": 15,
                "precipitacao": 10
            }
        ])

        resultado = analisar_condicoes(clima)

        self.assertIn("Risco de geada", resultado["alertas"])

    def test_risco_de_chuva_forte(self):
        clima = self.criar_clima([
            {
                "temperatura_minima": 15,
                "temperatura_maxima": 25,
                "precipitacao": 25
            }
        ])

        resultado = analisar_condicoes(clima)

        self.assertIn(
            "Previsão de chuva forte",
            resultado["alertas"]
        )

    def test_risco_de_seca(self):
        clima = self.criar_clima([
            {
                "temperatura_minima": 20,
                "temperatura_maxima": 32,
                "precipitacao": 1
            },
            {
                "temperatura_minima": 21,
                "temperatura_maxima": 31,
                "precipitacao": 1
            },
            {
                "temperatura_minima": 22,
                "temperatura_maxima": 30,
                "precipitacao": 1
            }
        ])

        resultado = analisar_condicoes(clima)

        self.assertIn(
            "Possível risco de seca",
            resultado["alertas"]
        )

    def test_baixa_previsao_de_chuva(self):
        clima = self.criar_clima([
            {
                "temperatura_minima": 15,
                "temperatura_maxima": 25,
                "precipitacao": 1
            },
            {
                "temperatura_minima": 16,
                "temperatura_maxima": 26,
                "precipitacao": 1
            },
            {
                "temperatura_minima": 17,
                "temperatura_maxima": 27,
                "precipitacao": 1
            }
        ])

        resultado = analisar_condicoes(clima)

        self.assertIn(
            "Baixa previsão de chuva",
            resultado["alertas"]
        )

    def test_nenhum_risco_identificado(self):
        clima = self.criar_clima([
            {
                "temperatura_minima": 15,
                "temperatura_maxima": 25,
                "precipitacao": 10
            },
            {
                "temperatura_minima": 16,
                "temperatura_maxima": 26,
                "precipitacao": 8
            }
        ])

        resultado = analisar_condicoes(clima)

        self.assertIn(
            "Nenhum risco identificado",
            resultado["alertas"]
        )

    def test_previsao_vazia(self):
        clima = self.criar_clima([])

        with self.assertRaises(ValueError):
            analisar_condicoes(clima)


if __name__ == "__main__":
    unittest.main()
