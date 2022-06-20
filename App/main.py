from fastapi import FastAPI, Depends, HTTPException, UploadFile, File
import uvicorn
import pandas as pd
from schemas import LoanSchema, RetrievedDataSchema,FileSchema
import json
from db import SessionLocal
from inference import make_prediction
from prediction_model import LoanApplication
from sqlalchemy.orm import Session
from io import BytesIO

app = FastAPI(title='Loan Prediction', version='1.0', description='fastapi for loan prediction')
db = SessionLocal()


def get_db():
    dbsession = SessionLocal()
    try:
        yield dbsession
    finally:
        dbsession.close()

# returning user prediction
#wil return user predictions from the database
@app.get('/retrieve_prediction/{loan_id}', response_model=RetrievedDataSchema)
async def get_prediction(loan_id: str, database: Session = Depends(get_db)):
    user_prediction = database.query(LoanApplication).filter(LoanApplication.Loan_ID == loan_id).first()
    if user_prediction is None:
        raise HTTPException(status_code=404, detail="User not found")
    return user_prediction

# returning all records
@app.get("/get_all")
def show_records(database: Session = Depends(get_db)):
    records = database.query(LoanApplication).all()
    if records is None:
        raise HTTPException(status_code=404, detail="No Records Found")
    return records




@app.post('/fileType')
async def predict(file: FileSchema):
    file_dict = file.dict()
    data_to_list = json.loads(file_dict['file_data'])
    resultArray = []
    # iteration inside files

    for x in data_to_list:
        data_dict = x
        data_df = pd.DataFrame.from_dict([data_dict])
        prediction = make_prediction(data_df)
        resultDict = {**x, "loan_eligibile": prediction[0]}
        resultArray.append(resultDict)
        db_item = LoanApplication(**x, loan_eligibile=prediction[0])
        db.add(db_item)
        db.commit()
        #db.refresh(db_item)

    return json.dumps(resultArray)



@app.post('/individualEntry')
def predict_individual(data: LoanSchema):
    data_dict = data.dict()
    data_df = pd.DataFrame.from_dict([data_dict])
    prediction = make_prediction(data_df)
    add_database(data, prediction)
    return {'predict': prediction[0]}


def add_database(data, prediction):
    db_item = LoanApplication(**data.dict(), loan_eligibile=prediction[0])
    db.add(db_item)
    db.commit()
    db.refresh(db_item)


if __name__ == '__main__':
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)

