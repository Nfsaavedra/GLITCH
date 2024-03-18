resource "kubernetes_network_policy" "bad_example" {
  metadata {
    name      = "terraform-example-network-policy"
    namespace = "default"
  }

  spec {
    pod_selector {
      match_expressions {
        operator = "In"
        values   = ["webfront", "api"]
      }
    }

    ingress {
      ports {
        port     = "http"
        protocol = "TCP"
      }
      ports {
        port     = "8125"
        protocol = "UDP"
      }

      from {
        ip_block {
          cidr = "0.0.0.0/0"
          except = [
            "10.0.0.0/24",
            "10.0.1.0/24",
          ]
        }
      }
    }

    egress {
      ports {
        port     = "http"
        protocol = "TCP"
      }
      ports {
        port     = "8125"
        protocol = "UDP"
      }

      to {
        ip_block {
          cidr = "10.0.0.0/16"
          except = [
            "10.0.0.0/24",
            "10.0.1.0/24",
          ]
        }
      }
    }

    policy_types = ["Ingress", "Egress"]
  }
}

resource "kubernetes_network_policy" "good_example" {
  metadata {
    name      = "terraform-example-network-policy"
    namespace = "default"
  }

  spec {
    pod_selector {
      match_expressions {
        operator = "In"
        values   = ["webfront", "api"]
      }
    }

    ingress {
      ports {
        port     = "http"
        protocol = "TCP"
      }
      ports {
        port     = "8125"
        protocol = "UDP"
      }

      from {
        ip_block {
          cidr = "10.0.0.0/16"
          except = [
            "10.0.0.0/24",
            "10.0.1.0/24",
          ]
        }
      }
    }

    egress {
      ports {
        port     = "http"
        protocol = "TCP"
      }
      ports {
        port     = "8125"
        protocol = "UDP"
      }

      to {
        ip_block {
          cidr = "10.0.0.0/16"
          except = [
            "10.0.0.0/24",
            "10.0.1.0/24",
          ]
        }
      }
    }

    policy_types = ["Ingress", "Egress"]
  }
}
