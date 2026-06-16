"""Carregamento dos requisitos e do ground truth humano."""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

import pandas as pd

from . import config
from .config import DomainSpec


@dataclass
class DomainData:
    """Dados de um domínio prontos para o experimento.

    - ``requirement``: texto do documento de requisitos (knowledge base).
    - ``example_overview`` / ``example_description``: primeiro caso humano,
      usado como exemplo few-shot (não é avaliado).
    - ``tests``: DataFrame com os casos humanos restantes a serem avaliados,
      colunas ``ID``, ``test-overview``, ``test-description``.
    """

    name: str
    requirement: str
    example_overview: str
    example_description: str
    tests: pd.DataFrame


def _read_text(path: Path) -> str:
    with open(path, encoding="utf-8") as f:
        return f.read()


def load_domain_data(
    spec: DomainSpec,
    dataset_dir: Path | None = None,
    ground_truth_dir: Path | None = None,
) -> DomainData:
    """Carrega requisito + ground truth de um domínio.

    A primeira linha do CSV é separada como exemplo few-shot; o restante é
    retornado para avaliação. Linhas com campos vazios são descartadas.
    """
    dataset_dir = dataset_dir or config.dataset_dir()
    ground_truth_dir = ground_truth_dir or config.ground_truth_dir()

    requirement = _read_text(dataset_dir / spec.requirement_file)

    df = pd.read_csv(ground_truth_dir / spec.ground_truth_file)
    df = df.dropna(subset=["test-overview", "test-description"]).reset_index(drop=True)

    if df.empty:
        raise ValueError(f"Ground truth vazio para o domínio {spec.name}")

    example = df.iloc[0]
    tests = df.iloc[1:].reset_index(drop=True)

    return DomainData(
        name=spec.name,
        requirement=requirement,
        example_overview=str(example["test-overview"]),
        example_description=str(example["test-description"]),
        tests=tests,
    )
