query "roles/assign_permission" verb=POST {
  api_group = "admin"
  auth = "user"

  input {
    int role_id
    int permission_id
  }

  stack {
    function.run require_permission {
      input = {
        user_id: $auth.id
        permission_code: "permissions.manage"
      }
    } as $authorization

    db.get role {
      field_name = "id"
      field_value = $input.role_id
    } as $role

    precondition ($role != null) {
      error_type = "notfound"
      error = "Role not found."
    }

    db.get permission {
      field_name = "id"
      field_value = $input.permission_id
    } as $permission

    precondition ($permission != null) {
      error_type = "notfound"
      error = "Permission not found."
    }

    db.query role_permission {
      where = $db.role_permission.role_id == $role.id && $db.role_permission.permission_id == $permission.id
      return = {type: "single"}
    } as $existing_assignment

    conditional {
      if ($existing_assignment == null) {
        db.add role_permission {
          data = {
            created_at: "now"
            role_id: $role.id
            permission_id: $permission.id
          }
        } as $assignment
      }
    }
  }

  response = {
    role_id: $role.id
    permission_id: $permission.id
    assigned: true
  }
}