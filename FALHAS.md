# Falhas corrigidas nos materiais derivados

| data | o que quebrou | menor correção | prompt \| infra |
|---|---|---|---|
| 2026-09-18 | catálogo PRO resolve capa em guia/capa, mas a geração salva na raiz | emitir alias da capa no build público, sem duplicar fonte | infra |
| 2026-09-18 | verificação Git acusou finais CRLF dos CSVs | padronizar arquivos e exportador em LF | infra |
| 2026-09-18 | links âmbar do template tinham contraste insuficiente no tema claro | escurecer somente a cor de texto e preservar preenchimento dos botões | infra |
| 2026-09-18 | comandos longos alargavam o guia no celular | limitar a coluna dos passos com minmax(0,1fr), preservando scroll interno do código | infra |
| 2026-09-18 | resultado da consulta poderia aparecer no caso selecionado durante a espera | vincular resposta ao ID e ao payload enviados antes de renderizar | infra |
| 2026-09-18 | transcrição mistura US$ 0,0042 por chamada de 10 mil tokens com totais dez vezes menores | recalcular na tarifa oficial e registrar US$ 0,00042 na análise, preservando o original | prompt (conteúdo-fonte) |
