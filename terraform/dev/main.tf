provider "azurerm" {
  features {
  }
}

data "azurerm_client_config" "current" {}

resource "azuread_application" "app" {
  display_name = "${var.project_name}-${var.environment}-app"
}


module "common" {
  source = "../modules/azure/common"

  environment        = var.environment
  location           = var.location
  project_name       = var.project_name
  secrets            = var.secrets
  repo_url           = var.repo_url
  branch             = var.branch
  github_token       = var.github_token
  tenant_id          = data.azurerm_client_config.current.tenant_id
}


terraform {
  backend "azurerm" {
    resource_group_name   = "losttamshun_dev_rg"
    storage_account_name  = "losttamshundevsa"
    container_name        = "losttamshundevtfstate"
    key                   = "terraform.tfstate"
  }
}
