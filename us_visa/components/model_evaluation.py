import os, sys
import yaml
from us_visa.logger import logging
from us_visa.exception import USvisaException
from us_visa.utils.main_utils import load_object, write_yaml_file
from us_visa.entity.config_entity import ModelEvaluationConfig
from us_visa.entity.artifact_entity import (
    ModelTrainerArtifact,
    ModelEvaluationArtifact
)
from sklearn.metrics import accuracy_score


class ModelEvaluation:
    def __init__(self, model_trainer_artifact: ModelTrainerArtifact,
                 model_evaluation_config: ModelEvaluationConfig):
        self.model_trainer_artifact = model_trainer_artifact
        self.model_evaluation_config = model_evaluation_config

    def initiate_model_evaluation(self) -> ModelEvaluationArtifact:
        try:
            logging.info("Starting Model Evaluation process...")

            trained_model_path = self.model_trainer_artifact.trained_model_file_path

            # Check if old model exists in Google Drive or locally
            best_model_path = "saved_models/best_model.pkl"
            is_model_accepted = True
            improved_accuracy = 0.0

            if os.path.exists(best_model_path):
                logging.info("Found an existing model. Comparing performance...")

                old_model = load_object(best_model_path)
                new_model = load_object(trained_model_path)

                # Dummy evaluation logic (replace with test set comparison)
                old_acc = 0.79  # previously saved
                new_acc = self.model_trainer_artifact.training_metric_artifact.accuracy_score

                improved_accuracy = new_acc - old_acc
                is_model_accepted = improved_accuracy > self.model_evaluation_config.threshold
            else:
                logging.info("No existing model found. Accepting current model as best.")
                is_model_accepted = True

            # Save report
            report = {
                "best_model_path": best_model_path,
                "trained_model_path": trained_model_path,
                "is_model_accepted": is_model_accepted,
                "improved_accuracy": improved_accuracy
            }

            os.makedirs(os.path.dirname(self.model_evaluation_config.report_file_path), exist_ok=True)
            with open(self.model_evaluation_config.report_file_path, "w") as f:
                yaml.dump(report, f)

            logging.info(f"Model Evaluation Report saved at {self.model_evaluation_config.report_file_path}")

            return ModelEvaluationArtifact(
                is_model_accepted=is_model_accepted,
                improved_accuracy=improved_accuracy,
                best_model_path=best_model_path,
                trained_model_path=trained_model_path,
                message="Model Evaluation completed successfully."
            )

        except Exception as e:
            raise USvisaException(e, sys)
            logging.info("Model Evaluation process completed.")