terraform {
  required_version = ">= 1.5.0"
  required_providers {
    kubernetes = {
      source  = "hashicorp/kubernetes"
      version = "~> 2.35"
    }
  }
}

provider "kubernetes" {
  config_path    = pathexpand("~/.kube/config")
  config_context = "kind-devops-cluster"
}

resource "kubernetes_namespace_v1" "capstone" {
  metadata {
    name = "production-capstone"
    labels = {
      "app.kubernetes.io/name" = "production-capstone"
      environment             = "production"
    }
  }
}

output "namespace" {
  value = kubernetes_namespace_v1.capstone.metadata[0].name
}
