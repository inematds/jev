# Publicação verificada — 18/09/2026

- Aplicação: https://inematds.github.io/jev/guia/ (HTTP 200).
- Laboratório: https://inematds.github.io/jev/app/.
- Curso com 36 aulas e oito laboratórios em Markdown: https://github.com/inematds/jev-curso.
- Portal/PRO: ambos cadastrados; curso indica explicitamente formato Markdown. A versão HTML aguarda resposta do usuário à escolha v5/v2, enviada nesta sessão.

Pushes confirmados: aplicação `4078bb2`, curso `8c64a88`, portal `78fa905`, inemabuscas `6dd5c9a`, INEMAPRO `9d0011b`.

Verificação: 14 testes Python; fluxo de navegador desktop/mobile; revisão visual aprovada; build portal, TypeScript e 7 testes; 41 testes da base; classificação das duas entradas confirmada. Workflow Pages concluído. Nenhuma consulta ao Vercel.

Limite: sem TYPESAFE_API_KEY nos arquivos autorizados. O cliente real tem validação e retries testados com respostas controladas; nenhuma qualidade ou latência Jev real foi medida. Dataset de referência contém 24 tickets fictícios; baseline lexical 20 acertos. Materiais recebidos nunca foram versionados.

## Continuidade técnica

Publicação dos catálogos foi isolada em `/tmp/jev-publicacao/{portal,inemabuscas,inemapro-mono}` por edição concorrente de outro curso. Ramos `publish-jev-20260918` foram enviados ao main remoto com integração das atualizações concorrentes. Os diretórios originais com alterações existentes foram preservados.

ATENÇÃO: no inemabuscas, o remote `origin` aponta para outro projeto (INEMAPRO). O destino correto é o remote `inemabuscas`, upstream `inemabuscas/main`. Não usar origin nesse repo.

Ao escolher a versão visual do curso: ler a skill correspondente, gerar HTML a partir de `conteudo/curso.json`, verificar aprendizagem/navegação e publicar Pages. Atualizar a URL do card e migrar enrichment de `curso:inematds-jev-curso` para o ID derivado da nova URL, preservando relacionados.

## Verificação da atualização v1.2.1 — 19/09/2026

Vinte casos validados; 27 testes Python passaram. Teste de navegador passou para os 20 casos, perguntas combinadas, importação/exportação, relatórios, temas, custos e layouts desktop/mobile sem overflow ou erros JavaScript. Build mantém somente app, guia, capa e entrada. Banner dos recursos adicionado ao README. Curso v1.2.0 validado: 12 módulos, 36 aulas e 12 laboratórios; casos sincronizados com o app.

Mantida a identidade visual existente; o detector de estilo apontou avisos de tipografia e tokens, sem impedir os testes funcionais. A geração do banner usou a ferramenta integrada imagegen, com composição de prisma de decisões, fundo escuro e acentos âmbar. Não houve inferência Jev real.

### Pushes e disponibilidade confirmados nesta atualização

- Aplicação e banner: `a0dc4de` em `inematds/jev`; Pages concluído com sucesso. Laboratório v1.2.1, guia e banner retornaram HTTP 200.
- Curso: `b37d99a` em `inematds/jev-curso`.
- Portal: `000325b` em `NeiMaldaner/portal`.
- Busca: `b93348d` em `inematds/inemabuscas`.
- PRO: `ef6b5bd` em `inematds/inemapro`.

Verificações dos catálogos: 7 testes do portal, TypeScript sem erros e 41 testes da base. Acervo final preservado com 18.276 IDs, incluindo 277 cursos, 234 projetos e 12.312 clipes; 100% dos cursos/projetos classificados. Conflito JSON legado resolvido sem descartar classificações. Fontes de clipes sincronizadas antes da verificação final de IDs. Correções registradas no FALHAS.md do PRO. Nenhuma consulta ao Vercel.

Trabalho dos catálogos isolado em `/tmp/jev-update-20260919/` para preservar alterações preexistentes nos diretórios originais.
