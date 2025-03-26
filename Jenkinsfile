pipeline {
    agent any
    
    stages {
        stage('Cloning from Github Repo') {
            steps {
                script {
                    echo 'Cloning from Github Repo...'
                    checkout scmGit(branches: [[name: '*/main']], extensions: [], userRemoteConfigs: [[credentialsId: 'mlops-github-tokens', url: 'https://github.com/AbdulSamad512/MLOPS-PROJECT-AIRLINE.git']])
                }
            }
        }
    }
}
