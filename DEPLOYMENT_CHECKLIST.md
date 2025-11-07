# ✅ E-Learning Platform - Deployment Checklist

**Project**: E-Learning Platform with Secure DevOps Pipeline  
**Created**: November 7, 2025  
**Status**: Ready for Deployment

---

## 🎯 Pre-Deployment Phase

### Local Environment Setup

- [ ] **OS & System**
  - [ ] macOS 10.15+, Ubuntu 18.04+, or Windows 10+ (WSL2)
  - [ ] 8GB+ RAM available
  - [ ] 20GB+ free disk space
  - [ ] Internet connection (package downloads)

- [ ] **Git Setup**
  - [ ] Git installed (`git --version`)
  - [ ] GitHub account created
  - [ ] SSH key configured (or HTTPS credentials ready)
  - [ ] Repository created on GitHub

- [ ] **Python Environment**
  - [ ] Python 3.11+ installed (`python3 --version`)
  - [ ] Virtual environment created (`.venv/`)
  - [ ] Activated virtualenv (`source .venv/bin/activate`)
  - [ ] Dependencies installed (`pip install -r requirements.txt`)
  - [ ] Run tests locally (`pytest -v` passes 2/2)

- [ ] **Docker Installation**
  - [ ] Docker installed (`docker --version`)
  - [ ] Docker daemon running
  - [ ] Docker Compose installed (`docker-compose --version`)
  - [ ] Docker Hub account created (optional, for image registry)

### Local Testing

- [ ] **App Starts Successfully**
  - [ ] Run `python -m app.main`
  - [ ] Check: "Running on http://127.0.0.1:5001"
  - [ ] Test: `curl -I http://127.0.0.1:5001/` returns 200 OK

- [ ] **Database Initialized**
  - [ ] SQLite database created (`instance/elearn.db` exists)
  - [ ] Default admin user created (admin/admin)
  - [ ] Can login successfully via API or UI

- [ ] **Tests Pass**
  - [ ] Run `pytest -v` from project root
  - [ ] Result: 2 tests passed
  - [ ] No syntax errors
  - [ ] No import errors

- [ ] **API Endpoints Work**
  - [ ] GET `/` returns 200 (HTML page)
  - [ ] POST `/register` creates user
  - [ ] POST `/login` returns JWT token
  - [ ] GET `/courses` returns course list
  - [ ] POST `/courses` restricted to teacher/admin

- [ ] **Frontend Pages Load**
  - [ ] Index page accessible
  - [ ] Register page shows form
  - [ ] Login page shows form
  - [ ] Profile page displays after login
  - [ ] Courses page shows create form (if teacher)

---

## 🐳 Docker Phase

### Docker Build & Test

- [ ] **Build Docker Image**
  - [ ] Run: `docker build -t elearn:latest .`
  - [ ] No build errors
  - [ ] Image successfully created
  - [ ] Check: `docker images | grep elearn`

- [ ] **Test Docker Image Standalone**
  - [ ] Run: `docker run -it -p 5001:5000 elearn:latest`
  - [ ] App starts inside container
  - [ ] Test: `curl http://127.0.0.1:5001/` returns 200
  - [ ] Stop: Ctrl+C stops container gracefully

- [ ] **Docker Security Scan**
  - [ ] Trivy installed (`trivy version`)
  - [ ] Run: `trivy image elearn:latest`
  - [ ] Review HIGH/CRITICAL vulnerabilities
  - [ ] Document any known/acceptable risks

### Docker Compose

- [ ] **Start Services**
  - [ ] Run: `docker-compose up --build`
  - [ ] Both services start: web (Flask) + nginx
  - [ ] No port conflicts (80, 5000 available)
  - [ ] No volume errors

- [ ] **Test via Nginx (port 80)**
  - [ ] Test: `curl http://localhost/` returns 200
  - [ ] Page loads with navbar
  - [ ] Static assets served (Bootstrap CSS)
  - [ ] Nginx logs show successful proxy to Flask

- [ ] **Test API through Nginx**
  - [ ] `/register` POST works via port 80
  - [ ] `/login` POST returns token
  - [ ] `/courses` GET returns data
  - [ ] Authorization header forwarded correctly

- [ ] **Docker Compose Cleanup**
  - [ ] Run: `docker-compose down`
  - [ ] All containers stopped/removed
  - [ ] Network cleaned up
  - [ ] No orphaned containers (check `docker ps -a`)

- [ ] **Compose Health Checks**
  - [ ] View logs: `docker-compose logs -f`
  - [ ] No errors in Flask app logs
  - [ ] No 502/504 errors from Nginx
  - [ ] Both services restart on failure

---

## 🔐 Security Phase

### Code Security

- [ ] **Python Linting**
  - [ ] Run: `flake8 app/`
  - [ ] No critical style violations
  - [ ] No obvious bugs detected

- [ ] **Dependency Vulnerabilities**
  - [ ] Run: `pip list --outdated`
  - [ ] Review outdated packages
  - [ ] Update if needed: `pip install --upgrade package-name`
  - [ ] Re-run tests after updates

- [ ] **OWASP Dependency Check**
  - [ ] Run: `dependency-check --project "E-Learning" --scan requirements.txt`
  - [ ] Review HIGH vulnerabilities
  - [ ] Document mitigation strategies

- [ ] **Secrets Management**
  - [ ] No hardcoded credentials in code
  - [ ] `ADMIN_USERNAME` and `ADMIN_PASSWORD` set via env vars
  - [ ] JWT_SECRET_KEY generated securely
  - [ ] `.env` file excluded from Git (`.gitignore` has `*.env`)

### Container Security

- [ ] **Image Scan with Trivy**
  - [ ] Run: `trivy image elearn:latest`
  - [ ] Review vulnerabilities by severity
  - [ ] Compare against baseline
  - [ ] Export JSON report: `trivy image --format json elearn:latest`

- [ ] **Dockerfile Security**
  - [ ] Using official base image (python:3.11-slim)
  - [ ] Running as non-root user (check Dockerfile)
  - [ ] Multi-stage build for optimization
  - [ ] Health checks defined
  - [ ] No use of `latest` tag in production

- [ ] **Docker Registry Setup (Optional)**
  - [ ] Docker Hub account created
  - [ ] Repository created: `username/elearn`
  - [ ] Image tagged properly: `username/elearn:v1.0.0`
  - [ ] Repository made private if needed

### Network Security

- [ ] **Firewall Rules**
  - [ ] Port 80 (HTTP) accessible
  - [ ] Port 443 (HTTPS) configured (if using SSL)
  - [ ] Port 5000 restricted to internal only
  - [ ] Management ports (8080, 9090) internal only

- [ ] **HTTPS/TLS (Optional)**
  - [ ] SSL certificate obtained (Let's Encrypt)
  - [ ] Nginx configured for HTTPS
  - [ ] HTTP redirects to HTTPS
  - [ ] Certificate auto-renewal configured

---

## 🚀 CI/CD Phase

### GitHub Setup

- [ ] **Repository Created**
  - [ ] Repo name: `elearn` (or similar)
  - [ ] Visibility: Public or Private
  - [ ] README.md visible on main page
  - [ ] All files committed and pushed

- [ ] **Git Workflows**
  - [ ] Initial commit: `git add . && git commit -m "Initial commit"`
  - [ ] Push to main: `git push origin main`
  - [ ] Verify files on GitHub

- [ ] **GitHub Secrets Configured**
  - [ ] Go to: Repo → Settings → Secrets and variables → Actions
  - [ ] Add `DOCKER_USERNAME` (Docker Hub username)
  - [ ] Add `DOCKER_PASSWORD` (Docker Hub access token, NOT password)
  - [ ] Verify secrets are masked in logs
  - [ ] Test: `gh secret list` (if GitHub CLI installed)

- [ ] **GitHub Actions Workflow**
  - [ ] `.github/workflows/ci.yml` exists
  - [ ] Workflow triggered on push to main
  - [ ] View workflow: Repo → Actions tab

### CI/CD Execution

- [ ] **First Workflow Run**
  - [ ] Push code to main branch
  - [ ] Monitor: Repo → Actions tab
  - [ ] Expected duration: 3-5 minutes
  - [ ] All 3 jobs should complete: lint-and-test, build-and-scan, push-to-registry

- [ ] **Job 1: Lint and Test**
  - [ ] ✅ Python dependencies installed
  - [ ] ✅ Tests execute (2/2 passing)
  - [ ] ✅ No linting errors
  - [ ] ✅ Job completes successfully

- [ ] **Job 2: Build and Scan**
  - [ ] ✅ Docker image built
  - [ ] ✅ Trivy scan runs
  - [ ] ✅ Vulnerability report generated
  - [ ] ✅ Exit code 0 (scan completed)
  - [ ] Review CVEs: HIGH/CRITICAL noted

- [ ] **Job 3: Push to Registry**
  - [ ] ✅ Image tagged with version
  - [ ] ✅ Image pushed to Docker Hub (only on main branch push)
  - [ ] ✅ Verify on Docker Hub: `docker pull username/elearn:latest`

### Workflow Monitoring

- [ ] **Check Logs**
  - [ ] Each job has readable logs
  - [ ] No secrets leaked in logs
  - [ ] Timestamps show proper execution
  - [ ] Failures (if any) clearly identified

- [ ] **Artifacts**
  - [ ] Build artifacts available for download
  - [ ] Logs retained for 90 days
  - [ ] Space used: < 5GB

---

## ☸️ Kubernetes Phase

### Prerequisites

- [ ] **Kubernetes Tools Installed**
  - [ ] `kubectl` installed (`kubectl version --client`)
  - [ ] `minikube` installed (`minikube version`)
  - [ ] `helm` installed (`helm version`)

- [ ] **Minikube Cluster**
  - [ ] Started: `minikube start --cpus=4 --memory=8192`
  - [ ] Status: `minikube status` shows "Running"
  - [ ] Check cluster: `kubectl cluster-info`
  - [ ] Nodes ready: `kubectl get nodes` shows STATUS=Ready

### Deploy with kubectl

- [ ] **Manifest Files Present**
  - [ ] `k8s/deployment.yaml` exists
  - [ ] `k8s/service.yaml` exists
  - [ ] `k8s/configmap.yaml` exists
  - [ ] `k8s/secrets.yaml` exists (or created via kubectl)

- [ ] **Apply Manifests**
  - [ ] Run: `kubectl apply -f k8s/`
  - [ ] Or: `bash k8s/deploy.sh`
  - [ ] No errors in output

- [ ] **Check Deployment**
  - [ ] `kubectl get deployments` shows elearn with 2 replicas
  - [ ] `kubectl get pods` shows 2 running pods
  - [ ] `kubectl get svc` shows LoadBalancer service
  - [ ] Wait: `kubectl rollout status deployment/elearn` completes

- [ ] **Test Service Access**
  - [ ] Run: `kubectl port-forward svc/elearn 8080:80`
  - [ ] In another terminal: `curl http://localhost:8080/`
  - [ ] Returns 200 OK with HTML
  - [ ] Stop port-forward: Ctrl+C

- [ ] **Pod Health**
  - [ ] All pods: STATUS=Running
  - [ ] Ready: 1/1
  - [ ] Restart count: 0 (or minimal)
  - [ ] Liveness probes: passing
  - [ ] Readiness probes: passing

### Deploy with Helm (Optional)

- [ ] **Helm Chart**
  - [ ] `helm/elearn-chart/Chart.yaml` exists
  - [ ] `helm/elearn-chart/values.yaml` configured
  - [ ] Version: 0.1.0+

- [ ] **Install Release**
  - [ ] Run: `helm install elearn ./helm/elearn-chart`
  - [ ] Or with custom values: `helm install elearn ./helm/elearn-chart --set replicaCount=3`
  - [ ] Check: `helm list` shows elearn release

- [ ] **Verify Helm Deployment**
  - [ ] `kubectl get all -l app=elearn` shows all resources
  - [ ] Pods running: `kubectl get pods`
  - [ ] Service accessible: `kubectl port-forward svc/elearn 8080:80`

### Kubernetes Scaling

- [ ] **Manual Scaling**
  - [ ] Scale to 3 replicas: `kubectl scale deployment elearn --replicas=3`
  - [ ] Verify: `kubectl get pods` shows 3 pods
  - [ ] Scale down: `kubectl scale deployment elearn --replicas=2`

- [ ] **Rolling Update**
  - [ ] Update image: `kubectl set image deployment/elearn elearn=elearn:v2.0 --record`
  - [ ] Check rollout: `kubectl rollout status deployment/elearn`
  - [ ] Verify: `kubectl describe deployment elearn` shows new image

### Kubernetes Cleanup

- [ ] **Delete Resources**
  - [ ] Option 1: `kubectl delete -f k8s/`
  - [ ] Option 2: `helm uninstall elearn`
  - [ ] Verify: `kubectl get pods` returns empty
  - [ ] Check persistent data: no volumes left behind

---

## 📊 Monitoring Phase (Optional)

### Prometheus Setup

- [ ] **Install Prometheus**
  - [ ] Add Helm repo: `helm repo add prometheus-community https://prometheus-community.github.io/helm-charts`
  - [ ] Update: `helm repo update`
  - [ ] Install: `helm install prometheus prometheus-community/kube-prometheus-stack`
  - [ ] Check: `kubectl get pods | grep prometheus`

- [ ] **Access Prometheus**
  - [ ] Port forward: `kubectl port-forward svc/prometheus-kube-prom-prometheus 9090:9090`
  - [ ] Open: http://localhost:9090
  - [ ] Check targets: all showing "UP"
  - [ ] Query example: `up` (checks all targets are up)

- [ ] **App Metrics**
  - [ ] Flask app exposes `/metrics` endpoint
  - [ ] Metrics visible in Prometheus
  - [ ] Example queries working:
    - [ ] `flask_http_requests_total`
    - [ ] `process_resident_memory_bytes`
    - [ ] `python_gc_collections_total`

### Grafana Setup

- [ ] **Install Grafana**
  - [ ] Add repo: `helm repo add grafana https://grafana.github.io/helm-charts`
  - [ ] Install: `helm install grafana grafana/grafana`
  - [ ] Get password: `kubectl get secret grafana -o jsonpath="{.data.admin-password}" | base64 --decode`

- [ ] **Access Grafana**
  - [ ] Port forward: `kubectl port-forward svc/grafana 3000:80`
  - [ ] Open: http://localhost:3000
  - [ ] Login: admin / <password from above>

- [ ] **Datasource Configuration**
  - [ ] Add Prometheus datasource
  - [ ] URL: `http://prometheus-kube-prom-prometheus:9090`
  - [ ] Test connection: "Data source is working"
  - [ ] Save & Test

- [ ] **Dashboard Creation**
  - [ ] Create custom dashboard
  - [ ] Add panels for key metrics:
    - [ ] Request rate
    - [ ] Error rate
    - [ ] Response time
    - [ ] Memory usage
    - [ ] CPU usage
  - [ ] Save dashboard

---

## 📝 Post-Deployment Validation

### Functionality Tests

- [ ] **User Management**
  - [ ] Register new user (student role)
  - [ ] Register new user (teacher role)
  - [ ] Login with credentials
  - [ ] JWT token valid and usable
  - [ ] Logout clears token

- [ ] **Course Management**
  - [ ] Student: Can view courses, cannot create
  - [ ] Teacher: Can view and create courses
  - [ ] Admin: Can view and create courses
  - [ ] Course data persists

- [ ] **Authorization**
  - [ ] Unauthenticated users cannot access /profile
  - [ ] Students cannot POST to /courses
  - [ ] Teachers can POST to /courses
  - [ ] Admin has full access

- [ ] **Database**
  - [ ] Data persists after pod restart
  - [ ] No data loss on redeployment
  - [ ] Database backups working (if configured)

### Performance Tests

- [ ] **Response Times**
  - [ ] GET / < 500ms
  - [ ] POST /login < 1000ms
  - [ ] GET /courses < 500ms
  - [ ] POST /courses < 1000ms

- [ ] **Load Testing** (Optional)
  - [ ] Use `ab` or `hey` to load test
  - [ ] 100 concurrent requests: no errors
  - [ ] 500 concurrent requests: graceful degradation
  - [ ] RPS sustained: > 50 req/sec

- [ ] **Resource Usage**
  - [ ] Pods use < 200MB RAM (typical)
  - [ ] CPU usage < 100m idle
  - [ ] Disk I/O reasonable
  - [ ] No memory leaks over 24 hours

### Security Validation

- [ ] **API Security**
  - [ ] No SQL injection vulnerabilities
  - [ ] JWT tokens validated
  - [ ] CORS headers appropriate
  - [ ] Rate limiting (if implemented)

- [ ] **Data Protection**
  - [ ] Passwords hashed (not plain text)
  - [ ] Sensitive data not logged
  - [ ] Secrets not in config files
  - [ ] HTTPS used (production)

- [ ] **Container Security**
  - [ ] Running as non-root user
  - [ ] Read-only filesystem where possible
  - [ ] Resource limits enforced
  - [ ] Network policies applied

---

## 🔄 Maintenance & Ongoing

### Regular Tasks

- [ ] **Weekly**
  - [ ] Check pod health: `kubectl get pods`
  - [ ] Review error logs: `kubectl logs -f deployment/elearn`
  - [ ] Monitor resource usage: `kubectl top pods`
  - [ ] Verify backup completion (if configured)

- [ ] **Monthly**
  - [ ] Update dependencies: `pip list --outdated`
  - [ ] Security scan: `trivy image elearn:latest`
  - [ ] Database maintenance/optimization
  - [ ] Review Prometheus metrics
  - [ ] Check storage usage

- [ ] **Quarterly**
  - [ ] Performance review: tune resource limits
  - [ ] Security audit: review access logs
  - [ ] Backup restoration test (RTO/RPO check)
  - [ ] Disaster recovery drill

- [ ] **Annually**
  - [ ] Major version upgrades
  - [ ] Kubernetes cluster upgrade
  - [ ] Database migration planning
  - [ ] Architecture review

### Documentation

- [ ] **Runbooks Created**
  - [ ] How to scale deployment
  - [ ] How to update container image
  - [ ] How to rollback deployment
  - [ ] How to handle pod failure
  - [ ] How to access logs

- [ ] **Incident Response**
  - [ ] Incident response plan documented
  - [ ] On-call rotation configured
  - [ ] Alert thresholds defined
  - [ ] Escalation procedure clear

- [ ] **Change Management**
  - [ ] Change log maintained
  - [ ] Rollback procedure tested
  - [ ] Communication plan ready
  - [ ] Version control for all configs

---

## 📊 Final Verification

### Pre-Production Checklist

- [ ] All development tasks completed and tested
- [ ] All security scans passing or documented
- [ ] All tests passing (unit, integration, security)
- [ ] Documentation complete (README, DEVOPS_GUIDE, runbooks)
- [ ] Team trained on deployment procedure
- [ ] Backup and recovery tested
- [ ] Monitoring and alerting configured
- [ ] Incident response plan ready

### Production Sign-Off

- [ ] [ ] Project Lead: ________________  Date: _______
- [ ] [ ] Security Lead: ______________  Date: _______
- [ ] [ ] DevOps Lead: ________________  Date: _______
- [ ] [ ] QA Lead: ____________________  Date: _______

---

## 📞 Quick Help

**Need help?**
- Check `DEVOPS_GUIDE.md` for step-by-step instructions
- Check `QUICK_REFERENCE.md` for common commands
- Review `README.md` for API documentation
- Check logs: `kubectl logs -f deployment/elearn`

**Report Issues:**
- GitHub Issues: [Create an issue]
- Email Support: support@example.com
- Slack: #elearn-devops channel

---

**Last Updated**: November 7, 2025  
**Status**: ✅ Ready for Deployment  
**Estimated Deployment Time**: 30-45 minutes (first time)
