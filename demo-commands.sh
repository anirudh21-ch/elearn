#!/bin/bash
# 🚀 E-Learning Platform - Quick Demo Commands
# Copy-paste these commands during your presentation

# ============================================
# SETUP - Run these BEFORE presentation
# ============================================

# Start minikube
minikube start --cpus=2 --memory=2048

# Start all port-forwards in background
kubectl port-forward svc/elearn-service 8080:80 > /dev/null 2>&1 &
kubectl port-forward svc/prometheus-kube-prometheus-prometheus 9090:9090 > /dev/null 2>&1 &
kubectl port-forward svc/prometheus-grafana 3000:80 > /dev/null 2>&1 &

# Get Grafana password
echo "Grafana Password:"
kubectl get secret prometheus-grafana -o jsonpath="{.data.admin-password}" | base64 -d && echo

# ============================================
# DEMO 1: Project Overview
# ============================================

cd "/Users/anirudhbabuch/Documents/projects/e learning platform"
ls -la
ls -la app/
ls -la k8s/
ls -la .github/workflows/

# ============================================
# DEMO 2: Code & Tests
# ============================================

source .venv/bin/activate
pytest -v
cat requirements.txt

# Optional: Run Flask server locally
# PORT=5001 python -m app.main
# In another terminal: curl -I http://localhost:5001/
# Press Ctrl+C to stop

# ============================================
# DEMO 3: Docker
# ============================================

cat Dockerfile
docker-compose up -d
docker-compose ps
curl -I http://localhost:5001/

# ============================================
# DEMO 4: Security Scan
# ============================================

trivy image --severity HIGH,CRITICAL elearn:latest

# ============================================
# DEMO 5: GitHub Actions & Docker Hub
# ============================================

# Open in browser:
# https://github.com/anirudh21-ch/e-learning/actions
# https://hub.docker.com/r/anirudh2105/elearn

# Live push demo:
echo "# Demo update - $(date)" >> README.md
git add README.md
git commit -m "demo: live presentation update"
git push origin main

# ============================================
# DEMO 6: Kubernetes
# ============================================

kubectl get all
kubectl get pods -o wide
kubectl get svc
kubectl logs -l app=elearn-app --tail=20

POD_NAME=$(kubectl get pods -l app=elearn-app -o jsonpath='{.items[0].metadata.name}')
kubectl describe pod $POD_NAME | head -50

curl -I http://localhost:8080/

# ============================================
# DEMO 7: Monitoring
# ============================================

# Prometheus: http://localhost:9090
# Grafana: http://localhost:3000 (admin / password from setup)

kubectl get pods | grep prometheus
kubectl get pods | grep grafana

# ============================================
# DEMO 8: API Testing
# ============================================

# Register student
curl -X POST http://localhost:8080/register \
  -H "Content-Type: application/json" \
  -d '{"username":"demo_student","password":"pass123","role":"student"}'

# Register teacher
curl -X POST http://localhost:8080/register \
  -H "Content-Type: application/json" \
  -d '{"username":"demo_teacher","password":"pass123","role":"teacher"}'

# Login and get token
TOKEN=$(curl -s -X POST http://localhost:8080/login \
  -H "Content-Type: application/json" \
  -d '{"username":"demo_teacher","password":"pass123"}' \
  | grep -o '"access_token":"[^"]*' | cut -d'"' -f4)

echo "Token: $TOKEN"

# Create course (teacher only)
curl -X POST http://localhost:8080/courses \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $TOKEN" \
  -d '{"title":"DevOps Fundamentals","description":"Learn Docker, Kubernetes, CI/CD"}'

# List courses
curl http://localhost:8080/courses | jq .

# Get profile
curl http://localhost:8080/profile -H "Authorization: Bearer $TOKEN" | jq .

# View metrics
curl http://localhost:8080/metrics | grep flask

# ============================================
# DEMO 9: Self-Healing & Scaling
# ============================================

# Show current pods
kubectl get pods -l app=elearn-app

# Delete one pod (self-healing demo)
POD_TO_DELETE=$(kubectl get pods -l app=elearn-app -o jsonpath='{.items[0].metadata.name}')
kubectl delete pod $POD_TO_DELETE
kubectl get pods -l app=elearn-app -w  # Press Ctrl+C after new pod starts

# Scale up
kubectl scale deployment elearn-app --replicas=4
kubectl get pods -l app=elearn-app -w  # Press Ctrl+C after 4 pods running

# Scale down
kubectl scale deployment elearn-app --replicas=2
kubectl get pods -l app=elearn-app

# ============================================
# DEMO 10: Final Stats
# ============================================

echo "=== Project Statistics ==="
find . -type f ! -path "./.git/*" ! -path "./.venv/*" ! -path "./instance/*" | wc -l
find app tests -name "*.py" -exec wc -l {} + | tail -1
kubectl get all --no-headers | wc -l
docker images elearn:latest --format "{{.Size}}"
pytest --tb=no -q

# ============================================
# CLEANUP - After presentation
# ============================================

pkill -f "kubectl port-forward"
docker-compose down
# minikube stop  # Optional
deactivate
