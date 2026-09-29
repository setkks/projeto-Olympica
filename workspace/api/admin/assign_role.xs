query "users/assign_role" verb=POST {
  api_group = "admin"
  auth = "user"

  input {
    int user_id
    int role_id
  }

  stack {
    function.run require_permission {
      input = {
        user_id: $auth.id
        permission_code: "users.manage"
      }
    } as $authorization

    db.get user {
      field_name = "id"
      field_value = $input.user_id
      output = ["id", "email"]
    } as $user

    precondition ($user != null) {
      error_type = "notfound"
      error = "User not found."
    }

    db.get role {
      field_name = "id"
      field_value = $input.role_id
    } as $role

    precondition ($role != null) {
      error_type = "notfound"
      error = "Role not found."
    }

    db.query user_role {
      where = $db.user_role.user_id == $user.id && $db.user_role.role_id == $role.id
      return = {type: "single"}
    } as $existing_assignment

    conditional {
      if ($existing_assignment == null) {
        db.add user_role {
          data = {
            created_at: "now"
            user_id: $user.id
            role_id: $role.id
          }
        } as $assignment
      }
    }
  }

  response = {
    user_id: $user.id
    role_id: $role.id
    assigned: true
  }
}