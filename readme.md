# City Management API

## Overview
This project consists of a RESTful API in Python that provides CRUD functionality for managing cities and their alliances. It includes models for City data and City alliances, using SQLAlchemy for database interactions and FastAPI for the web framework.

## Features
- CRUD operations for City data.
- Managing bidirectional city alliances.
- Calculating allied power based on city population and distance.

## Requirements
- Python
- FastAPI
- SQLAlchemy
- Psycopg
- PostgreSQL
- Docker

## Running the Application

### Using Docker 

1. To run the application using Docker Compose with a preconfigured PostgreSQL database:
    ```bash
    docker-compose up --build
    ```
    This will start the API service on `localhost:8080` and the PostgreSQL database.

2. To build and run the application directly with Docker:
    ```bash
    docker build -t city-api .
    docker run -p 8080:1337 city-api
    ```
   Make sure to set the environment varaibles before running the docker

## Configuration
The API uses environment variables for configuration. Make sure to set the following:
- `PGHOST`
- `PGPORT`
- `PGUSER`
- `PGPASSWORD`
- `PGDATABASE`

## API Endpoints
- `POST cities/`: Create a new city.
- `GET cities/`: Retrieve all cities with pagination.
- `GET cities/{city_uuid}`: Retrieve a single city by UUID.
- `PATCH cities/{city_uuid}`: Update a city by UUID.
- `DELETE cities/{city_uuid}`: Delete a city by UUID.

## API Docs
- Swagger UI (Interactive Documentation): http://localhost:8080/docs
    - Explore available API endpoints.
    - Send test requests to the API.
    - View detailed information about each endpoint and its parameters.

- ReDoc (Human-Readable Documentation): http://localhost:8080/redoc
    - Access clear and well-structured API documentation.
   - Understand API endpoints, request payloads, and responses in a user-friendly format.

## API Constraints

- **City Name**:
  - Type: String
  - Constraints: 3 to 100 characters, only letters and spaces allowed.

- **Geo-Location Latitude**:
  - Type: Float
  - Constraints: Range -90.0 to 90.0, maximum of 6 decimal places.

- **Geo-Location Longitude**:
  - Type: Float
  - Constraints: Range -180.0 to 180.0, maximum of 6 decimal places.

- **Beauty**:
  - Type: Enum (BeautyEnum)
  - Values: 'Ugly', 'Average', 'Gorgeous'.

- **Population**:
  - Type: Integer
  - Constraints: Range from 1 to 1 billion.


## Database Schema
```sql
CREATE TYPE beauty_type AS ENUM ('Ugly', 'Average', 'Gorgeous');

CREATE TABLE city (
    city_uuid UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    name VARCHAR NOT NULL,
    geo_location_latitude FLOAT NOT NULL,
    geo_location_longitude FLOAT NOT NULL,
    beauty beauty_type NOT NULL,
    population BIGINT NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE city_alliances (
    alliance_id SERIAL PRIMARY KEY,
    city_uuid UUID REFERENCES city(city_uuid) NOT NULL,
    allied_city_uuid UUID REFERENCES city(city_uuid) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

## Additional Information
For any additional concerns or specific implementation details, please refer to the provided classes.

## Security Audit Report

### Bandit Report

Last scanned: `2024-01-07`

#### Summary
- **Python Version**: 3.10.11
- **Total Lines of Code**: 689
- **Total Lines Skipped** (`#nosec`): 0

#### Issues by Severity
- **Undefined**: 0
- **Low**: 0
- **Medium**: 0
- **High**: 0

#### Issues by Confidence
- **Undefined**: 0
- **Low**: 0
- **Medium**: 0
- **High**: 0

#### Conclusion
No security issues identified in the current codebase.


# Task Results

The `tasks` folder contains test cities and code for the execution, which generated the following results:

## City Creation Results

- **Berlin Created**: 
```json
{
'name': 'Berlin',
'geo_location_latitude': 52.52001,
'geo_location_longitude': 13.40495,
'beauty': 'Gorgeous',
'population': 3645000,
'city_uuid': '7e8bafc6-e481-4885-85b2-c3d79ccbf355',
'alliances': []
}
```
- **New York Created**:
```json
{
'name': 'New York',
'geo_location_latitude': 40.71278,
'geo_location_longitude': -74.00594,
'beauty': 'Gorgeous',
'population': 8419000,
'city_uuid': '4020fb51-27c9-4d02-9928-532d8e2631c0',
'alliances': [{'allied_city_uuid': '7e8bafc6-e481-4885-85b2-c3d79ccbf355'}]
}
```
- **Munich Created**: 
```json
{
'name': 'Munich',
'geo_location_latitude': 48.13512,
'geo_location_longitude': 11.58198,
'beauty': 'Gorgeous',
'population': 1472000,
'city_uuid': '2c1a751d-4d92-4828-ad93-7870f374dc6d',
'alliances': [{'allied_city_uuid': '7e8bafc6-e481-4885-85b2-c3d79ccbf355'}]
}
```

## State of Each City After Initial Creation

| City      | Alliances         |
|-----------|-------------------|
| Berlin    | New York, Munich  |
| New York  | Berlin            |
| Munich    | Berlin            |

## State of Each City After Updating New York's Alliances

| City      | Alliances             |
|-----------|-----------------------|
| Berlin    | Munich                |
| New York  | Munich                |
| Munich    | Berlin, New York      |
