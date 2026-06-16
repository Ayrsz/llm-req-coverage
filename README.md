# LLM Requirements → Test Cases

Geração e avaliação de **casos de teste de alto nível a partir de documentação de
software** usando LLMs (Gemini), com foco em apoiar práticas de **TDD**.

O projeto transforma documentos de requisitos em casos de teste e os avalia
contra um *benchmark* humano usando **similaridade semântica**, comparando duas
estratégias de *prompting*.

---

## Visão geral

```
Documento de requisitos
        │
        ▼
   LLM gera o caso de teste  ──►  Estratégia A: geração direta
        │                         Estratégia B: técnicas de teste → geração guiada
        ▼
 Caso gerado + caso humano  ──►  embeddings  ──►  similaridade do cosseno
        │
        ▼
 Classificação (MATCH / REVIEW / NO_MATCH)  ──►  Precision · Recall · F1
```

### Domínios

Funcionalidades do Firefox, extraídas da documentação pública da Mozilla:

- **Bookmark** — favoritos
- **History** — histórico de navegação
- **Password** — gerenciador de senhas

### Estratégias comparadas

| Estratégia | Descrição |
|---|---|
| **A — Direta** | requisito + overview → LLM gera o teste |
| **B — Duas etapas** | LLM identifica as técnicas de teste aplicáveis → gera o teste guiado por elas |

### Classificação por similaridade

| Status | Faixa | Significado |
|---|---|---|
| `MATCH` | ≥ 0.80 | match automático com o teste humano |
| `REVIEW` | 0.65 – 0.79 | requer revisão manual |
| `NO_MATCH` | < 0.65 | não cobre o teste humano |

---

## Estrutura do repositório

```
.
├── dataset/              # documentos de requisitos (entrada)
│   ├── req_bookmark.txt
│   ├── req_history.txt
│   └── req_password.txt
├── human_tests/          # benchmark humano (ground truth)
│   ├── req_tests_bookmark.csv
│   ├── req_tests_history.csv
│   └── req_tests_password.csv
├── testgen/              # pacote Python (uma responsabilidade por módulo)
│   ├── config.py         # caminhos, modelos, thresholds, domínios, API key
│   ├── data_loader.py    # carrega requisito + ground truth
│   ├── prompts.py        # construtores de prompt (funções puras)
│   ├── llm_client.py     # LLMClient (interface) + GeminiClient
│   ├── strategies.py     # DirectStrategy (A) e TwoStepStrategy (B)
│   ├── evaluation.py     # similaridade, classificação, métricas
│   ├── pipeline.py       # ExperimentRunner (geração + avaliação)
│   ├── reporting.py      # salvar CSV, imprimir métricas
│   └── main.py           # CLI
├── tests/                # suíte pytest (usa FakeClient, sem API)
├── prompts/              # notebook original (Colab)
├── output/               # CSVs gerados (gitignored)
├── requirements.txt
└── .env.example
```

O LLM fica atrás da interface `LLMClient` e é **injetado** no `ExperimentRunner`,
o que permite testar todo o pipeline com um cliente fake — sem chamadas de API.

---

## Instalação

```bash
pip install -r requirements.txt
```

### Chave da API

Obtenha uma chave em <https://aistudio.google.com/apikey>, copie `.env.example`
para `.env` e preencha a chave (o `.env` é ignorado pelo git):

```bash
cp .env.example .env
# edite .env: GEMINI_API_KEY=sua-chave
```

Alternativamente, exporte como variável de ambiente:

```bash
export GEMINI_API_KEY="sua-chave"
```

---

## Uso

```bash
# Todos os domínios, estratégias A e B
python -m testgen.main

# Apenas um domínio
python -m testgen.main --domains BOOKMARK

# Apenas a geração direta
python -m testgen.main --strategies A

# Combinações
python -m testgen.main --domains BOOKMARK HISTORY --strategies A B
```

Os resultados são salvos em:

- `output/direct_prompt/<DOMINIO>_tests.csv` (Estratégia A)
- `output/two_step_prompt/<DOMINIO>_tests.csv` (Estratégia B)

Cada CSV contém, por caso: similaridade, status, técnicas (estratégia B), os
textos humano e gerado, e colunas qualitativas em branco para revisão manual
(clareza, executabilidade, rastreabilidade, correção, redundância, alucinação,
utilidade para TDD).

---

## Testes

A suíte usa um `FakeClient` determinístico — **não consome cota de API**:

```bash
python -m pytest
```

Cobre: similaridade do cosseno, thresholds de classificação, cálculo de
precision/recall/F1, encadeamento técnica→geração da Estratégia B, colunas do
CSV e o carregamento dos dados reais.

---

## Métricas

- **Precision** = matches / total de testes gerados pelo LLM
- **Recall** = matches / total de testes humanos (cobertura do benchmark)
- **F1** = média harmônica de precision e recall
