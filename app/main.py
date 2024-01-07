from fastapi import FastAPI

from config.log_config import setup_logging
from routers import city_router

setup_logging()

app = FastAPI()

app.include_router(city_router.router, prefix="/cities", tags=["cities"])
