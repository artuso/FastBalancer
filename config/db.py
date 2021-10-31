from pymongo import MongoClient
import mongomock
import json
import os


class DB:

    def __init__(self, host="localhost", port="27017", db="appium", user=None, password=None):
        #os.environ["TESTING"] = "1"
        if "TESTING" not in os.environ:
            if user is None:
                link = f"mongodb://{host}:{port}/{db}"
            else:
                link = f"mongodb://{user}:{password}@{host}:{port}/{db}"
            self.connection = MongoClient(link)
        elif int(os.environ.get("TESTING")):
            self.connection = mongomock.MongoClient(f"mongodb://{host}:{port}/{db}_test")

        self.connection.appium.stand.delete_many({})

        with open('./config/stands.json') as json_file:
            data = json.load(json_file)
            for stand in data:
                stand.update({"available": True})
                self.connection.appium.stand.insert_one(dict(stand))





