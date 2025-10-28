
US Visa Approval Prediction Web App 🇺🇸

An end-to-end Machine Learning Project that predicts whether a US visa application will be approved or denied, based on applicant and employer details.
Built using FastAPI, Scikit-learn, and integrated with Google Drive for model management.

🚀 Project Overview

This project automates the process of predicting visa approval outcomes using historical US visa data.
It covers the complete MLOps lifecycle — from data ingestion to model deployment via a web interface.

✅ Key Features:

Automatic data validation, transformation, training, and evaluation pipeline

Model trained and uploaded to Google Drive automatically

Web-based FastAPI app for real-time predictions

Reusable pipeline for retraining and model updates

Google Drive integration for model storage and versioning

🧩 Tech Stack
Layer	Tools / Libraries
Frontend	HTML, CSS, Bootstrap
Backend	FastAPI, Uvicorn
ML / Data	Scikit-learn, Pandas, NumPy, PyDrive
Logging & Configs	Python Logging, YAML
Storage	Google Drive (for trained model uploads/downloads)
📂 Project Structure
USA-Visa-Approval-Prediction/
│
├── app.py                         # FastAPI web app entry point
├── templates/
│   └── index.html                 # Frontend HTML form for user input
├── static/
│   └── style.css                  # Styling for frontend
│
├── us_visa/
│   ├── pipline/
│   │   ├── training_pipeline.py   # Handles full ML training pipeline
│   │   ├── prediction_pipeline.py # Google Drive model loading & prediction
│   │
│   ├── components/                # Data ingestion, validation, transformation, trainer, etc.
│   ├── entity/                    # Data and artifact classes
│   ├── logger/                    # Central logging setup
│   ├── utils/                     # Helper functions (save/load objects, YAML, etc.)
│   └── exception.py               # Custom exception handling
│
├── artifacts/                     # Stores pipeline outputs (CSV, model, etc.)
├── saved_models/                  # Local model cache (downloaded from Drive)
├── config/
│   ├── schema.yaml                # Defines feature schema
│   ├── model.yaml                 # Model configuration
│
├── client_secrets.json            # Google OAuth credentials (⚠️ ignored via .gitignore)
├── credentials.json               # Generated after OAuth authentication
│
├── requirements.txt               # Python dependencies
├── README.md                      # Project documentation (this file)
└── .gitignore                     # Ignored files list

⚙️ How It Works
🏗️ 1. Training Pipeline

Run end-to-end model training using:

Anaconda: https://www.anaconda.com/
Vs code: https://code.visualstudio.com/download
Git: https://git-scm.com/

For flowchart
https://whimsical.com/a

Data link:
Kaggle: https://www.kaggle.com/datasets/moro23/easyvisa-dataset

Workflow
constant
config_entity
artifact_entity
conponent

pipeline
app.py / demo.py


How to run?
git clone https://github.com/LaTashkhat17/USA-Visa-Approval-Prediction

conda create -n visa python=3.8 -y
conda activate visa
pip install -r requirements.txt

Then visit:

http://localhost:8080/train


This will:

Ingest and validate the dataset

Transform features (encoding, scaling, etc.)

Train an ML model (classification)

Evaluate it

Upload the trained model to Google Drive

🔮 2. Prediction via Web App

Start the app:

uvicorn app:app --reload


Then open:

http://127.0.0.1:8000/


You’ll see a form like this 👇
Enter visa application details and click Predict Visa Status — the model will:

Download the trained model from Google Drive (if not cached)

Preprocess your inputs

Predict whether the visa will be approved or not approved

🧠 Example Prediction
Feature	Example Input
Continent	Asia
Education of Employee	Master’s
Has Job Experience	Y
Requires Job Training	N
Number of Employees	12000
Region of Employment	West
Prevailing Wage	69370.58
Unit of Wage	Year
Full Time Position	Y
Company Age	115

✅ Output: Visa Approved

☁️ Google Drive Integration

This project uses PyDrive for automatic model uploads/downloads.

🔑 Setup Steps

Create a project in Google Cloud Console
.

Enable the Google Drive API.

Download your client_secrets.json and place it in your project root.

The first time you run the app, a browser window will open for Google login authorization.

The model will then be saved under your Drive folder.

🧾 Requirements

Install dependencies:

pip install -r requirements.txt


Key libraries:

fastapi
uvicorn
pandas
numpy
scikit-learn
PyDrive
imblearn
jinja2
python-dotenv

🛠️ Local Development

Start local FastAPI server:

uvicorn app:app --reload


Re-train model:

python app.py
# Visit http://localhost:8080/train

🧑‍💻 Author

Omar Rashid
🎓 Department of Information and Communication Engineering,
Noakhali Science and Technology University

📧 Email: omarrashid852@gmail.com

💼 GitHub: @LaTashkhat17
