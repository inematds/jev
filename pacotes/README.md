# Pacotes para levar ao seu projeto

Comece pelo seu objetivo. Esta pasta reúne os primeiros recursos de integração do Jev Decision Lab, reaproveitando o núcleo `jev_lab/`.

| Quero… | Pacote | Disponível agora |
|---|---|---|
| Usar decisões no meu código | [Python](python/README.md) | Função de integração e exemplo executável offline ou com API |
| Pedir ao meu agente para integrar Jev | [Skill jev-integrar](skills/jev-integrar/SKILL.md) | Instruções copiáveis para o agente trabalhar no projeto de destino |
| Começar por uma atividade | [Dez áreas](areas/README.md) | Dez pacotes executáveis com templates, fixture e instruções |
| Integrar no meu backend | [Integração nos sistemas](INTEGRACAO.md) | Exemplo Python e contrato de subprocesso para outros sistemas |
| Adaptar um fluxo de trabalho | [Receitas](receitas/README.md) | Triagem, seleção de skills, evidências e revisão de código |

## Experimente sem chave

Na raiz do repositório, execute:

```bash
python3 -m pacotes.executar atendimento
```

A execução usa uma resposta simulada identificada como tal. Não acessa a rede. Para integrar textos próprios, veja o pacote Python.

## Como estão organizados

```text
pacotes/
├── areas/                   Dez aplicações com exemplos executáveis
├── integracao.py            Função avaliar_area para seu backend
├── executar.py              Executor compartilhado
├── python/                  Exemplo que importa o cliente existente
├── skills/jev-integrar/     Instruções para o agente de programação
└── receitas/                Aplicações e templates já existentes
```

O cliente continua em [`jev_lab/`](../jev_lab/); os templates continuam em [`exemplos/`](../exemplos/). Assim, correções ficam em uma fonte única.

**Limites desta primeira entrega:** não existe distribuição no PyPI, instalador universal ou conector pronto para n8n. A skill orienta a integração, mas não executa outras skills. A inferência real funciona via OpenRouter ou TypeSafe direta. Há dez consultas reais de integração, sem benchmark independente. Veja [OpenRouter](../docs/10-openrouter.md). Publicação e instalação de pacotes não concedem permissão para executar ações externas.
