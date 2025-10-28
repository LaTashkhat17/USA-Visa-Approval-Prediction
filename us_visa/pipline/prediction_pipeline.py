import sys
import pandas as pd
from us_visa.logger import logging
from us_visa.exception import USvisaException
from us_visa.utils.main_utils import load_object
from us_visa.entity.estimator import USvisaModel


class PredictionPipeline:
    """
    Handles loading the trained model and preprocessor,
    accepting new user inputs, and returning predictions.
    """

    def __init__(self, model_path: str, preprocessor_path: str):
        try:
            logging.info("Initializing PredictionPipeline.")
            self.model = load_object(model_path)
            self.preprocessor = load_object(preprocessor_path)
            logging.info("Model and Preprocessor loaded successfully.")
        except Exception as e:
            raise USvisaException(e, sys)

    def predict(self, input_data: pd.DataFrame):
        """
        Accepts a Pandas DataFrame (raw input), preprocesses it,
        and returns predictions as human-readable labels.
        """
        try:
            logging.info("Starting prediction process.")
            transformed_data = self.preprocessor.transform(input_data)
            preds = self.model.trained_model_object.predict(transformed_data)
            
            # Convert numeric prediction to label
            mapping = {0: "Certified", 1: "Denied"}
            return [mapping[p] for p in preds]
        except Exception as e:
            raise USvisaException(e, sys)

