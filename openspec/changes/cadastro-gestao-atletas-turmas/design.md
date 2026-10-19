# Design

## Context

Consulte [proposal.md](proposal.md) para a motivacao e [specs/gestao-de-atletas-e-turmas/spec.md](specs/gestao-de-atletas-e-turmas/spec.md) para os requisitos. O workspace contem APIs XanoScript e autenticacao JWT com verificacao RBAC reutilizavel. Ainda nao ha tabelas ou APIs de negocio de atletas e turmas; o frontend tambem nao faz parte dos artefatos Xano deste workspace.

## Goals / Non-Goals

### Goals

- Manter atletas, turmas e seus vinculos em tabelas Xano relacionadas.
- Expor operacoes autenticadas para gerir cadastros e matriculas.
- Preservar registros e historico por meio de desativacao e encerramento de matricula, em vez de exclusao fisica.
- Aplicar permissoes explicitas do RBAC existente em cada operacao protegida.

### Non-Goals

- Definir interface de usuario, regras de frequencia, pagamentos, capacidade ou horarios.
- Definir campos pessoais alem dos estritamente necessarios para identificar atletas e turmas; confirmar os campos de negocio antes de implementar o schema final.

## Decisoes

### Modelar atleta, turma e matricula separadamente

Adicionar tabelas `athlete`, `gymnastics_class` e `athlete_class`, usando os nomes de tabela singulares e campos `snake_case` do workspace. `athlete_class` representa uma matricula e armazena seu estado e datas relevantes. Uma chave unica no par atleta/turma impede matriculas duplicadas; reativar um vinculo encerrado atualiza a matricula existente, preservando seu historico.

Alternativa considerada: armazenar os identificadores de turma diretamente no atleta ou atletas diretamente na turma. Foi rejeitada por dificultar consultas, integridade referencial e evolucao do relacionamento muitos-para-muitos.

### Desativar cadastros sem apagar historico

Atletas e turmas terao estado ativo/inativo; matriculas poderao ser encerradas. Cadastros inativos nao poderao receber novas matriculas. A desativacao nao apaga matriculas ja existentes, para preservar o historico. A politica de exibicao dessas matriculas em consultas sera definida junto aos endpoints.

### Proteger operacoes com permissoes RBAC dedicadas

As APIs usarao autenticacao `user` do Xano e a funcao existente `require_permission`. Definir permissoes para gerir atletas, turmas e matriculas, e exigir a permissao correspondente em cada operacao. Nenhum endpoint de negocio sera publico; a primeira atribuicao dessas permissoes a perfis autorizados sera feita pelo mecanismo administrativo existente.

Alternativa considerada: reutilizar permissoes administrativas genericas de usuarios ou permitir leitura sem autenticacao. Foi rejeitada por misturar responsabilidades e enfraquecer o acesso por padrao negado.

### Fazer matricula com validacao atomica do vinculo

Antes de criar ou reativar uma matricula, validar que atleta e turma existem e estao ativos, e que nao ha matricula ativa para o mesmo par. Uma matricula encerrada podera ser reativada. As verificacoes e a gravacao devem ocorrer numa unica operacao de API; usar restricao unica no banco como ultima defesa contra duplicatas concorrentes.

Alternativa considerada: permitir registros duplicados e consolidar na camada de consulta. Foi rejeitada por produzir estado ambiguo e exigir tratamento repetido em todos os consumidores.

## Riscos / Trade-offs

- [Os campos necessarios para identificar atletas e turmas ainda nao estao definidos] -> Confirmar o schema com a equipe antes de criar tabelas; manter o primeiro corte restrito aos campos essenciais e evitar coletar dados pessoais sem necessidade.
- [As permissoes novas nao serao atribuidas automaticamente a perfis existentes] -> Provisionar os codigos de permissao e atribui-los explicitamente a perfis apropriados antes de liberar os endpoints.
- [Reativar uma matricula existente preserva apenas um registro por par atleta/turma] -> Confirmar se o produto precisa de ciclos de matricula separados; caso precise, modelar historico em entidade propria antes da implementacao.
- [Nao ha politica de exclusao ou retencao de dados definida] -> Usar desativacao sem exclusao fisica neste escopo e decidir retencao em uma mudanca dedicada, se necessaria.

## Migration Plan

1. Confirmar os campos essenciais e a politica de reativacao de matriculas.
2. Importar as novas tabelas e verificar compatibilidade no ambiente Xano de desenvolvimento.
3. Provisionar as permissoes e atribui-las aos perfis autorizados.
4. Importar e validar as APIs de atletas, turmas e matriculas com acesso permitido e negado.
5. Promover os artefatos depois de confirmar consultas, integridade dos vinculos e preservacao dos historicos.

Rollback: desabilitar os novos endpoints e manter as tabelas e os registros criados. Nao apagar cadastros nem matriculas durante o rollback.
