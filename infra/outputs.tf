output "user_pool_id" {
    value = aws_cognito_user_pool.my_user_pool.id
}

output "app_client_id" {
    value = aws_cognito_user_pool_client.my_app_client.id
}