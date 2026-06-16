# LLM Requirements → Executable Tests

Projeto experimental que avalia se um LLM consegue **gerar testes unitários
executáveis (`pytest`)** a partir de requisitos escritos em linguagem natural.

A pergunta central é objetiva e verificável por execução:

> O teste gerado **valida a implementação correta** e **detecta implementações
> defeituosas**?

Cada teste gerado é executado contra uma implementação correta e contra várias
implementações com defeitos controlados (estilo *mutation testing*). Um bom teste
passa na implementação correta e falha em pelo menos uma defeituosa.

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
  mutation_run.py        # mutação automática (mutmut) sobre a suíte gerada
  results_matrix.csv     # matriz de execução (gerada)
  metrics_summary.csv    # métricas (gerada)
  mutation_summary.csv   # mutation_score automático por config (gerado)
  mutation_survivors.csv # mutantes sobreviventes, com diff (gerado)
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

### Mutação manual vs automática

Há **dois** `mutation_score`, complementares e **não comparáveis numericamente**
(medem conjuntos de mutantes diferentes):

- **manual** (`metrics.py` → `metrics_summary.csv`): sobre os 5 mutantes manuais
  por requisito (`bug_00N.py`), derivados de uma taxonomia de faltas. Serve à
  análise fina **por tipo de defeito** (QP4), mas satura em 1.0 (poucos mutantes).
- **automático** (`mutation_run.py` → `mutation_summary.csv`, coluna
  `mutation_score_auto`): o [`mutmut`](https://github.com/boxed/mutmut) gera
  dezenas de mutantes sobre `correct.py` e a suíte gerada pelo LLM tenta matá-los.
  Volta a discriminar entre estratégias/requisitos. Os mutantes sobreviventes
  (com diff) vão para `mutation_survivors.csv` — um sobrevivente pode ser
  **mutante equivalente** (não-matável), então exige triagem humana.

Para garantir o **baseline verde** que o `mutmut` exige (a suíte precisa passar
inteira na implementação não-mutada), `mutation_run.py` deseleciona os testes que
reprovam na `correct.py`, lidos de `results_matrix.csv`; uma config sem nenhum
teste verde é marcada `skipped`.

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

Flags de `mutation_run.py`: `--strategy {direct,two_step,all}`, `--limit`,
`--timeout` (s por config), `--matrix`, `--out`, `--survivors-out`. Requer
`results_matrix.csv` (passo 2) para o filtro de baseline verde.

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
