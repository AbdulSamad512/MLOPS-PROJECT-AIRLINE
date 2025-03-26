pipeline {
    agent any
    
    environment {
        DOCKER_IMAGE = "mlops-airline:latest"
    }
    
    stages {
        stage('Cloning from Github Repo') {
            steps {
                script {
                    echo 'Cloning from Github Repo...'
                    checkout scmGit(branches: [[name: '*/main']], 
                                     extensions: [], 
                                     userRemoteConfigs: [[credentialsId: 'mlops-github-tokens', 
                                                           url: 'https://github.com/AbdulSamad512/MLOPS-PROJECT-AIRLINE.git']])
                }
            }
        }
        
        stage('Build Docker Image') {
            steps {
                script {
                    echo 'Building Docker Image...'
                    sh "docker build -t ${DOCKER_IMAGE} ."
                }
            }
        }

        stage('Run Docker Container') {
            steps {
                script {
                    echo 'Running Docker Container...'
                    sh "docker run -d -p 8080:8080 ${DOCKER_IMAGE}"
                }
            }
        }
    }
}
