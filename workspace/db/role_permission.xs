table role_permission {
  schema {
    int id
    timestamp created_at?=now
    int role_id {
      table = "role"
    }
    int permission_id {
      table = "permission"
    }
  }

  index = [
    {type: "primary", field: [{name: "id"}]}
    {type: "btree|unique", field: [{name: "role_id", op: "asc"}, {name: "permission_id", op: "asc"}]}
    {type: "btree", field: [{name: "permission_id", op: "asc"}]}
  ]
}