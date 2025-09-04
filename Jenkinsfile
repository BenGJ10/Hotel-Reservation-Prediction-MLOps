pipeline{
    agent any

    environment{
        VENV_DIR = 'venv'
        GCP_PROJECT = 'affable-visitor-470408-s2'
        GCLOUD_PATH = '/var/jenkins_home/google-cloud-sdk/bin'
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
                        export PATH=$PATH:${GCLOUD_PATH}

                        gcloud auth activate-service-account --key-file=${GOOGLE_APPLICATION_CREDENTIALS}

                        gcloud config set project ${GCP_PROJECT}

                        gcloud auth configure-docker --quiet

                        docker build -t gcr.io/${GCP_PROJECT}/ml-project:latest .

                        docker push gcr.io/${GCP_PROJECT}/ml-project:latest 
                        '''
                    }
                }
            }
        }
    }
}