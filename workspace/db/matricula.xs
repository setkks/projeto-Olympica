table "matricula" {
  auth = false

  schema {
    int id
    timestamp created_at
    int atleta_id
    int turma_id
    date data_matricula
    text status
  }
}