from fastapi import FastAPI
from fastapi.responses import JSONResponse
from pydantic import computed_field, Field, BaseModel
from typing import Annotated
import pandas as pd
import joblib

app = FastAPI()

def age_group(age):
    if age < 30:
        return 'young'  
    elif age < 50:
        return 'middle-aged'
    elif age < 70:
        return 'senior'
    else:
        return 'elderly'

def calculate_lifestyle_risk(smoker, bmi, age):
    risk = 0
    if smoker:
        risk += 3
    if bmi > 30:
        risk += 2
    elif bmi > 25:
        risk += 1
    if age > 60:
        risk += 2
    elif age > 50:
        risk += 1
    return risk

def city_tier(city):
    tier_1 = ["Mumbai", "Delhi", "Bangalore", "Chennai", "Kolkata", "Hyderabad", "Pune"]
    tier_2 = ["Jaipur", "Lucknow", "Indore", "Nagpur", "Ahmedabad"]
    if city in tier_1:
        return 1
    elif city in tier_2:
        return 2
    else:
        return 3

def bmi_category(bmi):
    if bmi < 18.5:
        return 'underweight'
    elif bmi < 25:
        return 'normal'
    elif bmi < 30:
        return 'overweight'
    else:
        return 'obese'

class PatientInput(BaseModel):
    age: Annotated[int, Field(gt=0, lt=120)]
    weight: Annotated[float, Field(gt=0)]
    height: Annotated[float, Field(gt=0)]
    income_lpa: Annotated[float, Field(gt=0)]
    smoker: Annotated[bool, Field()]
    city: Annotated[str, Field()]
    occupation: Annotated[str, Field()]
    
    @computed_field
    @property
    def bmi(self) -> float:
        return self.weight / (self.height ** 2)
    
    @computed_field
    @property
    def age_group(self) -> str:
        return age_group(self.age)
    
    @computed_field
    @property
    def lifestyle_risk(self) -> int:
        return calculate_lifestyle_risk(self.smoker, self.bmi, self.age)
    
    @computed_field
    @property
    def city_tier(self) -> int:
        return city_tier(self.city)
    
    @computed_field
    @property
    def bmi_category(self) -> str:
        return bmi_category(self.bmi)

model = joblib.load('model.pkl')

@app.post("/predict")
def predict_insurance_cost(patient: PatientInput):
    input_df = pd.DataFrame([{
        "bmi": patient.bmi,
        "age_group": patient.age_group,
        "lifestyle_risk": patient.lifestyle_risk,
        "city_tier": patient.city_tier,
        "income_lpa": patient.income_lpa,
        "occupation": patient.occupation,
        "bmi_category": patient.bmi_category    
    }])
    
    predict_result = model.predict(input_df)[0]
    return JSONResponse(content={"predicted_insurance_cost": predict_result})