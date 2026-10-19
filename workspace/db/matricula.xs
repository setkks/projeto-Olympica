db.table "matricula" {
  auth = false

  schema {
    int id {
      primary = true
    }
    timestamp created_at {
      default = "now"
    }
    int atleta_id {
      table = "atleta"
    }
    int turma_id {
      table = "turma"
    }
    date data_matricula
    text status {
      default = "Ativa"
    }
  }
}