import os
import sys
from dataclasses import dataclass

from xgboost import XGBRegressor
from catboost import CatBoostRegressor
from sklearn.ensemble import (AdaBoostRegressor, GradientBoostingRegressor, RandomForestRegressor)
from sklearn.linear_model import LinearRegression
from sklearn.neighbors import KNeighborsRegressor
from sklearn.tree import DecisionTreeRegressor
from sklearn.metrics import r2_score

from src.logger import logging
from src.exception import CustomException
from src.utils import save_object, evaluate_models

@dataclass
class ModelTrainerConfig:
    trained_model_file_path = os.path.join("artifacts", "model_trainer.pkl")

class ModelTrainer:
    def __init__(self):
        self.model_trainer_config = ModelTrainerConfig()

    def initiate_model_trainer(self, train_array, test_array):
        try:
            logging.info("Splitting training and test input array")
            X_train, Y_train, X_test, Y_test = train_array[:,:-1], train_array[:,-1], test_array[:,:-1], test_array[:,-1]
            models = {"AdaBoost Regressor" : AdaBoostRegressor(), 
                      'Gradient Boosting Regressor': GradientBoostingRegressor(), 
                      'Random Forest': RandomForestRegressor(),
                      'Linear Regression': LinearRegression(),
                      'K-Neighbors': KNeighborsRegressor(),
                      'Decision Tree': DecisionTreeRegressor(),
                      'XGBClassifier': XGBRegressor(),
                      'CatBoosting Regressor': CatBoostRegressor(verbose=False)}
            
            model_report: dict= evaluate_models(X_train= X_train, Y_train=Y_train, X_test=X_test, Y_test=Y_test, models=models)
            best_model_score = max(sorted(model_report.values()))
            best_model_name = list(model_report.keys())[list(model_report.values()).index(best_model_score)]
            best_model = models[best_model_name]

            if best_model_score<0.6:
                raise CustomException("No best model found.")
            
            logging.info(f"Best model : {best_model} found on both training and testing datasets.")

            save_object(
                file_path=self.model_trainer_config.trained_model_file_path,
                obj = best_model
            )

            predicted = best_model.predict(X_test)
            model_score = r2_score(Y_test, predicted)
            return best_model_name, model_score

        except Exception as e:
            raise CustomException(e, sys)
