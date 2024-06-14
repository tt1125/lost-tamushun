variable "resource_group_name" {
  description = "Name of the resource group"
  type        = string
}

variable "location" {
  description = "Location of the Azure Function App"
  type        = string
}

variable "search_service_name" {
  description = "Name of the Azure Search Service"
  type        = string
}

variable "search_index_name" {
  description = "Name of the Azure Search Index"
  type        = string
}
