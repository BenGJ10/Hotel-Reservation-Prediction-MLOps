import os
import sys

"""
Data Ingestion related paths configuration 
"""
RAW_DIR = "artifacts/data_ingestion"
RAW_FILE_PATH = os.path.join(RAW_DIR, "raw.csv")
TRAIN_FILE_PATH = os.path.join(RAW_DIR, "train.csv")
TEST_FILE_PATH = os.path.join(RAW_DIR, "test.csv")
CONFIG_PATH = "hotelreservation/config/config.yaml"


"""
Data Processing related paths configuration
"""
PROCESSED_DIR = "artifacts/data_processed"
PROCESSED_TRAIN_DATA_PATH = os.path.join(PROCESSED_DIR, "processed_train.csv")
PROCESSED_TEST_DATA_PATH = os.path.join(PROCESSED_DIR, "processed_test.csv")
TARGET_COLUMN = 'booking_status'


"""
Model Training related paths configuration
"""
MODEL_PATH = 'artifacts/model_training/lgbm.pkl'