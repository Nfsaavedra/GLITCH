resource "azurerm_security_center_contact" "bad_example" {
  email = "bad_example@example.com"
  phone = "+1-555-555-5555"

  alert_notifications = false
  alerts_to_admins = false
}

resource "azurerm_security_center_contact" "good_example" {
  email = "good_example@example.com"
  phone = "+1-555-555-5555"

  alert_notifications = true
  alerts_to_admins = true
}
