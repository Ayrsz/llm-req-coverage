# Spec — Avaliação por mutação automática

> Fase 2 de [docs/justificativa-e-plano.md](../justificativa-e-plano.md). Etapa SDD: **spec** (problema, escopo, critérios). O plano técnico (escolha de ferramenta, integração) vem no `/sdd-plan`.

## Problema

Hoje o `mutation_score` calculado em [evaluation/metrics.py](../../evaluation/metrics.py) satura em **1.0 em todas as configurações** (estratégia × requisito). Isso acontece porque cada requisito tem apenas **5 mutantes manuais** (`implementations/req_XXX/bug_00N.py`), simples e de autoria do próprio pesquisador. Consequências:

- **Efeito teto:** a métrica não discrimina — não distingue uma suíte forte de uma fraca, nem `direct` de `two_step`.
- **Viés de autoria:** os mutantes manuais foram escritos sabendo o que os testes provavelmente cobririam, superestimando a detecção.
- **QP3/QP5 enfraquecidas:** sem variação no score, não há sinal para responder "que proporção detecta defeito?" nem "two_step supera direct?".

Precisamos de um `mutation_score` que **volte a variar** — gerado por dezenas de mutantes automáticos e independentes da autoria — para que a detecção de defeito seja um eixo de comparação real entre estratégias e requisitos.

## Escopo

- Adicionar uma ferramenta de **mutação automática** (`mutmut` ou `cosmic-ray`) às dependências (`environment.yml` e `requirements.txt`).
- Criar **`evaluation/mutation_run.py`**: para cada `(requisito, estratégia)`, usar a suíte de testes gerada pelo LLM (`generated_tests/<estrategia>/test_<req>.py`) como conjunto de testes e rodar a ferramenta de mutação sobre a implementação correta (`implementations/req_XXX/correct.py`), montada como `solution.py` num diretório isolado — reaproveitando o padrão de isolamento já usado em [evaluation/run_tests.py](../../evaluation/run_tests.py).
- Coletar, por config, **mutantes mortos e sobreviventes**, e calcular o `mutation_score` automático (mortos / total).
- Persistir os resultados em CSV(s) sob `evaluation/` (uma linha por config, com contagens e o score automático), e **listar os mutantes sobreviventes** por config (sinal direto de lacuna de cobertura).
- Manter os mutantes manuais e a matriz por tipo de falta intactos: o `mutation_score` manual atual continua reportado lado a lado com o automático.
- Cobertura de teste em `tests/` para a lógica nova (parsing de saída da ferramenta, agregação de mortos/sobreviventes, cálculo do score), **sem chamar a API do Gemini nem a ferramenta de mutação real** (usar fixtures/saída sintética).

## Fora de Escopo

- **Não** remover nem alterar os mutantes manuais (`bug_00N.py`) — eles permanecem para a matriz fina por tipo de falta (QP4).
- **Não** regerar testes via LLM nesta feature (a suíte gerada já existe em `generated_tests/`); nenhuma chamada nova à API.
- **Não** implementar a normalização por volume / suíte mínima (isso é a Fase 4) nem a variância multi-seed (Fase 5).
- **Não** adicionar novos requisitos (Fase 3).
- **Não** inspecionar/classificar mutantes equivalentes automaticamente — apenas reportar sobreviventes brutos (a análise qualitativa fica para o relatório, Fase 7).

## Histórias de Usuário

- Como **pesquisador**, quero um `mutation_score` derivado de dezenas de mutantes automáticos, para que a métrica volte a discriminar entre estratégias e requisitos em vez de saturar em 1.0.
- Como **pesquisador**, quero a lista de mutantes sobreviventes por `(requisito, estratégia)`, para identificar lacunas concretas de cobertura dos testes gerados pelo LLM.
- Como **pesquisador**, quero que os mutantes manuais e sua matriz por tipo de falta continuem disponíveis, para não perder a análise por categoria de defeito (QP4).
- Como **mantenedor do harness**, quero testes automatizados da lógica nova que rodem sem rede nem mutação real, para que `python -m pytest` seja rápido, determinístico e reproduzível em CI.

## Critérios de Aceite

1. **Mutantes manuais preservados (QP4).** Os arquivos `implementations/req_XXX/bug_00N.py` permanecem inalterados; `run_tests.py`/`metrics.py` continuam produzindo a matriz por tipo de falta e o `mutation_score` manual como antes. Verificável: rodar os 3 passos existentes ainda reproduz `results_matrix.csv` / `metrics_summary.csv`.
2. **Score automático discrimina.** Após rodar `evaluation/mutation_run.py`, o `mutation_score` automático **não é 1.0 em todas as configs** — varia entre pelo menos duas estratégias e/ou requisitos. Verificável: inspeção do CSV de saída mostra ao menos dois valores distintos de score.
3. **Sobreviventes listados por config.** A saída registra, para cada `(requisito, estratégia)`, os mutantes que nenhum teste matou (identificador/localização do mutante). Verificável: o CSV/arquivo de saída contém a lista de sobreviventes por config (vazia é permitida, mas a coluna/seção existe).
4. **Teste pytest sem API/ferramenta real.** Há ao menos um teste em `tests/` que cobre a lógica nova de `mutation_run.py` (parsing, agregação, cálculo do score) usando saída sintética/fixtures — **sem** invocar a API do Gemini nem executar a ferramenta de mutação de verdade. Verificável: o teste passa offline.
5. **Suíte verde.** `python -m pytest` passa (todos os testes, incluindo os novos).

## Observações para o `/sdd-plan`

- **Decisão pendente:** `mutmut` vs `cosmic-ray`. Critérios a avaliar no plano: facilidade de apontar a ferramenta a um único `solution.py` + um arquivo de teste isolado; formato de saída parseável (mortos/sobreviventes); custo de configuração por config. Ambos suportam execução programática; preferir o de integração mais simples com o padrão de diretório temporário já existente.
- **Reúso:** o isolamento `solution.py` + cópia do teste já está em `run_tests.py::run_against_variant`; a lógica nova deve reaproveitar esse padrão em vez de reimplementá-lo.
- **Free tier:** esta feature **não** chama o LLM; opera sobre a suíte já gerada em `generated_tests/`. Sem impacto de quota.
