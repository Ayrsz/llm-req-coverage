# Spec — Escalar o número de requisitos (Fase 3)

> Fase 3 de [docs/justificativa-e-plano.md](../justificativa-e-plano.md). Etapa SDD: **spec** (problema, escopo, critérios). O plano técnico vem no `/sdd-plan`.

## Problema

O piloto tem **apenas 3 requisitos** (`req_001` desconto, `req_002` senha,
`req_003` faixa etária). Com N=3 nenhuma conclusão das questões de pesquisa é
robusta: as taxas (`valid_rate`, `correct_pass_rate`, `bug_detection_rate`) e a
comparação `direct × two_step` (QP5) variam muito por requisito, e a Fase 2
mostrou que o `mutation_score_auto` só discriminou em 1 dos 3 requisitos —
sinal de que **funções-brinquedo demais e poucas** não dão poder estatístico nem
diversidade de classes de defeito.

O desenho experimental original mira **10–20 requisitos**. Escalar de 3 para
**15**, cobrindo classes variadas de problema, é o passo que mais fortalece as
conclusões — e é barato, porque a receita de "adicionar um requisito" já está
documentada e o harness (`generate_tests → run_tests → metrics → mutation_run`)
já roda sobre qualquer `req_XXX`.

## Escopo

- Autorar **12 novos requisitos** (`req_004`..`req_015`+), atingindo **15 no
  total**, cada um seguindo o contrato existente: `requirements/req_XXX.md` com
  descrição, **módulo `solution`**, **assinatura**, regras, classes de
  equivalência, valores-limite, entradas inválidas, invariantes e critérios de
  aceitação.
- Cobrir **classes de problema variadas** (não repetir o perfil dos 3 atuais):
  pelo menos numérico/fronteira, string/validação, **datas/tempo**, **coleções/**
  agregação**, regra de negócio com ramificação, e estado simples/contador.
- Para cada novo requisito: `implementations/req_XXX/correct.py` +
  `bug_001.py..bug_00N.py` (mesma assinatura; **um único defeito** por mutante;
  derivados de uma taxonomia de faltas; sem erro de sintaxe/import).
- Um **teste de consistência estrutural** (em `tests/`, offline) que valida o
  conjunto de requisitos: cada `implementations/req_*` tem `correct.py` e ≥1
  `bug_*.py`, todos importáveis, com a função da assinatura declarada.
- Regenerar os artefatos do pipeline para o conjunto ampliado: `results_matrix.csv`,
  `metrics_summary.csv`, `mutation_summary.csv`, `mutation_survivors.csv`.

## Fora de Escopo

- **Não** alterar o harness (`generate_tests.py`, `run_tests.py`, `metrics.py`,
  `mutation_run.py`) nem a lógica de métricas/classificação — a feature é de
  **conteúdo** (requisitos + implementações), não de ferramenta. Ajuste no harness
  só se um requisito legítimo expuser um bug nele (aí vira correção pontual).
- **Não** mexer nos `req_001..req_003` existentes nem em seus mutantes.
- **Não** introduzir requisitos que dependam de I/O, rede, relógio do sistema,
  aleatoriedade ou estado externo — mantém-se o escopo de funções pequenas e
  **determinísticas** (datas entram como argumento, não via `now()`).
- **Não** implementar mutação automática nova (já existe, Fase 2), nem a
  comparação normalizada/variância (Fases 4/5).
- **Não** depender de validade externa / documentos reais (Fase 6).

## Histórias de Usuário

- Como **pesquisador**, quero ≥10 requisitos cobrindo classes de problema
  diversas, para que as taxas e a comparação `direct × two_step` deixem de ser
  dominadas por idiossincrasia de 3 funções.
- Como **pesquisador**, quero requisitos que produzam mais mutantes automáticos
  não-triviais, para que o `mutation_score_auto` discrimine em mais de 1
  requisito (relaxando o teto observado na Fase 2).
- Como **mantenedor do harness**, quero um teste de consistência que falhe se um
  requisito for adicionado fora do contrato (sem `correct.py`, sem mutante, com
  assinatura divergente), para que o conjunto cresça sem quebrar o pipeline.
- Como **avaliador**, quero o pipeline regenerado para o conjunto ampliado, para
  ler métricas e mutation score do novo N num único conjunto de CSVs.

## Critérios de Aceite

1. **N = 15.** `requirements/` tem 15 `req_XXX.md` e `implementations/` tem 15
   diretórios `req_XXX/` correspondentes; os 3 originais permanecem inalterados
   (verificável por `git`).
2. **Diversidade.** Entre os novos requisitos há ao menos uma instância de cada
   classe: numérico/fronteira, string/validação, **data/tempo**, **coleção/
   agregação**, regra de negócio ramificada, estado simples. (Verificável por
   inspeção da tabela de requisitos no plano/relatório.)
3. **Contrato por requisito.** Cada `req_XXX.md` novo declara módulo `solution` e
   assinatura; cada `implementations/req_XXX/` tem `correct.py` + ≥3 `bug_*.py`,
   todos com **um único defeito**, mesma assinatura, importáveis sem erro.
4. **Teste de consistência (offline, sem API).** Existe um teste em `tests/` que,
   para todo `implementations/req_*`, verifica: há `correct.py` e ≥1 `bug_*.py`;
   `correct.py` importa e expõe a função declarada; cada `bug_*.py` importa e
   expõe a mesma função. O teste passa.
5. **`python -m pytest` verde** (harness + consistência), sem chamar a API.
6. **Pipeline regenerado.** `run_tests.py`, `metrics.py` e `mutation_run.py`
   rodam sobre o conjunto ampliado e produzem os 4 CSVs cobrindo **todos** os
   requisitos (≥15). Para os requisitos cujos testes do LLM foram gerados, há
   linha na matriz e nas métricas; configs sem teste gerado aparecem como `skip`
   (matriz) / `skipped` (mutação), sem quebrar a execução.

## Observações para o `/sdd-plan` (não são compromissos da spec)

- **Restrição de quota (free tier ~20 gerações/dia):** gerar testes para 12 novos
  requisitos × 2 estratégias = 24+ chamadas. A geração pode precisar ser
  **incremental** (`--limit`, `--sleep`) e apoiada pelo cache em disco; o CA6
  admite que parte das configs ainda não tenha teste gerado, contanto que o
  pipeline as trate como `skip`/`skipped` em vez de falhar. O plano decide se a
  meta de "todos gerados" é bloqueante ou faseada.
- A taxonomia de faltas para os mutantes manuais e a lista concreta de
  requisitos (tema + assinatura por classe) são detalhadas no plano.
