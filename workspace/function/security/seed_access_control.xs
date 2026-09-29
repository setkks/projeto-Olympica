function "seed_access_control" {
  input {
  }

  stack {
    db.add_or_edit role {
      field_name = "name"
      field_value = "admin"
      data = {
        name: "admin"
        description: "Administrative access"
      }
    } as $admin_role

    db.add_or_edit role {
      field_name = "name"
      field_value = "user"
      data = {
        name: "user"
        description: "Standard user access"
      }
    } as $user_role

    db.add_or_edit permission {
      field_name = "code"
      field_value = "users.manage"
      data = {
        code: "users.manage"
        description: "Create users and assign user roles"
      }
    } as $users_manage

    db.add_or_edit permission {
      field_name = "code"
      field_value = "roles.manage"
      data = {
        code: "roles.manage"
        description: "Create roles"
      }
    } as $roles_manage

    db.add_or_edit permission {
      field_name = "code"
      field_value = "permissions.manage"
      data = {
        code: "permissions.manage"
        description: "Create permissions and assign them to roles"
      }
    } as $permissions_manage

    db.query role_permission {
      where = $db.role_permission.role_id == $admin_role.id && $db.role_permission.permission_id == $users_manage.id
      return = {type: "single"}
    } as $users_manage_assignment

    conditional {
      if ($users_manage_assignment == null) {
        db.add role_permission {
          data = {
            role_id: $admin_role.id
            permission_id: $users_manage.id
          }
        } as $users_manage_assignment_created
      }
    }

    db.query role_permission {
      where = $db.role_permission.role_id == $admin_role.id && $db.role_permission.permission_id == $roles_manage.id
      return = {type: "single"}
    } as $roles_manage_assignment

    conditional {
      if ($roles_manage_assignment == null) {
        db.add role_permission {
          data = {
            role_id: $admin_role.id
            permission_id: $roles_manage.id
          }
        } as $roles_manage_assignment_created
      }
    }

    db.query role_permission {
      where = $db.role_permission.role_id == $admin_role.id && $db.role_permission.permission_id == $permissions_manage.id
      return = {type: "single"}
    } as $permissions_manage_assignment

    conditional {
      if ($permissions_manage_assignment == null) {
        db.add role_permission {
          data = {
            role_id: $admin_role.id
            permission_id: $permissions_manage.id
          }
        } as $permissions_manage_assignment_created
      }
    }
  }

  response = {
    role: $admin_role
    default_role: $user_role
    permissions: [$users_manage, $roles_manage, $permissions_manage]
  }
}