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
