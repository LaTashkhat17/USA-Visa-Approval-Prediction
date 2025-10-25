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


