table user {
  auth = true

  schema {
    int id
    timestamp created_at?=now
    email email filters=trim|lower
    password password filters=min:8|minAlpha:1|minDigit:1
    bool is_active?=true
    timestamp last_login_at?
  }

  index = [
    {type: "primary", field: [{name: "id"}]}
    {type: "btree|unique", field: [{name: "email", op: "asc"}]}
  ]
}