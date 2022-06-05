# from fastapi import FastAPI
from fastapi import Depends, FastAPI
from sqlalchemy import create_engine
import uvicorn
import pandas as pd
from Loan_apn import Loan_application
from pydantic import BaseModel
import joblib
import preprocessing as p
import database
from inference import make_prediction
# import db_table
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session
from sqlalchemy import Column, Integer, String, Float


app = FastAPI(title='Loan Prediction', version='1.0', description='fastapi for loan pred')

db = database.Session()

# creating the database
db_host = "localhost"
db_name = "postgres"
db_pass = "4895"
db_user = "postgres"
my_database_connection = f"postgresql://{db_user}:{db_pass}@{db_host}/{db_name}"

engine = create_engine(my_database_connection)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()


class testAPIModel(Base):
    __tablename__ = "testingthis"
    id = Column(Integer, primary_key=True)
    email = Column(String(256))


class testingSchema(Base):
    __tablename__ = "newtestingthis"
    id = Column(Integer, primary_key=True)
    email = Column(String(256))


class LoanApplication(Base):
    __tablename__ = "loan_eligibility"
    Loan_ID = Column(String, primary_key=True)
    Gender = Column(String)
    Married = Column(String)
    Dependents = Column(String)
    Education = Column(String)
    Self_Employed = Column(String)
    ApplicantIncome = Column(Integer, default=0)
    CoapplicantIncome = Column(Integer)
    LoanAmount = Column(Float, default=0)
    Loan_Amount_Term = Column(Float, default=0)
    Credit_History = Column(Float, default=0)
    Property_Area = Column(String)
    loan_eligibile = Column(String)


class loanSchema(BaseModel):
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


Base.metadata.create_all(bind=engine)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.get("/testing_api")
def read_users(db: Session = Depends(get_db)):
    print("read_users")
    users = db.query(testAPIModel).all()
    print(users)
    return users
    # return users


@app.get('/')
async def root():
    print("read_users")
    return {"message": "called"}


@app.post('/fileType')
def predict(myfiles):
    myfiles = myfiles[3:]
    df = pd.read_csv(myfiles)
    a = make_prediction(df)
    strings = ' '.join(str(i) for i in a)
    return strings


@app.post('/individualEntry')
def predict_individual(data: Loan_application):
    data_dict = data.dict()
    data_df = pd.DataFrame.from_dict([data_dict])
    pred = make_prediction(data_df)
    add_database(data, pred)
    return {'predict': pred[0]}


def add_database(data, pred):
    db_item = LoanApplication(**data.dict(), loan_eligibile=pred[0])
    db.add(db_item)
    db.commit()
    db.refresh(db_item)


if __name__ == '__main__':
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)
