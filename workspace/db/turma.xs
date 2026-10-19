db.table "turma" {
  auth = false

  schema {
    int id {
      primary = true
    }
    timestamp created_at {
      default = "now"
    }
    text nome
    text horario
    int capacidade {
      default = 15
    }
  }
}