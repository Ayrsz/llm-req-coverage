# LLM Requirements → Executable Tests

Projeto experimental que avalia se um LLM consegue **gerar testes unitários executáveis (`pytest`)** a partir de requisitos escritos em linguagem natural.

A pergunta central é objetiva e verificável por execução:

> O teste gerado **valida a implementação correta** e **detecta implementações defeituosas**?

Cada teste gerado é executado contra uma implementação correta e contra várias implementações com defeitos controlados (estilo *mutation testing*). Um bom teste passa na implementação correta e falha em pelo menos uma defeituosa.

## Questões de pesquisa

- **QP1 — Executabilidade:** que proporção dos testes gerados é válida e executa?
- **QP2 — Correção:** que proporção passa na implementação correta?
- **QP3 — Detecção:** que proporção detecta pelo menos um defeito?
- **QP4 — Efetividade por bug:** quais tipos de defeito são mais detectados?
- **QP5 — Estratégia:** gerar em duas etapas (identificar técnicas e depois
  escrever os testes) supera a geração direta?

## Fluxo

```text
Requisito em linguagem natural
        ↓  (generate_tests.py)
LLM gera testes pytest
        ↓  (run_tests.py)
Testes executam contra implementação correta + implementações com bugs
        ↓  (metrics.py)
Métricas objetivas por execução
        ↓  (mutation_run.py)
Mutação automática (mutmut) sobre a suíte gerada
```

## Estrutura do repositório

```text
requirements/            # requisitos em linguagem natural (req_XXX.md)
dataset/                 # documentação real (Firefox) que origina req_016/req_017
implementations/
  req_XXX/
    correct.py           # 1 implementação correta
    bug_001.py ...       # N implementações com 1 defeito controlado cada
generated_tests/
  direct/                # estratégia A: requisito → testes
  two_step/              # estratégia B: requisito → técnicas → testes
prompts/                 # templates de prompt (direct / técnicas / pytest)
evaluation/
  llm_client.py          # cliente Gemini (retry, cota, cache em disco)
  generate_tests.py      # gera os testes pytest (2 estratégias)
  run_tests.py           # executa cada teste contra cada implementação
  metrics.py             # calcula as métricas (inclui suíte mínima)
  mutation_run.py        # mutação automática (mutmut) sobre a suíte gerada
  results_matrix.csv     # matriz de execução (gerada)
  metrics_summary.csv    # métricas (gerada)
  mutation_summary.csv   # mutation_score automático por config (gerado)
  mutation_survivors.csv # mutantes sobreviventes, com diff (gerado)
tests/                   # suíte do próprio harness (pytest, offline)
  test_metrics.py
  test_mutation_run.py
  test_requirements_consistency.py
  fixtures/              # saídas reais do mutmut p/ testar o parser, sem chamar a ferramenta
reports/                 # relatório do experimento
```

Cada `req_XXX.md` declara a **assinatura da função** e o **módulo a importar** (`solution`). Todas as implementações de um requisito compartilham a mesma assinatura; o runner monta a variante escolhida como `solution.py` num diretório isolado, e o teste sempre faz `from solution import ...`.

## Requisitos atuais

**17 requisitos no total:** um núcleo de **15 sintéticos** em 6 classes de problema, mais **2 derivados de documentação real** do Firefox para checagem de validade externa.

### Núcleo sintético (15)

| Req | Classe | Tema | Assinatura |
|---|---|---|---|
| `req_001` | regra ramificada | preço final com desconto | `calculate_final_price(value: float, customer_type: str) -> float` |
| `req_002` | string/validação | força de senha | `validate_password(password: str) -> bool` |
| `req_003` | numérico/fronteira | faixa etária | `age_bracket(age: int) -> str` |
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

### Validação externa (2)

Derivados de `dataset/` (documentação do Firefox), mantendo a interface por assinatura e isolando o núcleo determinístico do texto:

| Req | Origem | Tema | Assinatura |
|---|---|---|---|
| `req_016` | `dataset/req_history.txt` (*Places history*) | URLs mais visitadas | `most_visited_urls(visits: list, n: int) -> list` |
| `req_017` | `dataset/req_bookmark.txt` (*Smart Folders / Tagging*) | filtrar favoritos por tag | `filter_by_tag(bookmarks: list, tag: str) -> list` |

## Classificação dos testes

| Classificação    | Significado                                                              |
| ---------------- | ------------------------------------------------------------------------ |
| `useful`         | passa na correta e falha em ≥1 defeituosa                                 |
| `weak`           | passa na correta mas não detecta nenhum defeito                          |
| `invalid`        | falha na implementação correta                                           |
| `not_executable` | não executa (erro de sintaxe/import/coleta)                              |

## Métricas

Colunas de `metrics_summary.csv`:

```text
valid_rate          = testes executáveis / testes gerados
correct_pass_rate   = testes que passam na correta / testes executáveis
bug_detection_rate  = testes úteis / testes que passam na correta
mutation_score      = mutantes (manuais) mortos / total, por requisito
redundant_tests     = testes úteis além da suíte mínima
min_suite_size      = menor subconjunto que mata o mesmo conjunto de mutantes (set cover guloso)
essential_tests     = testes que matam sozinhos algum mutante (kills únicos)
kills_per_test_mean = média de mutantes mortos por teste útil
```

`min_suite_size`, `essential_tests` e `kills_per_test_mean` permitem comparar as estratégias **controlando o volume** de testes (QP5), evitando que a estratégia que apenas gera mais testes pareça melhor.

### Mutação manual vs automática

Há **dois** `mutation_score`, complementares e **não comparáveis numericamente** (medem conjuntos de mutantes diferentes):

- **manual** (`metrics.py` → `metrics_summary.csv`): sobre os 5 mutantes manuais por requisito (`bug_00N.py`), derivados de uma taxonomia de faltas. Serve à análise fina **por tipo de defeito** (QP4), mas satura em 1.0 (poucos mutantes).
- **automático** (`mutation_run.py` → `mutation_summary.csv`, coluna `mutation_score_auto`): o [`mutmut`](https://github.com/boxed/mutmut) gera dezenas de mutantes sobre `correct.py` e a suíte gerada pelo LLM tenta matá-los. Volta a discriminar entre estratégias/requisitos. Os mutantes sobreviventes (com diff) vão para `mutation_survivors.csv` — um sobrevivente pode ser **mutante equivalente** (não-matável), então exige triagem humana.

Para garantir o **baseline verde** que o `mutmut` exige (a suíte precisa passar inteira na implementação não-mutada), `mutation_run.py` deseleciona os testes que reprovam na `correct.py`, lidos de `results_matrix.csv`; uma config sem nenhum teste verde é marcada `skipped`.

## Setup

```bash
conda env create -f environment.yml
conda activate llm-req-coverage
# ou: pip install -r requirements.txt
```

Defina a chave do Gemini em um arquivo `.env` na raiz (carregado automaticamente):

```text
GEMINI_API_KEY=sua-chave
```

(Chave obtida em https://aistudio.google.com/apikey. Aceita também `GEMINI_TOKEN`.)

## Como executar

```bash
# 1) Gerar os testes (ambas as estratégias). --limit/--sleep ajudam no free tier.
python evaluation/generate_tests.py --sleep 7

# smoke test rápido (1 requisito):
python evaluation/generate_tests.py --limit 1

# 2) Executar os testes contra todas as implementações e montar a matriz.
python evaluation/run_tests.py

# 3) Calcular as métricas.
python evaluation/metrics.py

# 4) Mutação automática (mutmut) sobre a suíte gerada.
#    Não chama o LLM; usa results_matrix.csv para o baseline verde.
python evaluation/mutation_run.py
```

Flags de `mutation_run.py`: `--strategy {direct,two_step,all}`, `--limit`, `--timeout` (s por config), `--matrix`, `--out`, `--survivors-out`. Requer `results_matrix.csv` (passo 2) para o filtro de baseline verde.

Principais flags de `generate_tests.py`: `--strategy {direct,two_step,all}`, `--model`, `--temperature`, `--limit`, `--sleep`, `--cache-dir`, `--no-cache`.

> **Nota de reprodução:** a coleta usou `gemini-2.5-flash-lite` a temperatura 0,0 (determinística).

## Testes do harness

A suíte em `tests/` valida o próprio arcabouço (parser do `mutmut`, cálculo de métricas, consistência dos requisitos), **sem** chamar o LLM nem o `mutmut` reais — usa fixtures em `tests/fixtures/` com saídas reais capturadas da ferramenta:

```bash
python -m pytest
```

## Free tier / quota

O free tier do Gemini impõe limites baixos (ex.: ~20 gerações/dia em `gemini-2.5-flash-lite`). O pipeline mitiga isso:

- **Cache em disco** (`evaluation/.cache/`): re-rodar com os mesmos parâmetros é praticamente gratuito; execuções interrompidas por quota retomam de onde pararam.
- **`--sleep N`**: pausa entre chamadas (respeita o limite por minuto).
- **`--limit N`**: roda um subconjunto de requisitos.
- Modelo com teto maior: `--model gemini-2.5-flash-lite`.

## Adicionando um novo requisito

1. Crie `requirements/req_XXX.md` com descrição, **assinatura**, módulo `solution`, regras, classes de equivalência, valores-limite, entradas inválidas e invariantes.
2. Crie `implementations/req_XXX/correct.py` e `bug_001.py..bug_00N.py` (mesma assinatura; **um único defeito** por arquivo; sem erro de sintaxe/import).
3. Rode os quatro passos acima.

## Limitações conhecidas

- **Viés de autoria dos bugs:** mutantes simples superestimam a capacidade; os bugs são derivados de uma taxonomia de faltas, independente dos testes gerados.
- **Escopo:** funções pequenas e determinísticas; não cobre sistemas com estado, I/O, UI ou integração externa.
- **Dependência da assinatura:** o requisito padroniza a interface para reduzir isso.
- **N moderado:** 15 requisitos sintéticos + 2 de origem real; um modelo, uma execução. Ampliar a amostra e estimar variância (múltiplas sementes/modelos) fortaleceria as conclusões.
