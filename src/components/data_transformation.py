import os
import sys
import pandas as pd
import numpy as np
from dataclasses import dataclass

from sklearn.compose import ColumnTransformer
from sklearn.impute import SimpleImputer
from sklearn.preprocessing import StandardScaler, OneHotEncoder
from sklearn.pipeline import Pipeline

from src.exception import CustomException
from src.logger import logging
from src.utils import save_object

@dataclass
class DataTransformationConfig:
    preprocessor_obj_file_path = os.path.join("artifacts","preprocessor.pkl")

class DataTransformation:
    '''
    This function is for data transformation
    '''

    def __init__(self):
        self.data_transformation_config = DataTransformationConfig()

    def get_data_transformer_obj(self):
        try:
            numerical_features = ['reading_score', 'writing_score']
            categorical_features =['gender', 'race_ethnicity', 'parental_level_of_education', 'lunch', 'test_preparation_course']

            num_pipeline = Pipeline(steps=[
                                    ("imputer",SimpleImputer(strategy="median")),
                                    ("scaler", StandardScaler())
                                    ])
            cat_pipeline = Pipeline(steps=[
                                    ("imputer",SimpleImputer(strategy="most_frequent")),
                                    ("one_hot_encoder", OneHotEncoder()),
                                    ("scaler", StandardScaler(with_mean=False))
                                    ])  
            logging.info(f"Numerical columns: {numerical_features}")
            logging.info(f"Categorical columns: {categorical_features}")  

            preprocessor = ColumnTransformer(
                [
                    ("num_pipeline" , num_pipeline, numerical_features),
                    ("cat_pipeline", cat_pipeline, categorical_features)
                ]
            )

            return preprocessor
                                        
        except Exception as e:
            raise CustomException(e, sys)
        
    def initiate_data_transformation(self, train_path, test_path):
        try:
            train_df = pd.read_csv(train_path)
            test_df = pd.read_csv(test_path)

            logging.info("Read train and test data completed")

            logging.info("Obtaining preprocessing object...")

            preprocessing_obj = self.get_data_transformer_obj()

            target_column_name = "math_score"
            numerical_columns = ['reading_score', 'writing_score']

            input_feature_train_df = train_df.drop(columns=[target_column_name], axis=1)
            target_feature_train_df = train_df[target_column_name]

            input_feature_test_df = test_df.drop(columns=[target_column_name], axis=1)
            target_feature_test_df = test_df[target_column_name]

            logging.info("Applying preprocessing object on training and testing dataframe...")

            input_feature_train = preprocessing_obj.fit_transform(input_feature_train_df)
            input_feature_test = preprocessing_obj.transform(input_feature_test_df)

            train_arr = np.c_[input_feature_train, np.array(target_feature_train_df)]
            test_arr = np.c_[input_feature_test, np.array(target_feature_test_df)]

            save_object(
                file_path = self.data_transformation_config.preprocessor_obj_file_path,
                obj = preprocessing_obj
            )

            logging.info("Saved preprocessing object")

            return (train_arr, test_arr, self.data_transformation_config.preprocessor_obj_file_path)
        except Exception as e:
            raise CustomException(e, sys)