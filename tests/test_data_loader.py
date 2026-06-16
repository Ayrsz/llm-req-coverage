"""Testes do carregamento de dados contra os arquivos reais do repositório."""

import pytest

from testgen import config
from testgen.data_loader import load_domain_data


@pytest.mark.parametrize("domain_key", list(config.DOMAINS))
def test_loads_real_domain(domain_key):
    spec = config.DOMAINS[domain_key]
    data = load_domain_data(spec)

    assert data.name == domain_key
    assert data.requirement.strip()                 # requisito não vazio
    assert data.example_overview.strip()            # exemplo few-shot extraído
    assert data.example_description.strip()
    assert len(data.tests) > 0                       # há casos a avaliar
    assert {"ID", "test-overview", "test-description"}.issubset(data.tests.columns)


def test_example_is_excluded_from_tests():
    spec = config.DOMAINS["BOOKMARK"]
    data = load_domain_data(spec)

    # O overview de exemplo não deve reaparecer entre os casos avaliados
    assert data.example_overview not in data.tests["test-overview"].values
