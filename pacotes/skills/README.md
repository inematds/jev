# Skills para incorporar

- **[jev-decidir](jev-decidir/README.md):** consultas diretas no Codex e Claude Code, com variantes instaláveis e script testado.
- **[jev-integrar](jev-integrar/SKILL.md):** orientações para acrescentar Jev ao código de um sistema.

[`jev-integrar`](jev-integrar/SKILL.md) orienta o agente a incorporar o cliente e as receitas em um projeto de destino. Ela contém instruções; não é um classificador autônomo nem um instalador de outras skills.

Copie a pasta `jev-integrar/` para o diretório de skills aceito pelo seu agente, preservando `SKILL.md`. Você também pode fornecer o caminho do arquivo diretamente ao agente. Esta entrega não altera a configuração nem instala skills globalmente.

Exemplo de pedido:

> Use a skill jev-integrar para acrescentar triagem de suporte ao meu projeto. Comece com um exemplo fictício offline e mantenha os casos incertos em revisão.

A skill depende do cliente no clone Jev, localizado durante o uso. O formato foi validado; o comportamento não foi homologado em todos os agentes. A skill de integração permanece como fonte genérica; as variantes instaláveis para consultas diretas estão em jev-decidir.
