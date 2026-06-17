# Relatório do Experimento — Avaliação Executável de Testes Gerados por LLM

> Gerado a partir de `evaluation/results_matrix.csv`, `metrics_summary.csv`,
> `mutation_summary.csv` e `mutation_survivors.csv`.
> Para reproduzir: `generate_tests.py` → `run_tests.py` → `metrics.py` →
> `mutation_run.py` (este último só roda em Linux/WSL; ver nota em §3).

## 1. Configuração do experimento

- **Modelo gerador:** gemini-2.5-flash
- **Temperatura:** 0.0 (determinística) — exceção: `direct/req_012` regerado a
  0.4 (a temp 0 o modelo entrou em loop degenerado, saída inutilizável).
- **Data da execução:** 2026-06-16 (Fase 3 — escala de 3 → 15 requisitos)
- **Requisitos:** 15, cobrindo 6 classes (numérico/fronteira, string/validação,
  string/transformação, data/tempo, coleção/agregação, regra ramificada, estado
  simples) — ver tabela em `README.md`.
- **Bugs manuais por requisito:** 5 (75 mutantes manuais no total), derivados de
  uma taxonomia de faltas fixa (fronteira, operador, ramo, constante, guarda).
- **Estratégias:** direct, two_step
- **Testes gerados (funções):** 1014 (direct 581, two_step 433)

## 2. Métricas agregadas (linhas `ALL`)

| Estratégia | valid_rate | correct_pass_rate | bug_detection_rate | mutation_score (manual) | redundância |
| ---------- | ---------: | ----------------: | -----------------: | ----------------------: | ----------: |
| direct     |       1.00 |            0.9914 |             0.7309 |                  0.9733 |         389 |
| two_step   |       1.00 |            0.9746 |             0.7275 |                  0.9600 |         272 |

## 3. Mutação automática (`mutmut`)

Sinal **complementar** ao `mutation_score` manual e **não comparável
numericamente** com ele (mede mutantes diferentes: dezenas gerados pelo `mutmut`
sobre `correct.py`, não os 5 manuais). Roda só em Linux/WSL — o `mutmut` 3.6.0
recusa Windows nativo (`platform.system()=="Windows"` → `sys.exit(1)` no import).
30 configs avaliadas (15 reqs × 2 estratégias), **todas `ok`**, sem `skip`.

| Estratégia | mutantes | mortos | sobreviventes | timeout | score_auto (micro) | score_auto (macro) | mínimo |
| ---------- | -------: | -----: | ------------: | ------: | -----------------: | -----------------: | -----: |
| direct     |      372 |    346 |            24 |       2 |             0.9301 |             0.9444 | 0.7059 |
| two_step   |      372 |    341 |            29 |       2 |             0.9167 |             0.9332 | 0.7059 |

**57 mutantes não-mortos** (sobreviventes + timeouts) ficam em
`mutation_survivors.csv` com o diff, para triagem humana — um sobrevivente pode
ser **mutante equivalente** (não-matável), não necessariamente lacuna de teste.
Concentram-se nos requisitos maiores: req_012 (16), req_005 (10), req_011 (10),
req_007 (9), req_013 (4), req_001 (4), req_006 (2), req_008 (2).

## 4. Mutation score por requisito (manual × automático)

| Requisito | Classe | manual (direct/two_step) | auto (direct/two_step) |
| --------- | ------ | -----------------------: | ---------------------: |
| req_001 | regra ramificada     | 1.00 / 1.00 | 0.96 / 0.88 |
| req_002 | string/validação     | 1.00 / 1.00 | 1.00 / 1.00 |
| req_003 | numérico/fronteira   | 1.00 / 1.00 | 1.00 / 1.00 |
| req_004 | numérico/fronteira   | 1.00 / 1.00 | 1.00 / 1.00 |
| req_005 | numérico/fronteira   | 1.00 / 1.00 | 0.85 / 0.85 |
| req_006 | string/validação     | 1.00 / 1.00 | 0.96 / 0.96 |
| req_007 | string/transformação | 1.00 / 1.00 | 0.92 / 0.90 |
| req_008 | data/tempo           | 1.00 / 0.80 | 0.94 / 0.94 |
| req_009 | data/tempo           | 1.00 / 1.00 | 1.00 / 1.00 |
| req_010 | coleção/agregação    | 1.00 / 1.00 | 1.00 / 1.00 |
| req_011 | coleção/agregação    | 0.80 / 0.80 | 0.71 / 0.71 |
| req_012 | regra ramificada     | 0.80 / 0.80 | 0.86 / 0.86 |
| req_013 | regra ramificada     | 1.00 / 0.89 | 0.96 / 0.89 |
| req_014 | estado simples       | 1.00 / 1.00 | 1.00 / 1.00 |
| req_015 | estado simples       | 1.00 / 1.00 | 1.00 / 1.00 |

O score **manual** ainda satura em 1.0 na maioria (poucos mutantes), mas já
**não satura em tudo**: req_011 e req_012 caem a 0.80 nas duas estratégias (um
mutante manual sobrevive). O score **automático** discrimina muito mais
(0.71–1.0), revelando os reqs maiores como os mais exigentes — exatamente a
hipótese que motivou a Fase 3.

## 5. Distribuição das classificações (1014 testes)

| Classificação    | Total | direct | two_step |
| ---------------- | ----: | -----: | -------: |
| `useful`         |   728 |    421 |      307 |
| `weak`           |   270 |    155 |      115 |
| `invalid`        |    16 |      5 |       11 |
| `not_executable` |     0 |      0 |        0 |

## 6. Análise das Questões de Pesquisa

### QP1 — Executabilidade (valid_rate = 1.00)
Todos os 1014 testes gerados foram válidos e executáveis (nenhum
`not_executable`), em escala 9× maior que o piloto. O modelo respeitou a
instrução de importar de `solution` com a assinatura correta em todos os 15
requisitos.

### QP2 — Correção (correct_pass_rate: direct 0.991, two_step 0.975)
16 testes `invalid` (5 direct, 11 two_step) — falham na implementação correta.
São, em sua maioria, **subespecificação** (o teste assume comportamento não
fixado pelo requisito), não erro de lógica do modelo. Padrões observados:
arredondamento em meio-centavo (`income_tax`, `final_balance`), normalização
Unicode/decomposição em `slugify`, datas extremas em `days_between`,
arredondamento *half-to-even* em `average_above`, e case-sensitivity em
`calculate_final_price`. two_step gera mais desses casos-limite ambíguos — daí
ter mais `invalid` (11 vs 5).

### QP3 — Detecção de defeitos (bug_detection_rate: direct 0.73 ≈ two_step 0.73)
Em escala, as duas estratégias **empatam** no `bug_detection_rate` (~0.73),
contrastando com o piloto (onde two_step 0.70 > direct 0.56). O ganho relativo
do raciocínio intermediário não se sustentou ao ampliar o conjunto.

### QP4 — Efetividade por tipo de bug
A mutação **automática** dá o quadro mais fino: os mutantes que sobrevivem
concentram-se em desigualdades de fronteira/desempate (ex.: `most_frequent`,
req_011 = 0.71), faixas progressivas (`income_tax`, req_012 = 0.86) e
classificação numérica densa (`triangle_type`, req_005 = 0.85). Parte dos
sobreviventes é provavelmente **equivalente** (ex.: `< 0` → `<= 0` quando o caso
de igualdade já é coberto por outra rota) e exige triagem manual — daí a coluna
`diff` em `mutation_survivors.csv`. Bugs de **constante** e **operador** em
funções simples morrem amplamente (score 1.0 em req_002/003/004/009/010/014/015).

### QP5 — Estratégia (two_step vs direct)
- `bug_detection_rate` praticamente igual (0.7309 vs 0.7275);
- score automático agregado levemente **a favor de direct** (macro 0.9444 vs
  0.9332; micro 0.9301 vs 0.9167);
- two_step gera mais testes ao todo? Não: direct gerou mais (581 vs 433), porém
  com redundância maior (389 vs 272);
- two_step expõe mais ambiguidade (11 `invalid` vs 5).

Conclusão honesta: no conjunto ampliado **não há vantagem clara do two_step**; o
sinal favorável do piloto era de N pequeno. As estratégias se equivalem em poder
de detecção, com perfis diferentes (direct mais redundante e robusto a
ambiguidade; two_step mais explorador de casos-limite).

## 7. Limitações observadas

- **Viés de autoria dos bugs manuais:** o `mutation_score` manual ainda satura
  em ~1.0 na maioria dos reqs; a mutação automática mitiga ao gerar mutantes mais
  variados, mas exige triagem de equivalentes.
- **Escopo estreito:** funções pequenas e determinísticas; não cobre estado real,
  I/O, UI ou integração externa (decisão consciente: mensurabilidade > validade
  ecológica).
- **Subespecificação:** o harness revela requisitos ambíguos (16 `invalid`);
  fechá-los nos `.md` é trabalho de curadoria pendente.
- **Redundância alta:** o número de testes não reflete diversidade de cobertura
  (389/272 redundantes).
- **Sobreviventes não triados:** os 57 mutantes não-mortos precisam de revisão
  humana (equivalente vs. lacuna) antes de virar conclusão sobre cobertura.
