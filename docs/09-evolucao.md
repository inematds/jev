# Evolução com simplicidade

## Disponível nesta versão

- Vinte casos autorais agrupados, com busca por tema ou primitiva.
- Editor Choice/Noul/Score; múltiplas perguntas; estado textual ou JSON.
- Importação de requisição e exportação do resultado com procedência explícita.
- Cálculo do custo de entrada e estimativa do processo completo.
- Validação de Score, incluindo limite de níveis e `legend`.
- Experimentos por arquivo com regras, Jev, híbrido e replay; comparação e leitura do relatório no navegador.
- Exemplos de skills, comentários, diffs, contexto, intenções, datas e logs, sem execução de ações externas.
- Curso enriquecido em Markdown e laboratórios de aprofundamento.

O caminho inicial continua simples: `python3 -m jev_lab serve`. O site público funciona sem chave, instalação ou servidor, com respostas didáticas. O núcleo Python continua usando só a biblioteca padrão.

## O que depende de evidência futura

| Expansão | Condição de avanço |
|---|---|
| Triagem real de atendimento | Referência humana em português, resultado independente e observação operacional |
| Integração de skills ao agente | Demonstrar recall e qualidade final; não remover instruções obrigatórias |
| Revisão automática de código | Medir falsos negativos também nos trechos descartados; manter testes e revisão |
| Filtro de contexto em produção | Preservar evidências necessárias e contradições; medir resposta final |
| LLM ao vivo e fallback multicanal | Escolher provedor/contrato e avaliar custo total; hoje comparação externa por replay |
| Navegador operacional | DOM atualizado, executor restrito, assertions e trace; escolher elemento não prova sucesso |
| Concorrência de chamadas | Medir demanda e taxa; servidor local atual serializa avaliação por desenho |
| HTML do curso | Escolha do formato v5 ou v2; as aulas atuais estão publicadas em Markdown |

Nenhuma promessa de retorno financeiro, autonomia física, imunidade a injeção ou substituição universal de LLMs faz parte do produto. [Exageros e dúvidas](07-exageros-e-duvidas.md).
