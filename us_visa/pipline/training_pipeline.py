import sys
from us_visa.exception import USvisaException
from us_visa.logger import logging

from us_visa.components.data_ingestion import DataIngestion
from us_visa.entity.config_entity import DataIngestionConfig
from us_visa.entity.artifact_entity import DataIngestionArtifact


class TrainingPipeline:
    """
    Class Name :   TrainingPipeline
    Description :  This pipeline currently handles only the Data Ingestion process.
                   It fetches data from MySQL, saves it to the feature store, and splits it into train/test sets.
    """

    def __init__(self):
        try:
            logging.info("Initializing TrainingPipeline for Data Ingestion only.")
            self.data_ingestion_config = DataIngestionConfig()
        except Exception as e:
            raise USvisaException(e, sys)

    def start_data_ingestion(self) -> DataIngestionArtifact:
        """
        Starts the data ingestion component — fetches data from MySQL,
        saves it into the feature store, and creates train/test splits.
        """
        try:
            logging.info("Starting Data Ingestion process (MySQL)...")
            data_ingestion = DataIngestion(data_ingestion_config=self.data_ingestion_config)
            data_ingestion_artifact = data_ingestion.initiate_data_ingestion()
            logging.info("Data Ingestion completed successfully.")
            return data_ingestion_artifact
        except Exception as e:
            raise USvisaException(e, sys)

    def run_pipeline(self):
        """
        Runs the Data Ingestion pipeline only.
        """
        try:
            logging.info(" Running TrainingPipeline (Data Ingestion Stage Only)")
            data_ingestion_artifact = self.start_data_ingestion()
            logging.info(f"Data Ingestion Pipeline completed.\nArtifact: {data_ingestion_artifact}")
        except Exception as e:
            raise USvisaException(e, sys)
