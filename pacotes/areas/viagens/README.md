# Hospedagem × perfis de viajantes

Extrair uma vez os atributos de um anúncio e cruzá-los por regra com vários perfis.

**Integração:** Ao cadastrar ou atualizar um anúncio de hospedagem.

**Uso da saída:** Guardar as respostas do anúncio e cruzar com perfis por regra (`pacotes.cruzamento`). Atributos em revisão deixam o perfil em `revisar`; nada é reservado ou recomendado automaticamente.

## A ideia

Em vez de perguntar "este hotel serve para este viajante?" para cada par (anúncios × perfis chamadas), o Jev lê **só o anúncio** e responde perguntas fixas sobre ele. Uma regra determinística cruza essas respostas com a lista de exigências de cada perfil. Doze perfis custam o mesmo que um: a consulta é por anúncio.

Cada pergunta tem uma saída de insuficiência. No exemplo, o anúncio manda "entrar em contato com a central de reservas" para saber o cancelamento: a resposta esperada é `insuficiente`, e todo perfil que exige reembolso fica em `revisar`, nunca em `compativel`.

## Executar

```bash
# Exemplo simulado, sem rede
python3 -m pacotes.executar viagens

# Cruzamento com os 12 perfis fictícios; o preço vem do seu sistema, não do modelo
python3 -m pacotes.cruzamento viagens --preco 420

# Anúncio próprio em JSON; API real e consumo de créditos
python3 -m pacotes.executar viagens --state-file /caminho/anuncio.json --state-format json --live --provider openrouter
```

No backend, use `cruzar(request, avaliar_area('viagens', estado), perfis, preco=...)`. Configure `OPENROUTER_API_KEY` no backend; nenhuma chave deve entrar no contexto.

## Perguntas

| Identificador | Tipo | Alternativas |
|---|---|---|
| `decisao` | choice | Reembolso garantido: `dinheiro`, `credito_hotel`, `sem_reembolso`, `insuficiente`. |
| `chegada_madrugada` | choice | Aceita chegada depois da meia-noite: `atende`, `viola`, `insuficiente`. |
| `piscina_inclusa` | choice | Piscina sem custo adicional: `atende`, `viola`, `insuficiente`. |
| `trilha_inclusa` | choice | Trilha guiada incluída: `atende`, `viola`, `insuficiente`. |
| `entrada_sem_escada` | choice | Entrada sem escadas: `atende`, `viola`, `insuficiente`. |
| `piscina_acessivel` | choice | Piscina acessível para cadeira de rodas: `atende`, `viola`, `insuficiente`. |

## Regra de cruzamento

| Situação | Status do perfil |
|---|---|
| Algum requisito sugerido fora dos rótulos aceitos, ou preço acima do orçamento | `incompativel` |
| Nenhuma violação, mas algum requisito em revisão (insuficiente ou abaixo dos limiares) | `revisar` |
| Todos os requisitos sugeridos dentro dos rótulos aceitos | `compativel` |

Desejáveis não bloqueiam; só são listados quando sugeridos como `atende`. No exemplo com diária de R$ 420: 4 compatíveis, 5 incompatíveis e 3 em revisão.

## Arquivos e limites

- [request.json](request.json): perguntas reutilizáveis e anúncio fictício.
- [fixture.json](fixture.json): resposta inventada, não inferência medida.
- [perfis.json](perfis.json): doze perfis fictícios, com orçamento como dado estruturado.
- [pacote.json](pacote.json): respostas esperadas autorais para todas as perguntas, sem validação humana independente.

A decisão principal esperada é `insuficiente`. `incompativel` depende de uma sugestão do modelo e continua em observação: confirme antes de descartar uma opção para o viajante. Acessibilidade é um requisito de segurança; trate `atende` como indício a confirmar com o estabelecimento. O Jev lê apenas texto: fotos do anúncio não são avaliadas neste pacote.

Veja [lotes, retomada e avaliação por pergunta](../../../docs/11-fluxos-praticos.md). Não há conector com plataformas de reserva, coleta de dados ou execução de ações externas neste pacote.
