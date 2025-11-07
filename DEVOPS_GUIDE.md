# 🔐 Secure DevOps Pipeline - Step-by-Step Guide

This guide walks you through setting up a complete secure DevOps pipeline for the E-Learning Platform from scratch.

## 📋 Prerequisites & Requirements

### System Requirements
- **OS**: macOS (Homebrew), Linux, or Windows (WSL2)
- **RAM**: Minimum 8GB (16GB recommended for Docker + k8s)
- **Disk**: 20GB free space

### Required Tools

| Tool | Version | Purpose |
|------|---------|---------|
| Docker | 20.10+ | Container runtime |
| Docker Compose | 2.0+ | Multi-container orchestration |
| kubectl | 1.24+ | Kubernetes client |
| minikube | 1.26+ | Local Kubernetes cluster (optional) |
| Git | 2.30+ | Version control |
| Python | 3.11+ | Application runtime |
| pip | 21.0+ | Python package manager |
| Trivy | 0.30+ | Container security scanner |
| Helm | 3.10+ | Kubernetes package manager (optional) |

### Software Dependencies (Python packages)

All listed in `requirements.txt`:
- Flask 2.0+
- Flask-SQLAlchemy 2.5+
- Flask-JWT-Extended 4.3+
- prometheus-client 0.14+
- pytest 7.0+
- werkzeug

---

## 🛠️ Installation Steps

### Step 1: Install Required Tools

#### macOS (using Homebrew)

```bash
# Update Homebrew
brew update

# Install Docker Desktop (includes Docker and Docker Compose)
# Download from: https://www.docker.com/products/docker-desktop
# OR use Homebrew:
brew install --cask docker

# Install kubectl
brew install kubectl

# Install minikube (for local k8s testing)
brew install minikube

# Install Trivy (security scanner)
brew install aquasecurity/trivy/trivy

# Install Helm (k8s package manager)
brew install helm

# Verify installations
docker --version
docker-compose --version
kubectl version --client
minikube version
trivy version
helm version
```

#### Linux (Ubuntu/Debian)

```bash
# Update package manager
sudo apt-get update && sudo apt-get upgrade -y

# Install Docker
curl -fsSL https://get.docker.com -o get-docker.sh
sudo sh get-docker.sh
sudo usermod -aG docker $USER
newgrp docker

# Install Docker Compose
sudo curl -L "https://github.com/docker/compose/releases/latest/download/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
sudo chmod +x /usr/local/bin/docker-compose

# Install kubectl
curl -LO "https://dl.k8s.io/release/$(curl -L -s https://dl.k8s.io/release/stable.txt)/bin/linux/amd64/kubectl"
sudo install -o root -g root -m 0755 kubectl /usr/local/bin/kubectl

# Install minikube
curl -LO https://github.com/kubernetes/minikube/releases/latest/download/minikube-linux-amd64
sudo install minikube-linux-amd64 /usr/local/bin/minikube

# Install Trivy
wget -qO - https://aquasecurity.github.io/trivy-repo/deb/public.key | sudo apt-key add -
echo "deb https://aquasecurity.github.io/trivy-repo/deb $(lsb_release -sc) main" | sudo tee -a /etc/apt/sources.list.d/trivy.list
sudo apt-get update && sudo apt-get install trivy

# Install Helm
curl https://raw.githubusercontent.com/helm/helm/main/scripts/get-helm-3 | bash
```

### Step 2: Clone/Setup Project

```bash
# Navigate to project directory
cd "/Users/anirudhbabuch/Documents/projects/e learning platform"

# Verify project structure
ls -la

# Expected files/folders:
# - app/                 (Flask application)
# - k8s/                 (Kubernetes manifests)
# - helm/                (Helm charts)
# - tests/               (Test files)
# - Dockerfile           (Container definition)
# - docker-compose.yml   (Docker compose config)
# - nginx.conf           (Nginx config)
# - requirements.txt     (Python dependencies)
# - .github/workflows/   (CI/CD config)
```

### Step 3: Install Python Dependencies

```bash
# Create virtual environment
python3 -m venv .venv

# Activate virtual environment
source .venv/bin/activate

# Upgrade pip
pip install --upgrade pip

# Install all dependencies
pip install -r requirements.txt

# Verify installation
pip list | grep -E "Flask|pytest|prometheus"
```

---

## 🐳 Phase 1: Docker & Local Testing

### Step 4: Build and Test Docker Image Locally

```bash
# Build Docker image
docker build -t elearn:latest .

# Verify image was created
docker images | grep elearn

# Run container locally (test)
docker run -p 5000:5000 elearn:latest

# In another terminal, test the app
curl http://localhost:5000/

# Stop container (Ctrl+C in first terminal)
```

### Step 5: Set Up Docker Compose

```bash
# Build with Docker Compose
docker-compose build

# Start all services (app + Nginx)
docker-compose up -d

# Check running containers
docker-compose ps

# View logs
docker-compose logs -f

# Test the app via Nginx (port 80)
curl http://localhost/

# Test API endpoints
curl http://localhost/courses

# Stop services
docker-compose down
```

---

## 🧪 Phase 2: Local Testing & Security Scanning

### Step 6: Run Unit Tests

```bash
# Activate virtual environment if not already
source .venv/bin/activate

# Run pytest
pytest -q

# Expected output:
# 2 passed in X.XXs

# Run with coverage (optional)
pip install pytest-cov
pytest --cov=app --cov-report=html
open htmlcov/index.html  # View coverage report
```

### Step 7: Run Security Scans Locally

#### Trivy Container Scan

```bash
# Scan Docker image for vulnerabilities
trivy image elearn:latest

# Scan with specific severity level
trivy image --severity HIGH,CRITICAL elearn:latest

# Generate JSON report
trivy image --format json --output trivy-report.json elearn:latest

# View report
cat trivy-report.json | jq .
```

#### OWASP Dependency Check (Optional)

```bash
# Install dependency-check
# macOS:
brew install dependency-check

# Run scan
dependency-check --project "E-Learning" --scan . --format JSON --out dependency-check-report.json

# View findings
cat dependency-check-report.json | jq .
```

---

## 🚀 Phase 3: GitHub Setup & CI/CD Pipeline

### Step 8: Initialize Git Repository

```bash
# Initialize git
git init

# Add all files
git add .

# Create initial commit
git commit -m "Initial commit: E-learning platform with secure DevOps pipeline"

# Verify git status
git status
```

### Step 9: Create GitHub Repository

1. Go to https://github.com/new
2. Create repository: `e-learning-platform`
3. Copy the repository URL (HTTPS or SSH)

```bash
# Add remote origin
git remote add origin https://github.com/YOUR-USERNAME/e-learning-platform.git

# Push to GitHub
git branch -M main
git push -u origin main

# Verify
git remote -v
```

### Step 10: Configure GitHub Secrets

1. Go to repository → **Settings** → **Secrets and variables** → **Actions**
2. Click **New repository secret** and add:

```
Secret Name: DOCKER_USERNAME
Secret Value: your-docker-hub-username

Secret Name: DOCKER_PASSWORD
Secret Value: your-docker-hub-token (NOT your password!)
```

To generate Docker Hub token:
1. Go to https://hub.docker.com/settings/security
2. Create **New Access Token**
3. Copy and paste in GitHub Secrets

### Step 11: Verify GitHub Actions Workflow

```bash
# The workflow file is already in place at:
# .github/workflows/ci.yml

# Push a test commit to trigger workflow
git add .github/workflows/ci.yml
git commit -m "Add GitHub Actions CI/CD workflow"
git push

# Monitor workflow:
# 1. Go to repository → Actions tab
# 2. Click on the latest workflow run
# 3. View build logs in real-time
```

---

## ☸️ Phase 4: Kubernetes Setup

### Step 12: Set Up Local Kubernetes Cluster (minikube)

```bash
# Start minikube cluster
minikube start --cpus 4 --memory 4096 --disk-size 20000mb

# Verify cluster is running
kubectl cluster-info

# Check nodes
kubectl get nodes

# Enable required addons
minikube addons enable ingress
minikube addons enable metrics-server
```

### Step 13: Deploy to Kubernetes

```bash
# Create namespace (optional)
kubectl create namespace elearn
kubectl config set-context --current --namespace=elearn

# Apply Kubernetes manifests
kubectl apply -f k8s/configmap.yaml
kubectl apply -f k8s/secrets.yaml
kubectl apply -f k8s/deployment.yaml
kubectl apply -f k8s/service.yaml

# Verify deployment
kubectl get pods
kubectl get svc
kubectl get configmap
kubectl get secrets
```

### Step 14: Access Application in Kubernetes

```bash
# Get service details
kubectl get svc elearn-service

# For minikube, use:
minikube service elearn-service

# Or manually port-forward:
kubectl port-forward svc/elearn-service 8080:80

# Then open:
# http://localhost:8080
```

### Step 15: Monitor Deployment

```bash
# View pod logs
kubectl logs -l app=elearn-app -f

# Describe pod for detailed info
kubectl describe pod <pod-name>

# Check resource usage
kubectl top pods
kubectl top nodes

# Watch pod status
kubectl get pods -w
```

---

## 🔐 Security Best Practices

### Secret Management

```bash
# ❌ WRONG - Don't store secrets in code or env files
echo "ADMIN_PASSWORD=mypassword" > .env

# ✅ CORRECT - Use Kubernetes Secrets
kubectl create secret generic elearn-secrets \
  --from-literal=admin-username=admin \
  --from-literal=admin-password=<secure-password>

# For CI/CD, use GitHub Secrets (shown in Step 10)
```

### Database Security

```bash
# Currently using SQLite (fine for development)
# For production, use:

# PostgreSQL (recommended)
# - Store credentials in k8s Secrets
# - Use SSL connections
# - Regular backups

# MySQL/MariaDB
# - Use strong passwords
# - Restrict network access
# - Enable query logging
```

### Network Security

```bash
# Create network policy (k8s)
kubectl apply -f - <<EOF
apiVersion: networking.k8s.io/v1
kind: NetworkPolicy
metadata:
  name: elearn-network-policy
spec:
  podSelector:
    matchLabels:
      app: elearn-app
  policyTypes:
    - Ingress
    - Egress
  ingress:
    - from:
        - namespaceSelector:
            matchLabels:
              name: elearn
  egress:
    - to:
        - namespaceSelector:
            matchLabels:
              name: elearn
EOF
```

### Container Security

```bash
# Run security audit
trivy image --severity HIGH,CRITICAL elearn:latest

# Check Dockerfile best practices
docker run --rm -i hadolint/hadolint < Dockerfile

# Scan for malware
trivy image --scanners vuln elearn:latest
```

---

## 📊 Phase 5: Monitoring & Logging (Optional)

### Step 16: Add Prometheus Monitoring

```bash
# The app already exposes /metrics endpoint
# Test it:
curl http://localhost/metrics

# Deploy Prometheus (Helm chart)
helm repo add prometheus-community https://prometheus-community.github.io/helm-charts
helm install prometheus prometheus-community/kube-prometheus-stack -n elearn

# Access Prometheus UI
kubectl port-forward -n elearn svc/prometheus-operated 9090:9090
# Open http://localhost:9090
```

### Step 17: Add Grafana Dashboards

```bash
# Install Grafana
helm repo add grafana https://grafana.github.io/helm-charts
helm install grafana grafana/grafana -n elearn

# Get Grafana admin password
kubectl get secret -n elearn grafana -o jsonpath="{.data.admin-password}" | base64 --decode

# Port forward to access
kubectl port-forward -n elearn svc/grafana 3000:80
# Open http://localhost:3000

# Add Prometheus datasource:
# Data Sources → Add → Prometheus
# URL: http://prometheus-operated.elearn:9090
```

---

## 🔄 Continuous Deployment Workflow

### Step 18: Set Up Auto-Deployment

```bash
# 1. Make code changes locally
# 2. Commit and push to GitHub
git add .
git commit -m "Feature: Add new course endpoint"
git push origin main

# 3. GitHub Actions automatically:
#    - Runs tests
#    - Builds Docker image
#    - Runs Trivy scan
#    - Pushes to Docker Hub (if main branch)

# 4. Deploy new version to k8s
kubectl set image deployment/elearn-app \
  web=<your-docker-hub>/elearn:$(git rev-parse --short HEAD)

# 5. Verify rollout
kubectl rollout status deployment/elearn-app
```

---

## 🧹 Cleanup & Maintenance

### Stop Services

```bash
# Stop Docker Compose
docker-compose down

# Stop minikube
minikube stop

# Delete minikube cluster (caution!)
minikube delete
```

### Clean Up Resources

```bash
# Delete k8s deployment
kubectl delete -f k8s/

# Delete Docker images
docker rmi elearn:latest

# Prune unused Docker resources
docker system prune -a --volumes
```

---

## ✅ Verification Checklist

- [ ] Docker installed and running
- [ ] Docker image builds successfully
- [ ] Docker Compose runs app + Nginx
- [ ] Unit tests pass (pytest)
- [ ] Trivy scan runs without errors
- [ ] GitHub repository created
- [ ] GitHub Secrets configured
- [ ] GitHub Actions workflow runs successfully
- [ ] minikube cluster started
- [ ] Kubernetes manifests applied
- [ ] Pods are running and healthy
- [ ] App is accessible at http://localhost (locally)
- [ ] All API endpoints respond correctly
- [ ] Prometheus metrics endpoint works (/metrics)

---

## 🐛 Troubleshooting

### Docker Issues

```bash
# Docker daemon not running
# macOS: Start Docker Desktop app

# Port 80/5000 already in use
lsof -i :80
lsof -i :5000
# Kill the process
kill -9 <PID>

# Docker build fails
docker system prune -a
docker-compose build --no-cache
```

### Kubernetes Issues

```bash
# minikube won't start
minikube delete
minikube start

# Pod not starting
kubectl describe pod <pod-name>
kubectl logs <pod-name>

# Service not accessible
kubectl get svc
kubectl port-forward svc/elearn-service 8080:80
```

### GitHub Actions Issues

```bash
# Workflow not triggering
git push -u origin main  # Ensure on main branch

# Docker push fails
# Check GitHub Secrets are set correctly:
# Settings → Secrets → Verify DOCKER_USERNAME and DOCKER_PASSWORD
```

---

## 📚 Additional Resources

- **Docker Documentation**: https://docs.docker.com/
- **Kubernetes Documentation**: https://kubernetes.io/docs/
- **Trivy Security Scanner**: https://github.com/aquasecurity/trivy
- **GitHub Actions**: https://docs.github.com/en/actions
- **Flask Best Practices**: https://flask.palletsprojects.com/
- **OWASP Top 10**: https://owasp.org/www-project-top-ten/
- **12 Factor App**: https://12factor.net/

---

## 🎓 Learning Path

1. **Beginner**: Follow Steps 1-5 (Local Docker setup)
2. **Intermediate**: Complete Steps 6-11 (Testing & GitHub CI/CD)
3. **Advanced**: Finish Steps 12-17 (Kubernetes & Monitoring)
4. **Expert**: Implement security scanning and auto-healing

---

## 📞 Support & Next Steps

If you need help:
1. Check troubleshooting section above
2. Review logs: `kubectl logs`, `docker-compose logs`, GitHub Actions logs
3. Open GitHub issues for problems

**Ready to deploy? Follow the phase workflow above!**
