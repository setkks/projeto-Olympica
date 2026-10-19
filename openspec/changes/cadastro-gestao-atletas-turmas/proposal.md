# Proposta: Cadastro e gestao de atletas e turmas de ginastica

## Por que

O workspace ainda nao possui recursos de negocio para cadastrar atletas, organizar turmas de ginastica ou registrar em quais turmas cada atleta participa. Sem esses recursos, a equipe nao tem uma fonte centralizada para manter esses cadastros e seus vinculos.

## O que muda

- Criar operacoes autenticadas para cadastrar, consultar, atualizar e desativar atletas.
- Criar operacoes autenticadas para cadastrar, consultar, atualizar e desativar turmas de ginastica.
- Permitir matricular atletas ativos em turmas ativas e encerrar matriculas, mantendo o historico do vinculo.
- Restringir operacoes por permissoes explicitas do RBAC existente e negar acesso por padrao.

## Capacidades

- `gestao-de-atletas-e-turmas`: cadastro e gestao de atletas, turmas e matriculas entre eles.

## Fora de escopo

- Interface web ou aplicativo para operar os cadastros.
- Presenca, frequencia, avaliacao, pagamentos ou cobranca.
- Gestao de horarios, capacidade de turma, instrutores ou lista de espera.
- Cadastro publico, importacao em massa ou integracao com servicos externos.
- Exclusao fisica de registros ou de historico de matriculas.
