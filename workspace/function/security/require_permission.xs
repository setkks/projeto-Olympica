function "require_permission" {
  input {
    int user_id
    text permission_code
  }

  stack {
    db.get user {
      field_name = "id"
      field_value = $input.user_id
      output = ["id", "is_active"]
    } as $user

    precondition ($user != null && $user.is_active == true) {
      error_type = "unauthorized"
      error = "Authentication required."
    }

    db.query user_role {
      where = $db.user_role.user_id == $input.user_id
      return = {type: "list"}
    } as $user_roles

    var $is_authorized {
      value = false
    }

    foreach ($user_roles) {
      each as $user_role {
        db.query role_permission {
          where = $db.role_permission.role_id == $user_role.role_id
          return = {type: "list"}
        } as $role_permissions

        foreach ($role_permissions) {
          each as $role_permission {
            db.get permission {
              field_name = "id"
              field_value = $role_permission.permission_id
              output = ["id", "code"]
            } as $permission

            conditional {
              if ($permission.code == $input.permission_code) {
                var.update $is_authorized {
                  value = true
                }
              }
            }
          }
        }
      }
    }

    precondition ($is_authorized == true) {
      error_type = "accessdenied"
      error = "Permission denied."
    }
  }

  response = {authorized: $is_authorized}
}