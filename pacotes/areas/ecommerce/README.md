# Comércio eletrônico

Organizar solicitações de pós-venda.

**Ponto de integração:** Avalie o ticket com os dados de pedido estritamente necessários.

**Uso da saída:** Sugerir fila logística; estorno e troca dependem da política da loja e de autorização.

## Executar

Na raiz do clone Jev:

```bash
# Demonstração sem rede nem chave
python3 -m pacotes.executar ecommerce

# Dados próprios em texto UTF-8; chamada real à API
python3 -m pacotes.executar ecommerce --state-file /caminho/entrada.txt --live --provider openrouter
```

Para estado estruturado, use `--state-format json` com um arquivo JSON. Para a consulta acima, configure `OPENROUTER_API_KEY` no backend. Revise os dados antes de enviá-los ao provedor. Não cole chaves no contexto.

## Arquivos

- [request.json](request.json): contexto fictício, instruções e alternativas editáveis.
- [fixture.json](fixture.json): resposta inventada para demonstrar o fluxo; não é benchmark.
- [pacote.json](pacote.json): metadados, rótulo esperado e exigência de supervisão.

No exemplo, a classificação esperada é **atraso**. O valor de confidence da fixture é inventado. A alternativa `revisar` e as alternativas de insuficiência continuam sob revisão mesmo com confidence alta. Sugestões não executam ações por conta própria.

## Adaptar e avaliar

Troque o contexto e os critérios do request pelas regras reais da sua operação. Mantenha uma saída para revisão ou falta de informação. O modo offline serve somente ao request original; arquivos alterados exigem validação com uma nova referência, não o reaproveitamento silencioso da resposta inventada.

Monte um conjunto separado com exemplos claros, ambíguos, incompletos e fora do escopo. Compare com rótulos humanos antes de automatizar. Veja [integração nos sistemas](../../INTEGRACAO.md) e [experimentos](../../../docs/08-experimentos.md). Não há conector pronto para plataformas comerciais neste pacote.
