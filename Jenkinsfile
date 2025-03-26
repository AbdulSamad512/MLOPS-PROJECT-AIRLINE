pipeline {
    agent any
    
    stages {
        stage('Build Docker image') {
            steps {
                script {
                    echo 'Build Docker image...'
                    docker.build("mlops")
                }
            }
        }
    }
}