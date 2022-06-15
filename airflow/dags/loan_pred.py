from datetime import datetime
from datetime import timedelta

import pandas as pd
from airflow.decorators import dag, task
from pendulum import today
from inference import make_prediction as pred


@dag(
    dag_id="loan_pred",
    description="Ingest data from a file to another DAG",
    tags=["example"],
    default_args={'owner': 'airflow'},
    schedule_interval=timedelta(minutes=1),
    start_date=today().add(hours=-1)
)
def loan_pred():
    @task
    def get_data_to_ingest_from_local_file_task():
        return get_data_to_ingest_from_local_file()

    @task
    def make_prediction():
        return make_prediction()

    @task
    def save_data_task(data_to_ingest_df):
        save_data(data_to_ingest_df)

    # Task relationships
    data_to_ingest = get_data_to_ingest_from_local_file_task()
    make_predict = make_prediction(data_to_ingest)
    save_data_task(make_predict)


ingest_data_dag = loan_pred()


#####
def get_data_to_ingest_from_local_file():
    input_data_df = pd.read_csv("input_data/test_loan_pred.csv")
    data_to_ingest_df = input_data_df.sample(n=5)
    return data_to_ingest_df


def make_pred(data_to_ingest_df):
    predict = pred(data_to_ingest_df)
    return predict


def save_data(make_pred_df):
    filepath = f"output_data/{datetime.now()}.csv"
    make_pred_df.to_csv(filepath, index=False)
