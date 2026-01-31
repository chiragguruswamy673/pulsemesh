terraform {
  required_providers {
    kubernetes = {
      source  = "hashicorp/kubernetes"
      version = "~> 2.27"
    }
  }
}

provider "kubernetes" {
  config_path = "~/.kube/config"
}

resource "kubernetes_namespace" "pulsemesh" {
  metadata {
    name = "pulsemesh-system"
  }
}

resource "kubernetes_deployment" "pulsemesh_app" {
  metadata {
    name      = "pulsemesh-app"
    namespace = kubernetes_namespace.pulsemesh.metadata[0].name
    labels = {
      app = "pulsemesh"
    }
  }

  spec {
    replicas = 1

    selector {
      match_labels = {
        app = "pulsemesh"
      }
    }

    template {
      metadata {
        labels = {
          app = "pulsemesh"
        }
      }

      spec {
        container {
          name  = "pulsemesh"
          image = "pulsemesh-app:latest"
          image_pull_policy = "Never"

          port {
            container_port = 8000
          }
        }
      }
    }
  }
}
resource "kubernetes_service" "pulsemesh_service" {
  metadata {
    name      = "pulsemesh-app"
    namespace = kubernetes_namespace.pulsemesh.metadata[0].name
  }

  spec {
    selector = {
      app = "pulsemesh"
    }

    port {
      port        = 8000
      target_port = 8000
    }

    type = "ClusterIP"
  }
}

