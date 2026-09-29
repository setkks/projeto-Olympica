table user_role {
  schema {
    int id
    timestamp created_at?=now
    int user_id {
      table = "user"
    }
    int role_id {
      table = "role"
    }
  }

  index = [
    {type: "primary", field: [{name: "id"}]}
    {type: "btree|unique", field: [{name: "user_id", op: "asc"}, {name: "role_id", op: "asc"}]}
    {type: "btree", field: [{name: "role_id", op: "asc"}]}
  ]
}