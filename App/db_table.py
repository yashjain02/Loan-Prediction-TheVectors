from sqlalchemy import Integer, String,Float,Column,Date
from database import Base


class Loan_application(Base):
    __tablename__='loan_eligibility'
    Loan_ID= Column(String,primary_key=True)
    Gender=Column(String)
    Married=Column(String)
    Dependents=Column(String)
    Education=Column(String)
    Self_Employed=Column(String)
    ApplicantIncome=Column(Integer,default=0)
    CoapplicantIncome=Column(Integer)
    LoanAmount=Column(Float, default=0)
    Loan_Amount_Term=Column(Float, default=0)
    Credit_History=Column(Float, default=0)
    Property_Area=Column(String)
    loan_eligibile=Column(String)

    def __repr__(self):
        return f"loanID={self.Loan_ID}"