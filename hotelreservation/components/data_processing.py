import os
import sys
import numpy as np
import pandas as pd
from sklearn.preprocessing import LabelEncoder
from sklearn.ensemble import RandomForestClassifier
from imblearn.over_sampling import SMOTE

from config.config_entities import *
from hotelreservation.utils.main_utils import load_data, read_yaml_file
from hotelreservation.logger.logger import logging
from hotelreservation.exception.exception import CustomException

class DataProcessor:
    """
    DataProcessor class is responsible for preprocessing the training and testing data.
    It handles missing values, encodes categorical variables, and transforms numerical features
    to reduce skewness. The processed data is then saved to specified file paths."""
    
    def __init__(self, train_path: str, test_path: str, processed_dir: str, config_path: str):
        self.train_path = train_path
        self.test_path = test_path
        self.processed_dir = processed_dir
        self.config = read_yaml_file(config_path)

        # Creating the processed directory in artifacts
        if not os.path.exists(self.processed_dir):
            os.makedirs(self.processed_dir)


    def preprocess_data(self, data: pd.DataFrame) -> pd.DataFrame:
        """
        Preprocess the data by handling missing values, encoding categorical variables,
        and transforming numerical features to reduce skewness.
        """
        try:
            logging.info("Starting Data Preprocessing..")

            logging.info("Dropping unnecessary columns")
            data.drop(columns = ['Unnamed: 0', 'Booking_ID'], inplace = True)

            logging.info("Dropping duplicates")
            data.drop_duplicates(inplace = True)

            categorical_columns = self.config['DataProcessing']['categorical_columns']
            numerical_columns = self.config['DataProcessing']['numerical_columns']
            logging.info(f"There are {len(categorical_columns)} categorical columns and {len(numerical_columns)} numerical columns")

            logging.info("Label Encoding to convert object datatypes into numerical")
            label_encoder = LabelEncoder()
            mappings = {}

            for col in categorical_columns:
                data[col] = label_encoder.fit_transform(data[col])
                mappings[col] = {label: code for label, code in zip(label_encoder.classes_, label_encoder.transform(label_encoder.classes_))}
    
            logging.info("Fixing the skewness in the dataset")
            skewness_threshold = self.config['DataProcessing']['skewness_threshold']
            skewness = data[numerical_columns].apply(lambda x: x.skew())

            # Applying log1p transformation to reduce skewness
            for column in skewness[skewness > skewness_threshold].index:
                data[column] = np.log1p(data[column])

            logging.info("Data Preprocessing successfully completed")
            return data
        
        except Exception as e:
            raise CustomException(e, sys)
        
    
    def balance_data(self, data: pd.DataFrame) -> pd.DataFrame:
        try:
            logging.info("Handling imbalanced data")
            X = data.drop(columns = TARGET_COLUMN)
            Y = data[TARGET_COLUMN]

            logging.info("Applying SMOTE for Data Resampling")
            smote = SMOTE(random_state = 42)
            X_resampled, Y_resampled = smote.fit_resample(X, Y)

            balanced_data = pd.DataFrame(X_resampled, columns = X.columns)
            balanced_data[TARGET_COLUMN] = Y_resampled
            logging.info("Data balanced successfully")

            return balanced_data
        
        except Exception as e:
            raise CustomException(e, sys)
        

    def feature_selection(self, data: pd.DataFrame) -> pd.DataFrame:
        try:
            logging.info("Starting Feature Selection using Random Forest Classifier")
            X = data.drop(columns = TARGET_COLUMN)
            Y = data[TARGET_COLUMN]

            rf_model = RandomForestClassifier(random_state = 42)            
            rf_model.fit(X, Y)
            
            important_features = rf_model.feature_importances_
            important_features_data = pd.DataFrame({
                'feature': X.columns,
                'importance': important_features
            })
            
            logging.info("Selecting the most important 10 features")
            top_important_features_data = important_features_data.sort_values(by = "importance" , ascending = False)
            numerical_features_to_select = self.config['DataProcessing']['numerical_features_to_select']
            top_10_features = top_important_features_data['feature'].head(numerical_features_to_select).values
            logging.info(f"Features Selected: {top_10_features}")
            top_10_data = data[top_10_features.tolist() + [TARGET_COLUMN]]

            logging.info("Feature Selection successfully completed")
            return top_10_data
        
        except Exception as e:
            raise CustomException(e, sys)
        
    def save_data(self, data: pd.DataFrame, file_path: str):
        try:
            logging.info("Saving data into CSV format")
            data.to_csv(file_path, index = False)
            logging.info("Data successfully saved in CSV format")

        except Exception as e:
            raise CustomException(e, sys)

    def initiate_data_processing(self):
        """
        Initiates the data processing components of training pipeline.
        """
        try:
            logging.info("Initiating Data processing..")
        
            train_data = load_data(self.train_path)
            test_data = load_data(self.test_path)

            train_data = self.preprocess_data(data = train_data)
            test_data = self.preprocess_data(data = test_data)

            train_data = self.balance_data(data = train_data)
            test_data = self.balance_data(data = test_data)
                
            train_data = self.feature_selection(data = train_data)
            test_data = test_data[train_data.columns]

            self.save_data(data = train_data, file_path = PROCESSED_TRAIN_DATA_PATH)
            self.save_data(data = test_data, file_path = PROCESSED_TEST_DATA_PATH)
            
            print("Successfully completed Data Processing..")
            logging.info("Data processing successfully completed.")

        except Exception as e:
            raise CustomException(e, sys)
        

if __name__ == "__main__":
    
    data_processor = DataProcessor(train_path = TRAIN_FILE_PATH, test_path = TEST_FILE_PATH, 
                                   processed_dir = PROCESSED_DIR, config_path = CONFIG_PATH,) 
    data_processor.initiate_data_processing()