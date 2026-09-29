query permissions verb=POST {
  api_group = "admin"
  auth = "user"

  input {
    text code filters=trim|lower
    text description?
  }

  stack {
    function.run require_permission {
      input = {
        user_id: $auth.id
        permission_code: "permissions.manage"
      }
    } as $authorization

    db.get permission {
      field_name = "code"
      field_value = $input.code
    } as $existing_permission

    precondition ($existing_permission == null) {
      error_type = "accessdenied"
      error = "Permission already exists."
    }

    db.add permission {
      data = {
        created_at: "now"
        code: $input.code
        description: $input.description
      }
    } as $permission
  }

  response = {
    id: $permission.id
    code: $permission.code
    description: $permission.description
  }
}