# Proposta: Usuarios, RBAC e autenticacao JWT

## Por que

O workspace ainda nao define identidade de usuarios, controle de acesso ou autenticacao. Sem esses recursos, as APIs nao conseguem identificar com seguranca quem esta fazendo uma requisicao nem limitar operacoes por permissao.

## O que muda

- Definir a estrutura de usuarios e o provisionamento de contas com identificador de email unico e senha armazenada com hash seguro.
- Definir perfis (roles), permissoes e a associacao entre usuarios e perfis para controle de acesso baseado em roles (RBAC).
- Definir autenticacao por credenciais, emissao e validacao de JWT, incluindo expiracao e identidade do usuario.
- Exigir verificacao de autenticacao e permissao nas APIs protegidas, negando acesso por padrao quando nao houver permissao explicita.

## Capacidades

- `identidade-e-acesso`: usuarios, perfis, permissoes e autenticacao JWT no Xano.

## Fora de escopo

- Cadastro publico, recuperacao de senha e verificacao de email.
- Renovacao de tokens (refresh tokens), logout com revogacao antes da expiracao e login por provedores externos.
- Definicao de permissoes especificas de negocio; elas serao cadastradas conforme os endpoints protegidos forem identificados.