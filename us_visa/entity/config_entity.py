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
