CREATE SEQUENCE auto_increment;

CREATE TABLE google_direction (
    id VARCHAR(255) PRIMARY KEY,
    northeast_lat FLOAT NOT NULL,
    northeast_lng FLOAT NOT NULL,
    southwest_lat FLOAT NOT NULL,
    southwest_lng FLOAT NOT NULL,
    distance FLOAT,
    duration INTEGER,
    end_address VARCHAR(255) NOT NULL,
    start_address VARCHAR(255) NOT NULL,
    ingested_at TIMESTAMP NOT NULL
);


CREATE TABLE temperature_2m (
    id SERIAL PRIMARY KEY,
    hash VARCHAR(255) NOT NULL,
    datetime TIMESTAMP NOT NULL,
    temperature VARCHAR(255) NOT NULL,
    latitude FLOAT NOT NULL,
    longitude FLOAT NOT NULL,
    elevation FLOAT,
    timezone_abbreviation VARCHAR(70),
    timezone VARCHAR(70),
    ingested_at TIMESTAMP NOT NULL
);