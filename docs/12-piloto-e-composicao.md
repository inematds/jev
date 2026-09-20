# Um piloto que cabe em uma página

Escolha uma decisão recorrente e acompanhe a mesma decisão do desenho à avaliação. O roteiro abaixo pode ser copiado para qualquer um dos 17 pacotes.

1. **Decisão e responsável:** quem usará o resultado e o que poderá fazer com ele?
2. **Entrada disponível:** quais campos existem na hora da decisão? Uma transcrição pode estar incompleta; identifique quem falou cada frase.
3. **Pergunta atômica:** avalie uma propriedade por pergunta. Não misture “há intenção de comprar?” com “o vendedor ofereceu um produto?”.
4. **Critérios e fronteiras:** escreva inclusão, exclusão e informação insuficiente; mantenha exemplos positivos, negativos e ambíguos.
5. **Referência humana:** rotule sem olhar a resposta do modelo. Registre desacordo, origem e autorização para usar os dados.
6. **Comparação:** congele critérios, modelos e versões. Separe ajuste e teste; compare regras, Jev e alternativa generativa com a mesma referência.
7. **Política:** avalie erro e cobertura por faixa e por classe. Um corte de 0,9 é uma hipótese, não uma garantia. Nunca transforme ausência de texto em evidência negativa.
8. **Observação:** registre decisões sem executar ações, revise erros e só depois defina o que pode ser automatizado.

## Três casos de fronteira autorais

| Contexto | Pergunta | Referência |
|---|---|---|
| Atendente: “Você quer comprar?” Cliente: “Não, preciso recuperar minha senha.” | O cliente expressou intenção de compra? | Não |
| Cliente: “Qual o preço? Também preciso corrigir meu acesso.” | Quais intenções aparecem? | Compra e suporte em perguntas separadas |
| “[áudio indisponível]” | Qual a intenção principal? | Informação insuficiente |

Alterar critérios para acertar estes três exemplos é ajuste. Verifique outros casos separados antes de alegar melhoria.

## Combinar pontuações com significado explícito

`pacotes.composicao.compor(request, response, pesos)` valida a requisição e a resposta completas antes de combinar perguntas Score. Para cada pergunta, divide o valor pelo último índice da rubrica (`número de níveis − 1`); calcula então a média ponderada. Os pesos podem somar qualquer valor positivo. A saída fica entre 0 e 1 e **não é probabilidade nem confiança**.

```python
from pacotes.composicao import compor

# request e response são os objetos completos já obtidos pelo cliente.
# As duas rubricas devem crescer no mesmo sentido: maior = mais prioritário.
ranking = compor(request, response, {"relevancia": 2, "urgencia": 1})
print(ranking["indice"])
```

Exemplo numérico fictício: relevância 3 numa rubrica de 5 níveis → 0,75; urgência 1 numa rubrica de 3 níveis → 0,5. Com pesos 2 e 1, o índice é 0,6667. Uma rubrica de risco crescente não deve ser somada a uma de segurança crescente sem redefinir a direção. A fórmula supõe intervalos equivalentes entre níveis ordinais; teste se essa aproximação serve para a finalidade. Não agregamos `confidence`.

Uma média alta pode esconder um requisito obrigatório ausente. Preserve os resultados por pergunta e aplique impedimentos explícitos antes de usar a ordenação. Esta função não executa ações e não altera a política conservadora do adaptador.

## O que aproveitamos e o que não tratamos como evidência

A referência educacional [jev.teachme.love](https://jev.teachme.love/) motivou o roteiro contínuo, a atenção ao falante e a composição de rubricas. O texto e os exemplos acima são autorais. A fórmula também aparece na [documentação oficial de composição](https://docs.typesafe.ai/patterns/composite-scoring).

Na consulta de 20/09/2026, a página inicial descrevia 40 chamadas reais, mas a primeira aula descrevia transcrições sintéticas. Não adotamos esse conjunto nem seus números como validação do projeto. Acerto por etiqueta e acerto de todas as etiquetas de uma chamada têm denominadores diferentes; 39/40 e 92,5% não são, por si só, uma contradição. Demonstrações de alteração de critério precisam de nova execução e teste independente para comprovar melhoria.

O curso HTML v2 aplica este roteiro em [Jev na prática](https://inematds.github.io/jev-curso/). Progresso e atividades são locais ao navegador; nenhum exercício chama API ou usa créditos de terceiros.
