pipeline {
    agent any

    stages {
        stage('Test Docker') {
            steps {
                bat '''
                    docker --version
                    docker images
                '''
            }
        }
    }
}