db.table "atleta" {
  auth = false

  schema {
    int id {
      primary = true
    }
    timestamp created_at {
      default = "now"
    }
    text nome
    date data_nascimento
    text categoria
    text status {
      default = "Ativo"
    }
  }
}