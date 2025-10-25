from dataclasses import dataclass

# ---------------------------------------------------------------
# Data Ingestion Artifact
# ---------------------------------------------------------------
@dataclass
class DataIngestionArtifact:
    feature_store_file_path: str
    training_file_path: str
    testing_file_path: str
    is_ingested: bool
    message: str


# ---------------------------------------------------------------
# Data Validation Artifact
# ---------------------------------------------------------------
@dataclass
class DataValidationArtifact:
    schema_file_path: str
    drift_report_file_path: str
    validation_status_file_path: str
    is_validated: bool
    message: str
