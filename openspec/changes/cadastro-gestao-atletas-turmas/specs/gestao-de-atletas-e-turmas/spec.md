## ADDED Requirements

### Requirement: Gestao de atletas
O sistema MUST permitir a usuarios autenticados e autorizados cadastrar, consultar, atualizar e desativar atletas, preservando os registros existentes.

#### Scenario: Cadastrar atleta
- **WHEN** um usuario com permissao de gestao de atletas envia os dados obrigatorios validos para um novo atleta
- **THEN** o sistema cria e retorna o atleta ativo

#### Scenario: Atualizar atleta
- **WHEN** um usuario com permissao de gestao de atletas atualiza um atleta existente com dados validos
- **THEN** o sistema persiste as alteracoes e retorna o cadastro atualizado

#### Scenario: Consultar atleta
- **WHEN** um usuario autenticado e autorizado consulta atletas ou um atleta especifico
- **THEN** o sistema retorna os registros correspondentes sem incluir campos internos ou sensiveis que nao sejam necessarios

#### Scenario: Desativar atleta
- **WHEN** um usuario com permissao de gestao de atletas desativa um atleta existente
- **THEN** o sistema marca o atleta como inativo, preserva o registro e suas matriculas existentes, e impede novas matriculas para esse atleta

### Requirement: Gestao de turmas de ginastica
O sistema MUST permitir a usuarios autenticados e autorizados cadastrar, consultar, atualizar e desativar turmas de ginastica, preservando os registros existentes.

#### Scenario: Cadastrar turma
- **WHEN** um usuario com permissao de gestao de turmas envia os dados obrigatorios validos para uma nova turma
- **THEN** o sistema cria e retorna a turma ativa

#### Scenario: Atualizar turma
- **WHEN** um usuario com permissao de gestao de turmas atualiza uma turma existente com dados validos
- **THEN** o sistema persiste as alteracoes e retorna a turma atualizada

#### Scenario: Consultar turma
- **WHEN** um usuario autenticado e autorizado consulta turmas ou uma turma especifica
- **THEN** o sistema retorna os registros correspondentes e seus estados

#### Scenario: Desativar turma
- **WHEN** um usuario com permissao de gestao de turmas desativa uma turma existente
- **THEN** o sistema marca a turma como inativa, preserva o registro e suas matriculas existentes, e impede novas matriculas nessa turma

### Requirement: Matricula de atletas em turmas
O sistema MUST permitir vincular atletas a turmas por meio de matriculas, manter o estado dessas matriculas e impedir pares duplicados ativos.

#### Scenario: Matricular atleta ativo em turma ativa
- **WHEN** um usuario com permissao de gestao de matriculas solicita a matricula de um atleta ativo em uma turma ativa sem matricula ativa para esse par
- **THEN** o sistema cria a matricula ativa e a disponibiliza nas consultas do atleta e da turma

#### Scenario: Rejeitar matricula invalida ou duplicada
- **WHEN** um usuario solicita matricula para atleta ou turma inexistente ou inativa, ou para um par que ja possui matricula ativa
- **THEN** o sistema rejeita a operacao sem criar uma matricula duplicada

#### Scenario: Encerrar matricula
- **WHEN** um usuario com permissao de gestao de matriculas encerra uma matricula ativa
- **THEN** o sistema marca a matricula como encerrada e preserva o registro para consulta historica

#### Scenario: Reativar matricula encerrada
- **WHEN** um usuario autorizado reativa uma matricula encerrada e atleta e turma estao ativos
- **THEN** o sistema reativa o vinculo existente sem criar um segundo registro para o mesmo par

#### Scenario: Consultar matriculas
- **WHEN** um usuario autenticado e autorizado consulta as matriculas de um atleta ou de uma turma
- **THEN** o sistema retorna os vinculos e seus estados correspondentes

### Requirement: Autorizacao das operacoes de negocio
O sistema MUST exigir autenticacao e permissao RBAC explicita para operacoes de atletas, turmas e matriculas, negando acesso por padrao.

#### Scenario: Usuario com permissao requerida
- **WHEN** um usuario autenticado solicita uma operacao para a qual possui a permissao de negocio requerida
- **THEN** o sistema permite a operacao

#### Scenario: Usuario sem permissao requerida
- **WHEN** um usuario autenticado solicita uma operacao sem possuir a permissao de negocio requerida
- **THEN** o sistema nega a operacao

#### Scenario: Requisicao nao autenticada
- **WHEN** uma requisicao para qualquer operacao protegida nao apresenta autenticacao valida
- **THEN** o sistema rejeita a requisicao como nao autenticada sem realizar alteracoes
