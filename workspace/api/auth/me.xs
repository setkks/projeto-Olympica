query me verb=GET {
  api_group = "auth"
  auth = "user"

  input {
  }

  stack {
    db.get user {
      field_name = "id"
      field_value = $auth.id
      output = ["id", "created_at", "email", "is_active", "last_login_at"]
    } as $user

    precondition ($user != null && $user.is_active == true) {
      error_type = "unauthorized"
      error = "Account is inactive."
    }
  }

  response = $user
}