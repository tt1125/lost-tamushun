module "resource_group" {
  source = "../resource_group/"

  resource_group_name = "${var.project_name}_${var.environment}_rg"
  location            = var.location
  environment         = var.environment
}


module "azure_storage" {
  depends_on          = [module.resource_group]
  source              = "../storage"
  resource_group_name = module.resource_group.resource_group_name

  storage_account_name = "${var.project_name}${var.environment}sa"
  location             = module.resource_group.resource_group_location
  environment          = var.environment
  project_name         = var.project_name
}

module "functions" {
  depends_on = [module.resource_group, module.azure_storage, module.key_vault_secret]
  source = "../functions"

  function_app_name     = "${var.project_name}-${var.environment}-functions"
  resource_group_name   = module.resource_group.resource_group_name
  location              = module.resource_group.resource_group_location
  storage_account_name  = module.azure_storage.storage_account_name
  app_service_plan_name = "${var.project_name}${var.environment}functionsasp"
  app_settings = {
      "FUNCTIONS_WORKER_RUNTIME" = "node"
      "FUNCTIONS_EXTENSION_VERSION": "~4",
      "WEBSITE_NODE_DEFAULT_VERSION": "18",
      # "NEXT_PUBLIC_DATABASE_URL"                 = module.key_vault_secret.secrets["next-public-database-url"]
      # "NEXT_PUBLIC_AZURE_STORAGE_CONNECTION_STRING" = module.key_vault_secret.secrets["next-public-azure-storage-connection-string"]
      # "NEXT_PUBLIC_PROJECT_ID"                   = module.key_vault_secret.secrets["next-public-project-id"]
      # "NEXT_PUBLIC_FIREBASE_CLIENT_EMAIL"        = module.key_vault_secret.secrets["next-public-firebase-client-email"]
      # "NEXT_PUBLIC_FIREBASE_PRIVATE_KEY"         = module.key_vault_secret.secrets["next-public-firebase-private-key"]
  }
}

module "static_site" {
  depends_on          = [module.key_vault_secret, module.functions]
  source = "../static_site"

  static_site_name = "${var.project_name}-${var.environment}-static-site"
  resource_group_name = module.resource_group.resource_group_name
  location            = "eastus2"
  repo_url            = var.repo_url
  branch              = var.branch
  github_token        = var.github_token

  app_settings = {
    # "NEXT_PUBLIC_DATABASE_URL" = module.key_vault_secret.secrets["next-public-database-url"]
    # "NEXT_PUBLIC_FIREBASE_API_KEY"        = module.key_vault_secret.secrets["next-public-firebase-api-key"]
    # "NEXT_PUBLIC_FIREBASE_AUTH_DOMAIN"    = module.key_vault_secret.secrets["next-public-firebase-auth-domain"]
    # "NEXT_PUBLIC_FIREBASE_APP_ID"=module.key_vault_secret.secrets["next-public-firebase-app-id"]
    # "NEXT_PUBLIC_FIREBASE_STORAGE_BUCKET"=module.key_vault_secret.secrets["next-public-firebase-storage-bucket"]
    # "NEXT_PUBLIC_FIREBASE_MESSAGING_SENDER_ID"=module.key_vault_secret.secrets["next-public-firebase-messaging-sender-id"]
    # "NEXT_PUBLIC_PROJECT_ID"=module.key_vault_secret.secrets["next-public-project-id"]
    # "NEXT_PUBLIC_FIREBASE_PRIVATE_KEY"=module.key_vault_secret.secrets["next-public-firebase-private-key"]
    # "NEXT_PUBLIC_FIREBASE_CLIENT_EMAIL"=module.key_vault_secret.secrets["next-public-firebase-client-email"]
    # "NEXT_PUBLIC_AZURE_STORAGE_CONNECTION_STRING"=module.key_vault_secret.secrets["next-public-azure-storage-connection-string"]
    # "NEXT_PUBLIC_OPEN_AI_KEY"=module.key_vault_secret.secrets["next-public-open-ai-key"]
  }

}