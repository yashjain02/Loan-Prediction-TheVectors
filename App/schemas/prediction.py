from pydantic import BaseModel

# to validate data,used BasedModel
class LoanSchema(BaseModel):
    Loan_ID: str
    Gender: str
    Married: str
    Dependents: str
    Education: str
    Self_Employed: str
    ApplicantIncome: int
    CoapplicantIncome: int
    LoanAmount: float
    Loan_Amount_Term: float
    Credit_History: float
    Property_Area: str
#the configuration class for the model
    class Config:
        env_file = "../.env"
        orm_mode = True


class RetrieveSchema(BaseModel):
    Loan_ID: str

    class Config:
        env_file = "../.env"
        orm_mode = True


class FileSchema(BaseModel):
    file_data: str

    class Config:
        env_file = "../.env"
        orm_mode = True

class RetrievedDataSchema(BaseModel):
    Loan_ID: str
    Gender: str
    Married: str
    Dependents: str
    Education: str
    Self_Employed: str
    ApplicantIncome: int
    CoapplicantIncome: int
    LoanAmount: float
    Loan_Amount_Term: float
    Credit_History: float
    Property_Area: str
    loan_eligibile: str

    class Config:
        env_file = "../.env"
        orm_mode = True