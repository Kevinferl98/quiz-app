terraform {
  required_providers {
    aws = {
        source = "hashicorp/aws"
        version = "~> 6.15.0"
    }
  }
}

provider "aws" {
  region = var.aws_region
}

resource "aws_cognito_user_pool" "my_user_pool" {
    name = "my-user-pool"

    username_attributes = []
    alias_attributes    = []
    
    admin_create_user_config {
      allow_admin_create_user_only = true
    }
}

resource "aws_cognito_user_pool_client" "my_app_client" {
    name = "my-app-client"
    user_pool_id = aws_cognito_user_pool.my_user_pool.id

    explicit_auth_flows = [
      "ALLOW_USER_PASSWORD_AUTH",
      "ALLOW_REFRESH_TOKEN_AUTH",
      "ALLOW_USER_SRP_AUTH"
    ]
}