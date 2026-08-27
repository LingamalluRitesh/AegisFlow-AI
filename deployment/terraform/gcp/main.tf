# Terraform GCP Production Infrastructure for AegisFlow AI
terraform {
  required_version = ">= 1.5.0"
  required_providers {
    google = {
      source  = "hashicorp/google"
      version = "~> 5.0"
    }
  }
}

provider "google" {
  project = var.gcp_project_id
  region  = var.gcp_region
}

variable "gcp_project_id" {
  type    = string
  default = "aegisflow-cloud-production"
}

variable "gcp_region" {
  type    = string
  default = "us-central1"
}

resource "google_container_cluster" "primary" {
  name     = "aegisflow-gke-cluster"
  location = var.gcp_region

  remove_default_node_pool = true
  initial_node_count       = 1

  network    = "default"
  subnetwork = "default"
}

resource "google_container_node_pool" "primary_nodes" {
  name       = "aegisflow-node-pool"
  location   = var.gcp_region
  cluster    = google_container_cluster.primary.name
  node_count = 5

  node_config {
    preemptible  = false
    machine_type = "e2-standard-8"

    oauth_scopes = [
      "https://www.googleapis.com/auth/cloud-platform"
    ]
  }
}
