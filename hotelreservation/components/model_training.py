import os
import sys
import pickle
import numpy as np
import pandas as pd
import lightgbm as lgbm
from scipy.stats import randint
from sklearn.model_selection import RandomizedSearchCV
from sklearn.metrics import accuracy_score, recall_score, precision_score, f1_score

import mlflow
import mlflow.sklearn
from config.config_entities import *
from config.model_params import *
from hotelreservation.utils.main_utils import load_data, read_yaml_file
from hotelreservation.logger.logger import logging
from hotelreservation.exception.exception import CustomException

class ModelTraining:
    """
    This class is responsible for training and evaluating the machine learning model.
    It utilizes LightGBM as the primary algorithm for classification tasks. 
    Model training and evaluation are performed using MLflow for tracking experiments.
    """
    def __init__(self, train_path: str, test_path: str, model_path: str):
        self.train_path = train_path
        self.test_path = test_path
        self.model_path = MODEL_PATH

        self.lgbm_params = LIGHTGBM_PARAMS
        self.random_search_params = RANDOM_SEARCH_PARAMS

    def load_and_split_data(self):
        """
        Load the training and testing data from specified file paths and split them into features and target variable.

        """
        try:
            logging.info(f"Loading data from {self.train_path}")
            train_data = load_data(self.train_path)

            logging.info(f"Loading data from {self.test_path}")
            test_data = load_data(self.test_path)

            logging.info("Train-Test Splitting")
            X_train = train_data.drop(columns = [TARGET_COLUMN])
            Y_train = train_data[TARGET_COLUMN]
            X_test = test_data.drop(columns = [TARGET_COLUMN])
            Y_test = test_data[TARGET_COLUMN]

            logging.info("Data Successfully splitted")
            return X_train, Y_train, X_test, Y_test

        except Exception as e:
            raise CustomException(e, sys)

            
    def train_lgbm_model(self, X_train, Y_train):
        """
        Train the LightGBM model using the provided training data.
        """
        try:
            logging.info("Initializing LGBM Model")
            lgbm_model = lgbm.LGBMClassifier(random_state = self.random_search_params["random_state"])
            
            logging.info("Starting Hyperparameter Tuning..")
            random_search_cv = RandomizedSearchCV(
                estimator = lgbm_model,
                param_distributions = self.lgbm_params,
                n_iter = self.random_search_params["n_iter"],
                cv = self.random_search_params["cv"],
                n_jobs = self.random_search_params["n_jobs"],
                verbose = self.random_search_params["verbose"],
                random_state = self.random_search_params["random_state"],
                scoring = self.random_search_params["scoring"]
            )

            random_search_cv.fit(X_train, Y_train)
            logging.info("Completed Hyperparameter Tuning")

            best_params = random_search_cv.best_params_
            best_lgbm_model = random_search_cv.best_estimator_
            logging.info(f"Best parameters are {best_params}")

            return best_lgbm_model
        
        except Exception as e:
            raise CustomException(e, sys)

    def evaluate_model(self, model, X_test, Y_test):
        """
        Evaluate the trained model using the test dataset.
        """
        try:
            logging.info("Starting Model Evaluation..")
            Y_pred = model.predict(X_test)

            accuracy = accuracy_score(Y_test, Y_pred)
            precision = precision_score(Y_test, Y_pred)
            recall = recall_score(Y_test, Y_pred)
            f1 = f1_score(Y_test, Y_pred)

            logging.info(f"Accuracy Score: {accuracy}")
            logging.info(f"Precision Score: {precision}")
            logging.info(f"Recall Score: {recall}")
            logging.info(f"F1 Score: {f1}")
            
            return {
                "accuracy": accuracy,
                "precision": precision,
                "recall": recall,
                "f1": f1
            }
        
        except Exception as e:
            raise CustomException(e, sys)
        
    def save_model(self, model):
        """
        Save the trained model to the specified path.
        """
        try:
            logging.info("Saving the final model..")
            os.makedirs(os.path.dirname(self.model_path), exist_ok = True)

            with open(self.model_path, "wb") as file:
                pickle.dump(model, file)
            logging.info(f"Model saved to {self.model_path}")

        except Exception as e:
            raise CustomException(e, sys)
        

    def initiate_model_training(self):
        """
        Initiates the model training components of training pipeline.
        Also sets up MLflow for experiment tracking.
        """
        try:
            with mlflow.start_run():
                logging.info("Initiating Model Training..")
                logging.info("Starting MLFlow experimentation..")

                logging.info("Saving training and testing data into MLFlow")
                mlflow.log_artifact(self.train_path, artifact_path = "datasets") # Logging training data artifact
                mlflow.log_artifact(self.test_path, artifact_path = "datasets") # Logging testing data artifact

                X_train, Y_train, X_test, Y_test = self.load_and_split_data()

                best_lgbm_model = self.train_lgbm_model(X_train, Y_train)
                
                metrics = self.evaluate_model(model = best_lgbm_model, X_test = X_test, Y_test = Y_test)

                self.save_model(best_lgbm_model)
                
                logging.info("Saving the model into MLFlow")
                mlflow.log_artifact(self.model_path, artifact_path = "models") # Logging model artifact

                logging.info("Saving params and metrics into MLFlow")
                mlflow.log_params(best_lgbm_model.get_params()) # Logging model parameters
                mlflow.log_metrics(metrics = metrics)           # Logging model metrics

                print("Successfully completed Model Training..")
                logging.info("Model training successfully completed.")

        except Exception as e:
            raise CustomException(e, sys)
        

if __name__ == "__main__":
    
    model_trainer = ModelTraining(train_path = PROCESSED_TRAIN_DATA_PATH, test_path = PROCESSED_TEST_DATA_PATH,
                                  model_path = MODEL_PATH)
    
    model_trainer.initiate_model_training()