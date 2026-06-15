# LLM Requirements → Executable Tests

Projeto experimental para avaliar se um LLM consegue **gerar testes unitários
executáveis (`pytest`)** a partir de requisitos em linguagem natural.

A qualidade do teste **não** é medida por similaridade textual com testes
humanos. É medida por **execução**: um bom teste passa na implementação correta
e falha em pelo menos uma implementação defeituosa (estilo *mutation testing*).

> A abordagem anterior (similaridade por embeddings) foi descontinuada em favor
> desta avaliação executável.

## Fluxo

```text
Requisito em linguagem natural
        ↓  (generate_tests.py)
LLM gera testes pytest
        ↓  (run_tests.py)
Testes executam contra implementação correta + implementações com bugs
        ↓  (metrics.py)
Métricas objetivas por execução
```

## Estrutura do repositório

```text
requirements/            # requisitos em linguagem natural (req_XXX.md)
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
  metrics.py             # calcula as métricas
  results_matrix.csv     # matriz de execução (gerada)
  metrics_summary.csv    # métricas (gerada)
reports/                 # relatório do experimento
```

Cada `req_XXX.md` declara a **assinatura da função** e o **módulo a importar**
(`solution`). Todas as implementações de um requisito compartilham a mesma
assinatura; o runner monta a variante escolhida como `solution.py` num diretório
isolado, e o teste sempre faz `from solution import ...`.

## Classificação dos testes

| Classificação    | Significado                                                              |
| ---------------- | ------------------------------------------------------------------------ |
| `useful`         | passa na correta e falha em ≥1 defeituosa                                 |
| `weak`           | passa na correta mas não detecta nenhum defeito                          |
| `invalid`        | falha na implementação correta                                           |
| `not_executable` | não executa (erro de sintaxe/import/coleta)                              |

## Métricas

```text
valid_rate         = testes executáveis / testes gerados
correct_pass_rate  = testes que passam na correta / testes executáveis
bug_detection_rate = testes úteis / testes que passam na correta
mutation_score     = mutantes mortos / total de mutantes (por requisito)
```

Também são reportadas redundância (testes que matam o mesmo conjunto de bugs) e
a quebra por estratégia (direct × two_step → QP5).

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
```

Principais flags de `generate_tests.py`: `--strategy {direct,two_step,all}`,
`--model`, `--temperature`, `--limit`, `--sleep`, `--cache-dir`, `--no-cache`.

## Free tier / quota

O free tier do Gemini impõe limites baixos (ex.: ~20 gerações/dia em
`gemini-2.5-flash`). O pipeline mitiga isso:

- **Cache em disco** (`evaluation/.cache/`): re-rodar com os mesmos parâmetros é
  praticamente gratuito; execuções interrompidas por quota retomam de onde pararam.
- **`--sleep N`**: pausa entre chamadas (respeita o limite por minuto).
- **`--limit N`**: roda um subconjunto de requisitos.
- Modelo com teto maior: `--model gemini-2.5-flash-lite`.

## Adicionando um novo requisito

1. Crie `requirements/req_XXX.md` com descrição, **assinatura**, módulo `solution`,
   regras, classes de equivalência, valores-limite, entradas inválidas e invariantes.
2. Crie `implementations/req_XXX/correct.py` e `bug_001.py..bug_00N.py`
   (mesma assinatura; **um único defeito** por arquivo; sem erro de sintaxe/import).
3. Rode os três passos acima.

## Limitações conhecidas

- **Viés de autoria dos bugs:** mutantes simples superestimam a capacidade;
  os bugs são derivados de uma taxonomia de faltas, independente dos testes gerados.
- **Escopo:** funções pequenas e determinísticas; não cobre sistemas com estado,
  I/O, UI ou integração externa.
- **Dependência da assinatura:** o requisito padroniza a interface para reduzir isso.
- **N pequeno:** piloto com 3 requisitos; ampliar para conclusões mais fortes.
```
