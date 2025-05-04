pipeline {
    agent any

    environment {
        IMAGE_NAME = 'term-paper'
    }

    stages {
        stage('Checkout') {
            steps {
                git 'https://github.com/Yadlapalli-SivaNagaDurga/Termpaper2.git'
            }
        }

        stage('Build Docker Image') {
            steps {
                script {
                    sh "docker build -t $IMAGE_NAME ."
                }
            }
        }

        stage('Snyk Scan') {
            steps {
                script {
                    sh "snyk test --json > snyk_report.json || true"
                    sh "snyk test --docker $IMAGE_NAME --json > snyk_docker_report.json || true"
                }
            }
        }

        stage('RL Decision') {
            steps {
                script {
                    sh 'python3 rl_decision.py'
                }
            }
        }

        stage('Deploy Container') {
            when {
                expression { sh(script: 'python3 rl_decision.py', returnStatus: true) == 0 }
            }
            steps {
                script {
                    sh "docker run -d -p 8501:8501 $IMAGE_NAME"
                }
            }
        }
    }
}
