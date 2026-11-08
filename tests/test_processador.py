
import unittest
from unittest.mock import mock_open, patch

from src.processador import carregar_produtores


class TestProcessador(unittest.TestCase):

    def test_carregar_produtor_valido(self):
        csv_teste = (
            "id,nome,cultura,latitude,longitude\n"
            "P001,Joao Silva,tomate,-23.5,-46.6\n"
        )

        with patch("builtins.open", mock_open(read_data=csv_teste)):
            validos, invalidos = carregar_produtores()

        self.assertEqual(len(validos), 1)
        self.assertEqual(len(invalidos), 0)

    def test_identificar_latitude_invalida(self):
        csv_teste = (
            "id,nome,cultura,latitude,longitude\n"
            "P001,Joao Silva,tomate,999,-46.6\n"
        )

        with patch("builtins.open", mock_open(read_data=csv_teste)):
            validos, invalidos = carregar_produtores()

        self.assertEqual(len(validos), 0)
        self.assertEqual(len(invalidos), 1)

    def test_identificar_id_duplicado(self):
        csv_teste = (
            "id,nome,cultura,latitude,longitude\n"
            "P001,Joao Silva,tomate,-23.5,-46.6\n"
            "P001,Maria Souza,milho,-22.9,-43.1\n"
        )

        with patch("builtins.open", mock_open(read_data=csv_teste)):
            validos, invalidos = carregar_produtores()

        self.assertEqual(len(validos), 1)
        self.assertEqual(len(invalidos), 1)

    def test_identificar_campo_obrigatorio_vazio(self):
        csv_teste = (
            "id,nome,cultura,latitude,longitude\n"
            "P001,,tomate,-23.5,-46.6\n"
        )

        with patch("builtins.open", mock_open(read_data=csv_teste)):
            validos, invalidos = carregar_produtores()

        self.assertEqual(len(validos), 0)
        self.assertEqual(len(invalidos), 1)
        self.assertIn(
            "Campo obrigatório vazio",
            invalidos[0]["erro"]
        )

    def test_arquivo_inexistente(self):
        with patch(
            "builtins.open",
            side_effect=FileNotFoundError
        ):
            with self.assertRaises(FileNotFoundError):
                carregar_produtores()


if __name__ == "__main__":
    unittest.main()
