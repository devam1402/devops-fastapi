# Monitoring Stack – Prometheus & Grafana

This project uses Prometheus and Grafana to monitor the Kubernetes cluster
and FastAPI application running on Amazon EKS.

The monitoring stack is installed using the **kube-prometheus-stack Helm chart**.



 🔧 Tools Used

- Prometheus
- Grafana
- kube-state-metrics
- node-exporter
- Alertmanager
- Helm



 📦 Installation

```bash
kubectl create namespace monitoring

helm repo add prometheus-community https://prometheus-community.github.io/helm-charts
helm repo update

helm install monitoring prometheus-community/kube-prometheus-stack \
  --namespace monitoring \
  -f monitoring/values.yaml
