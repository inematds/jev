# Experimentos reproduzíveis

O laboratório executa **regras**, **Jev direto**, **híbrido de regras + Jev** e **replay**. Nenhum modo executa a ação classificada. A avaliação usa uma pergunta `Choice` como alvo; a requisição pode conter perguntas auxiliares. Noul e Score estão disponíveis no editor e na consulta, mas não têm métrica de qualidade automática nesse avaliador. Para avaliar todas as perguntas Choice/Noul/Score contra referências explícitas, use o avaliador complementar [pacotes.qualidade](11-fluxos-praticos.md).

## Um comando para começar

```bash
python3 -m jev_lab experiment data/tickets-sinteticos.jsonl --out runs/regras
```

A pasta recebe `report.json` e `predictions.csv`. Importe o JSON na seção “Leia seu experimento” do laboratório. `runs/` é ignorada pelo Git; IDs ainda podem ser sensíveis, portanto não publique relatórios operacionais sem revisão.

## Modos

```bash
# Jev: requer TYPESAFE_API_KEY; não inventa resposta na ausência de acesso
python3 -m jev_lab experiment data/tickets-sinteticos.jsonl --provider jev --out runs/jev

# Híbrido experimental: regra resolve o que reconhecer; os demais vão ao Jev
python3 -m jev_lab experiment data/tickets-sinteticos.jsonl --provider hybrid --out runs/hibrido

# Comparar no mesmo dataset e nas mesmas classes
python3 -m jev_lab compare runs/regras/report.json runs/jev/report.json

# Observar estabilidade sem contar repetições como exemplos independentes
python3 -m jev_lab experiment data/tickets-sinteticos.jsonl --provider jev --repeats 3 --max-calls 72 --out runs/repeticoes
```

O limite padrão é 100 observações por execução, contado antes de iniciar. Cada chamada Jev tem até três tentativas HTTP com prazo global do cliente. `--max-calls` limita observações, não tentativas HTTP. O híbrido é uma hipótese a medir: regras também podem errar. Não use a simples presença de uma palavra como autorização operacional.

## Dataset e template próprio

Formato JSONL, um objeto por linha:

```json
{"id":"item-001","state":{"pedido":"Criar uma apresentação nova"},"expected":"criar_deck","sensitive":false}
```

`text`/`label` também são aceitos para os tickets existentes. IDs não podem se repetir. `expected` precisa existir entre as alternativas. `sensitive: true` obriga revisão, inclusive em regra.

```bash
python3 -m jev_lab cases
python3 -m jev_lab cases --id skills --out runs/skills-template.json
python3 -m jev_lab experiment data/skills-sinteticas.jsonl --template exemplos/skills-request.json --provider jev --question decisao --out runs/skills
```

O `state` do template é substituído pelo estado de cada registro. Descrições do catálogo devem estar nos critérios ou no próprio estado de cada evento. Regras/híbrido aceitam somente o template padrão de atendimento; não fingem avaliar outros domínios.

## Comparar um LLM ou uma execução já registrada

Use `--provider replay --replay caminho.jsonl`. A coleta do LLM é externa; **não há adaptador LLM ao vivo embutido**. Normalize sua resposta para o contrato TypeSafe da pergunta, conservando os valores efetivamente medidos. Não invente probabilidades: se o seu modelo não as forneceu, esse formato de replay probabilístico não é adequado.

Cada linha exige `id`, `request_sha256`, `response` e `origin` (`measured` ou `simulation`). Pode incluir `repetition` (padrão 0), `latency_ms` e `cost_usd`; valor desconhecido deve ser `null`. O hash é calculado por `jev_lab.experiments.digest(payload)`, após substituir o estado pelo registro. IDs/repetições devem corresponder exatamente ao dataset.

Exemplo fictício executável:

```bash
python3 -m jev_lab experiment data/tickets-sinteticos.jsonl --provider replay --replay data/replay-didatico.jsonl --out runs/replay
python3 -m jev_lab compare runs/regras/report.json runs/replay/report.json
```

`data/replay-didatico.jsonl` contém **números autorais simulados**, incluindo erros intencionais. Não mede Jev nem LLM. `origin: measured` é uma declaração de quem produziu o arquivo, não autenticação criptográfica da origem. Replay reutiliza latências declaradas, não cronometra inferência nova.

## Interpretação das métricas

- Acurácia, macro-F1, matriz e qualidade das sugestões: somente primeira repetição; erro operacional permanece no denominador.
- Cobertura: fração com sugestão; precisão aceita: acertos entre as sugestões. Sem sugestões, precisão é `null`.
- Brier multiclasse: soma dos erros quadráticos por item; ECE: dez intervalos da maior probabilidade. Regras não recebem probabilidades inventadas.
- Repetibilidade: acordo de rótulo em todas as repetições de cada item; falhas não contam como estabilidade bem-sucedida.
- p50/p95: observações completas do componente medido, incluindo tentativas. Replay mostra medidas declaradas.
- Custo conhecido: subtotal de valores observados/estimados. Após retry de API, o custo total permanece desconhecido porque o consumo anterior pode não estar disponível. Falha não é custo zero.

`compare` exige mesmo hash do dataset e mesmas classes. Informa se template ou política diferem; nesse caso, compare fluxos com cuidado. Um arquivo simulado nunca vira resultado real por estar numa comparação.

Congele limiares antes do teste. Ganhos precisam considerar coleta, fallback, revisão, infraestrutura e retrabalho. Consulte o [protocolo](04-avaliacao.md) e o [documento de exageros e dúvidas](07-exageros-e-duvidas.md).
