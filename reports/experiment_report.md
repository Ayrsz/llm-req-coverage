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
- **Testes gerados (funções):** 115 (direct 50, two_step 65)
- **Nota:** req_001 usa arredondamento *half-up* determinístico (`Decimal.quantize`),
  fixado no requisito após a primeira rodada.

## 2. Métricas agregadas (linhas `ALL`)

| Estratégia | valid_rate | correct_pass_rate | bug_detection_rate | mutation_score | redundância |
| ---------- | ---------: | ----------------: | -----------------: | -------------: | ----------: |
| direct     |       1.00 |            1.0000 |             0.5600 |           1.00 |          17 |
| two_step   |       1.00 |            0.9846 |             0.7031 |           1.00 |          39 |

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
requisito (mutation_score = 1.0).

## 4. Distribuição das classificações (115 testes)

| Classificação    | Total |
| ---------------- | ----: |
| `useful`         |    73 |
| `weak`           |    41 |
| `invalid`        |     1 |
| `not_executable` |     0 |

## 5. Análise das Questões de Pesquisa

### QP1 — Executabilidade (valid_rate = 1.00)
Todos os 115 testes gerados foram válidos e executáveis (nenhum `not_executable`).
O modelo respeitou a instrução de importar de `solution` com a assinatura correta.

### QP2 — Correção (correct_pass_rate: direct 1.00, two_step 0.985)
Sobrou **1 teste `invalid`**, em **req_001 / two_step**: o teste assumiu que
`customer_type` é **case-insensitive** (esperou que `"PREMIUM"` recebesse o
desconto premium), mas o requisito reconhece apenas `"premium"` exato e trata o
resto como `common`. É **subespecificação** (a sensibilidade a maiúsculas não está
fixada), não erro de lógica do modelo.

> A rodada anterior tinha **4 invalids**, todos por ambiguidade de arredondamento
> em meio-centavo. Foram **eliminados** ao fixar arredondamento *half-up* no
> requisito e usar `Decimal.quantize(ROUND_HALF_UP)` na implementação. Resta a
> ambiguidade de case-sensitivity acima — mesma classe de problema, candidata ao
> mesmo tratamento (fixar no requisito).

### QP3 — Detecção de defeitos (bug_detection_rate: two_step 0.70 > direct 0.56)
two_step gera mais testes `useful`. Boa parte dos `weak` (41) está em
req_002/req_003 — muitos testes de casos válidos que não exercitam fronteira de
defeito. Ainda assim, o suíte completo cobre todos os bugs (ver mutation_score).

### QP4 — Efetividade por tipo de bug
mutation_score 1.0 em tudo: nenhum mutante sobreviveu. Da matriz: bugs de
**fronteira** (req_003 12/17/18/60) e o **caso ausente** (req_003 idade negativa,
bug_003) só morrem com testes que exercitam exatamente aquela fronteira/entrada
inválida — os mais dependentes de boa cobertura. Bugs de **constante** (taxas em
req_001) e de **operador** (req_002 OR-vs-AND) morrem amplamente.

### QP5 — Estratégia (two_step vs direct)
- two_step tem **bug_detection_rate maior** (0.70 vs 0.56) e mais testes `useful`
  (45 vs 28);
- direct teve **0 invalid** nesta rodada; two_step teve 1 (a ambiguidade de
  case-sensitivity);
- redundância alta em ambas (esperado para funções pequenas).

Indício favorável à hipótese de que o raciocínio intermediário sobre técnicas de
teste produz suítes com maior poder de detecção.

## 6. Limitações observadas

- **N pequeno:** 3 requisitos, 5 bugs cada — ampliar antes de generalizar.
- **Viés de autoria dos bugs:** mutation_score 1.0 sugere que os defeitos podem
  estar fáceis demais; próximo passo são bugs mais sutis.
- **Subespecificação:** o harness é bom para revelar requisitos ambíguos
  (arredondamento — já corrigido; case-sensitivity de `customer_type` — pendente).
- **Redundância alta:** o número de testes não reflete diversidade de cobertura.
