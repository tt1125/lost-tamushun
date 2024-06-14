resource "azurerm_storage_account" "sa" {
  name                     = var.storage_account_name
  resource_group_name      = var.resource_group_name
  location                 = var.location
  account_tier             = "Standard"
  account_replication_type = "LRS"
}

resource "azurerm_storage_container" "sc" {
  depends_on = [azurerm_storage_account.sa]
  name                  = "${var.project_name}${var.environment}tfstate"
  storage_account_name  = azurerm_storage_account.sa.name
  container_access_type = "private"
}

resource "azurerm_storage_container" "file" {
  depends_on = [azurerm_storage_account.sa]
  name                  = "imgs"
  storage_account_name  = azurerm_storage_account.sa.name
  container_access_type = "blob"
}
