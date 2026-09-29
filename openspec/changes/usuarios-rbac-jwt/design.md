# Design

## Context

Consulte [proposal.md](proposal.md) para a motivacao e [specs/identidade-e-acesso/spec.md](specs/identidade-e-acesso/spec.md) para os requisitos. O workspace versiona arquivos XanoScript, mas nao tem credenciais/conexao com uma instancia Xano; os artefatos serao preparados localmente para importacao no Xano. Atualmente nao ha tabelas ou APIs de negocio exportadas.

## Goals / Non-Goals

automatically.

Alternativa considerada: gerar e validar JWT manualmente com JWS e segredo de aplicacao. Foi rejeitada por duplicar o mecanismo de autenticacao do Xano e aumentar o risco de gestao incorreta de segredo e validacao.

### Modelar RBAC com tabelas normalizadas

Usar tabelas `role` e `permission`, com tabelas de associacao `user_role` e `role_permission`. Indices unicos nas chaves de email, perfil/permissao e pares de associacao impedem duplicatas. As permissoes efetivas serao consultadas no servidor em cada operacao protegida; alteracoes de perfil passam a valer sem esperar a expiracao de um token.

Alternativa considerada: guardar um unico campo de role no usuario ou incluir roles no JWT. Foi rejeitada por nao suportar multiplos perfis e por manter autorizacao desatualizada depois de uma mudanca de acesso.

### Exigir autenticacao e permissao em cada API protegida

APIs protegidas usam a autenticacao `user` do Xano e uma verificacao reutilizavel que carrega o usuario atual, rejeita contas inativas e exige uma chave de permissao explicita. A verificacao nao encontra permissao ou identidade valida, a operacao falha fechada. As APIs de gerenciamento exigem permissoes administrativas (`users.manage`, `roles.manage` ou `permissions.manage`); a primeira conta administrativa e provisionada por um operador no Xano, fora de um endpoint publico.

Alternativa considerada: confiar apenas no campo de autenticacao da API ou aceitar acesso quando nenhuma permissao foi configurada. Foi rejeitada porque autenticar nao e o mesmo que autorizar e a segunda alternativa viola negacao por padrao.

## Risks / Trade-offs

- [Instancia Xano pode ja conter uma tabela `user` ou convencoes diferentes] -> Importar primeiro em ambiente de desenvolvimento e reconciliar nomes/campos antes de aplicar em producao.
- [Middleware precisa ser associado a cada API protegida] -> Manter essa associacao explicita nos artefatos e cobrir cada endpoint protegido com teste de acesso autorizado e negado.
- [Consultas RBAC por requisicao aumentam o trabalho no banco] -> Indexar chaves e pares de associacao; nao cachear autorizacao ate existir requisito e estrategia segura de invalidacao.
- [Chaves iniciais de permissao sao administrativas, nao de negocio] -> Criar permissoes de negocio junto com os endpoints que as exigirem.

## Migration Plan

1. Importar as tabelas em ambiente Xano de desenvolvimento e verificar compatibilidade com dados e tabelas existentes.
2. Provisionar as permissoes administrativas e uma primeira conta administradora por meio do console seguro do Xano.
3. Importar login, verificacao de permissao e endpoints administrativos; aplicar autenticacao e permissoes aos endpoints protegidos.
4. Validar fluxos de sucesso e negacao antes de promover os artefatos para producao.

Rollback: desabilitar os novos endpoints e middleware nos grupos de API, preservando as tabelas e registros de acesso ate decidir a remocao. Nao apagar contas ou associacoes durante o rollback.