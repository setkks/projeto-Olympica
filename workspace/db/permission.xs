table permission {
  schema {
    int id
    timestamp created_at?=now
    text code filters=trim|lower
    text description?
  }

  index = [
    {type: "primary", field: [{name: "id"}]}
    {type: "btree|unique", field: [{name: "code", op: "asc"}]}
  ]
}