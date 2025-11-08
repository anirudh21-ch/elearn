# E-Learning Portal with Complete DevOps Pipeline 🚀

A full-stack e-learning platform showcasing real-world DevOps practices including containerization, CI/CD automation, Kubernetes orchestration, security scanning, and production-grade monitoring.

## 🎯 **For Presentations & Demos**

**📖 Complete Presentation Guide**: See [`PRESENTATION_DEMO.md`](PRESENTATION_DEMO.md) for step-by-step demo instructions  
**⚡ Quick Commands**: See [`demo-commands.sh`](demo-commands.sh) for copy-paste ready commands  
**🌐 Browser URLs**: See [`BROWSER_URLS.txt`](BROWSER_URLS.txt) for all access URLs and test queries  
**✅ Checklist**: See [`PRESENTATION_CHECKLIST.md`](PRESENTATION_CHECKLIST.md) for pre-demo setup

---

## Features

- **User Authentication**: Register/Login with role-based access (Student, Teacher, Admin)
- **Courses**: Create, browse, and manage courses (teachers/admin only)
- **Quizzes**: Add and view quizzes for courses
- **JWT Tokens**: Secure API endpoints with JWT authentication
- **Role-Based Access Control**: Different permissions for students, teachers, and admins
- **Prometheus Metrics**: `/metrics` endpoint for monitoring
- **Docker & Kubernetes**: Full containerization and k8s manifests
- **CI/CD Pipeline**: GitHub Actions with Trivy security scans

## Quick Start (Local)

### Prerequisites
- Python 3.11+
- Virtual environment (venv)

### Install & Run

```bash
# Create and activate virtual environment
python3 -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Run the app
PORT=5001 python -m app.main
```

Open http://localhost:5001 in your browser.

## Docker (Local Development)

### Build & Run with Docker Compose

```bash
docker-compose up --build
```

This starts:
- **Flask app** on port 5000 (internal)
- **Nginx reverse proxy** on port 80 (external)

Access the app at http://localhost in your browser.

### Build Docker image manually

```bash
docker build -t elearn:latest .
docker run -p 5000:5000 elearn:latest
```

## CI/CD Pipeline (GitHub Actions)

The GitHub Actions workflow (`.github/workflows/ci.yml`) runs:

1. **Lint & Test**: pytest for all routes
2. **Build Docker image**: Builds image locally
3. **Trivy scan**: Checks for vulnerabilities in the Docker image
4. **Push to Docker Hub**: Pushes image on main branch push (requires secrets)

### Required GitHub Secrets

Add these to your repository settings:

```
DOCKER_USERNAME: <your-docker-hub-username>
DOCKER_PASSWORD: <your-docker-hub-token>
SONAR_TOKEN: <sonarqube-token> (optional, for code quality)
SONAR_HOST_URL: <sonarqube-url> (optional)
```

### Workflow Triggers

- Runs on every push to `main` or `develop`
- Runs on every pull request
- Pushes image to Docker Hub only on `main` branch push

## Kubernetes Deployment

### Prerequisites

- Kubernetes cluster (local: `minikube start`, or cloud: EKS, GKE, AKS)
- `kubectl` configured
- Docker image pushed to a registry (Docker Hub, ECR, GCR, etc.)

### Deploy using kubectl

```bash
# Apply all manifests
kubectl apply -f k8s/

# Check deployment status
kubectl get pods
kubectl get svc elearn-service

# View logs
kubectl logs -l app=elearn-app
```

### Access the app

```bash
# Get service external IP (cloud) or use localhost (minikube)
kubectl get svc elearn-service

# On local minikube:
minikube service elearn-service
```

### Deploy using Helm (Optional)

```bash
helm install elearn ./helm/elearn-chart
helm list
helm uninstall elearn
```

## Security Considerations

### Secrets Management

**DO NOT commit secrets to git.** Instead:

1. Use GitHub Secrets for CI/CD tokens
2. Use Kubernetes Secrets for production credentials:
   ```bash
   kubectl create secret generic elearn-secrets \
     --from-literal=admin-username=admin \
     --from-literal=admin-password=<secure-password>
   ```
3. Use HashiCorp Vault or AWS Secrets Manager for production

### Security Scans

- **Trivy**: Scans Docker image for vulnerabilities (runs in CI)
- **SonarQube**: Code quality and security (optional, configure in CI)
- **OWASP Dependency Check**: Scans for vulnerable libraries (can be added to CI)

To run Trivy locally:

```bash
trivy image elearn:latest
```

## API Endpoints

### Auth

- `POST /register` - Register new user (JSON: `{username, password, role}`)
- `POST /login` - Login (JSON: `{username, password}`)

### Courses

- `GET /courses` - List all courses (returns HTML in browser, JSON in API)
- `POST /courses` - Create course (requires teacher/admin JWT)

### Profile

- `GET /profile` - View user profile (requires JWT)

### Metrics

- `GET /metrics` - Prometheus metrics (for monitoring)

## Database

Currently uses **SQLite** (`instance/elearn.db`). For production, migrate to:
- PostgreSQL
- MySQL
- MongoDB

## Testing

```bash
pytest -q
```

## Project Structure

```
e-learning-platform/
├── app/
│   ├── __init__.py
│   ├── main.py
│   ├── models.py
│   ├── routes.py
│   ├── templates/
│   │   ├── base.html
│   │   ├── index.html
│   │   ├── register.html
│   │   ├── login.html
│   │   ├── profile.html
│   │   └── courses.html
│   └── static/
├── k8s/
│   ├── deployment.yaml
│   ├── service.yaml
│   ├── configmap.yaml
│   ├── secrets.yaml
│   └── deploy.sh
├── helm/
│   └── elearn-chart/
│       ├── Chart.yaml
│       ├── values.yaml
│       └── templates/
├── tests/
│   └── test_app.py
├── Dockerfile
├── docker-compose.yml
├── nginx.conf
├── requirements.txt
├── Jenkinsfile
├── .github/
│   └── workflows/
│       └── ci.yml
└── README.md
```

## Next Steps

1. **Customize**: Update admin credentials, configure database, adjust roles
2. **Push to GitHub**: Commit and push to GitHub to trigger CI/CD
3. **Deploy**: Use Docker Compose for local testing, Kubernetes for production
4. **Monitor**: Add Prometheus + Grafana for metrics and dashboards
5. **Scale**: Use k8s horizontal pod autoscaling (HPA) for load

## Troubleshooting

### Port 5000/80 already in use

```bash
# Find process using port
lsof -i :5000

# Kill process (or use different PORT)
kill -9 <PID>
PORT=5002 python -m app.main
```

### Docker build fails

```bash
# Clean build cache
docker system prune -a
docker-compose build --no-cache
```

### k8s pod not starting




