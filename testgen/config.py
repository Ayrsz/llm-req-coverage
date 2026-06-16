"""Constantes e caminhos centrais do experimento.

Tudo que é "ajustável" (modelos, thresholds, domínios, pastas) vive aqui para
não ficar espalhado pelo código.
"""

from __future__ import annotations

import os
from dataclasses import dataclass
from pathlib import Path

# --- Localização do projeto -------------------------------------------------

PACKAGE_DIR = Path(__file__).resolve().parent
REPO_ROOT = PACKAGE_DIR.parent


def base_dir() -> Path:
    """Raiz onde estão os dados.

    No Colab os arquivos são enviados para /content; localmente usamos a raiz
    do repositório (um nível acima do pacote).
    """
    if Path("/content/dataset").is_dir():
        return Path("/content")
    return REPO_ROOT


def dataset_dir() -> Path:
    return base_dir() / "dataset"


def ground_truth_dir() -> Path:
    return base_dir() / "human_tests"


def output_dir() -> Path:
    return base_dir() / "output"


# --- Modelos ----------------------------------------------------------------

GENERATION_MODEL = "gemini-2.5-flash-lite"  # disponível no free tier; gemini-2.5-flash dá 503/quota
EMBEDDING_MODEL = "gemini-embedding-001"  # modelo de embedding disponível nesta API key

GENERATION_TEMPERATURE = 0.6
TECHNIQUE_TEMPERATURE = 0.2  # menor temperatura -> seleção de técnica mais estável

# --- Thresholds de avaliação ------------------------------------------------

MATCH_THRESHOLD = 0.80   # >= : match automático
REVIEW_THRESHOLD = 0.65  # >= e < MATCH : revisão manual ; abaixo : não match

# Colunas qualitativas deixadas em branco para preenchimento humano.
QUALITATIVE_COLUMNS = [
    "CLARITY",
    "EXECUTABILITY",
    "TRACEABILITY",
    "CORRECTNESS",
    "REDUNDANCY",
    "HALLUCINATION",
    "TDD_UTILITY",
]


# --- Domínios ---------------------------------------------------------------


@dataclass(frozen=True)
class DomainSpec:
    """Descreve um domínio do experimento (bookmark, history, password)."""

    name: str
    requirement_file: str
    ground_truth_file: str


DOMAINS: dict[str, DomainSpec] = {
    "BOOKMARK": DomainSpec("BOOKMARK", "req_bookmark.txt", "req_tests_bookmark.csv"),
    "HISTORY": DomainSpec("HISTORY", "req_history.txt", "req_tests_history.csv"),
    "PASSWORD": DomainSpec("PASSWORD", "req_password.txt", "req_tests_password.csv"),
}


# --- API key ----------------------------------------------------------------


def get_api_key() -> str:
    """Lê GEMINI_API_KEY do .env (ou de variável de ambiente já definida)."""
    try:
        from dotenv import load_dotenv

        load_dotenv(REPO_ROOT / ".env")
    except ImportError:
        pass

    key = os.environ.get("GEMINI_API_KEY")
    if not key:
        raise RuntimeError(
            "GEMINI_API_KEY não encontrado. Adicione a um arquivo .env na raiz do "
            "repositório ou defina com `export GEMINI_API_KEY=...`."
        )
    return key
