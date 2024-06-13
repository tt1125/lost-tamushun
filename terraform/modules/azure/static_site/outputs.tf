output "static_site_url" {
  value = azurerm_static_web_app.nextjs_app.default_host_name
}
