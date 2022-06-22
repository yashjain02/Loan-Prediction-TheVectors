from datetime import datetime
from datetime import timedelta
import pandas as pd
from airflow.decorators import dag, task
from pendulum import today
import preprocessing as p
import joblib as job

@dag(
    dag_id="loan_predict",
    description="Loan Prediction",
    tags=["loan"],
    default_args={'owner': 'airflow'},
    schedule_interval=timedelta(days=1),
    start_date=today().add(hours=-1)
)
def loan_prediction():
    @task
    def get_data_to_ingest_from_local_file_task():
        return get_data_to_ingest_from_local_file()

    @task
    def save_data_task(data_to_ingest_df):
        save_data(data_to_ingest_df)

    # Task relationships
    data_to_ingest = get_data_to_ingest_from_local_file_task()
    save_data_task(data_to_ingest)


ingest_data_dag = loan_prediction()


def get_data_to_ingest_from_local_file():
    input_data_df = pd.read_csv("input_data/test_loan_pred.csv")
    data_to_ingest_df = input_data_df.sample(n=5)
    return data_to_ingest_df


def save_data(data_to_ingest_df):
    def make_prediction(test):
        test = p.fill_missing(test)
        test = p.model_preprocessing(test)
        model = job.load("model")
        final_prediction = model.predict(test)
        return final_prediction
    data_to_ingest_df = make_prediction(data_to_ingest_df)
    filepath = f"output_data/{datetime.now()}.csv"
    pd.DataFrame(data_to_ingest_df).to_csv(filepath, index=False)
