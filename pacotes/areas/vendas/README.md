# Vendas e CRM

Qualificar oportunidades segundo critérios explícitos.

**Ponto de integração:** Acione após receber um formulário de contato. Acrescente ao contexto seu catálogo e critérios comerciais.

**Uso da saída:** Sugerir uma tarefa de demonstração no CRM; não enviar mensagens automaticamente.

## Executar

Na raiz do clone Jev:

```bash
# Demonstração sem rede nem chave
python3 -m pacotes.executar vendas

# Dados próprios em texto UTF-8; chamada real à API
python3 -m pacotes.executar vendas --state-file /caminho/entrada.txt --live
```

Para estado estruturado, use `--state-format json` com um arquivo JSON. Revise os dados antes de enviá-los ao provedor. Não cole chaves no contexto.

## Arquivos

- [request.json](request.json): contexto fictício, instruções e alternativas editáveis.
- [fixture.json](fixture.json): resposta inventada para demonstrar o fluxo; não é benchmark.
- [pacote.json](pacote.json): metadados, rótulo esperado e exigência de supervisão.

No exemplo, a classificação esperada é **demonstracao**. O valor de confidence da fixture é inventado. A alternativa `revisar` e as alternativas de insuficiência continuam sob revisão mesmo com confidence alta. Sugestões não executam ações por conta própria.

## Adaptar e avaliar

Troque o contexto e os critérios do request pelas regras reais da sua operação. Mantenha uma saída para revisão ou falta de informação. O modo offline serve somente ao request original; arquivos alterados exigem validação com uma nova referência, não o reaproveitamento silencioso da resposta inventada.

Monte um conjunto separado com exemplos claros, ambíguos, incompletos e fora do escopo. Compare com rótulos humanos antes de automatizar. Veja [integração nos sistemas](../../INTEGRACAO.md) e [experimentos](../../../docs/08-experimentos.md). Não há conector pronto para plataformas comerciais neste pacote.
