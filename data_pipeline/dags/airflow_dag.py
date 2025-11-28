from airflow import DAG
from airflow.operators.bash import BashOperator
from datetime import datetime, timedelta
import os

# Define paths
# Using absolute paths for reliability in this specific environment
BASE_DIR = "c:/Users/user/Desktop/Kabarak_Lost_And_Found"
SCRIPT_PATH = os.path.join(BASE_DIR, "data_pipeline/scripts/spark_processor.py")
JAR_PATH = os.path.join(BASE_DIR, "database/postgresql-42.7.8.jar")

default_args = {
    'owner': 'kabarak',
    'depends_on_past': False,
    'email_on_failure': False,
    'email_on_retry': False,
    'retries': 1,
    'retry_delay': timedelta(minutes=5),
}

with DAG(
    'kabarak_lost_found_analytics',
    default_args=default_args,
    description='Daily analytics for Kabarak Lost and Found items',
    schedule_interval='@daily',
    start_date=datetime(2023, 1, 1),
    catchup=False,
    tags=['kabarak', 'analytics', 'spark'],
) as dag:

    # Task to run the Spark processor script
    run_spark_job = BashOperator(
        task_id='run_spark_processor',
        bash_command=f'spark-submit --jars "{JAR_PATH}" "{SCRIPT_PATH}"'
    )

    run_spark_job
