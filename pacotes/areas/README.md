# 17 áreas de aplicação

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

Sete pacotes adicionais com perguntas combinadas:

| Área | Objetivo |
|---|---|
| [Caixa de entrada](caixa-entrada/README.md) | Tipo, urgência, documentos financeiros e patrocínio. |
| [Comentários do YouTube](comentarios-youtube/README.md) | Ajuda, resposta, ideias de conteúdo e compra explícita. |
| [Comunidades](comunidades/README.md) | Dúvidas, intervenção e insatisfação expressa. |
| [Reuniões](reunioes/README.md) | Decisão, ação, responsável e prazo explícitos. |
| [Cortes](cortes/README.md) | Clareza e independência da transcrição de um trecho. |
| [Notas](notas/README.md) | Tarefa, ideia, diário e referência após transcrição. |
| [Curadoria](curadoria/README.md) | Relevância textual conforme interesses declarados. |

[Lotes e avaliação por pergunta](../../docs/11-fluxos-praticos.md).

Use `python3 -m pacotes.executar --list` para listar os pacotes. Veja [como integrar](../INTEGRACAO.md).
