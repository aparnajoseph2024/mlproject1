import os
import sys
import dill
import pandas as pd
import numpy as np

from sklearn.metrics import r2_score
from src.exception import CustomException

def save_object(file_path, obj):
    try:
        dir_name = os.path.dirname(file_path)

        os.makedirs(dir_name, exist_ok=True)

        with open(file_path, "wb") as file_obj:
            dill.dump(obj, file_obj)
    except:
        pass

def evaluate_models(X_train, Y_train, X_test, Y_test, models):
    try:
        report = {}
        for i in range(len(list(models))):
            model = list(models.values())[i]

            model.fit(X_train, Y_train)

            Y_train_pred = model.predict(X_train)
            Y_test_pred = model.predict(X_test)

            train_model_score = r2_score(Y_train_pred, Y_train)
            test_model_score = r2_score(Y_test_pred, Y_test)

            report[list(models.keys())[i]] = test_model_score
        return report

    except Exception as e:
        raise CustomException(e, sys)