from fastapi import FastAPI, Form, Request, Depends
from fastapi.responses import HTMLResponse, RedirectResponse, JSONResponse, Response
from fastapi.templating import Jinja2Templates
from pymongo import MongoClient
from bson.objectid import ObjectId
from fastapi.staticfiles import StaticFiles

# Initialize FastAPI app
app = FastAPI()

# MongoDB setup
client = MongoClient("mongodb://localhost:27017")  # Replace with your MongoDB URI

# Database and collection for doctors
doctor_db = client["doctor_collection"]  
doctor_collection = doctor_db["doctor_collection"]

# Database and collection for patients (for login)
patient_db = client["patient_collection"]  
patient_collection = patient_db["patient_collection"]

# Database and collection for patient signup
patient_signup_db = client["patient_data"]  
patient_signup_collection = patient_signup_db["patient_data"]

# Templates setup (for rendering HTML pages)
templates = Jinja2Templates(directory="../templates")  # HTML templates directory

# Static files setup (for images, CSS, etc.)
app.mount("/static", StaticFiles(directory="C:/Users/ADMIN/Downloads/BCH FINAL/static"), name="static")

# Routes
@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    return templates.TemplateResponse("first.html", {"request": request})

@app.post("/doctor_login")
async def doctor_login(request: Request, doctor_id: str = Form(...), password: str = Form(...)):
    doctor = doctor_collection.find_one({"Doctor ID": doctor_id, "Password": password})
    if doctor:
        response.set_cookie(key="doctor_session", value=doctor_id, httponly=True, max_age=3600)
        response = RedirectResponse(url="/doctor_homepage") 
        return response 
    return templates.TemplateResponse("doctorlogin.html", {"request": request, "error": "Invalid Doctor ID or Password"})

@app.post("/patient_login")
async def patient_login(
    request: Request, 
    response: Response, 
    patient_name: str = Form(...), 
    password: str = Form(...)
):
    patient = patient_collection.find_one({"Patient Name": patient_name, "Password": password})

    if patient:
        # Set a cookie valid for 1 hour
        response.set_cookie(key="patient_session", value=patient_name, max_age=3600, httponly=True)
        response = RedirectResponse(url="/homepage")
        return response

    return templates.TemplateResponse("patientlogin.html", {"request": request, "error": "Invalid Patient Name or Password"})

@app.post("/patient_signup")
async def patient_signup(
    request: Request, 
    response: Response, 
    patient_name: str = Form(...), 
    age: str = Form(...), 
    phone_number: str = Form(...), 
    password: str = Form(...), 
    retype_password: str = Form(...)
):
    # Check if patient already exists
    patient = patient_collection.find_one({"Patient Name": patient_name})
    if patient:
        return templates.TemplateResponse("patientlogin.html", {"request": request, "error": "Patient already exists!"})

    # Ensure passwords match
    if password != retype_password:
        return templates.TemplateResponse("patientlogin.html", {"request": request, "error": "Passwords do not match!"})

    # Insert new patient into the database
    new_patient = {
        "Patient Name": patient_name,
        "Age": age,
        "Phone Number": phone_number,
        "Password": password
    }
    patient_collection.insert_one(new_patient)

    # Set a cookie for session (valid for 1 hour)
    response.set_cookie(key="patient_session", value=patient_name, max_age=3600, httponly=True)
    response = RedirectResponse(url="/patient_login")
    return response

@app.get("/doctor_login_get", response_class=HTMLResponse)
async def home(request: Request):
    return templates.TemplateResponse("doctorlogin.html", {"request": request})

@app.get("/patient_login_get", response_class=HTMLResponse)
async def home(request: Request):
    return templates.TemplateResponse("patientlogin.html", {"request": request})

@app.get("/patient_signup_get", response_class=HTMLResponse)
async def home(request: Request):
    return templates.TemplateResponse("patientsignup.html", {"request": request})

@app.get("/doctor_homepage", response_class=HTMLResponse)
async def home(request: Request):
    return templates.TemplateResponse("doctorhomepage.html", {"request": request})

@app.get("/homepage", response_class=HTMLResponse)
async def home(request: Request):
    return templates.TemplateResponse("homepage.html", {"request": request}) 

@app.get("/stepfirst", response_class=HTMLResponse)
async def home(request: Request):
    return templates.TemplateResponse("stepfirst.html", {"request": request}) 

@app.get("/stepsecond", response_class=HTMLResponse) 
async def home(request: Request):
    return templates.TemplateResponse("stepsecond.html", {"request": request}) 

@app.get("/stepthird", response_class=HTMLResponse)
async def home(request: Request):
    return templates.TemplateResponse("stepthird.html", {"request": request}) 

@app.get("/stepfourth", response_class=HTMLResponse)
async def home(request: Request):
    return templates.TemplateResponse("stepfourth.html", {"request": request}) 

@app.get("/stepfifth", response_class=HTMLResponse)
async def home(request: Request):
    return templates.TemplateResponse("stepfifth.html", {"request": request}) 

@app.get("/mamoimages", response_class=HTMLResponse)
async def home(request: Request):
    return templates.TemplateResponse("mamoimages.html", {"request": request}) 

@app.get("/result", response_class=HTMLResponse)
async def home(request: Request):
    return templates.TemplateResponse("result.html", {"request": request}) 

@app.get("/consultation", response_class=HTMLResponse)
async def home(request: Request):
    return templates.TemplateResponse("consultation.html", {"request": request}) 

db = client['form_information']  
form_collection = db['form_information']  

@app.post("/submit")
async def submit(
    request: Request,
    form_name: str = Form(...)
):
    form_data = await request.form()
    form_dict = {key: value for key, value in form_data.items()}

    # Save to MongoDB
    await form_collection.insert_one({
        'formType': form_name,
        'data': form_dict
    })