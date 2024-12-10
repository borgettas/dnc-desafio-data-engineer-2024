import psycopg2
from sqlalchemy import create_engine


def create_connection(
    user:       str
    , password: str
    , dbname:   str= 'postgres'
    , host:     str= 'localhost'
    , port:     int= 5432
):
    connection_string = f'postgresql+psycopg2://{user}:{password}@{host}:{port}/{dbname}'

    try:
        return create_engine(connection_string)
    except Exception as e:
        print(f"Error connecting to the database: {e}")