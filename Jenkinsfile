pipeline {
    agent any

    environment {
        IMAGE_A = "ms-service-a"
        IMAGE_B = "ms-service-b"
    }

    stages {

        stage('Checkout Code') {
            steps {
                checkout scm
                echo "Branch being built: ${env.BRANCH_NAME}"
            }
        }

        stage('Build Docker Images') {
            steps {
                sh '''
                    echo "🐳 Building image for Service A..."
                    docker build -t ms-service-a:latest ./service-a

                    echo "🐳 Building image for Service B..."
                    docker build -t ms-service-b:latest ./service-b
                '''
            }
        }

        stage('Deploy Based on Branch') {
            steps {
                script {

                    if (env.BRANCH_NAME == "INT") {
                        echo "🚀 Deploying to INT environment..."

                        sh '''
                            docker rm -f int-service-a || true
                            docker rm -f int-service-b || true

                            docker run -d --name int-service-a -p 5001:5001 ms-service-a:latest

                            docker run -d --name int-service-b \
                                --link int-service-a:service-a \
                                -p 5002:5002 ms-service-b:latest

                            echo "✔ INT Deployment done"
                        '''
                    }

                    else if (env.BRANCH_NAME == "PROD") {
                        echo "🚀 Deploying to PROD environment..."

                        sh '''
                            docker rm -f prod-service-a || true
                            docker rm -f prod-service-b || true

                            docker run -d --name prod-service-a -p 6001:5001 ms-service-a:latest

                            docker run -d --name prod-service-b \
                                --link prod-service-a:service-a \
                                -p 6002:5002 ms-service-b:latest

                            echo "✔ PROD Deployment done"
                        '''
                    }

                    else {
                        echo "🛑 Not deploying this branch (not INT or PROD)"
                    }
                }
            }
        }

        stage('Health Check') {
            when { anyOf { branch 'INT'; branch 'PROD' } }
            steps {
                script {
                    if (env.BRANCH_NAME == 'INT') {
                        sh '''
                            curl -s http://localhost:5001 || true
                            curl -s http://localhost:5002 || true
                        '''
                    } else {
                        sh '''
                            curl -s http://localhost:6001 || true
                            curl -s http://localhost:6002 || true
                        '''
                    }
                }
            }
        }
    }

    post {
        success {
            echo "🎉 Deployment success for branch: ${env.BRANCH_NAME}"
        }
        failure {
            echo "❌ Deployment failed for branch: ${env.BRANCH_NAME}"
        }
    }
}
