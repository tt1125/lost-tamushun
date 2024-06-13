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