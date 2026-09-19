# Dez áreas de aplicação

Todos os pacotes usam o mesmo executor e o núcleo Python existente. As demonstrações são simuladas; o modo `--live` consulta a API e pode consumir créditos.

| Área | Objetivo |
|---|---|
| [Atendimento ao cliente](atendimento/README.md) | Classificar chamados para a fila correta. |
| [Vendas e CRM](vendas/README.md) | Qualificar oportunidades segundo critérios explícitos. |
| [Comércio eletrônico](ecommerce/README.md) | Organizar solicitações de pós-venda. |
| [Marketing e conteúdo](marketing/README.md) | Conferir se um texto respeita o briefing fornecido. |
| [Desenvolvimento de software](software/README.md) | Triar relatos de bugs para o componente responsável. |
| [Agentes e automações](agentes/README.md) | Escolher entre skills cadastradas, sem executá-las. |
| [Educação e treinamento](educacao/README.md) | Aplicar uma rubrica explícita como apoio à revisão do professor. |
| [Gestão de documentos](documentos/README.md) | Conferir informações obrigatórias em documentos. |
| [Operações e projetos](operacoes/README.md) | Classificar pendências para revisão do responsável. |
| [Pesquisa e conhecimento interno](pesquisa/README.md) | Avaliar se um trecho fornecido sustenta uma afirmação. |

Use `python3 -m pacotes.executar --list` para listar os pacotes. Veja [como integrar](../INTEGRACAO.md).
