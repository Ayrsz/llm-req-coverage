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


# --- T07: seleção de testes verdes/reprovados a partir da matriz -----------

_MATRIX_CSV = (
    "requirement,strategy,test,correct,bug_001,classification\n"
    "req_001,direct,test_a,pass,fail,useful\n"
    "req_001,direct,test_b,pass,pass,weak\n"
    "req_001,direct,test_c,fail,fail,invalid\n"          # reprovado na correta
    "req_001,two_step,test_d,pass,fail,useful\n"          # outra estratégia
    "req_002,direct,test_e,pass,fail,useful\n"            # outro requisito
    "req_003,direct,<collection_error>,error,error,not_executable\n"
)


@pytest.fixture
def matrix_file(tmp_path):
    p = tmp_path / "results_matrix.csv"
    p.write_text(_MATRIX_CSV, encoding="utf-8")
    return p


def test_select_passing_tests_filtra_por_config(matrix_file):
    # só os correct == pass de (req_001, direct)
    assert mr.select_passing_tests("req_001", "direct", matrix_file) == ["test_a", "test_b"]


def test_select_passing_tests_outra_config(matrix_file):
    assert mr.select_passing_tests("req_001", "two_step", matrix_file) == ["test_d"]


def test_select_failing_tests_exclui_pass_e_collection_error(matrix_file):
    # reprovados reais (correct != pass), sem a linha <collection_error>
    assert mr.select_failing_tests("req_001", "direct", matrix_file) == ["test_c"]


def test_select_failing_tests_collection_error_nao_e_node_id(matrix_file):
    # <collection_error> não é um node id deselecionável -> não entra
    assert mr.select_failing_tests("req_003", "direct", matrix_file) == []


# --- T08: guard puro should_skip ------------------------------------------

def test_should_skip_lista_vazia():
    assert mr.should_skip([]) is True


def test_should_skip_com_testes():
    assert mr.should_skip(["test_x"]) is False


# --- T09: prepare_workdir (filesystem; não invoca mutmut) ------------------

def test_prepare_workdir_monta_arquivos():
    failing = ["test_calculate_final_price_unknown_customer_type_treated_as_common[uppercase_premium_customer_type]"]
    workdir = mr.prepare_workdir("req_001", "two_step", failing)
    try:
        assert (workdir / "solution.py").exists()
        assert (workdir / "test_generated.py").exists()
        cfg = (workdir / "setup.cfg").read_text(encoding="utf-8")
        assert "source_paths=solution.py" in cfg
        # o reprovado vira node id deselecionado
        assert "--deselect" in cfg
        assert f"test_generated.py::{failing[0]}" in cfg
    finally:
        import shutil
        shutil.rmtree(workdir, ignore_errors=True)


def test_prepare_workdir_sem_reprovados_nao_emite_deselect():
    workdir = mr.prepare_workdir("req_001", "direct", [])
    try:
        cfg = (workdir / "setup.cfg").read_text(encoding="utf-8")
        assert "source_paths=solution.py" in cfg
        assert "--deselect" not in cfg
    finally:
        import shutil
        shutil.rmtree(workdir, ignore_errors=True)


# --- T11/T12: montagem de linhas de CSV (puro) + caminho skipped -----------

def test_summary_row_skipped():
    row = mr.summary_row("req_001", "direct", "skipped")
    assert row["status"] == "skipped"
    assert row["mutants_total"] == 0 and row["mutation_score_auto"] == 0.0


def test_summary_row_ok():
    res = mr.MutationResult(total=26, killed=23, survived=["a", "b", "c"])
    row = mr.summary_row("req_001", "two_step", "ok", res)
    assert row["mutants_total"] == 26
    assert row["mutants_killed"] == 23
    assert row["mutants_survived"] == 3
    assert row["mutation_score_auto"] == 0.8846
    assert row["status"] == "ok"


def test_survivor_rows():
    res = mr.MutationResult(total=5, killed=3, survived=["m1"], timeout=["m2"])
    rows = mr.survivor_rows("req_001", "direct", res, {"m1": "diff-1"})
    assert {r["mutant_id"]: r["status"] for r in rows} == {"m1": "survived", "m2": "timeout"}
    by_id = {r["mutant_id"]: r for r in rows}
    assert by_id["m1"]["diff"] == "diff-1"
    assert by_id["m2"]["diff"] == ""  # sem diff fornecido


def test_evaluate_config_skipped_nao_invoca_mutmut(matrix_file):
    # req_003 só tem <collection_error> -> sem testes verdes -> skipped, sem I/O
    summary, survivors = mr.evaluate_config("req_003", "direct", matrix_path=matrix_file)
    assert summary["status"] == "skipped"
    assert survivors == []
