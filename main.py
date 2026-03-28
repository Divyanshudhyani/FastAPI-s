from fastapi import FastAPI, HTTPException, Path, Query
from fastapi.responses import JSONResponse
from pydantic import computed_field, Field, BaseModel
from typing import Annotated, Literal  # Fixed import
import json

app = FastAPI()

class Patient(BaseModel):
    id: Annotated[str, Field(
        ..., 
        description="The unique identifier for the patient", 
        pattern=r"^P\d{3}$",  # Added pattern for validation
        examples=["P001"]
    )]
    name: Annotated[str, Field(
        ...,  # Fixed: removed 'str' argument
        min_length=1, 
        max_length=100, 
        title="Name of the Patient", 
        description="give the name of the patient in less than 100 characters", 
        examples=["John Doe"]
    )]
    city: Annotated[str, Field(
        ...,  # Fixed: removed 'str' argument
        min_length=1, 
        max_length=100, 
        title="City of the Patient", 
        description="give the city of the patient in less than 100 characters", 
        examples=["New York"]
    )]
    age: Annotated[int, Field(
        ..., 
        gt=0, 
        lt=120, 
        title="Age of the Patient", 
        description="give the age of the patient between 1 and 120", 
        examples=[30]
    )]
    gender: Annotated[Literal['Male', 'Female'], Field(
        ..., 
        title="Gender of the Patient", 
        description="give the gender of the patient"
    )]
    height: Annotated[float, Field(
        ..., 
        gt=0, 
        title="Height of the Patient", 
        description="give the height of the patient in centimeters", 
        examples=[175.5]
    )]
    weight: Annotated[float, Field(
        ..., 
        gt=0, 
        title="Weight of the Patient", 
        description="give the weight of the patient in kilograms", 
        examples=[70.5]
    )]
    
    @computed_field
    @property
    def bmi(self) -> float:
        return round(self.weight / ((self.height / 100) ** 2), 2)
    
    @computed_field
    @property
    def health_status(self) -> str:
        bmi = self.bmi
        if bmi < 18.5:
            return "Underweight"
        elif 18.5 <= bmi < 25:
            return "Normal weight"
        elif 25 <= bmi < 30:
            return "Overweight"
        else:
            return "Obese"

def load_data():
    with open('patients.json', 'r') as f:
        data = json.load(f)
    return data

@app.get("/")
def hello():
    return {"message": "Patient Management System API"}

@app.get("/about")
def about():
    return {"message": "This is a fully functional API to manage your patient records."}

@app.get("/view")
def view():
    data = load_data()
    return data

@app.get("/view/{patient_id}")
def view_patient(
    patient_id: str = Path(
        ..., 
        description="The ID of the patient to retrieve", 
        examples=["P001"]
    )
):
    data = load_data()
    if patient_id in data:
        return data[patient_id]
    raise HTTPException(status_code=404, detail="Patient not found")

@app.get('/sort')
def sort_patients(
    sort_by: Literal['height', 'weight', 'bmi'] = Query(
        ..., 
        description="The field to sort by"
    ),
    order: Literal['asc', 'desc'] = Query(
        'asc', 
        description="The sort order: 'asc' for ascending, 'desc' for descending"
    )
):
    data = load_data()
    reverse = order == 'desc'
    sorted_data = sorted(
        data.values(), 
        key=lambda x: x.get(sort_by, 0), 
        reverse=reverse
    )
    return sorted_data

@app.post("/create", status_code=201)
def create_patient(patient: Patient):
    data = load_data()
    if patient.id in data:
        raise HTTPException(status_code=400, detail="Patient already exists")
    
    # Save patient data (keep id in the stored data)
    data[patient.id] = patient.model_dump()
    
    with open('patients.json', 'w') as f:
        json.dump(data, f, indent=2)  # Added indent for readability
    
    return JSONResponse(
        content={
            "message": "Patient created successfully", 
            "patient_id": patient.id
        }
    )

# Optional: Add a GET endpoint to retrieve all patients with computed fields
@app.get("/patients")
def get_all_patients():
    """Get all patients with BMI and health status"""
    data = load_data()
    return data