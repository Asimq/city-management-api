import logging
from os import environ

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session
from sqlalchemy.ext.declarative import declarative_base

import config.db_engine_config as engine_config


# Function to get environment variable or raise error
def get_env_variable(var_name):
    try:
        return environ[var_name]
    except KeyError:
        logging.error(f"Environment variable {var_name} not found")
        raise EnvironmentError(f"Environment variable {var_name} not found")


# Construct DATABASE_URL from environment variables
DATABASE_URL = (
    f"postgresql+psycopg2://{get_env_variable('PGUSER')}:"
    f"{get_env_variable('PGPASSWORD')}@{get_env_variable('PGHOST')}:"
    f"{get_env_variable('PGPORT')}/{get_env_variable('PGDATABASE')}"
)

# SQLAlchemy engine creation with connection pooling and keepalive parameters
engine = create_engine(
    DATABASE_URL,
    pool_pre_ping=engine_config.POOL_PRE_PING,
    pool_recycle=engine_config.POOL_RECYCLE,
    connect_args={
        "keepalives": engine_config.KEEPALIVES,
        "keepalives_idle": engine_config.KEEPALIVES_IDLE,
        "keepalives_interval": engine_config.KEEPALIVES_INTERVAL,
        "keepalives_count": engine_config.KEEPALIVES_COUNT,
    }
)

# Session factory for creating new SQLAlchemy session instances
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base class for declarative class definitions
Base = declarative_base()

def get_engine():
    """
    Retrieve the SQLAlchemy engine.

    Returns:
        The SQLAlchemy engine connected to the database.
    """
    return engine

def get_db() -> Session:
    """
    Generator function that provides a database session and ensures its closure.

    Yields:
        A SQLAlchemy Session object.
    """
    db = SessionLocal()
    try:
        yield db
    except Exception as e:
        logging.error(f"Database connection error occurred: {e}")
        raise
    finally:
        db.close()
