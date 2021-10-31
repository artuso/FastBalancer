from schemas.serialize import serialize_dict, serialize_list
from fastapi import APIRouter
from bson import ObjectId
import index as app

accessibility = APIRouter()

messages = {
    "all_busy": {"message": "All the stands are busy", "no_stands_available": True},
    "all_available": {"message": "All the stands are available", "no_stands_available": False}
}


@accessibility.get('/get_available_stand')
async def get_available_stand(platform: str):
    stands = serialize_list(app.db.connection.appium.stand.find({"available": True, "platform": platform}, limit=1))
    if len(stands) != 0:
        app.db.connection.appium.stand.update_one({"_id": ObjectId(stands[0]["_id"])}, {"$set": {"available": False}})
        return serialize_dict(app.db.connection.appium.stand.find_one({"_id": ObjectId(stands[0]["_id"])}))
    else:
        return messages["all_busy"]


@accessibility.get('/take_over_all_stands')
async def take_over_all_stands(platform: str):
    stands = serialize_list(app.db.connection.appium.stand.find({"available": True, "platform": platform}))
    if len(stands) != 0:
        for stand in stands:
            app.db.connection.appium.stand.update_one({"_id": ObjectId(stand["_id"])}, {"$set": {"available": False}})
        return serialize_list(app.db.connection.appium.stand.find({"platform": platform}))
    else:
        return messages["all_busy"]


@accessibility.get('/vacate_all_stands')
async def vacate_all_stands(platform: str):
    stands = serialize_list(app.db.connection.appium.stand.find({"available": False, "platform": platform}))
    if len(stands) != 0:
        for stand in stands:
            app.db.connection.appium.stand.update_one({"_id": ObjectId(stand["_id"])}, {"$set": {"available": True}})
        return serialize_list(app.db.connection.appium.stand.find({"platform": platform}))
    else:
        return messages["all_available"]


