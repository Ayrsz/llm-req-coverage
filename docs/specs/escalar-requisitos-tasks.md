# Tarefas — Escalar o número de requisitos (Fase 3)

> Quebra de [escalar-requisitos-plan.md](escalar-requisitos-plan.md) em tarefas atômicas. Etapa SDD: **tasks**. Marque `[x]` ao concluir. Uma tarefa por vez; commits granulares.
>
> Convenção de IDs: **T01..T18**. "Pré-req" lista dependências. As tarefas de autoria (T03–T08) são **independentes entre si** e paralelizáveis depois de T01.

## Bloco A — Rede de segurança (TDD primeiro)

### [x] T01 — Teste de consistência estrutural
- **O que fazer:** criar `tests/test_requirements_consistency.py`, parametrizado por `implementations/req_*`: lê o nome da função em `requirements/<req>.md` (regex `from solution import (\w+)`); carrega `correct.py` e cada `bug_*.py` por caminho (`importlib.util.spec_from_file_location`, nome de módulo único por arquivo); afirma que há `correct.py` e ≥1 `bug_*.py`, que todos importam sem erro e expõem `<nome>` como `callable`.
- **Onde fazer:** `tests/test_requirements_consistency.py` (novo).
- **Pré-req:** nenhuma.
- **Como validar:** `python -m pytest tests/test_requirements_consistency.py` passa para os 3 reqs atuais (rede de segurança ativa antes de adicionar os novos).

## Bloco B — Gabarito e taxonomia

### [x] T02 — Fixar gabarito de requisito e taxonomia de mutantes
- **O que fazer:** registrar (em `STATE.md` ou nota curta) o gabarito de `req_XXX.md` (seções obrigatórias + linha `from solution import`) e a taxonomia dos 5 mutantes (`bug_001` fronteira/off-by-one, `bug_002` operador errado, `bug_003` ramo/retorno trocado, `bug_004` constante errada, `bug_005` guarda ausente/condição invertida), conforme o plano.
- **Onde fazer:** `STATE.md`.
- **Pré-req:** T01.
- **Como validar:** a nota existe e é seguida nas tarefas T03–T08.

## Bloco C — Autoria dos 12 requisitos (paralelizável; 2 por tarefa, por classe)

> Cada tarefa entrega, para os 2 requisitos: `requirements/req_XXX.md` (gabarito completo, com `from solution import`) + `implementations/req_XXX/correct.py` + `bug_001..bug_005.py` (1 defeito cada, taxonomia T02, mesma assinatura, determinístico — sem `now()`/`random`/I/O).
> **Validação comum a T03–T08:** `python -m pytest tests/test_requirements_consistency.py` cobre os novos reqs e passa; leitura dos critérios de aceite no `.md`; `correct.py` satisfaz os ACs declarados.

### [x] T03 — Numérico/fronteira (req_004, req_005)
- **O que fazer:** `req_004` `bmi_category(weight: float, height: float) -> str`; `req_005` `triangle_type(a: int, b: int, c: int) -> str`.
- **Onde fazer:** `requirements/req_004.md`, `req_005.md`; `implementations/req_004/`, `req_005/`.
- **Pré-req:** T01, T02.
- **Como validar:** validação comum do Bloco C.

### [x] T04 — String/validação e transformação (req_006, req_007)
- **O que fazer:** `req_006` `is_valid_ipv4(s: str) -> bool`; `req_007` `slugify(text: str) -> str`.
- **Onde fazer:** `requirements/req_006.md`, `req_007.md`; `implementations/req_006/`, `req_007/`.
- **Pré-req:** T01, T02.
- **Como validar:** validação comum do Bloco C.

### [x] T05 — Data/tempo (req_008, req_009)
- **O que fazer:** `req_008` `is_leap_year(year: int) -> bool`; `req_009` `days_between(start: str, end: str) -> int` (datas ISO **como argumento**, sem `now()`).
- **Onde fazer:** `requirements/req_008.md`, `req_009.md`; `implementations/req_008/`, `req_009/`.
- **Pré-req:** T01, T02.
- **Como validar:** validação comum do Bloco C.

### [x] T06 — Coleção/agregação (req_010, req_011)
- **O que fazer:** `req_010` `average_above(values: list, threshold: float) -> float`; `req_011` `most_frequent(items: list) -> str` (definir desempate no `.md`).
- **Onde fazer:** `requirements/req_010.md`, `req_011.md`; `implementations/req_010/`, `req_011/`.
- **Pré-req:** T01, T02.
- **Como validar:** validação comum do Bloco C.

### [x] T07 — Regra de negócio ramificada (req_012, req_013)
- **O que fazer:** `req_012` `income_tax(income: float) -> float` (faixas progressivas); `req_013` `shipping_cost(weight: float, region: str, express: bool) -> float`.
- **Onde fazer:** `requirements/req_012.md`, `req_013.md`; `implementations/req_012/`, `req_013/`.
- **Pré-req:** T01, T02.
- **Como validar:** validação comum do Bloco C.

### [x] T08 — Estado simples/contador (req_014, req_015)
- **O que fazer:** `req_014` `final_balance(initial: float, operations: list) -> float`; `req_015` `apply_commands(start: int, commands: list) -> int` (estado interno determinístico, sem efeito externo).
- **Onde fazer:** `requirements/req_014.md`, `req_015.md`; `implementations/req_014/`, `req_015/`.
- **Pré-req:** T01, T02.
- **Como validar:** validação comum do Bloco C.

## Bloco D — Verificação do conjunto

### [x] T09 — Suíte verde com os 15 requisitos
- **O que fazer:** rodar a suíte completa da ferramenta com o conjunto ampliado.
- **Onde fazer:** —.
- **Pré-req:** T03–T08.
- **Como validar:** `python -m pytest` verde (harness + consistência), sem chamar a API; `ls requirements/req_*.md | wc -l` = 15 e `ls -d implementations/req_*/ | wc -l` = 15 (**CA1**); diversidade conferida na tabela do plano (**CA2**).

## Bloco E — Regeneração do pipeline (ordem importa)

### [x] T10 — Gerar testes do LLM (faseado por quota)
- **O que fazer:** `python evaluation/generate_tests.py --sleep N` para os novos reqs (apoiar no cache; retomar entre dias se a quota estourar). Não-bloqueante: configs não geradas viram `skip`/`skipped` adiante.
- **Onde fazer:** `generated_tests/{direct,two_step}/`.
- **Pré-req:** T03–T08.
- **Como validar:** existem `test_req_XXX.py` para os reqs gerados; quota esgotada não derruba o restante do pipeline.

### [ ] T11 — Regenerar a matriz de execução
- **O que fazer:** `python evaluation/run_tests.py` (precisa vir **antes** do `mutation_run.py`, que lê a matriz para o baseline verde).
- **Onde fazer:** `evaluation/results_matrix.csv`.
- **Pré-req:** T10.
- **Como validar:** a matriz cobre os reqs com teste gerado; reqs sem teste aparecem como `skip`; arquivo regenerado sem erro.

### [ ] T12 — Recalcular métricas
- **O que fazer:** `python evaluation/metrics.py`.
- **Onde fazer:** `evaluation/metrics_summary.csv`.
- **Pré-req:** T11.
- **Como validar:** `metrics_summary.csv` tem linhas por estratégia/requisito para o conjunto ampliado.

### [ ] T13 — Rodar mutação automática no conjunto ampliado
- **O que fazer:** `python evaluation/mutation_run.py` (após T11).
- **Onde fazer:** `evaluation/mutation_summary.csv`, `mutation_survivors.csv`.
- **Pré-req:** T11.
- **Como validar:** `mutation_summary.csv` tem linha por config; configs sem teste verde = `skipped`; sem quebra (**CA6**).

## Bloco F — Documentação

### [ ] T14 — Atualizar tabela de requisitos e N nas docs
- **O que fazer:** atualizar a tabela "Requisitos atuais" (3 → 15, com classe) e o N citado nas limitações.
- **Onde fazer:** `README.md` e `CLAUDE.md`.
- **Pré-req:** T09.
- **Como validar:** ambos listam os 15 reqs; revisão de leitura.

## Definition of Done (espelha o plano)

- [x] DoD1 — CA1: 15 reqs + 15 dirs; `req_001..003` intactos. *(T09)*
- [x] DoD2 — CA2: 6 classes representadas. *(T03–T08, T09)*
- [x] DoD3 — CA3: cada novo req com `correct.py` + 5 `bug_*.py`, 1 defeito, importáveis. *(T03–T08)*
- [x] DoD4 — CA4: teste de consistência cobre todos e passa. *(T01, T03–T08)*
- [x] DoD5 — CA5: `python -m pytest` verde, sem API. *(T09)*
- [ ] DoD6 — CA6: 4 CSVs regenerados; `skip`/`skipped` sem quebra. *(T11, T12, T13)*
- [ ] DoD7 — docs atualizadas. *(T14)*

## Paralelização

- **Sequencial obrigatório:** T01 → T02 → (autoria) → T09; e no pipeline T10 → **T11** → {T12, T13}.
- **Paralelizável:** T03–T08 (autoria de pares de requisitos) são independentes entre si após T02. T12 e T13 podem rodar em paralelo, ambas após T11.
- **Ordem crítica:** `run_tests.py` (T11) **sempre antes** de `mutation_run.py` (T13) — o baseline verde lê `results_matrix.csv`.
