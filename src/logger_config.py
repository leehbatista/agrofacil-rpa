
import logging
from pathlib import Path


def configurar_logging():
    pasta_projeto = Path(__file__).resolve().parent.parent
    pasta_logs = pasta_projeto / "logs"

    pasta_logs.mkdir(exist_ok=True)

    arquivo_log = pasta_logs / "agrofacil.log"

    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s | %(levelname)s | %(message)s",
        handlers=[
            logging.FileHandler(
                arquivo_log,
                encoding="utf-8"
            )
        ],
        force=True
    )
