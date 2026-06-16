# Plano técnico — Escalar o número de requisitos (Fase 3)

> Plano de engenharia para [escalar-requisitos.md](escalar-requisitos.md). Etapa SDD: **plano**. Não implementa código. Baseado no estado atual do repositório.

## Resumo

Feature de **conteúdo**, não de ferramenta: autorar 12 novos requisitos
(`req_004`..`req_015`) + implementações (correct + mutantes), adicionar um teste
de consistência estrutural e regenerar os 4 CSVs. O harness não muda — `run_tests.py`
e `mutation_run.py` já descobrem requisitos por `impl_root.glob("req_*")`
([run_tests.py:163](../../evaluation/run_tests.py#L163),
[mutation_run.py:343](../../evaluation/mutation_run.py#L343)) e
`generate_tests.py` por `requirements/glob("req_*.md")`.

## Arquitetura afetada

### Novos requisitos (conteúdo) — lista concreta

12 novos, cobrindo as 6 classes exigidas (CA2). Assinatura sempre com módulo
`solution` e função determinística. Proposta:

| Req | Classe | Tema | Assinatura |
|---|---|---|---|
| `req_004` | numérico/fronteira | categoria de IMC | `bmi_category(weight: float, height: float) -> str` |
| `req_005` | numérico/fronteira | tipo de triângulo | `triangle_type(a: int, b: int, c: int) -> str` |
| `req_006` | string/validação | validar IPv4 | `is_valid_ipv4(s: str) -> bool` |
| `req_007` | string/transformação | slug de título | `slugify(text: str) -> str` |
| `req_008` | data/tempo | ano bissexto | `is_leap_year(year: int) -> bool` |
| `req_009` | data/tempo | dias entre datas ISO | `days_between(start: str, end: str) -> int` |
| `req_010` | coleção/agregação | média acima de limiar | `average_above(values: list, threshold: float) -> float` |
| `req_011` | coleção/agregação | item mais frequente | `most_frequent(items: list) -> str` |
| `req_012` | regra ramificada | imposto progressivo | `income_tax(income: float) -> float` |
| `req_013` | regra ramificada | custo de frete | `shipping_cost(weight: float, region: str, express: bool) -> float` |
| `req_014` | estado simples | saldo após operações | `final_balance(initial: float, operations: list) -> float` |
| `req_015` | estado simples | aplicar comandos a contador | `apply_commands(start: int, commands: list) -> int` |

Datas entram **como argumento string ISO** (`days_between`), nunca via `now()` —
mantém determinismo (Fora de Escopo da spec). Cada `requirements/req_XXX.md`
segue o gabarito de `req_001..003`: descrição, módulo `solution`, **assinatura**,
regras, classes de equivalência, valores-limite, entradas inválidas, invariantes,
critérios de aceitação, **incluindo a linha `from solution import <nome>`** (âncora
usada pelo teste de consistência — presente em todos os reqs atuais).

### Implementações — `implementations/req_XXX/`

Para cada novo req: `correct.py` + **5 `bug_*.py`** (mantém o padrão dos 3 atuais;
satisfaz CA3 que pede ≥3). Cada mutante introduz **um único defeito**, derivado
de uma **taxonomia de faltas** explícita:

| bug | tipo de falta |
|---|---|
| `bug_001` | fronteira / off-by-one (`<` vs `<=`, limite incluso/excluso) |
| `bug_002` | operador errado (aritmético ou de comparação trocado) |
| `bug_003` | ramo/retorno trocado (classe certa, valor de outra) |
| `bug_004` | constante/literal errado (taxa, limite, mensagem) |
| `bug_005` | guarda ausente / condição invertida (caso inválido não tratado) |

A taxonomia é a mesma família já usada implicitamente nos `req_001..003`,
agora documentada para consistência e para a matriz por tipo de falta (QP4).

### Teste de consistência — `tests/test_requirements_consistency.py` (novo)

Offline, sem API, **parametrizado por `implementations/req_*`**:

- descobre a função declarada lendo `from solution import <nome>` no
  `requirements/<req>.md` (regex `from solution import (\w+)`);
- carrega `correct.py` e cada `bug_*.py` **por caminho** via
  `importlib.util.spec_from_file_location` com **nome de módulo único** por
  arquivo (evita colisão entre funções homônimas);
- afirma: existe `correct.py` e ≥1 `bug_*.py`; cada módulo importa sem erro e
  expõe `<nome>` como `callable`.

Não monta `solution.py` nem chama pytest aninhado — só importa e introspecta.
Roda para **todos** os requisitos (inclui `req_001..003`), então também é uma
rede de segurança para o conjunto existente.

### Artefatos regenerados (gerados, versionados)

`evaluation/results_matrix.csv`, `metrics_summary.csv`, `mutation_summary.csv`,
`mutation_survivors.csv` — regerados sobre os 15 requisitos.

### Documentação

`README.md` e `CLAUDE.md`: atualizar a tabela "Requisitos atuais" (de 3 para 15,
com classe) e o N citado nas limitações.

## Mudanças no banco/APIs

- **Sem banco de dados.**
- **API do LLM (Gemini), com custo de quota:** `generate_tests.py` precisa rodar
  para os 12 novos × 2 estratégias = **24+ gerações** (free tier ~20/dia). Isto
  é a única dependência externa e o principal gargalo. Mitigações já existentes:
  cache em disco (`evaluation/.cache/`), `--sleep`, `--limit`. **Decisão do plano:**
  a geração é **faseada e não-bloqueante** para o restante — autoria de
  requisitos/implementações e o teste de consistência (CA1–CA5) **não** dependem
  da API; só o CA6 (pipeline regenerado com testes do LLM) depende, e o próprio
  CA6 admite configs ainda-não-geradas como `skip`/`skipped`. Assim a feature
  fecha em conteúdo+consistência mesmo que a geração leve alguns dias de quota.

## Impactos colaterais

- **Colunas de bug na matriz crescem com o máximo global.** `run_tests.py` monta
  `bug_001..bug_00N` com `max_bugs` entre **todos** os requisitos
  ([run_tests.py:185](../../evaluation/run_tests.py#L185)). Se todos os novos
  reqs tiverem 5 mutantes, segue `bug_001..bug_005`; reqs com menos bugs deixam
  células vazias — `metrics.py::bugs_present` já trata isso (conta só colunas não
  vazias por requisito). Manter 5 por req evita surpresa.
- **`pytest.ini` (`testpaths = tests`)** garante que os novos `generated_tests/*`
  e os `implementations/*` **não** sejam coletados pela suíte da ferramenta — o
  novo teste de consistência vive em `tests/` e é coletado normalmente.
- **Tempo de execução cresce ~5×.** `run_tests.py` roda pytest por (teste×variante)
  e `mutation_run.py` roda o `mutmut` por config; com 15 reqs a etapa de mutação
  fica visivelmente mais lenta. Mitigar com `--limit`/`--strategy`/`--timeout` já
  existentes; não requer mudança de código.
- **Baseline verde por config (Fase 2) depende de `results_matrix.csv`.** A ordem
  de regeneração importa: `run_tests.py` **antes** de `mutation_run.py`, senão o
  filtro de baseline verde lê uma matriz desatualizada (sem os novos reqs).
- **Subespecificação vira `invalid` (achado, não bug).** Requisitos novos mais
  ricos têm mais chance de gerar testes que assumem comportamento não fixado e
  reprovam na `correct.py`. Isso é resultado de pesquisa; o filtro de baseline
  verde do `mutation_run.py` já os deseleciona. Redigir os `req_XXX.md` o mais
  fechados possível reduz ruído.
- **Risco de mutante manual com 2 defeitos / não-importável.** Quebraria CA3/CA4.
  O teste de consistência pega o "não-importável"; o "um único defeito" é
  garantido por revisão na autoria (não há verificação automática de
  "exatamente um defeito").
- **Determinismo das implementações.** Proibido `now()`, `random`, I/O. O revisor
  confere na autoria; o teste de consistência não detecta não-determinismo.

## Definition of Done

1. **CA1 (N=15):** 15 `requirements/req_XXX.md` e 15 `implementations/req_XXX/`;
   `req_001..003` inalterados (`git` confirma).
2. **CA2 (diversidade):** as 6 classes da tabela representadas entre os novos.
3. **CA3 (contrato):** cada novo req tem `correct.py` + 5 `bug_*.py`, mesma
   assinatura, um defeito por mutante, todos importáveis.
4. **CA4 (consistência):** `tests/test_requirements_consistency.py` cobre todos os
   `req_*` e passa, offline.
5. **CA5:** `python -m pytest` verde (harness + consistência), sem API.
6. **CA6 (pipeline):** `run_tests.py` → `metrics.py` → `mutation_run.py` (nessa
   ordem) regeneram os 4 CSVs cobrindo os 15 reqs; configs sem teste gerado
   aparecem como `skip`/`skipped`, sem quebrar.
7. **Docs:** tabela de requisitos e N atualizados em `README.md`/`CLAUDE.md`.

## Sequência sugerida para o `/sdd-tasks`

1. **Teste de consistência primeiro (TDD):** `tests/test_requirements_consistency.py`
   parametrizado — passa para os 3 atuais, será a rede de segurança dos novos.
2. **Autoria em lotes por classe** (1 tarefa por par de requisitos ou por classe):
   `req_XXX.md` + `correct.py` + 5 mutantes; validação = consistência verde +
   leitura dos critérios de aceite no md.
3. **Regeneração do pipeline** (após ter ao menos parte dos testes gerados):
   `run_tests.py` → `metrics.py` → `mutation_run.py`; commitar os 4 CSVs.
4. **Geração de testes do LLM** (faseada por quota; cache): `generate_tests.py
   --sleep --limit`, retomando entre dias se necessário.
5. **Docs:** atualizar tabelas e N.
