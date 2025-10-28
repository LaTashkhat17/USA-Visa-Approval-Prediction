from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse, Response
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from starlette.templating import Jinja2Templates
from uvicorn import run as app_run
import pandas as pd
from typing import Optional

# Internal imports
from us_visa.constants import APP_HOST, APP_PORT
from us_visa.pipline.prediction_pipeline import USvisaData, USvisaClassifier
from us_visa.pipline.training_pipeline import TrainingPipeline


# =========================================================
# APP CONFIGURATION
# =========================================================
app = FastAPI(title="US Visa Approval Prediction", version="1.0")

# Static and Template setup
app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")

# Enable CORS for all origins
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# =========================================================
# FORM DATA HANDLER
# =========================================================
class DataForm:
    def __init__(self, request: Request):
        self.request = request
        self.continent: Optional[str] = None
        self.education_of_employee: Optional[str] = None
        self.has_job_experience: Optional[str] = None
        self.requires_job_training: Optional[str] = None
        self.no_of_employees: Optional[int] = None
        self.region_of_employment: Optional[str] = None
        self.prevailing_wage: Optional[float] = None
        self.unit_of_wage: Optional[str] = None
        self.full_time_position: Optional[str] = None
        self.company_age: Optional[int] = None

    async def get_usvisa_data(self):
        form = await self.request.form()
        self.continent = form.get("continent")
        self.education_of_employee = form.get("education_of_employee")
        self.has_job_experience = form.get("has_job_experience")
        self.requires_job_training = form.get("requires_job_training")
        self.no_of_employees = int(form.get("no_of_employees"))
        self.region_of_employment = form.get("region_of_employment")
        self.prevailing_wage = float(form.get("prevailing_wage"))
        self.unit_of_wage = form.get("unit_of_wage")
        self.full_time_position = form.get("full_time_position")
        self.company_age = int(form.get("company_age"))


# =========================================================
# ROUTES
# =========================================================

@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    """Render the homepage."""
    return templates.TemplateResponse("index.html", {"request": request, "context": None})


@app.get("/train")
async def train_model():
    """Trigger model training."""
    try:
        training_pipeline = TrainingPipeline()
        training_pipeline.run_pipeline()
        return Response("Model training completed successfully!")
    except Exception as e:
        return Response(f"Error during training: {e}")



@app.post("/", response_class=HTMLResponse)
async def predict(request: Request):
    """Handles visa prediction requests"""
    try:
        form = DataForm(request)
        await form.get_usvisa_data()

        # Create input DataFrame
        input_df = pd.DataFrame([{
            "continent": form.continent,
            "education_of_employee": form.education_of_employee,
            "has_job_experience": form.has_job_experience,
            "requires_job_training": form.requires_job_training,
            "no_of_employees": form.no_of_employees,
            "region_of_employment": form.region_of_employment,
            "prevailing_wage": form.prevailing_wage,
            "unit_of_wage": form.unit_of_wage,
            "full_time_position": form.full_time_position,
            "company_age": form.company_age
        }])

        # ✅ Use USvisaClassifier for predictions
        from us_visa.pipline.prediction_pipeline import USvisaClassifier
        classifier = USvisaClassifier()
        prediction = classifier.predict(input_df)[0]

        # Format result
        if prediction in ["Certified", "Visa Approved"]:
            status = " Visa Approved"
        elif prediction in ["Denied", "Visa Not Approved"]:
            status = " Visa Not Approved"
        else:
            status = f" Unknown result: {prediction}"

        return templates.TemplateResponse("index.html", {"request": request, "context": status})

    except Exception as e:
        return templates.TemplateResponse("index.html", {"request": request, "context": f"⚠️ Error: {e}"})

# =========================================================
# RUN APP
# =========================================================
if __name__ == "__main__":
    app_run(app, host=APP_HOST, port=APP_PORT)
