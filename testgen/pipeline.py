"""Orquestração: roda uma estratégia sobre um domínio e avalia o resultado."""

from __future__ import annotations

from dataclasses import dataclass

import pandas as pd

from . import config, evaluation
from .data_loader import DomainData
from .evaluation import Metrics
from .llm_client import LLMClient
from .strategies import GenerationStrategy


@dataclass
class ExperimentResult:
    domain: str
    strategy_code: str
    records: pd.DataFrame
    metrics: Metrics


class ExperimentRunner:
    """Executa uma estratégia de geração e avalia contra o ground truth.

    O ``LLMClient`` é injetado, então o runner é totalmente testável com um
    cliente fake (sem chamadas de API).
    """

    def __init__(self, client: LLMClient):
        self.client = client

    def run(self, domain: DomainData, strategy: GenerationStrategy) -> ExperimentResult:
        system_instruction = strategy.build_system_instruction(domain)
        records: list[dict] = []

        for _, row in domain.tests.iterrows():
            overview = row["test-overview"]
            ground_truth = row["test-description"]

            predicted, techniques = strategy.produce(self.client, system_instruction, overview)

            score = evaluation.cosine_similarity(
                self.client.embed(ground_truth),
                self.client.embed(predicted),
            )
            status = evaluation.classify(score)

            record = {
                "TEST ID": row["ID"],
                "STRATEGY": strategy.code,
                "TECHNIQUES": techniques,
                "GT": ground_truth,
                "PREDICT": predicted,
                "SIMILARITY": round(score, 4),
                "STATUS": status,
            }
            for col in config.QUALITATIVE_COLUMNS:
                record[col] = ""
            records.append(record)

        df = pd.DataFrame(records)
        metrics = evaluation.compute_metrics(
            df["STATUS"].tolist() if not df.empty else [],
            total_human=len(domain.tests),
        )
        return ExperimentResult(
            domain=domain.name,
            strategy_code=strategy.code,
            records=df,
            metrics=metrics,
        )
