# Plano técnico — Avaliação por mutação automática

> Plano de engenharia para [mutacao-automatica.md](mutacao-automatica.md). Etapa SDD: **plano**. Não implementa código. Baseado no estado atual do repositório.

## Decisão de ferramenta: manter `mutmut`, agora com versão fixada e validada (`3.6.0`); a config correta é `source_paths`, não `paths_to_mutate`.

## Arquitetura afetada
 
### Configuração do `mutmut`
 
- Fixar **`mutmut==3.6.0`** em `requirements.txt`/`environment.yml`. Os formatos de saída abaixo são dessa versão; a série 3.x muda saída entre releases.
- O `setup.cfg` escrito no dir isolado usa **`source_paths=solution.py`** (NÃO `paths_to_mutate`, que está deprecado no 3.6.0 e emite um `UserWarning`
  que polui a saída lida pelo parser):
```ini
  [mutmut]
  source_paths=solution.py
```
 
### Pré-requisito obrigatório: baseline verde (NOVO — bloqueador)
 
`mutmut` roda a suíte na implementação **sem mutação** antes de mutar; se **qualquer** teste falhar nessa etapa, ele aborta toda a execução
(`failed to collect stats. runner returned 1`) e não testa nenhum mutante.
 
Como a suíte gerada pode conter testes `invalid` (falham na `correct.py` — já existe um em `req_001/two_step`), o `mutation_run.py` precisa rodar o `mutmut` **apenas com o subconjunto de testes que passam na correta**.
 
- **Fonte do subconjunto:** `evaluation/results_matrix.csv` já classifica cada teste por `correct == pass`. Reusar isso (acopla os dois harnesses) em vez de recalcular.
- **Como aplicar:** ao montar o `test_generated.py` no dir isolado, incluir só as funções/testes cujo `correct == pass` para aquele `(requisito, estratégia)`. Se a granularidade do arquivo de teste não permitir remover funções individuais com segurança, usar deselect do pytest (`--deselect`) pelos nomes reprovados. Decisão fina fica para as tasks; o **invariante** é: o baseline passado ao `mutmut` é verde.
- Se, após o filtro, sobrarem **0 testes** para a config, registrar a config como `skipped` no summary (não é falha do harness).

### Novo: `evaluation/mutation_run.py`
 
Mesma estrutura em camadas do plano, com o parser ajustado ao formato real. **`mutation_run.py` não importa `llm_client`** (nem qualquer coisa que toque a API), para o teste offline (CA4) importar o módulo sem efeitos colaterais.
 
- **Camada de invocação (I/O, não unit-testada):**
  - `prepare_workdir(req_id, strategy, passing_tests) -> Path`: dir temporário; copia `implementations/req_XXX/correct.py` → `solution.py`; escreve
    `setup.cfg` (`source_paths=solution.py`); escreve `test_generated.py` contendo **apenas os testes verdes** (ver pré-requisito). Reusa o padrão de
    isolamento de `run_tests.py::run_against_variant`. 
  - `run_mutmut(workdir, timeout) -> tuple[str, str]`: executa, **com cwd no workdir**, `mutmut run` e captura a stdout (para o total) e, em seguida,
    `mutmut results` (para a lista de não-mortos). Único ponto que chama a ferramenta real. Devolve as duas saídas brutas.
  - `show_survivor_diff(workdir, mutant_id) -> str` (para CA3 acionável): `mutmut show <id>` com cwd no workdir, devolve o diff bruto.
- **Camada pura (unit-testada com fixtures sintéticas — CA4):**
  - `parse_run_total(run_stdout: str) -> int`: extrai o total de mutantes da linha-resumo do `mutmut run` via regex sobre `(\d+)/(\d+)` (o segundo grupo). Exemplo real da linha (com emojis e spinners no entorno): `26/26  🎉 21 🫥 0  ⏰ 0  🤔 0  🙁 5  🔇 0  🧙 0`
  - `parse_results(results_stdout: str) -> dict[str, list[str]]`: o `mutmut results` lista **só os não-mortos**, uma linha por mutante no formato `    solution.<nome_mascarado>__mutmut_<N>: <status>` (`status` ∈ `survived | timeout | suspicious | skipped`). Devolve `{status: [ids]}`. Deve ignorar linhas de ruído (o `UserWarning`, linhas em branco).
  - `build_mutation_result(total, results_by_status) -> MutationResult`: `MutationResult` = dataclass com `total: int`, `killed: int`, `survived: list[str]`, `timeout: list[str]`, `suspicious: list[str]`, `skipped: list[str]`. Convenção (explícita e a manter consistente): **`killed = total - (len de todas as linhas do `results`)`** — ou seja, tudo que o `m utmut results` lista é "não-morto"; o resto é morto.
  - `mutation_score(result) -> float`: `killed / total` (0.0 se `total == 0`), arredondado com `round(x, 4)` como em `metrics.py`.
- **Orquestração:**
  - `evaluate_config(req_id, strategy, passing_tests, timeout) -> dict`: invocação → parsing → score, para uma config.
  - `main()`: para cada `(requisito × estratégia)` com teste gerado existente, lê os testes verdes de `results_matrix.csv`, roda `evaluate_config`, agrega e grava os CSVs. Flags análogas às existentes: `--timeout`, e (recomendado) `--limit`/`--strategy` por causa do custo.

### Saída (novos artefatos sob `evaluation/`)
 
- `evaluation/mutation_summary.csv`: uma linha por `(requirement, strategy)` com `requirement, strategy, mutants_total, mutants_killed, mutants_survived, mutants_timeout, mutants_suspicious, mutation_score_auto, status` (`status` ∈ `ok | skipped`). Nomeação no padrão de `metrics_summary.csv`.
- `evaluation/mutation_survivors.csv`: uma linha por mutante sobrevivente, com `requirement, strategy, mutant_id, status, diff` — `diff` vindo de
  `mutmut show` (CA3 acionável). Registrar que sobrevivente pode ser **mutante equivalente** (inmatável) e que a leitura "sobrevivente = lacuna de cobertura" exige triagem humana.

### Testes: `tests/test_mutation_run.py`
 
- Cobrir, **sem invocar `mutmut` nem a API**, com fixtures que reproduzem a saída real (incluindo o `UserWarning` e ruído):
  - `parse_run_total`: linha-resumo real; caso sem match → erro/ valor sentinela.
  - `parse_results`: misto de `survived`/`timeout`/`suspicious`; lista vazia (todos mortos); linhas de ruído ignoradas.
  - `build_mutation_result` + `mutation_score`: morto/sobrevivente/misto, e `total == 0` (divisão por zero).
  - Montagem da linha de `mutation_summary.csv` e de `mutation_survivors.csv`.
- Limpar/ignorar o `__pycache__` órfão em `tests/`. Garantir import de `mutation_run` (ex.: `conftest.py` ajustando `sys.path`) **sem** empacotar e **sem** quebrar a execução standalone dos scripts.

### Documentação
 
- `CLAUDE.md`/`README.md`: acrescentar `mutation_run.py` aos comandos/estrutura; descrever `mutation_score_auto` (mutmut, muitos mutantes) **vs** `mutation_score` manual (5 mutantes por requisito) lado a lado, deixando claro que **não são numericamente comparáveis** (conjuntos de mutantes diferentes), e sim complementares.

---

## Mudanças no banco/APIs

- **Nenhuma chamada de API externa.** A feature opera sobre a suíte já gerada em `generated_tests/` e a implementação `correct.py`. Sem uso do Gemini, sem impacto de quota.
- **Sem banco de dados.** Persistência é CSV em disco, no mesmo padrão dos artefatos existentes. (Caso a implementação use `cosmic-ray`, ele cria um sqlite de sessão **efêmero** no dir temporário, descartado ao fim — não é estado versionado.)
- **Subprocess novo:** `mutmut` é invocado via subprocess, análogo ao `pytest` em `run_tests.py`. Precisa de `timeout` (flag, como o `--timeout` de `run_tests.py`).

## Impactos colaterais

- **Pipeline existente intacto (CA1).** `mutation_run.py` é um script novo e independente; não altera `generate_tests.py`, `run_tests.py`, `metrics.py` nem os `bug_00N.py`. O `mutation_score` manual de `metrics.py` continua sendo reportado; o automático é **adicional e lado a lado**.
- **Importabilidade de `evaluation/`.** Os scripts hoje rodam standalone (`python evaluation/x.py`) e importam módulos irmãos por estarem no mesmo dir (ex.: `import llm_client`). Para os testes em `tests/` importarem a lógica de `mutation_run.py`, será preciso um mecanismo de import (ex.: `conftest.py` ajustando `sys.path`, ou import por caminho). Escolher a abordagem mínima que **não** force empacotamento e **não** quebre a execução standalone.
- **Tempo de execução.** Mutação automática roda a suíte uma vez por mutante; com dezenas de mutantes × 6 configs (3 req × 2 estratégias), é a etapa mais lenta do harness. Mitigar com `timeout` por config e, se necessário, flag `--limit`/`--strategy` análoga às existentes.
- **Determinismo.** `mutmut` enumera mutantes de forma determinística sobre o mesmo `solution.py`; o score deve ser reproduzível. Registrar a versão fixada garante isso entre máquinas.
- **Risco de score ainda saturado.**  o probe mostrou ~26 mutantes e ~5 sobreviventes (score ~0,81) numa função do tamanho de `req_001`. A saturação é improvável já nos requisitos atuais; CA2 deve fechar sem depender da Fase 3.
- **`mutmut` e `from solution import`.** Como o teste importa `solution` e mutamos `solution.py` no dir isolado, o runner do `mutmut` precisa ser executado **com cwd no dir isolado** (igual ao `pytest` em `run_against_variant`). Validar na execução.

## Definition of Done

1. `evaluation/mutation_run.py` existe, roda standalone (`python evaluation/mutation_run.py`) e, para cada `(requisito × estratégia)` com teste gerado, produz `evaluation/mutation_summary.csv` com `mutation_score_auto` por config.
2. **CA1:** `bug_00N.py` inalterados; os 3 passos antigos (`generate_tests`→`run_tests`→`metrics`) seguem reproduzindo `results_matrix.csv`/`metrics_summary.csv` com o `mutation_score` manual.
3. **CA2:** o `mutation_score_auto` apresenta ≥2 valores distintos entre configs (não é 1.0 em tudo). Verificável por inspeção do CSV.
4. **CA3:** os mutantes sobreviventes são listados por `(requisito, estratégia)` no artefato de saída.
5. **CA4:** `tests/test_mutation_run.py` cobre parsing + score + montagem de linha com saída sintética, **sem** invocar `mutmut` nem a API; passa offline.
6. **CA5:** `python -m pytest` passa (suíte verde), incluindo os novos testes.
7. `mutmut` (versão fixada) adicionado a `requirements.txt` e `environment.yml`; instalação limpa roda a feature.
8. `CLAUDE.md`/`README.md` atualizados mencionando `mutation_run.py` e o score automático vs manual.
9. "O `mutmut` recebe sempre um baseline verde: testes que reprovam na `correct.py` são filtrados via `results_matrix.csv` antes da execução; config sem testes verdes é marcada `skipped`, não falha."

## Sequência para o `/sdd-tasks` (substitui a original)
 
1. **Dependência:** adicionar `mutmut==3.6.0` a `requirements.txt`/`environment.yml`
   e validar que instala e roda no ambiente.
2. **Camada pura + testes (TDD, teste primeiro):** `MutationResult`,
   `parse_run_total`, `parse_results`, `build_mutation_result`, `mutation_score`,
   com `tests/test_mutation_run.py` alimentado por **fixtures da saída real**
   (capturadas do probe: linha-resumo, lista de `results`, ruído de warning).
3. **Filtro de baseline verde:** função que, dada uma config, lê
   `results_matrix.csv` e devolve os testes com `correct == pass`; testar a
   seleção. (É o passo que impede o `mutmut` de abortar.)
4. **Camada de invocação:** `prepare_workdir` (com `setup.cfg source_paths` +
   testes verdes), `run_mutmut` (cwd no workdir; captura `run` e `results`),
   `show_survivor_diff`. Reusa isolamento de `run_tests.py`.
5. **Orquestração + CSVs:** `evaluate_config`, `main()`, escrita de
   `mutation_summary.csv` e `mutation_survivors.csv`; tratar config sem testes
   verdes como `skipped`.
6. **Rodar nas 6 configs:** confirmar CA2 (≥2 scores distintos, não-saturado) e
   CA3 (sobreviventes com diff por config). Registrar achados.
7. **Docs:** atualizar `CLAUDE.md`/`README.md`.
