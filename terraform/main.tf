############################################
# Root Terraform Module
############################################

# -----------------------------
# VPC Module
# -----------------------------
module "vpc" {
  source = "./vpc"

  project      = "fastapi-devops"
  environment  = "dev"
  cluster_name = "fastapi-eks"

  cidr = "10.0.0.0/16"

  availability_zones = [
    "ap-south-1a",
    "ap-south-1b"
  ]

  public_subnets = [
    "10.0.1.0/24",
    "10.0.2.0/24"
  ]

  private_subnets = [
    "10.0.101.0/24",
    "10.0.102.0/24"
  ]
}

# -----------------------------
# ECR Module
# -----------------------------
module "ecr" {
  source = "./ecr"
  repository_name = "fastapi-devops"
  project         = "fastapi-devops"
  environment     = "dev"
}

# -----------------------------
# EKS Module
# -----------------------------
module "eks" {
  source = "./eks"

  vpc_id         = module.vpc.vpc_id
  public_subnets = module.vpc.public_subnets
}

module "rds" {
  source = "./rds"

  project        = var.project
  environment    = var.environment
  vpc_id         = module.vpc.vpc_id
  public_subnets = module.vpc.public_subnets

  db_name     = var.db_name
  db_username = var.db_username
  db_password = var.db_password
}
