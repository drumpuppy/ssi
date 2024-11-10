terraform {
  required_providers {
    scaleway = {
      source = "scaleway/scaleway"
    }
  }
  required_version = ">= 0.13"

  backend "remote" {
    organization = "ssi-soc-ia"
    workspaces {
      name = "ssi"
    }
  }
}

variable "scw_access_key" {
  type        = string
  description = "Scaleway access key"
}

variable "scw_secret_key" {
  type        = string
  description = "Scaleway secret key"
}

variable "scw_project_id" {
  type        = string
  description = "Scaleway project ID"
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
  access_key = var.scw_access_key
  secret_key = var.scw_secret_key
  project_id = var.scw_project_id
  region     = var.region
  zone       = var.zone
}

# Private Virtual Network
resource "scaleway_vpc_private_network" "pvn" {
  name       = "k8s-private-network"
  project_id = var.scw_project_id
}

# Sous-réseau public pour le Load Balancer
resource "scaleway_vpc_private_network_subnet" "public_subnet" {
  vpc_id     = scaleway_vpc_private_network.pvn.id
  region     = var.region
  zone       = var.zone
  cidr_block = "192.168.1.0/24"

  tags = ["public"]
}

# Sous-réseau privé pour le cluster et les nœuds
resource "scaleway_vpc_private_network_subnet" "private_subnet" {
  vpc_id     = scaleway_vpc_private_network.pvn.id
  region     = var.region
  zone       = var.zone
  cidr_block = "192.168.2.0/24"

  tags = ["private"]
}

# Kubernetes Cluster
resource "scaleway_k8s_cluster" "cluster" {
  name        = "k8s-cluster"
  version     = "1.30.2"
  cni         = "cilium"
  region      = var.region
  description = "Scaleway Kubernetes Cluster"
  type        = "kapsule"

  auto_upgrade {
    enable                      = false
    maintenance_window_day      = "sunday"
    maintenance_window_start_hour = "3"
  }

  autoscaler_config {
    balance_similar_node_groups = true
  }

  delete_additional_resources = false

  private_network_id          = scaleway_vpc_private_network.pvn.id
  private_network_subnet_id   = scaleway_vpc_private_network_subnet.private_subnet.id
}

# Kubernetes Pool
resource "scaleway_k8s_pool" "pool" {
  cluster_id        = scaleway_k8s_cluster.cluster.id
  name              = "k8s-pool"
  node_type         = "PLAY2-MICRO"
  size              = 2
  min_size          = 2
  max_size          = 2
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
  project_id              = var.scw_project_id
  ip_ids                  = [scaleway_lb_ip.lb_ip.id]
  zone                    = var.zone
  ssl_compatibility_level = "ssl_compatibility_level_intermediate"

  private_network {
    private_network_id = scaleway_vpc_private_network.pvn.id
    subnet_id          = scaleway_vpc_private_network_subnet.public_subnet.id
  }
  depends_on = [scaleway_vpc_private_network.pvn]
}

# Load Balancer IP
resource "scaleway_lb_ip" "lb_ip" {
  project_id = var.scw_project_id
  zone       = var.zone
}
