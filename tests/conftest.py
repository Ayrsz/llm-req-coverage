"""Configuração de testes: torna os módulos de ``evaluation/`` importáveis.

Os scripts em ``evaluation/`` rodam standalone (``python evaluation/x.py``) e não
formam um pacote instalável. Para os testes importarem ``mutation_run`` como
``import mutation_run``, inserimos ``evaluation/`` no ``sys.path`` — sem empacotar
e sem afetar a execução standalone dos scripts.
"""

import sys
from pathlib import Path

EVALUATION_DIR = Path(__file__).resolve().parents[1] / "evaluation"
if str(EVALUATION_DIR) not in sys.path:
    sys.path.insert(0, str(EVALUATION_DIR))
