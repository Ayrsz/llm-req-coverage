"""Similaridade semântica, classificação por threshold e métricas."""

from __future__ import annotations

from dataclasses import dataclass

import numpy as np

from . import config


def cosine_similarity(vector_a, vector_b) -> float:
    """Similaridade do cosseno entre dois vetores."""
    a = np.asarray(vector_a, dtype=float)
    b = np.asarray(vector_b, dtype=float)
    norm_a = np.linalg.norm(a)
    norm_b = np.linalg.norm(b)
    if norm_a == 0 or norm_b == 0:
        return 0.0
    return float(np.dot(a, b) / (norm_a * norm_b))


def classify(
    score: float,
    match_threshold: float = config.MATCH_THRESHOLD,
    review_threshold: float = config.REVIEW_THRESHOLD,
) -> str:
    """Classifica um score de similaridade em MATCH / REVIEW / NO_MATCH."""
    if score >= match_threshold:
        return "MATCH"
    if score >= review_threshold:
        return "REVIEW"
    return "NO_MATCH"


@dataclass
class Metrics:
    total_human: int
    total_generated: int
    matches: int
    reviews: int
    no_matches: int
    precision: float
    recall: float
    f1: float


def compute_metrics(statuses: list[str], total_human: int) -> Metrics:
    """Calcula precision/recall/F1 a partir das classificações.

    - precision = matches / total gerado
    - recall    = matches / total humano (cobertura do benchmark)
    """
    total_generated = len(statuses)
    matches = sum(s == "MATCH" for s in statuses)
    reviews = sum(s == "REVIEW" for s in statuses)
    no_matches = sum(s == "NO_MATCH" for s in statuses)

    precision = matches / total_generated if total_generated else 0.0
    recall = matches / total_human if total_human else 0.0
    f1 = 2 * precision * recall / (precision + recall) if (precision + recall) else 0.0

    return Metrics(
        total_human=total_human,
        total_generated=total_generated,
        matches=matches,
        reviews=reviews,
        no_matches=no_matches,
        precision=precision,
        recall=recall,
        f1=f1,
    )
