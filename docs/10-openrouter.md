# Jev pelo OpenRouter

Integração confirmada em 19/09/2026 com o alias `~typesafe/jev-latest`. A chamada retornou o modelo `typesafe/jev-1.13-20260917`.

## Endpoint e autenticação

- POST `https://openrouter.ai/api/alpha/decisions`
- Modelo: `~typesafe/jev-latest`
- Autenticação: Bearer com `OPENROUTER_API_KEY`.
- Corpo: `model`, `state` e `questions`; resposta tipada com `answers` e `usage`.

Esta rota é a Decisions API, atualmente alpha. Não use `/chat/completions` para os requests destes pacotes. A documentação específica do modelo confirma a rota; exemplos genéricos de chat não substituem o contrato de decisões.

Referências oficiais: [API do modelo](https://openrouter.ai/~typesafe/jev-latest/api), [especificação OpenAPI](https://openrouter.ai/openapi.json), [Jev 1.13](https://openrouter.ai/typesafe/jev-1.13/).

## Nos pacotes

```bash
python3 -m pacotes.executar atendimento --live --provider openrouter
python3 -m pacotes.executar documentos --state-file entrada.json --state-format json --live --provider openrouter
```

A segunda chamada exige que `entrada.json` contenha o contexto completo, incluindo o checklist necessário. Sem `--live`, continua sendo demonstração simulada e não há consumo de API.

## No seu código

Com o clone no caminho de importação do backend:

```python
from pacotes.integracao import avaliar_area

resultado = avaliar_area(
    'atendimento',
    'Paguei duas vezes a mesma fatura.',
    provider='openrouter',
)

if resultado['action'] == 'review':
    print('Revisar', resultado['error'])
else:
    print(resultado['response']['answers']['decisao']['choice'])
```

A função retorna uma sugestão ou revisão. Seu sistema conserva a autorização para executar qualquer ação. A chave fica no backend.

## CLI, experimentos e servidor local

```bash
python3 -m jev_lab ask exemplos/triagem-composta-request.json --provider openrouter

JEV_PROVIDER=openrouter python3 -m jev_lab experiment data/tickets-sinteticos.jsonl --provider jev --out runs/openrouter

JEV_PROVIDER=openrouter python3 -m jev_lab serve
```

No comando `experiment`, `--provider jev` seleciona a estratégia de inferência; `JEV_PROVIDER` escolhe o transporte. Os exemplos do site continuam simulados até clicar na consulta local. A página pública não recebe credenciais.

## Seleção e credenciais

O parâmetro explícito `provider` tem precedência, seguido por `JEV_PROVIDER`. Sem esses valores, um identificador `typesafe/...` ou `~typesafe/...` seleciona OpenRouter; os identificadores nativos continuam usando TypeSafe direta.

Com OpenRouter selecionado, o modelo nativo conhecido `jev-1.13.0` é convertido para `~typesafe/jev-latest` no envio, preservando o request original. Um ID OpenRouter específico é mantido. Não há fallback silencioso entre provedores. Para experimentos que exigem uma versão fixa, use um identificador específico disponível e registre o modelo efetivamente retornado; `latest` pode mudar.

`OPENROUTER_API_KEY` é carregada em runtime do ambiente ou dos arquivos autorizados `~/projetos/openpcbotv2/.env` e `~/projetos/wifi/.env`. TypeSafe direta continua usando `TYPESAFE_API_KEY`. Nenhuma chave foi copiada para este repo.

## Evidência observada

- Uma consulta combinada confirmou Choice, Noul e Score, inclusive `legend` e validação de probabilidades.
- Os dez pacotes foram consultados uma vez cada, usando os contextos fictícios publicados.
- Dez respostas recebidas sem falha; dez classificações coincidiram com os rótulos esperados.
- Custo total declarado em `usage.cost` para as dez áreas: **US$ 0,000184968**. Esse total não inclui as chamadas de diagnóstico anteriores.
- [Relatório das dez áreas](../reports/openrouter-smoke.json).

O cliente preserva `usage.cost` quando informado, sem deduzi-lo de texto gerado. Retentativas podem ter custos não observados; o avaliador mantém custo desconhecido nesses casos.

Isso comprova que a integração funcionou para os exemplos. Não é amostra independente, teste de robustez, medição de calibração nem estimativa de qualidade em produção. Os exemplos e critérios já eram conhecidos, e a latência inclui a rede local.

O catálogo genérico `/api/v1/models` não listou Jev na consulta desta sessão, apesar da página oficial e das chamadas à rota alpha funcionarem. A ausência naquela listagem não deve ser usada isoladamente como prova de indisponibilidade.

Os sete pacotes adicionados na v1.6.1 usam o mesmo cliente, mas não fazem parte do relatório de dez consultas acima. Foram verificados com fixtures e testes controlados. [Novos fluxos](11-fluxos-praticos.md).
