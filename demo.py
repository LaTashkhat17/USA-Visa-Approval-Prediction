from us_visa.pipline.training_pipeline import TrainingPipeline
from us_visa.logger import logging

if __name__ == "__main__":
    try:
        logging.info("Starting US Visa Approval Prediction Pipeline...")
        pipeline = TrainingPipeline()
        pipeline.run_pipeline()
    except Exception as e:
        logging.error(f"Pipeline execution failed: {e}")
        print(f"Pipeline execution failed: {e}")
