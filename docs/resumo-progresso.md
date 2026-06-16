# Resumo de progresso — sessão atual

> Documento de acompanhamento. Resume tudo que foi feito até agora nesta sessão,
> com ponteiros para os artefatos. Data: 2026-06-16. Branch: `dev/readme-projeto-atual`.

## Visão geral

Dois blocos de trabalho foram concluídos nesta sessão:

1. **Reescrita do `CLAUDE.md`** para refletir a arquitetura atual (avaliação por
   execução / mutation testing), substituindo a descrição do pipeline antigo de
   embeddings que havia sido removido da branch.
2. **Início da Fase 2 — Avaliação por mutação automática**, percorrendo o fluxo
   SDD completo (`spec → plano → tarefas → execução`) e implementando até o
   **checkpoint da camada pura** (tarefas T01–T06), com a suíte verde.

---

## 1. Reescrita do `CLAUDE.md`

- **Problema:** o `CLAUDE.md` descrevia um pipeline de similaridade por embeddings
  (comparação cosseno com benchmark humano) que **não existe mais** nesta branch.
- **Feito:** reescrito do zero a partir do `README.md` e do código real
  (`evaluation/`, `requirements/`, `implementations/`, `prompts/`). Passou a
  documentar: requisitos-como-função, `correct.py` + mutantes, as duas estratégias
  de prompting (`direct`/`two_step`), o harness `generate_tests → run_tests →
  metrics`, as 4 classificações de teste, as 4 métricas, convenções e limitações.
- **Observação:** `CLAUDE.md` é **gitignored** (não versiona); é doc do agente. A
  doc pública equivalente é o `README.md`.

---

## 2. Fase 2 — Avaliação por mutação automática

### Por que

Hoje o `mutation_score` (em `evaluation/metrics.py`) **satura em 1.0** em todas as
configurações, porque cada requisito tem só 5 mutantes manuais simples (efeito
teto + viés de autoria). A métrica não discrimina entre estratégias nem
requisitos. A Fase 2 introduz **mutação automática** (`mutmut`) para gerar dezenas
de mutantes independentes e fazer o score voltar a variar.

### Artefatos do fluxo SDD (em `docs/specs/`)

| Etapa | Arquivo | Conteúdo |
|---|---|---|
| Spec | [mutacao-automatica.md](specs/mutacao-automatica.md) | problema, escopo, fora de escopo, histórias, 5 critérios de aceite |
| Plano | [mutacao-automatica-plan.md](specs/mutacao-automatica-plan.md) | arquitetura em camadas, decisão de ferramenta, impactos, DoD |
| Tarefas | [mutacao-automatica-tasks.md](specs/mutacao-automatica-tasks.md) | 14 tarefas atômicas (T01–T14) com validação cada |

### Decisão de ferramenta

`mutmut==3.6.0` (sobre `cosmic-ray`): apontar a 1 `solution.py` + 1 arquivo de
teste é direto e o custo por config é menor. O risco de saída instável entre
versões 3.x foi mitigado **fixando a versão** e **isolando o parsing** numa camada
pura testada por fixtures.

### O que foi implementado (T01–T06)

Arquitetura em camadas em `evaluation/mutation_run.py`. Esta sessão entregou a
**camada pura** (sem I/O), que é onde mora o risco de regressão:

- `MutationResult` (dataclass: `total`, `killed`, `survived/timeout/suspicious/skipped`).
- `parse_run_total(run_stdout)` — total de mutantes (2º grupo do último `N/N`).
- `parse_results(results_stdout)` — parseia os não-mortos por status; ignora ruído.
- `build_mutation_result(total, by_status)` — `killed = total − nº de não-mortos`.
- `mutation_score(result)` — `killed/total`, `round(…,4)`, `0.0` se `total==0`.

O módulo **não importa `llm_client`** (nem nada que toque a API), para o teste
offline importá-lo sem efeitos colaterais.

### Testes e infraestrutura de teste

- `tests/test_mutation_run.py` — **13 testes** da camada pura, offline (sem invocar
  `mutmut` nem a API), alimentados por:
  - **fixtures reais** capturadas de um probe do `mutmut` em `req_001/direct`
    (`tests/fixtures/mutmut_run_stdout.txt`, `…_results_stdout.txt`, `…_show_survivor.txt`);
  - casos sintéticos no formato exato da saída real (misto survived/timeout/
    suspicious; vazio; ruído).
- `tests/conftest.py` — torna `evaluation/` importável (`import mutation_run`) sem
  empacotar e sem quebrar a execução standalone.
- `pytest.ini` (`testpaths = tests`) — evita que `python -m pytest` na raiz tente
  coletar os `generated_tests/*` (que fazem `from solution import …` e só rodam
  nos diretórios isolados). Sem isso o CA5 quebrava com 6 erros de coleta.

### Estado da suíte

`python -m pytest` na raiz: **13 passed** (verde). Confirmado que o `pytest.ini`
da raiz não interfere nos runs isolados de `run_tests.py`/`mutmut` (cwd em `/tmp`).

### Achados técnicos relevantes (registrados em `STATE.md`)

- **Ambiente:** `python` = miniconda 3.13 (o `environment.yml` declara 3.11 —
  divergência conhecida). Usar sempre `python -m pip` / `python -m mutmut`; o
  binário no PATH aponta para outro interpretador.
- **`mutmut` 3.6.0:** carrega config avidamente (exige `setup.cfg` com
  `source_paths=solution.py` no cwd); exige **baseline verde** (aborta com
  `failed to collect stats` se algum teste falha antes de mutar).
- **Formato de saída:** `run` → linha-resumo `… N/N 🎉K 🙁S …` (🎉=morto,
  🙁=sobrevive); `results` → lista só não-mortos (`solution.x_<fn>__mutmut_<N>: status`).
- **Mutante equivalente real:** o único sobrevivente em `req_001/direct` foi
  `if v < 0` → `if v <= 0` (em `v==0` ambos retornam 0.0) — exemplo concreto de
  que "sobrevivente ≠ necessariamente lacuna de teste".

---

## Commits desta sessão

| Commit | Escopo |
|---|---|
| `586e94d` | `chore`: definições do fluxo SDD (`.claude/`) |
| `bedfde2` | `docs`: spec/plano/tarefas da Fase 2 |
| `e61907f` | `feat(mutation)`: camada pura + deps + fixtures (T01–T06) |

*(O `CLAUDE.md` reescrito não aparece nos commits por ser gitignored.)*

---

## O que falta (T07–T14)

- **T07/T08 — Baseline verde:** ler `results_matrix.csv`, selecionar testes
  `correct == pass`, e guard `should_skip` para config sem verdes.
- **T09/T10 — Camada de I/O:** `prepare_workdir` (solution.py + setup.cfg + testes
  verdes via deselect por node id), `run_mutmut`, `show_survivor_diff`.
- **T11/T12 — Orquestração e CSVs:** `evaluate_config`, `main()`, escrita de
  `mutation_summary.csv` e `mutation_survivors.csv`.
- **T13 — Execução real:** rodar as 6 configs; validar CA2 (score varia) e CA3
  (sobreviventes por config).
- **T14 — Docs:** atualizar `CLAUDE.md`/`README.md`.

O `STATE.md` já contém o mecanismo de deselect por node id validado, que guia T07–T10.
