# Tarefas — Avaliação por mutação automática

> Quebra de [mutacao-automatica-plan.md](mutacao-automatica-plan.md) em tarefas atômicas. Etapa SDD: **tasks**. Marque `[x]` ao concluir. Uma tarefa por vez; commits granulares.
>
> Convenção de IDs: **T01..T14**. "Pré-req" lista as tarefas das quais a tarefa depende. Tarefas sem dependência entre si podem ser feitas em paralelo (ver "Paralelização" ao final).

## Bloco A — Dependência e fixtures

### [x] T01 — Fixar `mutmut==3.6.0` nas dependências
- **O que fazer:** adicionar `mutmut==3.6.0` à lista de dependências (pip).
- **Onde fazer:** `requirements.txt` e o bloco `pip:` de `environment.yml`.
- **Pré-req:** nenhuma.
- **Como validar:** `pip install -r requirements.txt` (ou `pip install mutmut==3.6.0`) conclui sem erro e `mutmut version` imprime `3.6.0`.

### [x] T02 — Capturar fixtures reais da saída do `mutmut`
- **O que fazer:** rodar o probe do `mutmut` sobre `req_001` (correct.py + suíte verde) num dir isolado manual e **salvar** as saídas brutas de `mutmut run` (linha-resumo `N/N 🎉 …`) e de `mutmut results` (linhas `solution.<...>__mutmut_<N>: <status>`), incluindo o ruído de `UserWarning` se aparecer. Guardar como arquivos de fixture (ex.: `tests/fixtures/mutmut_run_stdout.txt`, `tests/fixtures/mutmut_results_stdout.txt`).
- **Onde fazer:** `tests/fixtures/` (novo).
- **Pré-req:** T01.
- **Como validar:** os arquivos existem e contêm a linha-resumo com `(\d+)/(\d+)` e ≥1 linha de mutante não-morto no formato esperado. (Estes arquivos alimentam T04.)

## Bloco B — Camada pura (TDD: testes primeiro)

### [x] T03 — Definir `MutationResult` e assinaturas da camada pura
- **O que fazer:** criar `evaluation/mutation_run.py` com a dataclass `MutationResult` (`total: int`, `killed: int`, `survived/timeout/suspicious/skipped: list[str]`) e os stubs de `parse_run_total`, `parse_results`, `build_mutation_result`, `mutation_score`. **Sem** `import llm_client` nem qualquer import que toque a API (CA4).
- **Onde fazer:** `evaluation/mutation_run.py` (novo).
- **Pré-req:** nenhuma (pode começar em paralelo a T01/T02).
- **Como validar:** `python -c "import evaluation.mutation_run"` (ou import por caminho) não dispara rede/efeitos colaterais; `MutationResult` instancia.

### [x] T04 — Escrever os testes da camada pura (falhando)
- **O que fazer:** criar `tests/test_mutation_run.py` cobrindo, com as fixtures de T02 + casos sintéticos: `parse_run_total` (linha real; sem match → erro/sentinela); `parse_results` (misto survived/timeout/suspicious; vazio = todos mortos; ruído ignorado); `build_mutation_result` + `mutation_score` (morto/sobrevivente/misto; `total == 0` → 0.0). **Sem** invocar `mutmut` nem a API. As fixtures sintéticas de `timeout`/`suspicious` devem usar exatamente o formato de linha real do `results` (`solution.<nome>__mutmut_<N>: timeout`), senão `parse_results` passa no teste e falha na execução real.
- **Onde fazer:** `tests/test_mutation_run.py` (novo).
- **Pré-req:** T02 (fixtures), T03 (assinaturas).
- **Como validar:** `python -m pytest tests/test_mutation_run.py` roda e os testes **falham** pelos stubs vazios (vermelho do TDD), não por erro de import/coleta.

### [x] T05 — Garantir importabilidade de `mutation_run` nos testes
- **O que fazer:** adicionar mecanismo mínimo de import (ex.: `tests/conftest.py` inserindo a raiz/`evaluation/` no `sys.path`) sem empacotar e sem quebrar a execução standalone (`python evaluation/mutation_run.py`). Limpar/ignorar o `__pycache__` órfão em `tests/`.
- **Onde fazer:** `tests/conftest.py` (novo) e `tests/`.
- **Pré-req:** T03.
- **Como validar:** `python -m pytest tests/` coleta `test_mutation_run.py` sem `ModuleNotFoundError`; `python evaluation/mutation_run.py --help` ainda funciona.

### [x] T06 — Implementar a camada pura (verde)
- **O que fazer:** implementar `parse_run_total` (regex `(\d+)/(\d+)`, 2º grupo), `parse_results` (parseia linhas `solution.…__mutmut_N: status`, ignora ruído/branco), `build_mutation_result` (convenção **`killed = total − nº de linhas listadas por `results``**), `mutation_score` (`killed/total`, 0.0 se `total==0`, `round(x,4)`).
- **Onde fazer:** `evaluation/mutation_run.py`.
- **Pré-req:** T04, T05.
- **Como validar:** `python -m pytest tests/test_mutation_run.py` passa (verde).

## Bloco C — Filtro de baseline verde

### [x] T07 — Função de seleção de testes verdes
- **O que fazer:** implementar função que, dada `(req_id, strategy)`, lê `evaluation/results_matrix.csv` e devolve os nomes de teste com `correct == pass` para aquela config.
- **Onde fazer:** `evaluation/mutation_run.py`.
- **Pré-req:** T03.
- **Como validar:** teste em `tests/test_mutation_run.py` com um CSV sintético (linhas pass/fail/error) retorna apenas os `pass`; passa em `python -m pytest`.

### [x] T08 — Guard puro de skip (config sem testes verdes)
- **O que fazer:** implementar uma função pura `should_skip(passing_tests) -> bool` (ou `select_or_skip(...)`) que decide, a partir da lista de testes verdes de T07, se a config deve ser marcada `skipped` (lista vazia ⇒ `True`). O `evaluate_config` (T11) apenas consome esse guard; nenhuma lógica de skip vive dentro do `evaluate_config`.
- **Onde fazer:** `evaluation/mutation_run.py`.
- **Pré-req:** T07.
- **Como validar:** teste unitário em `tests/test_mutation_run.py`: `should_skip([]) is True` e `should_skip(["test_x"]) is False`; passa em
  `python -m pytest` **sem** invocar `mutmut`. 

## Bloco D — Camada de invocação (I/O; não unit-testada)

### [x] T09 — `prepare_workdir`
- **O que fazer:** criar dir temporário; copiar `implementations/req_XXX/correct.py` → `solution.py`; escrever `setup.cfg` com `[mutmut]\nsource_paths=solution.py`; escrever `test_generated.py` contendo **apenas os testes verdes** (T07). Reusar o padrão de isolamento de `run_tests.py::run_against_variant`.
- **Onde fazer:** `evaluation/mutation_run.py`.
- **Pré-req:** T07.
- **Como validar:** chamada manual gera um dir com `solution.py`, `setup.cfg` (com `source_paths`) e `test_generated.py` só com os verdes; `pytest test_generated.py` nesse dir passa (baseline verde).

### [x] T10 — `run_mutmut` e `show_survivor_diff`
- **O que fazer:** `run_mutmut(workdir, timeout)` executa `mutmut run` e depois `mutmut results` **com cwd no workdir**, devolvendo as duas saídas brutas (tratar `timeout` como em `run_tests.py`). **`mutmut results` deve ser chamado sem a flag `--all`** — com `--all` os mortos passam a ser listados e a convenção de score do T06 fica incorreta. `show_survivor_diff(workdir, mutant_id)` roda `mutmut show <id>` e devolve o diff bruto.
- **Onde fazer:** `evaluation/mutation_run.py`.
- **Pré-req:** T09.
- **Como validar:** execução manual sobre o workdir de `req_001` retorna uma linha-resumo parseável por `parse_run_total` e uma lista parseável por `parse_results`; `show` de um sobrevivente retorna diff não-vazio.

## Bloco E — Orquestração e saída

### [ ] T11 — `evaluate_config` + `main()` + flags
- **O que fazer:** `evaluate_config(req_id, strategy, passing_tests, timeout)` encadeia invocação→parsing→score e devolve a linha de resultado (incl. `status` ok/skipped). `main()` itera as `(req × estratégia)` com teste gerado, lê os verdes (T07), agrega; flags `--timeout` e (recomendado) `--limit`/`--strategy`, no padrão dos scripts existentes.
- **Onde fazer:** `evaluation/mutation_run.py`.
- **Pré-req:** T06, T08, T10.
- **Como validar:** `python evaluation/mutation_run.py --limit 1` roda uma config ponta-a-ponta sem erro.

### [ ] T12 — Escrita dos CSVs de saída
- **O que fazer:** gravar `evaluation/mutation_summary.csv` (`requirement, strategy, mutants_total, mutants_killed, mutants_survived, mutants_timeout, mutants_suspicious, mutation_score_auto, status`) e `evaluation/mutation_survivors.csv` (`requirement, strategy, mutant_id, status, diff`). UTF-8, no padrão de `metrics.py`.
- **Onde fazer:** `evaluation/mutation_run.py`.
- **Pré-req:** T11.
- **Como validar:** após rodar, os dois CSVs existem com os cabeçalhos especificados; teste unitário cobre a montagem de uma linha de cada CSV (CA4) e passa em `python -m pytest`.

## Bloco F — Execução real, validação e docs

### [ ] T13 — Rodar nas 6 configs e validar CA2/CA3
- **O que fazer:** `python evaluation/mutation_run.py` nas 3 req × 2 estratégias; inspecionar os CSVs. Registrar achados (scores, sobreviventes; nota sobre mutante equivalente exigir triagem humana).
- **Onde fazer:** execução + `reports/` (ou nota no PR/STATE.md).
- **Pré-req:** T12.
- **Como validar:** **CA2** — `mutation_score_auto` tem ≥2 valores distintos (não 1.0 em tudo); **CA3** — `mutation_survivors.csv` lista sobreviventes por config com `diff`. **CA1** — sobre os `generated_tests/` já existentes (sem re-rodar `generate_tests.py`), `python evaluation/run_tests.py` → `python evaluation/metrics.py` reproduz `results_matrix.csv`/`metrics_summary.csv`, e `git status` confirma que os `bug_00N.py` e os scripts antigos estão intactos. **CA5** — `python -m pytest` verde.
- **Como validar:** **Baseline verde funcionando** — a config `req_001/two_step` aparece no `mutation_summary.csv` com `status="ok"` (não `skipped`) e `mutants_total > 0`. Isso comprova que o teste `invalid` foi filtrado e o `mutmut` não abortou (`failed to collect stats`).

### [ ] T14 — Atualizar documentação
- **O que fazer:** acrescentar `mutation_run.py` à estrutura/comandos e descrever `mutation_score_auto` (mutmut, muitos mutantes) **vs** `mutation_score` manual (5 por req) lado a lado, deixando explícito que **não são numericamente comparáveis** (conjuntos de mutantes diferentes) e sim complementares; mencionar o filtro de baseline verde e o status `skipped`.
- **Onde fazer:** `CLAUDE.md` e `README.md`.
- **Pré-req:** T13.
- **Como validar:** ambos os arquivos citam `mutation_run.py`, os dois CSVs e a distinção auto vs manual; revisão de leitura.

## Definition of Done (espelha o plano)

- [ ] DoD1 — `mutation_run.py` roda standalone e produz `mutation_summary.csv` por config. *(T11, T12)*
- [ ] DoD2 — CA1: `bug_00N.py` intactos; pipeline antigo reproduz seus CSVs. *(T13)*
- [ ] DoD3 — CA2: `mutation_score_auto` com ≥2 valores distintos. *(T13)*
- [ ] DoD4 — CA3: sobreviventes listados por config. *(T12, T13)*
- [ ] DoD5 — CA4: `tests/test_mutation_run.py` cobre parsing+score+linhas de CSV, offline. *(T04, T06, T07, T12)*
- [ ] DoD6 — CA5: `python -m pytest` verde. *(T13)*
- [ ] DoD7 — `mutmut==3.6.0` nas deps; instalação limpa roda. *(T01)*
- [ ] DoD8 — docs atualizadas. *(T14)*
- [ ] DoD9 — baseline verde garantido (filtro via `results_matrix.csv`; config sem verdes = `skipped`). *(T07, T08)*

## Paralelização

- **Paralelas:** T01, T02 (deps/fixtures) e T03 (stubs) podem andar juntas; T05 (importabilidade) em paralelo a T02.
- **Caminho crítico:** T03 → T04 → T06 → (T07/T08) → T09 → T10 → T11 → T12 → T13 → T14.
- **Bloqueadores fortes:** T02 alimenta T04 (fixtures reais); T07 é pré-requisito do baseline verde que destrava T09/T11.
