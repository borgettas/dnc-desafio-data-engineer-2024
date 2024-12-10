import os
import pandas as pd
import requests

from commons.postgres.postgres import create_connection
from commons.ingestion.hash import generate_hash
from datetime import datetime


def get_directions(
    destination: str
    , origin: str
):
    try:
        url= f"https://maps.googleapis.com/maps/api/directions/json?destination={destination}&origin={origin}&key={os.environ.get('POSTGRES_DW_GOOGLE_API_KEY')}"
        response = requests.get(url)
    except requests.exceptions.RequestException as e:
        raise e

    response_json= response.json()
    
    if response_json['status'] == 'NOT_FOUND': raise Exception('Not Found Results')
    
    base_dataframe = {
        'northeast_lat': [response_json['routes'][0]['bounds']['northeast']['lat']]
        , 'northeast_lng': [response_json['routes'][0]['bounds']['northeast']['lng']]
        , 'southwest_lat': [response_json['routes'][0]['bounds']['southwest']['lat']]
        , 'southwest_lng': [response_json['routes'][0]['bounds']['southwest']['lng']]
        , 'distance': [response_json['routes'][0]['legs'][0]['distance']['value']]
        , 'duration': [response_json['routes'][0]['legs'][0]['duration']['value']]
        , 'start_address': [response_json['routes'][0]['legs'][0]['start_address']]
        , 'end_address': [response_json['routes'][0]['legs'][0]['end_address']]
    }
    
    df = pd.DataFrame(data= base_dataframe)
    df['ingested_at']= datetime.now()
    
    df['id']= (df['start_address']+df['end_address']).apply(generate_hash)
    
    try:
        df.to_sql(
            'google_direction'
            , create_connection(
                user=os.environ.get('POSTGRES_DW_USER')
                , password=os.environ.get('POSTGRES_DW_PASSWORD')
                , port=os.environ.get('POSTGRES_DW_PORT')
                , host=os.environ.get('POSTGRES_DW_HOST')
            )
            , if_exists='replace'
            , index=False
        )
        print("Dados inseridos com sucesso")
    except Exception as e:
        raise e
