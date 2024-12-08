from airflow import DAG
from airflow.operators.python import PythonOperator

# from airflow.providers.standard.operators.python import (
#     # ExternalPythonOperator,
#     PythonOperator,
#     # PythonVirtualenvOperator,
# )
import datetime
import openmeteo_requests
import pandas as pd
import requests_cache

from retry_requests import retry


def ingestion_weather():
    # Setup the Open-Meteo API client with cache and retry on error
    cache_session = requests_cache.CachedSession('.cache', expire_after = 3600)
    retry_session = retry(cache_session, retries = 5, backoff_factor = 0.2)
    openmeteo = openmeteo_requests.Client(session = retry_session)

    # Make sure all required weather variables are listed here
    # The order of variables in hourly or daily is important to assign them correctly below
    url = "https://api.open-meteo.com/v1/forecast"

    # SJCampos
    params = {
        "latitude": -23.1794,
        "longitude": -45.8869,
        "start_date": "2020-01-01",
        "end_date": "2024-11-30",
        "hourly": "temperature_2m"
    }
    responses = openmeteo.weather_api(url, params=params)

    # Process first location. Add a for-loop for multiple locations or weather models
    response = responses[0]
    print(f"Coordinates {response.Latitude()}°N {response.Longitude()}°E")
    print(f"Elevation {response.Elevation()} m asl")
    print(f"Timezone {response.Timezone()} {response.TimezoneAbbreviation()}")
    print(f"Timezone difference to GMT+0 {response.UtcOffsetSeconds()} s")

    # Process hourly data. The order of variables needs to be the same as requested.
    hourly = response.Hourly()
    hourly_temperature_2m = hourly.Variables(0).ValuesAsNumpy()

    hourly_data = {
        "date": pd.date_range(
            start = pd.to_datetime(hourly.Time(), unit = "s", utc = True),
            end = pd.to_datetime(hourly.TimeEnd(), unit = "s", utc = True),
            freq = pd.Timedelta(seconds = hourly.Interval()),
            inclusive = "left"
        )
    }
    hourly_data["temperature_2m"] = hourly_temperature_2m

    hourly_dataframe = pd.DataFrame(data = hourly_data)
    print(hourly_dataframe)


with DAG(
    dag_id= 'weather',
    default_args= {
        'owner': 'dnc',
        'depends_on_past': False,
    },
    catchup= False,
    tags= ['weather', 'ingestion'],
    max_active_runs= 1,
):

    sao_jose_dos_campos = PythonOperator(
        task_id= 'sao_jose_dos_campos'
        , python_callable= ingestion_weather
        # , op_kwargs= {"random_base": i / 10}
    )
