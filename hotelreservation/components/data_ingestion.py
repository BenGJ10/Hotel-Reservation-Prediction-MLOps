import os
import sys
import pandas as pd
from google.cloud import storage
from sklearn.model_selection import train_test_split

from config.config_entities import *
from hotelreservation.utils.main_utils import read_yaml_file
from hotelreservation.logger.logger import logging
from hotelreservation.exception.exception import CustomException


class DataIngestion:
    """
    DataIngestion class is responsible for ingesting data from a GoogleCloud Storage bucket,
    processing it, and exporting it into a feature store as well as splitting it into
    training and testing datasets. It handles the connection to the database,
    retrieves the data, and manages the file paths for the feature store and datasets.
    """

    def __init__(self, config):
        self.config = config["DataIngestion"]
        self.bucket_name = self.config["bucket_name"]
        self.bucket_file_name = self.config["bucket_file_name"]
        self.train_ratio = self.config["train_ratio"]

        # Creating a raw directory for artifacts
        os.makedirs(RAW_DIR, exist_ok = True)
        logging.info(f"Got bucket: {self.bucket_name} and file: {self.bucket_file_name} from Google Cloud.")

    def download_data_from_gcp(self):
        try:
            client = storage.Client()
            bucket = client.bucket(self.bucket_name)
            blob = bucket.blob(self.bucket_file_name)

            # Downloading the file from GCP to RAW_FILE_PATH
            blob.download_to_filename(RAW_FILE_PATH)
            logging.info(f"CSV file successfully downloaded to {RAW_FILE_PATH}")
        
        except Exception as e:
            raise CustomException(e, sys)
        
    def split_data_with_ratio(self):
        try:
            data = pd.read_csv(RAW_FILE_PATH)

            # Splitting the data into train and test data
            train_data, test_data = train_test_split(data, test_size = 1 - self.train_ratio, random_state = 42)

            # Converting to CSV files
            train_data.to_csv(TRAIN_FILE_PATH)
            test_data.to_csv(TEST_FILE_PATH)
            logging.info(f"Train data saved to {TRAIN_FILE_PATH}")
            logging.info(f"Test data saved to {TEST_FILE_PATH}")

        except Exception as e:
            raise CustomException(e, sys)
        
    
    def initiate_data_ingestion(self):
        """
        Initiates the data ingestion components of training pipeline.
        """
        try:
            logging.info("Initiating Data ingestion..")
        
            self.download_data_from_gcp()
            self.split_data_with_ratio()
            
            print("Successfully completed Data Ingestion..")
            logging.info("Data ingestion successfully completed.")

        except Exception as e:
            raise CustomException(e, sys)
        

if __name__ == "__main__":

    config = read_yaml_file(CONFIG_PATH)
    data_ingestion = DataIngestion(config = config)
    data_ingestion.initiate_data_ingestion()
    