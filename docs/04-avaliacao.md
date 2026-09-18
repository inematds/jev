# Protocolo de avaliação

Status: desenho de experimento. Nenhum resultado real foi produzido.

## Hipótese e referências

Hipótese: a triagem com Jev reduz custo ou tempo total sem exceder o orçamento de erro aceito pelo responsável. Comparar quatro caminhos no mesmo conjunto: regras simples; Jev; LLM com saída estruturada; híbrido Jev + fallback. Congelar versões, perguntas, parâmetros e região de execução. Selecionar o LLM pela tarefa, preço atual e disponibilidade quando o experimento começar.

## Dados

Proposta inicial: 600 tickets anonimizados e revisados, distribuídos em desenvolvimento (200), calibração (200) e teste final (200). Separar por conversa/cliente e tempo quando possível; nenhuma mensagem da mesma conversa pode cruzar partições. Esses tamanhos são um começo exploratório, não prova de segurança para erros raros.

Manter um conjunto adicional de desafio com negações, duas intenções, falta de contexto, linguagem informal, português com erros, texto transcrito incorretamente, injeção de instruções e classes novas. Reportar esse conjunto separadamente: ele não estima a prevalência no tráfego.

Cada item terá rótulo de fila, suficiência, justificativa curta e trecho de evidência. Duas pessoas revisam amostras e todos os casos ambíguos; desempate pelo responsável. Medir concordância. Rótulos produzidos por IA podem auxiliar, mas precisam de revisão humana antes de virar referência.

## Métricas

- Macro-F1 e matriz de confusão por classe; reportar suporte amostral.
- Precisão das sugestões aceitas automaticamente e cobertura (fração automatizável).
- Recall dos casos que exigem revisão; custo do falso negativo por classe.
- Acurácia da decisão final após fallback, incluindo os erros dessa etapa.
- Latência ponta a ponta p50/p95, taxa de timeout e falhas; incluir fila, rede e retries.
- Custo por evento e por decisão final correta; registrar tokens efetivamente cobrados.
- Taxa e minutos de revisão humana, retrabalho e chamadas ao modelo maior evitadas.
- Brier multiclasses e diagrama de confiabilidade para probabilities; ECE com bins e contagens publicados. Não usar confidence como probabilidade de classe sem validação.
- Repetir um subconjunto 10 vezes para observar variação; não misturar isso com amostras independentes de qualidade.

Publicar intervalos de incerteza para taxas e comparação pareada por evento. Zero erros em uma amostra pequena não significa risco zero. No caso de zero erros, a aproximação 3/n para o limite superior de 95% ilustra por que 20 decisões não comprovam erro menor que 1%.

## Calibração da política

Usar desenvolvimento para escrever perguntas. Usar calibração para selecionar limiares por ação e modelo. Abrir teste final uma vez depois de congelar a política; se alterar após inspecionar o teste, reservar outro conjunto. Não transferir um limiar de Noul para Choice ou para outra versão do modelo.

## Metas candidatas, a negociar antes do teste

| Dimensão | Meta inicial proposta | Se falhar |
|---|---|---|
| Precisão nas rotas automatizáveis | ≥98%, com incerteza e volume por classe apresentados | Manter revisão ou recolher mais dados |
| Qualidade final versus referência operacional | Queda máxima de 1 ponto percentual, com comparação pareada | Ajustar desenho no desenvolvimento e retestar em holdout novo |
| Cobertura | ≥40% dos eventos com rota segura | Avaliar se complexidade se paga |
| Economia total | ≥30% contra baseline, incluindo revisão e integração amortizada | Não justificar expansão por preço/token |
| Latência p95 completa | ≤2 s no piloto de triagem, se compatível com produto | Rever filas/retries ou manter processamento assíncrono |
| Contrato/permissões | Zero execução fora das rotas autorizadas | Bloquear liberação até correção em código |

São critérios de projeto, não métricas do Jev. As 200 amostras finais podem não bastar para demonstrar metas estreitas; aumentar amostra em vez de declarar aprovação por estimativa pontual. Um resultado inconclusivo é uma saída válida.

## Observação e retorno

Durante observação, a operação anterior continua decidindo. Inspecionar todos os desacordos e amostra das concordâncias. Se houver aumento de erro relevante, deriva de classes, falhas sustentadas ou custo inesperado, suspender sugestão automática e investigar. Atualização de modelo exige reavaliação antes de reusar limiares.

## Artefatos esperados

Manifesto do dataset e hashes; instruções de rotulagem; configuração congelada; predições por ID; versão de cada provedor; CSV de métricas; relatório de erros; decisão de continuar, ampliar amostra ou encerrar. Todos ainda por produzir.
