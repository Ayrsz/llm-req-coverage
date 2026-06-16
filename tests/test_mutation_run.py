"""Testes da camada pura de ``mutation_run`` (parsing + score).

Não invocam o ``mutmut`` nem a API: usam as fixtures reais capturadas em
``tests/fixtures/`` e casos sintéticos no formato exato da saída real.
"""

from pathlib import Path

import pytest

import mutation_run as mr

FIXTURES = Path(__file__).resolve().parent / "fixtures"


def _fixture(name: str) -> str:
    return (FIXTURES / name).read_text(encoding="utf-8")


# --- parse_run_total ------------------------------------------------------

def test_parse_run_total_fixture_real():
    """A linha-resumo real do probe (req_001/direct) tem 26 mutantes."""
    assert mr.parse_run_total(_fixture("mutmut_run_stdout.txt")) == 26


def test_parse_run_total_usa_ultima_ocorrencia():
    # progresso intermediário 0/26 seguido do resumo final 26/26
    stdout = "⠏ 0/26  🎉 0 🙁 0\n⠴ 26/26  🎉 25 🙁 1\n"
    assert mr.parse_run_total(stdout) == 26


def test_parse_run_total_sem_match_levanta():
    with pytest.raises(ValueError):
        mr.parse_run_total("nenhum número de progresso aqui")


# --- parse_results --------------------------------------------------------

def test_parse_results_fixture_real():
    parsed = mr.parse_results(_fixture("mutmut_results_stdout.txt"))
    assert parsed == {"survived": ["solution.x_calculate_final_price__mutmut_4"]}


def test_parse_results_misto():
    stdout = (
        "    solution.x_f__mutmut_1: survived\n"
        "    solution.x_f__mutmut_2: timeout\n"
        "    solution.x_f__mutmut_3: suspicious\n"
        "    solution.x_f__mutmut_4: skipped\n"
    )
    parsed = mr.parse_results(stdout)
    assert parsed == {
        "survived": ["solution.x_f__mutmut_1"],
        "timeout": ["solution.x_f__mutmut_2"],
        "suspicious": ["solution.x_f__mutmut_3"],
        "skipped": ["solution.x_f__mutmut_4"],
    }


def test_parse_results_vazio_todos_mortos():
    assert mr.parse_results("") == {}


def test_parse_results_ignora_ruido():
    stdout = (
        "/path/__main__.py:1107: DeprecationWarning: use of fork() ...\n"
        "\n"
        "    solution.x_f__mutmut_1: survived\n"
        "linha aleatória sem formato\n"
    )
    assert mr.parse_results(stdout) == {"survived": ["solution.x_f__mutmut_1"]}


# --- build_mutation_result ------------------------------------------------

def test_build_mutation_result_misto():
    res = mr.build_mutation_result(26, {"survived": ["solution.x_f__mutmut_4"]})
    assert res.total == 26
    assert res.killed == 25
    assert res.survived == ["solution.x_f__mutmut_4"]
    assert res.timeout == [] and res.suspicious == [] and res.skipped == []


def test_build_mutation_result_todos_mortos():
    res = mr.build_mutation_result(10, {})
    assert res.killed == 10
    assert res.survived == []


def test_build_mutation_result_varios_nao_mortos():
    by_status = {
        "survived": ["a", "b"],
        "timeout": ["c"],
        "suspicious": ["d"],
    }
    res = mr.build_mutation_result(10, by_status)
    assert res.killed == 10 - 4  # 4 não-mortos listados
    assert res.timeout == ["c"]


# --- mutation_score -------------------------------------------------------

def test_mutation_score_basico():
    res = mr.MutationResult(total=26, killed=25)
    assert mr.mutation_score(res) == 0.9615


def test_mutation_score_todos_mortos():
    res = mr.MutationResult(total=10, killed=10)
    assert mr.mutation_score(res) == 1.0


def test_mutation_score_total_zero():
    res = mr.MutationResult(total=0, killed=0)
    assert mr.mutation_score(res) == 0.0
