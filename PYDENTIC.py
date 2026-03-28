# problem -> same things we has to write in every function to validate the data and type of data is called data validation and type validation respectively. We can use try and except block to handle the exceptions that may arise during the execution of the code.
def insert_patient_data(name: str, age: int):  # type validation
    
    if type(name) == str and type(age) == int:
        if age < 0:  # data validation
            raise ValueError("Age cannot be negative.")
        else:  
            print(f"Patient Name: {name}, Age: {age}")
    else:
        raise TypeError("Invalid input type. Name should be a string and age should be an integer.")
    
# solve this problem using pydantic library which is used for data validation and settings management using python type annotations. It provides a way to define data models with type annotations and automatically validates the data against those models.

from typing import Annotated, Dict, List, Optional

from pydantic import AnyUrl, BaseModel, EmailStr, Field, ValidationError, computed_field, field_validator  , model_validator

class Patient(BaseModel):
    # define ideal schema , (type validation)
    name: Annotated[str, Field(min_length=1, max_length=100 , title="Name of the Patient" , description="give the name of the patient in less than 100 characters" , examples=["John Doe"] )]  # data validation, name should not be empty
    age: int = Field(gt=0, lt=120)  # data validation, age should be greater than 0 and less than 120
    email: EmailStr
    linkdin: AnyUrl
    weight: Annotated[float, Field(gt=0 , strict=True)] = None  # optional field with default value None
    marrided: Annotated[bool, Field(default=False)]  # optional field with default value False
    allergies: Optional[List[str]] = None  # optional field with default value None
    contact_details: Dict[str, str] = {}  # optional field with default value empty dictionary

    # field validator is used for only one field validation.
    # model validator is used for multiple field validation. we can use both of them together in the same model.
    # computed field is used to define a field that is computed based on other fields. it is not stored in the database but can be accessed like any other field.
    @field_validator('email' , mode='before')
    @classmethod
    def validate_email(cls, value):
        valid_domaiuns = ['gmail.com', 'yahoo.com', 'outlook.com']
        if not value.endswith(tuple(valid_domaiuns)):
            raise ValueError("Email must be a valid address.")
        return value
    
    @model_validator(mode='before')
    def validate_emergency_contact(cls, model):
        if model.age > 60 and 'emergency_contact' not in model.contact_details:
            raise ValueError("Emergency contact details are required for patients above 60 years old.")
        
    @computed_field  
    @property
    def calculate_bmi(self) -> Optional[float]:
        if self.weight is not None and self.age is not None:
            return self.weight / (self.age ** 2)  # just for demonstration, not actual BMI calculation
        return None

def insert_patient_data(patient: Patient):  # data validation
    print(f"Patient Name: {patient.name}, Age: {patient.age}, Weight: {patient.weight} , Married: {patient.marrided}, Allergies: {patient.allergies}, Contact Details: {patient.contact_details}")  

patient_data = {
    "name": "John Doe",
    "age": 30,
    "weight": 70.5, 
    "marrided"  : True,
    "allergies": ["pollen", "dust"],
    "contact_details": {"email": "dhyanidivyanshu27@gmail.com"}
}


patient1 = Patient(**patient_data)  # data validation

insert_patient_data(patient1)