pipeline {
  agent any
  stages {
    stage('Checkout') { steps { checkout scm } }
    stage('Install') {
      steps { sh 'python -m pip install --upgrade pip && pip install -r requirements.txt' }
    }
    stage('Test') { steps { sh 'pytest -q' } }
    stage('Build Docker') { steps { sh 'docker build -t yourdockerhub/elearn:latest .' } }
    stage('Scan') { steps { sh 'echo "Run Trivy and SonarQube scans here"' } }
    stage('Push') { steps { sh 'echo "Push to registry (use credentials)"' } }
  }
}
