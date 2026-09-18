# Análise crítica consolidada

Data de consulta: 18/09/2026. Não fizemos chamadas ao modelo. “Confirmado” significa documentado pelo fornecedor, não validado experimentalmente por nós.

## Conclusão

Vale realizar um piloto limitado. O valor a investigar é quanto trabalho caro pode ser evitado mantendo a qualidade da decisão final. A economia por token, isoladamente, não demonstra benefício operacional. Se uma regra simples resolver o caso, ela é a primeira referência de comparação.

A análise separa capacidades documentadas, alegações de desempenho e hipóteses de aplicação. Nenhum benchmark externo foi reproduzido nesta etapa.

## Auditoria das principais afirmações

| Afirmação | Avaliação | Tratamento no projeto |
|---|---|---|
| Jev avalia contexto e perguntas com respostas delimitadas | Documentada | Base da arquitetura; tipos Choice, Noul e Score [1] |
| É apenas um classificador antigo | Analogia funcional, não descrição comprovada da arquitetura | Explicar classificação sem inferir implementação interna |
| Nova arquitetura, sampler paralelo e RLCD | Declaração do fornecedor | Não tratar como auditoria independente [2] |
| Sempre 193,6x mais rápido / 444,6x mais barato | Generalização indevida | Máximos de workflows publicados; comparar com nossa linha de base [2] |
| Zero alucinação significa decisão correta | Incorreto | Restrição de tipo não demonstra verdade semântica |
| Saída delimitada significa determinismo integral | Não decorre dessa propriedade | Registrar versão, entrada e variação entre repetições |
| LLM não consegue retornar opções fechadas | Generalização indevida | O próprio benchmark usa wrapper de LLM com decisões estruturadas [2] |
| Probabilidade, confidence e intervalo de confiança são iguais | Incorreto | Ensinar conceitos separados [3] |
| Basta confidence maior que 90% para executar | Inadequado | Ajustar por ação e avaliar erros reais; não há limiar universal |
| Jev lê screenshot e encontra botão | Não é a modalidade documentada | Usar DOM/texto ou extrator anterior; contabilizar essa etapa [4] |
| Verifica verdade sem fontes | Não demonstrado | Avaliar apoio em evidências fornecidas, com opção de insuficiência |
| Substitui qualquer juiz LLM | Não demonstrado | Reservar julgamentos estreitos; raciocínio complexo continua separado |
| O exemplo do hotel produz explicação livre | Não é saída nativa esperada | Classificar política; explicação e citação vêm de extração/código/LLM |

## O contrato real importa

`Choice` escolhe uma classe e devolve sua distribuição. `Noul` expressa a probabilidade de “sim”; não traz campo separado de confidence. `Score` usa níveis ordenados e pode retornar valor intermediário, não necessariamente uma nota inteira. [1, 5, 6]

`confidence` é uma estatística derivada da distribuição. Não assumir que equivale à maior probabilidade nem que 0,93 garante 93% de acerto no nosso tráfego. Intervalos estatísticos sobre taxas de acerto devem ser calculados no experimento. [3]

Perguntas avaliadas isoladamente no mesmo contexto não garantem coerência lógica entre respostas. Invariantes, permissões e regras comerciais pertencem ao código. A documentação também reconhece dificuldades com números, datas, contexto irrelevante e conteúdo adversarial. [7]

## Como interpretar benchmarks

Resultados de amostras pequenas, sintéticas ou rotuladas por IA não comprovam desempenho em produção. Definir a unidade de medida: acertar todas as etiquetas de uma chamada é diferente de acertar cada etiqueta isoladamente. Ganhos relativos dependem do modelo comparado, tarefa, configuração e infraestrutura.

O benchmark do fornecedor usa probabilidades de modelos como referência. Concordância com essa referência não equivale a verdade objetiva. Os próprios autores reconhecem viés potencial e que os maiores ganhos não são expectativa universal. [2]

## Correção econômica

Com a tarifa consultada de US$ 0,042 por milhão de tokens de entrada, 10.000 tokens custam **US$ 0,00042**, não US$ 0,0042. O vídeo combina o valor por chamada incorreto com totais posteriores compatíveis com o valor correto. Ver [memória de cálculo](05-custos.md). [4]

## Decisão recomendada

Pilotar triagem de tickets antes de integrar CRM, agentes ou modelos. Medir português brasileiro, ambiguidades e dados ausentes. Avançar apenas quando o custo completo, a qualidade final e a taxa de revisão humana justificarem a mudança. Não assumir que o desempenho em inglês se transfere ao português.

## Referências

1. [Introdução](https://docs.typesafe.ai/introduction)
2. [Lançamento e metodologia](https://typesafe.ai/blog/introducing-system-one-models-and-jev)
3. [Confidence](https://docs.typesafe.ai/confidence)
4. [Modelos, preço e modalidades](https://docs.typesafe.ai/models)
5. [Noul](https://docs.typesafe.ai/primitives/noul)
6. [Score](https://docs.typesafe.ai/primitives/score)
7. [Limitações Jev 1.13](https://docs.typesafe.ai/model-jaggedness/jev-1.13)
