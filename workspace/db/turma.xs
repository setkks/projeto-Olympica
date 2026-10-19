table "turma" {
  auth = false

  schema {
    int id
    timestamp created_at
    text nome
    text horario
    int capacidade
  }
}