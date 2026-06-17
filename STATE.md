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

### Progresso Fase 3
- [x] T01–T02 — teste de consistência + gabarito/taxonomia.
- [x] T03–T08 — 12 novos requisitos (req_004..req_015) autorados em paralelo por subagentes; cada um `correct.py` + 5 mutantes (taxonomia fixa).
- [x] T09 — **CA1/CA2/CA4/CA5 OK**: 15 reqs/15 dirs, `pytest` 41 passed, sem termos não-determinísticos, originais intactos. **Divergência dos 60 mutantes verificada por probe diferencial** (nenhum equivalente; os subagentes já haviam podado equivalentes em req_005/bug_005 e req_011/bug_004).
- [x] T10 — testes do LLM gerados para os 15 reqs × 2 estratégias (30 arquivos). Quota diária estourou 2×; concluído com chave nova. **Exceção:** `generated_tests/direct/test_req_012.py` saiu degenerado a temp 0 (uma linha gigante de "6", loop de repetição do modelo — saída determinística, ficou cacheada); removida a entrada de cache envenenada e **regenerado a `--temperature 0.4`** (único arquivo fora do temp 0; 32 testes, passa na correta).
- [x] T11 — matriz regenerada p/ 15 reqs: `results_matrix.csv` = **1014 linhas** (`useful=728, weak=270, invalid=16`, 0 `not_executable`). As 16 `invalid` são testes que reprovam na `correct.py` (subespecificação/achados, previstos no plano), não erro de pipeline.
- [x] T12 — `metrics_summary.csv` regenerado (33 linhas: 15 reqs + ALL × 2 estratégias); reproduz byte a byte o versionado. Agregados: direct `bug_det=0.7309 mut_sc=0.9733`; two_step `bug_det=0.7275 mut_sc=0.96`. valid_rate=1.0 em tudo; correct_pass_rate ≥0.91.
- [x] T13 — `mutation_summary.csv` regenerado p/ 15 reqs: **30 configs, todas `ok`** (0 skip/quebra → CA6). `mutation_survivors.csv` = **57 sobreviventes** (req_012=16, req_005=10, req_011=10, req_007=9, req_013=4, req_001=4, req_006=2, req_008=2) p/ triagem (equivalentes vs. lacuna). Discriminação agora real: `mutation_score_auto` 0.71–1.0; reqs maiores não saturam mais (hipótese da Fase 3 confirmada). Rodado no **WSL** (mutmut só roda em Linux).
- [ ] T14 — docs (tabela 3→15 + N).

### ⚠️ AMBIENTE (mudou desde a Fase 2 — LER ANTES DE RODAR)
- **Usar SEMPRE o env conda `llm-req-coverage`**: `python.exe` em `C:\Users\Eduar\miniconda3\envs\llm-req-coverage\` (Python **3.11.15** conda-forge, pytest 9.1.0, pygments OK, mutmut 3.6.0). O `python` "nu" do PATH resolve para o Python 3.11 do **AppData**, cujo pytest está QUEBRADO (sem `pygments`) → toda a matriz vira `not_executable`. STATE da Fase 2 dizia "miniconda 3.13" — **desatualizado**.
- `conda` não está no PATH do shell; invocar o interpretador por caminho absoluto.
- **mutmut tem guard rígido de plataforma:** `mutmut/__main__.py` faz `if platform.system()=="Windows": sys.exit(1)` no import (qualquer subcomando). Logo o `mutmut` NÃO roda no env conda do Windows — só `run_tests.py`/`metrics.py` (pytest puro) rodam lá.
- **Mutação (T13) roda no WSL:** existe um env conda gêmeo `llm-req-coverage` dentro do WSL Ubuntu (`/home/eduardo/miniconda3/envs/llm-req-coverage`, Python 3.11.15 Linux, pytest 9.1.0, mutmut 3.6.0). Repro: `wsl -d Ubuntu bash -lc "conda activate llm-req-coverage && cd '/mnt/c/.../llm-requirements-document-coverage' && python evaluation/mutation_run.py"` (workdirs vão p/ `/tmp` Linux; lê o repo via `/mnt/c`). Levou ~2 min para as 30 configs.

Decisões de autoria documentadas nos `.md`: req_006 rejeita zero à esquerda; req_008 `year<=0`→False; req_009 retorno com sinal + sentinela `-999999` p/ inválido; req_011 desempate = primeira ocorrência; req_014 saque ignora se sem saldo; req_015 piso 0 no contador.

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