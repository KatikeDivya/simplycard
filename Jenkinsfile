
pipeline {
    agent any

    stages {
        stage('Checkout') {
            steps {
                checkout scm
            }
        }

        stage('Check AWS CLI') {
            steps {
                withCredentials([usernamePassword(
                    credentialsId: 'aws-simplycard',
                    usernameVariable: 'AWS_ACCESS_KEY_ID',
                    passwordVariable: 'AWS_SECRET_ACCESS_KEY'
                )]) {
                    bat '''
                        set AWS_DEFAULT_REGION=ap-southeast-2
                        aws --version
                        aws sts get-caller-identity
                    '''
                }
            }
        }
    }
}
