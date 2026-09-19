# Falhas corrigidas nos materiais derivados

| data | o que quebrou | menor correção | prompt \| infra |
|---|---|---|---|
| 2026-09-19 | leitura da análise assumiu exemplos/emails-request.json inexistente | consultar o caso emails em app/cases.json antes de resolver o caminho | prompt |
| 2026-09-19 | pedido de tradução do README foi associado ao bot em vez do repo atual Jev | confirmar o escopo pelo diretório atual e aplicar a correção antes de editar | prompt |
| 2026-09-19 | definição polyskill escrita com frontmatter de SKILL.md foi recusada | usar identity.description.full e declarar recursos conforme o template do CLI | prompt |
| 2026-09-19 | validador aceitava Score acima do teto documentado e resposta sem legend | limitar a 2–10 níveis e exigir legenda correspondente, com testes negativos | infra |
| 2026-09-19 | contagem inicial da análise considerou só oito arquivos e omitiu o vídeo colado na conversa | inventariar todos os links por ID: 11 envios, nove vídeos únicos | prompt |
| 2026-09-18 | catálogo PRO resolve capa em guia/capa, mas a geração salva na raiz | emitir alias da capa no build público, sem duplicar fonte | infra |
| 2026-09-18 | verificação Git acusou finais CRLF dos CSVs | padronizar arquivos e exportador em LF | infra |
| 2026-09-18 | links âmbar do template tinham contraste insuficiente no tema claro | escurecer somente a cor de texto e preservar preenchimento dos botões | infra |
| 2026-09-18 | comandos longos alargavam o guia no celular | limitar a coluna dos passos com minmax(0,1fr), preservando scroll interno do código | infra |
| 2026-09-18 | resultado da consulta poderia aparecer no caso selecionado durante a espera | vincular resposta ao ID e ao payload enviados antes de renderizar | infra |
| 2026-09-18 | transcrição mistura US$ 0,0042 por chamada de 10 mil tokens com totais dez vezes menores | recalcular na tarifa oficial e registrar US$ 0,00042 na análise, preservando o original | prompt (conteúdo-fonte) |
