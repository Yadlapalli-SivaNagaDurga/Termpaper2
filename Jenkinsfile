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
        bat 'docker build -t myimage .'
    }
}


        stage('Snyk Scan') {
            steps {
                script {
                    bat "snyk test --json > snyk_report.json || true"
                    bat "snyk test --docker $IMAGE_NAME --json > snyk_docker_report.json || true"
                }
            }
        }

        stage('RL Decision') {
            steps {
                script {
                    bat 'python3 rl_decision.py'
                }
            }
        }

        stage('Deploy Container') {
            when {
                expression { bat(script: 'python3 rl_decision.py', returnStatus: true) == 0 }
            }
            steps {
                script {
                    bat "docker run -d -p 8501:8501 $IMAGE_NAME"
                }
            }
        }
    }
}
