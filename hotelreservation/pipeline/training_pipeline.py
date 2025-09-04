import os
import sys

from hotelreservation.config.config_entities import *
from hotelreservation.utils.main_utils import read_yaml_file
from hotelreservation.logger.logger import logging
from hotelreservation.exception.exception import CustomException
from hotelreservation.components.data_ingestion import DataIngestion
from hotelreservation.components.data_processing import DataProcessor
from hotelreservation.components.model_training import ModelTraining


if __name__ == "__main__":

    try:
        logging.info("Starting the entire training pipeline...")
        
        # Initiating Data Ingestion
        
        data_ingestion = DataIngestion(read_yaml_file(CONFIG_PATH))
        data_ingestion.initiate_data_ingestion()

        # Initiating Data Processing
        
        data_processor = DataProcessor(TRAIN_FILE_PATH, TEST_FILE_PATH, PROCESSED_DIR, CONFIG_PATH)
        data_processor.initiate_data_processing()
        
        # Initiating Model Training

        model_trainer = ModelTraining(PROCESSED_TRAIN_DATA_PATH, PROCESSED_TEST_DATA_PATH, MODEL_PATH)
        model_trainer.initiate_model_training()

    except Exception as e:
        raise CustomException(e, sys)
