# City Management API

## Overview
This project consists of a RESTful API in Python that provides CRUD functionality for managing cities and their alliances. It includes models for City data and City alliances, using SQLAlchemy for database interactions and FastAPI for the web framework.

## Features
- CRUD operations for City data.
- Managing city alliances.
- Calculating allied power based on city population and distance.

## Requirements
- Python
- FastAPI
- SQLAlchemy
- PostgreSQL
- Docker

## Running the Application

### Using Docker
Ensure Docker and Docker Compose are installed on your machine. 

1. To build and run the application directly with Docker:
    ```bash
    docker build -t city-api .
    docker run -p 1337:1337 city-api
    ```

2. To run the application using Docker Compose with a preconfigured PostgreSQL database:
    ```bash
    docker-compose up
    ```
    This will start the API service on `localhost:8080` and the PostgreSQL database.

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

## Configuration
The API uses environment variables for configuration. Make sure to set the following:
- `PGHOST`
- `PGPORT`
- `PGUSER`
- `PGPASSWORD`
- `PGDATABASE`

## Database Schema
```sql
CREATE TYPE beauty_type AS ENUM ('Ugly', 'Average', 'Gorgeous');

CREATE TABLE city (
    city_uuid UUID PRIMARY KEY,
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
For any additional concerns or specific implementation details, please refer to the provided classes and the assessment task description.
