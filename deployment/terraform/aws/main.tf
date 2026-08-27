# Terraform AWS Production Infrastructure Configuration for AegisFlow AI
terraform {
  required_version = ">= 1.5.0"
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 5.0"
    }
  }
}

provider "aws" {
  region = var.aws_region
}

variable "aws_region" {
  type    = string
  default = "us-east-1"
}

variable "environment" {
  type    = string
  default = "production"
}

resource "aws_vpc" "aegisflow_vpc" {
  cidr_block           = "10.0.0.0/16"
  enable_dns_hostnames = true
  enable_dns_support   = true

  tags = {
    Name        = "aegisflow-${var.environment}-vpc"
    Environment = var.environment
    ManagedBy   = "Terraform"
  }
}

resource "aws_subnet" "public_subnets" {
  count                   = 3
  vpc_id                  = aws_vpc.aegisflow_vpc.id
  cidr_block              = "10.0.${count.index + 1}.0/24"
  availability_zone       = data.aws_availability_zones.available.names[count.index]
  map_public_ip_on_launch = true

  tags = {
    Name = "aegisflow-public-subnet-${count.index + 1}"
  }
}

data "aws_availability_zones" "available" {
  state = "available"
}

resource "aws_msk_cluster" "aegisflow_kafka" {
  cluster_name           = "aegisflow-${var.environment}-kafka"
  kafka_version          = "3.5.1"
  number_of_broker_nodes = 3

  broker_node_group_info {
    instance_type   = "kafka.m5.xlarge"
    client_subnets  = aws_subnet.public_subnets[*].id
    security_groups = [aws_security_group.kafka_sg.id]
  }

  encryption_info {
    encryption_in_transit {
      client_broker = "TLS"
      in_cluster    = true
    }
  }

  tags = {
    Environment = var.environment
  }
}

resource "aws_security_group" "kafka_sg" {
  name        = "aegisflow-kafka-sg"
  description = "Security group for MSK Kafka brokers"
  vpc_id      = aws_vpc.aegisflow_vpc.id

  ingress {
    from_port   = 9092
    to_port     = 9096
    protocol    = "tcp"
    cidr_blocks = ["10.0.0.0/16"]
  }

  egress {
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]
  }
}

resource "aws_elasticache_replication_group" "aegisflow_redis" {
  replication_group_id          = "aegisflow-online-features"
  replication_group_description = "Vortex Online Feature Store Redis Cluster"
  node_type                     = "cache.r6g.xlarge"
  num_cache_clusters            = 3
  port                          = 6379
  automatic_failover_enabled    = true
  multi_az_enabled              = true
  at_rest_encryption_enabled    = true
  transit_encryption_enabled    = true

  tags = {
    Environment = var.environment
  }
}

resource "aws_eks_cluster" "aegisflow_eks" {
  name     = "aegisflow-${var.environment}-cluster"
  role_arn = aws_iam_role.eks_cluster_role.arn
  version  = "1.29"

  vpc_config {
    subnet_ids = aws_subnet.public_subnets[*].id
  }
}

resource "aws_iam_role" "eks_cluster_role" {
  name = "aegisflow-eks-cluster-role"

  assume_role_policy = jsonencode({
    Version = "2012-10-17"
    Statement = [{
      Action = "sts:AssumeRole"
      Effect = "Allow"
      Principal = {
        Service = "eks.amazonaws.com"
      }
    }]
  })
}
