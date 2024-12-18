import os
import openmeteo_requests
import pandas as pd
import requests_cache

from commons.postgres.postgres import create_connection
from commons.ingestion.hash import generate_hash
from commons.ingestion.normalization import treat_cols_with_null_values_to_zero
from datetime import datetime
from retry_requests import retry


def ingestion_hourly(
        latitude: float
        , longitude: float
        , start_date: float
        , end_date: float
        , tablename: str
        , category: str
    ):
    cache_session = requests_cache.CachedSession('.cache', expire_after = 3600)
    retry_session = retry(cache_session, retries = 5, backoff_factor = 0.2)
    openmeteo = openmeteo_requests.Client(session = retry_session)
    url = "https://api.open-meteo.com/v1/forecast"

    # SJCampos
    params = {
        "latitude": latitude,
        "longitude": longitude,
        "start_date": start_date,
        "end_date": end_date,
        "hourly": category
    }
    responses = openmeteo.weather_api(url, params=params)

    for response in responses:
        hourly = response.Hourly()
        hourly_temperature_2m = hourly.Variables(0).ValuesAsNumpy()

        hourly_data = {
            "datetime": pd.date_range(
                start = pd.to_datetime(hourly.Time(), unit = "s", utc = True),
                end = pd.to_datetime(hourly.TimeEnd(), unit = "s", utc = True),
                freq = pd.Timedelta(seconds = hourly.Interval()),
                inclusive = "left"
            )
        }
        hourly_data["temperature"] = hourly_temperature_2m

        df = pd.DataFrame(data = hourly_data)

        df['latitude']= response.Latitude()
        df['longitude']= response.Longitude()
        df['elevation']= response.Elevation()
        df['timezone_abbeviation']= response.TimezoneAbbreviation()
        df['timezone']= response.Timezone()
        df['hash'] = df['datetime'].apply(generate_hash)
        df['ingested_at']= datetime.now()
        
        
        # normalizations
        df = treat_cols_with_null_values_to_zero(df, ['temperature', 'latitude', 'longitude', 'elevation'])
        
        
        # save
        try:
            df.to_sql(
                tablename
                , create_connection(
                    user=os.getenv('POSTGRES_DW_USER')
                    , password=os.getenv('POSTGRES_DW_PASSWORD')
                    , port=os.getenv('POSTGRES_DW_PORT')
                    , host=str(os.getenv('POSTGRES_DW_HOST'))
                )
                , if_exists='replace'
                , index=False
            )
            print("Dados inseridos com sucesso")
        except Exception as e:
            raise e