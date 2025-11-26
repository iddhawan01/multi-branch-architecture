pipeline {
    agent any
    parameters {
        choice(name: 'TARGET_ENV', choices: ['INT', 'PROD'], description: 'Select environment')
    }
    environment {
        IMAGE_A = "ms-service-a"
        IMAGE_B = "ms-service-b"
    }
    stages {
        stage('Checkout') {
            steps { checkout scm }
        }
        stage('Docker Check') {
            steps {
                sh 'docker --version'
                sh 'df -h'
            }
        }
        stage('Build Images') {
            steps {
                sh 'docker build -t ms-service-a:latest ./service-a'
                sh 'docker build -t ms-service-b:latest ./service-b'
            }
        }
        stage('Deploy') {
            steps {
                script {
                    if (params.TARGET_ENV == 'INT') {
                        sh '''
                            docker rm -f int-service-a || true
                            docker rm -f int-service-b || true
                            docker run -d --name int-service-a -p 5001:5001 ms-service-a:latest
                            docker run -d --name int-service-b --link int-service-a:service-a -p 5002:5002 ms-service-b:latest
                        '''
                    } else {
                        sh '''
                            docker rm -f prod-service-a || true
                            docker rm -f prod-service-b || true
                            docker run -d --name prod-service-a -p 6001:5001 ms-service-a:latest
                            docker run -d --name prod-service-b --link prod-service-a:service-a -p 6002:5002 ms-service-b:latest
                        '''
                    }
                }
            }
        }
    }
}
