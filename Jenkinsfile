
pipeline {
    agent any

    environment {
        AWS_REGION = 'ap-southeast-2'
        ECR_REPOSITORY = '839937205070.dkr.ecr.ap-southeast-2.amazonaws.com/simplycard-prod-app'
    }

    stages {
        stage('Checkout') {
            steps {
                checkout scm
            }
        }

        stage('Build Docker Image') {
            steps {
                bat '''
                    docker build -t simplycard-prod-app:%BUILD_NUMBER% .
                    docker tag simplycard-prod-app:%BUILD_NUMBER% %ECR_REPOSITORY%:%BUILD_NUMBER%
                    docker tag simplycard-prod-app:%BUILD_NUMBER% %ECR_REPOSITORY%:latest
                '''
            }
        }

        stage('Push to ECR') {
            steps {
                withCredentials([usernamePassword(
                    credentialsId: 'aws-simplycard',
                    usernameVariable: 'AWS_ACCESS_KEY_ID',
                    passwordVariable: 'AWS_SECRET_ACCESS_KEY'
                )]) {
                    bat '''
                        set "AWS_DEFAULT_REGION=%AWS_REGION%"
                        aws ecr get-login-password --region %AWS_REGION% | docker login --username AWS --password-stdin 839937205070.dkr.ecr.ap-southeast-2.amazonaws.com

                        docker push %ECR_REPOSITORY%:%BUILD_NUMBER%
                        docker push %ECR_REPOSITORY%:latest
                    '''
                }
            }
        }
    }
}
