import os
import sys
import json
import pandas as pd
from evidently.report import Report
from evidently.metric_preset import DataDriftPreset
from us_visa.exception import USvisaException
from us_visa.logger import logging
from us_visa.utils.main_utils import read_yaml_file, write_yaml_file
from us_visa.entity.artifact_entity import DataIngestionArtifact, DataValidationArtifact
from us_visa.entity.config_entity import DataValidationConfig
from us_visa.constants import SCHEMA_FILE_PATH


class DataValidation:
    def __init__(self, data_ingestion_artifact: DataIngestionArtifact,
                 data_validation_config: DataValidationConfig):
        """
        :param data_ingestion_artifact: Output from Data Ingestion stage
        :param data_validation_config: Configuration for data validation stage
        """
        try:
            self.data_ingestion_artifact = data_ingestion_artifact
            self.data_validation_config = data_validation_config
            self._schema_config = read_yaml_file(file_path=SCHEMA_FILE_PATH)
            logging.info("DataValidation initialized successfully (MySQL Version).")
        except Exception as e:
            raise USvisaException(e, sys)

    # ------------------------------------------------------------------
    # 1️ Read Train and Test Data
    # ------------------------------------------------------------------
    @staticmethod
    def read_data(file_path: str) -> pd.DataFrame:
        """
        Reads CSV file as DataFrame.
        """
        try:
            df = pd.read_csv(file_path)
            logging.info(f"Loaded dataset: {file_path} | Shape: {df.shape}")
            return df
        except Exception as e:
            raise USvisaException(e, sys)

    # ------------------------------------------------------------------
    # 2️ Validate Column Count
    # ------------------------------------------------------------------
    def validate_number_of_columns(self, df: pd.DataFrame) -> bool:
        try:
            expected_columns = self._schema_config["columns"]
            status = len(df.columns) == len(expected_columns)
            if not status:
                logging.error(f"Column count mismatch: Expected {len(expected_columns)}, Got {len(df.columns)}")
            else:
                logging.info("Column count validation passed.")
            return status
        except Exception as e:
            raise USvisaException(e, sys)

    # ------------------------------------------------------------------
    # 3️⃣ Validate Required Columns (numerical + categorical)
    # ------------------------------------------------------------------
    def validate_required_columns(self, df: pd.DataFrame) -> bool:
        try:
            missing_columns = []
            for column in self._schema_config["columns"]:
                if column not in df.columns:
                    missing_columns.append(column)

            if len(missing_columns) > 0:
                logging.error(f" Missing columns: {missing_columns}")
                return False

            logging.info("All required columns found in dataset.")
            return True
        except Exception as e:
            raise USvisaException(e, sys)

    # ------------------------------------------------------------------
    # 4️⃣ Detect Data Drift using Evidently
    # ------------------------------------------------------------------
    def detect_data_drift(self, train_df: pd.DataFrame, test_df: pd.DataFrame) -> str:
        """
        Generates Evidently Data Drift Report and saves it as HTML + JSON.
        """
        try:
            logging.info("Generating data drift report...")
            report = Report(metrics=[DataDriftPreset()])
            report.run(reference_data=train_df, current_data=test_df)

            # Save HTML report
            drift_report_html_path = self.data_validation_config.drift_report_file_path
            os.makedirs(os.path.dirname(drift_report_html_path), exist_ok=True)
            report.save_html(drift_report_html_path)

            # Save JSON report
            drift_json_path = drift_report_html_path.replace(".html", ".json")
            report_dict = report.as_dict()
            with open(drift_json_path, "w") as f:
                json.dump(report_dict, f, indent=4)

            logging.info(f" Drift report saved: {drift_report_html_path}")
            return drift_report_html_path

        except Exception as e:
            raise USvisaException(e, sys)

    # ------------------------------------------------------------------
    # 5️⃣ Initiate Data Validation
    # ------------------------------------------------------------------
    def initiate_data_validation(self) -> DataValidationArtifact:
        """
        Executes all validation steps and returns the DataValidationArtifact.
        """
        try:
            logging.info(" Starting Data Validation Process (MySQL Version)...")

            # Load datasets
            train_df = self.read_data(self.data_ingestion_artifact.training_file_path)
            test_df = self.read_data(self.data_ingestion_artifact.testing_file_path)

            # Validate schema
            schema_valid = self.validate_number_of_columns(train_df) and self.validate_required_columns(train_df)
            test_valid = self.validate_number_of_columns(test_df) and self.validate_required_columns(test_df)

            validation_status = schema_valid and test_valid
            message = "Schema validation passed." if validation_status else "Schema validation failed."

            # Generate data drift report if schema is valid
            drift_report_path = None
            if validation_status:
                drift_report_path = self.detect_data_drift(train_df, test_df)
                message += " Drift report generated successfully."
            else:
                message += " Skipping drift detection due to schema mismatch."

            # Prepare artifact
            data_validation_artifact = DataValidationArtifact(
                schema_file_path=self.data_validation_config.schema_file_path,
                drift_report_file_path=drift_report_path or "N/A",
                validation_status_file_path=self.data_validation_config.validation_status_file_path,
                is_validated=validation_status,
                message=message
            )

            # Save validation summary file
            os.makedirs(os.path.dirname(self.data_validation_config.validation_status_file_path), exist_ok=True)
            with open(self.data_validation_config.validation_status_file_path, "w") as f:
                f.write(f"Validation Status: {'PASSED' if validation_status else 'FAILED'}\n")
                f.write(f"Message: {message}\n")

            logging.info(f" Data Validation Completed.\nArtifact: {data_validation_artifact}")
            return data_validation_artifact

        except Exception as e:
            raise USvisaException(e, sys)
