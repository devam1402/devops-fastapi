# 🚀 devops-fastapi

> A production-ready FastAPI application with a complete DevOps pipeline — containerized with Docker, orchestrated on **Amazon EKS**, provisioned via Terraform on **AWS**, and monitored end-to-end.

---

## 📋 Table of Contents

- [Overview](#overview)
- [Architecture](#architecture)
- [Tech Stack](#tech-stack)
- [Project Structure](#project-structure)
- [Getting Started](#getting-started)
  - [Prerequisites](#prerequisites)
  - [Local Development](#local-development)
  - [Docker Compose](#docker-compose)
- [Database Migrations](#database-migrations)
- [Kubernetes Deployment](#kubernetes-deployment)
- [Infrastructure (Terraform)](#infrastructure-terraform)
- [AWS Services](#aws-services)
- [Monitoring](#monitoring)
- [CI/CD Pipeline](#cicd-pipeline)
- [Environment Variables](#environment-variables)
- [Contributing](#contributing)

---

## Overview

`devops-fastapi` is a **full-stack DevOps showcase** built around a FastAPI backend. It demonstrates how a modern Python API service is developed, containerized, deployed, and observed in production — covering the entire lifecycle from local dev to cloud infrastructure.

Key highlights:
- ⚡ **FastAPI** with async support and auto-generated OpenAPI docs
- 🐘 **PostgreSQL** with **Alembic** for schema migrations
- 🐳 **Docker & Docker Compose** for local and staging environments
- ☸️ **Amazon EKS** for scalable, resilient Kubernetes orchestration
- 🗄️ **Amazon RDS (PostgreSQL)** for managed cloud database
- 📦 **Amazon ECR** as the private container registry
- 🌍 **Terraform** for AWS infrastructure-as-code provisioning
- 📊 **Monitoring stack** (Prometheus / Grafana + CloudWatch) for observability
- 🔄 **GitHub Actions** CI/CD for automated testing and deployment

---

## Architecture

```
┌──────────────────────────────────────────────────────────────┐
│                     GitHub Actions CI/CD                      │
│          (lint → test → build → push → deploy)               │
└──────────────────────┬───────────────────────────────────────┘
                       │ docker push
           ┌───────────▼───────────┐
           │   Amazon ECR           │  ← Private Container Registry
           │  (Container Images)    │
           └───────────┬───────────┘
                       │ image pull
┌──────────────────────▼───────────────────────────────────────┐
│                  AWS Cloud (Terraform-Provisioned)            │
│                                                              │
│  ┌─────────────────────────────────────────────────────┐    │
│  │                  Amazon EKS Cluster                  │    │
│  │  ┌─────────────┐  ┌──────────────┐  ┌───────────┐  │    │
│  │  │  FastAPI    │  │  Prometheus  │  │  Grafana  │  │    │
│  │  │  Pods (HPA) │  │  + CloudWatch│  │  Dashboard│  │    │
│  │  └──────┬──────┘  └──────────────┘  └───────────┘  │    │
│  └─────────│───────────────────────────────────────────┘    │
│            │                                                  │
│  ┌─────────▼──────┐   ┌─────────────┐   ┌───────────────┐  │
│  │  Amazon RDS    │   │  AWS Secrets│   │   AWS ALB     │  │
│  │  (PostgreSQL)  │   │  Manager    │   │ (Load Balancer│  │
│  └────────────────┘   └─────────────┘   └───────────────┘  │
│                                                              │
│  ┌─────────────────┐  ┌──────────────┐  ┌──────────────┐   │
│  │   Amazon VPC    │  │  IAM Roles & │  │  Amazon S3   │   │
│  │ (Subnets / SGs) │  │   Policies   │  │ (TF State)   │   │
│  └─────────────────┘  └──────────────┘  └──────────────┘   │
└──────────────────────────────────────────────────────────────┘
```

---

## Tech Stack

| Layer | Technology |
|---|---|
| API Framework | [FastAPI](https://fastapi.tiangolo.com/) |
| Language | Python 3.11+ |
| Database | PostgreSQL (local) / **Amazon RDS** (cloud) |
| ORM / Migrations | SQLAlchemy + Alembic |
| Containerization | Docker, Docker Compose |
| Container Registry | **Amazon ECR** |
| Orchestration | Kubernetes / **Amazon EKS** |
| Networking | **Amazon VPC**, ALB, Security Groups |
| Secrets | **AWS Secrets Manager** |
| IaC | Terraform (HCL) on **AWS** |
| TF State Backend | **Amazon S3** + DynamoDB lock |
| Monitoring | Prometheus + Grafana + **Amazon CloudWatch** |
| CI/CD | GitHub Actions |

---

## Project Structure

```
devops-fastapi/
├── .github/
│   └── workflows/           # GitHub Actions CI/CD pipelines
├── alembic/                 # Alembic migration scripts
│   └── versions/
├── app/                     # FastAPI application source
│   ├── api/                 # Route handlers / endpoints
│   ├── core/                # Config, settings, security
│   ├── db/                  # Database session, base models
│   ├── models/              # SQLAlchemy ORM models
│   ├── schemas/             # Pydantic request/response schemas
│   └── main.py              # App entrypoint
├── k8s/                     # Kubernetes manifests
│   ├── deployment.yaml
│   ├── service.yaml
│   ├── ingress.yaml
│   └── configmap.yaml
├── monitoring/              # Prometheus & Grafana configs
├── terraform/               # Infrastructure as Code (HCL)
├── alembic.ini              # Alembic configuration
├── debug_settings.py        # Local debug overrides
├── docker-compose.yml       # Multi-service local stack
├── Dockerfile               # Production container image
├── requirements.txt         # Python dependencies
└── test_connection.py       # Database connectivity test
```

---

## Getting Started

### Prerequisites

Make sure you have the following installed:

- [Python 3.11+](https://www.python.org/)
- [Docker](https://www.docker.com/) & [Docker Compose](https://docs.docker.com/compose/)
- [kubectl](https://kubernetes.io/docs/tasks/tools/) (for Kubernetes deployment)
- [AWS CLI v2](https://docs.aws.amazon.com/cli/latest/userguide/install-cliv2.html) — configured with `aws configure`
- [eksctl](https://eksctl.io/) (for EKS cluster management)
- [Terraform](https://www.terraform.io/) (for infrastructure provisioning)

---

### Local Development

1. **Clone the repository**

```bash
git clone https://github.com/devam1402/devops-fastapi.git
cd devops-fastapi
```

2. **Create a virtual environment and install dependencies**

```bash
python -m venv venv
source venv/bin/activate        # On Windows: venv\Scripts\activate
pip install -r requirements.txt
```

3. **Set up environment variables**

```bash
cp .env.example .env
# Edit .env with your database credentials and settings
```

4. **Run the development server**

```bash
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

The API will be available at `http://localhost:8000`
Interactive docs at `http://localhost:8000/docs`

---

### Docker Compose

Spin up the full stack (FastAPI + PostgreSQL) locally with a single command:

```bash
docker-compose up --build
```

| Service | URL |
|---|---|
| FastAPI API | http://localhost:8000 |
| Swagger UI | http://localhost:8000/docs |
| ReDoc | http://localhost:8000/redoc |
| PostgreSQL | localhost:5432 |

To shut down:

```bash
docker-compose down
```

To also remove volumes:

```bash
docker-compose down -v
```

---

## Database Migrations

This project uses **Alembic** for database schema migrations.

**Apply all migrations:**

```bash
alembic upgrade head
```

**Create a new migration after model changes:**

```bash
alembic revision --autogenerate -m "describe your change here"
```

**Rollback one step:**

```bash
alembic downgrade -1
```

**Test the database connection:**

```bash
python test_connection.py
```

---

## Kubernetes Deployment (Amazon EKS)

All Kubernetes manifests live in the `k8s/` directory. The cluster runs on **Amazon EKS**, provisioned via Terraform.

**Configure kubectl for EKS:**

```bash
aws eks update-kubeconfig --region <aws-region> --name <cluster-name>
```

**Apply all manifests:**

```bash
kubectl apply -f k8s/
```

**Check deployment status:**

```bash
kubectl get pods -n <your-namespace>
kubectl get svc -n <your-namespace>
```

**View application logs:**

```bash
kubectl logs -f deployment/devops-fastapi -n <your-namespace>
```

**Scale the deployment:**

```bash
kubectl scale deployment devops-fastapi --replicas=3 -n <your-namespace>
```

> 💡 The EKS cluster uses an **Application Load Balancer (ALB)** via the AWS Load Balancer Controller — check `k8s/ingress.yaml` for the ingress configuration.

---

## Infrastructure (Terraform)

Cloud infrastructure is managed with Terraform in the `terraform/` directory, targeting **AWS**.

**AWS resources provisioned:**

| Resource | AWS Service |
|---|---|
| Kubernetes Cluster | Amazon EKS |
| Managed Database | Amazon RDS (PostgreSQL) |
| Container Registry | Amazon ECR |
| Networking | VPC, Public/Private Subnets, NAT Gateway |
| Load Balancer | Application Load Balancer (ALB) |
| Secret Storage | AWS Secrets Manager |
| Terraform State | S3 bucket + DynamoDB table (locking) |
| IAM | Roles & Policies for EKS node groups |

**Deploy infrastructure:**

```bash
cd terraform/

# Configure AWS credentials
aws configure

# Initialize with S3 backend
terraform init

# Preview planned changes
terraform plan -var-file="terraform.tfvars"

# Apply infrastructure changes
terraform apply -var-file="terraform.tfvars"
```

**Destroy infrastructure:**

```bash
terraform destroy -var-file="terraform.tfvars"
```

> ⚠️ Set your AWS region and credentials in `terraform/terraform.tfvars` before applying. Never commit this file — it's in `.gitignore`.

---

## AWS Services

A breakdown of every AWS service used in this project and its role in the stack:

| AWS Service | Purpose |
|---|---|
| **Amazon EKS** | Managed Kubernetes control plane — runs the FastAPI workloads with auto-scaling node groups |
| **Amazon ECR** | Private Docker container registry — stores and versions all application images |
| **Amazon RDS (PostgreSQL)** | Managed relational database with automated backups, Multi-AZ failover, and parameter groups |
| **Amazon VPC** | Isolated network with public subnets (ALB), private subnets (EKS nodes, RDS), and NAT Gateway |
| **Application Load Balancer** | Terminates HTTPS, routes traffic to EKS pods via the AWS Load Balancer Controller |
| **AWS Secrets Manager** | Stores DB credentials, JWT secrets, and API keys — mounted as K8s secrets at runtime |
| **Amazon S3** | Stores the Terraform remote state file; also available for application object storage |
| **IAM Roles & Policies** | Scoped permissions for EKS node groups, IRSA (IAM Roles for Service Accounts), and CI/CD |
| **Amazon CloudWatch** | Collects EKS cluster logs, container insights, and custom API metrics via the CloudWatch agent |

### Pushing to Amazon ECR

```bash
# Authenticate Docker to ECR
aws ecr get-login-password --region <aws-region> | \
  docker login --username AWS --password-stdin <account-id>.dkr.ecr.<aws-region>.amazonaws.com

# Build and tag the image
docker build -t devops-fastapi .
docker tag devops-fastapi:latest <account-id>.dkr.ecr.<aws-region>.amazonaws.com/devops-fastapi:latest

# Push to ECR
docker push <account-id>.dkr.ecr.<aws-region>.amazonaws.com/devops-fastapi:latest
```

> 💡 In CI/CD, this is handled automatically by the GitHub Actions workflow using OIDC federation — no long-lived AWS credentials stored in secrets.

---

## Monitoring

The `monitoring/` directory contains configuration for a **Prometheus + Grafana** observability stack, complemented by **Amazon CloudWatch** in the cloud environment.

**Start the monitoring stack (local):**

```bash
docker-compose -f monitoring/docker-compose.monitoring.yml up -d
```

| Service | URL |
|---|---|
| Prometheus | http://localhost:9090 |
| Grafana | http://localhost:3000 |

FastAPI exposes metrics at `/metrics` (via `prometheus-fastapi-instrumentator`).

**CloudWatch on EKS:**

Container Insights is enabled on the EKS cluster, sending pod-level CPU, memory, and network metrics to CloudWatch automatically via the CloudWatch agent DaemonSet. Log groups are created per namespace under `/aws/containerinsights/<cluster-name>/`.

---

## CI/CD Pipeline

GitHub Actions workflows are located in `.github/workflows/`. The pipeline runs automatically on push to `main` and on pull requests.

**Pipeline stages:**

```
Push to main
    │
    ├── 1. Lint & Format Check (ruff / black)
    ├── 2. Unit & Integration Tests (pytest)
    ├── 3. Configure AWS credentials (OIDC)
    ├── 4. Build & Push Docker image → Amazon ECR
    ├── 5. Update kubeconfig for Amazon EKS
    └── 6. Deploy to EKS (kubectl apply / Helm upgrade)
```

AWS authentication in CI uses **GitHub OIDC + IAM Role federation** — no static access keys stored in GitHub Secrets.

---

## Environment Variables

| Variable | Description | Default |
|---|---|---|
| `DATABASE_URL` | PostgreSQL connection string (local) | `postgresql://user:pass@localhost/db` |
| `SECRET_KEY` | JWT signing secret | — |
| `ALGORITHM` | JWT algorithm | `HS256` |
| `ACCESS_TOKEN_EXPIRE_MINUTES` | Token expiry | `30` |
| `DEBUG` | Enable debug mode | `false` |
| `ALLOWED_ORIGINS` | CORS origins (comma-separated) | `*` |
| `AWS_REGION` | AWS region for all services | `us-east-1` |
| `ECR_REGISTRY` | ECR registry URL | `<account-id>.dkr.ecr.<region>.amazonaws.com` |
| `ECR_REPOSITORY` | ECR repository name | `devops-fastapi` |
| `EKS_CLUSTER_NAME` | EKS cluster name (for kubeconfig) | — |
| `RDS_HOST` | RDS instance endpoint (injected via Secrets Manager) | — |

> 🔐 In production, all secrets are stored in **AWS Secrets Manager** and injected into EKS pods at runtime via the AWS Secrets Store CSI Driver — not hardcoded in `.env` files.


---

<div align="center">

Built with ❤️ by [devam1402](https://github.com/devam1402)

</div>

