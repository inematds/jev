# Exageros, dúvidas e limites do Jev

Revisão: **19/09/2026**. Documento autoral de validação técnica. Não contém transcrições ou materiais privados. “Documentado” significa descrito pelo fornecedor; desempenho real no nosso domínio depende de experimento.

## O que podemos afirmar

Jev recebe estado textual e perguntas delimitadas. `Choice` seleciona uma alternativa, `Noul` informa a probabilidade de sim e `Score` posiciona o estado numa rubrica ordenada. Código prepara a entrada, valida o retorno e controla a ação. Esse desenho é útil para experimentar classificação, roteamento, avaliação semântica e seleção de candidatos. [Contrato oficial](https://docs.typesafe.ai/api)

## Exageros que não adotamos

| Afirmação | Veredito | Formulação tecnicamente defensável |
|---|---|---|
| “Zero alucinação significa nunca errar” | Incorreta | Restrição de saída não impede selecionar a alternativa errada |
| “Resposta fechada é determinística” | Incorreta | Repetições podem variar; estabilidade também não prova acerto |
| “LLMs não produzem respostas estruturadas” | Incorreta | A comparação deve usar um LLM configurado para a mesma tarefa |
| “Jev é imune a prompt injection” | Incorreta | Há limitações adversariais reconhecidas; permissões pertencem ao executor |
| “Lê screenshot, áudio e vídeo diretamente” | Incorreta para a versão consultada | DOM, OCR ou transcrição são etapas externas identificáveis |
| “Gera qualquer interface ou código” | Incorreta | Escolher componentes prontos não equivale a criar conteúdo arbitrário |
| “Escolher uma ferramenta já executa a tarefa” | Incorreta | Argumentos, execução e verificação do resultado são etapas separadas |
| “Não pode ajudar com argumentos” | Generalização incorreta | Pode selecionar valores enumerados ou candidatos já extraídos |
| “Toda demo com opções prontas é falsa” | Incorreta | Decisões finitas são úteis; a demo precisa revelar a divisão de responsabilidades |
| “Revisor semântico substitui testes” | Incorreta | Pode sinalizar suspeitas; não prova o comportamento que um teste executa |
| “Selecionar linhas substitui qualquer resumo” | Incorreta | Filtragem pode reduzir contexto; síntese é outro trabalho |
| “Classificar milhões de registros nunca é viável” | Generalização incorreta | Pode ser viável em lote com pré-filtro e orçamento; não implica consulta interativa |
| “Um Score de 2,91 é 91% de certeza” | Incorreta | A nota é posição na rubrica, não uma chance de acerto |
| “Probability, confidence e intervalo de confiança são iguais” | Incorreta | Campo da distribuição, estatística de concentração e incerteza amostral são conceitos distintos |
| “Alterar critérios retreina o modelo” | Incorreta | Muda a requisição; não altera pesos do Jev |
| “Saída grátis significa uso gratuito” | Incorreta | A entrada é cobrada; infraestrutura e revisão também custam |
| “Saída sem cobrança significa nenhum token de saída” | Incorreta | A API possui `usage.output_tokens` |
| “200 vezes mais rápido em toda aplicação” | Não demonstrada | Ganhos dependem de tarefa, comparação, rede e fluxo completo |
| “Simulador comprova condução autônoma física” | Não demonstrada | Simulação não valida percepção, controle e operação física |
| “Buy/sell/hold simples prova lucro financeiro” | Incorreta | Simplicidade da saída não demonstra capacidade de previsão |

A documentação reconhece dificuldades com números, datas, conteúdo adversarial e contexto irrelevante. Não se deve esperar que perguntas independentes satisfaçam todas as identidades lógicas entre si. [Limitações conhecidas](https://docs.typesafe.ai/model-jaggedness/jev-1.13)

## Dúvidas que continuam abertas

**Quanto economiza aqui?** Não há benchmark próprio Jev publicado neste projeto. Existem fixtures autorais, testes de contrato e uma baseline lexical em 24 tickets fictícios. A métrica de uma regra não é resultado do modelo. O novo comando `experiment` permite reunir evidência, não a antecipa.

**As probabilidades são calibradas em português?** Precisamos medir por classe, distribuição de dados e versão. Um limiar de 0,90 é didático, não autorização universal. Noul não tem confidence separado. [Como ler confidence](https://docs.typesafe.ai/confidence)

**Qual é a arquitetura interna?** O fornecedor anuncia nova arquitetura, sampler paralelo e RLCD. Hipóteses sobre cabeças de classificação ou implementação específica não são uma auditoria publicada. Os ganhos de lançamento têm configuração e ressalvas próprias. [Metodologia e limites dos benchmarks](https://typesafe.ai/blog/introducing-system-one-models-and-jev)

**Seleção de skills reduz contexto?** É uma hipótese de integração. No cookbook oficial, o agente mantém o catálogo; a sugestão melhora a escolha no experimento apresentado. Esse desenho não comprova eliminar o catálogo nem reduzir dez mil tokens. [Experimento de skills](https://docs.typesafe.ai/cookbooks/skill_suggestion)

**O navegador foi realmente operado pelo modelo?** Sem o código e os registros da demo, não podemos separar seleção, cache, valores prontos, animação e execução. Navegação por DOM é uma arquitetura possível. Digitar valores existentes não exige geração de strings pelo Jev.

**Qual rota de API está disponível?** O cliente deste projeto usa a API direta TypeSafe. Menções a outros gateways não garantem disponibilidade para nossa conta; cada rota exige contrato e preço próprios. Não configuramos adaptadores fictícios para provedores não verificados.

**A própria documentação pode mudar?** Sim. A página de Score informa até 10 níveis, enquanto a referência HTTP resumida não explicita o máximo. O laboratório adota 2–10 descrições textuais e valida `legend`; é um subconjunto intencional do contrato. [Score](https://docs.typesafe.ai/primitives/score)

## As contas que precisam acompanhar a promessa

Na tarifa consultada de **US$ 0,042 por milhão de tokens de entrada**:

| Situação hipotética | Custo de entrada |
|---|---:|
| Uma chamada com 10 mil tokens | US$ 0,00042 |
| Mil chamadas com 10 mil tokens cada | US$ 0,42 |
| 150 mil tokens | US$ 0,0063 |
| Um milhão de registros com 2 mil tokens cada | US$ 84 |

Portanto, US$ 0,0042 para dez mil tokens está dez vezes acima do cálculo. Uma API barata pode continuar cara no fluxo completo. A calculadora inclui estimativas de fallback, revisão humana e infraestrutura.

O modelo documentado é `jev-1.13.0`, textual, com orçamento total de 64k tokens e 32k para estado mais a maior pergunta. Limites de taxa podem mudar. Confira a fonte antes de executar um lote: **[modelos, modalidades, preços e limites oficiais](https://docs.typesafe.ai/models)**.

## Como validar uma aplicação sem se deixar levar pela demo

1. Fixar decisão, candidatos e opção de insuficiência.
2. Usar referência revisada por pessoas e separar desenvolvimento, calibração e teste.
3. Comparar mesma entrada entre componentes e mesma tarefa entre fluxos completos.
4. Medir erros, cobertura, latência ponta a ponta, custo total e retrabalho.
5. Distinguir `live`, regras, replay e simulação nos artefatos.
6. Amostrar também o que o filtro descartou; uma lista curta pode esconder falsos negativos.
7. Tornar explícita a condição para rejeitar a adoção.

**Decisão deste projeto:** investir em classificação e seleção delimitadas, com evidências recuperáveis e execução controlada. Simulações continuam úteis para aprender; nenhuma delas é apresentada como garantia operacional.

[Voltar ao README](../README.md) · [Executar experimentos](08-experimentos.md)
