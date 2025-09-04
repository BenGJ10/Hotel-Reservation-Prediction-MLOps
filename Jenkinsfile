pipeline{
    agent any

    environment{
        VENV_DIR = 'venv'
        GCP_PROJECT = "affable-visitor-470408-s2"
        GCLOUD_PATH = "/var/jenkins_home/google-cloud-sdk/bin"
        IMAGE_NAME = "hrp-mlops-proj"
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
                    
                    pip install --upgrade pip
                    
                    pip install -e .
                    '''
                }
            }
        }

        stage('Build and Push Docker image to Google Container Registry') {
            steps {
                withCredentials([file(credentialsId: 'gcp_mlops_hrp', variable: 'gcp_credentials')]) {
                    script {
                        echo 'Building and Pushing Docker image to Google Container Registry'
                        sh '''
                        export PATH=$PATH:${GCLOUD_PATH}

                        gcloud auth activate-service-account --key-file="${gcp_credentials}"
                        
                        gcloud config set project ${GCP_PROJECT}
                        
                        gcloud auth configure-docker --quiet

                        IMAGE_NAME=hrp-mlops-proj

                        docker build -t gcr.io/${GCP_PROJECT}/${IMAGE_NAME}:latest .
                        
                        docker push gcr.io/${GCP_PROJECT}/${IMAGE_NAME}:latest
                        '''
                    }
                }
            }
        }
    }
}