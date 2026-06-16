# Avaliação executável de testes gerados por LLM — justificativa e plano

> Decisão: adotar a abordagem de **avaliação por execução / mutation testing** (branch `dev/readme-projeto-atual`) como linha principal do projeto, no lugar da comparação por similaridade de embeddings.

---

## Parte 1 — Justificativa

### 1.1 O problema da abordagem anterior (embeddings)

A primeira abordagem gerava um teste a partir do *overview* de cada caso humano e media a similaridade do cosseno com a descrição daquele mesmo caso. Três defeitos a tornavam inconclusiva:

1. **Métricas degeneradas.** Como se gerava exatamente um teste por caso humano, `total_gerado = total_humano` com o mesmo numerador de matches; logo precision, recall e F1 colapsavam no mesmo número — não mediam coisas distintas.
2. **Oráculo subjetivo.** "Match" dependia de um limiar de cosseno arbitrário (0,80) sobre um espaço em que dois textos quaisquer de teste no mesmo formato já têm similaridade alta (piso observado ~0,75). O sinal não distinguia acerto de coincidência de forma.
3. **Viés de condicionamento.** O teste era gerado a partir do gabarito humano (mais um exemplo few-shot do mesmo conjunto), inflando a similaridade. Daí os resultados terem saído "todos positivos" — fato reconhecido no próprio histórico como *biased*.

### 1.2 Por que a abordagem executável resolve

A pergunta deixa de ser "os textos se parecem?" e passa a ser **"o teste mata o bug?"** — binária, reproduzível e independente de limiar. Cada teste gerado é executado contra uma implementação correta e contra mutantes com defeito controlado; um teste é *útil* se passa na correta e falha em ≥1 mutante.

Ganhos concretos:

- **Oráculo objetivo e reproduzível.** O veredito vem da execução (`pytest` + `junitxml`), não de julgamento humano nem de threshold. Re-rodar dá o mesmo resultado (temperatura 0.0 + cache em disco).
- **Métricas não-degeneradas.** `valid_rate`, `correct_pass_rate`, `bug_detection_rate`, `mutation_score` e redundância medem dimensões diferentes e independentes. Redundância, impossível de medir antes, agora é observável.
- **Mais próximo de TDD.** O artefato gerado é um teste *executável* que poderia guiar a implementação — que é a essência do TDD. Casos em linguagem natural não chegavam a esse ponto.
- **Subespecificação vira achado.** Quando um teste gerado falha na implementação correta por assumir comportamento não fixado (ex.: case-sensitivity de `customer_type`), isso expõe uma ambiguidade real do requisito — um resultado de pesquisa, não um erro.

### 1.3 O trade de escopo (declarado explicitamente)

Esta direção **estreita o escopo de propósito**: troca documentação de software real e testes de alto nível em linguagem natural por requisitos unitários executáveis (funções pequenas e determinísticas) com oráculo por execução.

Isso é uma escolha consciente de **mensurabilidade objetiva sobre validade ecológica**, e está alinhada com a linha de *mutation testing* que a proposta original já citava como extensão (§11.2). O custo é não exercitar mais os documentos do Firefox; a Fase 6 do plano reintroduz validade externa de forma controlada. Esta mudança de escopo deve ser **confirmada com a orientação** antes do fechamento, por divergir da proposta entregue.

### 1.4 Mapeamento com as questões de pesquisa

| QP | Pergunta | Métrica que responde |
|----|----------|----------------------|
| QP1 | Executabilidade | `valid_rate` |
| QP2 | Correção | `correct_pass_rate` (+ invalids como subespecificação) |
| QP3 | Detecção de defeito | `bug_detection_rate`, `mutation_score` |
| QP4 | Efetividade por tipo de bug | matriz por mutante (taxonomia de faltas) |
| QP5 | Estratégia (two_step vs direct) | comparação normalizada (Fase 4) |

---

## Parte 2 — Plano de implementação

Cada fase é uma unidade de trabalho fechada (no fluxo SDD, uma spec via `/sdd-init`), com critério de pronto explícito. Ordem por valor: as Fases 2 e 3 são as que mais fortalecem as conclusões.

### Estado atual (ponto de partida)

- 3 requisitos (`req_001` desconto, `req_002` senha, `req_003` faixa etária).
- 5 mutantes manuais por requisito (15 no total).
- 2 estratégias (`direct`, `two_step`); `gemini-2.5-flash`, temperatura 0.0.
- Harness `generate_tests.py → run_tests.py → metrics.py` funcionando e reproduzível.
- **Problema central a atacar:** `mutation_score = 1.0` em todas as configs (efeito teto — não discrimina); redundância muito maior no `two_step` (39 vs 17), sugerindo que parte da vantagem dele é volume, não qualidade.

---

### Fase 0 — Decisão de escopo e alinhamento 

- [x] Escrever 1 parágrafo de *reframing* da proposta (usar 1.3 acima).
- [x] Confirmar a mudança de escopo com a orientação (executável vs. docs reais).
- [ ] Registrar a decisão em `STATE.md` para memória entre sessões.

**Pronto quando:** a mudança de escopo está documentada e validada com a orientação.

---

### Fase 1 — Consolidar a base

- [ ] Promover `dev/readme-projeto-atual` para a linha principal (merge/PR); remover em definitivo o pipeline de embeddings do caminho principal.
- [ ] **Reescrever o `CLAUDE.md`** para esta arquitetura (requisitos-como-função, mutantes, harness `generate/run/metrics`) — o atual descreve o pipeline removido.
- [ ] Garantir que `environment.yml`/`requirements.txt` instalam tudo num ambiente limpo; documentar o caminho sem Conda.

**Pronto quando:** clone limpo → instala → roda os 3 passos e reproduz `metrics_summary.csv`.

---

### Fase 2 — Quebrar o teto de `mutation_score`

Hoje o score satura em 1.0 com 5 mutantes manuais fáceis. Introduzir **mutação automática** para (a) gerar dezenas de mutantes por requisito, (b) remover o viés de autoria e (c) fazer o score voltar a discriminar.

- [ ] Adicionar `mutmut` (ou `cosmic-ray`) às dependências.
- [ ] Criar `evaluation/mutation_run.py`: para cada `(requisito, estratégia)`, usar a suíte gerada pelo LLM como conjunto de testes e rodar a ferramenta sobre `correct.py`, coletando mutantes mortos/sobreviventes.
- [ ] Manter os mutantes manuais para a **matriz fina por tipo de falta** (QP4); usar os mutantes automáticos para o **`mutation_score` discriminante** (QP3/QP5). Reportar os dois lado a lado.
- [ ] Registrar mutantes sobreviventes (que nenhum teste matou) — sinal direto de lacuna de cobertura dos testes gerados.

**Pronto quando:** `mutation_score` varia entre estratégias/requisitos (não é mais 1.0 em tudo) e há lista de mutantes sobreviventes por config.

---

### Fase 3 — Escalar o número de requisitos

De 3 para **10–15** requisitos (alvo do desenho experimental original: 10–20).
Barato, pois a receita já está documentada no README.

- [ ] Definir 7–12 novos `requirements/req_XXX.md` cobrindo classes variadas (numérico/fronteira, string/validação, estado simples, regras de negócio, datas, coleções).
- [ ] Para cada um: `correct.py` + mutantes manuais (1 defeito por arquivo, taxonomia de faltas) — os automáticos saem da Fase 2.
- [ ] Gerar testes (`--sleep` para respeitar o free tier; o cache evita regeneração ao retomar).

**Pronto quando:** ≥10 requisitos no pipeline com matriz e métricas regeneradas.

---

### Fase 4 — Comparação justa entre estratégias

`two_step` parece melhor (bug_detection 0,70 vs 0,56), mas tem ~2× mais redundância: parte do ganho é volume. Normalizar para isolar qualidade.

- [ ] Calcular a **suíte mínima** por estratégia (set cover guloso: menor subconjunto de testes que mata o mesmo conjunto de mutantes) e comparar o tamanho.
- [ ] Reportar **kills únicos por teste** e **nº de testes para atingir X% de kill** (curva de cobertura por nº de testes).
- [ ] Incluir essas colunas no `metrics_summary.csv` e no relatório.

**Pronto quando:** a comparação `direct × two_step` é reportada controlando por volume de testes, não só em contagem bruta.

---

### Fase 5 — Variância e robustez

Hoje: 1 modelo, 1 temperatura, 1 execução. Sem isso, a QP5 não tem barra de erro.

- [ ] Rodar a geração com `k` sementes/temperaturas (ex.: temp 0.4, k=3–5) e reportar média ± desvio das métricas principais.
- [ ] Rodar ao menos um **segundo modelo** (`--model gemini-2.5-flash-lite`, ou outro provedor) para checar se a vantagem do `two_step` se mantém.

**Pronto quando:** as métricas principais vêm com dispersão, e a conclusão da QP5 é qualificada como estável ou dependente de modelo.

---

### Fase 6 — Validade externa

- [ ] Adicionar 1–2 requisitos derivados de um documento real (ou da documentação do Firefox antes usada), mantendo a interface por assinatura.
- [ ] Reportar se as taxas se mantêm fora das funções-brinquedo.

**Pronto quando:** há ao menos um requisito de origem realista no conjunto, com métricas comparadas às sintéticas.

---

### Fase 7 — Análise final, relatório e apresentação

- [ ] Atualizar `reports/experiment_report.md` com os dados das Fases 2–5.
- [ ] Análise qualitativa: catalogar invalids como subespecificações e os mutantes sobreviventes como lacunas de cobertura.
- [ ] Discussão de uso em TDD e das limitações (viés de mutante, N, escopo).
- [ ] Montar a apresentação.

**Pronto quando:** relatório reproduzível a partir dos CSVs e apresentação prontos.

---

## Cronograma sugerido (continuidade com a proposta original)

| Semana | Fases | Entrega |
|--------|-------|---------|
| 1 | 0, 1 | Escopo alinhado; base consolidada; `CLAUDE.md` reescrito |
| 2 | 2 | Mutação automática; `mutation_score` discriminante |
| 3 | 3 | 10–15 requisitos no pipeline |
| 4 | 4, 5 | Comparação normalizada + variância/segundo modelo |
| 5 | 6 (opc.), 7 | Validade externa; relatório e apresentação |

## Riscos e mitigação

| Risco | Mitigação |
|-------|-----------|
| Free tier estoura ao escalar N | cache em disco + `--sleep` + `--limit`; modelo `flash-lite` |
| Mutação automática gera mutantes equivalentes (não-matáveis) | inspecionar sobreviventes; reportar score bruto e ajustado |
| Vantagem do `two_step` é só volume | normalização da Fase 4 (suíte mínima) |
| Mudança de escopo rejeitada pela orientação | Fase 0 é bloqueante e vem antes de qualquer código |
| N ainda pequeno para conclusão forte | enquadrar como estudo exploratório/piloto |