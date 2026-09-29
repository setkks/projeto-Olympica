query login verb=POST {
  api_group = "auth"

  input {
    email email filters=trim|lower
    text password
  }

  stack {
    db.get user {
      field_name = "email"
      field_value = $input.email
    } as $user

    precondition ($user != null && $user.is_active == true) {
      error_type = "accessdenied"
      error = "Invalid email or password."
    }

    security.check_password {
      text_password = $input.password
      hash_password = $user.password
    } as $password_valid

    precondition ($password_valid == true) {
      error_type = "accessdenied"
      error = "Invalid email or password."
    }

    db.edit user {
      field_name = "id"
      field_value = $user.id
      data = {
        last_login_at: "now"
      }
    } as $updated_user

    security.create_auth_token {
      table = "user"
      extras = {}
      expiration = 3600
      id = $user.id
    } as $auth_token
  }

  response = {
    authToken: $auth_token
    user: {
      id: $user.id
      email: $user.email
    }
  }
}