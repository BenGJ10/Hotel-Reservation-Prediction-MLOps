pipeline{
    agent any

    environment{
        VENV_DIR = 'venv'
        GCP_PROJECT = 'affable-visitor-470408-s2'
        GCLOUD_PATH = '/var/jenkins_home/google-cloud-sdk/bin'
        IMAGE_NAME = 'hrp-mlops-proj'
    }
    stages{
        stage('Cloning GitHub repository: Hotel Reservation Prediction to Jenkins'){
            steps{
                script{
                    echo 'Cloning GitHub repository: BenGJ10/Hotel Reservation Prediction to Jenkins...'
                    checkout scmGit(branches: [[name: '*/main']], extensions: [], userRemoteConfigs: [[credentialsId: 'github_hrp_token', url: 'https://github.com/BenGJ10/Hotel-Reservation-Prediction-MLOps']])
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
                    
                    pip install --upgrade pip
                    
                    pip install -e .
                    '''
                }
            }
        }

        stage('Build and Push Docker image to Google Container Registry') {
            steps {
                withCredentials([file(credentialsId: 'gcp_credentials', variable: 'gcp_creds')]) {
                    script {
                        echo 'Building Docker image with GCP credentials...'
                        sh '''

                        docker build \
                            --build-arg GCP_CREDS_FILE="${gcp_creds}" \
                            -t gcr.io/${GCP_PROJECT}/${IMAGE_NAME}:latest .

                        docker push gcr.io/${GCP_PROJECT}/${IMAGE_NAME}:latest
                        '''
                    }
                }
            }
        }
    }
}