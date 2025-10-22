import os
import sys
from pandas import DataFrame
from sklearn.model_selection import train_test_split

from us_visa.entity.config_entity import DataIngestionConfig
from us_visa.entity.artifact_entity import DataIngestionArtifact
from us_visa.exception import USvisaException
from us_visa.logger import logging
from us_visa.data_access.usvisa_data import USvisaData


class DataIngestion:
    def __init__(self, data_ingestion_config: DataIngestionConfig = DataIngestionConfig()):
        """
        :param data_ingestion_config: configuration for data ingestion
        """
        try:
            self.data_ingestion_config = data_ingestion_config
            logging.info("DataIngestionConfig initialized successfully.")
        except Exception as e:
            raise USvisaException(e, sys)
        

    def export_data_into_feature_store(self) -> DataFrame:
        """
        Method Name :   export_data_into_feature_store
        Description :   This method exports data from MySQL into a CSV file.

        Output      :   Data is returned as a pandas DataFrame.
        On Failure  :   Write an exception log and then raise an exception.
        """
        try:
            logging.info(f" Exporting data from MySQL database: {self.data_ingestion_config.database_name}")
            
            # Fetch data from MySQL using the USvisaData class
            usvisa_data = USvisaData(database_name=self.data_ingestion_config.database_name)
            dataframe = usvisa_data.export_table_as_dataframe(table_name=self.data_ingestion_config.table_name)

            logging.info(f" Data fetched successfully with shape: {dataframe.shape}")

            # Save the data to the feature store directory
            feature_store_file_path = self.data_ingestion_config.feature_store_file_path
            dir_path = os.path.dirname(feature_store_file_path)
            os.makedirs(dir_path, exist_ok=True)

            logging.info(f" Saving exported data into feature store path: {feature_store_file_path}")
            dataframe.to_csv(feature_store_file_path, index=False, header=True)

            logging.info(f" Data successfully saved to feature store: {feature_store_file_path}")
            return dataframe

        except Exception as e:
            raise USvisaException(e, sys)


    def split_data_as_train_test(self, dataframe: DataFrame) -> None:
        """
        Method Name :   split_data_as_train_test
        Description :   This method splits the DataFrame into train and test sets based on the split ratio.

        Output      :   Train and test files are created in the artifacts directory.
        On Failure  :   Write an exception log and then raise an exception.
        """
        logging.info(" Entered split_data_as_train_test method of DataIngestion class")

        try:
            # Perform train-test split
            train_set, test_set = train_test_split(
                dataframe,
                test_size=self.data_ingestion_config.train_test_split_ratio,
                random_state=42
            )
            logging.info(" Train-test split performed successfully.")

            # Create directories if not exist
            train_dir = os.path.dirname(self.data_ingestion_config.training_file_path)
            test_dir = os.path.dirname(self.data_ingestion_config.testing_file_path)
            os.makedirs(train_dir, exist_ok=True)
            os.makedirs(test_dir, exist_ok=True)

            # Save the split datasets
            logging.info(f" Saving train data to {self.data_ingestion_config.training_file_path}")
            train_set.to_csv(self.data_ingestion_config.training_file_path, index=False, header=True)

            logging.info(f" Saving test data to {self.data_ingestion_config.testing_file_path}")
            test_set.to_csv(self.data_ingestion_config.testing_file_path, index=False, header=True)

            logging.info(" Train and test datasets saved successfully.")
        except Exception as e:
            raise USvisaException(e, sys)


    def initiate_data_ingestion(self) -> DataIngestionArtifact:
        """
        Method Name :   initiate_data_ingestion
        Description :   This method initiates the data ingestion component of the training pipeline.

        Output      :   Train and test set paths are returned as artifacts.
        On Failure  :   Write an exception log and then raise an exception.
        """
        logging.info(" Entered initiate_data_ingestion method of DataIngestion class")

        try:
            # Step 1: Export data from MySQL to feature store
            dataframe = self.export_data_into_feature_store()
            logging.info(" Data successfully exported to feature store.")

            # Step 2: Perform train-test split
            self.split_data_as_train_test(dataframe)
            logging.info(" Train-test split completed.")

            # Step 3: Create artifact object
            data_ingestion_artifact = DataIngestionArtifact(
                feature_store_file_path=self.data_ingestion_config.feature_store_file_path,
                training_file_path=self.data_ingestion_config.training_file_path,
                testing_file_path=self.data_ingestion_config.testing_file_path,
                is_ingested=True,
                message="Data Ingestion completed successfully."
            )

            logging.info(f" Data Ingestion Artifact: {data_ingestion_artifact}")
            logging.info(" Exiting initiate_data_ingestion method of DataIngestion class")
            return data_ingestion_artifact

        except Exception as e:
            raise USvisaException(e, sys)
