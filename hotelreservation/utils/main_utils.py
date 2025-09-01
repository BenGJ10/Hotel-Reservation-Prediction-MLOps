import os
import sys
import yaml
import pandas as pd
from hotelreservation.logger.logger import logging
from hotelreservation.exception.exception import CustomException

def read_yaml_file(file_path: str) -> dict:
    """
    Reads a YAML file and returns its content as a dictionary.
    """
    try:
        if not os.path.exists(file_path):
            raise FileNotFoundError(f"The file {file_path} does not exist.")
        with open(file_path, "r") as yaml_file:
            logging.info("Successfully read the YAML file")
            return yaml.safe_load(yaml_file)
    
    except Exception as e:
        raise CustomException(e, sys)
    
def load_data(file_path: str):
    """
    Loading data in the form of CSV files
    """
    try:
        return pd.read_csv(file_path) 
    except Exception as e:
        raise CustomException(e, sys)