# STATE — memória entre sessões

Feature em execução: **Escalar o número de requisitos** (Fase 3, 3 → 15).
Specs: [docs/specs/escalar-requisitos.md](docs/specs/escalar-requisitos.md) ·
[plano](docs/specs/escalar-requisitos-plan.md) ·
[tarefas](docs/specs/escalar-requisitos-tasks.md).

## Fase 3 — gabarito e taxonomia (T02, seguir em T03–T08)

**Gabarito de `requirements/req_XXX.md`** (igual a `req_001..003`): título; Descrição;
Interface (módulo `solution` + **Assinatura**) **com a linha `from solution import <nome>`**
num bloco de código (âncora do teste de consistência); Domínio de entrada; Regras
(numeradas); Classes de equivalência; Valores-limite; Entradas inválidas; Invariantes;
Critérios de aceitação (AC1..). Função **determinística** — proibido `now()`, `random`, I/O.

**Taxonomia dos 5 mutantes** (1 defeito cada, sem erro de sintaxe/import):
- `bug_001` — fronteira / off-by-one (`<` vs `<=`, limite incluso/excluso)
- `bug_002` — operador errado (aritmético ou de comparação trocado)
- `bug_003` — ramo/retorno trocado (classe certa, valor de outra)
- `bug_004` — constante/literal errado (taxa, limite, mensagem)
- `bug_005` — guarda ausente / condição invertida (caso inválido não tratado)

**Lista (plano):** req_004 `bmi_category` · req_005 `triangle_type` · req_006 `is_valid_ipv4`
· req_007 `slugify` · req_008 `is_leap_year` · req_009 `days_between` · req_010 `average_above`
· req_011 `most_frequent` · req_012 `income_tax` · req_013 `shipping_cost` · req_014 `final_balance`
· req_015 `apply_commands`.

**Rede de segurança:** `tests/test_requirements_consistency.py` (T01) valida o contrato de
todo `implementations/req_*` — rodar após cada par autorado.

---

## Histórico — Fase 2 (Avaliação por mutação automática, CONCLUÍDA)
Specs: [docs/specs/mutacao-automatica.md](docs/specs/mutacao-automatica.md) ·
[plano](docs/specs/mutacao-automatica-plan.md) ·
[tarefas](docs/specs/mutacao-automatica-tasks.md).

## Progresso

- [x] T01 — `mutmut==3.6.0` em `requirements.txt`/`environment.yml`; instalado e validado.
- [x] T02 — fixtures reais em `tests/fixtures/` (run, results, show).
- [x] T03–T06 — camada pura de `evaluation/mutation_run.py` + `tests/test_mutation_run.py` (13 testes verdes); `tests/conftest.py` torna `evaluation/` importável.
- **Checkpoint (parada pedida):** `python -m pytest` na raiz VERDE (13 passed), antes da camada de I/O.
- [x] T07–T08 — filtro de baseline verde (`select_passing/failing_tests`, `should_skip`).
- [x] T09–T10 — camada de I/O (`prepare_workdir` com deselect, `run_mutmut`, `show_survivor_diff`).
- [x] T11–T12 — orquestração (`evaluate_config`/`main`) + escrita de `mutation_summary.csv`/`mutation_survivors.csv`.
- [x] T13 — rodadas as 6 configs; CA1/CA2/CA3/CA5 validados (ver achados abaixo).
- [ ] T14 — pendente (atualizar README.md/CLAUDE.md).

### T13 — resultados e achados (mutação automática, 6 configs)
- `mutation_score_auto`: req_001 direct=0.9615, two_step=0.8846; req_002 e req_003 = 1.0 nas duas estratégias.
- **CA2 satisfeito** (3 valores distintos, não-saturado em tudo) — mas o teto só quebrou no req_001; req_002/req_003 **ainda saturam em 1.0** mesmo com mutação automática. Achado honesto: em funções-brinquedo deste tamanho, a discriminação plena provavelmente exige os requisitos maiores da Fase 3.
- **Sobreviventes (CA3):** 1 em req_001/direct, 3 em req_001/two_step. Inclui **mutante equivalente** real (`if v < 0` → `if v <= 0`) e mutações no `_round2` (`rounding=None`/sem `rounding`) — sinalizam que "sobrevivente" exige triagem humana (pode ser equivalente, não lacuna).
- **CA1:** `bug_00N.py` e scripts antigos intocados; re-rodar `run_tests.py`+`metrics.py` reproduz os CSVs **semanticamente idênticos** — única diferença é EOL (o `csv` default escreve CRLF; os versionados são LF). Não é regressão desta feature; os CSVs antigos foram restaurados (não sobrescritos).
- **Decisão:** `_write_csv` usa `lineterminator="\n"` para os novos CSVs saírem em LF, consistente com os artefatos versionados.

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