---
description: Quebra o plano técnico em tarefas atômicas (Spec-Driven Development)
argument-hint: [caminho_do_plan]
---
Siga a metodologia Spec-Driven Development.

Leia o plano em `$ARGUMENTS` e quebre-o em tarefas atômicas, sequenciais e
(quando possível) paralelizáveis, no arquivo `docs/specs/<nome>-tasks.md`,
preenchido com checkboxes `[ ]`.

Cada tarefa deve conter:
- **O que fazer** — ação concreta.
- **Onde fazer** — arquivo/módulo.
- **Pré-requisitos** — tarefas das quais depende.
- **Como validar** — teste ou verificação que comprova a conclusão.

Regras de ouro: tarefas pequenas e independentes para não perder contexto; não
implemente código nesta etapa. Ao final, mostre o caminho do arquivo e pare.
