# 🚀 Quick Reference Guide

> **Last Updated**: November 7, 2025  
> **Project**: E-Learning Platform with Secure DevOps Pipeline

---

## 📋 Table of Contents

1. [Local Development](#local-development)
2. [Docker & Compose](#docker--compose)
3. [Testing & Security](#testing--security)
4. [GitHub Actions & CI/CD](#github-actions--cicd)
5. [Kubernetes Deployment](#kubernetes-deployment)
6. [Monitoring & Logs](#monitoring--logs)
7. [Troubleshooting](#troubleshooting)
8. [Database Operations](#database-operations)
9. [API Testing](#api-testing)

---

## Local Development

### First-Time Setup

```bash
# Navigate to project
cd ~/Documents/projects/e\ learning\ platform

# Create virtual environment
python3 -m venv .venv
source .venv/bin/activate  # macOS/Linux
# .venv\Scripts\activate  # Windows

# Install dependencies
pip install --upgrade pip
pip install -r requirements.txt

# Create database and run app
python -m app.main
# App available at http://127.0.0.1:5001
```

### Daily Development Workflow

```bash
# Activate virtual environment
source .venv/bin/activate

# Set environment variables (optional)
export FLASK_ENV=development
export ADMIN_USERNAME=admin
export ADMIN_PASSWORD=admin
export PORT=5001

# Run the app
python -m app.main

# In another terminal: Run tests
pytest -v
pytest --cov=app tests/

# Format code (optional)
black app/

# Lint code (optional)
flake8 app/
```

### Environment Variables Reference

```bash
# Development
export FLASK_ENV=development          # or 'production'
export FLASK_DEBUG=1                  # Enable debug mode
export PORT=5001                      # App port (default: 5000)
export ADMIN_USERNAME=admin           # Admin user (default: admin)
export ADMIN_PASSWORD=admin           # Admin password (default: admin)

# Database
export SQLALCHEMY_DATABASE_URI=sqlite:///instance/elearn.db
# PostgreSQL example:
# export SQLALCHEMY_DATABASE_URI=postgresql://user:pass@localhost:5432/elearn

# JWT
export JWT_SECRET_KEY=$(openssl rand -hex 32)  # Generate random key

# Security
export SECURITY_PASSWORD_SALT=$(openssl rand -hex 32)
```

### File Structure Quick Look

```
e learning platform/
├── app/                    # Application package
│   ├── __init__.py        # Flask app factory
│   ├── main.py            # Entry point
│   ├── models.py          # Database models
│   ├── routes.py          # API routes
│   └── templates/         # HTML templates
│       ├── base.html
│       ├── index.html
│       ├── register.html
│       ├── login.html
│       ├── profile.html
│       └── courses.html
├── instance/              # Instance folder (gitignored)
│   └── elearn.db         # SQLite database
├── tests/                 # Test suite
│   └── test_app.py
├── .github/workflows/     # GitHub Actions
│   └── ci.yml
├── k8s/                   # Kubernetes manifests
│   ├── deployment.yaml
│   ├── service.yaml
│   ├── configmap.yaml
│   ├── secrets.yaml
│   └── deploy.sh
├── helm/                  # Helm chart
│   └── elearn-chart/
│       ├── Chart.yaml
│       ├── values.yaml
│       └── README.md
├── Dockerfile            # Container definition
├── docker-compose.yml    # Multi-service orchestration
├── nginx.conf            # Reverse proxy config
├── requirements.txt      # Python dependencies
├── REQUIREMENTS.md       # This file
├── DEVOPS_GUIDE.md      # Step-by-step pipeline guide
└── README.md            # Project overview
```

---

## Docker & Compose

### Build & Run Locally

```bash
# Build Docker image
docker build -t elearn:latest .

# Run container standalone
docker run -it -p 5000:5000 elearn:latest
docker run -it -p 5001:5000 -e PORT=5001 elearn:latest

# View images
docker images | grep elearn

# View running containers
docker ps
```

### Docker Compose Commands

```bash
# Start services (build if needed)
docker-compose up --build

# Start in background
docker-compose up -d

# View logs
docker-compose logs -f              # All services
docker-compose logs -f web          # Flask app only
docker-compose logs -f nginx        # Nginx only

# Stop services
docker-compose down

# Remove volumes too
docker-compose down -v

# Restart specific service
docker-compose restart web
docker-compose restart nginx

# Execute command in running container
docker-compose exec web bash
docker-compose exec web python -m pytest

# View running containers in compose
docker-compose ps

# View service network
docker network ls | grep elearn
docker network inspect elearn-net
```

### Docker Cleanup

```bash
# Remove unused images
docker image prune

# Remove unused containers
docker container prune

# Remove unused networks
docker network prune

# Remove unused volumes
docker volume prune

# Clean everything (caution!)
docker system prune -a
```

### Docker Debugging

```bash
# Build with detailed output
docker build --progress=plain -t elearn:latest .

# Inspect image layers
docker history elearn:latest

# Check image size
docker images elearn

# Get image configuration
docker inspect elearn:latest

# Run with debug shell
docker run -it elearn:latest /bin/bash
```

---

## Testing & Security

### Unit Tests

```bash
# Run all tests
pytest -v
pytest tests/test_app.py

# Run specific test
pytest tests/test_app.py::test_register_login -v

# Run with coverage
pytest --cov=app tests/
pytest --cov=app --cov-report=html tests/  # Generate HTML report

# Run with detailed output
pytest -vv -s

# Run and stop on first failure
pytest -x

# Run last failed tests only
pytest --lf
```

### Security Scanning

```bash
# Trivy: Scan Docker image
trivy image elearn:latest
trivy image --severity HIGH,CRITICAL elearn:latest

# Trivy: Scan filesystem
trivy fs .

# Trivy: Generate JSON report
trivy image --format json -o trivy-report.json elearn:latest

# OWASP Dependency Check (Python packages)
dependency-check --project "E-Learning Platform" --scan requirements.txt

# Hadolint: Lint Dockerfile
hadolint Dockerfile

# flake8: Lint Python code
flake8 app/

# bandit: Find security issues in Python
bandit -r app/
```

### Manual API Testing

```bash
# Health check
curl -i http://localhost/

# Register user
curl -X POST http://localhost/register \
  -H "Content-Type: application/json" \
  -d '{
    "username": "alice",
    "password": "pass123",
    "role": "student"
  }'

# Login (get token)
curl -X POST http://localhost/login \
  -H "Content-Type: application/json" \
  -d '{"username": "alice", "password": "pass123"}'
# Save token from response: TOKEN="eyJ..."

# Get courses (no auth required)
curl http://localhost/courses

# Create course (requires teacher/admin token)
curl -X POST http://localhost/courses \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $TOKEN" \
  -d '{
    "title": "Python Basics",
    "description": "Learn Python fundamentals"
  }'

# Get profile (requires token)
curl http://localhost/api/profile \
  -H "Authorization: Bearer $TOKEN"

# Metrics
curl http://localhost/metrics
```

---

## GitHub Actions & CI/CD

### GitHub Repo Setup

```bash
# Initialize Git (if new repo)
cd ~/Documents/projects/e\ learning\ platform
git init
git add .
git commit -m "Initial commit: E-Learning platform with DevOps"

# Add remote
git remote add origin https://github.com/YOUR_USERNAME/elearn.git
git branch -M main
git push -u origin main

# Create GitHub Secrets
# 1. Go to repo → Settings → Secrets and variables → Actions
# 2. Add DOCKER_USERNAME: your_docker_hub_username
# 3. Add DOCKER_PASSWORD: your_docker_hub_access_token (NOT password!)
# 4. (Optional) Add SONAR_TOKEN: your_sonarqube_token
```

### Trigger CI/CD Pipeline

```bash
# Push to main branch (triggers workflow)
git add .
git commit -m "Updated app logic"
git push origin main

# Push to develop branch (workflow runs, no push to registry)
git checkout -b develop
git push origin develop

# View workflow status
# Go to repo → Actions tab in GitHub UI

# Force rebuild (push empty commit)
git commit --allow-empty -m "Rebuild"
git push origin main
```

### Check Workflow Logs

```bash
# Via GitHub UI:
# 1. Go to repo → Actions
# 2. Click workflow run
# 3. Click job to see logs

# Via GitHub CLI (if installed):
gh run list --repo YOUR_USERNAME/elearn
gh run view <RUN_ID> --log
```

---

## Kubernetes Deployment

### Prerequisites

```bash
# Install tools
brew install kubectl minikube helm  # macOS
# Or use apt-get for Linux

# Start minikube cluster
minikube start --cpus=4 --memory=8192

# Check cluster status
kubectl cluster-info
kubectl get nodes
```

### Deploy to Kubernetes

```bash
# Using kubectl directly
kubectl apply -f k8s/

# Or use provided script
bash k8s/deploy.sh

# Check deployment status
kubectl get deployments
kubectl get pods
kubectl get services

# Check pod logs
kubectl logs -f deployment/elearn

# Get specific pod logs
kubectl logs <POD_NAME>

# Port forward to access service locally
kubectl port-forward service/elearn 8080:80
# Access at http://localhost:8080

# Get service details
kubectl describe service elearn
```

### Deploy with Helm

```bash
# Install Helm chart
helm install elearn ./helm/elearn-chart

# Check installation
helm list
helm status elearn

# Upgrade release
helm upgrade elearn ./helm/elearn-chart --set replicaCount=3

# Uninstall
helm uninstall elearn

# Override values
helm install elearn ./helm/elearn-chart \
  --set replicaCount=2 \
  --set image.tag=v1.0 \
  --set admin.username=superadmin \
  --set admin.password=secure123
```

### Scale & Update

```bash
# Scale deployment
kubectl scale deployment elearn --replicas=5

# Update image
kubectl set image deployment/elearn elearn=elearn:v2.0 --record

# Check rollout status
kubectl rollout status deployment/elearn

# Rollback to previous version
kubectl rollout undo deployment/elearn
kubectl rollout undo deployment/elearn --to-revision=1
```

### Debug Kubernetes

```bash
# Exec into pod
kubectl exec -it <POD_NAME> -- /bin/bash

# Describe pod (detailed info)
kubectl describe pod <POD_NAME>

# View events
kubectl get events --sort-by='.lastTimestamp'

# Check resource usage
kubectl top nodes
kubectl top pods

# View pod resources
kubectl describe pod <POD_NAME> | grep -A 5 "Requests"

# Check cluster networking
kubectl get svc
kubectl get ingress
```

### Cleanup Kubernetes

```bash
# Delete all resources
kubectl delete -f k8s/

# Or use helm
helm uninstall elearn

# Stop minikube
minikube stop

# Delete minikube cluster
minikube delete
```

---

## Monitoring & Logs

### Prometheus Setup

```bash
# Add Prometheus repo
helm repo add prometheus-community https://prometheus-community.github.io/helm-charts
helm repo update

# Install kube-prometheus-stack
helm install prometheus prometheus-community/kube-prometheus-stack

# Port forward to Prometheus
kubectl port-forward svc/prometheus-kube-prom-prometheus 9090:9090
# Access at http://localhost:9090

# Query examples in UI:
# http_requests_total
# flask_http_request_duration_seconds_bucket
# process_resident_memory_bytes
```

### Grafana Setup

```bash
# Add Grafana repo
helm repo add grafana https://grafana.github.io/helm-charts
helm repo update

# Install Grafana
helm install grafana grafana/grafana \
  --set persistence.enabled=true \
  --set persistence.size=10Gi

# Get admin password
kubectl get secret --namespace default grafana -o jsonpath="{.data.admin-password}" | base64 --decode

# Port forward
kubectl port-forward svc/grafana 3000:80
# Access at http://localhost:3000

# Login with admin / <password from above>

# Add Prometheus as datasource:
# 1. Grafana UI → Configuration → Data Sources
# 2. Add Prometheus
# 3. URL: http://prometheus-kube-prom-prometheus:9090
# 4. Save & Test
```

### Logs & Debugging

```bash
# Check app logs
kubectl logs -f deployment/elearn

# Follow all pod logs
kubectl logs -f -l app=elearn

# View logs from multiple pods
kubectl logs -f pod/elearn-* 

# Get logs with timestamps
kubectl logs deployment/elearn --timestamps=true

# Export logs for analysis
kubectl logs deployment/elearn > app-logs.txt
```

---

## Troubleshooting

### Common Issues

```bash
# Port already in use
lsof -i :5000
lsof -i :5001
lsof -i :80
# Kill process: kill -9 <PID>

# Docker image not found
docker images | grep elearn
docker pull elearn:latest

# Docker Compose connection error
docker-compose ps
docker-compose logs

# Kubernetes pod not starting
kubectl describe pod <POD_NAME>
kubectl logs <POD_NAME>

# Can't access service from outside cluster
kubectl get svc
kubectl describe svc elearn

# Database locked error
rm instance/elearn.db
rm -rf instance/
python -m app.main
```

### Performance Issues

```bash
# Check resource usage
docker stats

# Check Kubernetes resource usage
kubectl top nodes
kubectl top pods

# Inspect container memory/CPU
docker inspect <CONTAINER_ID> | grep -i memory

# Check database size
ls -lh instance/elearn.db

# Check disk space
df -h
```

### Network Issues

```bash
# Test connectivity
curl -v http://localhost:5000
curl -v http://localhost/

# Check container network
docker network inspect elearn-net

# Test pod-to-pod connectivity
kubectl exec -it <POD_NAME> -- curl http://elearn:5000

# Check Kubernetes network policies
kubectl get networkpolicies
```

---

## Database Operations

### SQLite (Development)

```bash
# Access database
sqlite3 instance/elearn.db

# Inside sqlite3:
.tables                    # Show all tables
.schema                    # Show schema
SELECT * FROM user;        # View users
SELECT * FROM course;      # View courses
.quit                      # Exit

# Backup database
cp instance/elearn.db instance/elearn.db.backup

# Reset database
rm instance/elearn.db
python -m app.main  # Recreates with default admin
```

### PostgreSQL (Production)

```bash
# Connection string
postgresql://postgres:password@localhost:5432/elearn

# Create database
createdb -U postgres elearn

# Connect via psql
psql -U postgres -d elearn

# Inside psql:
\dt                        # List tables
\d user;                   # Describe user table
SELECT * FROM "user";      # Query table
\q                         # Exit

# Backup database
pg_dump -U postgres elearn > elearn-backup.sql

# Restore database
psql -U postgres -d elearn < elearn-backup.sql
```

### Database Migrations

```bash
# With Flask-Migrate (if installed)
flask db init
flask db migrate -m "Initial migration"
flask db upgrade

# Manual migration from SQLite to PostgreSQL
# 1. Export SQLite data
sqlite3 instance/elearn.db ".dump" > dump.sql

# 2. Create PostgreSQL database
createdb elearn

# 3. Update connection string and run app
export SQLALCHEMY_DATABASE_URI=postgresql://user:pass@localhost:5432/elearn
python -m app.main
```

---

## API Testing

### User Management

```bash
# Register student
curl -X POST http://localhost/register \
  -H "Content-Type: application/json" \
  -d '{"username": "student1", "password": "pass", "role": "student"}'

# Register teacher
curl -X POST http://localhost/register \
  -H "Content-Type: application/json" \
  -d '{"username": "teacher1", "password": "pass", "role": "teacher"}'

# Login
curl -X POST http://localhost/login \
  -H "Content-Type: application/json" \
  -d '{"username": "student1", "password": "pass"}'
# Save token: TOKEN="eyJ..."
```

### Course Management

```bash
# Get all courses
curl http://localhost/courses

# Create course (teacher/admin only)
curl -X POST http://localhost/courses \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $TOKEN" \
  -d '{"title": "Python 101", "description": "Learn Python"}'

# Test RBAC (student should get 403)
curl -X POST http://localhost/courses \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $STUDENT_TOKEN" \
  -d '{"title": "Fail", "description": "Should fail"}'
```

### Quiz Management

```bash
# Get quiz
curl http://localhost/quiz/1

# Create quiz (requires auth)
curl -X POST http://localhost/quiz/1 \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $TOKEN" \
  -d '{"question": "What is 2+2?", "answer": "4"}'
```

### Metrics & Health

```bash
# Health check
curl -I http://localhost/

# Prometheus metrics
curl http://localhost/metrics

# API Profile (requires token)
curl http://localhost/api/profile \
  -H "Authorization: Bearer $TOKEN"
```

---

## Performance Optimization

### Docker

```bash
# Reduce image size
docker build --build-arg BUILDKIT_INLINE_CACHE=1 -t elearn:latest .

# Multi-stage build (already in Dockerfile)
# View layers
docker history --human elearn:latest
```

### Python

```bash
# Profile app performance
pip install flask-profiler
python -m flask_profiler

# Check slow endpoints
python -c "from app import create_app; app = create_app(); app.run()"
```

### Kubernetes

```bash
# Set resource requests/limits
kubectl set resources deployment elearn \
  --requests=cpu=100m,memory=128Mi \
  --limits=cpu=500m,memory=512Mi

# Enable horizontal pod autoscaling
kubectl autoscale deployment elearn --min=2 --max=10 --cpu-percent=80
kubectl get hpa
```

---

## Useful Aliases

Add to `~/.zshrc` or `~/.bashrc`:

```bash
# Project navigation
alias elearn='cd ~/Documents/projects/e\ learning\ platform'

# Virtual environment
alias venv='source .venv/bin/activate'

# Docker shortcuts
alias dcup='docker-compose up --build'
alias dcdown='docker-compose down'
alias dclogs='docker-compose logs -f'

# Kubernetes shortcuts
alias k='kubectl'
alias kgp='kubectl get pods'
alias kgs='kubectl get svc'
alias kgd='kubectl get deployments'
alias kdp='kubectl describe pod'
alias kl='kubectl logs -f'

# Testing
alias test='pytest -v'
alias cov='pytest --cov=app tests/'
```

---

## Additional Resources

- **Flask Documentation**: https://flask.palletsprojects.com/
- **Kubernetes Docs**: https://kubernetes.io/docs/
- **Docker Docs**: https://docs.docker.com/
- **Helm Charts**: https://artifacthub.io/
- **Trivy Documentation**: https://github.com/aquasecurity/trivy
- **GitHub Actions**: https://docs.github.com/en/actions

---

**Last Updated**: November 7, 2025  
**Questions?** Check DEVOPS_GUIDE.md for step-by-step instructions or troubleshooting section above.
