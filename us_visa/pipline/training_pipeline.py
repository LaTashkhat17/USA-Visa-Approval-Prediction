import sys
from us_visa.exception import USvisaException
from us_visa.logger import logging

# Components
from us_visa.components.data_ingestion import DataIngestion
from us_visa.components.data_validation import DataValidation
from us_visa.components.data_transformation import DataTransformation
from us_visa.components.model_trainer import ModelTrainer
from us_visa.components.model_evaluation import ModelEvaluation
from us_visa.components.model_pusher import ModelPusher

# Entities
from us_visa.entity.config_entity import (
    DataIngestionConfig,
    DataValidationConfig,       
    DataTransformationConfig,
    ModelTrainerConfig,
    ModelEvaluationConfig,
    ModelPusherConfig
)
from us_visa.entity.artifact_entity import (
    DataIngestionArtifact,
    DataValidationArtifact,
    DataTransformationArtifact,
    ModelTrainerArtifact,
    ModelEvaluationArtifact,
    ModelPusherArtifact
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
            self.data_transformation_config = DataTransformationConfig()
            self.model_trainer_config = ModelTrainerConfig()
            self.model_evaluation_config = ModelEvaluationConfig()
            self.model_pusher_config = ModelPusherConfig()

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
    # STEP 3: DATA TRANSFORMATION
    # ----------------------------------------------------------------
    def start_data_transformation(
        self,
        data_ingestion_artifact: DataIngestionArtifact,
        data_validation_artifact: DataValidationArtifact
    ) -> DataTransformationArtifact:
        """
        Transforms data: feature engineering, encoding, scaling, and saves preprocessor.
        """
        try:
            logging.info("Starting Data Transformation process.")
            data_transformation = DataTransformation(
                data_ingestion_artifact=data_ingestion_artifact,
                data_validation_artifact=data_validation_artifact,
                data_transformation_config=self.data_transformation_config
            )
            data_transformation_artifact = data_transformation.initiate_data_transformation()
            logging.info("Data Transformation completed successfully.")
            return data_transformation_artifact
        except Exception as e:
            raise USvisaException(e, sys)



    def start_model_trainer(
            self,
            data_transformation_artifact: DataTransformationArtifact
        ) -> ModelTrainerArtifact:
            """
            Trains the model using the transformed data and saves the trained model.
            """
            try:
                logging.info("Starting Model Training process.")
                model_trainer = ModelTrainer(
                    data_transformation_artifact=data_transformation_artifact,
                    model_trainer_config=self.model_trainer_config
                )
                model_trainer_artifact = model_trainer.initiate_model_trainer()
                logging.info("Model Training completed successfully.")
                return model_trainer_artifact
            except Exception as e:
                raise USvisaException(e, sys)

    # ----------------------------------------------------------------
    # Step 5: Model Evaluation
    # ----------------------------------------------------------------
    def start_model_evaluation(self, model_trainer_artifact: ModelTrainerArtifact) -> ModelEvaluationArtifact:
        try:
            logging.info("Starting Model Evaluation process.")
            model_evaluation = ModelEvaluation(
                model_trainer_artifact=model_trainer_artifact,
                model_evaluation_config=self.model_evaluation_config
            )
            return model_evaluation.initiate_model_evaluation()
        except Exception as e:
            raise USvisaException(e, sys)

   # ----------------------------------------------------------------
    # Step 6: Model Pusher (Google Drive)
    # ----------------------------------------------------------------
    def start_model_pusher(self, model_evaluation_artifact: ModelEvaluationArtifact) -> ModelPusherArtifact:
        try:
            logging.info("Starting Model Pusher process (Google Drive Upload).")
            model_pusher = ModelPusher(
                model_pusher_config=self.model_pusher_config,
                model_evaluation_artifact=model_evaluation_artifact
            )
            return model_pusher.initiate_model_pusher()
        except Exception as e:
            raise USvisaException(e, sys)



    # ----------------------------------------------------------------
    # RUN THE COMPLETE PIPELINE
    # ----------------------------------------------------------------
    def run_pipeline(self):
        try:
            logging.info("Pipeline execution started.")

            # Step 1: Data Ingestion
            data_ingestion_artifact = self.start_data_ingestion()

            # Step 2: Data Validation
            data_validation_artifact = self.start_data_validation(data_ingestion_artifact)

            # Step 3: Data Transformation
            data_transformation_artifact = self.start_data_transformation(
                data_ingestion_artifact=data_ingestion_artifact,
                data_validation_artifact=data_validation_artifact
            )

            # Step 4: Model Training
            model_trainer_artifact = self.start_model_trainer(data_transformation_artifact)

            # Step 5: Model Evaluation
            model_evaluation_artifact = self.start_model_evaluation(model_trainer_artifact)

            # Step 6: Model Pusher (Google Drive Upload)
            model_pusher_artifact = self.start_model_pusher(model_evaluation_artifact)

            logging.info("Pipeline execution completed successfully.")
            logging.info(f"Model uploaded to Google Drive: {model_pusher_artifact.pushed_model_google_drive_url}")

            print("\nPipeline Run Summary:")
            print(f"Data Ingestion Output: {data_ingestion_artifact}")
            print(f"Data Validation Output: {data_validation_artifact}")
            print(f"Data Transformation Output: {data_transformation_artifact}")
            print(f"Model Trainer Output: {model_trainer_artifact}")
            print(f"Model Evaluation Output: {model_evaluation_artifact}")
            print(f"Model Pusher Output: {model_pusher_artifact}")

        except Exception as e:
            raise USvisaException(e, sys)
        