import pandas as pd
from us_visa.pipline.prediction_pipeline import PredictionPipeline

# --- Update timestamp to your latest run ---
timestamp = "10_28_2025_10_56_41"

model_path = f"artifacts/{timestamp}/model_trainer/trained_model/model.pkl"
preprocessor_path = f"artifacts/{timestamp}/data_transformation/preprocessing/preprocessor.pkl"

# Initialize the prediction pipeline
pipeline = PredictionPipeline(model_path=model_path, preprocessor_path=preprocessor_path)

# Example input data (must match your training schema)
input_dict = {
    "continent": ["Asia"],
    "education_of_employee": ["Bachelor's"],
    "has_job_experience": ["Y"],
    "requires_job_training": ["N"],
    "no_of_employees": [3481],
    "region_of_employment": ["South"],
    "prevailing_wage": [99957.16],
    "unit_of_wage": ["Year"],
    "full_time_position": ["Y"],
    "company_age": [46] 
}

input_df = pd.DataFrame(input_dict)

# Run prediction
prediction = pipeline.predict(input_df)
print("Prediction Result:", prediction)
