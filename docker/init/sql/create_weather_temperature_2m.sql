CREATE SEQUENCE auto_increment;

CREATE TABLE temperature_2m (
    id SERIAL PRIMARY KEY,
    hash VARCHAR(255) NOT NULL,
    datetime TIMESTAMP NOT NULL,
    temperature VARCHAR(255) NOT NULL,
    latitude FLOAT NOT NULL,
    longitude FLOAT NOT NULL,
    elevation FLOAT,
    timezone_abbreviation VARCHAR(70),
    timezone VARCHAR(70)
);