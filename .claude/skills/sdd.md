# Spec-Driven Development (SDD) Skill

Esta habilidade força o Claude a seguir a metodologia de Desenvolvimento Guiado por Especificações, garantindo economia de tokens, consistência e código correto na primeira tentativa.

## Comandos Disponíveis

### `/sdd-init [descricao]`
Gera a especificação inicial de uma funcionalidade com base em um prompt livre ou PRD.
- **Ação:** Cria o arquivo em `docs/specs/[nome-da-feature].md`.
- **Conteúdo Obrigatório:** Problema, Escopo, Fora de Escopo, Histórias de Usuário e Critérios de Aceite explícitos.

### `/sdd-plan [caminho_da_spec]`
Lê uma especificação existente e monta o plano de engenharia de software antes do código.
- **Ação:** Analisa o codebase e gera o arquivo `docs/specs/[nome]-plan.md`.
- **Conteúdo Obrigatório:** Arquitetura afetada, mudanças no banco/APIs, impactos colaterais e definição de "Pronto" (Definition of Done).

### `/sdd-tasks [caminho_do_plan]`
Quebra o plano técnico em tarefas atômicas, sequenciais e paralelizáveis para evitar perda de contexto.
- **Ação:** Cria o arquivo `docs/specs/[nome]-tasks.md` preenchido com checkboxes `[ ]`.
- **Regra:** Cada tarefa deve conter: O que fazer, Onde fazer, Pré-requisitos e Como validar.

### `/sdd-execute [caminho_das_tasks]`
Inicia a implementação incremental guiada estritamente pelo arquivo de tarefas.
- **Diretriz de Execução:**
  1. Use subagentes isolados (`context: fork`) para processar tarefas paralelas.
  2. Para cada tarefa: Escreva o teste ➔ Escreva o código ➔ Rode o linter/testes ➔ Marque como feito `[x]`.
  3. Atualize o arquivo `STATE.md` na raiz para persistir decisões e manter a memória entre sessões do Claude Code.

## Regras de Ouro (Constituição do Agente)
- NUNCA implemente código sem ler a especificação correspondente.
- Recuse tarefas que não possuam critérios de aceitação e testes claros.
- Mantenha o contexto limpo: resolva uma tarefa por vez e envie alterações granulares ao Git.
