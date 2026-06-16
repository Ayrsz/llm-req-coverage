"""Testes da lógica de avaliação (similaridade, classificação, métricas)."""

import math

import pytest

from testgen import evaluation


class TestCosineSimilarity:
    def test_identical_vectors(self):
        assert evaluation.cosine_similarity([1, 2, 3], [1, 2, 3]) == pytest.approx(1.0)

    def test_orthogonal_vectors(self):
        assert evaluation.cosine_similarity([1, 0], [0, 1]) == pytest.approx(0.0)

    def test_opposite_vectors(self):
        assert evaluation.cosine_similarity([1, 0], [-1, 0]) == pytest.approx(-1.0)

    def test_zero_vector_returns_zero(self):
        assert evaluation.cosine_similarity([0, 0], [1, 1]) == 0.0


class TestClassify:
    @pytest.mark.parametrize(
        "score,expected",
        [
            (0.95, "MATCH"),
            (0.80, "MATCH"),      # borda inferior do match
            (0.79, "REVIEW"),
            (0.65, "REVIEW"),     # borda inferior do review
            (0.64, "NO_MATCH"),
            (0.0, "NO_MATCH"),
        ],
    )
    def test_thresholds(self, score, expected):
        assert evaluation.classify(score) == expected


class TestComputeMetrics:
    def test_all_match(self):
        m = evaluation.compute_metrics(["MATCH", "MATCH"], total_human=2)
        assert m.precision == 1.0
        assert m.recall == 1.0
        assert m.f1 == 1.0

    def test_partial_coverage(self):
        # 1 match em 2 gerados; benchmark humano tem 4 casos
        m = evaluation.compute_metrics(["MATCH", "NO_MATCH"], total_human=4)
        assert m.precision == 0.5            # 1/2
        assert m.recall == pytest.approx(0.25)  # 1/4
        assert m.f1 == pytest.approx(2 * 0.5 * 0.25 / (0.5 + 0.25))

    def test_no_matches_gives_zero_f1(self):
        m = evaluation.compute_metrics(["NO_MATCH", "REVIEW"], total_human=2)
        assert m.precision == 0.0
        assert m.recall == 0.0
        assert m.f1 == 0.0

    def test_counts(self):
        m = evaluation.compute_metrics(["MATCH", "REVIEW", "REVIEW", "NO_MATCH"], total_human=10)
        assert (m.matches, m.reviews, m.no_matches) == (1, 2, 1)
        assert m.total_generated == 4
        assert m.total_human == 10

    def test_empty_is_safe(self):
        m = evaluation.compute_metrics([], total_human=0)
        assert m.precision == m.recall == m.f1 == 0.0
        assert not math.isnan(m.f1)
