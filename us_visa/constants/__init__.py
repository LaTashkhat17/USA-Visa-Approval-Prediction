import os
from datetime import date

# ---------------- Database Configuration ----------------
DATABASE_NAME = "us_visa"          # Your MySQL database name
TABLE_NAME = "applicants"          # The table name in MySQL

# ---------------- Pipeline Configuration ----------------
PIPELINE_NAME: str = "usvisa"
ARTIFACT_DIR: str = "artifacts"

# ---------------- Model & File Configurations ----------------
MODEL_FILE_NAME: str = "model.pkl"
PREPROCESSING_OBJECT_FILE_NAME: str = "preprocessing.pkl"

# ---------------- Data Files ----------------
FILE_NAME: str = "usvisa.csv"
TRAIN_FILE_NAME: str = "train.csv"
TEST_FILE_NAME: str = "test.csv"

# ---------------- Target and Year ----------------
TARGET_COLUMN: str = "case_status"
CURRENT_YEAR: int = date.today().year

# ---------------- Schema Path ----------------
SCHEMA_FILE_PATH: str = os.path.join("config", "schema.yaml")


# =======================================================
# 🧩 DATA INGESTION RELATED CONSTANTS
# =======================================================
DATA_INGESTION_DIR_NAME: str = "data_ingestion"
DATA_INGESTION_FEATURE_STORE_DIR: str = "feature_store"
DATA_INGESTION_INGESTED_DIR: str = "ingested"
DATA_INGESTION_TRAIN_TEST_SPLIT_RATIO: float = 0.2

# =======================================================
# ✅ DATA VALIDATION CONSTANTS
# =======================================================
DATA_VALIDATION_DIR_NAME: str = "data_validation"  # Folder for validation outputs
DATA_VALIDATION_DRIFT_REPORT_DIR: str = "drift_report"  # Subfolder for drift reports
DATA_VALIDATION_DRIFT_REPORT_FILE_NAME: str = "data_drift_report.html"  # HTML report file
DATA_VALIDATION_SCHEMA_FILE_NAME: str = "schema.yaml"  # Schema file
DATA_VALIDATION_STATUS_FILE: str = "validation_status.txt"  # Optional file to log validation result


# =======================================================
# DATA TRANSFORMATION CONSTANTS
# =======================================================
DATA_TRANSFORMATION_DIR_NAME: str = "data_transformation"
DATA_TRANSFORMATION_TRANSFORMED_DATA_DIR: str = "transformed"
DATA_TRANSFORMATION_PREPROCESSING_DIR: str = "preprocessing"
DATA_TRANSFORMATION_PREPROCESSING_OBJECT_FILE_NAME: str = "preprocessor.pkl"
DATA_TRANSFORMATION_TRAIN_FILE_NAME: str = "train_transformed.csv"
DATA_TRANSFORMATION_TEST_FILE_NAME: str = "test_transformed.csv"



"""
MODEL TRAINER related constant start with MODEL_TRAINER var name
"""
MODEL_TRAINER_DIR_NAME: str = "model_trainer"
MODEL_TRAINER_TRAINED_MODEL_DIR: str = "trained_model"
MODEL_TRAINER_TRAINED_MODEL_NAME: str = "model.pkl"
MODEL_TRAINER_EXPECTED_SCORE: float = 0.6
MODEL_TRAINER_MODEL_CONFIG_FILE_PATH: str = os.path.join("config", "model.yaml")


MODEL_EVALUATION_CHANGED_THRESHOLD_SCORE: float = 0.02
MODEL_BUCKET_NAME = "usvisabucket25"
MODEL_PUSHER_S3_KEY = "model-registry"