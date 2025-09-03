pipeline{
    agent any

    stages{
        stage('Cloning GitHub repository: Hotel Reservation Prediction to Jenkins'){
            steps{
                script{
                    echo 'Cloning GitHub repository: BenGJ10/Hotel Reservation Prediction to Jenkins...'
                    checkout scmGit(branches: [[name: '*/main']], extensions: [], userRemoteConfigs: [[credentialsId: 'hrp_mlops_github_token', url: 'https://github.com/BenGJ10/Hotel-Reservation-Prediction-MLOps.git']])
                }
            }
        }
    }
}