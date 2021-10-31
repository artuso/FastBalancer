from routes.accessibility import accessibility
from dotenv import dotenv_values
from routes.stand import stand
from fastapi import FastAPI

from config.db import DB


def start_app():
    fa = FastAPI()
    fa.include_router(stand)
    fa.include_router(accessibility)
    return fa


config = dotenv_values(".env")
app = start_app()
db = DB(host=config["MONGO_HOST"], port=config["MONGO_PORT"], db=config["MONGO_DB"])


