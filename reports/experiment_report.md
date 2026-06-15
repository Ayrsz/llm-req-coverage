# Relatório do Experimento — Avaliação Executável de Testes Gerados por LLM

> Gerado a partir de `evaluation/results_matrix.csv` e `evaluation/metrics_summary.csv`.
> Para reproduzir: `generate_tests.py` → `run_tests.py` → `metrics.py`.

## 1. Configuração do experimento

- **Modelo gerador:** gemini-2.5-flash
- **Temperatura:** 0.0 (determinística)
- **Data da execução:** 2026-06-15
- **Requisitos:** req_001 (desconto), req_002 (senha), req_003 (faixa etária)
- **Bugs por requisito:** 5 (15 mutantes no total)
- **Estratégias:** direct, two_step
- **Testes gerados (funções):** 142 (direct 73, two_step 69)

## 2. Métricas agregadas (linhas `ALL`)

| Estratégia | valid_rate | correct_pass_rate | bug_detection_rate | mutation_score | redundância |
| ---------- | ---------: | ----------------: | -----------------: | -------------: | ----------: |
| direct     |       1.00 |            0.9452 |             0.6667 |           1.00 |          40 |
| two_step   |       1.00 |            1.0000 |             0.7101 |           1.00 |          43 |

## 3. Mutation score por requisito

| Requisito | Estratégia | Bugs totais | Bugs mortos | mutation_score |
| --------- | ---------- | ----------: | ----------: | -------------: |
| req_001   | direct     |           5 |           5 |           1.00 |
| req_001   | two_step   |           5 |           5 |           1.00 |
| req_002   | direct     |           5 |           5 |           1.00 |
| req_002   | two_step   |           5 |           5 |           1.00 |
| req_003   | direct     |           5 |           5 |           1.00 |
| req_003   | two_step   |           5 |           5 |           1.00 |

Em **todas** as combinações o conjunto de testes gerado matou os 5 mutantes do
requisito (mutation_score = 1.0). Ou seja, considerando o suíte inteiro, o modelo
detectou todos os defeitos controlados.

## 4. Distribuição das classificações (142 testes)

| Classificação    | Total |
| ---------------- | ----: |
| `useful`         |    95 |
| `weak`           |    43 |
| `invalid`        |     4 |
| `not_executable` |     0 |

## 5. Análise das Questões de Pesquisa

### QP1 — Executabilidade (valid_rate = 1.00)
Todos os 142 testes gerados foram sintaticamente válidos e executáveis. O modelo
respeitou a instrução de importar do módulo `solution` com a assinatura correta —
nenhum `not_executable`. Forte indício de que LLMs lidam bem com a mecânica de
gerar pytest a partir de requisitos pequenos e bem definidos.

### QP2 — Correção (correct_pass_rate: two_step 1.00, direct 0.945)
Os únicos 4 testes `invalid` estão em **req_001 / direct** e têm a mesma causa:
**desacordo de arredondamento em meio-centavo**. Exemplos (bruto → resultado):

| Entrada                | bruto    | `round()` (correta) | modelo esperou |
| ---------------------- | -------- | ------------------: | -------------: |
| 150.5, common          | 142.975  |              142.97 |         142.98 |
| 100.0157…, common      | 95.015   |               95.01 |          95.02 |
| 100.0052…, common      | 95.005   |               95.01 |          95.00 |

O modelo assumiu arredondamento *half-up* (convenção humana), enquanto a
implementação usa `round()` do Python (*half-to-even* sobre o float real). Isso é
em boa parte **subespecificação do requisito** (o modo de arredondamento no
meio-centavo não foi fixado), não erro puro do modelo. A estratégia **two_step
não caiu nessa armadilha** (escolheu valores de fronteira "limpos").
**Ação:** fixar o modo de arredondamento em `req_001.md` (ou usar `Decimal.quantize`).

### QP3 — Detecção de defeitos (bug_detection_rate: two_step 0.71 > direct 0.667)
Cerca de 1/3 dos testes que passam na correta são `weak` (43 de 138 que passam).
Concentram-se em req_002/req_003 — muitos testes redundantes de casos válidos que
não exercitam nenhuma fronteira de defeito. Ainda assim, o suíte completo cobre
todos os bugs (ver mutation_score).

### QP4 — Efetividade por tipo de bug
Como o mutation_score foi 1.0 em tudo, nenhum mutante sobreviveu. Observações da
matriz: bugs de **fronteira** (req_003 12/17/18/60) e o **caso ausente** (req_003
idade negativa, bug_003) só são mortos por testes que exercitam exatamente aquela
fronteira/entrada inválida — são os mais dependentes de boa cobertura. Bugs de
**constante** (taxas em req_001) e de **operador** (req_002 OR-vs-AND, bug_005)
são mortos amplamente, por quase qualquer teste positivo.

### QP5 — Estratégia (two_step vs direct)
- two_step: **correct_pass_rate maior** (1.00 vs 0.945, evitou a armadilha de
  arredondamento) e **bug_detection_rate maior** (0.71 vs 0.667);
- two_step gerou menos testes (69 vs 73) porém mais `useful` (49 vs 46);
- redundância alta em ambas (esperado para funções pequenas).

Indício favorável à hipótese de que o raciocínio intermediário sobre técnicas de
teste produz suítes ligeiramente melhores e mais "comportados".

## 6. Limitações observadas

- **N pequeno:** 3 requisitos, 5 bugs cada — tendência amostral; ampliar antes de
  generalizar.
- **Viés de autoria dos bugs:** mutantes simples; mutation_score 1.0 sugere que os
  defeitos podem estar fáceis demais. Próximo passo: bugs mais sutis.
- **Subespecificação (arredondamento):** ver QP2; requisito precisa de critério
  de arredondamento explícito.
- **Redundância alta:** o número de testes não reflete diversidade de cobertura.
