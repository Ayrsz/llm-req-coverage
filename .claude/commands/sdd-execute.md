---
description: Implementa incrementalmente guiado pelo arquivo de tarefas (Spec-Driven Development)
argument-hint: [caminho_das_tasks]
---
Siga a metodologia Spec-Driven Development.

Implemente as tarefas listadas em `$ARGUMENTS`, estritamente guiado por elas.

Diretrizes de execução:
1. Use subagentes isolados (`context: fork`) para tarefas paralelas.
2. Para cada tarefa, nesta ordem: escreva o teste -> escreva o código ->
   rode o linter/testes -> marque a tarefa como feita `[x]`.
3. Atualize o arquivo `STATE.md` na raiz para persistir decisões e manter a
   memória entre sessões.

Regras de ouro: nunca implemente sem ler a spec correspondente; recuse tarefas
sem critério de aceite e teste claros; resolva uma tarefa por vez e faça commits
granulares no Git.
