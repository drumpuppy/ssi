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
  description = "Your Scaleway project ID."
}

variable "region" {
  type        = string
  default     = "fr-par"
  description = "Scaleway region."
}

variable "zone" {
  type        = string
  default     = "fr-par-1"
  description = "Scaleway zone."
}


provider "scaleway" {
  region = "fr-par"
  zone   = "fr-par-1"
}

# Private Virtual Network
resource "scaleway_vpc_private_network" "pvn" {
  name       = "k8s-private-network"
  project_id = var.project_id
}

# Kubernetes Cluster
resource "scaleway_k8s_cluster" "cluster" {
  name              = "k8s-cluster"
  version           = "1.30.2"
  cni               = "cilium"
  region            = var.region
  description       = "Scaleway Kubernetes Cluster"
  type              = "kapsule"
  private_network_id = scaleway_vpc_private_network.pvn.id
}

# Kubernetes Pool
resource "scaleway_k8s_pool" "pool" {
  cluster_id        = scaleway_k8s_cluster.cluster.id
  name              = "k8s-pool"
  node_type         = "PLAY2-NANO"
  size              = 1
  min_size          = 1
  max_size          = 1
  autohealing       = true
  autoscaling       = false
  container_runtime = "containerd"
  zone              = var.zone

  upgrade_policy {
    max_surge       = 1
    max_unavailable = 1
  }
}

# Load Balancer
resource "scaleway_lb" "lb" {
  name                    = "k8s-lb"
  description             = "Load Balancer for Kubernetes"
  type                    = "lb-s"
  project_id              = var.project_id
  ip_ids                  = [scaleway_lb_ip.lb_ip.id]
  zone                    = var.zone
  ssl_compatibility_level = "ssl_compatibility_level_intermediate"
}

# Load Balancer IP
resource "scaleway_lb_ip" "lb_ip" {
  project_id = var.project_id
  zone       = var.zone
}
