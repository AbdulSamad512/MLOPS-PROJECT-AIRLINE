pipeline {
    agent any
    
    environment {
        DOCKER_IMAGE = 'mlops-airline:latest'
        DOCKER_USERNAME = credentials('dockerhub-username')
        DOCKER_PASSWORD = credentials('dockerhub-password')
        REPO_URL = 'https://github.com/AbdulSamad512/MLOPS-PROJECT-AIRLINE.git'
        GITHUB_CREDENTIALS = 'mlops-github-tokens'
    }
    
    stages {
        stage('Cloning from Github Repo') {
            steps {
                script {
                    echo 'Cloning from Github Repo...'
                    checkout scmGit(branches: [[name: '*/main']], extensions: [], userRemoteConfigs: [[credentialsId: GITHUB_CREDENTIALS, url: REPO_URL]])
                }
            }
        }

        stage('Build Docker Image') {
            steps {
                script {
                    echo 'Building Docker Image...'
                    sh 'docker build -t $DOCKER_IMAGE .'
                }
            }
        }

        stage('Login to Docker Hub') {
            steps {
                script {
                    echo 'Logging in to Docker Hub...'
                    sh 'echo $DOCKER_PASSWORD | docker login -u $DOCKER_USERNAME --password-stdin'
                }
            }
        }

        stage('Push Docker Image to Docker Hub') {
            steps {
                script {
                    echo 'Tagging and Pushing Docker Image...'
                    sh 'docker tag $DOCKER_IMAGE $DOCKER_USERNAME/$DOCKER_IMAGE'
                    sh 'docker push $DOCKER_USERNAME/$DOCKER_IMAGE'
                }
            }
        }

        stage('Run Docker Container') {
            steps {
                script {
                    echo 'Running Docker Container...'
                    sh 'docker run -d -p 8080:8080 $DOCKER_IMAGE'
                }
            }
        }
    }

    post {
        success {
            echo 'Pipeline executed successfully!'
        }
        failure {
            echo 'Pipeline failed! Check the logs for details.'
        }
    }
}
