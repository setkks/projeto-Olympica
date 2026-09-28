## 1. Modelo de identidade e acesso

- [ ] 1.1 Definir no Xano as tabelas de usuarios, perfis, permissoes e associacoes entre usuarios/perfis e perfis/permissoes.
- [ ] 1.2 Configurar unicidade do email, estado da conta e armazenamento de senha usando o mecanismo seguro de autenticacao/hash do Xano.
- [ ] 1.3 Definir e provisionar as permissoes iniciais necessarias para proteger os endpoints existentes.

## 2. Autenticacao JWT

- [ ] 2.1 Implementar autenticacao por email e senha, bloqueando contas inativas e credenciais invalidas.
- [ ] 2.2 Configurar emissao de JWT assinado, com identificador do usuario e expiracao definidos por configuracao segura.
- [ ] 2.3 Implementar validacao do JWT nas APIs protegidas e retornar resposta nao autenticada para tokens ausentes, invalidos ou expirados.

## 3. Autorizacao RBAC

- [ ] 3.1 Implementar verificacao de permissoes efetivas a partir dos perfis associados ao usuario.
- [ ] 3.2 Aplicar negacao por padrao e negar operacoes quando a permissao requerida estiver ausente.
- [ ] 3.3 Restringir operacoes de gerenciamento de usuarios, perfis e permissoes a identidades autorizadas.

## 4. Validacao

- [ ] 4.1 Testar provisionamento, unicidade de email, conta inativa e protecao de senha.
- [ ] 4.2 Testar login valido/invalido, expiracao e rejeicao de JWT adulterado ou ausente.
- [ ] 4.3 Testar autorizacao com permissao concedida, permissao ausente e acesso negado por padrao.