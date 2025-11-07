#!/bin/bash
# k8s/deploy.sh - Simple k8s deployment script

set -e

NAMESPACE="default"
DOCKER_IMAGE="${DOCKER_USERNAME}/elearn:latest"

echo "Deploying E-Learning Platform to Kubernetes..."
echo "Namespace: $NAMESPACE"
echo "Image: $DOCKER_IMAGE"

# Apply manifests
kubectl apply -f k8s/configmap.yaml
kubectl apply -f k8s/secrets.yaml
kubectl apply -f k8s/deployment.yaml
kubectl apply -f k8s/service.yaml

# Wait for deployment to be ready
echo "Waiting for deployment to be ready..."
kubectl rollout status deployment/elearn-app -n $NAMESPACE --timeout=5m

# Get service info
echo ""
echo "Deployment complete! Service info:"
kubectl get svc elearn-service -n $NAMESPACE
echo ""
echo "Access the app via the EXTERNAL-IP (on cloud providers) or localhost:80 (local)"
