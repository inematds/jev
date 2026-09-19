# Jev Decision Lab

**Languages:** [Português](README.md) · [English](README.en.md) · [Español](README.es.md)

![Jev Decision Lab — more features, simple to use: 20 practical cases, experiments and comparisons](capa/novos-recursos-v1.2.1.png)

**v1.5.1** · A lab for defining, testing and comparing AI decisions, with a simple interface and advanced features when you need them.

[Open the lab](https://inematds.github.io/jev/app/) · [User guide](https://inematds.github.io/jev/guia/) · [Course in Portuguese](https://github.com/inematds/jev-curso)

This README is translated into English. The interface, linked project documentation, course and example content remain in Portuguese. Commands, paths and identifiers below retain their original spelling so you can run them as written.

**Official reference for models, pricing, modalities and limits:** https://docs.typesafe.ai/models

**Also read: [Jev: overstatements, open questions and limitations](docs/07-exageros-e-duvidas.md).** This document distinguishes documented capabilities, hypotheses, extrapolations and evidence still needed.

## Bring it into your project

The **[pacotes/](pacotes/README.md)** directory contains **ten packages by activity**, a Python integration, the `jev-integrar` skill and usage recipes. Start offline with `python3 -m pacotes.executar atendimento`. For your backend, see [how to integrate Jev into your systems](pacotes/INTEGRACAO.md). Each package explains what already works and what still requires integration.

## Real Jev inference through OpenRouter

Support for **`~typesafe/jev-latest`**, confirmed through the Decisions API. Configure `OPENROUTER_API_KEY` in your backend and run:

```bash
python3 -m pacotes.executar atendimento --live --provider openrouter
```

All ten packages were tested with real inference: ten successful responses and ten expected classifications on fictional examples. This is an integration test, not an independent benchmark. [Setup and code for your system](docs/10-openrouter.md) · [Measured report](reports/openrouter-smoke.json).

## Use it in Codex, Claude Code and openpcbotv3

- **Codex:** `$jev-decidir` followed by the context and alternatives.
- **Claude Code:** `/jev-decidir` followed by the context and alternatives.
- **openpcbotv3:** `/jev observar` compares route, agent and skill; `/jev` shows the result and `/jev off` disables observation. Native integration through the gateway, with budget checks and recorded costs.

[Skill installation and examples](pacotes/skills/jev-decidir/README.md) · [Bot integration](https://github.com/inematds/openpcbotv3/blob/main/docs/JEV.md). Direct queries use this repository's client; the bot retains its own gateway and router, with Jev operating in observation mode.

## Get started in one minute

On the public site, choose one of **20 original cases**, inspect the context and criteria, and explore the educational response. You can edit questions, import/export JSON and estimate costs without providing an API key.

To run it on your computer:

```bash
git clone https://github.com/inematds/jev.git
cd jev
python3 -m jev_lab serve
```

Open `http://127.0.0.1:8765`. Requires Python 3.10+; the core uses only the standard library. No framework, database or queue service installation is required.

## Available features

| Feature | What you can do |
|---|---|
| 20 searchable cases | Explore support, evidence, agents, skills, code, logs and more |
| Choice, Noul and Score | Choose alternatives, measure the probability of yes or use ordered rubrics |
| Multiple questions over the same context | Separate queue, urgency, sufficiency and intents |
| Text or JSON context | Represent documents, catalogs and structured states |
| Import and export | Take requests to the CLI and save results with provenance |
| Educational policy | Observe how thresholds and abstention affect review; no external action is executed |
| Estimated total cost | Add fallback, human review and infrastructure to input cost |
| Batch experiments | Run rules, direct Jev, hybrid or replay on a labeled dataset |
| Comparison and metrics | Inspect macro-F1, confusion, coverage, precision on accepted predictions, Brier/ECE, latency and unknown cost |
| Report viewer | Open report.json in the browser and identify errors to investigate |

Responses on the website are **original simulations**, clearly labeled. Editing the context, type, options or question disables the previous fixture. The public page does not call an API; real queries on the local server require an API key.

## The 20 cases

The initial ten: claims, customer support, contracts, changes in email threads, models, step verification, agents, browser actions selected from candidates, fictional clinical review and fictional financial alerts.

The additional ten: **skills, comment quality, evidence filtering, compound triage, simultaneous intents, dates selected from candidates, log severity, minimized personal data, topic versus intent and diff review**.

Each case includes state, questions, a fixture, an explanation and a next step. Tool/browser cases suggest candidates; they do not control agents, browsers or devices. Sensitive examples remain supervised.

## Terminal: from example to experiment

```bash
# List and export an example
python3 -m jev_lab cases
python3 -m jev_lab cases --id triagem-composta --out exemplos/minha-requisicao.json

# Validate the contract without making an API call
python3 -m jev_lab validate exemplos/triagem-composta-request.json

# Query Jev when access is available
python3 -m jev_lab ask exemplos/triagem-composta-request.json

# Reproducible experiment without an API key
python3 -m jev_lab experiment data/tickets-sinteticos.jsonl --out runs/regras

# Experiment with real Jev inference
python3 -m jev_lab experiment data/tickets-sinteticos.jsonl --provider jev --out runs/jev

# Compare two runs on the same dataset
python3 -m jev_lab compare runs/regras/report.json runs/jev/report.json
```

The earlier `batch` command remains available. For templates for other tasks, repeatability, hybrid experiments and importing LLM results, see **[Reproducible experiments](docs/08-experimentos.md)**. There is no live LLM adapter: external comparisons use replay with a request hash and declared provenance.

## Local configuration

The client uses `OPENROUTER_API_KEY` for OpenRouter and `TYPESAFE_API_KEY` for direct TypeSafe access. It loads the key from the environment or, at runtime, from `~/projetos/openpcbotv2/.env` and `~/projetos/wifi/.env`. It does not copy the key or send it to the browser. Without access, examples, export, the calculator and rules still work; real calls report an explicit failure.

The server listens only on loopback, validates origins and serves allowlisted files. It serializes provider queries. It is not a public multiuser backend. The application accepts textual descriptions, up to 30 questions and 100 KB per payload; these last two limits are local, not advertised Jev limits. Score uses 2–10 levels and requires a matching `legend` in the response.

## Evidence and limitations

- The baseline was rerun: **20/24 correct (83.33%)**, macro-F1 **0.84235**, on fictional tickets. [Rules report](reports/experimento-regras/report.json).
- An [educational replay](data/replay-didatico.jsonl) includes intentional errors and unknown cost/latency. The [example comparison](reports/comparacao-didatica.json) is an exercise, not a Jev benchmark.
- Tests check contracts, budgets, failures, duplicates, replay, repeatability and policies. Browser checks cover the 20 cases, editing, types, import/export and report viewing.
- **There is a real integration test through OpenRouter, but no independent benchmark.** The automated suite uses controlled responses; a separate report records the ten real queries. Portuguese-language quality and calibration still need evaluation against human reference labels on independent data.
- There is no message sending, payment, merge, diagnosis or tool execution. Classification does not grant permission.

## Documentation

- [Use Jev through OpenRouter](docs/10-openrouter.md)
- [Overstatements, open questions and limitations](docs/07-exageros-e-duvidas.md)
- [Experiments and replay format](docs/08-experimentos.md)
- [What was added and what still needs evidence](docs/09-evolucao.md)
- [Conceptual analysis](docs/01-analise.md) · [Ten initial applications](docs/02-aplicacoes.md)
- [Original plan](docs/03-plano-aplicacao.md) · [Evaluation protocol](docs/04-avaliacao.md) · [Costs](docs/05-custos.md)
- [Course: 36 lessons and 12 labs](https://github.com/inematds/jev-curso)
- [Official models](https://docs.typesafe.ai/models) · [Official API](https://docs.typesafe.ai/api)

## Development and publication

```bash
python3 -m unittest discover -s tests -v
python3 scripts/build_site.py
```

Browser tests in `tests/browser.cjs` use Playwright only during development. Install it in your test environment with `npm install --no-save --package-lock=false playwright` and `npx playwright install chromium`; the application does not require this dependency. `BASE_URL`, `GUIDE_URL` and `SCREENSHOT_DIR` let you select the servers and screenshot directory for the test. The build publishes an explicit list: `app/`, `guia/`, `capa/` and the site entry point. Public documentation stays in the repository.

**Transcripts and supplied materials remain local only**, ignored by Git and excluded from the build. Operational reports go into `runs/`, also ignored. Public documents are original work with official references. See the [changelog](CHANGELOG.md).
