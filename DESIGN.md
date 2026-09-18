---
name: Jev Decision Lab — INEMA
description: Laboratório educacional e guia de uso em dark âmbar com tema claro alternativo.
colors:
  app-bg: "#101217"
  app-panel: "#191d24"
  app-text: "#eef0f4"
  app-muted: "#b0b7c2"
  app-line: "#363d48"
  app-accent: "#edb354"
  app-button-text: "#211803"
  app-sky: "#66caf3"
  app-light-bg: "#f6f5f1"
  app-light-panel: "#fff"
  app-light-text: "#1b2330"
  app-light-muted: "#515d6c"
  app-light-line: "#cbd0d5"
  app-light-accent: "#875500"
  app-light-button-text: "#fff"
  app-light-sky: "#03658c"
  guide-bg: "#0c0c10"
  guide-bg2: "#14141b"
  guide-card: "#16161e"
  guide-line: "#272730"
  guide-text: "#e9e9ee"
  guide-muted: "#9a9aa6"
  guide-amber: "#E2A23B"
  guide-amber2: "#f0c070"
  guide-sky: "#38bdf8"
  guide-pro: "#cbd5e1"
  guide-button-text: "#1a1206"
  guide-light-bg: "#f6f7f9"
  guide-light-bg2: "#eceef2"
  guide-light-card: "#ffffff"
  guide-light-line: "#e1e3ea"
  guide-light-text: "#1a1a22"
  guide-light-muted: "#5b5b68"
  guide-light-amber: "#875500"
  guide-light-amber2: "#a16207"
  guide-light-sky: "#0369a1"
  guide-light-pro: "#b45309"
typography:
  app-display:
    fontFamily: "system-ui, sans-serif"
    fontSize: "clamp(2rem,4vw,3.2rem)"
    lineHeight: 1.15
    letterSpacing: "-.03em"
  app-body:
    fontFamily: "system-ui, sans-serif"
    fontSize: "17px"
    lineHeight: 1.65
  app-code:
    fontFamily: "monospace"
    fontSize: "14px"
    lineHeight: 1.6
  guide-display:
    fontFamily: "Sora, sans-serif"
    fontSize: "clamp(2.2rem,5vw,3.5rem)"
    fontWeight: 800
    lineHeight: 1.15
    letterSpacing: "-.025em"
  guide-body:
    fontFamily: "Inter, system-ui, sans-serif"
    fontSize: "16px"
    lineHeight: 1.65
  guide-code:
    fontFamily: '"JetBrains Mono", monospace'
    fontSize: ".86rem"
    lineHeight: 1.6
rounded:
  app-control: "7px"
  app-notice: "8px"
  guide-button: "10px"
  guide-code: "12px"
  guide-card: "14px"
  guide-hero: "16px"
  guide-pill: "999px"
spacing:
  app-action-gap: "10px"
  app-field-padding: "14px"
  guide-grid-gap: "16px"
  guide-card-padding: "20px"
components:
  app-button-primary:
    backgroundColor: "{colors.app-accent}"
    textColor: "{colors.app-button-text}"
    rounded: "{rounded.app-control}"
    padding: ".65rem 1rem"
  app-button-primary-light:
    backgroundColor: "{colors.app-light-accent}"
    textColor: "{colors.app-light-button-text}"
    rounded: "{rounded.app-control}"
    padding: ".65rem 1rem"
  guide-button-primary:
    backgroundColor: "{colors.guide-amber}"
    textColor: "{colors.guide-button-text}"
    rounded: "{rounded.guide-button}"
    padding: ".6em 1.05em"
  guide-card:
    backgroundColor: "{colors.guide-card}"
    textColor: "{colors.guide-text}"
    rounded: "{rounded.guide-card}"
    padding: "20px"
---

# Design System: Jev Decision Lab

## Overview

O mundo visual estabelecido é o padrão INEMA dark âmbar, com tema claro alternativo e identificação INEMA.CLUB em azul. Esta documentação registra o código existente em `app/app.css`, `app/index.html` e `guia/index.html`; não representa aprovação estética de uma proposta nova.

O aplicativo usa o modo **Operate**: navegação por casos, edição e resultado na mesma área de trabalho. O guia usa **Read/Persuade**: apresentação ilustrada, explicação e passos de instalação. Essa diferença de composição preserva a identidade compartilhada sem substituir o template do guia pela interface operacional.

Características recorrentes: fundos escuros, superfícies delimitadas por bordas, âmbar nas ações e tema claro explícito. O caráter educacional permanece visível nos avisos de simulação e nos rótulos de resultados.

## Colors

O frontmatter contém os valores normativos extraídos, separados por superfície e tema. No CSS, a classe `light` no `body` troca os papéis sem mudar a estrutura.

- **Primária:** âmbar orienta ações, links e destaques. No app, o botão principal troca fundo e texto no tema claro. No guia, o preenchimento dos botões e números dos passos conserva o âmbar original através de `--amb-fill`, enquanto links usam o âmbar escuro do tema claro.
- **Secundária:** azul identifica INEMA.CLUB. O link PRO tem cor própria no guia.
- **Neutras:** fundo, painel/cartão, texto, texto secundário e bordas têm tokens distintos. O guia acrescenta uma segunda superfície de fundo.

A última declaração de âmbar claro no guia é a efetiva; preservar a cascata ao editar. Não inferir estados de erro ou sucesso pela cor: a interface informa estados com texto.

## Typography

O app usa a pilha de sistema em títulos e corpo; código usa monoespaçada. Seu título principal tem largura máxima de 22 caracteres, títulos de seção usam 1,5rem e parágrafos têm limite de 78 caracteres.

O guia combina Sora para títulos e botões, Inter para leitura e JetBrains Mono para código, com fallbacks declarados. As fontes do guia são carregadas pelo Google Fonts. Títulos de seção variam entre 1,5rem e 2,1rem; a abertura usa o display do frontmatter. O texto de apresentação fica em 1,18rem com limite de 34 caracteres e subtítulos de seção em até 62 caracteres.

A hierarquia vem de tamanho, peso e espaço. Conteúdo técnico mantém fonte monoespaçada e rolagem horizontal quando necessário.

## Layout

No app, o cabeçalho tem limite de 1440px e a área principal de 1380px, com recuo horizontal de 32px. A área de trabalho combina coluna de casos de 245px e editor flexível, separados por 42px. A calculadora dispõe quatro colunas. Abaixo de 800px, a área passa a uma coluna, os casos e a calculadora usam duas colunas, o recuo diminui para 20px e os botões podem ocupar a linha disponível.

No guia, o conteúdo tem largura máxima de 1160px e recuo de 22px. O hero tem duas colunas proporcionais, intervalo de 40px e recuo vertical de 74px; abaixo de 780px passa a uma coluna com 48px verticais. Seções têm 62px verticais. Grades usam intervalo de 16px, reduzem a duas colunas abaixo de 820px e uma abaixo de 540px. Os links de seção da navegação são ocultados abaixo de 760px; os demais controles quebram linha.

Passos do guia reservam 46px para o número e deixam o texto encolher com `minmax(0,1fr)`. Blocos de código possuem rolagem própria. Esses comportamentos protegem a leitura em telas estreitas.

## Elevation & Depth

O app é plano: painéis, bordas e mudanças tonais separam regiões, sem sombras decorativas. O guia preserva o brilho radial âmbar do hero e a sombra da imagem principal (`0 30px 80px -30px #000`). A navegação fixa do guia usa desfoque de 12px e fundo translúcido no escuro; o tema claro aplica fundo sólido. Cartões permanecem sem sombra.

## Shapes

Controles do app são discretamente arredondados; avisos e código usam o raio de aviso. No guia, botões, código, cartões e imagem principal possuem raios progressivamente maiores conforme o frontmatter. Etapas do fluxo e etiquetas do rodapé usam formato de cápsula. Bordas finas de 1px delimitam controles e superfícies.

## Components

- **Botões do app:** principal em âmbar e demais em superfície de painel. Hover destaca a borda em âmbar. Estado desabilitado reduz a opacidade para 0,5 e muda o cursor. Ações quebram linha quando falta espaço.
- **Seleção de caso:** lista de botões alinhados à esquerda. `aria-current=true` aplica painel, borda, texto âmbar e peso 700; o estado também é programático.
- **Campos:** rótulos associados, fundo de painel, borda e preenchimento de 14px. Textareas permitem redimensionamento vertical. Dicas explicam a consequência da edição. Não há um componente visual separado de erro de campo documentado no CSS atual.
- **Resultado:** região inicialmente oculta, barras âmbar com rótulo e valor textual, controle de limiar e aviso de decisão. O status tem `role=status` e `aria-live=polite`. A consulta local permanece oculta até ser disponibilizada pelo ambiente.
- **Requisição:** expansão nativa com `details`/`summary` e JSON monoespaçado em bloco rolável.
- **Navegação e tema:** o app apresenta links e botão textual de tema; o guia mantém navegação fixa e botão com ícone e nome acessível. Os dois oferecem o tema claro alternativo.
- **Guia:** cartões de conteúdo, botões principal/secundário, etapas numeradas, fluxo em cápsulas e linhas de roadmap seguem o template existente. Não há diálogo modal implementado.

Acessibilidade presente: idioma pt-BR, títulos estruturados, rótulos, texto alternativo na imagem do guia e foco visível âmbar de 3px com afastamento de 4px. O app acrescenta atalho para pular ao laboratório e nomes para navegações. Ambos respeitam preferência de movimento reduzido ao tratar rolagem; não há animação necessária para operar. Estes são recursos observados, não uma declaração de conformidade integral.

## Do's and Don'ts

- **Do** preservar os pares de tokens escuro/claro e verificar ambos após alterações.
- **Do** manter contexto, ações e resultado próximos no app, com avisos textuais distinguindo simulação e consulta real.
- **Do** preservar o template e a hierarquia de leitura do guia.
- **Do** manter foco visível, rótulos, seleção programática e anúncios de status.
- **Don't** transformar exemplos ou barras simuladas em evidência de benchmark real.
- **Don't** depender apenas de cor para explicar o estado ou a decisão.
- **Don't** substituir a identidade INEMA, introduzir componentes inexistentes como regras consolidadas ou tratar esta extração como aprovação estética.
