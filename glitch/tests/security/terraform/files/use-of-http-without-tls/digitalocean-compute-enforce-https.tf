resource "digitalocean_loadbalancer" "bad_example" {
  name   = "bad_example-1"
  region = "nyc3"

  forwarding_rule {
    entry_port     = 80
    entry_protocol = "http"

    target_port     = 80
    target_protocol = "http"
  }

  droplet_ids = [digitalocean_droplet.web.id]
}

resource "digitalocean_loadbalancer" "bad_example" {
  name   = "bad_example-1"
  region = "nyc3"

  forwarding_rule {
  entry_port     = 443
  entry_protocol = "https"

  target_port     = 443
  target_protocol = "https"
  }

  droplet_ids = [digitalocean_droplet.web.id]
}
