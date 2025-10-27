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


# =======================================================
# DATA TRANSFORMATION ARTIFACT
# =======================================================
@dataclass
class DataTransformationArtifact:
    """
    Contains paths to transformed data and preprocessing object.
    """
    transformed_train_file_path: str
    transformed_test_file_path: str
    preprocessing_object_path: str
    is_transformed: bool
    message: str


@dataclass
class ClassificationMetricArtifact:
    f1_score: float
    accuracy_score: float
    precision_score: float
    recall_score: float


@dataclass
class ModelTrainerArtifact:
    trained_model_file_path: str
    training_metric_artifact: ClassificationMetricArtifact
    is_trained: bool
    message: str
    

@dataclass
class ModelEvaluationArtifact:
    is_model_accepted: bool
    improved_accuracy: float
    best_model_path: str
    trained_model_path: str
    message: str

    
@dataclass
class ModelPusherArtifact:
    pushed_model_google_drive_url: str
    message: str
