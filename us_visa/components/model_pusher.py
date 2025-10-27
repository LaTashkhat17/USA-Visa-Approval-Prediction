import os, sys
from pydrive2.auth import GoogleAuth
from pydrive2.drive import GoogleDrive  # use pydrive2 (better maintained)
from us_visa.logger import logging
from us_visa.exception import USvisaException
from us_visa.entity.config_entity import ModelPusherConfig
from us_visa.entity.artifact_entity import ModelEvaluationArtifact, ModelPusherArtifact


class ModelPusher:
    """
    Handles uploading the best trained model to Google Drive.
    Creates folder automatically if it doesn’t exist and reuses existing credentials.
    """

    def __init__(self, model_pusher_config: ModelPusherConfig,
                 model_evaluation_artifact: ModelEvaluationArtifact):
        self.model_pusher_config = model_pusher_config
        self.model_evaluation_artifact = model_evaluation_artifact

    # ------------------------------------------------------------------
    # AUTHENTICATION HANDLER
    # ------------------------------------------------------------------
    def authenticate_drive(self) -> GoogleDrive:
        try:
            logging.info("Authenticating with Google Drive...")

            # Check if client_secrets.json exists
            client_secret_path = os.path.join(os.getcwd(), "client_secrets.json")
            if not os.path.exists(client_secret_path):
                raise FileNotFoundError(
                    f"Missing Google OAuth client secrets file: {client_secret_path}\n"
                    f"Please download it from Google Cloud Console and place it in your project root."
                )

            # Setup GoogleAuth
            gauth = GoogleAuth()
            gauth.LoadClientConfigFile(client_secret_path)

            # Try to load saved credentials
            cred_path = os.path.join(os.getcwd(), "credentials.json")
            if os.path.exists(cred_path):
                gauth.LoadCredentialsFile(cred_path)
                if gauth.access_token_expired:
                    gauth.Refresh()
                else:
                    gauth.Authorize()
            else:
                # First-time login; will open a browser for OAuth
                gauth.LocalWebserverAuth()
                gauth.SaveCredentialsFile(cred_path)

            logging.info("Google Drive authentication successful.")
            return GoogleDrive(gauth)

        except Exception as e:
            raise USvisaException(e, sys)

    # ------------------------------------------------------------------
    # UPLOAD TO GOOGLE DRIVE
    # ------------------------------------------------------------------
    def upload_to_drive(self, local_file_path: str, folder_name: str = "ML_Models") -> str:
        """
        Uploads a given file to Google Drive inside the specified folder.
        Creates folder automatically if not present.
        Returns the public URL of the uploaded model.
        """
        try:
            drive = self.authenticate_drive()

            # Search or create folder
            folder_list = drive.ListFile(
                {'q': f"title='{folder_name}' and mimeType='application/vnd.google-apps.folder' and trashed=false"}
            ).GetList()

            if folder_list:
                folder_id = folder_list[0]['id']
                logging.info(f"Found existing folder in Google Drive: {folder_name}")
            else:
                folder_metadata = {'title': folder_name, 'mimeType': 'application/vnd.google-apps.folder'}
                folder = drive.CreateFile(folder_metadata)
                folder.Upload()
                folder_id = folder['id']
                logging.info(f"Created new folder in Google Drive: {folder_name}")

            # Upload model file
            file_metadata = {'title': os.path.basename(local_file_path), 'parents': [{'id': folder_id}]}
            file = drive.CreateFile(file_metadata)
            file.SetContentFile(local_file_path)
            file.Upload()

            file_url = f"https://drive.google.com/uc?id={file['id']}"
            logging.info(f"Model uploaded successfully to Google Drive: {file_url}")

            return file_url

        except Exception as e:
            raise USvisaException(e, sys)

    # ------------------------------------------------------------------
    # INITIATE MODEL PUSHER
    # ------------------------------------------------------------------
    def initiate_model_pusher(self) -> ModelPusherArtifact:
        """
        Uploads the trained model to Google Drive if it was accepted in evaluation.
        """
        try:
            logging.info("Initiating Model Pusher...")

            if not self.model_evaluation_artifact.is_model_accepted:
                logging.info("Model rejected. Skipping Google Drive upload.")
                return ModelPusherArtifact(
                    pushed_model_google_drive_url="",
                    message="Model was not accepted; upload skipped."
                )

            model_path = self.model_evaluation_artifact.trained_model_path
            drive_url = self.upload_to_drive(local_file_path=model_path, folder_name="US_Visa_Models")

            return ModelPusherArtifact(
                pushed_model_google_drive_url=drive_url,
                message="Model uploaded successfully to Google Drive."
            )

        except Exception as e:
            raise USvisaException(e, sys)
