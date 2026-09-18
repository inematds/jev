# Jev Decision Lab

**v1.1.1** · Laboratório educacional de decisões estruturadas.

[Guia de uso](https://inematds.github.io/jev/guia/) · [Abrir laboratório](https://inematds.github.io/jev/app/) · [Curso](https://github.com/inematds/jev-curso)

Explore **dez aplicações**, veja respostas didáticas, ajuste o contexto, exporte requisições e calcule custos. O cliente Python permite validar contratos, consultar a API TypeSafe e avaliar uma baseline de regras em lote.

## Começar

```bash
git clone https://github.com/inematds/jev.git
cd jev
python3 -m jev_lab serve
```

Abra `http://127.0.0.1:8765`. Requer Python 3.10+; o núcleo usa apenas a biblioteca padrão.

A página pública usa **respostas autorais simuladas**, nunca apresentadas como inferência. Ao editar contexto/pergunta, a simulação é desativada; o JSON continua exportável. Casos sensíveis sempre pedem revisão.

## Comandos

```bash
# Validação local, sem inferência
python3 -m jev_lab validate exemplos/triagem-request.json

# Chamada real quando houver credencial
python3 -m jev_lab ask exemplos/triagem-request.json

# Baseline de regras; não é benchmark Jev
python3 -m jev_lab batch data/tickets-sinteticos.jsonl --out reports/baseline

# Testes sem chave
python3 -m unittest discover -s tests -v

# Empacotar somente os arquivos públicos
python3 scripts/build_site.py
```

O cliente carrega `TYPESAFE_API_KEY` do ambiente ou, em runtime, de `~/projetos/openpcbotv2/.env` e `~/projetos/wifi/.env`. Não copia a chave e não a envia ao navegador. Sem acesso ao provedor, exemplos, exportação, calculadora e baseline continuam disponíveis. A chamada real falha com mensagem explícita, sem inventar resposta.

O servidor escuta somente loopback, recusa origens externas e serve uma lista fechada de arquivos. É uma ferramenta local, não um backend público multiusuário. Não expor por túnel nem alterar a interface de bind sem adicionar autenticação e limites apropriados.

## Resultados verificados

- 14 testes automatizados do núcleo passaram, incluindo contrato, probabilidades inválidas, timeout/retries, credenciais e IDs duplicados.
- Navegador: dez exemplos, política, edição, JSON, tema persistido e custo verificados em desktop/mobile.
- Baseline lexical: **20/24 acertos (83,33%)**, macro-F1 **0,84235**, em dados fictícios. Consulte [métricas](reports/baseline/metrics.json).
- **Nenhuma inferência real Jev foi executada:** não havia credencial disponível. O adaptador HTTP foi testado com respostas controladas; qualidade/latência reais permanecem por medir.

Não há CRM, envio de mensagens, execução de agentes, pagamentos ou diagnóstico. As sugestões permanecem em observação. Não existe fallback LLM implementado; falhas levam a revisão.

## Documentação

[Análise crítica](docs/01-analise.md) · [Dez aplicações](docs/02-aplicacoes.md) · [Plano original](docs/03-plano-aplicacao.md) · [Protocolo de avaliação](docs/04-avaliacao.md) · [Custos](docs/05-custos.md) · [Fontes oficiais](fontes/README.md)

Materiais recebidos ficam somente locais e ignorados pelo Git. O build público inclui apenas `app/`, `guia/`, `capa/` e a entrada do site.
