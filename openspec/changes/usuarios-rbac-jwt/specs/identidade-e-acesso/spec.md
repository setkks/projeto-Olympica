## ADDED Requirements

### Requirement: Provisionamento de usuarios
O sistema MUST manter usuarios com identificador de email unico, estado da conta e senha protegida por hash seguro, sem armazenar a senha em texto puro.

#### Scenario: Criar usuario
- **WHEN** um usuario e provisionado com email ainda nao utilizado e senha valida
- **THEN** o sistema cria uma conta ativa e armazena somente o hash seguro da senha

#### Scenario: Email ja cadastrado
- **WHEN** um usuario e provisionado com um email que ja pertence a outra conta
- **THEN** o sistema rejeita a operacao sem criar uma segunda conta para o mesmo email

### Requirement: Perfis e permissoes RBAC
O sistema MUST permitir associar usuarios a um ou mais perfis (roles), perfis a permissoes e proteger operacoes com base nas permissoes requeridas.

#### Scenario: Usuario tem permissao requerida
- **WHEN** um usuario autenticado solicita uma operacao e pelo menos um de seus perfis concede a permissao requerida
- **THEN** o sistema autoriza a operacao

#### Scenario: Usuario nao tem permissao requerida
- **WHEN** um usuario autenticado solicita uma operacao sem possuir a permissao requerida
- **THEN** o sistema nega a operacao

#### Scenario: Acesso negado por padrao
- **WHEN** uma operacao protegida nao declara uma permissao concedida ao usuario
- **THEN** o sistema nega a operacao

### Requirement: Autenticacao por JWT
O sistema MUST autenticar usuarios por credenciais e emitir JWT assinado com a identidade do usuario e prazo de expiracao.

#### Scenario: Credenciais validas
- **WHEN** um usuario ativo envia email e senha corretos
- **THEN** o sistema emite um JWT assinado com identificador do usuario e expiracao

#### Scenario: Credenciais invalidas ou conta inativa
- **WHEN** um usuario envia credenciais incorretas ou pertence a uma conta inativa
- **THEN** o sistema rejeita a autenticacao sem emitir um JWT

### Requirement: Validacao de acesso autenticado
O sistema MUST validar assinatura, expiracao e estado da conta ao aceitar um JWT em uma operacao protegida.

#### Scenario: Token valido
- **WHEN** uma requisicao protegida apresenta JWT com assinatura valida, nao expirado e associado a conta ativa
- **THEN** o sistema identifica o usuario e continua a verificacao de permissoes

#### Scenario: Token invalido ou expirado
- **WHEN** uma requisicao protegida apresenta JWT ausente, invalido ou expirado
- **THEN** o sistema rejeita a requisicao como nao autenticada