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