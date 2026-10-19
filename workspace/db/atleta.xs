table "atleta" {
  auth = false

  schema {
    int id
    timestamp created_at
    text nome
    date data_nascimento
    text categoria
    text status
  }
}