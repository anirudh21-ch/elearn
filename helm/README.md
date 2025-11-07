# E-Learning Platform - Helm Chart

A Helm chart for deploying the E-Learning Portal to Kubernetes.

## Quick Start

```bash
helm install elearn ./helm/elearn-chart
```

## Values

See `helm/elearn-chart/values.yaml` for configuration options.

## Prerequisites

- Kubernetes cluster (local: minikube, or cloud: EKS, GKE, AKS)
- Helm 3+
- kubectl configured to access your cluster
