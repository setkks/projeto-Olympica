## 1. Modelo de dados

- [ ] 1.1 Confirmar e documentar os campos essenciais de atleta e turma antes de implementar o schema.
- [ ] 1.2 Criar tabelas Xano para atletas, turmas de ginastica e matriculas, com estados, chaves estrangeiras e indices unicos necessarios.
- [ ] 1.3 Definir os codigos de permissao para gestao de atletas, turmas e matriculas e provisiona-los no RBAC existente.

## 2. Gestao de atletas e turmas

- [ ] 2.1 Implementar APIs autenticadas para criar, consultar, atualizar e desativar atletas.
- [ ] 2.2 Implementar APIs autenticadas para criar, consultar, atualizar e desativar turmas.
- [ ] 2.3 Aplicar a verificacao RBAC correspondente em cada operacao e retornar respostas sem expor campos sensiveis desnecessarios.

## 3. Matriculas

- [ ] 3.1 Implementar matricula de atleta ativo em turma ativa e rejeitar entidades inexistentes, inativas ou pares ja matriculados.
- [ ] 3.2 Implementar encerramento e reativacao de matriculas sem criar duplicatas nem apagar historico.
- [ ] 3.3 Expor consultas para visualizar atletas por turma e turmas por atleta, incluindo estado da matricula.

## 4. Validacao

- [ ] 4.1 Validar unicidade, referencias, estados e preservacao dos registros ao desativar atleta ou turma.
- [ ] 4.2 Validar matricula, rejeicao de duplicata, encerramento e reativacao do vinculo.
- [ ] 4.3 Validar acesso autorizado e negado por permissao em cada grupo de APIs.
