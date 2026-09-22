# Jev Decision Lab

**Idiomas:** [Português](README.md) · [English](README.en.md) · [Español](README.es.md)

![Jev Decision Lab — mais recursos, uso simples: 20 casos práticos, experimentos e comparação](capa/novos-recursos-v1.2.1.png)

**v1.7.1** · Um laboratório para formular, testar e comparar decisões de IA, com uma interface simples e recursos avançados quando você precisar.

[Abrir laboratório](https://inematds.github.io/jev/app/) · [Guia de uso](https://inematds.github.io/jev/guia/) · [Curso em português](https://inematds.github.io/jev-curso/)

[Acervo Jev no Eventos INEMA](https://eventos.inema.pro/jev/) — projeto, curso e pacotes reunidos em uma página, com apresentação em português, inglês e espanhol.

**Referência oficial de modelos, preços, modalidades e limites:** https://docs.typesafe.ai/models

**Leia também: [Exageros, dúvidas e limites do Jev](docs/07-exageros-e-duvidas.md).** O documento separa capacidade documentada, hipótese, extrapolação e evidência ainda necessária.

## Leve para seu projeto

A pasta **[pacotes/](pacotes/README.md)** reúne **17 pacotes por área**, uma integração Python, a skill `jev-integrar` e receitas de uso. Comece offline com `python3 -m pacotes.executar atendimento`. Para seu backend, veja [como integrar Jev nos sistemas](pacotes/INTEGRACAO.md). Veja em cada pacote o que já funciona e o que ainda depende de integração.

## Novos fluxos práticos

Agora são **17 pacotes reutilizáveis**: os dez originais mais **caixa de entrada, comentários do YouTube, comunidades, reuniões, cortes por transcrição, notas e curadoria de feed**. Os novos pacotes combinam Choice, Noul e Score; suas fixtures são fictícias, sem benchmark real.

```bash
python3 -m pacotes.executar reunioes
python3 -m pacotes.qualidade reunioes
python3 -m pacotes.lote reunioes data/reunioes-eventos.jsonl
```

Os dois primeiros comandos demonstram o exemplo e suas métricas simuladas. O terceiro faz uma prévia sem API. Com `--live`, o executor processa JSONL, permite até quatro workers e retoma resultados salvos. A avaliação por pergunta mede acurácia, Brier ou erro de Score conforme o tipo. **[Instruções, integração e limites](docs/11-fluxos-praticos.md)**. Não há coleta de plataformas ou ações automáticas.

## Jev real pelo OpenRouter

Suporte a **`~typesafe/jev-latest`**, confirmado na Decisions API. Configure `OPENROUTER_API_KEY` no backend e execute:

```bash
python3 -m pacotes.executar atendimento --live --provider openrouter
```

Os dez pacotes originais foram testados com inferência real: dez respostas sem falha e dez classificações esperadas nos exemplos fictícios. Isso é um teste de integração, não benchmark independente. [Configuração e código para seu sistema](docs/10-openrouter.md) · [Relatório medido](reports/openrouter-smoke.json).

## Usar no Codex, Claude Code e openpcbotv3

- **Codex:** `$jev-decidir` seguido do contexto e das alternativas.
- **Claude Code:** `/jev-decidir` seguido do contexto e das alternativas.
- **openpcbotv3:** `/jev observar` compara rota, agente e skill; `/jev` mostra o resultado, `/jev off` desliga. Integração nativa via gateway, com orçamento e custos registrados.

[Instalação e exemplos da skill](pacotes/skills/jev-decidir/README.md) · [Integração no bot](https://github.com/inematds/openpcbotv3/blob/main/docs/JEV.md). A consulta direta usa o cliente deste repo; o bot conserva seu próprio gateway e seu roteador em modo de observação.

## Uma porta só para as consultas: jev-gw

Quando a consulta ao Jev sai de vários pontos do mesmo sistema, o **[jev-gw](https://github.com/inematds/jev-gw)** concentra tudo numa porta: teto de gasto diário conferido antes de cada consulta, cache por pedido idêntico, registro de custo e latência, e falha conservadora — Jev fora do ar, chave errada ou teto estourado devolvem revisão em vez de quebrar quem chamou. Biblioteca Python, serviço HTTP e CLI, só biblioteca padrão. Usa o cliente deste repositório, vendorizado.

[Guia](https://inematds.github.io/jev-gw/guia/) · [Arquitetura](https://github.com/inematds/jev-gw/blob/main/ARQUITETURA.md)

## Comece em um minuto

No site público, escolha um dos **20 casos autorais**, examine contexto e critérios e explore a resposta didática. Você pode editar as perguntas, importar/exportar JSON e estimar custos sem cadastrar uma chave.

Para abrir no computador:

```bash
git clone https://github.com/inematds/jev.git
cd jev
python3 -m jev_lab serve
```

Abra `http://127.0.0.1:8765`. Requer Python 3.10+; o núcleo usa apenas a biblioteca padrão. Não precisa instalar um framework, banco ou serviço de filas.

## O que está disponível

| Recurso | O que você faz |
|---|---|
| 20 casos com busca | Explora atendimento, evidências, agentes, skills, código, logs e mais |
| Choice, Noul e Score | Escolhe alternativas, mede probabilidade de sim ou usa rubricas ordenadas |
| Várias perguntas no mesmo contexto | Separa fila, urgência, suficiência e intenções |
| Contexto textual ou JSON | Representa documentos, catálogos e estados estruturados |
| Importação e exportação | Leva requisições para a CLI e salva resultados com procedência |
| Política didática | Observa como limiares e abstenção mudam a revisão; nenhuma ação externa é executada |
| Custo completo estimado | Acrescenta fallback, revisão humana e infraestrutura ao custo de entrada |
| Experimentos em lote | Executa regras, Jev direto, híbrido ou replay em dataset rotulado |
| Comparação e métricas | Examina macro-F1, confusão, cobertura, precisão aceita, Brier/ECE, latência e custo desconhecido |
| Leitor de relatórios | Abre report.json no navegador e identifica erros para investigar |

As respostas do site são **simulações autorais**, claramente identificadas. Editar contexto, tipo, opções ou pergunta desativa a fixture anterior. A página pública não consulta uma API; no servidor local, a consulta real precisa de chave.

## Os 20 casos

Os dez iniciais: afirmações, atendimento, contratos, mudanças em e-mails, modelos, verificação de etapas, agentes, navegador por candidatos, revisão clínica fictícia e alertas financeiros fictícios.

Os dez adicionais: **skills, qualidade de comentários, filtro de evidências, triagem composta, intenções simultâneas, datas por candidatos, gravidade de logs, dados pessoais minimizados, assunto versus intenção e revisão de diff**.

Cada caso possui estado, perguntas, fixture, explicação e próximo passo. Casos de ferramentas/navegador sugerem candidatos; não controlam agentes, navegadores ou dispositivos. Os exemplos sensíveis permanecem supervisionados.

## Terminal: do exemplo ao experimento

```bash
# Listar e exportar um exemplo
python3 -m jev_lab cases
python3 -m jev_lab cases --id triagem-composta --out exemplos/minha-requisicao.json

# Verificar contrato, sem consumir API
python3 -m jev_lab validate exemplos/triagem-composta-request.json

# Consultar Jev quando houver acesso
python3 -m jev_lab ask exemplos/triagem-composta-request.json

# Experimento reproduzível, sem chave
python3 -m jev_lab experiment data/tickets-sinteticos.jsonl --out runs/regras

# Experimento com Jev real
python3 -m jev_lab experiment data/tickets-sinteticos.jsonl --provider jev --out runs/jev

# Comparar duas execuções do mesmo dataset
python3 -m jev_lab compare runs/regras/report.json runs/jev/report.json
```

O comando anterior `batch` continua disponível. Para templates de outras tarefas, repetibilidade, híbrido e importação de resultados de LLM, veja **[Experimentos reproduzíveis](docs/08-experimentos.md)**. Não há adaptador LLM ao vivo: a comparação externa usa replay com hash da requisição e origem declarada.

## Configuração local

O cliente usa `OPENROUTER_API_KEY` com OpenRouter e `TYPESAFE_API_KEY` com TypeSafe direta. Carrega a chave do ambiente ou, em runtime, de `~/projetos/openpcbotv2/.env` e `~/projetos/wifi/.env`. Não copia a chave e não a envia ao navegador. Sem acesso, exemplos, exportação, calculadora e regras continuam funcionando; chamadas reais registram falha explícita.

O servidor escuta somente loopback, valida origem e serve arquivos permitidos. Serializa as consultas ao provedor. Não é um backend público multiusuário. A aplicação aceita descrições textuais, até 30 perguntas e 100 KB por payload; esses dois últimos limites são locais, não limites anunciados do Jev. Score usa 2–10 níveis e exige legend correspondente na resposta.

## Evidência e limites

- A baseline foi reexecutada: **20/24 acertos (83,33%)**, macro-F1 **0,84235**, em tickets fictícios. [Relatório de regras](reports/experimento-regras/report.json).
- Há um [replay didático](data/replay-didatico.jsonl) com erros intencionais e custo/latência desconhecidos. A [comparação de exemplo](reports/comparacao-didatica.json) é um exercício, não benchmark Jev.
- Os testes verificam contratos, orçamento, falhas, duplicatas, replay, repetibilidade e políticas. O navegador verifica os 20 casos, edição, tipos, importação/exportação e leitura de relatório.
- **Há teste de integração real pelo OpenRouter, mas não benchmark independente.** A suíte automatizada usa respostas controladas; o relatório separado registra as dez consultas reais. Qualidade em português e calibração ainda precisam de avaliação com referência humana em dados independentes.
- Não há envio de mensagens, pagamentos, merge, diagnóstico ou execução de ferramentas. A classificação não concede permissão.

## Documentação

- [Usar Jev pelo OpenRouter](docs/10-openrouter.md)

- [Exageros, dúvidas e limites](docs/07-exageros-e-duvidas.md)
- [Experimentos e formato de replay](docs/08-experimentos.md)
- [O que foi agregado e o que depende de evidência](docs/09-evolucao.md)
- [Análise conceitual](docs/01-analise.md) · [Dez aplicações iniciais](docs/02-aplicacoes.md)
- [Plano original](docs/03-plano-aplicacao.md) · [Protocolo de avaliação](docs/04-avaliacao.md) · [Custos](docs/05-custos.md)
- [Curso: 36 aulas e 12 laboratórios](https://inematds.github.io/jev-curso/)
- [Modelos oficiais](https://docs.typesafe.ai/models) · [API oficial](https://docs.typesafe.ai/api)

## Desenvolvimento e publicação

```bash
python3 -m unittest discover -s tests -v
python3 scripts/build_site.py
```

Os testes de navegador em `tests/browser.cjs` usam Playwright somente no desenvolvimento. Instale-o no ambiente de testes com `npm install --no-save --package-lock=false playwright` e `npx playwright install chromium`; a aplicação não precisa dessa dependência. `BASE_URL`, `GUIDE_URL` e `SCREENSHOT_DIR` permitem apontar o teste para os servidores e diretório de capturas escolhidos. O build publica uma lista explícita: `app/`, `guia/`, `capa/` e a entrada do site. Documentação pública fica no repositório.

**Transcrições e materiais recebidos permanecem somente locais**, ignorados pelo Git e excluídos do build. Relatórios operacionais vão em `runs/`, também ignorada. Os documentos públicos são autorais, com referências oficiais. Confira o [changelog](CHANGELOG.md).

## Roteiro de piloto e composição

[Planeje uma decisão, escreva casos de fronteira e combine rubricas Score](docs/12-piloto-e-composicao.md). A função `pacotes.composicao.compor` valida os dados e calcula um índice ponderado; não representa confiança nem autoriza ações. [Curso HTML v2](https://inematds.github.io/jev-curso/) com 36 aulas, progresso e roteiro pessoal.

## Próximos passos e alternativa local

[Pendências confirmadas](tasks/current.md#pendências-confirmadas-em-21092026) · [Análise do Laya para comparação com Jev e piloto no bot v3](docs/13-analise-laya.md). A integração Laya é proposta, ainda não implementada.

### Referências Laya

Laya é um candidato local para o piloto comparativo. A análise e as referências já estão disponíveis; o adaptador no Jev e a integração no bot continuam pendentes.

[Laya INEMA](https://github.com/inematds/laya) · [Código original](https://github.com/NandhaKishorM/laya) · [Modelos e model card](https://huggingface.co/convaiinnovations/laya) · [Laya no Eventos](https://eventos.inema.pro/jev/#laya)
