table role {
  schema {
    int id
    timestamp created_at?=now
    text name filters=trim|lower
    text description?
  }

  index = [
    {type: "primary", field: [{name: "id"}]}
    {type: "btree|unique", field: [{name: "name", op: "asc"}]}
  ]
}