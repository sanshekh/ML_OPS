import pandas as pd
import numpy as np
import os
from ml_ops import logger
from sklearn.linear_model import ElasticNet
import joblib
from ml_ops.entity.config_entity import ModelEvaluationConfig
from ml_ops.utils.common import save_json
from pathlib import Path
from sklearn.metrics import r2_score, mean_absolute_error, mean_squared_error


class ModelEvaluation:
    def __init__(self, config: ModelEvaluationConfig):
        self.config = config

    def eval_metrics(self, actual, pred):
        rmse = np.sqrt(mean_squared_error(actual, pred))
        mae = mean_absolute_error(actual, pred)
        r2 = r2_score(actual, pred)
        return rmse, mae, r2

    def save_results(self):

        test_data = pd.read_csv(self.config.test_data_path)
        model = joblib.load(self.config.model_path)

        x_test = test_data.drop([self.config.target_column], axis=1)
        y_test = test_data[[self.config.target_column]]

        predicted_qualities = model.predict(x_test)
        (rmse, mae, r2) = self.eval_metrics(y_test, predicted_qualities)

        # Saving metrics as local
        scores = {"rmse": rmse, "mae": mae, "r2": r2}
        save_json(path = Path(self.config.metric_file_name), data=scores)