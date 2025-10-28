import numpy as np
from sklearn.metrics import accuracy_score
from us_visa.utils.main_utils import load_object, load_numpy_array_data

# ---- Update timestamp to match your latest run ----
timestamp = "10_28_2025_10_56_41"

# Paths
model_path = f"artifacts/{timestamp}/model_trainer/trained_model/model.pkl"
test_data_path = f"artifacts/{timestamp}/data_transformation/transformed/test_transformed.csv"

# Load model and test data
model = load_object(model_path)
test_data = load_numpy_array_data(test_data_path)

# Split features and labels
X_test, y_test = test_data[:, :-1], test_data[:, -1]

# Predict
y_pred = model.trained_model_object.predict(X_test)

# Evaluate accuracy
accuracy = accuracy_score(y_test, y_pred)
print(f"Model accuracy on actual test data: {accuracy * 100:.2f}%")
