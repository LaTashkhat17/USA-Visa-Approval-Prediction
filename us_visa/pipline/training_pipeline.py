import sys
from us_visa.exception import USvisaException
from us_visa.logger import logging

# Components
from us_visa.components.data_ingestion import DataIngestion
from us_visa.components.data_validation import DataValidation

# Entities
from us_visa.entity.config_entity import (
    DataIngestionConfig,
    DataValidationConfig
)
from us_visa.entity.artifact_entity import (
    DataIngestionArtifact,
    DataValidationArtifact
)


class TrainingPipeline:
    """
    Class Name :   TrainingPipeline
    Description :  Executes the Data Ingestion and Data Validation components
                   sequentially using MySQL as the data source.
    """

    def __init__(self):
        try:
            logging.info("Initializing TrainingPipeline for Data Ingestion and Validation (MySQL).")

            # Configuration entities
            self.data_ingestion_config = DataIngestionConfig()
            self.data_validation_config = DataValidationConfig()

        except Exception as e:
            raise USvisaException(e, sys)

    # ----------------------------------------------------------------
    # Step 1: Data Ingestion
    # ----------------------------------------------------------------
    def start_data_ingestion(self) -> DataIngestionArtifact:
        """
        Starts the data ingestion component.
        Fetches data from MySQL, saves it into the feature store,
        and splits into training and testing datasets.
        """
        try:
            logging.info("Starting Data Ingestion process.")
            data_ingestion = DataIngestion(data_ingestion_config=self.data_ingestion_config)
            data_ingestion_artifact = data_ingestion.initiate_data_ingestion()
            logging.info("Data Ingestion completed successfully.")
            return data_ingestion_artifact
        except Exception as e:
            raise USvisaException(e, sys)

    # ----------------------------------------------------------------
    # Step 2: Data Validation
    # ----------------------------------------------------------------
    def start_data_validation(self, data_ingestion_artifact: DataIngestionArtifact) -> DataValidationArtifact:
        """
        Starts the data validation component.
        Validates schema, checks missing columns, and detects data drift.
        """
        try:
            logging.info("Starting Data Validation process.")
            data_validation = DataValidation(
                data_ingestion_artifact=data_ingestion_artifact,
                data_validation_config=self.data_validation_config
            )
            data_validation_artifact = data_validation.initiate_data_validation()
            logging.info("Data Validation completed successfully.")
            return data_validation_artifact
        except Exception as e:
            raise USvisaException(e, sys)

    # ----------------------------------------------------------------
    # Step 3: Run Pipeline
    # ----------------------------------------------------------------
    def run_pipeline(self):
        """
        Executes the full training pipeline up to the data validation stage.
        """
        try:
            logging.info("Pipeline execution started.")

            # Step 1: Data Ingestion
            data_ingestion_artifact = self.start_data_ingestion()

            # Step 2: Data Validation
            data_validation_artifact = self.start_data_validation(data_ingestion_artifact=data_ingestion_artifact)

            logging.info("Pipeline execution completed successfully.")
            logging.info(f"Data Ingestion Artifact: {data_ingestion_artifact}")
            logging.info(f"Data Validation Artifact: {data_validation_artifact}")

            print("\nPipeline Run Summary:")
            print(f"Data Ingestion Output: {data_ingestion_artifact}")
            print(f"Data Validation Output: {data_validation_artifact}")

        except Exception as e:
            raise USvisaException(e, sys)
