from schemas.serialize import serialize_dict, serialize_list
from models.stand import Stand, StandUpdate
from fastapi import APIRouter
from bson import ObjectId
import index as app

stand = APIRouter()


@stand.get('/stands')
async def find_all_stands():
    return serialize_list(app.db.connection.appium.stand.find())


@stand.get('/stand/{id}')
async def find_stand(id: str):
    return serialize_dict(app.db.connection.appium.stand.find_one({"_id": ObjectId(id)}))


@stand.post('/stand')
async def create_stand(stand: Stand):
    result = app.db.connection.appium.stand.insert_one(dict(stand))
    print(result)
    return serialize_list(app.db.connection.appium.stand.find())


@stand.put('/stand/{id}')
async def update_stand(id: str, stand: Stand):
    app.db.connection.appium.stand.find_one_and_update({"_id": ObjectId(id)}, {"$set": dict(stand)})
    return serialize_dict(app.db.connection.appium.stand.find_one({"_id": ObjectId(id)}))


@stand.patch('/stand/{id}')
async def update_stand(id: str, update_data: StandUpdate):
    update_data = dict(update_data)
    stand_data = serialize_dict(app.db.connection.appium.stand.find_one({"_id": ObjectId(id)}))
    stand_data.pop("_id")
    for item in update_data:
        if update_data[item] is not None:
            stand_data[item] = update_data[item]
    app.db.connection.appium.stand.update_one({"_id": ObjectId(id)}, {"$set": stand_data})
    return serialize_dict(app.db.connection.appium.stand.find_one({"_id": ObjectId(id)}))


@stand.delete('/stand/{id}')
async def delete_stand(id: str):
    return serialize_dict(app.db.connection.appium.stand.find_one_and_delete({"_id": ObjectId(id)}))


