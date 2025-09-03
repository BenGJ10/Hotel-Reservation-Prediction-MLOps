pipeline{
    agent any

    environment{
        VENV_DIR = 'venv'
    }
    stages{
        stage('Cloning GitHub repository: Hotel Reservation Prediction to Jenkins'){
            steps{
                script{
                    echo 'Cloning GitHub repository: BenGJ10/Hotel Reservation Prediction to Jenkins...'
                    checkout scmGit(branches: [[name: '*/main']], extensions: [], userRemoteConfigs: [[credentialsId: 'hrp_mlops_github_token', url: 'https://github.com/BenGJ10/Hotel-Reservation-Prediction-MLOps.git']])
                }
            }
        }

        stage('Setting up virtual environment and installing dependencies'){
            steps{
                script{
                    echo 'Setting up virtual environment: venv and installing dependencies...'
                    sh'''
                    python -m venv ${VENV_DIR}
                    . ${VENV_DIR}/bin/activate
                    pip install upgrade pip
                    pip install -e .
                    '''
                }
            }
        }
    }
}