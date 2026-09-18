# Dez aplicações — da ideia ao experimento

Prioridades são propostas para este projeto, não resultados medidos. P0 = piloto; P1 = expansão após avaliação; P2 = estudo avançado supervisionado.

| # | Caso do vídeo | Entrada e decisão delimitada | Próxima ação proposta | Como avaliar / limite | Prioridade |
|---|---|---|---|---|---|
| 1 | Checagem de afirmações | Afirmação + passagens: apoiada / contradita / insuficiente | Encaminhar para revisão editorial | Precisão por classe; não confundir apoio textual com verdade externa | P1 |
| 2 | Atendimento | Ticket + contexto: suporte / cobrança / vendas / outro / insuficiente | Sugerir fila; humano pode corrigir | Macro-F1, erro por fila e retrabalho | P0 |
| 3 | Revisão contratual | Cláusula + checklist: presente / ausente / ambígua | Marcar pontos para profissional | Recall de omissões; nunca liberar contrato só pelo modelo | P2 |
| 4 | Mudanças em e-mails | Mensagens ordenadas + candidatos: quinta / sexta / sábado / não informado / conflito | Sinalizar mudança | Acerto de evidência; datas e precedência calculadas em código | P1 |
| 5 | Roteamento de modelos | Tarefa + capacidades permitidas: simples / código / pesquisa / revisão | Selecionar destino permitido | Qualidade final e custo, incluindo erros de rota | P1 |
| 6 | Verificar etapa de agente | Resultado + critério estreito: atende / falha / insuficiente | Continuar, repetir com limite ou escalar | Erro de aprovação e loops; não substitui execução de testes | P1 |
| 7 | Roteamento de agentes | Pedido + catálogo: agente A / B / C / nenhum | Despachar tarefa com permissões já definidas | Resolução final; escolha de agente não concede acesso | P1 |
| 8 | Navegador | Texto/DOM + IDs de elementos: candidato / nenhum / ambíguo | Resolver ID e executar ação permitida | Sucesso de localização e tempo completo, incluindo extração | P2 |
| 9 | Apoio à revisão clínica | Caso fictício + checklist elaborado por profissional: revisar / insuficiente | Organizar revisão humana | Exercício de engenharia, sem diagnóstico ou decisão clínica automática | P2 |
| 10 | Alertas financeiros | Alerta fictício + política: arquivar / revisar / acompanhar | Organizar fila simulada | Erro de descarte; sem recomendação de investimento ou ordem automática | P2 |

Casos 3, 9 e 10 serão exercícios com dados fictícios. Uma eventual aplicação real exige projeto próprio de validação e responsáveis do domínio; não faz parte deste piloto.

## Oportunidades no ecossistema INEMA

- **Atendimento da comunidade:** aplicar o caso 2 a dúvidas de acesso, conteúdo, cobrança e contato comercial. Entrada inicial por arquivo; integrações somente após evidência.
- **Transcrições do inemavox:** combinar “houve agendamento?”, “houve interesse comercial?” e “faltam dados?” em perguntas separadas; mais de uma rota pode ser ativada.
- **Qualidade editorial de cursos:** avaliar se uma afirmação está apoiada pelo material de referência; links, cálculos e presença de seções continuam verificados em código.
- **Gestão de agentes / LOOP-R:** usar julgamentos estreitos em observar e rotear. Alterações de memória, políticas e ferramentas precisam de processo próprio; não promover uma hipótese do modelo a regra permanente automaticamente.

Estas são propostas de integração. Nenhum desses projetos foi alterado.

## Por que começar por atendimento

Há classes compreensíveis, revisão humana acessível, possibilidade de reversão e facilidade de montar dados em português. Roteamento de modelos parece atraente, mas exige medir o resultado do trabalho posterior; isso torna o primeiro experimento mais caro e confuso.
