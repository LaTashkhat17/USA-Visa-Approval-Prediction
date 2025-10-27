import os
from dataclasses import dataclass
from datetime import datetime
from us_visa.constants import *

# Timestamp for artifact versioning
TIMESTAMP: str = datetime.now().strftime("%m_%d_%Y_%H_%M_%S")

# ---------------------------------------------------------------------
# TRAINING PIPELINE CONFIGURATION
# ---------------------------------------------------------------------
@dataclass
class TrainingPipelineConfig:
    """
    Defines base configuration for the overall ML pipeline.
    Creates a timestamped artifact directory for organized workflow outputs.
    """
    pipeline_name: str = PIPELINE_NAME
    artifact_dir: str = os.path.join(ARTIFACT_DIR, TIMESTAMP)
    timestamp: str = TIMESTAMP


training_pipeline_config: TrainingPipelineConfig = TrainingPipelineConfig()

# ---------------------------------------------------------------------
# DATA INGESTION CONFIGURATION (MYSQL VERSION)
# ---------------------------------------------------------------------
@dataclass
class DataIngestionConfig:
    """
    Configuration for data ingestion stage.
    Defines paths for raw data, train/test data, and MySQL table info.
    """
    data_ingestion_dir: str = os.path.join(training_pipeline_config.artifact_dir, DATA_INGESTION_DIR_NAME)
    feature_store_file_path: str = os.path.join(data_ingestion_dir, DATA_INGESTION_FEATURE_STORE_DIR, FILE_NAME)
    training_file_path: str = os.path.join(data_ingestion_dir, DATA_INGESTION_INGESTED_DIR, TRAIN_FILE_NAME)
    testing_file_path: str = os.path.join(data_ingestion_dir, DATA_INGESTION_INGESTED_DIR, TEST_FILE_NAME)
    train_test_split_ratio: float = DATA_INGESTION_TRAIN_TEST_SPLIT_RATIO

    # MySQL-specific configuration
    database_name: str = DATABASE_NAME
    table_name: str = TABLE_NAME


# =======================================================
# ✅ DATA VALIDATION CONFIGURATION
# =======================================================
@dataclass
class DataValidationConfig:
    """
    Configuration for data validation stage.
    Includes schema path, drift report path, and validation status file.
    """
    data_validation_dir: str = os.path.join(training_pipeline_config.artifact_dir, DATA_VALIDATION_DIR_NAME)
    drift_report_file_path: str = os.path.join(
        data_validation_dir, DATA_VALIDATION_DRIFT_REPORT_DIR, DATA_VALIDATION_DRIFT_REPORT_FILE_NAME
    )
    schema_file_path: str = SCHEMA_FILE_PATH
    validation_status_file_path: str = os.path.join(data_validation_dir, DATA_VALIDATION_STATUS_FILE)


# =======================================================
# ✅ DATA VALIDATION ARTIFACT
# =======================================================
@dataclass
class DataValidationArtifact:
    """
    Holds output information from the data validation stage.
    Includes schema info, drift report path, and validation result.
    """
    schema_file_path: str                 # Path to schema.yaml
    drift_report_file_path: str           # Path to Evidently data drift HTML report
    validation_status_file_path: str      # Path to file storing pass/fail result
    is_validated: bool                    # True if validation passed
    message: str                          # Status message


# ---------------------------------------------------------------------
# DATA TRANSFORMATION CONFIGURATION
# ---------------------------------------------------------------------
@dataclass
class DataTransformationConfig:
    """
    Configuration for data transformation:
    Handles transformed datasets and preprocessing object.
    """
    data_transformation_dir: str = os.path.join(training_pipeline_config.artifact_dir, DATA_TRANSFORMATION_DIR_NAME)

    transformed_train_file_path: str = os.path.join(
        data_transformation_dir,
        DATA_TRANSFORMATION_TRANSFORMED_DATA_DIR,
        DATA_TRANSFORMATION_TRAIN_FILE_NAME
    )

    transformed_test_file_path: str = os.path.join(
        data_transformation_dir,
        DATA_TRANSFORMATION_TRANSFORMED_DATA_DIR,
        DATA_TRANSFORMATION_TEST_FILE_NAME
    )

    preprocessing_object_path: str = os.path.join(
        data_transformation_dir,
        DATA_TRANSFORMATION_PREPROCESSING_DIR,
        DATA_TRANSFORMATION_PREPROCESSING_OBJECT_FILE_NAME
    )


@dataclass
class ModelTrainerConfig:
    model_trainer_dir: str = os.path.join(training_pipeline_config.artifact_dir, MODEL_TRAINER_DIR_NAME)
    trained_model_file_path: str = os.path.join(model_trainer_dir, MODEL_TRAINER_TRAINED_MODEL_DIR, MODEL_FILE_NAME)
    expected_accuracy: float = MODEL_TRAINER_EXPECTED_SCORE
    model_config_file_path: str = MODEL_TRAINER_MODEL_CONFIG_FILE_PATH


@dataclass
class ModelEvaluationConfig:
    model_evaluation_dir: str = os.path.join(
        training_pipeline_config.artifact_dir, "model_evaluation"
    )
    report_file_path: str = os.path.join(model_evaluation_dir, "report.yaml")
    threshold: float = 0.01  # minimum improvement needed to accept new model


@dataclass
class ModelPusherConfig:
    model_pusher_dir: str = os.path.join(training_pipeline_config.artifact_dir, "model_pusher")
    saved_model_dir: str = os.path.join("saved_models")
