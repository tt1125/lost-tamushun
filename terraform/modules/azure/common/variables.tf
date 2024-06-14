variable "environment" {
  description = "The environment name."
  type        = string
}

variable "project_name" {
  description = "The project name."
  type        = string
  default      = "losttamshun"
}

variable "location" {
  description = "Specifies the supported Azure location where the resource exists."
  type        = string
}


variable "repo_url" {
  description = "The URL of the GitHub repository."
  type        = string
}

variable "branch" {
  description = "The branch of the GitHub repository."
  type        = string
}

variable "github_token" {
  description = "The token for the GitHub repository."
  type        = string
}

variable "secrets" {
  description = "A map of secrets to be stored in the Key Vault."
  type        = map(string)
  default     = {}
}

variable "tenant_id" {
  description = "The tenant ID for the Azure subscription."
  type        = string
}

variable "current_user_id" {
  description = "The current user ID."
  type        = string
  default     = null
}

variable "msi_id" {
  type        = string
  description = "The Managed Service Identity ID. If this value isn't null (the default), 'data.azurerm_client_config.current.object_id' will be set to this value."
  default     = null
}