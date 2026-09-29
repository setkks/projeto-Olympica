query roles verb=POST {
  api_group = "admin"
  auth = "user"

  input {
    text name filters=trim|lower
    text description?
  }

  stack {
    function.run require_permission {
      input = {
        user_id: $auth.id
        permission_code: "roles.manage"
      }
    } as $authorization

    db.get role {
      field_name = "name"
      field_value = $input.name
    } as $existing_role

    precondition ($existing_role == null) {
      error_type = "accessdenied"
      error = "Role already exists."
    }

    db.add role {
      data = {
        created_at: "now"
        name: $input.name
        description: $input.description
      }
    } as $role
  }

  response = {
    id: $role.id
    name: $role.name
    description: $role.description
  }
}