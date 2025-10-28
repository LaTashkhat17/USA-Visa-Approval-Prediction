import sys
import numpy as np
import pandas as pd
from imblearn.combine import SMOTEENN
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler, OneHotEncoder, OrdinalEncoder, PowerTransformer
from sklearn.compose import ColumnTransformer

from us_visa.constants import TARGET_COLUMN, SCHEMA_FILE_PATH, CURRENT_YEAR
from us_visa.entity.config_entity import DataTransformationConfig
from us_visa.entity.artifact_entity import (
    DataTransformationArtifact,
    DataIngestionArtifact,
    DataValidationArtifact,
)
from us_visa.exception import USvisaException
from us_visa.logger import logging
from us_visa.utils.main_utils import save_object, save_numpy_array_data, read_yaml_file, drop_columns
from us_visa.entity.estimator import TargetValueMapping


class DataTransformation:
    def __init__(self, data_ingestion_artifact: DataIngestionArtifact,
                 data_transformation_config: DataTransformationConfig,
                 data_validation_artifact: DataValidationArtifact):
        """
        Initialize the DataTransformation class with all artifacts and configuration.
        """
        try:
            self.data_ingestion_artifact = data_ingestion_artifact
            self.data_transformation_config = data_transformation_config
            self.data_validation_artifact = data_validation_artifact
            self._schema_config = read_yaml_file(file_path=SCHEMA_FILE_PATH)
        except Exception as e:
            raise USvisaException(e, sys)

    @staticmethod
    def read_data(file_path) -> pd.DataFrame:
        try:
            return pd.read_csv(file_path)
        except Exception as e:
            raise USvisaException(e, sys)

    def get_data_transformer_object(self) -> Pipeline:
        """
        Creates and returns a data transformation pipeline based on schema configuration.
        """
        logging.info("Entered get_data_transformer_object method of DataTransformation class")

        try:
            numeric_transformer = StandardScaler()
            oh_transformer = OneHotEncoder(handle_unknown="ignore")
            ordinal_encoder = OrdinalEncoder(handle_unknown="use_encoded_value", unknown_value=-1)
            transform_pipe = Pipeline(steps=[('transformer', PowerTransformer(method='yeo-johnson'))])

            oh_columns = self._schema_config['oh_columns']
            or_columns = self._schema_config['or_columns']
            transform_columns = self._schema_config['transform_columns']
            num_features = self._schema_config['num_features']

            preprocessor = ColumnTransformer(
                transformers=[
                    ("OneHotEncoder", oh_transformer, oh_columns),
                    ("OrdinalEncoder", ordinal_encoder, or_columns),
                    ("PowerTransformer", transform_pipe, transform_columns),
                    ("StandardScaler", numeric_transformer, num_features)
                ],
                remainder='drop'
)


            logging.info("Preprocessor object created successfully")
            return preprocessor

        except Exception as e:
            raise USvisaException(e, sys)

    def initiate_data_transformation(self) -> DataTransformationArtifact:
        """
        Executes the transformation process:
        - Reads train/test data
        - Preprocesses features
        - Handles imbalance via SMOTEENN
        - Saves transformed arrays and preprocessing object
        """
        try:
            if not self.data_validation_artifact.is_validated:
                raise Exception("Data Validation failed. Transformation aborted.")

            logging.info("Starting Data Transformation process")

            preprocessor = self.get_data_transformer_object()
            train_df = self.read_data(self.data_ingestion_artifact.training_file_path)
            test_df = self.read_data(self.data_ingestion_artifact.testing_file_path)

            logging.info("Train and Test datasets loaded successfully")

            # Split input & target features
            input_feature_train_df = train_df.drop(columns=[TARGET_COLUMN], axis=1)
            target_feature_train_df = train_df[TARGET_COLUMN]
            input_feature_test_df = test_df.drop(columns=[TARGET_COLUMN], axis=1)
            target_feature_test_df = test_df[TARGET_COLUMN]

            # Add derived feature
            input_feature_train_df['company_age'] = CURRENT_YEAR - input_feature_train_df['yr_of_estab']
            input_feature_test_df['company_age'] = CURRENT_YEAR - input_feature_test_df['yr_of_estab']

            # Drop unnecessary columns
            drop_cols = self._schema_config['drop_columns']
            input_feature_train_df = drop_columns(df=input_feature_train_df, cols=drop_cols)
            input_feature_test_df = drop_columns(df=input_feature_test_df, cols=drop_cols)

            # Encode target values
            target_feature_train_df = target_feature_train_df.replace(TargetValueMapping()._asdict())
            target_feature_test_df = target_feature_test_df.replace(TargetValueMapping()._asdict())

            # Apply preprocessing
            input_feature_train_arr = preprocessor.fit_transform(input_feature_train_df)
            input_feature_test_arr = preprocessor.transform(input_feature_test_df)

            logging.info("Applied preprocessing transformations on datasets")

            # Handle imbalance using SMOTEENN
            smt = SMOTEENN(sampling_strategy="minority")
            input_feature_train_final, target_feature_train_final = smt.fit_resample(
                input_feature_train_arr, target_feature_train_df
            )
            input_feature_test_final, target_feature_test_final = smt.fit_resample(
                input_feature_test_arr, target_feature_test_df
            )

            # Combine input & target arrays
            train_arr = np.c_[input_feature_train_final, np.array(target_feature_train_final)]
            test_arr = np.c_[input_feature_test_final, np.array(target_feature_test_final)]

            # Save transformed data and preprocessor
            save_object(self.data_transformation_config.preprocessing_object_path, preprocessor)
            save_numpy_array_data(self.data_transformation_config.transformed_train_file_path, array=train_arr)
            save_numpy_array_data(self.data_transformation_config.transformed_test_file_path, array=test_arr)

            logging.info("Saved transformed datasets and preprocessing object")

            # Create and return artifact
            data_transformation_artifact = DataTransformationArtifact(
                transformed_train_file_path=self.data_transformation_config.transformed_train_file_path,
                transformed_test_file_path=self.data_transformation_config.transformed_test_file_path,
                preprocessing_object_path=self.data_transformation_config.preprocessing_object_path,
                is_transformed=True,
                message="Data Transformation completed successfully."
            )

            logging.info(f"Data Transformation Artifact: {data_transformation_artifact}")
            return data_transformation_artifact

        except Exception as e:
            raise USvisaException(e, sys)
