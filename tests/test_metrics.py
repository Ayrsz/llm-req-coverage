"""Testes das funções puras de minimização de suíte (Fase 4) em ``metrics.py``.

A fronteira de teste é o cálculo sobre a matriz já carregada (lista de dicts no
formato de ``results_matrix.csv``): ``killset_of_row`` e ``suite_minimization``.
Sem I/O — monta matrizes sintéticas e confere os números exatos.
"""

import metrics

BUG_COLS = ["bug_001", "bug_002", "bug_003"]


def _row(req, test, correct, **bugs):
    base = {"requirement": req, "strategy": "direct", "test": test,
            "correct": correct, "classification": "x"}
    for c in BUG_COLS:
        base[c] = bugs.get(c, "pass")
    return base


# matriz sintética de req_A: tA3 domina tA1/tA2; tA4 é o único matador de bug_003
REQ_A = [
    _row("req_A", "tA1", "pass", bug_001="fail"),                 # mata {001}
    _row("req_A", "tA2", "pass", bug_002="fail"),                 # mata {002}
    _row("req_A", "tA3", "pass", bug_001="fail", bug_002="fail"), # mata {001,002}
    _row("req_A", "tA4", "pass", bug_003="fail"),                 # mata {003} (único)
    _row("req_A", "tA5", "pass"),                                 # weak: mata nada
    _row("req_A", "tA6", "fail", bug_001="fail"),                 # invalid: não conta
]


def test_killset_of_row_basico():
    assert metrics.killset_of_row(REQ_A[0], BUG_COLS) == frozenset({("req_A", "bug_001")})
    assert metrics.killset_of_row(REQ_A[2], BUG_COLS) == frozenset(
        {("req_A", "bug_001"), ("req_A", "bug_002")}
    )


def test_killset_of_row_weak_e_invalid_sao_vazios():
    # weak (passa na correta, não mata nada) e invalid (falha na correta) -> vazio
    assert metrics.killset_of_row(REQ_A[4], BUG_COLS) == frozenset()
    assert metrics.killset_of_row(REQ_A[5], BUG_COLS) == frozenset()


def test_killset_ignora_celula_vazia():
    # coluna de bug ausente para o requisito (célula "") não é "matada"
    r = _row("req_X", "t", "pass", bug_001="fail")
    r["bug_002"] = ""
    assert metrics.killset_of_row(r, BUG_COLS) == frozenset({("req_X", "bug_001")})


def test_suite_minimization_um_requisito():
    m = metrics.suite_minimization(REQ_A, BUG_COLS)
    assert m["min_suite_size"] == 2          # {tA3, tA4} cobre {001,002,003}
    assert m["essential_tests"] == 1         # só tA4 mata bug_003
    assert m["kills_per_test_mean"] == 1.25  # (1+1+2+1)/4 úteis
    assert m["candidate_tests"] == 5         # tA1..tA5 passam na correta; tA6 não


def test_suite_minimization_agrega_requisitos_disjuntos():
    rows = REQ_A + [_row("req_B", "tB1", "pass", bug_001="fail")]
    m = metrics.suite_minimization(rows, BUG_COLS)
    assert m["min_suite_size"] == 3          # tA3, tA4, tB1
    assert m["essential_tests"] == 2         # tA4 (003) e tB1 (B/001)
    assert m["kills_per_test_mean"] == 1.2   # (1+1+2+1+1)/5 úteis


def test_suite_minimization_sem_mutantes_detectaveis():
    rows = [_row("req_A", "tA5", "pass"), _row("req_A", "tA6", "fail")]
    m = metrics.suite_minimization(rows, BUG_COLS)
    assert m["min_suite_size"] == 0
    assert m["essential_tests"] == 0
    assert m["kills_per_test_mean"] == 0.0
