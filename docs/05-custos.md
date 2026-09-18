# Custos e viabilidade

Tarifa de referência consultada em 18/09/2026: **US$ 0,042 / milhão de tokens de entrada**, sem cobrança pelos tokens de saída. Confirmar tarifa e condições da rota escolhida antes do experimento. [Fonte oficial](https://docs.typesafe.ai/models)

## Correção da transcrição

```text
custo_API = chamadas × tokens_médios_de_entrada / 1.000.000 × 0,042
10.000 / 1.000.000 × 0,042 = US$ 0,00042 por chamada
```

| Chamadas | Entrada por chamada | Custo calculado |
|---:|---:|---:|
| 1 | 10.000 tokens | US$ 0,00042 |
| 1.000 | 10.000 tokens | US$ 0,42 |
| 10.000 | 10.000 tokens | US$ 4,20 |
| 100.000 | 10.000 tokens | US$ 42,00 |
| 1.000.000 | 10.000 tokens | US$ 420,00 |

O valor de US$ 0,0042 por chamada falado no vídeo está dez vezes acima do cálculo nessa tarifa. Os totais de US$ 4,20 para 10.000 chamadas e US$ 42 para 100.000 chamadas correspondem ao cálculo corrigido.

## O custo que decide a adoção

```text
baseline = N × custo_médio_LLM + revisão_atual + infraestrutura_atual
híbrido = custo_Jev_total + chamadas_LLM_residuais + revisão_nova
          + infraestrutura_nova + integração_amortizada + retrabalho
benefício = baseline - híbrido
```

Não assumir que todas as chamadas residuais têm o custo médio anterior: elas podem concentrar justamente os casos longos e difíceis. Perguntas, critérios, contexto, retries e novas chamadas entram na contagem real. Leitura/OCR/transcrição e filas também entram no orçamento quando usados.

Exemplo **hipotético**, não medido: 100.000 eventos; 2.000 tokens totais por evento no Jev; LLM a US$ 0,01 por evento; 20% seguem ao LLM, ao mesmo custo unitário. Jev = US$ 8,40; LLM residual = US$ 200; baseline só LLM = US$ 1.000. Economia bruta = US$ 791,60 (79,16%), antes de pessoal, infraestrutura, erros e implantação. O percentual de fallback é uma premissa, não uma previsão.

Num modelo simplificado com uma chamada por evento, o custo marginal compensa quando `custo_Jev + fração_fallback × custo_LLM + custo_extra_por_evento < custo_LLM`. Se revisão humana dominar, uma API quase gratuita ainda pode aumentar o custo total.

## Planilha a preencher no piloto

Volume mensal; distribuição de tokens; chamadas por evento; tarifa por rota; custo de fallback; segundos humanos por revisão; custo de retrabalho; infraestrutura incremental; horas de implantação amortizadas; economia líquida e sensibilidade a duas vezes mais fallback. Nenhum orçamento foi consumido em chamadas de inferência nesta etapa.
