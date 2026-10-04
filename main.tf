terraform {
  required_providers {
    local = {
      source  = "hashicorp/local"
      version = "~> 2.5"
    }
  }
}

provider "local" {}

resource "local_file" "environment" {
  filename = "${path.module}/${terraform.workspace}.txt"

  content = <<-EOT
    Environment: ${terraform.workspace}
    Managed by Terraform Workspace
  EOT
}
