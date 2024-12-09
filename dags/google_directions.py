from airflow import DAG
from airflow.operators.python import PythonOperator
from commons.google.directions.get import get_directions
from datetime import date, datetime, timedelta


with DAG(
    dag_id= 'google_directions',
    default_args= {
        'owner': 'dnc',
        'depends_on_past': False,
    },
    catchup= False,
    tags= ['google', 'directions', 'ingestion'],
    max_active_runs= 1,
):
    campinas_sp = PythonOperator(
        task_id= 'campinas_sp'
        , python_callable= get_directions
        , op_kwargs= {
            "origin": "Campinas",
            "destination": "São Paulo"
        }
    )