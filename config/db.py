from dotenv import dotenv_values
from pymongo import MongoClient
import json

config = dotenv_values(".env")


class DB:

    def __init__(self, host=config["MONGO_HOST"], port=config["MONGO_PORT"], db=config["MONGO_DB"],
                 user=config["MONGO_USER"], password=config["MONGO_PASSWORD"]):
        if user == '':
            link = f"mongodb://{host}:{port}/{db}"
        else:
            link = f"mongodb://{user}:{password}@{host}:{port}/{db}"
        self.connection = MongoClient(link)

    def clear_stand_document(self):
        self.connection.appium.stand.delete_many({})

    def add_defaults_stands(self, file_name):
        with open(f'./config/{file_name}') as json_file:
            data = json.load(json_file)
            for stand in data:
                stand.update({"available": True})
                self.connection.appium.stand.insert_one(dict(stand))





