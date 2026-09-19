# Jev diretamente no Codex e Claude Code

Uma fonte portátil (`definition.md`) e duas variantes geradas: Codex e Claude Code. A skill consulta o Jev pelo OpenRouter como ferramenta do agente. Não muda o modelo principal da conversa.

## Usar nesta máquina

Instalada em:

- Codex: `~/.agents/skills/jev-decidir/`.
- Claude Code: `~/.claude/skills/jev-decidir/`.

No Codex:

```text
$jev-decidir Classifique este pedido entre suporte, cobrança e insuficiente:
Paguei duas vezes a mesma fatura.
```

No Claude Code:

```text
/jev-decidir Classifique este pedido entre suporte, cobrança e insuficiente:
Paguei duas vezes a mesma fatura.
```

O agente monta o JSON, consulta uma vez e apresenta a decisão e as métricas recebidas. Se a skill não aparecer na sessão já aberta, recarregue o catálogo de skills ou abra uma nova sessão.

## Instalar em outra máquina

Requer Python 3.10+, clone `inematds/jev` em `~/projetos/jev` (ou `JEV_LAB_DIR`) e `OPENROUTER_API_KEY` configurada no ambiente do processo. A skill não inclui credenciais nem uma cópia do cliente.

A partir desta pasta, copie a variante desejada, preservando o diretório inteiro:

```bash
mkdir -p ~/.agents/skills ~/.claude/skills
cp -Rn dist/codex/jev-decidir ~/.agents/skills/
cp -Rn dist/claude/jev-decidir ~/.claude/skills/
```

Esses comandos não substituem arquivos existentes. Para atualizar uma instalação existente, revise o que mudou e use o fluxo de instalação do polyskill.

## Executar o recurso sem o agente

```bash
# Demonstração offline, sem chave
python3 ~/.agents/skills/jev-decidir/scripts/decidir.py --demo atendimento

# Request completo salvo pelo integrador; consulta real
python3 ~/.agents/skills/jev-decidir/scripts/decidir.py /caminho/request.json --live
```

O mesmo script existe na variante Claude Code. Um caminho relativo do request é resolvido antes de mudar para o clone Jev. Não há shell intermediário nem chave nos argumentos.

## Manter

Edite `definition.md`, `scripts/` e `references/`; depois:

```bash
polyskill validate
polyskill build
polyskill install
```

Não edite os arquivos de `dist/` diretamente. As duas variantes foram validadas e os scripts instalados foram executados com um request fictício real pelo OpenRouter a partir de outro diretório. [Evidência](../../../reports/skills-smoke.json).

Isso verifica instalação e execução dos recursos. A seleção automática da skill e a qualidade do uso por cada agente dependem da sessão e não foram medidas como benchmark.
