"""Consistência estrutural do conjunto de requisitos (offline, sem API).

Para cada ``implementations/req_*`` verifica o contrato compartilhado pelo harness:

- o ``requirements/<req>.md`` declara a função via ``from solution import <nome>``;
- há ``correct.py`` e ≥1 ``bug_*.py``;
- todos importam sem erro e expõem ``<nome>`` como ``callable``.

É a rede de segurança que faz a adição de um requisito fora do contrato falhar
cedo (sem ``correct.py``, sem mutante, assinatura divergente).
"""

import importlib.util
import re
from pathlib import Path

import pytest

REPO_ROOT = Path(__file__).resolve().parents[1]
REQUIREMENTS_DIR = REPO_ROOT / "requirements"
IMPL_DIR = REPO_ROOT / "implementations"

_IMPORT_RE = re.compile(r"from\s+solution\s+import\s+(\w+)")

# Diretórios de implementação descobertos em tempo de coleta.
REQ_DIRS = sorted(d for d in IMPL_DIR.glob("req_*") if d.is_dir())


def _declared_function(req_id: str) -> str:
    """Nome da função declarado no ``requirements/<req>.md`` (âncora de import)."""
    md = REQUIREMENTS_DIR / f"{req_id}.md"
    assert md.exists(), f"Requisito sem .md: {md}"
    m = _IMPORT_RE.search(md.read_text(encoding="utf-8"))
    assert m, f"{md} não tem a linha 'from solution import <nome>'"
    return m.group(1)


def _load(path: Path, mod_name: str):
    """Carrega um arquivo .py por caminho, com nome de módulo único."""
    spec = importlib.util.spec_from_file_location(mod_name, path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


@pytest.mark.parametrize("req_dir", REQ_DIRS, ids=[d.name for d in REQ_DIRS])
def test_requirement_contract(req_dir):
    req_id = req_dir.name
    func_name = _declared_function(req_id)

    correct = req_dir / "correct.py"
    bugs = sorted(req_dir.glob("bug_*.py"))
    assert correct.exists(), f"{req_id}: falta correct.py"
    assert bugs, f"{req_id}: nenhum bug_*.py"

    # correct e cada mutante importam e expõem a função declarada.
    for i, py in enumerate([correct, *bugs]):
        module = _load(py, f"{req_id}_{py.stem}_{i}")
        fn = getattr(module, func_name, None)
        assert callable(fn), f"{req_id}/{py.name}: não expõe '{func_name}' chamável"


def test_descobriu_requisitos():
    """Sanidade: a coleta encontrou ao menos os 3 requisitos do piloto."""
    assert len(REQ_DIRS) >= 3
