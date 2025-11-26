pipeline {
    agent any

    // Ask the user to choose INT or PROD at build time
    parameters {
        choice(
            name: 'TARGET_ENV',
            choices: ['INT', 'PROD'],
            description: 'Select environment to deploy the microservices'
        )
    }

    environment {
        IMAGE_A = "ms-service-a"   // Docker image for Service A
        IMAGE_B = "ms-service-b"   // Docker image for Service B
    }

    stages {

        stage('STAGE 1 --> Clone Repo') {
            steps {
                echo "📥 Cloning the GitHub repository..."

                // Explicitly clone your repo (BEGINNER FRIENDLY)
                git branch: 'main', url: 'https://github.com/iddhawan01/multi-branch-architecture.git'

                echo "✔ Repository cloned successfully"
            }
        }

        stage('STAGE 2 --> Check System Requirements') {
            steps {
                sh '''
                    echo "🔍 Checking Docker installation..."
                    docker --version

                    echo "💽 Checking disk space..."
                    df -h
                '''
            }
        }

        stage('STAGE 3 --> Build Docker Images') {
            steps {
                sh '''
                    echo "🐳 Building Docker image for Service A..."
                    docker build -t ms-service-a:latest ./service-a

                    echo "🐳 Building Docker image for Service B..."
                    docker build -t ms-service-b:latest ./service-b
                '''
            }
        }

        stage('STAGE 4 --> Deploy to Selected ENV (INT/PROD)') {
            steps {
                script {

                    echo "Environment Selected: ${params.TARGET_ENV}"

                    if (params.TARGET_ENV == "INT") {

                        echo "🚀 Deploying to INT..."

                        sh '''
                            docker rm -f int-service-a || true
                            docker rm -f int-service-b || true

                            docker run -d --name int-service-a -p 5001:5001 ms-service-a:latest

                            docker run -d --name int-service-b \
                                --link int-service-a:service-a \
                                -p 5002:5002 ms-service-b:latest

                            echo "✔ INT Deployment Completed"
                        '''

                    } else {

                        echo "🚀 Deploying to PROD..."

                        sh '''
                            docker rm -f prod-service-a || true
                            docker rm -f prod-service-b || true

                            docker run -d --name prod-service-a -p 6001:5001 ms-service-a:latest

                            docker run -d --name prod-service-b \
                                --link prod-service-a:service-a \
                                -p 6002:5002 ms-service-b:latest

                            echo "✔ PROD Deployment Completed"
                        '''
                    }
                }
            }
        }

        stage('STAGE 5 --> Health Check') {
            steps {
                script {

                    if (params.TARGET_ENV == "INT") {

                        sh '''
                            echo "🩺 Checking INT services..."
                            curl -I http://localhost:5001 || true
                            curl -I http://localhost:5002 || true
                        '''

                    } else {

                        sh '''
                            echo "🩺 Checking PROD services..."
                            curl -I http://localhost:6001 || true
                            curl -I http://localhost:6002 || true
                        '''
                    }
                }
            }
        }

        stage('STAGE 6 --> Clean Unused Docker Images') {
            steps {
                sh '''
                    echo "🧹 Cleaning docker garbage..."
                    docker image prune -f
                '''
            }
        }
    }

    post {
        success {
            echo "🎉 Deployment Successful!"
        }
        failure {
            echo "❌ Deployment Failed — check console logs."
        }
    }
}
