# Estado atual

19/09/2026 · v1.6.1. Laboratório ampliado para 20 casos, Choice/Noul/Score, perguntas combinadas, estado JSON, importação/exportação, custo completo e leitura de relatórios. CLI experiment e compare: regras, Jev direto, híbrido e replay, com hashes, procedência, falhas e métricas.

Score limitado a 2–10 níveis, legend validada. Baseline reexecutada: 20/24 fictícios; não há benchmark Jev real. Exemplos e replay são autorais simulados. Conteúdo recebido em doc/ e fontes/originais/ permanece local e excluído do build.

Curso irmão v1.3.0: 36 aulas enriquecidas, 12 laboratórios e 20 casos. HTML continua pendente de escolha de formato. Publicação via git; consultar docs/06-publicacao.md para evidências.

Pacotes iniciais em pacotes/: adaptador Python que usa o núcleo existente, skill jev-integrar e índice de receitas. Exemplo offline disponível; sem distribuição PyPI nem instalação global.

Dez áreas em pacotes/areas, executor comum pacotes.executar, função avaliar_area e guia INTEGRACAO.md. Verificação: 34 testes Python, dez demonstrações offline e validação estrutural da skill. Não há pacote PyPI, conectores comerciais ou benchmark de inferência real.

OpenRouter disponível com --provider openrouter ou JEV_PROVIDER=openrouter; modelo ~typesafe/jev-latest. Dez consultas reais passaram sem falha, além da consulta combinada Choice/Noul/Score. Report: reports/openrouter-smoke.json. Isso não é benchmark independente. Testes automatizados controlados: 41.

Skill jev-decidir gerada via polyskill e instalada em ~/.agents/skills e ~/.claude/skills. Scripts das duas variantes consultaram Jev real com exemplo fictício. openpcbotv3 recebeu integração nativa em observação no gateway; serviço 3.3.4 ativo, observação habilitada no chat principal, sem controle de ações pelo Jev.

Atualização v1.6.1: 17 pacotes (sete novos com perguntas combinadas), pacotes.lote com prévia/concorrência limitada/retomada, pacotes.qualidade com referência por pergunta. Novos pacotes validados apenas por fixtures e testes controlados; não houve novas chamadas reais. Guia: docs/11-fluxos-praticos.md.

Verificação v1.6.1: 52 testes automatizados passaram; sete demonstrações e sete avaliações simuladas rodaram pela CLI; prévia JSONL sem chamadas, links locais, comandos equivalentes nos três idiomas e build verificados.
