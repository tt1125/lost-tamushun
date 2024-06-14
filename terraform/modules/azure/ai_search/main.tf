resource "azurerm_search_service" "search_service" {
  name                = var.search_service_name
  resource_group_name = var.resource_group_name
  location            = var.location
  sku                 = "standard"
}
