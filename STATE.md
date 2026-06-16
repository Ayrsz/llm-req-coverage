# STATE — memória entre sessões

Feature em execução: **Avaliação por mutação automática** (Fase 2).
Specs: [docs/specs/mutacao-automatica.md](docs/specs/mutacao-automatica.md) ·
[plano](docs/specs/mutacao-automatica-plan.md) ·
[tarefas](docs/specs/mutacao-automatica-tasks.md).

## Progresso

- [x] T01 — `mutmut==3.6.0` em `requirements.txt`/`environment.yml`; instalado e validado.
- [x] T02 — fixtures reais em `tests/fixtures/` (run, results, show).
- [x] T03–T06 — camada pura de `evaluation/mutation_run.py` + `tests/test_mutation_run.py` (13 testes verdes); `tests/conftest.py` torna `evaluation/` importável.
- **Checkpoint (parada pedida):** `python -m pytest` na raiz VERDE (13 passed), antes da camada de I/O.
- [ ] T07–T14 — pendentes (próximo: T07/T08 filtro de baseline verde; depois I/O T09/T10).

### Decisão de escopo nova (T06)
- Adicionado **`pytest.ini`** na raiz com `testpaths = tests`. Sem ele, `python -m pytest` coletava `generated_tests/*` (que fazem `from solution import ...`) → 6 erros de coleta, quebrando o CA5. Não interfere nos runs isolados (`run_tests.py`/`mutmut` rodam com cwd em `/tmp`, fora desta árvore — verificado).

## Decisões e achados (não óbvios — ler antes de continuar)

### Ambiente
- `python` = miniconda **3.13.13** (`environment.yml` declara 3.11 — divergência conhecida, não bloqueia).
- **Sempre** usar `python -m pip` e `python -m mutmut`. O binário `mutmut` no PATH e o `pip` em `~/.local/bin` apontam para `/usr/bin/python3`, **não** para o interpretador de `python`.

### Comportamento real do `mutmut` 3.6.0 (verificado por probe em req_001/direct)
- Carrega config **avidamente**: qualquer subcomando (até `version`) exige `setup.cfg` com `[mutmut]\nsource_paths=solution.py` no cwd. Por isso só roda dentro do workdir isolado.
- **Baseline verde obrigatório:** roda a suíte sem mutação antes; se algum teste falha, aborta (`failed to collect stats`). Daí o filtro de testes `correct == pass` (T07).
- `mutmut run` — linha-resumo final (a ÚLTIMA com `N/N`): `… 26/26  🎉 25 🫥 0  ⏰ 0  🤔 0  🙁 1  🔇 0  🧙 0`. Convenção de emojis: 🎉=killed, 🙁=survived, ⏰=timeout, 🤔=suspicious. `parse_run_total` deve pegar o **2º grupo do último** `(\d+)/(\d+)`.
- `mutmut results` — lista **só os não-mortos**, formato `    solution.x_<fn>__mutmut_<N>: <status>` (note o prefixo `x_` no nome mascarado). Tudo que aparece aqui é não-morto ⇒ `killed = total − nº de linhas`.
- `mutmut show <id>` — devolve diff unificado do mutante (para `mutation_survivors.csv`, CA3).
- Ruído na saída de `run`: spinners Unicode e um `DeprecationWarning: ... use of fork()`. Parser deve ignorar.
- **Probe req_001/direct:** 26 mutantes, 25 mortos, 1 sobrevivente — `if v < 0` → `if v <= 0`, que é **mutante equivalente** (em `v==0` ambos retornam 0.0). Bom caso para a nota "sobrevivente ≠ necessariamente lacuna; pode ser equivalente" (CA3).

### Baseline verde — dado de entrada
- `evaluation/results_matrix.csv` já classifica por `correct`. Config crítica: `req_001/two_step` tem 1 teste `invalid` (`test_calculate_final_price_unknown_customer_type_treated_as_common[uppercase_premium_customer_type]`, `correct=fail`) — precisa ser deselecionado para o baseline ficar verde (validação do T13).

### Filtro de baseline verde — mecanismo validado (probe req_001-like)
- Deselect é por **node id parametrizado** (`funcao[param]`), não por função:
  `req_001/two_step` tem params bons e o ruim na mesma função.
- Lista de reprovados = linhas de `results_matrix.csv` com `correct != pass`,
  coluna `test` usada literal. Node id = `test_generated.py::<coluna test>`.
- Mecanismo: no `setup.cfg` do workdir, `pytest_add_cli_args` (1 arg por linha)
  com pares `--deselect` + node id. SEM deselect o mutmut aborta
  (`failed to collect stats`); COM, roda até o fim. Validado.
- `run_mutmut` invoca `sys.executable -m mutmut` (mutmut roda pytest in-process;
  o binário do PATH aponta pro interpretador errado). Default é `pytest -x`.