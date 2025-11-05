terraform {
  required_providers {
    kubernetes = {
      source  = "hashicorp/kubernetes"
      version = "~> 2.32"
    }
  }
}

provider "kubernetes" {
  config_path = "~/terraform/.kube/config"
}

resource "kubernetes_namespace" "flask" {
  metadata {
    name = "flask-api"
  }
}

resource "kubernetes_config_map" "flask-config" {
  metadata {
    name      = "flask-config"
    namespace = kubernetes_namespace.flask.metadata[0].name
  }

  data = {
    APP_ENV = "production"
    DEBUG   = "false"
  }
}

resource "kubernetes_ingress_v1" "flask-ingress" {
  metadata {
    name      = "flask-api-ingress"
    namespace = kubernetes_namespace.flask.metadata[0].name
    annotations = {
      "nginx.ingress.kubernetes.io/rewrite-target" = "/"
    }
  }

  spec {
    rule {
      host = "flask.local"
      http {
        path {
          path = "/"
          path_type = "Prefix"
          backend {
            service {
              name = "flask-api-service"
              port {
                number = 5000
              }
            }
          }
        }
      }
    }
  }
}
