import os, sys
from pydrive.auth import GoogleAuth
from pydrive.drive import GoogleDrive
from us_visa.logger import logging
from us_visa.exception import USvisaException
from us_visa.entity.config_entity import ModelPusherConfig
from us_visa.entity.artifact_entity import ModelEvaluationArtifact, ModelPusherArtifact


class ModelPusher:
    """ 
    Class to handle pushing the trained model to Google Drive.
    """

    def __init__(self, model_pusher_config: ModelPusherConfig,
                 model_evaluation_artifact: ModelEvaluationArtifact):
        self.model_pusher_config = model_pusher_config
        self.model_evaluation_artifact = model_evaluation_artifact

    def upload_to_drive(self, local_file_path: str, folder_name: str = "US_Visa_Models"):
        """
        Uploads the model to Google Drive and makes it publicly accessible.
        """
        try:
            logging.info("Authenticating with Google Drive...")
            gauth = GoogleAuth()
            gauth.LocalWebserverAuth()
            drive = GoogleDrive(gauth)

            # Create or find target folder
            folder_list = drive.ListFile(
                {'q': f"title='{folder_name}' and mimeType='application/vnd.google-apps.folder' and trashed=false"}
            ).GetList()

            if folder_list:
                folder_id = folder_list[0]['id']
                logging.info(f"Found existing Google Drive folder: {folder_name}")
            else:
                folder_metadata = {'title': folder_name, 'mimeType': 'application/vnd.google-apps.folder'}
                folder = drive.CreateFile(folder_metadata)
                folder.Upload()
                folder_id = folder['id']
                logging.info(f"Created new Google Drive folder: {folder_name}")

            # Upload file
            file = drive.CreateFile({'title': os.path.basename(local_file_path), 'parents': [{'id': folder_id}]})
            file.SetContentFile(local_file_path)
            file.Upload()

            # Set file permissions to public (anyone with link can view)
            file.InsertPermission({
                'type': 'anyone',
                'value': 'anyone',
                'role': 'reader'
            })

            shareable_link = f"https://drive.google.com/uc?id={file['id']}"
            logging.info(f"✅ Model uploaded successfully to Google Drive: {shareable_link}")

            return shareable_link

        except Exception as e:
            raise USvisaException(e, sys)

    def initiate_model_pusher(self) -> ModelPusherArtifact:
        """
        Initiates the model pushing process to Google Drive.
        """
        try:
            logging.info("Initiating Model Pusher...")

            if not self.model_evaluation_artifact.is_model_accepted:
                logging.info("Model was not accepted; skipping upload to Google Drive.")
                return ModelPusherArtifact(
                    pushed_model_google_drive_url="",
                    message="Model not accepted, skipping upload."
                )

            model_path = self.model_evaluation_artifact.trained_model_path
            drive_url = self.upload_to_drive(model_path)

            return ModelPusherArtifact(
                pushed_model_google_drive_url=drive_url,
                message="Model uploaded to Google Drive successfully (public link generated)."
            )

        except Exception as e:
            raise USvisaException(e, sys)
