import sys
from pandas import DataFrame
from sklearn.pipeline import Pipeline

from us_visa.exception import USvisaException
from us_visa.logger import logging


class TargetValueMapping:
    """
    Maps categorical target labels (e.g. 'Certified', 'Denied') 
    to numerical values for ML training, and provides reverse mapping.
    """
    def __init__(self):
        try:
            self.Certified: int = 0
            self.Denied: int = 1
        except Exception as e:
            raise USvisaException(e, sys)

    def _asdict(self) -> dict:
        """
        Returns dictionary representation of the mapping.
        Example: {'Certified': 0, 'Denied': 1}
        """
        try:
            return self.__dict__
        except Exception as e:
            raise USvisaException(e, sys)

    def reverse_mapping(self) -> dict:
        """
        Returns reversed dictionary: {0: 'Certified', 1: 'Denied'}
        """
        try:
            mapping_response = self._asdict()
            return dict(zip(mapping_response.values(), mapping_response.keys()))
        except Exception as e:
            raise USvisaException(e, sys)


class USvisaModel:
    def __init__(self, preprocessing_object: Pipeline, trained_model_object: object):
        """
        :param preprocessing_object: Input Object of preprocesser
        :param trained_model_object: Input Object of trained model 
        """
        self.preprocessing_object = preprocessing_object
        self.trained_model_object = trained_model_object

    def predict(self, dataframe: DataFrame) -> DataFrame:
        """
        Function accepts raw inputs and then transformed raw input using preprocessing_object
        which guarantees that the inputs are in the same format as the training data
        At last it performs prediction on transformed features
        """
        logging.info("Entered predict method of UTruckModel class")

        try:
            logging.info("Using the trained model to get predictions")

            transformed_feature = self.preprocessing_object.transform(dataframe)

            logging.info("Used the trained model to get predictions")
            return self.trained_model_object.predict(transformed_feature)

        except Exception as e:
            raise USvisaException(e, sys) from e

    def __repr__(self):
        return f"{type(self.trained_model_object).__name__}()"

    def __str__(self):
        return f"{type(self.trained_model_object).__name__}()"