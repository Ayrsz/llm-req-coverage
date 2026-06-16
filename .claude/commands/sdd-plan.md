---
description: Monta o plano de engenharia a partir de uma spec (Spec-Driven Development)
argument-hint: [caminho_da_spec]
---
Siga a metodologia Spec-Driven Development.

Leia a especificação em `$ARGUMENTS`, analise o codebase atual (README, código,
CLAUDE.md) e gere o plano técnico em `docs/specs/<nome>-plan.md`.

Conteúdo obrigatório do plano:
- **Arquitetura afetada** — módulos/arquivos que serão tocados.
- **Mudanças no banco/APIs** — se houver.
- **Impactos colaterais** — riscos e efeitos em outras partes.
- **Definition of Done** — quando a feature está pronta (inclui testes e validação).

Regras de ouro: baseie-se apenas no que existe no repositório, não invente; não
implemente código nesta etapa. Ao final, mostre o caminho do arquivo e pare.
