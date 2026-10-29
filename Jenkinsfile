pipeline {
    agent any

    environment {
        DOCKER_IMAGE = 'hello-mlops:alpine'
        PYTHON_VENV = '.venv/bin'
    }

    stages {
        // ============================================================
        // Step 6: Pull the code from github (Handled by Jenkins SCM checkout)
        // ============================================================
        stage('Checkout SCM') {
            steps {
                echo '=== Step 6: Pulling latest code from GitHub repository ==='
                checkout scm
            }
        }

        // ============================================================
        // Setup Python Environment & Dependencies
        // ============================================================
        stage('Install Dependencies') {
            steps {
                echo '=== Setting up Python virtual environment and dependencies ==='
                sh '''
                    if [ ! -d ".venv" ]; then
                        python3 -m venv .venv
                    fi
                    .venv/bin/pip install --upgrade pip
                    .venv/bin/pip install -r requirements.txt
                '''
            }
        }

        // ============================================================
        // Step 11: Configure pytest and print 1 test case
        // ============================================================
        stage('Run Pytest') {
            steps {
                echo '=== Step 11: Running pytest test suite and printing test cases ==='
                sh '''
                    .venv/bin/pytest -s -v --junitxml=pytest_report.xml
                '''
            }
        }

        // ============================================================
        // Step 9 & 10: Pull lightweight python docker image & Add hello.py
        // ============================================================
        stage('Docker Build') {
            steps {
                echo '=== Steps 8, 9 & 10: Building Docker image using lightweight python:3.11-alpine ==='
                sh '''
                    docker build -t ${DOCKER_IMAGE} .
                    docker images | grep hello-mlops || true
                '''
            }
        }

        // ============================================================
        // Run Docker Container
        // ============================================================
        stage('Docker Run') {
            steps {
                echo '=== Running Hello Application inside lightweight Docker container ==='
                sh '''
                    docker run --rm ${DOCKER_IMAGE}
                '''
            }
        }

        // ============================================================
        // Step 12: Configuration Evidently tool & Monitor
        // ============================================================
        stage('Evidently AI Monitoring') {
            steps {
                echo '=== Step 12: Running Evidently AI Drift Detection & Quality Monitoring ==='
                sh '''
                    .venv/bin/python evidently_monitor.py
                '''
            }
        }
    }

    post {
        always {
            echo '=== Pipeline Execution Completed ==='
            // Archive test results and Evidently monitoring reports
            junit allowEmptyResults: true, testResults: 'pytest_report.xml'
            archiveArtifacts artifacts: 'evidently_reports/**, hello.py, Dockerfile', allowEmptyArchive: true
        }
        success {
            echo '=== SUCCESS: All 12 MLOps POE Stages Succeeded! ==='
        }
        failure {
            echo '=== FAILURE: Pipeline failed. Check console logs for debugging. ==='
        }
    }
}
