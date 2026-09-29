query users verb=POST {
  api_group = "admin"
  auth = "user"

  input {
    email email filters=trim|lower
    text password
  }

  stack {
    function.run require_permission {
      input = {
        user_id: $auth.id
        permission_code: "users.manage"
      }
    } as $authorization

    db.get user {
      field_name = "email"
      field_value = $input.email
      output = ["id", "email"]
    } as $existing_user

    precondition ($existing_user == null) {
      error_type = "accessdenied"
      error = "Email is already in use."
    }

    db.get role {
      field_name = "name"
      field_value = "user"
    } as $default_role

    precondition ($default_role != null) {
      error_type = "notfound"
      error = "Default user role is not configured."
    }

    db.add user {
      data = {
        created_at: "now"
        email: $input.email
        password: $input.password
        is_active: true
      }
    } as $user

    db.add user_role {
      data = {
        created_at: "now"
        user_id: $user.id
        role_id: $default_role.id
      }
    } as $user_role
  }

  response = {
    id: $user.id
    email: $user.email
    is_active: $user.is_active
  }
}