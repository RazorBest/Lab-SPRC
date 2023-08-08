#!/bin/bash
set -e

psql -v ON_ERROR_STOP=1 --username "$POSTGRES_USER" --dbname "$POSTGRES_DB" <<-EOSQL
    CREATE TABLE IF NOT EXISTS countries (
        id SERIAL PRIMARY KEY,
        name VARCHAR(64) UNIQUE NOT NULL,
        latitude DOUBLE PRECISION,
        longitude DOUBLE PRECISION
    );
    CREATE TABLE IF NOT EXISTS cities (
        id SERIAL PRIMARY KEY,
        country_id INT NOT NULL,
        name VARCHAR(64) NOT NULL,
        latitude DOUBLE PRECISION,
        longitude DOUBLE PRECISION,
        UNIQUE (country_id, name),
        CONSTRAINT fk_country
            FOREIGN KEY(country_id)
                REFERENCES countries(id)
    );
    CREATE TABLE IF NOT EXISTS temperatures (
        id SERIAL PRIMARY KEY,
        timestamp TIMESTAMP,
        value DOUBLE PRECISION,
        city_id INT NOT NULL,
        UNIQUE (city_id, timestamp),
        CONSTRAINT fk_city
            FOREIGN KEY(city_id)
                REFERENCES cities(id)
    );
    CREATE INDEX temperature_time_index ON temperatures (timestamp);
EOSQL
