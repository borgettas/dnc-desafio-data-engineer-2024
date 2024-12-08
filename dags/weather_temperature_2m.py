from airflow import DAG
from airflow.operators.python import PythonOperator
from commons.open_meteo.temperature_2m import ingestion_temperature_2m
from datetime import date, datetime, timedelta


with DAG(
    dag_id= 'weather_temperature_2m',
    default_args= {
        'owner': 'dnc',
        'depends_on_past': False,
    },
    catchup= False,
    tags= ['weather', 'ingestion', 'temperature_2m'],
    max_active_runs= 1,
):

    sao_jose_dos_campos = PythonOperator(
        task_id= 'sao_jose_dos_campos'
        , python_callable= ingestion_temperature_2m
        , op_kwargs= {
            "latitude": -23.1794,
            "longitude": -45.8869,
            "start_date": date.today() - timedelta(days=7),
            "end_date": date.today()
        }
    )
