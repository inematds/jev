# Receitas para adaptar ao trabalho

Os templates são mantidos em uma única pasta: [`exemplos/`](../../exemplos/). Substitua o `state` pelos dados necessários, ajuste os critérios e valide antes de consultar.

| Receita | Template | Como incorporar |
|---|---|---|
| Triagem de atendimento | [Triagem composta](../../exemplos/triagem-composta-request.json) | Sugere fila, urgência e suficiência; seu sistema decide o encaminhamento |
| Escolha entre skills | [Skills](../../exemplos/skills-request.json) | Recebe pedido e catálogo de candidatos; sugere a skill sem executá-la |
| Seleção de evidências | [Evidências](../../exemplos/evidencias-request.json) | Ajuda a filtrar trechos antes da geração de uma resposta |
| Revisão de comentários | [Comentários](../../exemplos/comentarios-request.json) | Avalia comentários por rubrica para apoiar revisão |
| Revisão de alteração de código | [Diff](../../exemplos/diff-request.json) | Produz sinais de revisão, sem aprovar ou fazer merge |
| Intenções simultâneas | [Multirrótulos](../../exemplos/multirrotulos-request.json) | Faz perguntas independentes sobre o mesmo contexto |

Na raiz do clone:

```bash
# Valida sem usar API
python3 -m jev_lab validate exemplos/skills-request.json

# Consulta real; requer chave e pode consumir créditos
python3 -m jev_lab ask exemplos/skills-request.json
```

Para comparar resultados com uma referência humana, siga [Experimentos](../../docs/08-experimentos.md). O avaliador em lote atual tem uma pergunta Choice como alvo; não calcula automaticamente a qualidade conjunta de todas as perguntas de um template composto.

**Estado:** templates reutilizáveis, sem conectores prontos de CRM, help desk ou orquestradores. Cada template contém dados fictícios; os resultados reais dependem do provedor e da avaliação no domínio de destino.
