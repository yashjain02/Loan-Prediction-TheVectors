from datetime import datetime, timedelta
from airflow import DAG
from airflow.models import Variable
from airflow.operators.bash_operator import BashOperator

try:
    from airflow.operators import LivyBatchOperator
except ImportError:
    from airflow.batch import LivyBatchOperator

# Define configured variables to connect to AWS S3 and Redshift
main_file_path = Variable.get("C:\Users\KOMAL\Documents\airflow\notebook\loan_prediction_final.ipynb")
pyfiles_path = Variable.get("C:\Users\KOMAL\Documents\airflow\loan_prediction\inference.py")

# Default settings for DAG
default_args = {
    'owner': 'Komal',
    'depends_on_past': False,
    'start_date': datetime.today(),
    'retries': 5,
    'retry_delay': timedelta(minutes=1),
}

with DAG(dag_id='loan_prediction_model_predict', default_args=default_args,
         description='"Run Spark job via Livy Batches \
                      to preprocess data and train model',
         schedule_interval='@once') as dag:

    preprocess_data_step = LivyBatchOperator(
        name="preprocess_data_{{ run_id }}",
        file=main_file_path,
        py_files=[pyfiles_path],
        task_id="preprocess_data"
    )

    model_predict_step = LivyBatchOperator(
        name="model_predict_{{ run_id }}",
        file=main_file_path,
        py_files=[pyfiles_path],
        task_id="model_predict"
    )

    preprocess_data_step >> model_predict_step