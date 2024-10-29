terraform {
  required_providers {
    scaleway = {
      source = "scaleway/scaleway"
    }
  }
  required_version = ">= 0.13"
}

variable "project_id" {
  type        = string
  description = "Your project ID."
  default     = var.SCW_PROJECT_ID
}

provider "scaleway" {
  region = "fr-par"
  zone   = "fr-par-1"
}

# Create Private Network
resource "scaleway_vpc_private_network" "pvn" {
  project_id = var.project_id
  name       = "k8s-private-network"
}

# Kubernetes Cluster
resource "scaleway_k8s_cluster" "cluster" {
  name                = "k8s-cluster"
  version             = "1.30.2"
  cni                 = "cilium"
  private_network_id  = scaleway_vpc_private_network.pvn.id
  delete_additional_resources = false
}

# Kubernetes Pool (Nodes)
resource "scaleway_k8s_pool" "pool" {
  cluster_id   = scaleway_k8s_cluster.cluster.id
  name         = "k8s-pool"
  node_type    = "DEV1-M"
  size         = 2
  autoscaling  = false
  autohealing  = true
}

# Output kubeconfig for GitHub Actions
output "kubeconfig" {
  value = jsonencode({
    host                   = scaleway_k8s_cluster.cluster.kubeconfig[0].host
    token                  = scaleway_k8s_cluster.cluster.kubeconfig[0].token
    cluster_ca_certificate = scaleway_k8s_cluster.cluster.kubeconfig[0].cluster_ca_certificate
  })
  sensitive = true
}
