resource "azurerm_static_web_app" "nextjs_app" {
  name                = var.static_site_name
  resource_group_name = var.resource_group_name
  location            = var.location

  sku_tier = "Standard"
  sku_size = "Standard"
}
