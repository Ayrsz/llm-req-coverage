"""Testes de integração do pipeline com FakeClient (sem API)."""

from testgen import config
from testgen.pipeline import ExperimentRunner
from testgen.reporting import save_result
from testgen.strategies import DirectStrategy

from .conftest import FakeClient


def _embeddings_for(score_pairs):
    """Helper: monta um dict de embeddings que produz similaridades controladas.

    Para cada par (gt_text, predict_text), usamos vetores idênticos -> sim=1.0
    quando queremos MATCH, e ortogonais -> sim=0.0 para NO_MATCH.
    """
    return score_pairs


class TestExperimentRunner:
    def test_run_produces_record_per_test(self, sample_domain):
        client = FakeClient(default_text="PRED", default_embedding=[1.0, 0.0])
        runner = ExperimentRunner(client)

        result = runner.run(sample_domain, DirectStrategy())

        assert len(result.records) == len(sample_domain.tests)  # 2
        assert result.domain == "BOOKMARK"
        assert result.strategy_code == "A"

    def test_records_have_all_expected_columns(self, sample_domain):
        client = FakeClient()
        result = ExperimentRunner(client).run(sample_domain, DirectStrategy())

        expected = {"TEST ID", "STRATEGY", "TECHNIQUES", "GT", "PREDICT", "SIMILARITY", "STATUS"}
        expected |= set(config.QUALITATIVE_COLUMNS)
        assert expected.issubset(set(result.records.columns))

    def test_identical_embeddings_yield_match(self, sample_domain):
        # Toda GT e PRED mapeiam para o mesmo vetor -> similaridade 1.0 -> MATCH
        embeddings = {
            "GT one": [1.0, 0.0],
            "GT two": [1.0, 0.0],
            "PRED": [1.0, 0.0],
        }
        client = FakeClient(default_text="PRED", embeddings=embeddings)
        result = ExperimentRunner(client).run(sample_domain, DirectStrategy())

        assert (result.records["STATUS"] == "MATCH").all()
        assert result.metrics.precision == 1.0
        assert result.metrics.recall == 1.0

    def test_orthogonal_embeddings_yield_no_match(self, sample_domain):
        embeddings = {
            "GT one": [1.0, 0.0],
            "GT two": [1.0, 0.0],
            "PRED": [0.0, 1.0],  # ortogonal -> sim 0.0
        }
        client = FakeClient(default_text="PRED", embeddings=embeddings)
        result = ExperimentRunner(client).run(sample_domain, DirectStrategy())

        assert (result.records["STATUS"] == "NO_MATCH").all()
        assert result.metrics.matches == 0
        assert result.metrics.f1 == 0.0

    def test_save_result_writes_csv(self, sample_domain, tmp_path):
        client = FakeClient()
        result = ExperimentRunner(client).run(sample_domain, DirectStrategy())

        path = save_result(result, output_root=tmp_path)

        assert path.exists()
        assert path.name == "BOOKMARK_tests.csv"
        assert path.parent.name == "direct_prompt"
        content = path.read_text(encoding="utf-8-sig")
        assert "STATUS" in content
