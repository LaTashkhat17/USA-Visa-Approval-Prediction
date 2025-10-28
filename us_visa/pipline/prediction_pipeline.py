import os
import sys
import pandas as pd
from pandas import DataFrame
from us_visa.exception import USvisaException
from us_visa.logger import logging
from us_visa.utils.main_utils import load_object
from us_visa.constants import GOOGLE_DRIVE_MODEL_PATH


class USvisaData:
    def __init__(
        self,
        continent,
        education_of_employee,
        has_job_experience,
        requires_job_training,
        no_of_employees,
        region_of_employment,
        prevailing_wage,
        unit_of_wage,
        full_time_position,
        company_age
    ):
        """
        Class for structuring input data for US Visa Prediction
        """
        try:
            self.continent = continent
            self.education_of_employee = education_of_employee
            self.has_job_experience = has_job_experience
            self.requires_job_training = requires_job_training
            self.no_of_employees = no_of_employees
            self.region_of_employment = region_of_employment
            self.prevailing_wage = prevailing_wage
            self.unit_of_wage = unit_of_wage
            self.full_time_position = full_time_position
            self.company_age = company_age

        except Exception as e:
            raise USvisaException(e, sys)

    def get_usvisa_data_as_dict(self):
        """Returns user inputs as dictionary"""
        try:
            input_data = {
                "continent": [self.continent],
                "education_of_employee": [self.education_of_employee],
                "has_job_experience": [self.has_job_experience],
                "requires_job_training": [self.requires_job_training],
                "no_of_employees": [self.no_of_employees],
                "region_of_employment": [self.region_of_employment],
                "prevailing_wage": [self.prevailing_wage],
                "unit_of_wage": [self.unit_of_wage],
                "full_time_position": [self.full_time_position],
                "company_age": [self.company_age],
            }
            logging.info(" Created US Visa input dictionary successfully.")
            return input_data
        except Exception as e:
            raise USvisaException(e, sys)

    def get_usvisa_input_data_frame(self) -> DataFrame:
        """Converts input data into a pandas DataFrame"""
        try:
            df = DataFrame(self.get_usvisa_data_as_dict())
            logging.info(" Converted US Visa input dictionary into DataFrame.")
            return df
        except Exception as e:
            raise USvisaException(e, sys)


# =====================================================================
# MODEL CLASSIFIER USING GOOGLE DRIVE-STORED MODEL
# =====================================================================
class USvisaClassifier:
    def __init__(self, local_model_path: str = "saved_models/model.pkl") -> None:
        """
        Loads model from local or Google Drive location.
        The model is automatically downloaded if not available locally.
        """
        try:
            self.local_model_path = local_model_path

            # If model not available locally, try to download from Google Drive
            if not os.path.exists(self.local_model_path):
                logging.info("Local model not found. Attempting to download from Google Drive...")

                from pydrive.auth import GoogleAuth
                from pydrive.drive import GoogleDrive

                gauth = GoogleAuth()
                gauth.LocalWebserverAuth()
                drive = GoogleDrive(gauth)

                # ✅ Extract the file ID from your shared link in constants
                if "id=" in GOOGLE_DRIVE_MODEL_PATH:
                    file_id = GOOGLE_DRIVE_MODEL_PATH.split("id=")[-1]
                elif "/d/" in GOOGLE_DRIVE_MODEL_PATH:
                    file_id = GOOGLE_DRIVE_MODEL_PATH.split("/d/")[1].split("/")[0]
                else:
                    raise ValueError(f"Invalid Google Drive URL: {GOOGLE_DRIVE_MODEL_PATH}")

                file = drive.CreateFile({'id': file_id})
                file.GetContentFile(self.local_model_path)
                logging.info(" Model downloaded successfully from Google Drive.")

            # ✅ Load model into memory
            self.model = load_object(self.local_model_path)
            logging.info(" Model loaded successfully and ready for prediction.")

        except Exception as e:
            raise USvisaException(e, sys)

    def predict(self, dataframe: pd.DataFrame):
        """
        Perform prediction using the loaded model.
        The model is assumed to be a trained sklearn-compatible model.
        """
        try:
            logging.info("Starting prediction process using loaded model.")

            # Make predictions
            preds = self.model.predict(dataframe)

            # Map numerical results to readable labels
            mapping = {1: "Visa Approved", 0: "Visa Not Approved"}
            results = [mapping.get(int(p), "Unknown") for p in preds]

            logging.info(f"Predictions completed successfully: {results}")
            return results

        except Exception as e:
            raise USvisaException(e, sys)
