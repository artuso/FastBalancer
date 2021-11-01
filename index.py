from routes.accessibility import accessibility
from routes.stand import stand
from fastapi import FastAPI
from config.db import DB
import os


def start_app():
    fa = FastAPI()
    routes_collection = [stand, accessibility]
    for rout in routes_collection:
        fa.include_router(rout)
    return fa


app = start_app()
db = DB()
db.clear_stand_document()
if "TESTING" not in os.environ:
    db.add_defaults_stands('main_stands.json')
else:
    db.add_defaults_stands('test_stands.json')
