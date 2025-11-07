# 📦 Requirements & Dependencies

## All Project Dependencies

### System-Level Requirements

```bash
# Minimum requirements
OS: macOS 10.15+, Ubuntu 18.04+, or Windows 10+ (WSL2)
RAM: 8GB (16GB recommended)
Disk Space: 20GB free
CPU: 4-core processor minimum
```

### Tool Installation Summary

| Tool | macOS | Linux | Windows (WSL2) | URL |
|------|-------|-------|----------------|-----|
| Docker | Homebrew or DMG | apt/yum | WSL2 + Desktop | https://docker.com |
| Docker Compose | Included in Desktop | apt/yum | Included | Included with Docker |
| kubectl | Homebrew | apt/yum | WSL2 | https://kubernetes.io |
| minikube | Homebrew | Binary | WSL2 | https://minikube.sigs.k8s.io |
| Trivy | Homebrew | apt/yum | WSL2 | https://github.com/aquasecurity/trivy |
| Helm | Homebrew | Binary | WSL2 | https://helm.sh |
| Git | Homebrew | apt/yum | WSL2 | https://git-scm.com |

### Python Dependencies

From `requirements.txt`:

```
Flask>=2.0              # Web framework
Flask-SQLAlchemy>=2.5   # ORM for database
Flask-JWT-Extended>=4.3 # JWT authentication
prometheus_client>=0.14 # Metrics collection
pytest>=7.0             # Testing framework
requests                # HTTP client (for testing)
werkzeug                # WSGI utilities
```

**Installation:**
```bash
pip install -r requirements.txt
```

### Development Dependencies

```
pytest-cov              # Code coverage for pytest
dependency-check        # OWASP dependency scanning
hadolint               # Dockerfile linting
flake8                 # Python code linting (optional)
black                  # Code formatter (optional)
```

**Installation:**
```bash
pip install pytest-cov dependency-check hadolint flake8 black
```

---

## Docker Requirements

### Base Image
- `python:3.11-slim` - Official Python slim image

### Build Dependencies
- `build-essential` - C/C++ build tools (for some Python packages)

### Container Resources

```yaml
# Minimum
CPU: 0.1 (100m)
Memory: 128Mi

# Recommended
CPU: 0.5 (500m)
Memory: 512Mi

# High Load
CPU: 1
Memory: 1Gi
```

### Network Ports

| Service | Port | Protocol |
|---------|------|----------|
| Flask App | 5000 | TCP |
| Nginx | 80 | TCP |
| Nginx (HTTPS) | 443 | TCP (optional) |
| Prometheus | 9090 | TCP (optional) |
| Grafana | 3000 | TCP (optional) |

---

## Kubernetes Requirements

### Cluster Requirements

```bash
# Minimum (local testing with minikube)
Master Nodes: 1
Worker Nodes: 1
API Version: 1.20+
Memory: 4Gi (per node, minimum)
CPU: 2 (per node, minimum)

# Production
Master Nodes: 3 (High Availability)
Worker Nodes: 2+
API Version: 1.24+
Memory: 8Gi+ (per node)
CPU: 4+ (per node)
```

### Kubernetes Objects Used

- **Deployment**: App replicas (2)
- **Service**: LoadBalancer on port 80
- **ConfigMap**: Application configuration
- **Secret**: Sensitive data (admin credentials)
- **Optional**: Ingress, HPA, PVC for storage

---

## Database Requirements

### Current (Development)
```
Type: SQLite
File: instance/elearn.db
Max Connections: 1 (single-file based)
Suitable for: Development, Testing, <100 users
```

### Recommended (Production)

#### PostgreSQL
```
Version: 12+
Connections: 100-500
Storage: 50Gi+ (depending on data)
Memory: 2Gi+ container
Connection String: postgresql://user:pass@host:5432/elearn
```

#### MySQL/MariaDB
```
Version: 8.0+
Connections: 100-500
Storage: 50Gi+ (depending on data)
Memory: 2Gi+ container
Connection String: mysql+pymysql://user:pass@host:3306/elearn
```

---

## CI/CD Requirements

### GitHub Actions

```yaml
# Runners
ubuntu-latest: Recommended
macos-latest: For Mac builds
windows-latest: For Windows compatibility

# Storage
Artifact Storage: 5GB free
Log Retention: 90 days default

# Secrets Required
DOCKER_USERNAME: Docker Hub username
DOCKER_PASSWORD: Docker Hub access token
SONAR_TOKEN: SonarQube token (optional)
SONAR_HOST_URL: SonarQube server URL (optional)
```

### Jenkins (Alternative CI)

```bash
# Prerequisites
Java: 11+
Jenkins: 2.350+
Plugins: Docker, Pipeline, SonarQube, Trivy
Memory: 2Gi minimum
Storage: 50Gi for artifacts
```

---

## Security Scanning Requirements

### Trivy

```bash
Version: 0.30.0+
Signature Verification: Optional (GPG)
Database: Auto-downloaded on first run
Storage: 500MB for vulnerability DB
Scan Types:
  - Vulnerability scanning
  - Misconfiguration detection
  - Secret scanning (optional)
```

### SonarQube (Optional)

```bash
Version: 9.0+
Database: PostgreSQL 11+
Memory: 4Gi minimum (container)
Storage: 20Gi for projects/analysis
Token: Create in SonarQube UI
```

### OWASP Dependency Check

```bash
Version: Latest
Java: 1.8+
Storage: 2Gi for NVD database
Scan Types:
  - Known vulnerability detection
  - Transitive dependency analysis
```

---

## Monitoring & Logging Requirements

### Prometheus

```bash
Version: 2.30+
Retention: 15 days default (configurable)
Storage: 50Gi per month (high volume)
Memory: 1Gi for typical load
Scrape Interval: 15s (default)
```

### Grafana

```bash
Version: 8.0+
Database: SQLite (embedded) or PostgreSQL
Storage: 1Gi for dashboards/history
Memory: 512Mi minimum
```

### ELK Stack (Optional - for logging)

```bash
Elasticsearch: 7.10+
Logstash: 7.10+
Kibana: 7.10+
Storage: 100Gi+ (logs accumulate quickly)
Memory: 4Gi+ (total for stack)
```

---

## Installation Commands Quick Reference

### macOS

```bash
# All-in-one installation
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
brew install docker kubectl minikube trivy helm git

# Docker Desktop (GUI)
brew install --cask docker
```

### Ubuntu/Debian

```bash
sudo apt-get update
sudo apt-get install -y \
  docker.io \
  docker-compose \
  kubectl \
  minikube \
  trivy \
  helm \
  git \
  python3-pip \
  python3-venv

# Add user to docker group
sudo usermod -aG docker $USER
newgrp docker
```

### CentOS/RHEL

```bash
sudo yum install -y \
  docker \
  kubectl \
  git \
  python3 \
  python3-pip

# Add Kubernetes repo
cat <<EOF | sudo tee /etc/yum.repos.d/kubernetes.repo
[kubernetes]
name=Kubernetes
baseurl=https://packages.cloud.google.com/yum/repos/kubernetes-el7-x86_64
enabled=1
gpgcheck=1
repo_gpgcheck=1
gpgkey=https://packages.cloud.google.com/yum/doc/yum-key.gpg
       https://packages.cloud.google.com/yum/doc/rpm-package-key.gpg
EOF

sudo yum install -y kubectl
```

### Windows (WSL2)

```bash
# In WSL2 terminal (Ubuntu):
sudo apt-get update
sudo apt-get install -y \
  docker.io \
  kubectl \
  git \
  python3-pip \
  python3-venv

# Download Docker Desktop for Windows
# Download kubectl for Windows
# Download minikube for Windows
```

---

## Verification Commands

```bash
# Check all installations
echo "=== Docker ===" && docker --version && docker-compose --version
echo "=== Kubernetes ===" && kubectl version --client
echo "=== Minikube ===" && minikube version
echo "=== Trivy ===" && trivy version
echo "=== Helm ===" && helm version
echo "=== Git ===" && git --version
echo "=== Python ===" && python3 --version && pip --version

# All in one verification script
#!/bin/bash
for cmd in docker docker-compose kubectl minikube trivy helm git python3; do
  if ! command -v $cmd &> /dev/null; then
    echo "❌ $cmd NOT installed"
  else
    echo "✅ $cmd installed: $($cmd --version | head -n1)"
  fi
done
```

---

## Storage & Network Requirements

### Disk Space

```
Application code:           50MB
Docker images:              500MB
Database (SQLite):          10MB
Database (PostgreSQL):      1GB (initial)
Kubernetes artifacts:       100MB
Logs & backups:             5GB+
Total (dev environment):    10GB
Total (prod environment):   50GB+
```

### Network Bandwidth

```
Docker image push (CI/CD):  100-500MB per build
GitHub Actions logs:        10-50MB per run
Database replication:       1-10MB/sec (depends on data volume)
Monitoring metrics:         1-10MB/day
```

### Network Connectivity

- **Git**: HTTPS (port 443) or SSH (port 22)
- **Docker Hub**: HTTPS (port 443)
- **GitHub Actions**: HTTPS (port 443)
- **Kubernetes**: Cluster-internal networking + external access
- **Monitoring**: Internal + external (Prometheus, Grafana)

---

## Recommended Versions

```yaml
Production Stack:
  Kubernetes: 1.24.0+
  Docker: 20.10.0+
  Python: 3.11+
  Flask: 2.2.0+
  PostgreSQL: 14+
  Nginx: 1.21+
  
CI/CD Stack:
  GitHub Actions: Latest
  Jenkins: 2.350+
  GitLab CI: Latest
  
Security Stack:
  Trivy: 0.35.0+
  SonarQube: 9.5+
  Vault: 1.12+
  cert-manager: 1.9+
  
Monitoring Stack:
  Prometheus: 2.35+
  Grafana: 9.0+
  Loki: 2.5+
  Jaeger: 1.30+
```

---

## License & Support

All tools listed are open-source or have free tiers:
- Docker: Open-source (Community Edition free)
- Kubernetes: Open-source
- Trivy: Open-source (FOSS)
- Helm: Open-source
- GitHub Actions: Free for public repos, included with GitHub Pro
- SonarQube: Open-source version available
- Prometheus/Grafana: Open-source

For commercial support, check individual tool documentation.
